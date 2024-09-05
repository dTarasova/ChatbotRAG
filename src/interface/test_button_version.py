import streamlit as st
from src.rag.rag_model import RAGModel
from src.wo_rag import get_openai_answer
from src.rag.rag_model import RAGTypes

# todo: doesn't work button reflection(
# Initialize session state for counters if not already done
if 'counterGPT' not in st.session_state:
    st.session_state.counterGPT = 0
if 'counterRAG' not in st.session_state:
    st.session_state.counterRAG = 0

st.write("Please Enter Your name for the evaluation: ")

name = st.text_input("Name")

st.write("This chatbot is designed to help you with your questions about Requirements Engineering. Please ask your question below.")

question = st.text_input("Question")

if st.button("Ask"):
    try:
        rag_model = RAGModel(text_retriever_type='step-back')
        # results = rag_model.query(question, query_types=[RAGTypes.TEXT_DATA, RAGTypes.STRUCTURED_DATA, RAGTypes.COMBINED, RAGTypes.SUMMARISER]).get('answers')
        results = rag_model.query(question, query_types=[RAGTypes.TEXT_DATA]).get('answers')
        col1, col2 = st.columns(2)

        answerGPT = get_openai_answer(question)

        with col1:
            st.header(f"Answer with chatGPT:")
            buttonGPT = st.button("Answer with chatGPT is better", key="gpt_button")
            st.write(answerGPT)

        with col2:
            st.header(f"Answer with RAG Model:")
            buttonRAG = st.button("Answer with RAG Model is better", key="rag_button")
            answer = results[0].get('answer')
            st.write(answer)
            st.header(f"Context:")
            context = results[0].get('context')
            st.write(context)

        # # Update counters based on button clicks
        # if buttonGPT or buttonRAG: 
        #     if buttonGPT:
        #         st.session_state.counterGPT += 1
        #     if buttonRAG:
        #         st.session_state.counterRAG += 1

        #     # Write evaluation results to the file
        #     with open("evaluation.txt", "a") as file:
        #         file.write(f"Name: {name}\n")
        #         file.write(f"Question: {question}\n")
        #         file.write(f"Answer with chatGPT: {answerGPT}\n")
        #         file.write(f"Answer with RAG Model: {answer}\n")
        #         file.write(f"Context: {context}\n")
        #         file.write(f"Counter GPT: {st.session_state.counterGPT}\n")
        #         file.write(f"Counter RAG: {st.session_state.counterRAG}\n")
        #         file.write("\n")

        # Update counters based on button clicks
        if buttonGPT:
            st.session_state.counterGPT += 1
            with open("evaluation.txt", "a") as file:
                file.write(f"Name: {name}\n")
                file.write(f"Question: {question}\n")
                file.write(f"Answer with chatGPT: {answerGPT}\n")
                file.write(f"Answer with RAG Model: {answer}\n")
                file.write(f"Context: {context}\n")
                file.write(f"Won: GPT\n")
                file.write("\n")
        if buttonRAG:
            st.session_state.counterRAG += 1
            with open("evaluation.txt", "a") as file:
                file.write(f"Name: {name}\n")
                file.write(f"Question: {question}\n")
                file.write(f"Answer with chatGPT: {answerGPT}\n")
                file.write(f"Answer with RAG Model: {answer}\n")
                file.write(f"Context: {context}\n")
                file.write(f"Won: RAG\n")
                file.write("\n")

    except Exception as e:
        st.write("Sorry, I could not find an answer to your question. Please try again later.")
        st.write(e)
