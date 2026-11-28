from src.knowly.vectorstore.client import get_chunks_collection


def upsert_chunks(
    chunks: list,
    embeddings: list[list[float]],
):

    if len(chunks) != len(embeddings):
        raise ValueError(
            "Number of chunks and embeddings must match."
        )

    if not chunks:
        return 0

    collection = get_chunks_collection()

    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:

        metadata = {
            "document_id": chunk.document_id,
            "chunk_index": chunk.chunk_index,
            "chunking_strategy": chunk.chunking_strategy,
            "char_count": chunk.char_count,
            "content_hash": chunk.content_hash,
        }

        if chunk.section_heading is not None:
            metadata["section_heading"] = chunk.section_heading

        if chunk.page_number is not None:
            metadata["page_number"] = chunk.page_number

        ids.append(chunk.id)
        documents.append(chunk.content)
        metadatas.append(metadata)

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )

    return len(ids)