import json
from pathlib import Path

from langchain_core.documents import Document
from sqlalchemy.ext.asyncio import AsyncSession

from src.knowly.chunking.config import ChunkingConfig
from src.knowly.chunking.factory import ChunkerFactory
from src.knowly.db.models import Document as DocumentModel
from src.knowly.db.repositories.chunk import replace_document_chunks
import asyncio


PROCESSED_DIR = Path("data/processed")


async def chunk_document(
    document_id: str,
    db: AsyncSession,
    strategy: str = "recursive",
    config: ChunkingConfig | None = None,
):

    document = await db.get(DocumentModel, document_id)

    if not document:
        raise ValueError(
            f"Document not found: {document_id}"
        )

    processed_path = PROCESSED_DIR / f"{document_id}.json"

    if not processed_path.is_file():
        raise FileNotFoundError(
            f"Processed file not found: {processed_path}"
        )

    try:
        # Load previously extracted document sections
        data = json.loads(
            processed_path.read_text(encoding="utf-8")
        )

        documents = [
            Document(
                page_content=item["page_content"],
                metadata=item["metadata"],
            )
            for item in data
        ]

        if not documents:
            raise ValueError("No extracted content available.")

        # Use default configuration if none is supplied
        config = config or ChunkingConfig()

        # Select chunking strategy
        chunker = ChunkerFactory.get_chunker(
            strategy=strategy,
            config=config,
        )

        chunks = await asyncio.to_thread(
            chunker.chunk,
            documents,
        )

        if not chunks:
            raise ValueError("Chunking produced no results.")

        # Replace old chunks and save new chunks
        total_chunks = await replace_document_chunks(
            db=db,
            document_id=document_id,
            chunks=chunks,
        )

        document.status = "chunked"

        await db.commit()

        return {
            "status": "success",
            "document_id": document_id,
            "strategy": strategy,
            "total_chunks": total_chunks,
        }

    except Exception:
        await db.rollback()
        raise