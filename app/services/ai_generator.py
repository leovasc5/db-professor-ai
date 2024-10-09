import ollama
from utils.student import Student
from utils.files import read_file
import streamlit as st

MODEL_NAME = 'codellama'
PROMPT_TEMPLATE = read_file("app/prompts/prompt_template.txt")
        
def process_feedback(question: str, student: Student):
    """
    Generate the feedback for the student using generative AI and update the feedback in the Student object.

    Args:
        question (str): The question that will be used as instruction for the AI model.
        std (Student): The object that contains the student information.
        
    Returns:
        None: The feedback is setted in the Student object.
    """
    try:
        prompt = PROMPT_TEMPLATE.format(
            instruction=question,
            student_script=student.script
        )
        
        response = ollama.generate(
            model=MODEL_NAME,
            prompt=prompt,
        )

        print(response)

        exit()

        feedback = response.get('response')

        if feedback:
            student.feedback = feedback
            st.success(f"Feedback gerado para {student.get_name()}")
        else:
            st.error("Erro ao gerar o feedback.")
    
    except Exception as e:
        st.error(f"Erro ao processar o feedback: {e}")