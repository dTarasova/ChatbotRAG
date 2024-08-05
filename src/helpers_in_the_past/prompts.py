from langchain.prompts import ChatPromptTemplate

def get_basic_rag_prompt() -> ChatPromptTemplate:

    template = """ ### Instruction ### You are an expert in Requirements Engineering. 
    Answer the following question with detailed and accurate information. The answer should be explainable. 
    Use the provided context to enhance your response, but if the context does not add value, 
    you may disregard it. Ensure that your answer directly addresses the user's question.

    ### Context ###: {context}

    ### Question ### : {question}""" 

    prompt = ChatPromptTemplate.from_template(template)
    return prompt


def get_basic_openai_prompt() -> ChatPromptTemplate:
    template = """You are an expert in Requirements Engineering. 
    Answer the following question with detailed and accurate information. The answer should be explainable. 
    Ensure that your answer directly addresses the user's question.

    Question: {question}"""
    prompt = ChatPromptTemplate.from_template(template)
    return prompt


def get_rag_fusion_prompt() -> ChatPromptTemplate:
    template = """You are a helpful assistant that generates multiple search queries based on a single input query. \n
    Generate multiple search queries related to: {question} \n
    Output (4 queries):"""
    prompt = ChatPromptTemplate.from_template(template)
    return prompt