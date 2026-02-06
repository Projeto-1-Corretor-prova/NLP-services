from enum import Enum

from typing import TypedDict

class CriteriaEnum(Enum):
    SEMANTIC = "SEMANTIC"
    EXAMPLE = "EXAMPLE"
    KEYWORD = "KEYWORD"
    
MAP_CRITERIA_ENUM = {
    "SEMANTIC": CriteriaEnum.SEMANTIC,
    "EXAMPLE": CriteriaEnum.EXAMPLE,
    "KEYWORD": CriteriaEnum.KEYWORD
}
class QuestionCriteria(TypedDict):
    id: int
    type: CriteriaEnum
    criteria: str
    
class AnswerStudent(TypedDict):
    id: int
    statement: str
    question_criteria: list[QuestionCriteria]
    answer: str
class Comment(TypedDict):
    criteria_id: int
    content: str