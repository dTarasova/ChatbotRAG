from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_openai.embeddings import OpenAIEmbeddings
AMDIRE_PDF_PATH = "data/amdire.pdf"

loader = PyPDFLoader(AMDIRE_PDF_PATH)

pages = loader.load_and_split()

embeddings = OpenAIEmbeddings()
vectorstore = DocArrayInMemorySearch.from_documents(pages, embedding=embeddings)
