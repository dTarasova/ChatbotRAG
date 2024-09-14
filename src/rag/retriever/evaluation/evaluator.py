from langchain_openai import ChatOpenAI
import openai

from src.llm_settings import MODEL, TEMPERATURE

class Evaluator:
    

    def get_answer_evaluation(self, question: str, answer: str) -> dict:
        # Create a prompt for GPT-4 to evaluate correctness and relevance using numerical scores
        prompt = f"""
        Question: {question}
        Answer: {answer}
        
        Evaluate the answer with the following criteria:
        1. Completeness: How complete is the answer for resolving user query on a scale of 0 to 100, where 0 is does not resolve at all and 100 is fully resolve?
        2. Relevance: How relevant is the answer to the question on a scale of 0 to 100, where 0 is irrelevant and 100 is highly relevant?
        
        Please provide the evaluation in the following format:
        Completeness: <score from 0 to 100>
        Relevance: <score from 0 to 100>
        """
        
        # Send the prompt to OpenAI's API
        llm = ChatOpenAI(model=MODEL, temperature=TEMPERATURE)
        messages=[
                ("system", "You are an evaluator AI that assesses answers based on correctness and relevance, providing scores from 0 to 10."),
                ("user", prompt)
            ]
        result = llm.invoke(messages)
        

        # Extract the response and return as structured data
        evaluation = result.content.strip()

        # Optionally, you can parse the response if it's formatted in a specific way:
        lines = evaluation.splitlines()
        completeness_score = float(lines[0].split(":")[1].strip())
        relevance_score = float(lines[1].split(":")[1].strip())

        return {
            "completeness": completeness_score,
            "relevance": relevance_score
        }

# Example usage:
# evaluator = Evaluator("your_openai_api_key")
# result = evaluator.get_answer_evaluation("What is the capital of France?", "Paris")
# print(result)
