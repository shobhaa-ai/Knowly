
from pathlib import Path

from pypdf import PdfReader
from langchain_core.documents import Document

from src.knowly.ingestion.base import BaseDocumentLoader


class PDFLoader(BaseDocumentLoader):

    def load(
        self,
        file_path: Path,
    ) -> list[Document]:

        with open(file_path, "rb") as f:
            header = f.read(5)

        if header != b"%PDF-":
            text = file_path.read_text(encoding="utf-8", errors="replace")
            return [Document(page_content=text, metadata={"source": file_path.name, "file_type": "txt", "page_number": 1, "section_heading": None})] if text.strip() else []

        reader = PdfReader(str(file_path))

        documents = []

        for page_number, page in enumerate(
            reader.pages,
            start=1,
        ):

            content = page.extract_text() or ""

            if not content.strip():
                continue

            documents.append(
                Document(
                    page_content=content,
                    metadata={
                        "source": file_path.name,
                        "file_type": "pdf",
                        "page_number": page_number,
                        "section_heading": None,
                    },
                )
            )

        return documents
