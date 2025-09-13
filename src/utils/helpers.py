import os
import streamlit as st
import pandas as pd
from src.generator.question_generator import QuestionGenerator

def rerun():
    st.session_state["rerun_trigger"]= not st.session_state.get("rerun_trigger", False)

class QuizeManager:
    def __init__(self):
        self.questions = []
        self.user_answers = []
        self.result = []

    def generate_questions(self, generator:QuestionGenerator, exam:str, subject:str, topic:str , question_type:str, difficulty:str, number_questions:int):
        self.questions = []
        self.user_answers = []
        self.result = []

        try:
            for _ in range(number_questions):
                if question_type=="Multiple Choice":
                    question = generator.generate_mcq(exam, subject, topic, difficulty.lower())
                    
                    self.questions.append({
                    "type": "MCQ",
                    "exam":question.exam,
                    "subject": question.subject,
                    "topic": question.topic,
                    "difficulty":question.difficulty,
                    "question": question.question,
                    "options": question.options,
                    "correct_answer": question.correct_answer,
                    "explanantion": question.explanation})
                else:
                    question = generator.generate_fill_blank(exam, subject, topic, difficulty.lower())
                    self.questions.append({
                        "type":"Fill in the blank",
                        "exam": question.exam,
                        "subject": question.subject,
                        "topic":question.topic,
                        "difficulty": question.difficulty,
                        "question": question.question,
                        "correct_answer": question.answer,
                        "explanation": question.explanation
                    })
        except Exception as e:
            st.error(f"Error generating question {e}")
            return False
        return True
    
    def attempt_quiz(self):
        for i,q in enumerate(self.questions):

            st.markdown(f"**Question {i+1}**")
            st.markdown(f"**EXAM:** {q['exam']} | **subject:** {q['subject']} | **Topic:** {q['topic']} | **Difficulty:** {q['difficulty']}")
            st.markdown(f"**Question:** {q['question']}")

            if q["type"] == "MCQ":
                user_answer = st.radio(f"Select an answer for question {i+1}",
                                      q["options"],
                                      key = f"mcq_{i}",
                                      index=None)  # No default selection
                
                if user_answer is not None:
                    if len(self.user_answers) <= i:
                        self.user_answers.extend([None] * (i - len(self.user_answers) + 1))
                    self.user_answers[i] = user_answer
            else:
                user_answer = st.text_input(
                    f"Fill in the blank for question{i+1}",
                    key = f"fill_blank{i}")
                
                if len(self.user_answers) <= i:
                    self.user_answers.extend([None] * (i - len(self.user_answers) + 1))
                self.user_answers[i] = user_answer

    def evaluate_quiz(self):
        self.results = []

        for i, (q,user_ans) in enumerate(zip(self.questions,self.user_answers)):
            result_dict = {
                "question_number": i+1,
                "exam": q["exam"],
                "subject": q["subject"],
                "topic": q["topic"],
                "question": q["question"],
                "question_type": q["type"],
                "user_answer": user_ans,
                "correct_answer": q["correct_answer"],
                "explanation": q["explanation"],
                "is_correct": False
            }

            if q["type"] == "MCQ":
                result_dict["options"]=q["options"]
                result_dict["is_correct"] = user_ans == q["correct_answer"]

            else:
                result_dict["options"]= []
                result_dict["is_correct"] = user_ans.strip().lower() == q["correct_answer"].strip().lower()

            self.results.append(result_dict)

    def generate_result_dataframe(self):
        if not self.results:
            return pd.DataFrame()
        
        return pd.DataFrame(self.results)
    
    def save_to_csv(self, filname_prefix = "quiz_results"):
        if not self.results:
            st.warning("No results to save")
            return None
        
        df = self.generate_result_dataframe()

        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{filname_prefix}_{timestamp}.csv"

        os.makedirs("results", exist_ok=True)
        full_path = os.path.join("results", unique_filename)

        try:
            df.to_csv(full_path,index=False)
            st.success("Results saved sucessfully")
            return full_path
        except Exception as e:
            st.error(f"Failed to save results {e}")
            return None
