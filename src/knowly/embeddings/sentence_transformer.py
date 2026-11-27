from sentence_transformers import SentenceTransformer

from src.knowly.embeddings.base import BaseEmbeddingProvider


class SentenceTransformerProvider(BaseEmbeddingProvider):

    _model = None

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        if SentenceTransformerProvider._model is None:
            SentenceTransformerProvider._model = (
                SentenceTransformer(model_name)
            )

        self.model = SentenceTransformerProvider._model

    def embed_documents(self, texts: list[str]):
        return self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )