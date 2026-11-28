from src.knowly.embeddings.sentence_transformer import get_embedding_provider
from src.knowly.vectorstore.client import get_chunks_collection


def semantic_search(
    query: str,
    top_k: int = 5,
):

    embedding_provider = get_embedding_provider()

    # Convert the user query into a vector
    query_embedding = embedding_provider.embed_query(query)

    collection = get_chunks_collection()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    matches = []

    for index, content in enumerate(
        results["documents"][0]
    ):

        matches.append({
            "content": content,
            "metadata": results["metadatas"][0][index],
            "distance": results["distances"][0][index],
        })

    return matches