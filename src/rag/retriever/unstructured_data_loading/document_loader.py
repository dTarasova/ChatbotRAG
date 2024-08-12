import re

import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb
import pymupdf
from  langchain_core.documents.base import Document

from src.rag.retriever.unstructured_data_loading.pdf_preprocessor import process_pdf


PATH_DOCUMENTS = 'data/first_batch'
PERSIST_DIRECTORY = 'chroma_db'
EXAMPLE_FILE_PATH = 'data/first_batch/Rapid quality assurance with Requirements Smells.pdf'

def create_db(path_to_documents: str = PATH_DOCUMENTS) -> Chroma:
    # docs = [file for file in listdir(PATH_DOCUMENTS) if path.isfile(
    #     path.join(path_to_documents, file))]

    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=300, chunk_overlap=50)
    # pages = []

    # for doc in docs:
    #     # Split
    #     doc_path = path.join(PATH_DOCUMENTS, doc)
    #     loader = PyMuPDFLoader(doc_path)

    #     text = loader.load_and_split(text_splitter=text_splitter)

    #     #filtered_text = filter_text(text)

    #     pages.extend(text)

    # vectorstore = Chroma.from_documents(documents=pages,
    #                                     embedding=OpenAIEmbeddings(),
    #                                     persist_directory=PERSIST_DIRECTORY)
    vector_store = chromadb.PersistentClient(path=PERSIST_DIRECTORY)
    add_docs_from_folder(path_to_documents)
    return vector_store



def get_db():
    # vector_store = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=OpenAIEmbeddings())
    # result = vector_store.search("artefact-oriented re", search_type="similarity")
    vector_store = chromadb.PersistentClient(path=PERSIST_DIRECTORY)
    collections = vector_store.list_collections()
    if collections.count == 0:
        print("There are no collections in db")
    for collection in collections:
        print("\n\nnumber of items in the collection: " + str(collection.count()))
        # print(collection.peek(limit=1))
    return vector_store


def add_doc_todb(doc_path):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300, chunk_overlap=50)

    # loader = PyMuPDFLoader(doc_path)

    # pages = loader.load_and_split(text_splitter=text_splitter)
    head, tail = os.path.split(doc_path)

    processed_pdf = process_pdf(doc_path, tail+'.txt')

    pages = text_splitter.split_text(processed_pdf)

    documents = [Document(page_content=page, metadata={"source": tail}) for page in pages]

    vector_store = Chroma(persist_directory=PERSIST_DIRECTORY,
                          embedding_function=OpenAIEmbeddings())
    vector_store.add_documents(documents)
    print("Document " + doc_path + " added to db")


def add_docs_from_folder(folder_path):
    docs = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]

    for doc in docs:
        doc_path = os.path.join(folder_path, doc)
        add_doc_todb(doc_path)


"""For more refined document adding 
from langchain.docstore.document import Document

new_doc =  Document(
    page_content="Wareconn is the best web platform for warranty maintenance.",
    metadata={
        "source": "wareconn.com",
        "page": 1
    }
)


Expertiment 1.
number of items in the collection: 1964
number of items in the collection: 2526
Still one collection

TODO: Experiment 2 
Added a filtering function for text, so that it doesn't include content 
"""