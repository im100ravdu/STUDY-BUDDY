import os
import streamlit as st
from dotenv import load_dotenv
from src.utils.helpers import *
from src.generator.question_generator import QuestionGenerator
from src.config.exam_config import EXAM_CONFIG
load_dotenv()

def main():
    st.set_page_config(page_title="Studdy Buddy AI")

    if 'quiz_manager' not in st.session_state:
        st.session_state.quiz_manager = QuizeManager()
    
    if 'quiz_generated' not in st.session_state:
        st.session_state.quiz_generated = False

    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False

    if 'rerun_trigger' not in st.session_state:
        st.session_state.rerun_trigger = False

    st.title("Study Buddy AI")
    st.subheader("Exam Preparation Tool")

    exam = st.selectbox(
        "Select Exam",
        ["IIT JEE", "NEET", "SSC CGL", "UPSC"],
        key = "exam_selection"
    )

    if exam:
        subjects = EXAM_CONFIG[exam]["subjects"]
        subject = st.selectbox(
            "Select Subject",
            subjects,
            key="subject_selection"
        )
    if subjects:
        topics = EXAM_CONFIG[exam]["topics"][subject]
        topic = st.selectbox(
            "Select Topic",
            topics,
            key = "topic_selection"
        )
    st.sidebar.header("Model Provider")
    provider = st.sidebar.selectbox("Provider",
                                    ["groq", "openai"],
                                    index = 0)

    st.sidebar.header("Quiz Settings")
    if "exam" in locals() and 'subject' in locals() and 'topics' in locals():
        question_type = st.sidebar.selectbox(
            "Selection Question Type",
            EXAM_CONFIG[exam]["question_types"],
            index=0
        )

        difficulty = st.sidebar.selectbox(
            "Difficulty Level",
            EXAM_CONFIG[exam]["difficulty_level"],
            index=1
        )

        num_questions = st.sidebar.number_input("Number of questions", min_value=1, max_value=10, value = 5)


    
    if st.sidebar.button("Generate Quiz") and 'exam' in locals() and 'subject' in locals() and 'topic' in locals():
        st.session_state.quiz_submitted = False
        generator = QuestionGenerator()
        success = st.session_state.quiz_manager.generate_questions(
            generator,
            exam, subject, topic, question_type, difficulty, num_questions
        )

        st.session_state.quiz_generated = success
        rerun()
    else:
        if 'exam' not in locals() or 'subject' not in locals() or 'topic' not in locals():
            st.sidebar.warning("Please select exam, subject and topic first")

    if st.session_state.quiz_generated and st.session_state.quiz_manager.questions:
        st.header("Quiz")
        st.session_state.quiz_manager.attempt_quiz()

        if st.button("Submit Quiz"):
            st.session_state.quiz_manager.evaluate_quiz()
            st.session_state.quiz_submitted = True
            rerun()
    
    if st.session_state.quiz_submitted:
        st.header("Quiz Results")
        results_df = st.session_state.quiz_manager.generate_result_dataframe()
        if not results_df.empty:
            correct_count = results_df["is_correct"].sum()
            total_question = len(results_df)
            score_percentage = (correct_count/total_question)*100
            st.write(f"score: {score_percentage}")

            for _, result in results_df.iterrows():
                question_num = result["question_number"]
                if result["is_correct"]:
                    st.success(f"Right Question {question_num}: {result['question']}")
                else:
                    st.error(f"X Question {question_num}: {result['question']}")
                    st.write(f"Your anwer: {result['user_answer']}")
                    st.write(f"Correct answer: {result['correct_answer']}")
                
                st.markdown("-------")
            if st.button("Save Results"):
                saved_file = st.session_state.quiz_manager.save_to_csv()
                if saved_file:
                    with open(saved_file, "rb") as f:
                        st.download_button(
                            label="Download_Result",
                            data=f.read(),
                            file_name=os.path.basename(saved_file),
                            mime = 'text/csv'
                        )
                else:
                    st.warning("No results available")

if __name__=="__main__":
    main()
        