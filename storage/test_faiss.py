import faiss
import numpy as np

print("Initializing FAISS...")

# Create an index (e.g., for 384-dimensional Sentence-BERT)
dimension = 384
index = faiss.IndexFlatL2(dimension)

# Create dummy vectors
vectors = np.random.rand(5, dimension).astype('float32')
index.add(vectors)

# Search with a random query
query = np.random.rand(1, dimension).astype('float32')
distances, indices = index.search(query, 3)

print("Search results (indices):", indices)
print("Search distances:", distances)
