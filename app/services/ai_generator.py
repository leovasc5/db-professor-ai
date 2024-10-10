import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from utils.student import Student

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
  "temperature": 1.5,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash-8b",
  generation_config=generation_config,
  system_instruction="You are a database assistant specializing in natural language queries. You will be given a list of MySQL database exercises and a text script of the commands that a particular student has done. You will have to respond by highlighting the exercise's main errors, points for attention and improvements, as if you were a teacher correcting a student's lesson.\n\nYou should answer in the following format:\n\nErrors in interpreting the exercise: List where the student has made codes that don't match what was asked in the exercise.\n\nPoints for improvement: Highlight good SQL practices, formatting, typos and queries that could be improved.\n\nPerformance: Rate how well the student did according to the following parameters: Needs improvement, Within expectations, Exceeded expectations.\n\nAlways answer in brazilian portuguese.",
)

chat_session = model.start_chat(
  history=[
  ]
)

        
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
        response = chat_session.send_message(question + "\n" + student.script)
        feedback = response.text

        print(feedback)

        if feedback:
            student.feedback = feedback
            st.success(f"Feedback gerado para {student.get_name()}")

            st.write(f"Feedback para {student.get_name()}:")
            st.write(feedback)
        else:
            st.error("Erro ao gerar o feedback.")
    
    except Exception as e:
        st.error(f"Erro ao processar o feedback: {e}")