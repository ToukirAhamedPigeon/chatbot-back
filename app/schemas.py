from pydantic import BaseModel  # Import BaseModel from Pydantic to create data validation models
from typing import Optional       # Import Optional to allow some fields to be optional (can be None)

# Define the request model for the chat endpoint
class ChatRequest(BaseModel):
    query: str                   # The actual user question or query (required)
    topic: Optional[str] = None  # Optional metadata: topic of the question (e.g., education, health)
    difficulty: Optional[str] = None  # Optional metadata: difficulty level of the question (easy, medium, hard)

# Define the response model for the chat endpoint
class ChatResponse(BaseModel):
    answer: str                  # The AI-generated answer (required)
