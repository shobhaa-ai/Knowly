from src.knowly.chunking.base import BaseChunker
from src.knowly.chunking.config import ChunkingConfig
from src.knowly.chunking.strategies.fixed import FixedSizeChunker
from src.knowly.chunking.strategies.recursive import RecursiveChunker


class ChunkerFactory:

    _strategies = {
        "fixed": FixedSizeChunker,
        "recursive": RecursiveChunker,
    }

    @classmethod
    def get_chunker(
        cls,
        strategy: str,
        config: ChunkingConfig,
    ) -> BaseChunker:

        chunker_class = cls._strategies.get(strategy.lower())

        if chunker_class is None:
            raise ValueError(
                f"Unsupported chunking strategy: {strategy}"
            )

        return chunker_class(config)