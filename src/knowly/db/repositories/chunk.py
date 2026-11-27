import hashlib
from uuid import uuid4

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.knowly.db.models import DocumentChunk


def calculate_content_hash(content: str) -> str:
    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()


async def replace_document_chunks(
    db: AsyncSession,
    document_id: str,
    chunks: list,
) -> int:

    # Remove previously generated chunks
    await db.execute(
        delete(DocumentChunk).where(
            DocumentChunk.document_id == document_id
        )
    )

    chunk_records = []

    for index, chunk in enumerate(chunks):

        content = chunk.page_content
        metadata = chunk.metadata

        chunk_records.append(
            DocumentChunk(
                id=str(uuid4()),
                document_id=document_id,
                chunk_index=index,
                content=content,
                section_heading=metadata.get("section_heading"),
                page_number=metadata.get("page_number"),
                chunking_strategy=metadata.get(
                    "chunking_strategy",
                    "unknown",
                ),
                char_count=len(content),
                content_hash=calculate_content_hash(content),
            )
        )

    db.add_all(chunk_records)

    await db.flush()

    return len(chunk_records)