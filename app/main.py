import os
import streamlit as st
import zipfile
from utils.student import Student
from interface.layout import render_layout
from services.ai_generator import process_feedback

def main():
    st.title("Feedback de Exercícios de SQL com IA Generativa")
    
    response = render_layout()

    if response:
        question_input, uploaded_file = response

        if question_input and uploaded_file:
            with st.spinner('Analisando conteúdo...'):
                students = extract_students(uploaded_file)
                create_feedback(question_input, students)

                padding(3)

                st.success("Feedbacks gerados com sucesso! Você pode baixar um PDF com os feedbacks na parte superior direita da tela.")

def extract_students(zip_file):
    students = []

    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        for file_name in zip_ref.namelist():
            student_name = os.path.dirname(file_name).split('/')[-1]
            
            if file_name.endswith(".sql"):
                with zip_ref.open(file_name) as sql_file:
                    sql_content = sql_file.read().decode("utf-8")
                    
                    student = Student(name=student_name, script=sql_content)
                    students.append(student)
    return students

def create_feedback(question_input, students):
    for student in students:
        with st.spinner(f"Corrigindo exercício do aluno {student.get_name()}..."):
            process_feedback(question_input, student)
            padding(2)

def padding(size: int):
    for _ in range(size):
        st.write(" ")

if __name__ == "__main__":
    main()
