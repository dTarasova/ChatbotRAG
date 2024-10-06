from enum import Enum, auto

class VectorStoreType(Enum):
    CHROMA = auto()
    FAISS = auto()