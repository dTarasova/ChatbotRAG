

import json
from src.rag.retriever.structured_data_loading.structured_data_retriever import StructuredDataRetriever
from src.rag.retriever.retriever import Retriever
from src.rag.generator.generator import Generator


class RAGModel:
    def __init__(self, text_retriever_type='basic'):
        self.retriever_text_data = Retriever(text_retriever_type)
        self.retriever_structured_data = StructuredDataRetriever()
        self.generator = Generator()

    def get_context(self, question: str) -> tuple:
        context_from_text_data = self.retriever_text_data.retrieve_context(question)
        context_from_structured_data = self.retriever_structured_data.retrieve_context(question)
        return context_from_text_data, context_from_structured_data
    
    def query(self, question: str, query_types=['combined'] ) -> dict:
        results = {
            "question": question,
            "answers": []
        }
        question_lowered = question.lower()
        context_from_text_data, context_from_structured_data = self.get_context(question_lowered)
        for query_type in query_types:
            if query_type == 'text_data':
                answer_from_text_data =  self.generator.generate_answer(question, context_from_text_data, prompt_type='text_data')
                results["answers"].append(self.create_result_entry("text_data", context_from_text_data, answer_from_text_data))
            elif query_type == 'structured_data':
                answer_from_structured_data = self.generator.generate_answer(question, context_from_structured_data, prompt_type='structured_data')
                results["answers"].append(self.create_result_entry("structured_data", context_from_structured_data, answer_from_structured_data))
            elif query_type == 'combined':
                combined_context = "Context from general knowledge: \n" + context_from_text_data + "\n\n Context from real practical data: \n" + context_from_structured_data
                answer_from_combined = self.generator.generate_answer(question, combined_context, prompt_type='combined')
                results["answers"].append(self.create_result_entry("combined", combined_context, answer_from_combined))
            elif query_type == 'summariser':
                summarized_context_from_text_data = self.generator.generate_summary(context_from_text_data, question_lowered)
                summarized_context_from_structured_data = self.generator.generate_summary(context_from_structured_data, question_lowered)
                combined_summarized_context = "Context from general knowledge: \n" + summarized_context_from_text_data + "\n\n Context from real practical data: \n" + summarized_context_from_structured_data
                answer_from_summarized = self.generator.generate_answer(question, combined_summarized_context, prompt_type='combined')
                results["answers"].append(self.create_result_entry("summarised", combined_summarized_context, answer_from_summarized))

        with open('results.json', 'a') as f:
            json.dump(results, f, indent=4)

        return results
    

    def create_result_entry(self, model, context, answer):
        return {
            "model": model,
            "context": context,
            "answer": answer
        }



if __name__ == "__main__":
    rag_model = RAGModel()
    answer, retrieved_context = rag_model.query("What is RAG?")
    print("Answer:", answer)
    print("\n\nRetrieved Context:", retrieved_context)
