

from src.retriever.retriever import Retriever
from src.generator.generator import Generator
from src.structured_data_part.structured_data_retriever import StructuredDataRetriever


class RAGModel:
    def __init__(self, type='basic'):
        self.retriever = self.create_retriever(type)
        self.generator = Generator(type=type)

    def create_retriever(self, type='basic'):
        if(type == 'structured_data'):
            return StructuredDataRetriever()
        return Retriever(type=type)
    
    def query(self, question):
        question_lowered = question.lower()
        retrieved_context = self.retriever.retrieve_context(question_lowered)
        answer = self.generator.generate_answer(question_lowered, retrieved_context)
        return answer, retrieved_context

if __name__ == "__main__":
    rag_model = RAGModel()
    answer, retrieved_context = rag_model.query("What is RAG?")
    print("Answer:", answer)
    print("\n\nRetrieved Context:", retrieved_context)
