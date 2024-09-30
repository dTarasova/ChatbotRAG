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
    def __init__(self, path_to_db_directory='knowledge_bases/amdire_and_napire'):
        self.path_to_db_directory = path_to_db_directory
        self.vector_store = Chroma(persist_directory=path_to_db_directory, embedding_function=OpenAIEmbeddings())

    def create_db(self, path_to_documents) -> Chroma:
        """Create and return the vector store client."""
        # self.vector_store = chromadb.PersistentClient(path=self.path_to_db_directory)
        self.add_docs_from_folder(path_to_documents)
        return self.vector_store
     
    def get_vectorstore(self) -> Chroma:
        return self.vector_store
    
    def print_vectorstore_collections(self) -> None:
        for collection in self.vector_store._collection:
            print(f"Collection: {collection}")
            print(f"Number of documents in collection: {(self.vector_store._collection.count())}")
    
    def check_findings(self, query: str) -> list[Document]:
        """Retrieve documents based on a query."""
        documents = self.vector_store.search(query, search_type="mmr", search_kwargs={"k": 5})
        for doc in documents:
            print(f"Document: {doc.metadata['source']}\n")
            print(f"Content: {doc.page_content}\n\n")
        return documents

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
    path_db = 'knowledge_bases/amdire_napire_software4kmu'
    path_data = 'data/software4kmu papers'
    documentDatabase = DocumentDatabase(path_to_db_directory=path_db)
    documentDatabase.add_docs_from_folder(path_data)
    vector_store = documentDatabase.get_vectorstore()
    documentDatabase.print_vectorstore_collections()
    documents = documentDatabase.check_findings("Subjective Language refers to")


# used folders
# idea is to gradually add data to the existing databases to reduce embedding creation
# PATH_DB_AMDIRE_NAPIRE = 'knowledge_bases/amdire_napire'
# PATH_DB_AMDIRE_NAPIRE_SOFTWARE4KMU = 'knowledge_bases/amdire_napire_software4kmu'
# PATH_DB_ALL = 'knowledge_bases/all'

# PATH_DATA_AMDIRE_NAPIRE = 'data/just amdire and napire papers'
# PATH_DATA_SOFTWARE4KMU = 'data/software4kmu'
# PATH_DATA_OTHER_REQUIREMENTS = 'data/not amdire and napire'
