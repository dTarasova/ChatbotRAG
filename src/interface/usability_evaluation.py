import streamlit as st
from src.rag.rag_model import RAGModel
from src.wo_rag import get_openai_answer
from src.rag.rag_model import RAGTypes

st.write("""This is the LLM-based educational chatbot for Requirements Engineering (RE).   \n It uses evidence-based data sources to provide users in-depth insights on the topic. 
            \n Please help us evaluate the usability of the chatbot. 
         Kindly ask at least five questions about requirements engineering for evaluation.   \n Please submit your feedback with this questionnaire: https://forms.gle/vxvaRmMr6EHjmZNJ9""")
st.markdown("<h6>Type a question to compare answers. Press 'Ask button' to receive answers.</h3>", unsafe_allow_html=True)
question = st.text_input("Question", key="key_question", label_visibility="collapsed")

if st.button("Ask"):
    try:
        # Initialize the RAG model
        st.write("Processing the question... Please be aware it might take 1-2 minutes.")
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
