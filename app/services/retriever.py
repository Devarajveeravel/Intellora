from app.services.embedding import get_embedding
from app.db.chroma_client import collection
from sentence_transformers import CrossEncoder

# 🔥 Reranker model (very powerful)
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def add_documents(docs):
    for i, doc in enumerate(docs):
        embedding = get_embedding(doc)
        collection.add(
            documents=[doc],
            embeddings=[embedding],
            ids=[str(i)]
        )


def retrieve(query):
    query_embedding = get_embedding(query)

    # 🔥 Step 1: Get top 5 candidates
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    docs = results["documents"][0]

    # 🔥 Step 2: Rerank
    pairs = [(query, doc) for doc in docs]
    scores = reranker.predict(pairs)

    # Combine doc + score
    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)

    # 🔥 Step 3: Return top 2 best
    top_docs = [doc for doc, _ in ranked[:2]]

    return top_docs