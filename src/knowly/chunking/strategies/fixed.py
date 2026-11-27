from langchain_core.documents import Document

from src.knowly.chunking.base import BaseChunker


class FixedSizeChunker(BaseChunker):

    def chunk(
        self,
        documents: list[Document],
    ) -> list[Document]:

        chunks = []

        chunk_size = self.config.chunk_size
        overlap = self.config.chunk_overlap
        step = chunk_size - overlap

        for document in documents:
            text = document.page_content
            start = 0

            while start < len(text):
                end = min(start + chunk_size, len(text))

                content = text[start:end].strip()

                if content:
                    metadata = document.metadata.copy()
                    metadata["chunking_strategy"] = "fixed"
                    metadata["start_index"] = start

                    chunks.append(
                        Document(
                            page_content=content,
                            metadata=metadata,
                        )
                    )

                if end == len(text):
                    break

                start += step

        return chunks