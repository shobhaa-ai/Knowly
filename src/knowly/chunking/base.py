from abc import ABC, abstractmethod

from langchain_core.documents import Document

from src.knowly.chunking.config import ChunkingConfig


class BaseChunker(ABC):

    def __init__(self, config: ChunkingConfig):
        self.config = config

    @abstractmethod
    def chunk(
        self,
        documents: list[Document],
    ) -> list[Document]:
        pass