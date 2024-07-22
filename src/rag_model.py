

import json
from src.retriever.retriever import Retriever
from src.generator.generator import Generator
from src.structured_data_part.structured_data_retriever import StructuredDataRetriever
from src.wo_rag import get_openai_answer


class RAGModel:
    def __init__(self, text_retriever_type='basic'):
        self.retriever_text_data = Retriever(text_retriever_type)
        self.retriever_structured_data = StructuredDataRetriever()
        self.generator = Generator()

    def query(self, question):
        question_lowered = question.lower()
        results = []
        text_data_answer, text_data_context = self.query_text(question_lowered)
        results.append({
            "question": question,
        })
        results.append({
            "model": "text_data",
            "context": text_data_context,
            "answer": text_data_answer
        })
        structured_data_answer, structured_data_context = self.query_structured(question_lowered)  
        results.append({
            "model": "structured_data",
            "context": structured_data_context,
            "answer": structured_data_answer
        })
        combined_answer, combined_context = self.query_combined(question_lowered, text_data_context, structured_data_context)
        results.append({
            "model": "combined",
            "context": combined_context,
            "answer": combined_answer
        })

        openai_answer = get_openai_answer(question)
        results.append({    
            "model": "openai",
            "context": "",
            "answer": openai_answer
        })

        with open('results.json', 'w') as f:
            json.dump(results, f, indent=4)

        return combined_answer, combined_context

    
    # def query_combined(self, question):
    #     question_lowered = question.lower()
    #     context_from_text_data = self.retriever_text_data.retrieve_context(question_lowered)
    #     context_from_structured_data = self.retriever_structured_data.retrieve_context(question_lowered)
    #     combined_context = "Context from general knowledge: \n" + context_from_text_data + "\n\n Context from real practical data: \n" + context_from_structured_data
    #     answer = self.generator.generate_answer(question_lowered, combined_context)
    #     return answer, retrieved_context
    
    def query_text(self, question):
        retrieved_context = self.retriever_text_data.retrieve_context(question)
        answer = self.generator.generate_answer(question, retrieved_context, prompt_type='text_data')
        return answer, retrieved_context
    
    def query_structured(self, question):
        retrieved_context = self.retriever_structured_data.retrieve_context(question)
        answer = self.generator.generate_answer(question, retrieved_context, prompt_type='structured_data')
        return answer, retrieved_context
    
    def query_combined(self, question, context_text_data, context_structured_data):
        combined_context = "Context from general knowledge: \n" + context_text_data + "\n\n Context from real practical data: \n" + context_structured_data
        answer = self.generator.generate_answer(question, combined_context, prompt_type='combined')
        return answer, combined_context
    
    
    #TODO: Implement a function that select what is the most relevant context to use for the answer generation
    #TODO: Research dependencies between size of the context and quality of the answers


if __name__ == "__main__":
    rag_model = RAGModel()
    answer, retrieved_context = rag_model.query("What is RAG?")
    print("Answer:", answer)
    print("\n\nRetrieved Context:", retrieved_context)
