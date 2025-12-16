import json
from typing import List, Optional
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings


class BanglaRAG:
    """
    Bangla RAG engine:
    - Load FAQ data
    - Create embeddings with Bengali SBERT
    - Store embeddings in FAISS vectorstore
    - Retrieve relevant docs with optional filters
    """

    def __init__(self):
        # CPU-only embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="l3cube-pune/bengali-sentence-similarity-sbert",
            model_kwargs={"device": "cpu"}  # force CPU usage
        )
        self.vectorstore = self._build_vectorstore()

    def _load_faq(self) -> List[Document]:
        """Load FAQ JSON and return as LangChain Document objects"""
        with open("app/data/faq.json", "r", encoding="utf-8") as f:
            faq_data = json.load(f)

        documents = []
        for item in faq_data:
            content = f"প্রশ্ন: {item['question']}\nউত্তর: {item['answer']}"
            documents.append(
                Document(
                    page_content=content,
                    metadata={
                        "topic": item["metadata"]["topic"],
                        "difficulty": item["metadata"]["difficulty"],
                        "id": item["id"],
                    },
                )
            )
        return documents

    def _build_vectorstore(self) -> FAISS:
        """Build FAISS vectorstore from FAQ documents"""
        documents = self._load_faq()
        vectorstore = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )
        return vectorstore

    def retrieve(
        self,
        query: str,
        topic: Optional[str] = None,
        difficulty: Optional[str] = None,
        k: int = 3
    ) -> List[Document]:
        """Retrieve top-k relevant documents with optional metadata filters"""
        filters = {}
        if topic:
            filters["topic"] = topic
        if difficulty:
            filters["difficulty"] = difficulty

        docs = self.vectorstore.similarity_search(
            query=query,
            k=k,
            filter=filters if filters else None
        )
        return docs
