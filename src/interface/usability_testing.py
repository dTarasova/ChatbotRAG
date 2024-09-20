import json
import streamlit as st
import random
import os
import datetime

from src.rag.rag_model import RAGModel, RAGTypes
from src.wo_rag import get_openai_answer

def log_choice(question, answerGPT, answerRAG, user_choice, selected_model):
    log_entry = {
        "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "question": question,
        "answers": {
            "GPT": answerGPT,
            "RAG": answerRAG
        },
        "user_choice": {
            "selected_model": selected_model
        }
    }

    filename = "model_comparisons.json"
    
    # Check if file exists and is non-empty
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        # Append the new entry to the existing JSON data
        with open(filename, "r+") as f:
            file_data = json.load(f)
            file_data.append(log_entry)  # Append new data
            f.seek(0)  # Move the cursor to the start of the file to overwrite
            json.dump(file_data, f, indent=4)
    else:
        # Create a new JSON file with the first log entry
        with open(filename, "w") as f:
            json.dump([log_entry], f, indent=4)

# Function to get answers from two different models
def get_model_answers(question):
    rag_model = RAGModel(text_retriever_type='step-back')
    results = rag_model.query(question, query_types=[RAGTypes.SUMMARISER])
    answerRAG = results["models"][RAGTypes.SUMMARISER.name]["answer"]
    # context = results["models"][RAGTypes.COMBINED.name]["context"]
    answerGPT = get_openai_answer(question)
    # answerRAG = results[0].get('answer')
    return answerGPT, answerRAG

# Initialize session state variables if not present
if "questions" not in st.session_state:
    st.session_state.questions = []
if "logging" not in st.session_state:
    st.session_state.logging = {}

st.title("Compare RAG Chatbot and ChatGPT Answers")

# Text input for the user to enter a question
question = st.text_input("Enter a question to compare answers:")

if question and question not in st.session_state.questions:
    # Get answers from the models
    answerGPT, answerRAG = get_model_answers(question)
    
    # Randomize the order of the answers
    answers = [(answerGPT, 'GPT'), (answerRAG, 'RAG')]
    random.shuffle(answers)
    
    # Store the question and answers in session state
    st.session_state.questions.append(question)
    st.session_state.logging[question] = answers

# Check if the question exists in session state
if question and question in st.session_state.logging:
     # Show radio buttons for selecting the better answer
    choice = st.radio("Which answer is better?", ("Answer 1 (Left)", "Answer 2 (Right)"))

    # Button to submit the choice
    if st.button("Submit your choice"):
        # Determine the model based on randomized display order
        if choice == "Answer 1 (Left)":
            user_choice = st.session_state.logging[question][0][0]
            selected_model = st.session_state.logging[question][0][1]
        else:
            user_choice = st.session_state.logging[question][1][0]
            selected_model = st.session_state.logging[question][1][1]
        
        # Log the choice to a file
        log_choice(question, st.session_state.logging[question][0][0], st.session_state.logging[question][1][0], user_choice, selected_model)
        
        st.success(f"Your choice has been logged! You selected: {selected_model}")
    
    # Display the answers side by side
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Answer 1 (Left)")
        st.write(st.session_state.logging[question][0][0])
    with col2:
        st.subheader("Answer 2 (Right)")
        st.write(st.session_state.logging[question][1][0])
    
   
