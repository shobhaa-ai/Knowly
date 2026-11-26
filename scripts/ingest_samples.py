
import asyncio

from pathlib import Path

from src.knowly.db.session import AsyncSessionLocal
from src.knowly.ingestion.service import ingest_file


SAMPLE_DIR = Path("data/samples")


async def main():

    files = list(SAMPLE_DIR.iterdir())

    if not files:
        print("No sample documents found.")
        return

    async with AsyncSessionLocal() as db:

        for file_path in files:

            if not file_path.is_file():
                continue

            print(f"\nProcessing: {file_path.name}")

            try:

                result = await ingest_file(
                    file_path=file_path,
                    db=db,
                )

                print(result)

            except Exception as error:

                print(
                    f"Failed to ingest {file_path.name}: {error}"
                )


if __name__ == "__main__":
    asyncio.run(main())
