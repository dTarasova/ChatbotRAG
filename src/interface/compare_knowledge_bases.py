import streamlit as st
from typing import Dict, Any

from src.interface.helper_functions import load_questions, load_results
from src.rag.rag_model import RAGModel, RAGTypes
PATH_DB_AMDIRE_NAPIRE = 'knowledge_bases/amdire_napire'
PATH_DB_AMDIRE_NAPIRE_SOFTWARE4KMU = 'knowledge_bases/amdire_napire_software4kmu_chroma'
PATH_DB_ALL = 'knowledge_bases/all'

# Display results in a multi-column layout for comparison
def display_results(question: str, model_results: Dict[str, Any]):
    st.write(f"## Question: {question}")
    number_of_models = len(model_results)
    cols = st.columns(number_of_models)
    
    # Iterate over the models and their results with enumerate to track the index
    for i, (model_name, data) in enumerate(model_results.items()):
        with cols[i]:
            # Column 1: Model name
            st.write(f"### Model: {model_name}")

            # Display evaluation data if available
            if "evaluation" in data:
                completeness = data["evaluation"].get("completeness", "N/A")
                relevance = data["evaluation"].get("relevance", "N/A")
                st.write(f"**Completeness**: {completeness}")
                st.write(f"**Relevance**: {relevance}")
            else:
                st.write("No Evaluation Data")

            # Display the answer and context
            st.write(f"**Answer**: {data.get('answer', 'No Answer')}")
            st.write(f"**Context**: {data.get('context', 'No Context')}")

# Create different RAG models with varying paths to database directories
def create_rag_models():
    model1 = RAGModel(path_to_db_directory=PATH_DB_AMDIRE_NAPIRE, evaluate_answers=True)
    model2 = RAGModel(path_to_db_directory=PATH_DB_AMDIRE_NAPIRE_SOFTWARE4KMU, evaluate_answers=True)
    model3 = RAGModel(path_to_db_directory=PATH_DB_ALL, evaluate_answers=True)
    return {"Amdire and Napire": model1, "+ software4kmu": model2, "all": model3}


st.title("RAG Model Comparison Viewer")

# Load results and questions
results = load_results()
questions = load_questions()
st.write(f"Loaded {len(questions)} questions and {len(results)} results.")

if "question_number" not in st.session_state:
    st.session_state.question_number = 0
if st.button("Next Question"):
    st.session_state.question_number += 1
    if st.session_state.question_number >= len(questions):
        st.session_state.question_number = 0

question = questions[st.session_state.question_number]
st.write(f"Current question: {question}")
st.write(f"Question number: {st.session_state.question_number}")

st.write("Querying the RAG models...")
rag_models = create_rag_models()
model_results = {}
    
# Query each model with TEXT_DATA query type
for model_name, rag_model in rag_models.items():
    result = rag_model.query(question=question, query_types=[RAGTypes.TEXT_DATA])
    model_results[model_name] = result["models"][RAGTypes.TEXT_DATA.name]

# Display the results for all models in comparison
display_results(question, model_results)
