
import json
from src.rag.retriever.unstructured_data_loading.documents_extractor import get_random_texts_by_category


def get_contexts():
    random_contexts = get_random_texts_by_category()
    json.dump(random_contexts, open("data/random_contexts.json", "w"))

    