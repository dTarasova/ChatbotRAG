import streamlit as st

from src.rag.rag_model import RAGModel
from src.wo_rag import get_openai_answer
from src.rag.rag_model import RAGTypes



st.write("This chatbot is designed to help you with your questions about Requirements Engineering. Please ask your question below.")

question = st.text_input("Question")
       
if st.button("Ask"):
    try:
        rag_model = RAGModel(text_retriever_type='step-back')
        results = rag_model.query(question, query_types=[RAGTypes.TEXT_DATA, RAGTypes.STRUCTURED_DATA, RAGTypes.COMBINED, RAGTypes.SUMMARISER]).get('answers')

        col1, col2 = st.columns(2)

        answerGPT = get_openai_answer(question)
        

        with col1:
            st.header(f"Answer with chatGPT:")
            st.write(answerGPT)

        with col2:
            st.header(f"Answer with RAG Model:")
            answer = results[0].get('answer')
            st.write(answer)
            st.header(f"Context:") 
            context = results[3].get('context')
            st.write(context)
    except Exception as e:
        st.write("Sorry, I could not find an answer to your question. Please try again later.")
        st.write(e)       