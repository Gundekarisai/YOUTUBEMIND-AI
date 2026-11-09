import faiss
import numpy as np


def create_vector_store(embeddings):

    # Convert embeddings into float32
    vectors = np.array(embeddings).astype("float32")

    # Get embedding dimensions
    dimension = vectors.shape[1]

    # Create FAISS index
    index = faiss.IndexFlatIP(dimension)

    # Add embeddings to FAISS
    index.add(vectors)

    return index