import re
from os import listdir, path
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb
import pymupdf
from  langchain_core.documents.base import Document

PATH_DOCUMENTS = 'data/first_batch'
PERSIST_DIRECTORY = 'chroma_db'


def filter_text(text: list[Document]) -> list[Document]:
    # Define the pattern to match unwanted lines
    pattern = re.compile(r'(.*\..*){4,}')

    filtered_text = []

    # Split the text into lines
    for page in text:
        lines = page.page_content.split('\n')

        # Filter out lines that match the pattern
        filtered_lines = [line for line in lines if not pattern.match(line)]

        # Join the filtered lines back into a single string
        # filtered_text.extend(filtered_lines)

        filtered_text = '\n' + ''.join(filtered_lines)

        page.page_content = filtered_text

    return text


def create_db():
    docs = [file for file in listdir(PATH_DOCUMENTS) if path.isfile(
        path.join(PATH_DOCUMENTS, file))]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300, chunk_overlap=50)
    pages = []

    for doc in docs:
        # Split
        doc_path = path.join(PATH_DOCUMENTS, doc)
        loader = PyMuPDFLoader(doc_path)

        text = loader.load_and_split(text_splitter=text_splitter)

        filtered_text = filter_text(text)

        pages.extend(filtered_text)

    vectorstore = Chroma.from_documents(documents=pages,
                                        embedding=OpenAIEmbeddings(),
                                        persist_directory=PERSIST_DIRECTORY)


def shape(lst):
    length = len(lst)
    shp = tuple(shape(sub) if isinstance(sub, list) else 0 for sub in lst)
    if any(x != 0 for x in shp):
        return length, shp
    else:
        return length


def get_db():
    # vector_store = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=OpenAIEmbeddings())
    # result = vector_store.search("artefact-oriented re", search_type="similarity")
    vector_store = chromadb.PersistentClient(path=PERSIST_DIRECTORY)
    collections = vector_store.list_collections()
    if collections.count == 0:
        print("There are no collections in db")
    for collection in collections:
        print("\n\nnumber of items in the collection: " + str(collection.count()))
        # print(collection.peek(limit=1))


def add_doc_todb(doc_path):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300, chunk_overlap=50)

    loader = PyMuPDFLoader(doc_path)

    pages = loader.load_and_split(text_splitter=text_splitter)

    vector_store = Chroma(persist_directory=PERSIST_DIRECTORY,
                          embedding_function=OpenAIEmbeddings())
    vector_store.add_documents(pages)

def add_docs_from_folder(folder_path):
    docs = [file for file in listdir(folder_path) if path.isfile(
    path.join(PATH_DOCUMENTS, file))]

    for doc in docs:
        add_doc_todb(doc)


def playaround_pymupdf(doc_path='data/first_batch/Rapid quality assurance with Requirements Smells.pdf'):

    doc = pymupdf.open(doc_path)

    page = doc.load_page(0)
    content = page.get_contents()
    print("content")
    print(content)
    links = page.get_links()
    print("links")
    for link in page.links():
        print(link)
    print("annots")
    for annot in page.annots():
        # do something with 'annot'
        print(annot)

    text = page.get_text("blocks")
    for t in text:
        print(t)

create_db()
get_db()
# add_docs_todb('data\_second_batch\Rapid quality assurance with Requirements Smells.pdf')
# get_db()



"""For more refined document adding 
from langchain.docstore.document import Document

new_doc =  Document(
    page_content="Wareconn is the best web platform for warranty maintenance.",
    metadata={
        "source": "wareconn.com",
        "page": 1
    }
)


Expertiment 1.
number of items in the collection: 1964
number of items in the collection: 2526
Still one collection

TODO: Experiment 2 
Added a filtering function for text, so that it doesn't include content 
"""
