from src.document_loader import playaround_pymupdf, preprocess_scientific_paper
from src.rag_model import RAGModel
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from  langchain_core.documents.base import Document

# def invoke(question: str):
#     chain = retrieve_generate()
#     answer = chain.invoke(question)

#     return "Here is an answer " + '\n' + answer

# try:
#     while True:
#         print("\nHow can I help you? For the end of the conversation please press Ctrl+c")
#         question = input()
#         answer = invoke(question)
#         print(answer) 
# except KeyboardInterrupt:
#     pass

# rag_model = RAGModel(type='step-back')
# answer, retrieved_docs = rag_model.query("Is requirement 'System should be fast' a good requirement?")
# print("\n\nAnswer:\n\n", answer)
# print("\n\nRetrieved Documents:\n\n", retrieved_docs)
FILE2 = 'data/Naming the Pain in Requirements Engineering Contemporary Problems, Causes, and Effects in Practice.pdf'

# playaround_pymupdf(FILE2)
result = preprocess_scientific_paper()
# print(result)