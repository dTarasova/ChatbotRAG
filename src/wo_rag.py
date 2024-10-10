from langchain_openai import ChatOpenAI
from src.llm_settings import MODEL, TEMPERATURE

# def get_openai_answer(question: str) -> str:
#     template_wo_rag = """ ### Instruction ###: You are an expert in Requirements Engineering. 
#     Answer the following question with detailed and accurate information. 
#     Ensure that your answer directly addresses the user's question.
#     """ 
#     llm = ChatOpenAI(model=MODEL, temperature=TEMPERATURE)
#     messages = [("human", question), ("system", template_wo_rag)]
#     result = llm.invoke(messages)
#     return result.content

def get_openai_answer(question: str) -> str:
#     template_wo_rag = """ ### Instruction ###: You are an expert in Requirements Engineering.
#     give a comprehensive structured answer to the question.  
#    The answer should be clear, concise, and structured as follows:

#     Answer: Give short presise answer to the question.
# Details: Present supporting information from the given details, include explanations, examples.
#     """
# 


#in daniel evaluation
#     template_wo_rag = """
#     ### Instruction ###
#     As an expert in Requirements Engineering, your task is to generate a well-structured and organized response to the given query. Follow the specific format outlined below:

# **Answer**: Deliver a clear and direct answer to the question.
# **Details**: Present structured supporting information, including relevant explanations or examples.
# """
    template_wo_rag = """
### Instruction ###
As an expert in Requirements Engineering, your task is to generate a well-structured and organized response to the given query. 
###Answer format###
**Answer**: Deliver a clear and direct answer to the question.
**Details**: Present supporting information. Include relevant explanations. Provide a structured answer with headings, subheadings , examples when they contribute to explainability. Format text with bold, italics when needed
"""
    llm = ChatOpenAI(model=MODEL, temperature=TEMPERATURE)
    messages = [("human", question), ("system", template_wo_rag)]
    result = llm.invoke(messages)
    return result.content
    # return "lalala" + question

