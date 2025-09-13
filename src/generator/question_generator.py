from langchain.output_parsers import PydanticOutputParser
from src.models.question_schemas import MCQQuestion, FillBlankQuestion
from src.prompts.templates import get_mcq_prompt_template, get_fill_blank_prompt_template
from src.llm.groq_client import get_groq_llm
from src.config.settings import settings
from src.common.logger import get_logger
from src.common.custom_exception import CustomException


class QuestionGenerator:
    def __init__(self):
        self.llm = get_groq_llm()
        self.logger = get_logger(self.__class__.__name__)

    def _retry_and_parse(self, prompt, parser, exam, subject, topic, difficulty):

        for attempt in range(settings.MAX_RETRIES):
            try:
                self.logger.info(f"Generating question for exam {exam} {subject} - {topic} with difficulty {difficulty}")
                response = self.llm.invoke(prompt.format(exam = exam, subject = subject, topic = topic, difficulty = difficulty))
                self.logger.info(f"LLM raw response: {response.content}")
                parsed = parser.parse(response.content)
                self.logger.info("successfully parsed the question")
                return parsed

            except Exception as e:
                self.logger.error(f"Error coming: f{str(e)}")
                if attempt==settings.MAX_RETRIES-1:
                    raise CustomException(f"Generation failed after {settings.MAX_RETRIES} attempts")
    

    def generate_mcq(self, exam:str, subject:str, topic:str, difficulty:str = "medium")-> MCQQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=MCQQuestion)
            prompt_template = get_mcq_prompt_template(exam, subject, topic, difficulty)
            question = self._retry_and_parse(prompt_template, parser, exam, subject, topic, difficulty)

            if len(question.options)!= 4 or question.correct_answer not in question.options:
                raise ValueError("Invalid MCQ Structure")
            self.logger.info("Generated a valid MCQ")
            return question
        except Exception as e:
            self.logger.error(f"Failed to generated MCQ: {str(e)}")
            raise CustomException("MCQ generation failed", e)


    def generate_fill_blank(self, exam: str, subject: str, topic:str, difficulty:str = "medium")-> FillBlankQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=FillBlankQuestion)
            prompt_template = get_fill_blank_prompt_template(exam, subject, topic, difficulty)
            question = self._retry_and_parse(prompt_template, parser, exam, subject, topic, difficulty)

            self.logger.info("Generated a valid fill in the blank")
            return question
        except Exception as e:
            self.logger.error(f"Failed to generated Fillups: {str(e)}")
            raise CustomException("Fill blank generation failed", e)