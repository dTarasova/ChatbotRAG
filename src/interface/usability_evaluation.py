import streamlit as st
from src.rag.rag_model import RAGModel
from src.wo_rag import get_openai_answer
from src.rag.rag_model import RAGTypes

st.write("This chatbot is designed to help you with your questions about Requirements Engineering. Please ask your question below.")

question = st.text_input("Question")

if st.button("Ask"):
    try:
        # Initialize the RAG model
        st.write("Processing the question...")
        rag_model = RAGModel(text_retriever_type='step-back')
        
        # Query the model
        results = rag_model.query(question, query_types=[RAGTypes.SUMMARISER])
        
        # Debug: print the entire results structure for checking
        # st.write("Results structure:", results)

        # Access the answer from the model response
        answer = results["models"][RAGTypes.SUMMARISER.name]["answer"]
        context = results["models"][RAGTypes.SUMMARISER.name]["context"]
        
        # Display the answer
        st.header("Answer:")
        st.write(answer)
        
        # Optionally display the context
        # st.header("Context:")
        # st.write(context)
        
    except KeyError as ke:
        st.write("The expected key was not found in the response. Please check the structure of the model's output.")
        st.write(f"KeyError: {ke}")
        
    except Exception as e:
        st.write("Sorry, I could not find an answer to your question. Please try again later.")
        st.write(f"Error: {e}")
