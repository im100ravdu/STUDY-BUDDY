from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field, validator

class MCQQuestion(BaseModel):
    exam: str = Field(description = "The exam type (IIT JEE, NEET etc.)")
    subject: str = Field(description = "The subject within the exam")
    topic: str = Field(description = "The specific topic within the subject")
    difficulty: str = Field(description = "The difficulty level")
    question: str = Field(description = "The question text")
    options: List[str] = Field(description = "List of 4 options")
    correct_answer: str = Field(description = "The correct answer")
    explanation:str = Field(description = "Explanation for the answer")
     
    @validator("question", pre=True, allow_reuse=True)
    def clean_mcq_question(cls, v):
        if isinstance(v, dict):
            return v.get("description", str(v))
        return str(v)
    
class FillBlankQuestion(BaseModel):
    exam: str = Field(description="The exam type (IIT JEE, NEET, etc.)")
    subject: str = Field(description="The subject wuthin the exam")
    topic: str = Field(description="The specific topic within the subject")
    difficulty: str = Field(description="The difficulty levl")
    question: str = Field(description="The question text with '____' for the blank)")
    answer: str = Field(description="The correct word or phase for the bank")
    explanation: str = Field(description="Explanation for the answer")

    @validator("question", pre=True, allow_reuse=True)
    def clean_fill_blank_question(cls, v):
        if isinstance(v, dict):
            return v.get("description", str(v))
        return str(v)