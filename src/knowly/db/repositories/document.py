
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.knowly.db.models import Document


async def create_document(
    db: AsyncSession,
    filename: str,
    file_type: str,
    file_hash: str,
    storage_path: str,
):

    document = Document(
        filename=filename,
        file_type=file_type,
        file_hash=file_hash,
        storage_path=storage_path,
    )

    db.add(document)

    await db.flush()

    return document


async def get_document(
    db: AsyncSession,
    document_id: str,
):

    result = await db.execute(
        select(Document).where(
            Document.id == document_id
        )
    )

    return result.scalar_one_or_none()


async def get_document_by_hash(
    db: AsyncSession,
    file_hash: str,
):

    result = await db.execute(
        select(Document).where(
            Document.file_hash == file_hash
        )
    )

    return result.scalar_one_or_none()


async def list_documents(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 20,
):

    result = await db.execute(
        select(Document)
        .order_by(Document.created_at.desc())
        .offset(skip)
        .limit(limit)
    )

    return result.scalars().all()


async def delete_document(
    db: AsyncSession,
    document_id: str,
):

    document = await get_document(
        db,
        document_id,
    )

    if document is None:
        return False

    await db.delete(document)

    return True
