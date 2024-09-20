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
    template_wo_rag = """ ### Instruction ###: You are an expert in Requirements Engineering.
    give a comprehensive structured answer to the question.  
   Respond only to the question asked, response should be concise and relevant to the question.
    """ 
    llm = ChatOpenAI(model=MODEL, temperature=TEMPERATURE)
    messages = [("human", question), ("system", template_wo_rag)]
    result = llm.invoke(messages)
    return result.content
