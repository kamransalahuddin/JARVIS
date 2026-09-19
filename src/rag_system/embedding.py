import numpy as np
from sentence_transformers import SentenceTransformer
from .rag import read_context
doc_embeddings_list = []
context = read_context()
# Load the model
model = SentenceTransformer("Qwen/Qwen3-VL-Embedding-2B")
for i in context:
        doc_embeddings = model.encode(i)
        doc_embeddings_list.append(doc_embeddings)

def embed(text):
    query = text
    query_embeddings = model.encode(query)
    similarities = []

    for i in range(len(doc_embeddings_list)):
        dot = np.dot(query_embeddings, doc_embeddings_list[i])
        abs = np.linalg.norm(query_embeddings) * np.linalg.norm(doc_embeddings_list[i])
        similarity = dot / abs
        similarities.append(similarity)

    
    
    top_three = np.argsort(similarities)[-3:][::-1]
        

    return [context[i] for i in top_three]


