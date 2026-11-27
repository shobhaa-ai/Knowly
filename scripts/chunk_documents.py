import asyncio

from sqlalchemy import select

from src.knowly.db.models import Document as DocumentModel
from src.knowly.db.session import AsyncSessionLocal
from src.knowly.chunking.config import ChunkingConfig
from src.knowly.chunking.service import chunk_document


async def main():

    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(DocumentModel).where(
                DocumentModel.status.in_(
                    ["processed", "chunked"]
                )
            )
        )

        documents = result.scalars().all()

        if not documents:
            print("No processed documents found.")
            return

        for document in documents:

            print(f"\nProcessing: {document.filename}")

            try:
                result = await chunk_document(
                    document_id=document.id,
                    db=db,
                    strategy="semantic",
                    config=ChunkingConfig(
                        chunk_size=500,
                        chunk_overlap=100,
                    ),
                )

                print(result)

            except Exception as error:
                print(f"Failed: {error}")


if __name__ == "__main__":
    asyncio.run(main())