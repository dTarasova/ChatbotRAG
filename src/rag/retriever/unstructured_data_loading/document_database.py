import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents.base import Document
from src.custom_types import VectorStoreType
from langchain.vectorstores import FAISS
from src.rag.retriever.unstructured_data_loading.pdf_preprocessor import process_pdf
from langchain.embeddings.openai import OpenAIEmbeddings
import abc


# Base class to encapsulate common functionality
class DocumentDatabaseBase:
    def __init__(self, path_to_db_directory):
        self.path_to_db_directory = path_to_db_directory
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = None  # To be set by the child class

    def create_db(self, path_to_documents):
        """Create the vector store and add documents."""
        self.add_docs_from_folder(path_to_documents)
        return self.vector_store

    def get_vectorstore(self):
        return self.vector_store

    def check_findings(self, query: str):
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
        """Process and add a document to the vector store."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=400, chunk_overlap=50,
            strip_whitespace=True,
            separators=["\n\n", "\n", ".", " ", ""]
        )

        head, tail = os.path.split(doc_path)
        processed_pdf = process_pdf(doc_path, tail + '.txt')

        pages = text_splitter.split_text(processed_pdf)
        documents = [Document(page_content=page, metadata={"source": tail}) for page in pages]

        # Delegate to child classes for vector store-specific behavior
        self._handle_vector_store_add_documents(documents)

        print(f"Document {doc_path} added to db")

    @abc.abstractmethod
    def _handle_vector_store_add_documents(self, documents: list[Document]):
        """Abstract method to be implemented by child classes to handle vector store specifics."""
        pass

    def add_docs_from_folder(self, folder_path: str):
        """Add all documents from a folder to the vector store."""
        docs = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]

        for doc in docs:
            doc_path = os.path.join(folder_path, doc)
            self.add_doc_todb(doc_path)


# FAISS-specific child class
class DocumentDatabaseFaiss(DocumentDatabaseBase):
    def __init__(self, path_to_db_directory='knowledge_bases/amdire_napire_software4kmu_faiss'):
        super().__init__(path_to_db_directory)
        if os.path.exists(self.path_to_db_directory):
            from langchain.vectorstores import FAISS
            self.vector_store = FAISS.load_local(
                self.path_to_db_directory, self.embeddings, allow_dangerous_deserialization=True
            )
        else:
            self.vector_store = None

    def print_vectorstore_collections(self):
        """FAISS doesn't support collections, so print a summary instead."""
        if self.vector_store:
            print(f"Number of vectors in FAISS index: {self.vector_store.index.ntotal}")

    def _handle_vector_store_add_documents(self, documents: list[Document]):
        """FAISS-specific logic for adding documents to the vector store."""
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
        else:
            self.vector_store.add_documents(documents)
        self.vector_store.save_local(self.path_to_db_directory)


# Chroma-specific child class
class DocumentDatabaseChroma(DocumentDatabaseBase):
    def __init__(self, path_to_db_directory='knowledge_bases/amdire_napire_software4kmu_chroma'):
        super().__init__(path_to_db_directory)
        from langchain_community.vectorstores import Chroma
        self.vector_store = Chroma(persist_directory=self.path_to_db_directory, embedding_function=self.embeddings)

    def print_vectorstore_collections(self):
        """Print Chroma collections."""
        for collection in self.vector_store._collection:
            print(f"Collection: {collection}")
            print(f"Number of documents in collection: {self.vector_store._collection.count()}")

    def _handle_vector_store_add_documents(self, documents: list[Document]):
        """Chroma-specific logic for adding documents to the vector store."""
        if not self.vector_store:
            self.vector_store = Chroma(persist_directory=self.path_to_db_directory, embedding_function=self.embeddings)
        
        self.vector_store.add_documents(documents)

def create_document_database(vector_store_type: VectorStoreType, path_to_db_directory: str):
    if vector_store_type == VectorStoreType.CHROMA:
        return DocumentDatabaseChroma(path_to_db_directory=path_to_db_directory)
    elif vector_store_type == VectorStoreType.FAISS:
        return DocumentDatabaseFaiss(path_to_db_directory=path_to_db_directory)
    else:
        raise ValueError(f"Unknown vector store type: {vector_store_type}")
        
if __name__ == "__main__":
    path_db = 'knowledge_bases/amdire_napire_software4kmu'
    documentDatabase = DocumentDatabaseFaiss(path_db)
    documentDatabase.add_docs_from_folder('data/amdire_napire_software4kmu')
    documentDatabase.print_vectorstore_collections()
    documents = documentDatabase.check_findings("how to improve requirement System should be fast")
    print(documents)
