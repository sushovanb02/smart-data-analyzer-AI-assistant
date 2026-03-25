from langchain_community.chat_models import ChatOllama
from app.utils.config import OLLAMA_HOST

def get_llm():
    return ChatOllama(
        model="llama3",
        base_url=OLLAMA_HOST
    )