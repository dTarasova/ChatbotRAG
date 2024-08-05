import helpers_in_the_past.prompts as prompts
import helpers_in_the_past.retriever_generator as retriever_generator
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.load import dumps, loads
from operator import itemgetter
# from wo_rag import get_openai_answer
from json import dumps, loads
from operator import itemgetter
from langchain.prompts import ChatPromptTemplate

def create_query_pipeline():
    prompt_rag_fusion = prompts.get_rag_fusion_prompt()
    return (
        prompt_rag_fusion 
        | ChatOpenAI(temperature=0)
        | StrOutputParser() 
        | (lambda x: x.split("\n"))
    )

def format_qa_pairs(questions, answers):
    """Format Q and A pairs"""
    
    formatted_string = ""
    for i, (question, answer) in enumerate(zip(questions, answers), start=1):
        formatted_string += f"Question {i}: {question}\nAnswer {i}: {answer}\n\n"
    return formatted_string.strip()


def setup_rag_chain():
    llm = ChatOpenAI(temperature=0)
    template = """Here is a set of Q+A pairs:

    {context}

    Use these to synthesize an answer to the question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)
    final_rag_chain = (
    prompt
    | llm
    | StrOutputParser()
    )
    return final_rag_chain 

def retrieve_and_rag(question,prompt_rag,sub_question_generator_chain):
    """RAG on each sub-question"""
    llm = retriever_generator.get_llm()
    
    # Use our decomposition / 
    sub_questions = sub_question_generator_chain.invoke({"question":question})
    
    # Initialize a list to hold RAG chain results
    rag_results = []

    retriever = retriever_generator.get_retriever()
    
    for sub_question in sub_questions:
        
        # Retrieve documents for each sub-question
        retrieved_docs = retriever.get_relevant_documents(sub_question)
        
        # Use retrieved documents and sub-question in RAG chain
        answer = (prompt_rag | llm | StrOutputParser()).invoke({"context": retrieved_docs, 
                                                                "question": sub_question})
        rag_results.append(answer)
    
    return rag_results,sub_questions

def get_context(question):
    llm = retriever_generator.get_llm()
    prompt_rag = prompts.get_basic_rag_prompt()
    # Decomposition
    template = """You are a helpful assistant that generates multiple sub-questions related to an input question. \n
    The goal is to break down the input into a set of sub-problems / sub-questions that can be answers in isolation. \n
    Generate multiple search queries related to: {question} \n
    Output (3 queries):"""
    prompt_decomposition = ChatPromptTemplate.from_template(template)
    generate_queries_decomposition = ( prompt_decomposition | llm | StrOutputParser() | (lambda x: x.split("\n")))
    answers, questions = retrieve_and_rag(question, prompt_rag, generate_queries_decomposition)
    context = format_qa_pairs(answers, questions)
    return context


def main():
    question = "Is the requirement 'System should be secure' good?"
    
    context = get_context(question)
    print("\n\n\nContext:")
    print(context)

    final_rag_chain = setup_rag_chain()

    print("\n\nAnswer with RAG:")
    result = final_rag_chain.invoke({"context":context, "question": question})
    print(result)

    # get_openai_answer(question)

if __name__ == "__main__":
    main()
