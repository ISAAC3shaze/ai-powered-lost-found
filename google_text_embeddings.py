import os
import google.generativeai as genai

# Configure Google AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_google_text_embedding(text: str):
    """
    Uses Google AI (Gemini) text embeddings
    Returns a list[float]
    """
    response = genai.embed_content(
        model="models/text-embedding-004",
        content=text
    )
    return response["embedding"]
