import json
from pathlib import Path

from langchain_core.documents import Document

from src.knowly.chunking.config import ChunkingConfig
from src.knowly.chunking.factory import ChunkerFactory


PROCESSED_DIR = Path("data/processed")


def main():

    files = list(PROCESSED_DIR.glob("*.json"))

    if not files:
        print("No processed documents found. Run ingestion first.")
        return

    config = ChunkingConfig(
        chunk_size=500,
        chunk_overlap=100,
    )

    for file_path in files:

        data = json.loads(file_path.read_text(encoding="utf-8"))

        documents = [
            Document(
                page_content=item["page_content"],
                metadata=item["metadata"],
            )
            for item in data
        ]

        print(f"\nDocument: {file_path.name}")

        for strategy in ["fixed", "recursive"]:

            chunker = ChunkerFactory.get_chunker(
                strategy=strategy,
                config=config,
            )

            chunks = chunker.chunk(documents)

            print(f"\nStrategy: {strategy}")
            print(f"Total chunks: {len(chunks)}")

            for index, chunk in enumerate(chunks[:3]):
                print(f"\nChunk {index + 1}")
                print(f"Characters: {len(chunk.page_content)}")
                print(f"Metadata: {chunk.metadata}")
                print(f"Content: {chunk.page_content[:200]}")


if __name__ == "__main__":
    main()