
from src.rag.retriever.unstructured_data_loading.document_loader import DocumentDatabase
from src.rag.evaluation.generate_test_set import get_contexts
from src.rag.rag_model import RAGModel, RAGTypes
from src.interface.streamlit_incorporation import setup_streamlit 
from termcolor import colored

#setup_streamlit()


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

# #################
path_db = 'knowledge_bases/tester'
path_data = 'data/software4kmu_helper'
documentDatabase = DocumentDatabase(path_to_db_directory=path_db)
# documentDatabase.add_docs_from_folder(path_data)
# documentDatabase.print_vectorstore_collections()
documents = documentDatabase.check_findings("Subjective Language refers to")
documentDatabase.check_findings("such as almost always, significant and minimal.")
# print(documents)




# # Add all documents from a folder to one or more vector stores
# PATH_AMDIRE_NAPIRE_DOCS = 'data/just amdire and napire papers'
# vector_store_amdire_napire = DocumentDatabase(path_to_documents=PATH_AMDIRE_NAPIRE_DOCS, path_to_db_directory=path_amdire_and_napire_db).get_vectorstore()
# for collection in vector_store_amdire_napire._collection:
#     print(f"Collection: {collection}")
#     print(f"Number of documents in collection: {(vector_store_amdire_napire._collection.count())}")
# add_documents_from_folder(PATH_REQUIREMENTS_DOCS, [vector_store_requirements, vector_store_software4KMU])
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


