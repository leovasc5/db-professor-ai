import streamlit as st
import zipfile

def render_layout():    
    st.subheader("Insira os exercícios a serem corrigidos")
    question_input = st.text_area(
        "Exercício", 
        placeholder = "Copie e cole o exercício passado pelo professor aqui.",
        height = 300,
        max_chars = 10000,
        key= "unique_question_input"
    )
    
    st.subheader("Envie os arquivos para correção")
    uploaded_file = st.file_uploader(
        "Arquivo ZIP disponibilizado pelo Moodle", 
        type = "zip",
        key = "unique_zip_file"
    )
    
    if uploaded_file is not None:
        with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
            file_list = zip_ref.namelist()
            st.write("Arquivos contidos no ZIP:")
            st.write(file_list)
    
    if st.button("Processar", key=f"unique_button"):
        return (question_input, uploaded_file)

render_layout()