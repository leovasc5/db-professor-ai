import streamlit as st
import zipfile
import io

def render_layout():
    """
    Renderiza o layout da interface do usuário e retorna a entrada do usuário.
    """
    
    st.subheader("Insira os exercícios a serem corrigidos")
    user_input = st.text_area(
        "Exercício", 
        placeholder="Copie e cole o exercício passado pelo professor aqui."
    )
    
    st.subheader("Envie os arquivos para correção")
    uploaded_file = st.file_uploader("Arquivo ZIP disponibilizado pelo Moodle", type="zip")
    
    if uploaded_file is not None:
        with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
            file_list = zip_ref.namelist()
            st.write("Arquivos contidos no ZIP:")
            st.write(file_list)
    
    if st.button("Processar"):
        return user_input
    
    return None

render_layout()