import streamlit as st

from src.rag.rag_model import RAGModel
from src.wo_rag import get_openai_answer
from src.rag.rag_model import RAGTypes



st.write("This chatbot is designed to help you with your questions about Requirements Engineering. Please ask your question below.")

question = st.text_input("Question")
       
if st.button("Ask"):
    try:
        rag_model = RAGModel(text_retriever_type='step-back')
        results = rag_model.query(question, query_types=[RAGTypes.SUMMARISER]).get('answers')
        print(results["models"][RAGTypes.SUMMARISER.name]["answer"])

        st.header(f"Answer:")
        # answer = results[0].get('answer')
        answer = results["models"][RAGTypes.SUMMARISER.name]["answer"]
        context = results["models"][RAGTypes.SUMMARISER.name]["context"]
        st.write(answer)
        # st.header(f"Context:") 
        # context =  results["models"][RAGTypes.TEXT_DATA.name]["context"]
        # st.write(context)
    except Exception as e:
        st.write("Sorry, I could not find an answer to your question. Please try again later.")
        st.write(e)       