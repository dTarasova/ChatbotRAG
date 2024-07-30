
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

st.title("Requirements Engineering Chatbot")

st.write("This chatbot is designed to help you with your questions about Requirements Engineering. Please ask your question below.")

question = st.text_input("Question")

if st.button("Ask"):
    rag_model = RAGModel(text_retriever_type='step-back')
    answer, context, results = rag_model.query(question)
    col1, col2, col3 = st.columns(3)
    # results = json.load(open('results.json'))
    # todo align results and context
    # todo adjust the database agent. why it not foun d relevant columns? 
    col1.header(f"Answer with: {results[1]['model']}")
    col1.write(results[1]['answer'])
    col1.header(f"Context:")
    col1.write(results[1]['context'])

    col2.header(f"Answer with: {results[2]['model']}")
    col2.write(results[2]['answer'])
    col2.header(f"Context:")
    col2.write(results[2]['context'])

    col3.header(f"Answer with: {results[3]['model']}")
    col3.write(results[3]['answer'])
    col3.header(f"Context:")
    col3.write(results[3]['context'])

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
