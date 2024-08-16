import pandas as pd
import nest_asyncio
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
import pandas as pd


def evaluate(): 
    test_df = pd.read_csv("data/synthetic_testset.csv", header=0)
    test_questions = test_df['question'].values.tolist()
    test_answers = rag_model.query(test_questions, query_types=[RAGTypes.TEXT_DATA])
    test_answers = [[item] for item in test_df['answer'].values.tolist()]

def build_query_engine(embed_model):
    vector_index = VectorStoreIndex.from_documents(
        documents, service_context=ServiceContext.from_defaults(chunk_size=512),
        embed_model=embed_model,
    )

    query_engine = vector_index.as_query_engine(similarity_top_k=2)
    return query_engine