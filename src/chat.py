from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.chat_models import BaseChatModel

from src.settings import Settings

chat: BaseChatModel

def get_chat() -> BaseChatModel:
    match Settings.CHAT_TYPE:
        case "ollama":
            return ChatOllama(base_url=Settings.CHAT_URL, model=Settings.MODEL)
        case "google":
            return ChatGoogleGenerativeAI(model=Settings.MODEL, api_key=Settings.API_KEY)
        case "openai":
            return ChatOpenAI(model_name=Settings.MODEL, api_key=Settings.API_KEY)
        case _: 
            raise ValueError(f"Unsupported CHAT_TYPE: {Settings.CHAT_TYPE}")