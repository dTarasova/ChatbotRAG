from langchain_openai import ChatOpenAI

def get_openai_answer(question: str) -> str:
    template_wo_rag = """ ### Instruction ###: You are an expert in Requirements Engineering. 
    Answer the following question with detailed and accurate information. 
    Ensure that your answer directly addresses the user's question.
    """ 
    llm = ChatOpenAI(temperature=0)
    messages = [("human", question), ("system", template_wo_rag)]
    result = llm.invoke(messages)
    print("\n\nAnswer without RAG : ")
    print(result)
    return result.content

get_openai_answer("Is the requirement 'System should be secure' good?")