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


vector_store = Chroma(persist_directory='chroma_db', embedding_function=OpenAIEmbeddings())
retriever = vector_store.as_retriever()
answer = retriever.invoke("mendez")
print(answer)
print('\n\n\n')
rag_model = RAGModel()
retriever2 = rag_model.retriever.get_retriever()
print(retriever2.invoke("mendez"))
# answer, retrieved_docs = rag_model.query("Is requirement 'System should be fast' a good requirement?")
# print("\n\nAnswer:\n\n", answer)
# print("\n\nRetrieved Documents:\n\n", retrieved_docs)