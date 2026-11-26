
import asyncio
import hashlib
import json
import shutil

from pathlib import Path
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from src.knowly.db.repositories.document import (
    create_document,
    get_document_by_hash,
)

from src.knowly.ingestion.factory import LoaderFactory
from src.knowly.ingestion.normalizer import normalize_documents


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


def calculate_file_hash(file_path: Path) -> str:

    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:

        for block in iter(
            lambda: file.read(1024 * 1024),
            b"",
        ):
            sha256.update(block)

    return sha256.hexdigest()


async def ingest_file(
    file_path: Path,
    db: AsyncSession,
):

    if not file_path.is_file():
        raise FileNotFoundError(file_path)

    # 1. Validate file format
    loader = LoaderFactory.get_loader(file_path)

    # 2. Calculate SHA-256 hash
    file_hash = await asyncio.to_thread(
        calculate_file_hash,
        file_path,
    )

    # 3. Check for an existing document
    existing_document = await get_document_by_hash(
        db,
        file_hash,
    )

    if existing_document:
        return {
            "status": "duplicate",
            "document_id": existing_document.id,
            "filename": existing_document.filename,
        }

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    original_filename = file_path.name

    # 4. Preserve the original file
    raw_filename = (
        f"{uuid4().hex}_{original_filename}"
    )

    raw_path = RAW_DIR / raw_filename

    # Keep a relative path in the database
    storage_path = raw_path.as_posix()

    processed_path = None

    try:

        await asyncio.to_thread(
            shutil.copy2,
            file_path,
            raw_path,
        )

        # 5. Extract content
        documents = await asyncio.to_thread(
            loader.load,
            raw_path,
        )

        # Preserve the original uploaded filename in metadata
        for document in documents:
            document.metadata["source"] = original_filename

        # 6. Normalize content
        documents = normalize_documents(documents)

        if not documents:
            raise ValueError(
                "No readable text found in the document."
            )

        # 7. Create document record
        document = await create_document(
            db=db,
            filename=original_filename,
            file_type=file_path.suffix.lower().lstrip("."),
            file_hash=file_hash,
            storage_path=storage_path,
        )

        # 8. Save processed representation
        processed_path = (
            PROCESSED_DIR / f"{document.id}.json"
        )

        processed_data = [
            {
                "page_content": item.page_content,
                "metadata": item.metadata,
            }
            for item in documents
        ]

        await asyncio.to_thread(
            processed_path.write_text,
            json.dumps(
                processed_data,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        # 9. Update document status
        document.status = "processed"

        # 10. Commit transaction
        await db.commit()

        return {
            "status": "processed",
            "document_id": document.id,
            "filename": original_filename,
            "file_type": document.file_type,
            "sections_extracted": len(documents),
            "storage_path": storage_path,
            "processed_path": processed_path.as_posix(),
        }

    except Exception:

        await db.rollback()

        # Clean up files if ingestion fails
        if raw_path.exists():
            raw_path.unlink()

        if processed_path and processed_path.exists():
            processed_path.unlink()

        raise
