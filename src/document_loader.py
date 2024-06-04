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


def playaround_pymupdf(doc_path='data/Naming the Pain in Requirements Engineering Contemporary Problems, Causes, and Effects in Practice.pdf'):

    doc = pymupdf.open(doc_path)
    toc = doc.get_toc()

    for toc_item in toc:
        print(toc_item)
    one_toc = toc[0]
    print("\n\none_toc")
    for toc_item in one_toc:
        print(toc_item)
        print(type(toc_item))

    
    #[[lvl, title, page, …], …]
    # page = doc.load_page(0)
    # content = page.get_contents()
    # print("content")
    # print(content)
    # links = page.get_links()
    # print("links")
    # for link in page.links():
    #     print(link)
    # print("annots")
    # for annot in page.annots():
    #     # do something with 'annot'
    #     print(annot)

    # text = page.get_text("blocks")
    # for t in text:
    #     print(t)


# add_docs_todb('data\_second_batch\Rapid quality assurance with Requirements Smells.pdf')
# get_db()

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    document = pymupdf.open(pdf_path)
    text = ''
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

def extract_paragraphs(pdf_path):
    document = pymupdf.open(pdf_path)
    text = []
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        paragraphs = page.get_text("blocks")
        #print(paragraphs)
        text.extend(paragraphs)
    return text

def remove_references(text):
    """
    Removes the references section from the text.
    Assumes the references section starts with a heading like 'References' or 'Bibliography'
    and continues until the end of the document.
    """
    #TODO: search from the end
    #TODO: verify that it is one line word
    # Create a regex pattern to match the references section heading and its content
    pattern = re.compile(r'(References|Bibliography).*', re.DOTALL | re.IGNORECASE)
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

FILE2 = 'data/Naming the Pain in Requirements Engineering Contemporary Problems, Causes, and Effects in Practice.pdf'
FILE1 = 'data/first_batch/Rapid quality assurance with Requirements Smells.pdf'
def preprocess_scientific_paper(file_path = FILE1):
    # Extract text from file
    text = extract_text_from_pdf(file_path)

    # Remove the references section
    cleaned_text = remove_references(text)

    
    paragraphs = extract_paragraphs(file_path)
    try: 
        with open('text.txt', "w", encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print(f"An error occurred: {e}")
    paragraphs_text = ''
    for paragraph in paragraphs:
        paragraphs_text += paragraph[4] + '\n\n'

    print(type(paragraphs[0]))
    for p in paragraphs[0]:
        print(type(p))
    

    # cleaned_paragraphs = remove_references(paragraphs_text)
    with open('paragraphs.txt', "w", encoding="utf-8") as f:
        f.write(paragraphs_text)



    return cleaned_text


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
