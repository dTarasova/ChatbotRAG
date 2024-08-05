import streamlit as st

from src.rag_model import RAGModel
from src.wo_rag import get_openai_answer


def setup_streamlit():
    st.set_page_config(
        page_title="Requirements Engineering Chatbot",
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state="auto",
    )

    st.write("This chatbot is designed to help you with your questions about Requirements Engineering. Please ask your question below.")



def test_final_version():

    question = st.text_input("Question")
       
    if st.button("Ask"):
        rag_model = RAGModel(text_retriever_type='step-back')
        answer, context, results = rag_model.query(question)
        col1, col2 = st.columns(2)

        answerGPT = get_openai_answer(question)
        

        with col1:
            st.header(f"Answer with chatGPT:")
            st.write(answerGPT)

        with col2:
            st.header(f"Answer with RAG Model:")
            st.write(answer)
            st.header(f"Context:")  
            st.write(context)
       

def test_3types_of_text():
    st.write("This chatbot is designed to help you with your questions about Requirements Engineering. Please ask your question below.")
    question = st.text_input("Question")
    if st.button("Ask"):
        rag_model = RAGModel(text_retriever_type='step-back')
        answer, context, results = rag_model.query(question)
        col1, col2, col3 = st.columns(3)
        # results = json.load(open('results.json'))
        # todo align results and context
        # todo adjust the database agent. why it not foun d relevant columns? 
        col1.header(f"Answer with: {results[1]['model']}")
        col1.write(results[1]['answer'])
        col1.header(f"Context:")
        col1.write(results[1]['context'])

        col2.header(f"Answer with: {results[2]['model']}")
        col2.write(results[2]['answer'])
        col2.header(f"Context:")
        col2.write(results[2]['context'])

        col3.header(f"Answer with: {results[3]['model']}")
        col3.write(results[3]['answer'])
        col3.header(f"Context:")
        col3.write(results[3]['context'])