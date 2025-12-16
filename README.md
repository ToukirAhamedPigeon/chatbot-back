# Bengali RAG Chatbot Backend

## Overview
- FastAPI backend with FAISS + HuggingFace SBERT embeddings
- Topics: শিক্ষা, স্বাস্থ্য, ভ্রমণ, প্রযুক্তি, খেলাধুলা
- Metadata filtering by `topic` and `difficulty`
- Bengali input/output with GPT-4.1-mini via GitHub Models
- Fallback response if no answer is found

## Project Structure
```
backend/
  app/
    main.py
    model.py
    rag.py
    data/
      faq.json
requirements.txt
Dockerfile
docker-compose.yml
.gitignore
README.md
```

## Prerequisites
- Python 3.11+
- PowerShell (Windows)
- GitHub token with access to GitHub Models

## Windows Setup
```powershell
cd D:\chatbot\chatbot-back
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
$env:GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"
uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000
```

### Test API
```powershell
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{
  "question": "উচ্চশিক্ষায় গবেষণার বিষয় কীভাবে নির্বাচন করবো?",
  "filters": {"topic": "শিক্ষা", "difficulty": "মধ্যম"}
}'
```

## Docker (Windows)
```powershell
cd D:\chatbot\chatbot-back
docker compose up --build -d
```

## Environment
- `GITHUB_TOKEN`: GitHub Models token
- `HUGGINGFACE_CACHE`: optional local cache folder

## Notes
- First run downloads the Bengali SBERT model: `l3cube-pune/bengali-sentence-similarity-sbert`
- If `filters` are not provided, the system auto-classifies `topic` and `difficulty` in Bangla.
