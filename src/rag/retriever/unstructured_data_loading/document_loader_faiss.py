import re
import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_core.documents.base import Document
from src.rag.retriever.unstructured_data_loading.pdf_preprocessor import process_pdf
import faiss

PATH_DOCUMENTS = 'data/just amdire and napire papers'
PERSIST_DIRECTORY = 'knowledge_bases/amdire_and_napire'
EXAMPLE_FILE_PATH = 'data/first_batch/Rapid quality assurance with Requirements Smells.pdf'

class DocumentDatabaseFaiss:
    def __init__(self, path_to_db_directory='knowledge_bases/amdire_napire_software4kmu'):
        self.path_to_db_directory = path_to_db_directory
        self.embeddings = OpenAIEmbeddings()
        if os.path.exists(self.path_to_db_directory):
            self.vector_store = FAISS.load_local(
                self.path_to_db_directory, self.embeddings, allow_dangerous_deserialization=True
            )
        else:
            self.vector_store = None


    def create_db(self, path_to_documents) -> FAISS:
        """Create and return the FAISS vector store client."""
        self.add_docs_from_folder(path_to_documents)
        return self.vector_store
     
    def get_vectorstore(self) -> FAISS:
        return self.vector_store
    
    def print_vectorstore_collections(self) -> None:
        # FAISS doesn't have a concept of collections, so we will print a summary instead
        if self.vector_store:
            print(f"Number of vectors in FAISS index: {self.vector_store.index.ntotal}")
    
    def check_findings(self, query: str) -> list[Document]:
        """Retrieve documents based on a query."""
        if self.vector_store is None:
            print("No vector store found.")
            return []

        query_embedding = self.embeddings.embed_query(query)
        results = self.vector_store.similarity_search_by_vector(query_embedding, k=5)
        
        for result in results:
            print(f"Document: {result.metadata['source']}\n")
            print(f"Content: {result.page_content}\n\n")
        return results

    def add_doc_todb(self, doc_path: str):
        """Process and add a document to the FAISS vector store."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=400, chunk_overlap=50,
            strip_whitespace=True,
            separators=["\n\n", "\n", ".", " ", ""]
        )

        head, tail = os.path.split(doc_path)
        processed_pdf = process_pdf(doc_path, tail+'.txt')

        pages = text_splitter.split_text(processed_pdf)
        documents = [Document(page_content=page, metadata={"source": tail}) for page in pages]

        if self.vector_store is None:
            # index = faiss.IndexFlatL2(self.embeddings.dimension())
            # self.vector_store = FAISS(embedding_function=self.embeddings, index=index)
            self.vector_store = FAISS.from_documents(documents, self.embeddings)

        else: 
            self.vector_store.add_documents(documents)
        print(f"Document {doc_path} added to db")

    def add_docs_from_folder(self, folder_path: str):
        """Add all documents from a folder to the FAISS vector store."""
        docs = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]

        for doc in docs:
            doc_path = os.path.join(folder_path, doc)
            self.add_doc_todb(doc_path)
        self.vector_store.save_local(self.path_to_db_directory)


# Example usage
if __name__ == "__main__":
    path_db = 'knowledge_bases/amdire_napire_software4kmu'
    path_data = 'data/software4kmu papers'
    documentDatabase = DocumentDatabaseFaiss(path_to_db_directory=path_db)
    documentDatabase.add_docs_from_folder(path_data)
    vector_store = documentDatabase.get_vectorstore()
    documentDatabase.print_vectorstore_collections()
    documents = documentDatabase.check_findings("RE is just writing down wants and needs")
