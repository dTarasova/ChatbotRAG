
from src.retriever_generator import get_db
from src.document_loader import add_docs_from_folder, create_db
from src.document_preprocessor import process_pdf
from src.rag_model import RAGModel
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from  langchain_core.documents.base import Document

from src.wo_rag import get_openai_answer
from src.structured_data_part.data_preprocessing import improve_csv_quality
from termcolor import colored
import streamlit as st
import json

from streamlit_incorporation import setup_streamlit, test_final_version 

setup_streamlit()
test_final_version()

# try:
#     while True:
#         print(colored("\nHow can I help you? For the end of the conversation please press Ctrl+c", "blue"))
#         question = input()
#         rag_model = RAGModel(text_retriever_type='step-back')
#         print_context = True
#         answer, context = rag_model.query(question)
#         print(colored(("\n\nAnswer:\n\n"), "blue"))
#         print((answer))
#         if print_context:
#             print(colored("\n\nContext:\n\n", "blue"))
#             print(context)

# except KeyboardInterrupt:
#     pass


# What are the main challenges in requirements engineering?
# What are the main techniques of requirements elicitation?
# How to support maintainability of requirements?
# What are the architectural constraints in re?





# folder_path = 'data/second_batch'
# add_docs_from_folder(folder_path)



# from huggingface_hub import InferenceClient
# client = InferenceClient()
# image = client.text_to_image("An astronaut riding a horse on the moon.")
# image.save("astronaut.png")

# Give me a template for a textual use case - not improved
