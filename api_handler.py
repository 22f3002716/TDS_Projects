"""
API Handler Module
Orchestrates the entire build/revise workflow
"""

from typing import Dict, Tuple
from database.models import Database
from modules.llm_integration import LLMIntegration
from modules.github_automation import GitHubAutomation
from modules.evaluation_notifier import EvaluationNotifier
from utils.logger import setup_logger
from utils.validators import validate_request_payload

logger = setup_logger(__name__)


class APIHandler:
    """Main API request handler"""
    
    def __init__(self):
        self.db = Database()
        self.llm = LLMIntegration()
        self.github = GitHubAutomation()
        self.notifier = EvaluationNotifier()
        logger.info("✅ APIHandler initialized")
    
    def process_request(self, payload: Dict) -> Tuple[bool, Dict, str]:
        """
        Process incoming request (Round 1 or Round 2)
        
        Args:
            payload: Request JSON payload
        
        Returns:
            Tuple of (success, response_data, error_message)
        """
        logger.info(f"📥 Processing request for {payload.get('email')} - Round {payload.get('round')}")
        
        # Validate payload
        is_valid, error_msg = validate_request_payload(payload)
        if not is_valid:
            logger.error(f"❌ Validation failed: {error_msg}")
            return False, {}, error_msg
        
        # Save task to database
        try:
            self.db.save_task(payload)
            logger.info("✅ Task saved to database")
        except Exception as e:
            logger.error(f"❌ Database error: {str(e)}")
            return False, {}, f"Database error: {str(e)}"
        
        # Route to appropriate handler
        try:
            if payload['round'] == 1:
                success, response_data = self._handle_build(payload)
            elif payload['round'] == 2:
                success, response_data = self._handle_revise(payload)
            else:
                return False, {}, "Invalid round number"
            
            if not success:
                return False, {}, "Processing failed"
            
            return True, response_data, ""
        
        except Exception as e:
            logger.error(f"❌ Request processing failed: {str(e)}")
            return False, {}, str(e)
    
    def _handle_build(self, payload: Dict) -> Tuple[bool, Dict]:
        """
        Handle Round 1: Build new application
        
        Args:
            payload: Request payload
        
        Returns:
            Tuple of (success, response_data)
        """
        logger.info("🔨 Starting Round 1: BUILD")
        
        try:
            # Step 1: Generate code using LLM
            logger.info("Step 1/4: Generating code with LLM...")
            html_code, readme_content = self.llm.generate_application_code(
                brief=payload['brief'],
                checks=payload.get('checks', []),
                attachments=payload.get('attachments', [])
            )
            
            # Validate HTML structure
            if not self.llm.validate_html_structure(html_code):
                raise ValueError("Generated HTML has invalid structure")
            
            # Step 2: Create GitHub repository and deploy
            logger.info("Step 2/4: Creating GitHub repository...")
            github_result = self.github.create_or_update_repo(
                task_id=payload['task'],
                html_code=html_code,
                readme_content=readme_content,
                is_update=False
            )
            
            # Step 3: Save deployment to database
            logger.info("Step 3/4: Saving deployment info...")
            deployment_data = {
                'email': payload['email'],
                'task': payload['task'],
                'round': payload['round'],
                'nonce': payload['nonce'],
                'repo_url': github_result['repo_url'],
                'commit_sha': github_result['commit_sha'],
                'pages_url': github_result['pages_url'],
                'code_snapshot': {
                    'html': html_code,
                    'readme': readme_content
                }
            }
            self.db.save_deployment(deployment_data)
            
            # Step 4: Notify evaluation API
            logger.info("Step 4/4: Notifying evaluation API...")
            notification_payload = self.notifier.prepare_payload(
                email=payload['email'],
                task=payload['task'],
                round_num=payload['round'],
                nonce=payload['nonce'],
                repo_url=github_result['repo_url'],
                commit_sha=github_result['commit_sha'],
                pages_url=github_result['pages_url']
            )
            
            notification_success = self.notifier.notify_evaluation_api(
                evaluation_url=payload['evaluation_url'],
                payload=notification_payload
            )
            
            if not notification_success:
                logger.warning("⚠️  Evaluation API notification failed (but deployment succeeded)")
            
            logger.info("✅ Round 1 BUILD completed successfully")
            
            return True, {
                'status': 'success',
                'round': 1,
                'repo_url': github_result['repo_url'],
                'pages_url': github_result['pages_url'],
                'commit_sha': github_result['commit_sha']
            }
        
        except Exception as e:
            logger.error(f"❌ Build failed: {str(e)}")
            return False, {'status': 'error', 'message': str(e)}
    
    def _handle_revise(self, payload: Dict) -> Tuple[bool, Dict]:
        """
        Handle Round 2: Revise existing application
        
        Args:
            payload: Request payload
        
        Returns:
            Tuple of (success, response_data)
        """
        logger.info("🔄 Starting Round 2: REVISE")
        
        try:
            # Step 1: Retrieve Round 1 deployment
            logger.info("Step 1/5: Retrieving Round 1 deployment...")
            round1_deployment = self.db.get_deployment(
                email=payload['email'],
                task_id=payload['task'],
                round=1
            )
            
            if not round1_deployment:
                # Try to fetch from GitHub if not in database
                logger.warning("⚠️  Round 1 not in database, fetching from GitHub...")
                repo_files = self.github.get_repo_files(payload['task'])
                
                if not repo_files:
                    raise ValueError("Round 1 deployment not found in database or GitHub")
                
                existing_html = repo_files['html_code']
                existing_readme = repo_files['readme_content']
            else:
                code_snapshot = round1_deployment['code_snapshot']
                existing_html = code_snapshot.get('html', '')
                existing_readme = code_snapshot.get('readme', '')
            
            # Step 2: Generate revised code using LLM
            logger.info("Step 2/5: Generating revised code with LLM...")
            updated_html, updated_readme = self.llm.revise_application_code(
                existing_code=existing_html,
                existing_readme=existing_readme,
                new_brief=payload['brief'],
                new_checks=payload.get('checks', []),
                new_attachments=payload.get('attachments', [])
            )
            
            # Validate HTML structure
            if not self.llm.validate_html_structure(updated_html):
                raise ValueError("Updated HTML has invalid structure")
            
            # Step 3: Update GitHub repository
            logger.info("Step 3/5: Updating GitHub repository...")
            github_result = self.github.create_or_update_repo(
                task_id=payload['task'],
                html_code=updated_html,
                readme_content=updated_readme,
                is_update=True
            )
            
            # Step 4: Save Round 2 deployment
            logger.info("Step 4/5: Saving Round 2 deployment...")
            deployment_data = {
                'email': payload['email'],
                'task': payload['task'],
                'round': payload['round'],
                'nonce': payload['nonce'],
                'repo_url': github_result['repo_url'],
                'commit_sha': github_result['commit_sha'],
                'pages_url': github_result['pages_url'],
                'code_snapshot': {
                    'html': updated_html,
                    'readme': updated_readme
                }
            }
            self.db.save_deployment(deployment_data)
            
            # Step 5: Notify evaluation API
            logger.info("Step 5/5: Notifying evaluation API...")
            notification_payload = self.notifier.prepare_payload(
                email=payload['email'],
                task=payload['task'],
                round_num=payload['round'],
                nonce=payload['nonce'],
                repo_url=github_result['repo_url'],
                commit_sha=github_result['commit_sha'],
                pages_url=github_result['pages_url']
            )
            
            notification_success = self.notifier.notify_evaluation_api(
                evaluation_url=payload['evaluation_url'],
                payload=notification_payload
            )
            
            if not notification_success:
                logger.warning("⚠️  Evaluation API notification failed (but deployment succeeded)")
            
            logger.info("✅ Round 2 REVISE completed successfully")
            
            return True, {
                'status': 'success',
                'round': 2,
                'repo_url': github_result['repo_url'],
                'pages_url': github_result['pages_url'],
                'commit_sha': github_result['commit_sha']
            }
        
        except Exception as e:
            logger.error(f"❌ Revision failed: {str(e)}")
            return False, {'status': 'error', 'message': str(e)}