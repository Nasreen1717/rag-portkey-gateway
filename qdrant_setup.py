from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from fastembed import TextEmbedding

COLLECTION = "docs"

client = QdrantClient(path="qdrant_data")
model = TextEmbedding("BAAI/bge-small-en-v1.5")  # 384 dimensions

docs = [
    "A vector database stores embeddings and finds similar items fast.",
    "FastAPI is a Python framework for building APIs.",
    "Portkey is an AI gateway for routing, retries, and observability.",
    "LangGraph helps build multi-step AI agents as graphs.",
    "FlashRank reranks search results to improve relevance.",
]

vectors = list(model.embed(docs))

if client.collection_exists(COLLECTION):
    client.delete_collection(COLLECTION)

client.create_collection(
    collection_name=COLLECTION,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

client.upsert(
    collection_name=COLLECTION,
    points=[
        PointStruct(id=i, vector=v.tolist(), payload={"text": d})
        for i, (d, v) in enumerate(zip(docs, vectors))
    ],
)
print("Stored", len(docs), "docs in Qdrant")

query = "What is a vector database?"
qv = list(model.embed([query]))[0].tolist()
result = client.query_points(collection_name=COLLECTION, query=qv, limit=3)

print("\nTop results for:", query)
for p in result.points:
    print(round(p.score, 3), "|", p.payload["text"])

client.close()