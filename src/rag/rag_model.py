from enum import Enum
import json
import os
from src.rag.retriever.evaluation.evaluator import Evaluator
from src.rag.retriever.structured_data_loading.structured_data_retriever import StructuredDataRetriever
from src.rag.retriever.retriever import Retriever
from src.rag.generator.generator import Generator
from typing import List, Dict, Any, Optional

from src.wo_rag import get_openai_answer

class RAGTypes(Enum):
    TEXT_DATA = 'text_data'
    STRUCTURED_DATA = 'structured_data'
    COMBINED = 'combined'
    SUMMARISER = 'summariser'

class RAGModel:
    def __init__(self, text_retriever_type: str = 'step-back', path_to_db_directory: str = 'knowledge_bases/amdire_and_napire'):
        self.retriever_text_data = Retriever(path_to_db_directory = path_to_db_directory, type = text_retriever_type)
        self.retriever_structured_data = StructuredDataRetriever()
        self.generator = Generator()
        self.evaluator = Evaluator()

    def get_context_from_text_data(self, question: str) -> Optional[str]:
        """
        Retrieves context from text data source if needed.
        
        :param question: The question to query
        :return: Context from text data
        """
        try:
            return self.retriever_text_data.retrieve_context(question)
        except Exception as e:
            return f"Error retrieving text data: {str(e)}"
    
    def get_context_from_structured_data(self, question: str) -> Optional[str]:
        """
        Retrieves context from structured data source if needed.
        
        :param question: The question to query
        :return: Context from structured data
        """
        try:
            return self.retriever_structured_data.retrieve_context(question)
        except Exception as e:
            return f"Error retrieving structured data: {str(e)}"

    def query(self, question: str, query_types: List[RAGTypes] = [RAGTypes.COMBINED]) -> Dict[str, Any]:
        """
        Queries the model with the given question and retrieves answers based on the query types.
        
        :param question: The question to be answered
        :param query_types: A list of RAGTypes to determine which data sources to query
        :return: A dictionary containing the question, context, and answers organized by model type
        """
        results = {
            "question": question,
            "models": {}
        }

        question_lowered = question.lower()

        # Fetch contexts only when needed based on query types
        context_from_text_data = None
        context_from_structured_data = None

        openai_answer = get_openai_answer(question)
        openai_evaluation = self.evaluator.get_answer_evaluation(question, openai_answer)
        results["models"]["OpenAI"] = {
            "answer": openai_answer,
            "context": None,
            "evaluation": openai_evaluation

        }

        for query_type in query_types:
            if query_type == RAGTypes.TEXT_DATA and context_from_text_data is None:
                context_from_text_data = self.get_context_from_text_data(question_lowered)

            if query_type == RAGTypes.STRUCTURED_DATA and context_from_structured_data is None:
                context_from_structured_data = self.get_context_from_structured_data(question_lowered)

            if query_type == RAGTypes.TEXT_DATA:
                results["models"][RAGTypes.TEXT_DATA.name] = self.process_text_data_query(question, context_from_text_data)
            elif query_type == RAGTypes.STRUCTURED_DATA:
                results["models"][RAGTypes.STRUCTURED_DATA.name] = self.process_structured_data_query(question, context_from_structured_data)
            elif query_type == RAGTypes.COMBINED:
                results["models"][RAGTypes.COMBINED.name] = self.process_combined_query(question, context_from_text_data, context_from_structured_data)
            elif query_type == RAGTypes.SUMMARISER:
                results["models"][RAGTypes.SUMMARISER.name] = self.process_summarized_query(question_lowered, context_from_text_data, context_from_structured_data)

        self.save_results_to_file(results, 'results.json')

        return results

    def process_text_data_query(self, question: str, context_from_text_data: str) -> Dict[str, Any]:
        """Processes a text data query and returns a dictionary with context and answer."""
        if context_from_text_data:
            answer_from_text_data = self.generator.generate_answer(question, context_from_text_data, prompt_type='text_data')
            
            evaluation = self.evaluator.get_answer_evaluation(question, answer_from_text_data)
            return {
                "context": context_from_text_data,
                "answer": answer_from_text_data,
                "evaluation": evaluation
            }
        return {}

    def process_structured_data_query(self, question: str, context_from_structured_data: str) -> Dict[str, Any]:
        """Processes a structured data query and returns a dictionary with context and answer."""
        if context_from_structured_data:
            answer_from_structured_data = self.generator.generate_answer(question, context_from_structured_data, prompt_type='structured_data')
            evaluation = self.evaluator.get_answer_evaluation(question, answer_from_structured_data)
            return {
                "context": context_from_structured_data,
                "answer": answer_from_structured_data,
                "evaluation": evaluation
            }
        return {}

    def process_combined_query(self, question: str, context_from_text_data: Optional[str], context_from_structured_data: Optional[str]) -> Dict[str, Any]:
        """Processes a combined query and returns a dictionary with combined context and answer."""
        if context_from_text_data is None:
            context_from_text_data = self.get_context_from_text_data(question)
        if context_from_structured_data is None:
            context_from_structured_data = self.get_context_from_structured_data(question)

        combined_context = f"Context from general knowledge: \n{context_from_text_data}\n\nContext from real practical data: \n{context_from_structured_data}"
        answer_from_combined = self.generator.generate_answer(question, combined_context, prompt_type='combined')
        evaluation = self.evaluator.get_answer_evaluation(question, answer_from_combined)
        
        return {
            "context": combined_context,
            "answer": answer_from_combined,
            "evaluation": evaluation
        }

    def process_summarized_query(self, question: str, context_from_text_data: Optional[str], context_from_structured_data: Optional[str]) -> Dict[str, Any]:
        """Processes a summarized query and returns a dictionary with summarized context and answer."""
        if context_from_text_data is None:
            context_from_text_data = self.get_context_from_text_data(question)
        if context_from_structured_data is None:
            context_from_structured_data = self.get_context_from_structured_data(question)

        summarized_context_from_text_data = self.generator.generate_summary(context_from_text_data, question)
        summarized_context_from_structured_data = self.generator.generate_summary(context_from_structured_data, question)
        combined_summarized_context = f"Context from general knowledge: \n{summarized_context_from_text_data}\n\nContext from real practical data: \n{summarized_context_from_structured_data}"
        answer_from_summarized = self.generator.generate_answer(question, combined_summarized_context, prompt_type='combined')
        evaluation = self.evaluator.get_answer_evaluation(question, answer_from_summarized)
        return {
            "context": combined_summarized_context,
            "answer": answer_from_summarized,
            "evaluation": evaluation
        }

    def save_results_to_file(self, results: dict, filename: str):
        """Saves results to a JSON file."""
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                json.dump([], f)  # Create an empty array to start with

        # Read the existing data from the file
        with open(filename, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

        # Ensure data is a list
        if not isinstance(data, list):
            data = []

        # Append the new results
        data.append(results)

        # Write the updated data back to the file
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)


if __name__ == "__main__":
    rag_model = RAGModel()
    results = rag_model.query("What is RAG?", [RAGTypes.TEXT_DATA, RAGTypes.STRUCTURED_DATA])
    print(json.dumps(results, indent=4))
