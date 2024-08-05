from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from  langchain_core.documents.base import Document

from src.rag.retriever.query_translation import query_translator
from src.rag.retriever.retriever_results_ranker import RRFResultsRanker, ResultsRanker


class Retriever:

    def __init__(self, type='basic', persist_directory='chroma_db', ranker_type = 'rrf' ):
        self.embedding_model = OpenAIEmbeddings()
        self.vector_store = Chroma(persist_directory=persist_directory, embedding_function=self.embedding_model)
        self.retriever = self.vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 5})
        self.type = type
        self.ranker = self.create_ranker(ranker_type)

    def get_retriever(self): 
        return self.retriever
    
    def create_ranker(self, ranker_type) -> ResultsRanker:
        if ranker_type == 'rrf':
            return RRFResultsRanker()
        else:
            return ResultsRanker()
        
    def rank_results(self, results) -> list[Document]:
        return self.ranker.get_results(results)

    
    def retrieve_docs(self, query: str) -> list[Document]:
        documents =  self.retriever.invoke(query)
        return documents

    def retrieve_context(self, query: str) -> str:
        docs = self.retrieve_docs(query)
        additional_info = ""
        if self.type == 'step-back':
            self.query_translator = query_translator(type='step-back')
            adjusted_query = self.query_translator.translate_query(query)
            documents_stepback_query =  self.retriever.invoke(adjusted_query)
            documents_stepback_query.extend(docs)
            docs = documents_stepback_query
            additional_info += f"Step-back query: {adjusted_query}\n\n"
        
        ranked_docs = self.rank_results(docs)
        context = self.create_context(ranked_docs, additional_info=additional_info)
        return context

    def create_context(self, docs: list[Document], additional_info: str = "") -> str:
        context = additional_info
        for doc in docs:
            context_str = doc.page_content
            source_str = doc.metadata.get("source") or doc.metadata.get("title") or ""
            context += f"Context: {context_str}\n Source: {source_str}\n\n"
        return context
        

    
    

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