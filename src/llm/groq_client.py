from langchain_groq import ChatGroq
#from langchain_openai import ChatOpenAI
from src.config.settings import settings

def get_groq_llm():
    return ChatGroq(
        api_key = settings.GROK_API_KEY,
        model = settings.MODEL_NAME,
        temperature = settings.TEMPERATURE)