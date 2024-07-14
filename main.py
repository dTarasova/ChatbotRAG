
from src.retriever_generator import get_db
from src.document_loader import create_db
from src.document_preprocessor import process_pdf
from src.rag_model import RAGModel
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from  langchain_core.documents.base import Document

from src.wo_rag import get_openai_answer

try:
    while True:
        print("\nHow can I help you? For the end of the conversation please press Ctrl+c")
        question = input()
        rag_model = RAGModel(type='step-back')
        print_context = True
        answer, context = rag_model.query(question)
        print("\n\nAnswer:\n\n", answer)
        if print_context:
            print("\n\nContext:\n\n")
            print(context)

        openai_answer = get_openai_answer(question)
        print("\n\n Regular OpenAI without context: \n\n")
        print(openai_answer)


        rag2_model = RAGModel(type='structured_data')
        answer2, context2 = rag2_model.query(question)
        print("\n\nAnswer with data from NAPiRE:\n\n", answer2)  
        print("\n\nNAPiRE Context:\n\n")
        print(context2)

except KeyboardInterrupt:
    pass

# rag_model = RAGModel(type='step-back')
# answer, retrieved_docs = rag_model.query("Is requirement 'System should be fast' a good requirement?")
# print("\n\nAnswer:\n\n", answer)
# print("\n\nRetrieved Documents:\n\n", retrieved_docs)

# FILE1 = 'data/first_batch/Rapid quality assurance with Requirements Smells.pdf'
# FILE2 = 'data/Naming the Pain in Requirements Engineering Contemporary Problems, Causes, and Effects in Practice.pdf'

# playaround_pymupdf(FILE2)


# process_pdf(FILE2, 'text_new.txt')
# create_db()

# from huggingface_hub import InferenceClient
# client = InferenceClient()

# image = client.text_to_image("An astronaut riding a horse on the moon.")
# image.save("astronaut.png")