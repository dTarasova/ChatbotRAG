import random
import chromadb
from chromadb.utils import embedding_functions

PATH_DOCUMENTS = 'data/processed_pdfs'
PERSIST_DIRECTORY = 'chroma_db_larger'

def get_db():
    vector_store = chromadb.PersistentClient(path=PERSIST_DIRECTORY)
    collections = vector_store.list_collections()
    if collections.count == 0:
        print("There are no collections in db")
    for collection in collections:
        print("\n\nnumber of items in the collection: " + str(collection.count()))
        # print(collection.peek(limit=1))
    return vector_store

def get_documents():
    vector_store = get_db()
    documents = vector_store.list_collections()
    documents = vector_store.get_collection("langchain").get()
    print("Documents retrieved from db" + str(len(documents)))
    return documents

# Assuming you have already set up your ChromaDB collection
# and it is stored in `collection`.

def get_random_texts_by_category(metadata_tag='source', num_samples=4):
    # Get all distinct categories (sources)

    vector_store = get_db()
    
    collection = vector_store.get_collection("langchain")
    
    distinct_sources = collection.get_distinct_metadata_values(metadata_tag)

    # Dictionary to hold the results
    random_texts_by_category = {}

    for source in distinct_sources:
        # Query the collection to get all documents with the current source
        results = collection.get(
            where={metadata_tag: source},
            include=['documents']
        )
        
        # Get the documents from the results
        documents = results['documents']
        
        # Ensure we can get the required number of samples
        if len(documents) > num_samples:
            sampled_texts = random.sample(documents, num_samples)
        else:
            sampled_texts = documents  # Not enough documents to sample, return all of them
        
        # Store the sampled texts in the dictionary
        random_texts_by_category[source] = sampled_texts

    return random_texts_by_category



