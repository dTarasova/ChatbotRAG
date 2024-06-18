

from src.retriever.retriever import Retriever
from src.generator.generator import Generator


class RAGModel:
    def __init__(self, type='basic'):
        self.retriever = Retriever(type=type)
        self.generator = Generator()

    def query(self, question):
        question_lowered = question.lower()
        retrieved_docs = self.retriever.retrieve_context(question_lowered)
        answer = self.generator.generate_answer(question_lowered, retrieved_docs)
        return answer, retrieved_docs

if __name__ == "__main__":
    rag_model = RAGModel()
    answer, retrieved_docs = rag_model.query("What is RAG?")
    print("Answer:", answer)
    print("\n\nRetrieved Documents:", retrieved_docs)
