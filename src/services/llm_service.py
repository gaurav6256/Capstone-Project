from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import GEMINI_MODEL, GOOGLE_API_KEY, TEMPERATURE

def get_llm():
    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=TEMPERATURE,
    )
