from qdrant_client import QdrantClient
from fastembed import TextEmbedding
from flashrank import Ranker, RerankRequest

COLLECTION = "docs"

# Ek hi baar load hote hain (import par)
client = QdrantClient(path="qdrant_data")
model = TextEmbedding("BAAI/bge-small-en-v1.5")
ranker = Ranker()  # default tiny model, pehli baar download hoga


def retrieve(query: str, k: int = 15) -> list[str]:
    """Qdrant se top-k chunks (text) wapas karta hai."""
    qv = list(model.embed([query]))[0].tolist()
    result = client.query_points(collection_name=COLLECTION, query=qv, limit=k)
    return [p.payload["text"] for p in result.points]


def rerank(query: str, chunks: list[str], top_n: int = 5) -> list[str]:
    """FlashRank se chunks ko relevance ke hisab se dobara sort karta hai."""
    passages = [{"id": i, "text": c} for i, c in enumerate(chunks)]
    results = ranker.rerank(RerankRequest(query=query, passages=passages))
    for r in results[:top_n]:
        print(f"  score={r['score']:.3f} | {r['text']}")
    return [r["text"] for r in results[:top_n]]


def retrieve_docs(query: str, k: int = 15) -> list[dict]:
    """Qdrant se top-k chunks, text + source + chunk number ke saath."""
    qv = list(model.embed([query]))[0].tolist()
    result = client.query_points(collection_name=COLLECTION, query=qv, limit=k)
    return [
        {
            "text": p.payload["text"],
            "source": p.payload.get("source", "sample"),
            "chunk": p.payload.get("chunk"),
        }
        for p in result.points
    ]


def rerank_docs(query: str, docs: list[dict], top_n: int = 5) -> list[dict]:
    """FlashRank rerank, lekin source/chunk/score ke saath dict wapas karta hai."""
    passages = [
        {
            "id": i,
            "text": d["text"],
            "meta": {"source": d["source"], "chunk": d["chunk"]},
        }
        for i, d in enumerate(docs)
    ]
    results = ranker.rerank(RerankRequest(query=query, passages=passages))
    out = []
    for r in results[:top_n]:
        meta = r.get("meta") or {}
        out.append(
            {
                "text": r["text"],
                "source": meta.get("source", "sample"),
                "chunk": meta.get("chunk"),
                "score": round(float(r["score"]), 4),
            }
        )
    return out


if __name__ == "__main__":
    q = "What is Portkey used for?"
    docs = retrieve_docs(q, k=15)
    print("Reranked:")
    for d in rerank_docs(q, docs, top_n=5):
        print(f"  {d['score']} | {d['source']} #{d['chunk']} | {d['text'][:80]}")
    client.close()