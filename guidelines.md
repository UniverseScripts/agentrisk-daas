# Agent Execution Directives: Operational & Legal Compliance

## 0. The Prime Directive
You are an autonomous execution agent operating within a strictly constrained, zero-budget edge environment. Your outputs must mathematically align with resource asceticism, enterprise-grade security, and strict legal compliance. Deviation from these parameters will result in immediate operational failure and potential legal liability. 

## I. Legal & Terms of Service (ToS) Perimeter
**Thesis:** Aggressive web scraping extracts maximum data but triggers automated legal and technical countermeasures.
**Anti-Thesis:** Strictly abiding by rate limits ensures compliance but risks failing to aggregate enough data to provide B2B value.
**Synthesis:** Utilize official, authenticated GraphQL endpoints to extract aggregated metadata while remaining mathematically invisible to abuse-detection algorithms.

1. **Zero-PII Mandate:** You are strictly forbidden from scraping, storing, or transmitting Personally Identifiable Information (PII), including developer email addresses, real names, or location data. You will only query aggregated repository metrics (commits, issues, forks, stars). Selling PII violates GDPR and CCPA and introduces catastrophic legal liability.
2. **GraphQL Endpoint Exclusivity:** Do not write HTML parsers or use libraries like `BeautifulSoup` or `Selenium` against GitHub. You must exclusively use the official GitHub GraphQL API. 
3. **Rate Limit Adherence:** The GitHub Actions ingestion script must programmatically check the `rateLimit` object in the GraphQL response. If the remaining quota drops below 10%, the script must gracefully terminate and log a warning, rather than spamming the endpoint and triggering a shadowban.

## II. Silicon & Compute Conservation
**Thesis:** Modern Python development relies on heavy, robust data-processing libraries.
**Anti-Thesis:** Consumer edge silicon will thermally throttle and crash if heavy libraries are invoked during concurrent K3s operations.
**Synthesis:** Enforce absolute dependency minimalism. 

1. **Dependency Eradication:** You are strictly forbidden from importing `pandas`, `numpy`, `scipy`, `torch`, or any heavy data science library. The JSON parsing and normalizations must be executed using Python's standard library (`json`, `datetime`) and lightweight asynchronous request libraries (`httpx`).
2. **Asynchronous Exclusivity:** All I/O operations (API requests, PostgreSQL queries) must be asynchronous. You will not write blocking `requests.get()` or synchronous `psycopg2` calls that halt the ASGI event loop.

## III. Cryptographic & Ledger Security
**Thesis:** Hardcoded configurations allow for rapid prototyping and seamless agent execution.
**Anti-Thesis:** Hardcoded secrets pushed to a global Git ledger result in immediate credential harvesting by automated botnets.
**Synthesis:** Air-gap all cryptographic keys and database URIs from the application logic.

1. **The Air-Gapped Configuration:** You will never hardcode a PostgreSQL URI, a GitHub Personal Access Token (PAT), or a Merchant of Record (MoR) webhook secret. 
2. **Environment Injection:** All credentials must be extracted exclusively via `os.getenv()`. You will assume these variables are securely injected into the K3s containers via Kubernetes `Secret` objects or defined in the GitHub Actions repository secrets.
3. **Ledger Immutability:** When deducting tokens from the `api_key` table, you must execute the deduction atomically (e.g., `UPDATE api_key SET token_balance = token_balance - 1 WHERE id = X AND token_balance > 0`). Do not read the balance into Python memory, subtract, and write back, as this introduces race conditions under concurrent load.

## IV. Architectural Idempotency
1. **Idempotent Database Ingestion:** The GitHub Actions cron job will inevitably fail or retry. All `INSERT` operations into the PostgreSQL `repository_metrics` table must include `ON CONFLICT DO NOTHING` or `ON CONFLICT DO UPDATE` clauses to prevent duplicate primary keys and corrupted time-series visualizations in Grafana.
2. **Read-Only Infrastructure:** You are authorized to write and modify Python application logic. You are strictly forbidden from modifying the existing `grafana.yaml`, `prometheus.yaml`, or core K3s orchestration manifests unless explicitly authorized by a human operator.