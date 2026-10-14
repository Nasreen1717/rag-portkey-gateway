# RAG API with Portkey Gateway

A Retrieval-Augmented Generation (RAG) API built with **FastAPI**, **LangGraph**, **Qdrant**, **FlashRank** and **Groq**, with all LLM calls routed through the **Portkey AI Gateway** for retries, fallbacks, caching, timeouts, load balancing and observability.

You upload documents (PDF, TXT, MD), then ask questions. The API finds the most relevant chunks, reranks them, and generates an answer using only that context.

## What this app does

1. **Ingest:** upload a file, it is split into chunks (800 chars, 150 overlap), embedded and stored in a local Qdrant database.
2. **Plan:** an LLM turns the user question into a short search query.
3. **Retrieve:** Qdrant returns the top 15 similar chunks (vector search).
4. **Rerank:** FlashRank reorders them and keeps the top 5 most relevant.
5. **Answer:** an LLM answers using only those 5 chunks. The response also lists the sources (file name, chunk number, score).

The LangGraph agent runs these steps as a graph: `Planner -> Retriever -> Responder`.

## Why Portkey?

Every LLM call goes through the Portkey gateway instead of calling Groq directly. This gives:

- Automatic retries on 429/500/502/503/504
- Request timeouts
- Fallback (primary `gpt-oss-20b`, backup `gpt-oss-120b`)
- Simple caching (same question returns instantly)
- Load balancing between models
- Logs, metadata and observability in the Portkey dashboard

The production setup (`prod-config`) combines retry, timeout, fallback and cache in one saved config.

## Tech stack

| Part | Tool |
|------|------|
| API | FastAPI + Uvicorn |
| Agent | LangGraph + LangChain |
| LLM gateway | Portkey |
| LLM provider | Groq (`openai/gpt-oss-20b`, `openai/gpt-oss-120b`) |
| Vector DB | Qdrant (local, file based) |
| Embeddings | fastembed (`BAAI/bge-small-en-v1.5`, 384 dims) |
| Reranker | FlashRank (`ms-marco-TinyBERT-L-2-v2`) |
| PDF parsing | pypdf |

## Project structure

```
rag-portkey-gateway/
  main.py                  FastAPI app (/query, /ingest, /health)
  feature11_langgraph.py   LangGraph agent (Planner, Retriever, Responder)
  retriever.py             Qdrant search and FlashRank reranking
  ingest.py                File to chunks to embeddings to Qdrant
  qdrant_setup.py          Creates the collection with 5 sample docs (resets data)
  feature1_basic.py ...    Step by step Portkey feature demos (retries, cache, etc.)
  feature_prod.py          Full production config demo
  list_models.py           Lists available Groq models
  PROGRESS.md              Build log
  .env                     Your keys (not committed)
```

## Setup

### 1. Requirements

- Python 3.10 or newer (built and tested on 3.14.1)
- A [Groq](https://console.groq.com) API key
- A [Portkey](https://portkey.ai) account and API key

### 2. Clone and create a virtual environment

```powershell
git clone https://github.com/Nasreen1717/rag-portkey-gateway.git
cd rag-portkey-gateway
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks the script:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

On macOS/Linux use `source venv/bin/activate`.

### 3. Install packages

```powershell
pip install fastapi uvicorn portkey-ai langchain langchain-openai langgraph qdrant-client fastembed flashrank python-dotenv pypdf python-multipart
```

### 4. Configure Portkey

1. In the Portkey dashboard, open **Model Catalog** and add Groq as a provider with the slug `my-groq`. Models are then used as `@my-groq/openai/gpt-oss-20b`.
2. Create a saved config named `prod-config` (Configs > Create) with:
   - Fallback: `@my-groq/openai/gpt-oss-20b` then `@my-groq/openai/gpt-oss-120b`
   - Simple cache, max age 3600 seconds
   - Retry: 3 attempts on 429, 500, 502, 503, 504
   - Request timeout: 20000 ms
3. Copy the config ID (it looks like `pc-...`).

Portkey workspaces can block inline configs (`inline_config_blocked` error), which is why configs are saved in the dashboard and referenced by ID.

### 5. Create the `.env` file

```
GROQ_API_KEY=your_groq_key
PORTKEY_API_KEY=your_portkey_key
PORTKEY_PROD_CONFIG=pc-xxxxxx
```

Never commit this file.

### 6. Create the Qdrant collection (first time only)

```powershell
python qdrant_setup.py
```

This creates the `docs` collection with 5 sample documents. **Warning:** it deletes and recreates the collection, so do not run it again unless you want to wipe all ingested data.

## Run the API

```powershell
uvicorn main:api --port 8000
```

Open the interactive docs at `http://127.0.0.1:8000/docs`.

Notes:

- Do not use `--reload`. Local Qdrant only allows one process at a time.
- While the server is running, the local Qdrant folder is locked. Stop the server (Ctrl+C) before running `qdrant_setup.py`, `retriever.py` or `ingest.py`.

## API endpoints

### `POST /ingest`

Upload a `.pdf`, `.txt` or `.md` file (multipart form, field name `file`).

```powershell
curl -X POST http://127.0.0.1:8000/ingest -F "file=@data/attention.pdf"
```

Response:

```json
{ "filename": "attention.pdf", "chunks": 61 }
```

Ingesting the same file again overwrites its chunks (no duplicates).

You can also ingest from the command line (server must be stopped):

```powershell
python ingest.py data\attention.pdf
```

### `POST /query`

```powershell
curl -X POST http://127.0.0.1:8000/query -H "Content-Type: application/json" -d "{\"question\": \"What is multi-head attention?\"}"
```

Response:

```json
{
  "answer": "Multi-head attention runs several attention functions in parallel ...",
  "plan": "multi-head attention definition",
  "context": "the top 5 reranked chunks ...",
  "sources": [
    { "source": "attention.pdf", "chunk": 18, "score": 0.9421 }
  ]
}
```

- `answer`: the final answer
- `plan`: the search query the planner created
- `context`: the chunks the answer was based on
- `sources`: file name, chunk number and rerank score of the top 5 chunks (original sample docs show `sample` as the source)

### `GET /health`

Returns `{"status": "ok"}`.

## Try the Portkey feature demos

Each script shows one gateway feature. Run them from inside the project folder with the venv active:

| Script | Feature |
|--------|---------|
| `feature1_basic.py` | Basic routing through Portkey |
| `feature2_metadata.py` | Metadata and observability |
| `feature3_retries.py` | Automatic retries |
| `feature4_timeout.py` | Request timeouts |
| `feature5_fallback.py` | Fallbacks |
| `feature6_cache.py` | Caching |
| `feature7_loadbalance.py` | Load balancing |
| `feature9_langchain.py` | LangChain drop-in |
| `feature10_streaming.py` | Streaming responses |
| `feature_prod.py` | Retry + timeout + fallback + cache combined |

Some demos need their own config IDs in `.env` (for example `PORTKEY_RETRY_CONFIG`, `PORTKEY_CACHE_CONFIG`). Check the top of each script.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: No module named 'portkey_ai'` | Activate the venv first |
| `can't open file ... No such file or directory` | You are in the wrong folder, `cd rag-portkey-gateway` |
| `inline_config_blocked` | Use a saved config ID from the dashboard |
| Qdrant lock error | Another process (uvicorn) is using `qdrant_data`, stop it |
| Empty answer from the LLM | `gpt-oss` is a reasoning model, keep `max_tokens` at 1500 or more |
| `llama-3.3-70b-versatile` not found | Not available on this account, use `openai/gpt-oss-20b` |
| Logs missing in Portkey | Check the usage limit banner in the dashboard |

## Known limitations

- PDF text extraction can be messy for formulas and multi-column layouts. Answers are usually still correct.
- Simple cache only hits on the exact same question text.
- Local Qdrant supports one process only. For multiple workers, use a Qdrant server.
- No authentication on the endpoints, so do not expose it publicly as is.

## License

Add a license of your choice (for example MIT).
