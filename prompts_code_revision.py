"""
LLM Prompt Templates for Code Revision
Structured prompts for updating existing applications
"""

from typing import Dict, List


def generate_revision_prompt(
    existing_code: str,
    new_brief: str,
    new_checks: List[str],
    new_attachments: List[Dict]
) -> str:
    """
    Generate prompt for revising existing application
    
    Args:
        existing_code: Current HTML code from Round 1
        new_brief: New requirements for Round 2
        new_checks: New evaluation checks
        new_attachments: New attachments (if any)
    
    Returns:
        Formatted prompt string
    """
    
    # Format new attachments section
    attachments_section = ""
    if new_attachments:
        attachments_section = "\n\n## NEW ATTACHMENTS\n"
        for att in new_attachments:
            attachments_section += f"- **{att['name']}**: {att['url'][:100]}...\n"
    
    # Format new checks section
    checks_section = ""
    if new_checks:
        checks_section = "\n\n## NEW EVALUATION CHECKS\nThe updated code must pass:\n"
        for i, check in enumerate(new_checks, 1):
            checks_section += f"{i}. {check}\n"
    
    prompt = f"""You are an expert web developer tasked with updating an existing application.

## EXISTING CODE (Round 1)
```html
{existing_code}
```

## NEW REQUIREMENTS (Round 2)
{new_brief}
{attachments_section}
{checks_section}

## REVISION INSTRUCTIONS

1. **Preserve Existing Functionality**: Keep all features from Round 1 working
2. **Add New Features**: Implement the new requirements from the brief
3. **Maintain Code Quality**: Ensure clean, well-commented code
4. **Update Inline**: Modify the existing HTML structure rather than rewriting from scratch
5. **Test Compatibility**: Ensure new features don't break existing ones
6. **Keep Single File**: Maintain the single-file HTML structure

## WHAT TO MODIFY

- Add new HTML elements as needed
- Update CSS styles for new features
- Extend JavaScript functionality
- Integrate new attachments if provided
- Ensure all new checks will pass

## WHAT TO PRESERVE

- Existing UI elements and their IDs/classes
- Original functionality and behavior
- Bootstrap and other CDN links
- Overall application structure

## OUTPUT FORMAT

Provide ONLY the complete UPDATED HTML code. Do not include explanations.
Start directly with:
```html
<!DOCTYPE html>
<html lang="en">
...
```

The updated code should be a complete, working application that includes BOTH the original features AND the new requirements.

Now generate the complete updated HTML code."""

    return prompt


def generate_readme_update_prompt(
    existing_readme: str,
    new_brief: str,
    new_checks: List[str]
) -> str:
    """
    Generate prompt for updating README.md
    
    Args:
        existing_readme: Current README content
        new_brief: New requirements
        new_checks: New evaluation checks
    
    Returns:
        Formatted prompt for README update
    """
    
    checks_section = ""
    if new_checks:
        checks_section = "\n\n**New Features Added:**\n"
        for check in new_checks:
            checks_section += f"- {check}\n"
    
    prompt = f"""Update the existing README.md to reflect new features added in Round 2.

## EXISTING README
```markdown
{existing_readme}
```

## NEW FEATURES (Round 2)
{new_brief}
{checks_section}

## UPDATE INSTRUCTIONS

1. **Preserve Existing Content**: Keep all Round 1 information
2. **Add New Features**: Update the Features section with Round 2 additions
3. **Update Usage**: Extend usage instructions for new functionality
4. **Maintain Structure**: Keep the same section organization
5. **Professional Tone**: Ensure clarity and completeness

## OUTPUT FORMAT

Provide ONLY the complete UPDATED markdown content. Start directly with:
```markdown
# Project Title
...
```

Generate the updated README.md now."""

    return prompt