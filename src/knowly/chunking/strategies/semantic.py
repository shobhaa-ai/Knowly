import re

from langchain_core.documents import Document

from src.knowly.chunking.base import BaseChunker
from src.knowly.embeddings.sentence_transformer import (
    SentenceTransformerProvider,
)


def split_sentences(text: str) -> list[str]:
    sentences = re.split(
        r"(?<=[.!?])\s+",
        text.strip(),
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


class SemanticChunker(BaseChunker):

    def __init__(self, config):
        super().__init__(config)
        self.embedding_provider = SentenceTransformerProvider()

    def chunk(
        self,
        documents: list[Document],
    ) -> list[Document]:

        chunks = []

        for document in documents:

            sentences = split_sentences(
                document.page_content
            )

            if not sentences:
                continue

            if len(sentences) == 1:
                chunks.append(
                    Document(
                        page_content=sentences[0],
                        metadata={
                            **document.metadata,
                            "chunking_strategy": "semantic",
                        },
                    )
                )
                continue

            embeddings = (
                self.embedding_provider.embed_documents(
                    sentences
                )
            )

            current_sentences = [sentences[0]]

            for index in range(1, len(sentences)):

                previous_embedding = embeddings[index - 1]
                current_embedding = embeddings[index]

                similarity = float(
                    previous_embedding @ current_embedding
                )

                current_length = len(
                    " ".join(current_sentences)
                )

                next_length = (
                    current_length
                    + 1
                    + len(sentences[index])
                )

                semantic_break = (
                    similarity
                    < self.config.similarity_threshold
                )

                size_break = (
                    next_length > self.config.chunk_size
                )

                if semantic_break or size_break:

                    chunks.append(
                        Document(
                            page_content=" ".join(
                                current_sentences
                            ),
                            metadata={
                                **document.metadata,
                                "chunking_strategy": "semantic",
                            },
                        )
                    )

                    current_sentences = [sentences[index]]

                else:
                    current_sentences.append(
                        sentences[index]
                    )

            if current_sentences:
                chunks.append(
                    Document(
                        page_content=" ".join(
                            current_sentences
                        ),
                        metadata={
                            **document.metadata,
                            "chunking_strategy": "semantic",
                        },
                    )
                )

        return chunks