

from src.retriever.retriever import Retriever
from src.generator.generator import Generator


class RAGModel:
    def __init__(self, type='basic'):
        self.retriever = Retriever(type)
        self.generator = Generator(self.retriever)

    def query(self, question):
        retrieved_docs = self.retriever.retrieve(question)
        answer = self.generator.generate_answer(question, retrieved_docs)
        return answer, retrieved_docs

if __name__ == "__main__":
    rag_model = RAGModel()
    answer, retrieved_docs = rag_model.query("What is RAG?")
    print("Answer:", answer)
    print("\n\nRetrieved Documents:", retrieved_docs)
