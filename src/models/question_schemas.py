from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field, validator

class MCQQuestion(BaseModel):
    question: str = Field(description = "The Question text")
    options: List[str] =  Field(description = "List of 4 options")
    correct_answer: str = Field(description = "The correct answer from the options")

    @validator("question", pre=True, allow_reuse=True)
    def clean_mcq_question(cls, v):
        if isinstance(v, dict):
            return v.get("description", str(v))
        return str(v)
    
class FillBlankQuestion(BaseModel):
    question: str = Field(description = "The Question text with '___' for the blank")
    answer: str = Field(description = "The correct word or phase for the blank")

    @validator("question", pre=True, allow_reuse=True)
    def clean_fill_blank_question(cls, v):
        if isinstance(v, dict):
            return v.get("description", str(v))
        return str(v)