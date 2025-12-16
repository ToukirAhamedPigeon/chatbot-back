# Bengali RAG Chatbot Backend

A robust FastAPI backend implementing Retrieval-Augmented Generation (RAG) for a Bengali FAQ chatbot. It uses FAISS for vector search, HuggingFace SBERT embeddings for semantic understanding, and GitHub Models (GPT-4.1-mini) for generating natural language responses.

## 🚀 Features

- **RAG Architecture**: Combines vector search with LLM generation for accurate answers.
- **Bengali Language Support**: Native support for Bengali input and output.
- **Metadata Filtering**: Filters search results by `topic` (Topic) and `difficulty` (Difficulty).
- **Auto-Classification**: Automatically detects topic and difficulty if not provided by the user.
- **Fallback Mechanism**: Gracefully handles unknown queries with a polite fallback message.
- **Vector Database**: Uses FAISS (Facebook AI Similarity Search) for efficient similarity search.
- **Embeddings**: Uses `l3cube-pune/bengali-sentence-similarity-sbert` specifically optimized for Bengali.
- **API Documentation**: Auto-generated Swagger UI.

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Vector Store**: FAISS (CPU)
- **Embeddings**: LangChain + HuggingFace (`l3cube-pune/bengali-sentence-similarity-sbert`)
- **LLM**: OpenAI SDK connecting to GitHub Models (`gpt-4.1-mini`)
- **Validation**: Pydantic
- **Containerization**: Docker & Docker Compose

## 📂 Project Structure

```
backend/
  app/
    data/
      faq.json       # Knowledge base (FAQs in Bengali)
    main.py          # FastAPI application entry point & endpoints
    model.py         # Pydantic models for Request/Response
    rag.py           # RAG pipeline logic (Embedding, Indexing, Retrieval)
    __init__.py
requirements.txt     # Python dependencies
Dockerfile           # Docker image configuration
docker-compose.yml   # Docker services configuration
README.md            # Project documentation
```

## ⚙️ Prerequisites

- **Python**: 3.10 or 3.11
- **GitHub Account**: To access GitHub Models.
- **GitHub Token**: A personal access token with access to GitHub Models.

## 💻 Local Setup (Windows)

1.  **Clone/Navigate to the directory**:
    ```powershell
    cd D:\chatbot\chatbot-back
    ```

2.  **Create a Virtual Environment**:
    ```powershell
    python -m venv .venv
    ```

3.  **Activate the Virtual Environment**:
    ```powershell
    .\.venv\Scripts\Activate.ps1
    ```

4.  **Install Dependencies**:
    ```powershell
    pip install -r requirements.txt
    ```
    *Note: This installs PyTorch (via `sentence-transformers`), FAISS, FastAPI, etc.*

5.  **Set Environment Variables**:
    You need a GitHub Token to use the LLM.
    ```powershell
    $env:GITHUB_TOKEN = "your_github_token_here"
    ```
    *(Optional) Set a custom cache path for HuggingFace models:*
    ```powershell
    $env:HUGGINGFACE_CACHE = "D:\chatbot\chatbot-back\.cache\hf"
    ```

6.  **Run the Server**:
    ```powershell
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```

    The server will start at `http://localhost:8000`.

## 🐳 Docker Setup

Run the entire backend service in a container.

1.  **Build and Run**:
    ```powershell
    docker compose up --build -d
    ```
    *Make sure to set the `GITHUB_TOKEN` in `docker-compose.yml` or pass it as an environment variable.*

2.  **Stop Containers**:
    ```powershell
    docker compose down
    ```

## 📖 API Documentation

Once the server is running, visit **http://localhost:8000/docs** for the interactive Swagger UI.

### 1. Chat Endpoint
**POST** `/chat`

Generates an answer based on the user's question and optional filters.

**Request Body:**
```json
{
  "question": "উচ্চশিক্ষায় গবেষণার বিষয় কীভাবে নির্বাচন করবো?",
  "filters": {
    "topic": "শিক্ষা",
    "difficulty": "মধ্যম"
  }
}
```
*Note: `filters` is optional. If omitted, the system will try to classify the question automatically.*

**Response:**
```json
{
  "answer": "উচ্চশিক্ষায় গবেষণার বিষয় নির্বাচনের জন্য নিজের আগ্রহ, উপলব্ধ সম্পদ এবং সুপারভাইজারের বিশেষজ্ঞতা বিবেচনা করা উচিত।",
  "topic": "শিক্ষা",
  "difficulty": "মধ্যম",
  "sources": [
    {
      "question": "উচ্চশিক্ষায় গবেষণার বিষয় নির্বাচন কীভাবে করবো?",
      "answer": "নিজের আগ্রহ, উপলব্ধ সম্পদ, সুপারভাইজারের বিশেষজ্ঞতা এবং বাস্তবসম্মত লক্ষ্য বিবেচনা করে নির্বাচন করা উচিত。",
      "topic": "শিক্ষা",
      "difficulty": "কঠিন",
      "score": 0.45
    }
  ]
}
```

### 2. Health Check
**GET** `/health`

Returns the status of the API.
```json
{ "status": "ok" }
```

### 3. Rebuild Index
**POST** `/rebuild-index`

Reloads `faq.json` and rebuilds the FAISS vector index. Use this after modifying the dataset without restarting the server.
```json
{ "status": "rebuilt" }
```

## 📚 Data Management

The knowledge base is stored in `backend/app/data/faq.json`.

**Format:**
```json
[
  {
    "topic": "Topic Name (e.g., শিক্ষা)",
    "difficulty": "Level (e.g., সহজ, মধ্যম, কঠিন)",
    "question": "The question in Bengali?",
    "answer": "The answer in Bengali."
  }
]
```
To add new FAQs, simply edit this file and call the `/rebuild-index` endpoint or restart the server.

## ❓ Troubleshooting

- **`AuthenticationError` / 401**: Ensure `$env:GITHUB_TOKEN` is set correctly and has access to GitHub Models.
- **Dependency Conflicts**: If `pip install` fails, try upgrading pip: `python -m pip install --upgrade pip` and ensure you are using Python 3.10/3.11.
- **Model Download**: The first run might be slow as it downloads the SBERT model (~400MB). Ensure you have an internet connection.
