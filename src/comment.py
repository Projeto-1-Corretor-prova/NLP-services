from langchain.chat_models import BaseChatModel
from langchain.messages import SystemMessage, HumanMessage

from asyncio import gather

from re import search

from src.messages import SYSTEM_SEMANTIC_MESSAGE, CRITERIA_SEMANTIC_MESSAGE, SYSTEM_EXAMPLE_MESSAGE, CRITERIA_EXAMPLE_MESSAGE
from src.models import QuestionCriteria, AnswerStudent, Comment, CriteriaEnum, MAP_CRITERIA_ENUM

system_semantic_message = SystemMessage(content=SYSTEM_SEMANTIC_MESSAGE)
system_example_message = SystemMessage(content=SYSTEM_EXAMPLE_MESSAGE)

def generate_keyword_comment(answer: str, criteria: QuestionCriteria) -> Comment:
    possible_match = search(criteria["criteria"], answer)
    
    if possible_match:
        possible_match_group = possible_match.group(0)
        content = f"A resposta contém a palavra chave esperada: '{possible_match_group}'."
    else:
        content = "A resposta não contém os elementos esperados conforme o critério de aceitação."
        
    return Comment(criteria_id=criteria["id"], content=content)

async def generate_semantic_comment(chat: BaseChatModel, answer: str, criteria: QuestionCriteria) -> list[Comment]:
    human_criteria_message = HumanMessage(content=f"{CRITERIA_SEMANTIC_MESSAGE}: {criteria['criteria']}")
    human_answer_message = HumanMessage(content=f"Resposta do aluno: {answer}")
    
    response = await chat.agenerate(
        messages=[
            [system_semantic_message, human_criteria_message, human_answer_message]
        ]
    )
    
    comments = [generation.message.content for generation in response.generations[0]]
    
    return [Comment(criteria_id=criteria["id"], content=comment) for comment in comments]

async def generate_example_comment(chat: BaseChatModel, answer: str, criteria: QuestionCriteria) -> list[Comment]:
    human_criteria_message = HumanMessage(content=f"{CRITERIA_EXAMPLE_MESSAGE}: {criteria['criteria']}")
    human_answer_message = HumanMessage(content=f"Resposta do aluno: {answer}")
    
    response = await chat.agenerate(
        messages=[
            [system_example_message, human_criteria_message, human_answer_message]
        ]
    )
    
    comments = [generation.message.content for generation in response.generations[0]]
    
    return [Comment(criteria_id=criteria["id"], content=comment) for comment in comments]

async def generate_comments(question: AnswerStudent, chat: BaseChatModel) -> list[Comment]:
    criteria_keywords = [c for c in question["question_criteria"] if c["type"] == CriteriaEnum.KEYWORD]
    criteria_semantic = [c for c in question["question_criteria"] if c["type"] == CriteriaEnum.SEMANTIC]
    criteria_example = [c for c in question["question_criteria"] if c["type"] == CriteriaEnum.EXAMPLE]
    
    comments = []
    
    coments_keyword: list[Comment] = list(map(lambda c: generate_keyword_comment(question["answer"], c), criteria_keywords))    
    coments_generate_example_semantic = await gather(*[generate_semantic_comment(chat, question["answer"], c) for c in criteria_semantic])
    coments_generate_example_example = await gather(*[generate_example_comment(chat, question["answer"], c) for c in criteria_example])
    
    comments.extend(coments_keyword)
    for comment_list in coments_generate_example_semantic:
        comments.extend(comment_list)
    for comment_list in coments_generate_example_example:
        comments.extend(comment_list)
    
    return comments