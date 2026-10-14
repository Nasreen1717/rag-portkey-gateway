# Project: RAG API with Portkey Gateway (FastAPI + LangGraph + Qdrant + Groq)

**OS:** Windows | **Goal:** Learn concepts, build full pipeline step by step.
**Project folder:** `D:\code\LLM Gateway Explorer\rag-portkey-gateway` (venv, .env, .gitignore, PROGRESS.md, README.md, all .py files live here)
**GitHub:** https://github.com/Nasreen1717/rag-portkey-gateway

## Full Feature Checklist (from README)
- [x] Stage 1: Project folder + venv created
- [x] Stage 2: Packages installed (fastapi, uvicorn, portkey-ai, langchain, langchain-openai, langgraph, qdrant-client, flashrank, python-dotenv)
- [x] Stage 3: `.env` file with GROQ_API_KEY + PORTKEY_API_KEY (verified)
- [x] Stage 4: Qdrant setup (fastembed installed, `qdrant_setup.py` works, top result correct)
- [x] Feature 1: Basic routing through Portkey (`feature1_basic.py` works)
- [x] Feature 2: Metadata & observability (`feature2_metadata.py` works, user_001 visible in Logs)
- [x] Feature 3: Automatic retries (`feature3_retries.py` works with saved config)
- [x] Feature 4: Request timeouts (`feature4_timeout.py` works, config `pc-timeou-9d143b`, verified in Logs)
- [x] Feature 5: Fallbacks (`feature5_fallback.py` works, fallback verified in Logs)
- [x] Feature 6: Caching (`feature6_cache.py` works, config `pc-cache-2e9f8a`, Run 2 = cache Hit in 0.06s)
- [x] Feature 7: Load balancing (`feature7_loadbalance.py` works, 20b/120b split 50/50, verified in terminal)
- [x] Feature 8: Saved Config ID (`loadbalance-config` v2, weights 0.9/0.1 changed in dashboard with no code change, 5x 20b / 1x 120b verified)
- [x] Feature 9: LangChain drop-in (`feature9_langchain.py` works, ChatOpenAI pointed at Portkey)
- [x] Feature 10: Streaming responses (`feature10_streaming.py` works)
- [x] Full Production Config (retry+timeout+fallback+cache combined, `prod-config`, `feature_prod.py` works, Run 1 = 3.29s on 20b, Run 2 = 0.04s cache Hit)
- [x] LangGraph agent: Planner -> Retriever -> Responder (`feature11_langgraph.py`, real Qdrant retriever)
- [x] Qdrant search (top-15 chunks) via `retriever.py` (`retrieve()`)
- [x] FlashRank reranking (top-5) via `retriever.py` (`rerank()`, model ms-marco-TinyBERT-L-2-v2)
- [x] FastAPI endpoint: POST /query (`main.py`, app object is `api`)
- [x] Final: wired together, tested end-to-end in /docs (200 OK)
- [x] Upgrade 1: `ingest.py` (PDF/txt/md to chunks, embed, Qdrant). attention.pdf ingested = 61 chunks, collection total 66 points
- [x] Upgrade 2: POST /ingest endpoint in `main.py` (file upload). test.txt upload = 200 OK
- [x] Upgrade 3: POST /query tested on attention paper question ("What is multi-head attention?"), correct answer, context has real paper chunks
- [x] Upgrade 4: POST /query on "What is FlashRank?" = 200, answer came from test.txt line, so /ingest data is searchable (14 Oct)
- [x] Upgrade 5 (code): top-5 sources added. `retriever.py` has new `retrieve_docs()` + `rerank_docs()` (return text, source, chunk, score). `feature11_langgraph.py` State has `sources`. `main.py` has `Source` model and `QueryResponse.sources`. `python retriever.py` verified (source + chunk + score print correctly)
- [ ] Upgrade 5 (test): run POST /query in /docs and confirm `sources` list appears in the response
- [x] Upgrade 6: Project pushed to GitHub (`.env`, `venv/`, `qdrant_data/`, `data/`, `__pycache__/` excluded via .gitignore)
- [x] README.md written (English: what the app does, setup, run, endpoints, troubleshooting)

## Important Notes
- Python version is 3.14.1. fastembed and qdrant-client installed fine on it.
- VS Code terminal opens in `D:\code\LLM Gateway Explorer`. Run `cd rag-portkey-gateway` ONCE (if already inside, a second cd gives a harmless error).
- Always activate venv first: `.\venv\Scripts\Activate.ps1` (prompt must show `(venv)`). If it is missing, you get `ModuleNotFoundError: No module named 'portkey_ai'`.
- If scripts are blocked: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.
- Terminal must be inside `rag-portkey-gateway` folder before running any .py file. Running `python retriever.py` from the parent folder gives `can't open file ... No such file or directory`.
- VS Code interpreter (FIXED on 9 Oct): `Ctrl+Shift+P` > `Python: Select Interpreter` > `Enter interpreter path...` > paste `D:\code\LLM Gateway Explorer\rag-portkey-gateway\venv\Scripts\python.exe`. Status bar then shows `3.14.1 ('venv': venv)`. Do NOT pick "Create Environment" or the global Python.
- If terminal shows `fwd-i-search:` it is PowerShell history search (Ctrl+S pressed by mistake). Press Esc.
- Only type the command in the terminal. Lines like `Application startup complete.` are uvicorn OUTPUT, not commands (typing them gives CommandNotFoundException).
- Portkey blocks inline providers. Use Model Catalog slug: model string is `@my-groq/<model-id>`.
- Working Groq model: `openai/gpt-oss-20b` (also: `openai/gpt-oss-120b`, `qwen/qwen3.8-27b`).
  `llama-3.3-70b-versatile` is NOT available on this account anymore.
- To list current Groq models: `python list_models.py`.
- gpt-oss is a reasoning model, keep `max_tokens` at 300 or more.
- Portkey workspace has `block_inline_config` ON. Config dict in code gives `inline_config_blocked` error.
  Fix: create config in dashboard (Configs, Create), copy its `pc-...` ID, put it in `.env`,
  and use `config=os.getenv("...")` in Portkey client.
- Config IDs in `.env`:
  - `PORTKEY_RETRY_CONFIG` = `pc-llm-ga-ed0d4c` (Feature 3, auto-named "LLM Gateway Explorer")
  - `PORTKEY_TIMEOUT_CONFIG` = `pc-timeou-9d143b` (Feature 4)
  - `PORTKEY_FALLBACK_CONFIG` = `pc-fallba-7ccd0a` (Feature 5, config name `fallback-config`, now at v3)
  - `PORTKEY_CACHE_CONFIG` = `pc-cache-2e9f8a` (Feature 6, name `cache-config`, simple cache, max_age 3600 = 1 hour)
  - `PORTKEY_LB_CONFIG` = `pc-...` (Feature 7, name `loadbalance-config`, weights 0.5/0.5 between gpt-oss-20b and gpt-oss-120b) - paste the real ID from `.env`
  - `PORTKEY_PROD_CONFIG` = `pc-...` (Full Production Config, name `prod-config`: fallback 20b -> 120b, simple cache 3600s, retry 3 attempts on 429/500/502/503/504, request_timeout 20000 ms) - paste the real ID from `.env`
- Fallback config must keep primary = `@my-groq/openai/gpt-oss-20b`, backup = `@my-groq/openai/gpt-oss-120b`.
  If you edit it for testing (wrong model name), always restore it afterwards. (Verified restored on 7 Oct.)
- In fallback, cache, load balance and prod configs, no `model` is passed in code. Model comes from `override_params` in targets.
- With LangChain `ChatOpenAI`, `model="placeholder"` works because the config decides the real model (used in `feature11_langgraph.py`).
- Cache notes: simple cache hits only on exact same text. Cache is written after the response, so sending the same question again immediately can still be a Miss. Check Logs > Config Status for Cache Hit/Miss. A Hit returns the identical saved answer in under 0.1s.
- Load balance notes: split is random by weight, so 4/2 or 5/1 over 6 runs is normal. `response.model` shows which model answered.
- Add `client.close()` at end of Qdrant scripts to avoid the harmless msvcrt cleanup error on Python 3.14.
- Portkey dashboard shows "Upgrade to Pro" banner (usage limit warning). If logs stop appearing, check this.
- Logs tab: use "Logs" toggle (not "Traces"). `feature` and `env` metadata show inside the row detail.
- Run API from inside `rag-portkey-gateway`: `uvicorn main:api --port 8000` (no `--reload`, local Qdrant allows one process only). Test at `http://127.0.0.1:8000/docs`. `/` shows "Not Found", that is normal.
- Local Qdrant (`qdrant_data`) is locked by the running server. Stop uvicorn (Ctrl+C) before running `qdrant_setup.py`, `retriever.py` or `ingest.py`. While the server is running, upload files through POST /ingest instead.
- `qdrant_setup.py` DELETES and recreates the collection (wipes all ingested data). Do not run it again unless you want a reset. `ingest.py` only adds, it never deletes.
- `ingest.py` details: chunk size 800 chars, overlap 150, payload = `text`, `source` (file name), `chunk` (number). Chunk IDs are uuid5 of `source:chunk`, so ingesting the same file again overwrites, no duplicates. It reuses `client` and `model` from `retriever.py`.
- `retriever.py` now has 4 functions: `retrieve()` and `rerank()` (old, return plain text lists, kept for compatibility) and `retrieve_docs()` and `rerank_docs()` (new, return dicts with text, source, chunk, score). `feature11_langgraph.py` uses the new ones.
- The 5 original sample docs have no `source`/`chunk` in payload, so they show as source `sample` and chunk `None`. This is normal.
- Rerank score 0.0 on irrelevant chunks is normal (FlashRank scores them near zero).
- Extra packages installed on 13 Oct: `pypdf` (read PDF), `python-multipart` (FastAPI file upload).
- PDF text extraction is messy for formulas and columns (stray `\nn`, `W Qi`). This is normal and does not hurt answers much.
- `/ingest` accepts only .pdf, .txt, .md. Empty text gives 400.
- Sample data: `data\attention.pdf` (Attention Is All You Need, downloaded with `Invoke-WebRequest -Uri "https://arxiv.org/pdf/1706.03762" -OutFile "data\attention.pdf"`) and `data\test.txt` (3 short lines about Qdrant, Portkey, FlashRank).
- `max_tokens` in `feature11_langgraph.py` is 1500. At 400, gpt-oss-20b spent everything on reasoning and the answer came back empty.
- Collection `docs` now has about 67 points: 5 original sample docs + 61 attention.pdf chunks + 1 test.txt chunk. Reranking now has real data to work on.
- Git: the repo must live INSIDE `rag-portkey-gateway` (run `git init` after `cd rag-portkey-gateway`). On 14 Oct `git init` was run in the parent folder by mistake, fixed by deleting the parent `.git` folder and re-running `git init` inside the project folder.
- `.gitignore` content: `.env`, `venv/`, `qdrant_data/`, `data/`, `__pycache__/`. Always run `git status` before the first commit and confirm none of these appear.
- Never commit `.env`, `venv/`, `qdrant_data/`, `data/`.
- Never share screenshots showing `.env` keys (crop to the one line needed).

## Files in project
- `.env`, `.gitignore`, `PROGRESS.md`, `README.md`
- `feature1_basic.py` (working)
- `feature2_metadata.py` (working)
- `feature3_retries.py` (working)
- `feature4_timeout.py` (working)
- `feature5_fallback.py` (working)
- `feature6_cache.py` (working)
- `feature7_loadbalance.py` (working)
- `feature9_langchain.py` (working)
- `feature10_streaming.py` (working)
- `feature_prod.py` (working, uses PORTKEY_PROD_CONFIG, runs same question twice to show cache Hit)
- `feature11_langgraph.py` (updated 14 Oct: 3 nodes, State has `sources`, uses `retrieve_docs` + `rerank_docs`, PORTKEY_PROD_CONFIG via ChatOpenAI)
- `list_models.py` (helper to list Groq models)
- `qdrant_setup.py` (working, resets collection with 5 sample docs)
- `retriever.py` (updated 14 Oct: `retrieve()`, `rerank()`, `retrieve_docs()`, `rerank_docs()`, loads Qdrant, fastembed and FlashRank once at import)
- `ingest.py` (working: `ingest_text(text, source)`, CLI `python ingest.py data\file.pdf`)
- `main.py` (updated 14 Oct: FastAPI, POST /query with `sources`, POST /ingest and GET /health)
- `data/` folder (attention.pdf, test.txt)
- Note: there is no feature8 file, Feature 8 was a dashboard-only change.

## Progress Log
### Session 1 (29 Sep 2026)
- Explained project concept (LLM Gateway = proxy layer for reliability/observability).
- Fixed folder confusion: .env and .gitignore moved to project root.
- Stage 1 to 3 done. Fixed inline provider error with slug `my-groq`.
- Switched model to `openai/gpt-oss-20b`. Feature 1 complete.

### Session 2 (5 Oct 2026)
- Feature 2 done: metadata (_user, feature, env) visible in Portkey Logs.
- Stage 4 done: fastembed + Qdrant local storage, search returns correct top result.
- Feature 3 done: hit inline_config_blocked, fixed with saved dashboard config ID in `.env`.

### Session 3 (6 Oct 2026)
- Feature 4 done: timeout config created in dashboard, ID saved in `.env` as PORTKEY_TIMEOUT_CONFIG, verified in Logs (feature = timeout).
- Feature 5 done: fallback config (20b primary, 120b backup), ID saved as PORTKEY_FALLBACK_CONFIG.
- Fallback test done: primary set to `wrong-model-name`, it failed (0 tokens) and `gpt-oss-120b` answered. Both rows visible in Logs at the same timestamp.

### Session 4 (7 Oct 2026)
- Confirmed `fallback-config` is restored (primary 20b, backup 120b).
- Feature 6 done: `cache-config` (simple, 3600s) created, ID in `.env` as PORTKEY_CACHE_CONFIG. First run showed Miss (cache not written yet), second run showed identical answer in 0.06s = Hit.
- Hit `ModuleNotFoundError` because venv was not active. Fixed by activating venv.
- Feature 7 done: `loadbalance-config` (0.5/0.5), ID in `.env` as PORTKEY_LB_CONFIG. 6 runs split 3x 20b and 3x 120b.

### Session 5 (8 Oct 2026)
- Feature 8 done: `loadbalance-config` weights changed to 20b 0.9 / 120b 0.1 in dashboard (v2). Mistake fixed: weights must go in `weight`, not inside the model name. No code change, split verified (5x 20b, 1x 120b).
- Feature 9 done: `feature9_langchain.py`, ChatOpenAI with `base_url=PORTKEY_GATEWAY_URL` and `createHeaders(...)`, works, row visible in Logs.
- Feature 10 done: `feature10_streaming.py`, `llm.stream()` prints chunks as they arrive.

### Session 6 (9 Oct 2026)
- Full Production Config done: `prod-config` created in dashboard (fallback + cache + retry + timeout), ID in `.env` as PORTKEY_PROD_CONFIG. `feature_prod.py` result: Run 1 = 3.29s (gpt-oss-20b), Run 2 = 0.04s identical answer = cache Hit.
- Fixed VS Code `portkey_ai` wavy underline by selecting the venv interpreter (Problems now 0 errors, 0 warnings).
- LangGraph skeleton done: `feature11_langgraph.py` with State (question, plan, context, answer) and 3 nodes. Planner turned the question into a short search query, Retriever returned a hardcoded dummy context, Responder answered from it. Terminal printed all 3 nodes and FINAL ANSWER.

### Session 7 (10 Oct 2026)
- Added `retriever.py` (Qdrant top-15), replaced dummy Retriever in `feature11_langgraph.py`.
- Fixed empty Responder answer by raising max_tokens 400 to 1500.
- Added FlashRank rerank (top-5), then `main.py` FastAPI. POST /query returned 200 with answer, plan, context.
- Common mistake: terminal opened in `D:\code\LLM Gateway Explorer`, must `cd rag-portkey-gateway` first.

### Session 8 (13 Oct 2026)
- Chose to do the optional upgrades step by step: bigger doc set first, then /ingest endpoint.
- Step 2 done: created `ingest.py` (pypdf, 800 char chunks, 150 overlap, uuid5 IDs). Downloaded `data\attention.pdf` with Invoke-WebRequest. Result: "Ingested 61 chunks", "Total points in collection: 66".
- Step 3 done: `main.py` now has POST /ingest (UploadFile, .pdf/.txt/.md only). Installed `python-multipart`. Created `data\test.txt` from PowerShell here-string. Uploaded in /docs = 200 OK, filename test.txt.
- Mistake fixed: typed "Application startup complete." as a command (it is uvicorn output). Only `uvicorn main:api --port 8000` is the command.
- /query test on "What is multi-head attention?" = 200, correct answer, context had real paper chunks (MultiHead formula, h = 8, dk = dv = 64).

### Session 9 (14 Oct 2026)
- Upgrade 4 passed: /query on "What is FlashRank?" = 200, answer from test.txt ("lightweight reranking library... runs on CPU"), test.txt chunk is on top in context.
- Upgrade 5 code done: replaced `retriever.py`, `feature11_langgraph.py` and `main.py` with versions that return top-5 `sources` (source file, chunk number, score). `python retriever.py` verified: Portkey sample doc 0.9985 (`sample #None`), `test.txt #0` 0.1422, attention.pdf chunks 0.0.
- Mistake fixed: ran `python retriever.py` from the parent folder (`can't open file`). Fix: `cd rag-portkey-gateway` first.
- Upgrade 6 done: git set up and pushed to https://github.com/Nasreen1717/rag-portkey-gateway. Mistake fixed: first `git init` was in the parent folder and `__pycache__` was staged. Deleted the parent `.git`, added `__pycache__/` to `.gitignore`, re-ran `git init` inside `rag-portkey-gateway`. `git status` confirmed `.env`, `venv`, `qdrant_data`, `data` not staged.
- Wrote English `README.md` (overview, stack, setup, run, endpoints, troubleshooting).

## Next Session: Start Here
1. `cd rag-portkey-gateway` then `.\venv\Scripts\Activate.ps1`, then `uvicorn main:api --port 8000`.
2. In /docs run POST /query with `{"question": "What is multi-head attention?"}` and confirm the response has a `sources` list (attention.pdf, chunk, score). This finishes Upgrade 5.
3. Open the GitHub repo page and confirm `.env`, `venv`, `qdrant_data`, `data` are NOT there and README.md shows.
4. Optional: set `loadbalance-config` weights back to 0.5/0.5 (currently 0.9/0.1, v2).
5. Optional ideas: API key auth on endpoints, Dockerfile, Streamlit UI.

## How to Use This File
Next time, upload this file and say: "continue my Portkey RAG project from here."
