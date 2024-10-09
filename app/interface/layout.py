import streamlit as st
import zipfile
import random
import io

def render_layout():
    key = random.randint(0, 100000)
    
    st.subheader("Insira os exercícios a serem corrigidos")
    question_input = st.text_area(
        "Exercício", 
        placeholder = "Copie e cole o exercício passado pelo professor aqui.",
        height = 300,
        max_chars = 10000,
        key= f"unique_question_input{key}"
    )
    
    st.subheader("Envie os arquivos para correção")
    uploaded_file = st.file_uploader(
        "Arquivo ZIP disponibilizado pelo Moodle", 
        type = "zip",
        key = f"unique_zip_file{key}"
    )
    
    if uploaded_file is not None:
        with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
            file_list = zip_ref.namelist()
            st.write("Arquivos contidos no ZIP:")
            st.write(file_list)
    
    if st.button("Processar", key=f"unique_button{key}"):
        return (question_input, uploaded_file)
    
    return None

render_layout()