import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from utils.student import Student
import time
from utils import files

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
INTERVAL_SECONDS_PER_REQUEST = 60 / int(os.getenv("RPM"))
SECURITY_WAIT = int(os.getenv("SECURITY_WAIT"))
MODEL_NAME = os.getenv("MODEL_NAME")
PROMPT=files.read_file("app/prompts/prompt_template.txt")

generation_config = {
  "temperature": 1.5,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name=MODEL_NAME,
  generation_config=generation_config,
  system_instruction=PROMPT
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
        start_at = time.time()
        response = chat_session.send_message(question + "\n" + student.script)
        feedback = response.text
        end_at = time.time()

        wait(start_at, end_at)
        
        if feedback:
            student.feedback = feedback
            st.success(student.get_name())
            st.write(feedback)
        else:
            st.error("Erro ao gerar o feedback.")
    
    except Exception as e:
        st.error(f"Erro ao processar o feedback: {e}")

def wait(start_at, end_at):
    if end_at - start_at < INTERVAL_SECONDS_PER_REQUEST:
      time.sleep(INTERVAL_SECONDS_PER_REQUEST - (end_at - start_at) + SECURITY_WAIT)