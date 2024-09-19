from termcolor import colored

from src.rag.evaluation.generate_test_set import get_contexts
from src.rag.rag_model import RAGModel, RAGTypes
from src.interface.streamlit_incorporation import setup_streamlit 

setup_streamlit()
#test_final_version()
# TODO: adjust prompts so that it relies more on the context not the general knowledge
# try:
#     while True:
#         print(colored("\nHow can I help you? For the end of the conversation please press Ctrl+c", "blue"))
#         question = input()
#         rag_model = RAGModel(text_retriever_type='step-back')
#         print_context = True
#         query_types=[RAGTypes.TEXT_DATA, RAGTypes.STRUCTURED_DATA, RAGTypes.COMBINED, RAGTypes.SUMMARISER]
#         #query_types=[RAGTypes.STRUCTURED_DATA]
#         results = rag_model.query(question, query_types)
#         print(results)
#         answer = results["models"][RAGTypes.STRUCTURED_DATA.name]["answer"]
#         context = results["models"][RAGTypes.STRUCTURED_DATA.name]["context"]
#         evaluation = results["models"][RAGTypes.STRUCTURED_DATA.name]["evaluation"]
#         print(evaluation)
#         # print(colored(("\n\nAnswer:\n\n"), "blue"))
#         # print((results["answers"][0]["answer"]))    
#         # if print_context:
#         #     print(colored("\n\nContext:\n\n", "blue"))
#         #     print(context)

# except KeyboardInterrupt:
#     pass

#############################################################################

# import json
# import streamlit as st
# import random
# import os
# import datetime
# import streamlit as st
# import json
# import os
# from typing import Dict, Any
# import pandas as pd

# from src.rag.rag_model import RAGModel, RAGTypes
# from src.wo_rag import get_openai_answer


# # Load the results from results.json
# def load_results() -> Dict[str, Any]:
#     if os.path.exists('results.json'):
#         with open('results.json', 'r') as f:
#             return json.load(f)
#     return {}

# # Save the results back to results.json
# def save_results(results: Dict[str, Any]):
#     with open('results.json', 'a') as f:
#         json.dump(results, f, indent=4)

# # Load questions from evaluation_questions.txt
# def load_questions() -> list[str]:
#     with open('evaluation_questions.txt', 'r') as f:
#          return [line.strip() for line in f.readlines()]
    

# results = load_results()
# questions = load_questions()
# number = 0
# search_question = questions[number]
# found_item = next((item for item in results if item['question'] == search_question), None)
# if found_item:
#     print("Found")


########################################################################################

# if question in results:
#     model_results = results[question]["models"]
#     print("Results already exist for this question.")
# else:
#     # Query the RAG model if the answer doesn't exist
#     print("Querying the RAG model...")
#     rag_model = RAGModel()
#     result = rag_model.query(question=question, query_types=[RAGTypes.TEXT_DATA, RAGTypes.STRUCTURED_DATA, RAGTypes.COMBINED, RAGTypes.SUMMARISER])
#     model_results = result["models"]
    
#     # Add the result to the results dictionary
#     results[question] = result
    
#     # Save updated results
#     save_results(results)

# # Display results in a 5-column layout
# def display_results(question: str, model_results: Dict[str, Any], question_number: int):
#     st.write(f"## Question: {question}")
#     cols = st.columns(5)
#     # Iterate over the models and their results
#     for model_name, data, i in enumerate(model_results.items()):
        
        
#         # Column 1: Model name
#         cols[i].write(f"### Model: {model_name}")
        
#         if "evaluation" in data:
#             correctness = data["evaluation"].get("correctness", "N/A")
#             relevance = data["evaluation"].get("relevance", "N/A")
#             cols[i].write(f"**Correctness**: {correctness}")
#             cols[i].write(f"**Relevance**: {relevance}")
#         else:
#             cols[i].write("No Evaluation Data")
        

#         cols[i].write(f"**Answer**: {data.get('answer', 'No Answer')}")

#         cols[i].write(f"**Context**: {data.get('context', 'No Context')}")
        



# # st.title("Evaluation Results Viewer")
    
# Load results and questions

# st.write(f"Loaded {len(questions)} questions and {len(results)} results.")


# # if "question_number" not in st.session_state:
# #     st.session_state.question_number = 0




# # Display the results in a 5-column format
# display_results(question, model_results)

# if st.button("Next Question"):
#     st.session_state.question_number += 1
#     if st.session_state.question_number >= len(questions):
#         st.session_state.question_number = 0


