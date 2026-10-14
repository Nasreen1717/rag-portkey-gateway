import sys
import uuid
from pathlib import Path

from pypdf import PdfReader
from qdrant_client.models import Distance, PointStruct, VectorParams

from retriever import COLLECTION, client, model

CHUNK_SIZE = 800  # characters
OVERLAP = 150


def ensure_collection():
    if not client.collection_exists(COLLECTION):
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )


def read_file(path: Path) -> str:
    """PDF ya text file ka poora text wapas karta hai."""
    if path.suffix.lower() == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return path.read_text(encoding="utf-8", errors="ignore")


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> list[str]:
    """Text ko overlap ke saath chhote chunks mein todta hai."""
    text = " ".join(text.split())
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = end - overlap
    return [c for c in chunks if c.strip()]


def ingest_text(text: str, source: str) -> int:
    """Text ko chunk, embed aur Qdrant mein save karta hai. Chunks ki ginti wapas karta hai."""
    ensure_collection()
    chunks = chunk_text(text)
    if not chunks:
        return 0
    vectors = list(model.embed(chunks))
    points = [
        PointStruct(
            id=str(uuid.uuid5(uuid.NAMESPACE_URL, f"{source}:{i}")),
            vector=v.tolist(),
            payload={"text": c, "source": source, "chunk": i},
        )
        for i, (c, v) in enumerate(zip(chunks, vectors))
    ]
    client.upsert(collection_name=COLLECTION, points=points)
    return len(points)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Use: python ingest.py data\\yourfile.pdf")
        sys.exit(1)
    path = Path(sys.argv[1])
    n = ingest_text(read_file(path), path.name)
    print(f"Ingested {n} chunks from {path.name}")
    print("Total points in collection:", client.count(collection_name=COLLECTION).count)
    client.close()