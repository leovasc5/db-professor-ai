import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from utils.student import Student
import time

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
INTERVAL_SECONDS_PER_REQUEST = 60 / int(os.getenv("RPM"))

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
  system_instruction="Você é um assistente de banco de dados especializado em consultas de linguagem natural. Você receberá uma lista de exercícios de banco de dados MySQL e um script de texto dos comandos que um determinado aluno executou. Você terá de responder destacando os principais erros do exercício, pontos de atenção e melhorias, como se fosse um professor corrigindo a lição de um aluno. Você deve responder no seguinte formato: Erros na interpretação do exercício: Liste onde o aluno fez códigos que não correspondem ao que foi solicitado no exercício.",
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
      time.sleep(INTERVAL_SECONDS_PER_REQUEST - (end_at - start_at))