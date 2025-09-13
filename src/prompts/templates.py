from langchain_core.prompts import PromptTemplate

def get_mcq_prompt_template(exam:str, subject:str, topic:str, difficulty:str):
    base_template = f"""
Generate a {difficulty} multiple-choice questions for {exam} {subject} on the topic: {topic}.

Exam-specific requirements:
- Exam: {exam}
- Subject: {subject}
- Topic: {topic}
- Difficulty: {difficulty}
- Question Type: Multiple Choice

Return only a JSON object with these exact fields:
- 'exam': '{exam}'
- 'subject': '{subject}'
- 'topic': '{topic}'
- 'difficulty': '{difficulty}'
- 'question': A clear, specfic question appropiate for {exam} level
- 'options': An array of exactly 4 possible answers
- 'correct_answer': One of the options that is correct
- 'explanantion': Brief explanation of why the answer is correct

Example format:
{{
"exam":"{exam}",
"subject":"{subject}",
"topic":"{topic}",
"difficulty":"{difficulty}",
"question":"what is the capital of france",
"options": ["London" ,"Berlin", "Paris", "Madrid"],
"correct_answer":"Paris",
"explanation":"Paris is the capital and largest city of France."
}}

Your response
"""
    return PromptTemplate(template=base_template, input_variables=[])





def get_fill_blank_prompt_template(exam: str, subject: str, topic: str, difficulty: str):
    base_template = f"""
    Generate a {difficulty} fill-in-the-blank question for {exam} {subject} on the topic: {topic}.
    
    Exam-specific requirements:
    - Exam: {exam}
    - Subject: {subject}
    - Topic: {topic}
    - Difficulty: {difficulty}
    - Question Type: Fill in the Blank
    
    Return ONLY a JSON object with these exact fields:
    - 'exam': '{exam}'
    - 'subject': '{subject}'
    - 'topic': '{topic}'
    - 'difficulty': '{difficulty}'
    - 'question': A sentence with '_____' marking where the blank should be
    - 'answer': The correct word or phrase that belongs in the blank
    - 'explanation': Brief explanation of why this answer is correct
    
    Example format:
    {{
        "exam": "{exam}",
        "subject": "{subject}",
        "topic": "{topic}",
        "difficulty": "{difficulty}",
        "question": "The capital of France is _____.",
        "answer": "Paris",
        "explanation": "Paris is the capital and largest city of France."
    }}
    
    Your response:
    """
    return PromptTemplate(template=base_template, input_variables=[])