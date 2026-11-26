
from pathlib import Path

from src.knowly.ingestion.base import BaseDocumentLoader

from src.knowly.ingestion.loaders.pdf_loader import PDFLoader
from src.knowly.ingestion.loaders.markdown_loader import MarkdownLoader
from src.knowly.ingestion.loaders.text_loader import TextLoader
from src.knowly.ingestion.loaders.html_loader import HTMLLoader


class LoaderFactory:

    _loaders = {
        ".pdf": PDFLoader,
        ".md": MarkdownLoader,
        ".txt": TextLoader,
        ".html": HTMLLoader,
        ".htm": HTMLLoader,
    }

    @classmethod
    def get_loader(
        cls,
        file_path: Path,
    ) -> BaseDocumentLoader:

        extension = file_path.suffix.lower()

        loader_class = cls._loaders.get(extension)

        if loader_class is None:
            raise ValueError(
                f"Unsupported file format: {extension}"
            )

        return loader_class()
