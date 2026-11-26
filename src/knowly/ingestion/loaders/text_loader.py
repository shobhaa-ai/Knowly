
from pathlib import Path

from langchain_core.documents import Document

from src.knowly.ingestion.base import BaseDocumentLoader


class TextLoader(BaseDocumentLoader):

    def load(
        self,
        file_path: Path,
    ) -> list[Document]:

        content = file_path.read_text(
            encoding="utf-8"
        )

        if not content.strip():
            return []

        return [
            Document(
                page_content=content,
                metadata={
                    "source": file_path.name,
                    "file_type": "txt",
                    "page_number": None,
                    "section_heading": None,
                },
            )
        ]
