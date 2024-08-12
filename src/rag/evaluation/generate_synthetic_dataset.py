from ragas.testset.generator import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning, multi_context
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader

from src.rag.retriever.unstructured_data_loading.document_loader import get_db
import os


DIRECTORY_PATH = "data/processed_texts_txt"


def get_documents(directory_path=DIRECTORY_PATH): 
    text_loader_kwargs = {"autodetect_encoding": True}
    loader = DirectoryLoader(directory_path, glob="**/*.txt", loader_cls=TextLoader, loader_kwargs=text_loader_kwargs, silent_errors=True)
    documents = loader.load()
    for document in documents:
        document.metadata['filename'] = document.metadata['source']
    return documents
    # documents = [file for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]
    # for document in documents:
    #     loader = TextLoader(document, encoding = 'UTF-8')
    #     subdocs = loader.load()
    #     for subdoc in subdocs:
    #         document.metadata['source'] = document.metadata['filename']
    #         document.metadata['filename'] = document.metadata['source']
    #     document.metadata['filename'] = document.metadata['source']


    # return documents



# def get_documents():
#     vector_store = get_db()
#     documents = vector_store.list_collections()
#     documents = vector_store.get_collection("langchain").get()
#     print("Documents retrieved from db" + str(len(documents)))
#     return documents

def generate(documents=None): 
    # 2 euros for running generator_llm
    # 2,5 euros for running critic_llm
    # for 10 testset
    if documents is None: 
        documents = get_documents()

    generator_llm = ChatOpenAI(model="gpt-3.5-turbo-16k")
    critic_llm = ChatOpenAI(model="gpt-4")
    embeddings = OpenAIEmbeddings()

    generator = TestsetGenerator.from_langchain(
        generator_llm,
        critic_llm,
        embeddings
    )

    testset = generator.generate_with_langchain_docs(documents, test_size=10, distributions={simple: 0.5, reasoning: 0.25, multi_context: 0.25})
    testset.to_pandas().to_csv("data/synthetic_testset.csv")
    testset.to_pandas().to_json("data/synthetic_testset.json", orient="records")
