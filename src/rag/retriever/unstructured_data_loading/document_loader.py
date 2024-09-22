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


PATH_DOCUMENTS = 'data/just amdire and napire papers'
PERSIST_DIRECTORY = 'knowledge_bases/amdire_and_napire'
EXAMPLE_FILE_PATH = 'data/first_batch/Rapid quality assurance with Requirements Smells.pdf'

class DocumentDatabase:
    def __init__(self, path_to_documents='data/just amdire and napire papers', path_to_db_directory='knowledge_bases/amdire_and_napire'):
        self.path_to_documents = path_to_documents
        self.path_to_db_directory = path_to_db_directory
        self.vector_store = Chroma(persist_directory=path_to_db_directory, embedding_function=OpenAIEmbeddings())

    def create_db(self) -> Chroma:
        """Create and return the vector store client."""
        # self.vector_store = chromadb.PersistentClient(path=self.path_to_db_directory)
        self.add_docs_from_folder(self.path_to_documents)
        return self.vector_store
     
    def get_vectorstore(self) -> Chroma:
        return self.vector_store

    def add_doc_todb(self, doc_path: str):
        """Process and add a document to the vector store."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=400, chunk_overlap=50,
            strip_whitespace=True,
            separators=["\n\n", "\n", ".", " ", ""]
        )

        head, tail = os.path.split(doc_path)
        processed_pdf = process_pdf(doc_path, tail+'.txt')

        pages = text_splitter.split_text(processed_pdf)
        documents = [Document(page_content=page, metadata={"source": tail}) for page in pages]

        if not self.vector_store:
            self.vector_store = Chroma(persist_directory=self.path_to_db_directory, embedding_function=OpenAIEmbeddings())

        self.vector_store.add_documents(documents)
        print(f"Document {doc_path} added to db")

    def add_docs_from_folder(self, folder_path: str):
        """Add all documents from a folder to the vector store."""
        docs = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]

        for doc in docs:
            doc_path = os.path.join(folder_path, doc)
            self.add_doc_todb(doc_path)


# Example usage
if __name__ == "__main__":
    db = DocumentDatabase()
    db.create_db()

