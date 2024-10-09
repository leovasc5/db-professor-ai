import streamlit as st
from interface.layout import render_layout
from services.ai_generator import generate_query
from services.database import execute_query
from utils.validators import validate_query
from utils.plot import generate_plot

def main():
    st.title("Feedback de Exercícios de SQL com IA Generativa")
    
    response = render_layout()

    if response:
        question_input, uploaded_file = response

        if question_input:
            with st.spinner('Gerando query...'):
                # Gera a query a partir do prompt do usuário usando a IA
                generated_query, chart_config = generate_query(question_input)

            if generate_query:
                st.subheader("Query Gerada")
                st.code(generated_query, language='sql')
                
                # Valida a query gerada
                if validate_query(generated_query):
                    # Executa a query no banco de dados
                    results = execute_query(generated_query)
                    plot = generate_plot(results, chart_config)
                    
                    # Exibe os resultados
                    st.subheader("Resultados")
                    st.write(results)
                    if plot:
                        st.pyplot(plot)
                else:
                    st.error("A query gerada não é válida. Tente reformular a pergunta.")



    # Processa a entrada do usuário
    # if question_input:
    #     with st.spinner('Gerando query...'):
    #         # Gera a query a partir do prompt do usuário usando a IA
    #         generated_query, chart_config = generate_query(question_input)

    #     if generate_query:
    #         st.subheader("Query Gerada")
    #         st.code(generated_query, language='sql')
            
    #         # Valida a query gerada
    #         if validate_query(generated_query):
    #             # Executa a query no banco de dados
    #             results = execute_query(generated_query)
    #             plot = generate_plot(results, chart_config)
                
    #             # Exibe os resultados
    #             st.subheader("Resultados")
    #             st.write(results)
    #             if plot:
    #                 st.pyplot(plot)
    #         else:
    #             st.error("A query gerada não é válida. Tente reformular a pergunta.")
    
if __name__ == "__main__":
    main()
