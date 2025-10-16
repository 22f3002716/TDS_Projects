# 🧠 TDS Projects – LLM Code Generator & Evaluation Server

## 📘 Overview
This project provides a lightweight pipeline for **automatic web app generation and evaluation** using Google’s **Gemini API**, along with a minimal **FastAPI echo server** for request testing.

It’s part of a **TDS (Tools for Data Science)** assignment where an AI agent dynamically builds and deploys applications to GitHub Pages or Hugging Face Spaces.

The system consists of:
- **`llm_generator.py`** — the core module that interacts with the **Gemini LLM API** to generate code files dynamically (HTML, JS, etc.) based on a user brief.
- **`app.py`** — a simple **FastAPI** app that echoes incoming POST requests for evaluation or debugging.
- **`Dockerfile`** — a container definition enabling deployment to cloud platforms like Hugging Face Spaces or Docker Hub.

---

## 🧩 Project Structure
```
TDS_PROJECTS/
│
├── llm_generator.py     # Gemini API-based code generation module
├── app.py               # FastAPI echo server for evaluation
├── Dockerfile           # Container definition for deployment
├── .env (optional)      # Stores your GEMINI_API_KEY
└── requirements.txt     # Recommended dependencies (create if missing)
```

---

## ⚙️ llm_generator.py — Gemini-Powered Code Generation

### Purpose
This module automates **web app generation** using the **Gemini 2.5 Flash model**.  
It accepts structured input (brief, checks, attachments) and produces a set of complete files (HTML, CSS, JS, README, LICENSE).

### Key Features
- Uses **Google GenAI SDK (`google.genai`)**
- Validates LLM output via **Pydantic models**
- Automatically decodes and processes **base64 attachments**
- Ensures every generated app includes:
  - `index.html`
  - `README.md`
  - `LICENSE` (MIT License)
- Handles API errors, JSON parsing, and validation gracefully

### Environment Variables
| Variable | Description |
|-----------|-------------|
| `GEMINI_API_KEY` | Your Google Gemini API key (required) |

### Example Usage
```bash
export GEMINI_API_KEY="your_api_key_here"
python llm_generator.py
```

This runs the included **mock test** that sends a small CSV file to Gemini and generates the corresponding web app files.

---

## 🌐 app.py — FastAPI Echo Server

### Purpose
A minimal endpoint to confirm evaluation requests and inspect payloads.

### API Endpoint
| Method | Endpoint | Description |
|---------|-----------|-------------|
| `POST` | `/` | Echoes back the request headers and body |

### Example cURL Test
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```
Then test it:
```bash
curl -X POST http://localhost:8000/ -d "Hello"
```
Expected response:
```json
{
  "method": "POST",
  "headers": {...},
  "body": "Hello"
}
```

---

## 🐳 Dockerfile — Containerized Deployment

### Base Image
Uses a lightweight **Python 3.10+** image to deploy either:
- the **LLM generator service**, or
- the **FastAPI echo server**, depending on your CMD.

### Build and Run Locally
```bash
# Build the image
docker build -t tds_projects .

# Run the container
docker run -p 7860:7860 tds_projects
```

To deploy on **Hugging Face Spaces**, select **Docker** as the SDK type and push this repo directly.

---

## 🧰 Suggested requirements.txt
If not yet present, create a `requirements.txt` containing:
```
fastapi
uvicorn
pydantic
python-dotenv
google-genai
```

---

## 🚀 Deploying to Hugging Face Spaces

1. Create a new **Space** at [huggingface.co/spaces](https://huggingface.co/spaces)
2. Select:
   - SDK: **Docker**
   - Visibility: **Public**
3. Add your **GEMINI_API_KEY** under:  
   `Settings → Secrets → New secret`
4. Push this repository:
   ```bash
   git remote add origin https://huggingface.co/spaces/<username>/tds-projects
   git push origin main
   ```
5. Hugging Face will automatically build and deploy your app.  
   The echo server (or generator) will be accessible via the Space URL.

---

## 🧠 Future Improvements
- Add a web UI (Gradio / Streamlit) for interactive LLM task submission  
- Store generated files in GitHub automatically  
- Integrate evaluation feedback loops  

---

## 🪪 License
This project uses the **MIT License** — feel free to use, modify, and distribute with attribution.

---

## 👨‍💻 Author
**22f3002716 – IITM BS in Data Science and Applications**  
Course: *Tools for Data Science (TDS)*  
Semester Project: *LLM App Builder & Deployment Pipeline*