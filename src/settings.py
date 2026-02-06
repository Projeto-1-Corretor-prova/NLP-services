from dotenv import load_dotenv

from os import getenv

load_dotenv()

class Settings:
    CHAT_URL: str = getenv("CHAT_URL")
    MODEL: str = getenv("MODEL")
    API_KEY: str = getenv("API_KEY")
    CHAT_TYPE: str = getenv("CHAT_TYPE")