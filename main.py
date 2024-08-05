
from helpers_in_the_past.retriever_generator import get_db
from rag.rag_model import RAGModel
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from  langchain_core.documents.base import Document

from src.wo_rag import get_openai_answer
from termcolor import colored
import streamlit as st
import json

from interface.streamlit_incorporation import setup_streamlit, test_final_version 

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

