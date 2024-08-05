from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.load import dumps, loads
from helpers_in_the_past.retriever_generator import get_retriever
from operator import itemgetter
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough


def get_unique_union(documents: list[list]) -> list:
    """ Unique union of retrieved docs """
    # Flatten list of lists, and convert each Document to string
    flattened_docs = [dumps(doc.page_content) for sublist in documents for doc in sublist]
    # Get unique documents
    unique_docs = list(set(flattened_docs))
    # Return
    return [loads(doc) for doc in unique_docs]

# Multi Query: Different Perspectives
template_queries = """You are an AI language model assistant. Your task is to generate five 
different versions of the given user question to retrieve relevant documents from a vector 
database. By generating multiple perspectives on the user question, your goal is to help
the user overcome some of the limitations of the distance-based similarity search. 
Provide these alternative questions separated by newlines. Original question: {question}"""
prompt_perspectives = ChatPromptTemplate.from_template(template_queries)

# Generate alternative queries
generate_queries = (
    prompt_perspectives 
    | ChatOpenAI(temperature=0) 
    | StrOutputParser() 
    | (lambda x: x.split("\n"))
)

# Example question
question = "Is the requirement 'System should be secure' good?"

# Retrieve documents
retriever = get_retriever()
retrieval_chain = generate_queries | retriever.map() | get_unique_union

# Uncomment these lines to invoke the chain and print the results
# result = generate_queries.invoke({"question": question})
# print(result)
# docs = retrieval_chain.invoke({"question": question})
# print(docs)

# RAG (Retrieve and Generate)
template_rag = """You are a helpful assistant. Answer the following question. If possible, use this context to extend and clarify your answer:

{context}

Question: {question}
"""
prompt_rag = ChatPromptTemplate.from_template(template_rag)

llm = ChatOpenAI(temperature=0)

# Final RAG chain in intermediate steps

# 1. Generate alternative queries
alternative_queries = generate_queries.invoke({"question": question})
print("Alternative Queries:", alternative_queries)

# 2. Retrieve documents using generated queries
# retrieved_docs = retrieval_chain.invoke({"question": question})
# print("Retrieved Docs:", retrieved_docs)

# print("type of docs")
# print(type(retrieved_docs[0][0]))

#2.5 Ask differently
print("answers")
context_from_queries = []
for query in alternative_queries:
    answers = retriever.invoke(query, search_type="similarity")
    for answer in answers:
        context_from_queries.extend(answer.page_content)
        print(answer.page_content + "\n\n")



# # 3. Get unique union of retrieved documents
# unique_docs = get_unique_union(retrieved_docs)
# print("Unique Docs:", unique_docs)

# # 4. Prepare context for RAG
# context = unique_docs
context = context_from_queries


# 5. Generate final answer using context and question
final_rag_input = {"context": context, "question": question}
formatted_prompt = prompt_rag.format(**final_rag_input)
final_answer = llm.invoke(formatted_prompt)
print("Final Answer:", final_answer)

# Original result without retrieval context
messages = [("human", question)]
"system", "You are a helpful assistant that translates English to French."
original_result = llm.invoke(messages)
print("\n\nOriginal result: ")
print(original_result)


# final_rag_chain = (
#     {"context": retrieval_chain, 
#      "question": itemgetter("question")} 
#     | prompt_rag
#     | llm
#     | StrOutputParser()
# )

# final_rag_chain.invoke({"question":question})



""" TODO: fix sth like that might be considered context
3.5! System Quality Requirements..................................................................................... 16!
3.6! Architectural Constraints............................................................................................. 16!


3.5! System Quality Requirements..................................................................................... 16!
3.6! Architectural Constraints............................................................................................. 16!

D. M´
endez Fern´
andez et al.


TODO: this template is too blunt
Based on the context provided, it is not possible to determine whether the requirement
Answer the following question based on this context:

{context}

Question: {question}

TODO: RIGHT NOW IT SUCKS!!! BUT the problem is in how doc is splitted and used + chat . Problem - relates too much on the context 
Final Answer: content="Based on the provided information, the requirement 'System Quality Requirements' are being discussed, specifically in relation to architectural constraints. 
The text does not explicitly mention the specific requirement 'System should be secure'. Therefore, without further context or details, 
it is not possible to determine if the requirement 'System should be secure' is good or not. Additional information or clarification would be needed to make an informed assessment." 
response_metadata={'token_usage': {'completion_tokens': 80, 'prompt_tokens': 7430, 'total_tokens': 7510}, 'model_name': 'gpt-3.5-turbo', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-b0fb3083-66bd-4639-88a5-8a999e7e81d0-0'


Original result:
content='No, the requirement "System should be secure" is not specific enough to be considered a good requirement. It is too vague and does not provide clear criteria for what constitutes security in the context of 
the system. A more effective requirement would specify the specific security measures or standards that need to be implemented, such as encryption protocols, access controls, or vulnerability assessments.' response_


TODO: Experiment 3
After adding document about requirements smells

Still bad prompt You are a helpful assistant. Answer the following question. If possible, use this context to extend and clarify your answer


Final Answer: content="Based on the information provided, it is difficult to determine if the requirement 'System should be secure' is good without further context. The validation of requirements, especially in the 
context of comparative analysis, involves understanding the specific criteria and standards for security in the system. It is important to consider factors such as the level of security needed, potential risks, and 
compliance with industry standards. Without additional details, it is recommended to further analyze and define the security requirements to ensure the system meets the necessary criteria for security." response_metadata={'token_usage': {'completion_tokens': 101, 'prompt_tokens': 12393, 'total_tokens': 12494}, 'model_name': 'gpt-3.5-turbo', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-c0146633-5bc0-4d48-983a-f79b912b8176-0'


Original result:
content='No, the requirement "System should be secure" is not a good requirement because it is too vague and does not provide specific criteria for what constitutes security. It is important to define specific security requirements such as encryption protocols, access controls, authentication mechanisms, and other security measures that need to be implemented in the system. This will help ensure that the system is adequately protected against potential threats and vulnerabilities.' response_metadata={'token_usage': {'completion_tokens': 79, 'prompt_tokens': 18, 'total_tokens': 97}, 'model_name': 'gpt-3.5-turbo', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-56a88b2a-3cb8-4bc5-8962-2add3b13369c-0'
PS C:\Users\tarasova\Desktop\Coding\ChatbotRAG> 


Result: better. However, many duplications in the selected passages. Still might be found the ones that fit better. 
"""


