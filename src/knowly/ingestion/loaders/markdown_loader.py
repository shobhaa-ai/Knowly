
from pathlib import Path

from langchain_core.documents import Document

from src.knowly.ingestion.base import BaseDocumentLoader


class MarkdownLoader(BaseDocumentLoader):

    def load(
        self,
        file_path: Path,
    ) -> list[Document]:

        content = file_path.read_text(
            encoding="utf-8"
        )

        documents = []

        current_heading = "General"
        current_content = []

        def save_section():

            text = "\n".join(current_content).strip()

            if text:
                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": file_path.name,
                            "file_type": "md",
                            "page_number": None,
                            "section_heading": current_heading,
                        },
                    )
                )

        for line in content.splitlines():

            stripped = line.strip()

            if stripped.startswith("#"):

                save_section()

                current_heading = stripped.lstrip("#").strip()
                current_content = []

            else:
                current_content.append(line)

        save_section()

        return documents
