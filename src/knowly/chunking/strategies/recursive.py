from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from src.knowly.chunking.base import BaseChunker


class RecursiveChunker(BaseChunker):

    def chunk(
        self,
        documents: list[Document],
    ) -> list[Document]:

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap,
            length_function=len,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
            add_start_index=True,
        )

        chunks = splitter.split_documents(documents)

        for chunk in chunks:
            chunk.metadata["chunking_strategy"] = "recursive"

        return chunks