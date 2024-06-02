from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from  langchain_core.documents.base import Document

from src.query_translation.query_translator import query_translator

class Retriever:

    def __init__(self, type='basic', persist_directory='chroma_db' ):
        self.embedding_model = OpenAIEmbeddings()
        self.vector_store = Chroma(persist_directory=persist_directory, embedding_function=self.embedding_model)
        self.retriever = self.vector_store.as_retriever()
        self.type = type

    def get_retriever(self):
        return self.retriever


    def retrieve(self, query):
        if  self.type == 'basic':
            self.query_translator = query_translator(type='basic')
            adjusted_query = self.query_translator.translate_query(query)
            documents =  self.retriever.invoke(adjusted_query)
            formatted_docs = self.get_page_content(documents)
            return formatted_docs
        if  self.type == 'step-back':
            self.query_translator = query_translator(type='step-back')
            adjusted_query = self.query_translator.translate_query(query)
            documents =  self.retriever.invoke(adjusted_query)
            formatted_docs = self.get_page_content(documents)
            return formatted_docs
        else:
            raise ValueError("Unsupported retrieval method")
        
    def get_page_content(self, docs: list[Document]):
        result = "\n\n".join(doc.page_content for doc in docs)
        # print("Context:")
        # print(result)
        return result

    # def add_documents(self, new_documents):
        # self.vectorstore.add_documents(new_documents)
        # self.bm25_retriever.add_documents(new_documents)

# TODO: idea for the future
# def retrieve(self, query):
#     # Parse the query
#     parsed_query = self.parse_query(query)
    
#     # Expand the query (if applicable)
#     expanded_query = self.expand_query(parsed_query)
    
#     # Match and score documents
#     scored_docs = self.match_and_score(expanded_query)
    
#     # Rank and select top documents
#     top_docs = self.rank_documents(scored_docs)
    
#     return top_docs