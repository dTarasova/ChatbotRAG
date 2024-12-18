from langchain_openai import OpenAIEmbeddings
from  langchain_core.documents.base import Document

from src.rag.retriever.query_translation.query_translator import QueryTranslator
from src.rag.retriever.retriever_results_ranker import RRFResultsRanker, ResultsRanker
from src.rag.retriever.unstructured_data_loading.document_database import create_document_database
from src.custom_types import VectorStoreType

class Retriever:

    def __init__(self, path_to_db_directory: str, vector_store_type: VectorStoreType, type='step-back', ranker_type = 'rrf'  ):
        self.embedding_model = OpenAIEmbeddings()
        self.documentDatabase = create_document_database(vector_store_type=vector_store_type, path_to_db_directory=path_to_db_directory)
        self.vector_store = self.documentDatabase.get_vectorstore()

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
        # print("checking findings")
        # docs2 = self.documentDatabase.check_findings(query)

        if self.type == 'expand':
            self.query_translator = QueryTranslator(type='expand')
            adjusted_query = self.query_translator.translate_query(query)
            documents_expansion_query =  self.retriever.invoke(adjusted_query)
            docs = documents_expansion_query
            additional_info = f"Expansion query: {adjusted_query}\n\n"
        else: 
            docs = self.retrieve_docs(query)
            additional_info = ""
            if self.type == 'step-back':
                self.query_translator = QueryTranslator(type='step-back')
                adjusted_query = self.query_translator.translate_query(query)
                documents_stepback_query =  self.retriever.invoke(adjusted_query)
                documents_stepback_query.extend(docs)
                docs = documents_stepback_query
                additional_info += f"Step-back query: {adjusted_query}\n\n"
        
        ranked_docs = self.rank_results(docs)
        context = self.create_context(docs = ranked_docs, query=query, additional_info=additional_info)
        return context

    def create_context(self, docs: list[Document], query: str, additional_info: str = "") -> str:
        context_to_return = additional_info  # This will store the context without sources
        with open("context.txt", "a", encoding="utf-8") as file:
            # Write the query and context to the file
            file.write(f"Query: {query}\n")
            for doc in docs:
                context_str = doc.page_content
                source_str = doc.metadata.get("source") or doc.metadata.get("title") or ""
                context_to_return += f"{context_str}\n\n"  # Only context returned
                # Append context and source to the file
                file.write(f"Context: {context_str}\n")
                file.write(f"Source: {source_str}\n\n")
        return context_to_return
       
