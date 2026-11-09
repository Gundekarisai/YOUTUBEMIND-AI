from sentence_transformers import SentenceTransformer
from functools import lru_cache


@lru_cache(maxsize=1)
def load_embedding_model():

    model = SentenceTransformer("all-MiniLM-L6-v2")

    return model


def create_embeddings(chunks):

    model = load_embedding_model()

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return embeddings