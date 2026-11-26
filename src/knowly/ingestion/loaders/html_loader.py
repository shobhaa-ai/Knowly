
from pathlib import Path

from bs4 import BeautifulSoup
from langchain_core.documents import Document

from src.knowly.ingestion.base import BaseDocumentLoader


class HTMLLoader(BaseDocumentLoader):

    def load(
        self,
        file_path: Path,
    ) -> list[Document]:

        html_content = file_path.read_text(
            encoding="utf-8"
        )

        soup = BeautifulSoup(
            html_content,
            "html.parser",
        )

        # Remove non-content elements
        for element in soup(
            ["script", "style", "noscript"]
        ):
            element.decompose()

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
                            "file_type": "html",
                            "page_number": None,
                            "section_heading": current_heading,
                        },
                    )
                )

        for element in soup.find_all(
            [
                "h1", "h2", "h3", "h4",
                "p", "li", "pre", "blockquote"
            ]
        ):

            text = element.get_text(
                separator=" ",
                strip=True,
            )

            if not text:
                continue

            if element.name in ["h1", "h2", "h3", "h4"]:

                save_section()

                current_heading = text
                current_content = []

            else:
                current_content.append(text)

        save_section()

        return documents
