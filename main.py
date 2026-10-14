import io
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel
from pypdf import PdfReader

from feature11_langgraph import app as rag_graph
from ingest import ingest_text
from retriever import client as qdrant_client


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield
    qdrant_client.close()


api = FastAPI(title="RAG API with Portkey Gateway", lifespan=lifespan)


class QueryRequest(BaseModel):
    question: str


class Source(BaseModel):
    source: str
    chunk: Optional[int] = None
    score: float


class QueryResponse(BaseModel):
    answer: str
    plan: str
    context: str
    sources: list[Source]


class IngestResponse(BaseModel):
    filename: str
    chunks: int


@api.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="question khali hai")
    try:
        result = rag_graph.invoke({"question": question})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return QueryResponse(
        answer=result["answer"],
        plan=result["plan"],
        context=result["context"],
        sources=result["sources"],
    )


@api.post("/ingest", response_model=IngestResponse)
def ingest(file: UploadFile = File(...)):
    name = file.filename or "upload"
    suffix = Path(name).suffix.lower()
    if suffix not in (".pdf", ".txt", ".md"):
        raise HTTPException(status_code=400, detail="Sirf .pdf, .txt ya .md allowed hai")

    data = file.file.read()
    try:
        if suffix == ".pdf":
            reader = PdfReader(io.BytesIO(data))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        else:
            text = data.decode("utf-8", errors="ignore")
        n = ingest_text(text, name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if n == 0:
        raise HTTPException(status_code=400, detail="File se koi text nahi mila")
    return IngestResponse(filename=name, chunks=n)


@api.get("/health")
def health():
    return {"status": "ok"}