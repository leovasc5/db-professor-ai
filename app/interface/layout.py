import streamlit as st
import zipfile

st.set_page_config(
        page_title="DB Professor AI",
        page_icon="🧊",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

def render_layout():
    st.subheader("Insira os exercícios a serem corrigidos")
    question_input = st.text_area(
        "Exercício", 
        placeholder="Copie e cole o exercício passado pelo professor aqui.",
        height=300,
        max_chars=10000,
        key="question_input"
    )
    
    st.subheader("Envie os arquivos para correção")
    uploaded_file = st.file_uploader(
        "Arquivo ZIP disponibilizado pelo Moodle", 
        type="zip",
        key="zip_file"
    )
    
    if uploaded_file is not None:
        with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
            file_list = zip_ref.namelist()
            st.write("Arquivos contidos no ZIP:")
            st.write(file_list)
    
    if st.button("Processar", key="process_button"):
        return (question_input, uploaded_file)

render_layout()