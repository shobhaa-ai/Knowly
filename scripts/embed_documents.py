import asyncio

from sqlalchemy import select

from src.knowly.db.session import AsyncSessionLocal
from src.knowly.embeddings.service import embed_document
from src.knowly.db.models import Document


async def main():

    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(Document).where(
                Document.status.in_(
                    ["chunked", "embedded"]
                )
            )
        )

        documents = result.scalars().all()

        if not documents:
            print("No chunked documents found.")
            return

        for document in documents:

            print(f"\nEmbedding: {document.filename}")

            try:
                result = await embed_document(
                    document_id=document.id,
                    db=db,
                    batch_size=64,
                )

                print(result)

            except Exception as error:
                print(
                    f"Failed to embed {document.filename}: {error}"
                )


if __name__ == "__main__":
    asyncio.run(main())