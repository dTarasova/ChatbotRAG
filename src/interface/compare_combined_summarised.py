import streamlit as st
from typing import Dict, Any

from src.interface.helper_functions import load_questions, load_results, normalize
from src.rag.rag_model import RAGModel, RAGTypes


# Display results in a 5-column layout
def display_results(question: str, model_results: Dict[str, Any]):
    st.write(f"## Question: {question}")
    filtered_results = {model_name: data for model_name, data in model_results.items() 
                        if model_name in [RAGTypes.GPT.name, RAGTypes.COMBINED.name, RAGTypes.SUMMARISER.name]}
    number_of_models = len(filtered_results)
    st.write("model results ", number_of_models)
    cols = st.columns(number_of_models)
    
    # Iterate over the models and their results with enumerate to track the index
    for i, (model_name, data) in enumerate(filtered_results.items()):
        # Use index `i` to access the appropriate column
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
        



st.title("Evaluation Results Viewer")
    
# Load results and questions
results = load_results()
questions = load_questions()
st.write(f"Loaded {len(questions)} questions and {len(results)} results.")

# found_item = next((item for item in results if item['question'] == question), None)

if "question_number" not in st.session_state:
    st.session_state.question_number = 0
if st.button("Next Question"):
    st.session_state.question_number += 1
    if st.session_state.question_number >= len(questions):
        st.session_state.question_number = 0

question = questions[st.session_state.question_number]
st.write(f"Current question: {question}")
st.write(f"Question number: {st.session_state.question_number}")

found_item = next((item for item in results if normalize(item['question']) == normalize(question)), None)
if found_item:
    model_results = found_item["models"]
    st.write("Results already exist for this question.")
    
else:
    # Query the RAG model if the answer doesn't exist
    st.write("Querying the RAG model...")
    rag_model = RAGModel(evaluate_answers=True)
    result = rag_model.query(question=question, query_types=[RAGTypes.GPT, RAGTypes.COMBINED, RAGTypes.SUMMARISER])
    model_results = result["models"]
    
# Display the results in a 5-column format
display_results(question, model_results)

