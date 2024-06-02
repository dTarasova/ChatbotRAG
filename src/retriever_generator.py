from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate

PERSIST_DIRECTORY = 'chroma_db' #TODO: constants store somewhere in 1 place

def get_db():
    vector_store = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=OpenAIEmbeddings())
    result = vector_store.search("artefact-oriented re", search_type="similarity")
    # vector_store = chromadb.Client()
    # result = vector_store.list_collections()

    print (result)

def get_retriever():
    vector_store = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=OpenAIEmbeddings())
    return vector_store.as_retriever()

def get_llm():
    llm = ChatOpenAI(temperature=0)
    return llm

def get_retriever_prompt_basic():
    return hub.pull("rlm/rag-prompt")


def get_retriever_prompt():
    return get_retriever_prompt_basic()



def retrieve_generate():
    vector_store = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=OpenAIEmbeddings())
    retriever = vector_store.as_retriever()
    
    prompt = get_retriever_prompt()
    # LLM
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)



    # Chain
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain

    # Post-processing
def format_docs(docs):
    result = "\n\n".join(doc.page_content for doc in docs)
    print(result)
    return result
