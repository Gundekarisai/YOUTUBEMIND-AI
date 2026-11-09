import numpy as np

from backend.embeddings import load_embedding_model


def search_similar_chunks(query, index, chunks, top_k=3):

    # Load embedding model
    model = load_embedding_model()

    # Convert user question into embedding
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    # Convert into float32
    query_embedding = np.array(query_embedding).astype("float32")

    # Search FAISS database
    scores, indices = index.search(
        query_embedding,
        min(top_k, len(chunks))
    )

    results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx != -1:

            results.append({
                "chunk": chunks[idx],
                "score": float(score)
            })

    return results