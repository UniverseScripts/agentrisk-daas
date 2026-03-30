# Antigravity Agent Directives: Project DaaS (AI Developer Velocity API)

## 0. The Architectural Objective
You are engineering a strictly decoupled Data-as-a-Service (DaaS) pipeline. This architecture operates on consumer edge silicon orchestrated via K3s. You will not build a monolithic application. You will engineer three mathematically isolated components:
1. An asynchronous Python ingestion engine (executed ephemerally via GitHub Actions).
2. A normalized PostgreSQL data ledger.
3. A stateless FastAPI routing matrix protected by Redis atomic rate limiters and authenticated via static `X-API-Key` headers.

## 1. The PostgreSQL Ledger (State Matrix)
**Thesis:** Standard agents create unindexed, flattened tables.
**Anti-Thesis:** Unindexed querying of time-series alternative data will stall the ASGI event loop during concurrent B2B API requests.
**Synthesis:** Enforce strict normalization and B-Tree indexing on temporal and repository identifiers.

Execute the following database schemas utilizing SQLAlchemy 2.0 (`asyncpg`):
1. Create a `repository_metrics` table. Columns: `id` (UUID, Primary Key), `repo_name` (String, Indexed), `timestamp` (DateTime, Indexed), `commit_velocity_24h` (Integer), `open_issues_delta` (Integer), `fork_velocity_24h` (Integer), `contributor_churn` (Float).
2. Create an `api_key` table. Columns: `id` (String, PK), `valid_api_keys` (String, Unique, Indexed), `token_balance` (Integer), `is_active` (Boolean).

## 2. The Ingestion Engine (GitHub Actions Scraper)
**Thesis:** Standard agents build continuous `while True:` polling loops utilizing heavy web scraping frameworks like Selenium.
**Anti-Thesis:** Persistent polling will consume the local CPU baseline, triggering thermal throttling and bankrupting the compute limits.
**Synthesis:** Engineer an ephemeral, stateless Python script designed to run exclusively via GitHub Actions cron schedules.

Execute the ingestion logic:
1. Engineer `scraper/github_velocity.py`.
2. Utilize the native GitHub GraphQL API (to minimize payload overhead) via the `httpx` asynchronous library.
3. Target the top 50 AI/ML repositories (e.g., `pytorch/pytorch`, `huggingface/transformers`, `langchain-ai/langchain`).
4. Calculate the 24-hour delta for commits, forks, and closed issues.
5. The script must establish an asynchronous connection to the PostgreSQL remote tunnel, execute a bulk `INSERT` operation, and immediately terminate to release compute resources.

## 3. The Stateless Routing Matrix (FastAPI)
**Thesis:** Standard agents intertwine authentication, database querying, and rate-limiting within the endpoint function.
**Anti-Thesis:** Monolithic endpoints violate single-responsibility principles and create severe bottleneck vulnerabilities under Locust load testing.
**Synthesis:** Engineer strict middleware perimeters. The endpoint must only execute when the request is mathematically proven to be authorized and within quota constraints.

Execute the routing logic:
1. Define the primary endpoint: `GET /api/v1/ai-developer-velocity/{repo_name}`.
2. **The Authentication Perimeter:** Inject a FastAPI `Depends` function (`verify_api_key`) that strictly scans for the `X-API-Key` HTTP header. It must query the `api_key` table via `asyncpg`. If `token_balance <= 0` or the key is invalid, terminate the socket immediately with `HTTP 401` or `HTTP 402`.
3. **The Redis Rate Limiter:** Engineer an asynchronous Lua script injected into a Redis client within a FastAPI middleware layer. It must execute a sliding-window token bucket algorithm based on the client's API key. Reject overflow traffic with `HTTP 429`.
4. **The Ledger Deduction:** Upon successful retrieval of the PostgreSQL data, mathematically deduct 1 token from the `api_key.token_balance` and execute `db.commit()`.
5. Return the payload strictly serialized via Pydantic models.

## 4. The Execution Protocol
Do not hallucinate external dependencies. Do not import Heavy ML libraries (e.g., `torch`, `transformers`). This is a structured data pipeline, not an inference node. 

Iteratively execute the code generation for each section. Stop and request human verification before mutating the K3s deployment manifests.