import json
import streamlit as st
import random
import os
import time
import datetime

from src.rag.rag_model import RAGModel, RAGTypes
from src.wo_rag import get_openai_answer
from src.interface.helper_functions import get_answer, load_questions, load_results, normalize

def log_choice(question, answerGPT, answerRAG, correct_model, preferred_model, choice_explanation):
    log_entry = {
        "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "question": question,
        "answers": {
            "GPT": answerGPT,
            "RAG": answerRAG
        },
        "user_choice": {
            "correct_model": correct_model,
            "preferred_model": preferred_model,
            "choice_explanation": choice_explanation
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
    results = rag_model.query(question, query_types=[RAGTypes.GPT, RAGTypes.COMBINED])
    answerRAG = results["models"][RAGTypes.COMBINED.name]["answer"]
    answerGPT = results["models"][RAGTypes.GPT.name]["answer"]
    # context = results["models"][RAGTypes.SUMMARISER.name]["context"]
    # print("context ", context)
    # time.sleep(5)
    # answerRAG = "RAG answer" + question
    # answerGPT = "GPT answer" + question
    # answerRAG = results[0].get('answer')
    return answerGPT, answerRAG


# Initialize session state variables if not present
if "questions" not in st.session_state:
    st.session_state.questions = []
if "logging" not in st.session_state:
    st.session_state.logging = {}

st.title("Compare RAG Chatbot and ChatGPT Answers")
st.markdown("<h6>Type a question to compare answers. Press Enter to receive answers.</h3>", unsafe_allow_html=True)
# Text input for the user to enter a question
question = st.text_input("Type a question to compare answers. Press Enter to receive answers.", key="key_question", label_visibility="collapsed")
st.divider()

results = load_results()


if question and question not in st.session_state.questions:
    # Get answers from the models
    
    found_item = next((item for item in results if normalize(item['question']) == normalize(question)), None)
    if found_item:
        model_results = found_item["models"]
        #st.write("Results already exist for this question."
        if RAGTypes.COMBINED.name in model_results:
            answerRAG = model_results[RAGTypes.COMBINED.name]["answer"]
        else: 
            answerRAG = get_answer(question, RAGTypes.COMBINED)
        if RAGTypes.GPT.name in model_results:
            answerGPT = model_results[RAGTypes.GPT.name]["answer"]
        else:
            answerGPT = get_answer(question, RAGTypes.GPT)
        
    else:
        # Query the RAG model if the answer doesn't exist
        st.write("Querying the RAG model...")
        
        answerGPT, answerRAG = get_model_answers(question)
    
    # Randomize the order of the answers
    answers = [(answerGPT, 'GPT'), (answerRAG, 'RAG')]
    random.shuffle(answers)
    # st.write(f"Shuffled Answers: {answers}")
    
    # Store the question and answers in session state
    st.session_state.questions.append(question)
    st.session_state.logging[question] = answers

# Check if the question exists in session state
if question and question in st.session_state.logging:
     # Show radio buttons for selecting the better answer
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Answer 1 (Left)")
        st.write(st.session_state.logging[question][0][0])
    with col2:
        st.subheader("Answer 2 (Right)")
        st.write(st.session_state.logging[question][1][0])


    st.divider()    
    st.markdown("<h6>Which of the following answers is correct?</h3>", unsafe_allow_html=True)
    correctness_choice = st.radio("Correctness", ("Answer 1 (Left)", "Answer 2 (Right)", "Neither", "Both"), label_visibility="collapsed")
    st.markdown("<h6>If you had to choose, which answer would you prefer? </h6> ", unsafe_allow_html=True)
    st.markdown("<h6>Please choose the option that is more factually accurate, free from misleading or contradictory information, and offers deeper expertise and knowledge from an expert perspective.</h3>", unsafe_allow_html=True)
    preferred_choice = st.radio("Preferred", ("Answer 1 (Left)", "Answer 2 (Right)"), label_visibility="collapsed")
    st.markdown("<h6>Please provide a reason for your choice</h3>", unsafe_allow_html=True)
    choice_explanation = st.text_area("Reasoning", key="key_explanation", label_visibility="collapsed")

    submit_button = st.button("Submit your choice", key="key_submit")

        # Display the answers side by side
    # Button to submit the choice
    if submit_button:
        
        # Determine the model based on randomized display order
        if preferred_choice == "Answer 1 (Left)":
            #user_preferred_choice = st.session_state.logging[question][0][0]
            preferred_model = st.session_state.logging[question][0][1]
        else:
            #user_preferred_choice = st.session_state.logging[question][1][0]
            preferred_model = st.session_state.logging[question][1][1]
        st.write(f"User's preferred model: {preferred_model}")
        if correctness_choice == "Answer 1 (Left)":
            correct_model = st.session_state.logging[question][0][1]
        elif correctness_choice == "Answer 2 (Right)":
            correct_model = st.session_state.logging[question][1][1]
        elif correctness_choice == "Both":
            correct_model = "Both"
        else:
            correct_model = "Neither"

        if st.session_state.logging[question][0][1] == "RAG":
            answerRAG = st.session_state.logging[question][0][0]
            answerGPT = st.session_state.logging[question][1][0]
        else:
            answerGPT = st.session_state.logging[question][0][0]
            answerRAG = st.session_state.logging[question][1][0]
        
        log_choice(
            question=question,
            answerGPT=answerGPT,
            answerRAG=answerRAG,
            correct_model=correct_model,
            preferred_model=preferred_model,
            choice_explanation=choice_explanation
        )
        
        st.success(f"Your choice has been logged! You selected: {preferred_model}")


