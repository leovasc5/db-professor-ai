import ollama
from utils.files import read_file
from utils.student import Student
from services.database import get_db_structure
import re
import unidecode
import streamlit as st

# Configurações da API
MODEL_NAME = 'codellama'
PROMPT_TEMPLATE = read_file("app/prompts/prompt_template.txt")
        
def process_feedback(question: str, student: Student):
    """
    Gera o feedback para o aluno usando IA generativa e atualiza o feedback no objeto Student.
    
    Args:
        question (str): A pergunta que será usada como instrução para o modelo de IA.
        std (Student): O objeto Student contendo o script do aluno e outros dados.
        
    Returns:
        None: O feedback é salvo diretamente no objeto Student.
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


def generate_query(user_input: str) -> str:
    """
    Gera uma query SQL a partir da entrada do usuário usando IA generativa.
    
    Args:
        user_input (str): A consulta em linguagem natural fornecida pelo usuário.
        
    Returns:
        str: A query SQL gerada pelo modelo de IA.
    """
    try:
        isCorrect = False
        prompt_template = read_file("app/prompts/prompt_template.txt")
        db_structure = get_db_structure()

        if not db_structure:
            return None, None
        
        prompt = prompt_template.format(
            instruction=user_input,
            db_structure=db_structure
        )
        
        while not isCorrect:
            # Chama a API do modelo de IA para gerar a query
            response = ollama.generate(
                model=MODEL_NAME,
                prompt=prompt,
            )

            print(response.get('response'))

            query, chart_type, y_chart_value, x_chart_value = extract_values(response.get('response'))
            chart_config = {
                "chart_type": chart_type, 
                "y_chart_value": y_chart_value,
                "x_chart_value": x_chart_value
            }

            if query:
                isCorrect = True

            print(chart_config)
        
        return query, chart_config
    
    except Exception as e:
        st.error(f"Erro ao gerar a query: {e}")
        return ""