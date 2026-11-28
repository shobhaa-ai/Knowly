import chromadb
from pathlib import Path


CHROMA_DIR = Path("data/chroma")
COLLECTION_NAME = "knowly_chunks"


def get_chroma_client():

    CHROMA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    return chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )


def get_chunks_collection():

    client = get_chroma_client()

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={
            "hnsw:space": "cosine"
        },
    )

    return collection