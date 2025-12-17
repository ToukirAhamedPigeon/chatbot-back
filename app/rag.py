# ----------------------------------------
# File Purpose:
# This file defines the BanglaRAG class, which is responsible for:
# 1. Loading Bangla FAQ data from a JSON file
# 2. Creating embeddings using the Bengali SBERT model
# 3. Storing the embeddings in a FAISS vectorstore for efficient retrieval
# 4. Retrieving relevant documents based on a query with optional metadata filters
# ----------------------------------------

import json  # For reading and parsing JSON files
from typing import List, Optional  # Type hints for lists and optional parameters
from langchain_community.vectorstores import FAISS  # FAISS vectorstore for fast similarity search
from langchain_community.embeddings import HuggingFaceEmbeddings  # HuggingFace embeddings model
from langchain_core.documents import Document  # Document object used by LangChain

class BanglaRAG:
    """
    Handles:
    - Loading FAQ data
    - Embedding via Bengali SBERT
    - FAISS vectorstore
    - Metadata-based retrieval
    """

    def __init__(self):
        # Load SBERT embeddings model for Bengali sentence similarity
        self.embeddings = HuggingFaceEmbeddings(
            model_name="l3cube-pune/bengali-sentence-similarity-sbert"
        )
        # Build FAISS vectorstore from the FAQ documents immediately on initialization
        self.vectorstore = self._build_vectorstore()

    def _load_faq(self) -> List[Document]:
        """
        Load FAQ JSON into LangChain Document objects
        """
        # Open the JSON file containing FAQ data in UTF-8 encoding
        with open("app/data/faq.json", "r", encoding="utf-8") as f:
            faq_data = json.load(f)  # Parse the JSON file into a Python list/dict

        documents = []  # Initialize an empty list to hold Document objects
        for item in faq_data:  # Iterate through each FAQ entry
            # Combine question and answer into a single string for the Document
            content = f"প্রশ্ন: {item['question']}\nউত্তর: {item['answer']}"
            # Create a Document object with content and metadata
            documents.append(
                Document(
                    page_content=content,  # Set the text content of the document
                    metadata={  # Store additional info for filtering/search
                        "topic": item["metadata"]["topic"],
                        "difficulty": item["metadata"]["difficulty"],
                        "id": item["id"],
                    },
                )
            )
        return documents  # Return the list of Document objects

    def _build_vectorstore(self) -> FAISS:
        """
        Create FAISS vectorstore from documents
        """
        documents = self._load_faq()  # Load the FAQ documents
        # Create a FAISS vectorstore using the embeddings and documents
        vectorstore = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )
        return vectorstore  # Return the built FAISS vectorstore

    def retrieve(
        self,
        query: str,  # The search query string
        topic: Optional[str] = None,  # Optional topic filter
        difficulty: Optional[str] = None,  # Optional difficulty filter
        k: int = 3,  # Number of top documents to retrieve
    ) -> List[Document]:
        """
        Retrieve top-k relevant documents with optional metadata filter
        """
        filter_dict = {}  # Initialize empty filter dictionary
        if topic:  # If topic is specified
            filter_dict["topic"] = topic  # Add topic filter
        if difficulty:  # If difficulty is specified
            filter_dict["difficulty"] = difficulty  # Add difficulty filter

        # Perform similarity search in FAISS vectorstore with optional filters
        docs = self.vectorstore.similarity_search(
            query=query,  # Search query
            k=k,  # Number of top documents
            filter=filter_dict if filter_dict else None  # Apply filter if exists
        )
        return docs  # Return the list of retrieved Document objects
