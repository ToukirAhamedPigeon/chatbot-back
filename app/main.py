from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import ChatRequest, ChatResponse
from app.rag import BanglaRAG
from app.model import BanglaLLM

app = FastAPI(title="Bangla RAG Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ⛔ module level এ কিছু instantiate করো না
rag: BanglaRAG | None = None
llm: BanglaLLM | None = None


@app.on_event("startup")
def startup_event():
    global rag, llm
    print("Loading RAG & LLM models...")
    rag = BanglaRAG()
    llm = BanglaLLM()
    print("Models loaded successfully")


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    docs = rag.retrieve(
        query=req.query,
        topic=req.topic,
        difficulty=req.difficulty
    )

    if not docs:
        return ChatResponse(
            answer="দুঃখিত 😔 এই বিষয়ে এখনো আমার কাছে তথ্য নেই।"
        )

    context = "\n\n".join(doc.page_content for doc in docs)
    answer = llm.generate_answer(req.query, context)
    return ChatResponse(answer=answer)
