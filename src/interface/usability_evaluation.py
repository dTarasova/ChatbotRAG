import streamlit as st
from src.rag.rag_model import RAGModel
from src.wo_rag import get_openai_answer
from src.rag.rag_model import RAGTypes
import datetime

st.write("""Hi there! This is the LLM-based educational chatbot for Requirements Engineering (RE). It uses evidence-based data sources to provide users in-depth insights on the topic.
            \n We would love your help in evaluating the usability of the chatbot! Please ask at least five questions related to requirements engineering. 
            \n This is an educational chatbot whose primary purpose is to explain concepts, suggest techniques and provide examples in the Requirements Engineering domain. 
            \n Its application to concrete projects without enough relevant context is limited. 
            \n When testing, please evaluate the chatbot's answers based on their relevance, clarity, level of detail, and applicability for educational purposes. 
            \n Please submit your feedback with this questionnaire: https://forms.gle/vxvaRmMr6EHjmZNJ9""")
st.markdown("<h6>Type a question, press 'Ask button' to receive answer.</h3>", unsafe_allow_html=True)
question = st.text_input("Question", key="key_question", label_visibility="collapsed")

if st.button("Ask"):
    try:
        # Initialize the RAG model
        st.write("Processing the question... Please be aware it might take up to 1-2 minutes.")
        rag_model = RAGModel(text_retriever_type='step-back')
        
        # Query the model
        results = rag_model.query(question, query_types=[RAGTypes.COMBINED])
        
        # Debug: print the entire results structure for checking
        # st.write("Results structure:", results)

        # Access the answer from the model response
        answer = results["models"][RAGTypes.COMBINED.name]["answer"]
        context = results["models"][RAGTypes.COMBINED.name]["context"]
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("\n\n\n Usability evaluation")	
        print("timestamp: ", time)
        print("\n Question:", question)  
        print("\n\n Answer:", answer)
        print("\n\n Context:", context)

        
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
