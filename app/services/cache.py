import redis
import os
import json
from dotenv import load_dotenv
from app.services.embedding import get_embedding

load_dotenv()

redis_url = os.getenv("REDIS_URL")
r = redis.Redis.from_url(redis_url, decode_responses=True)

CACHE_KEY = "intellora_semantic_cache"

# Store query + embedding + answer
def set_cache(query: str, answer: str):
    embedding = get_embedding(query)
    
    entry = {
        "query": query,
        "embedding": embedding,
        "answer": answer
    }

    existing = r.get(CACHE_KEY)

    if existing:
        data = json.loads(existing)
    else:
        data = []

    data.append(entry)
    r.set(CACHE_KEY, json.dumps(data))


# Cosine similarity
def cosine_similarity(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    norm_a = sum(x*x for x in a) ** 0.5
    norm_b = sum(x*x for x in b) ** 0.5
    return dot / (norm_a * norm_b)


# Semantic search in cache
def get_cache(query: str, threshold=0.92):
    embedding = get_embedding(query)

    existing = r.get(CACHE_KEY)
    if not existing:
        return None

    data = json.loads(existing)

    for item in data:
        sim = cosine_similarity(embedding, item["embedding"])
        if sim > threshold:
            return item["answer"]

    return None


def clear_cache():
    r.delete(CACHE_KEY)