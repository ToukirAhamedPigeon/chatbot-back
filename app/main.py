"""
This file defines the FastAPI backend for the Bangla RAG Chatbot.
It loads environment variables, sets up CORS for frontend access,
initializes the RAG engine and GPT-4.1-mini model, and exposes a
single endpoint '/chat' to handle user queries. The endpoint retrieves
relevant FAQ documents based on topic and difficulty, constructs
context, calls the GPT model, and returns a Bangla answer.
"""

from fastapi import FastAPI  # Import FastAPI class to create API application
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware to allow frontend requests
from dotenv import load_dotenv  # Import function to load environment variables from .env file

# Load environment variables from .env file into the environment
load_dotenv()

from app.schemas import ChatRequest, ChatResponse  # Import Pydantic models for request and response validation
from app.rag import BanglaRAG  # Import RAG engine class for retrieval
from app.model import BanglaLLM  # Import GPT wrapper class for generating answers

# Create a FastAPI instance with a custom title
app = FastAPI(title="Bangla RAG Chatbot")

# Enable CORS (Cross-Origin Resource Sharing) so frontend can access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin (for React frontend)
    allow_credentials=True,  # Allow sending cookies/auth credentials
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Initialize the RAG engine (retrieval) instance
rag = BanglaRAG()

# Initialize the GPT model instance
llm = BanglaLLM()

# Define POST endpoint at '/chat' to handle user queries
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """
    Endpoint: /chat
    Request: ChatRequest object containing query, topic, and difficulty
    Response: ChatResponse object containing the generated Bangla answer
    """

    # Step 1: Retrieve relevant FAQ documents from the RAG engine based on query, topic, and difficulty
    docs = rag.retrieve(
        query=req.query,
        topic=req.topic,
        difficulty=req.difficulty
    )

    # Step 2: If no documents were found, return a fallback message
    if not docs:
        return ChatResponse(
            answer="দুঃখিত 😔 এই বিষয়ে এখনো আমার কাছে তথ্য নেই।"
        )

    # Step 3: Build the context string by joining retrieved document contents
    context = "\n\n".join([doc.page_content for doc in docs])

    # Step 4: Generate a Bangla answer from GPT-4.1-mini using the query and retrieved context
    answer = llm.generate_answer(req.query, context)

    # Return the answer wrapped in the ChatResponse model
    return ChatResponse(answer=answer)
