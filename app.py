from fastapi import FastAPI

from langchain.chat_models import BaseChatModel

from src.models import AnswerStudent, Comment
from src.comment import generate_comments
from src.chat import get_chat

app = FastAPI()

chat: BaseChatModel = get_chat()

@app.post("/comments/")
async def create_comments(question: AnswerStudent) -> list[Comment]:
    return await generate_comments(question, chat)