# This file defines a wrapper class for interacting with the GPT-4.1-mini model
# via GitHub Models/OpenAI API. It is designed to generate Bengali language
# answers using context retrieved from a RAG system or FAQ dataset.

import os  # Import the os module to access environment variables
from dotenv import load_dotenv  # Import load_dotenv to load environment variables from a .env file
from openai import OpenAI  # Import OpenAI client to interact with GPT models

# Load environment variables from the .env file into the system environment
load_dotenv()

class BanglaLLM:
    """
    GPT-4.1-mini wrapper for Bangla answers
    """
    def __init__(self):
        # Initialize the OpenAI client with the API key and base URL for GitHub Models
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),  # Get the API key from environment variables
            base_url="https://models.inference.ai.azure.com"  # Base URL for GitHub Models
        )

    def generate_answer(self, question: str, context: str) -> str:
        """
        Generate Bangla answer using retrieved context
        """
        # Build a prompt string for the GPT model with instructions and context
        prompt = f"""
তুমি একজন বাংলা সহকারী।
শুধুমাত্র নিচের তথ্য ব্যবহার করে উত্তর দাও।
যদি তথ্য না পাওয়া যায়, বলো: "এই বিষয়ে আমার কাছে তথ্য নেই।"

তথ্য:
{context}  # Inject retrieved context here

প্রশ্ন:
{question}  # Inject user's question here

উত্তর বাংলা ভাষায় দাও।
"""
        # Call the GPT-4.1-mini model with the prompt
        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",  # Specify the model to use
            messages=[{"role": "user", "content": prompt}],  # Send prompt as a user message
            temperature=0.3  # Set temperature for response randomness (low = more deterministic)
        )

        # Return the text content of the first response, stripping extra whitespace
        return response.choices[0].message.content.strip()
