from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.knowly.db.models import Document, DocumentChunk
from src.knowly.embeddings.sentence_transformer import get_embedding_provider
from src.knowly.vectorstore.repository import upsert_chunks



async def embed_document(
    document_id: str,
    db: AsyncSession,
    batch_size: int = 64,
):

    document = await db.get(Document, document_id)

    if not document:
        raise ValueError(
            f"Document not found: {document_id}"
        )

    result = await db.execute(
        select(DocumentChunk)
        .where(
            DocumentChunk.document_id == document_id
        )
        .order_by(DocumentChunk.chunk_index)
    )

    chunks = result.scalars().all()

    if not chunks:
        raise ValueError(
            "No chunks found for this document."
        )

    embedding_provider = get_embedding_provider()

    total_embedded = 0

    try:

        # Process chunks in batches
        for start in range(0, len(chunks), batch_size):

            batch = chunks[start:start + batch_size]

            texts = [
                chunk.content
                for chunk in batch
            ]

            embeddings = (
                embedding_provider.embed_documents(texts)
            )

            embedded_count = upsert_chunks(
                chunks=batch,
                embeddings=embeddings,
            )

            total_embedded += embedded_count

        document.status = "embedded"

        await db.commit()

        return {
            "status": "success",
            "document_id": document_id,
            "total_chunks_embedded": total_embedded,
        }

    except Exception:
        await db.rollback()
        raise