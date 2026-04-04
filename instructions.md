# Antigravity Agent Directives: Phase 3 - Autonomous Financial Perimeter

## 0. The Architectural Objective
The Data-as-a-Service (DaaS) ingestion and routing pipelines are operational. You must now engineer the financial monetization bridge. You will implement a highly secure webhook receiver that mathematically links the Lemon Squeezy Merchant of Record (MoR) to the PostgreSQL `api_key` ledger, and configure the Kubernetes ingress routing to expose this perimeter to the global internet.

## 1. The Cryptographic Webhook Receiver (Application Layer)
**Thesis:** Standard agents blindly trust incoming HTTP payloads, leading to API key generation forgery by malicious actors.
**Anti-Thesis:** Relying purely on network-layer security (IP whitelisting) is insufficient for financial transactions on edge nodes.
**Synthesis:** Enforce strict HMAC SHA-256 signature verification on the incoming payload before allocating any database resources.

You must mutate `api/main.py` to include the following endpoint: `POST /webhooks/lemon-squeezy`.
Execute the following strict logic:
1. **Air-gapped Secret:** Extract `LEMON_SQUEEZY_WEBHOOK_SECRET` via `os.getenv()`. Fail violently if missing.
2. **Signature Verification:** Extract the `X-Signature` HTTP header. Compute the HMAC SHA-256 digest of the raw request body using the air-gapped secret. You MUST use `hmac.compare_digest()` to prevent timing attacks. If the signature is forged, immediately raise `HTTP 401`.
3. **Event Parsing:** Parse the JSON payload. Ensure the `meta.event_name` equals `order_created`.
4. **Cryptographic Key Generation:** Generate a raw API key string (e.g., `daas_live_<uuid4>`). You MUST mathematically hash this raw string using SHA-256 before interacting with the database.
5. **Ledger Injection:** Asynchronously insert a new `APIKey` record into the database. Set `valid_api_keys` to the hashed string, `token_balance` to `10000`, and `is_active` to `True`. 
6. **Output Stub:** Print or log the raw API key and the client's email (extracted from `data.attributes.user_email`). Do not build a complex SMTP integration yet; leave a clear `# TODO: Async dispatch raw_api_key to client_email` marker.

## 2. The Kubernetes Ingress Routing (Infrastructure Layer)
**Thesis:** Hardcoding ports and relying on default NodePorts exposes the edge cluster to direct, unmitigated DDoS vectors.
**Anti-Thesis:** Complex service meshes (Istio) will consume the remaining memory baseline of the consumer-grade hardware.
**Synthesis:** Engineer a strict, lightweight Traefik IngressRoute utilizing your existing Cloudflare Tunnel perimeter.

You must create a new file: `k8s/base/routing/daas-ingress.yaml`.
Execute the following declarative infrastructure:
1. Define a standard Kubernetes `Ingress` resource targeting the `traefik` ingress class.
2. Map the host (e.g., `api.yourdomain.com`) strictly to the backend `fastapi-service` on port `8000`.
3. You must explicitly define two paths:
    * Path: `/api/v1/ai-developer-velocity` (Prefix match)
    * Path: `/webhooks/lemon-squeezy` (Exact match)

## 3. The Execution Protocol
* **Do not** modify the existing Lua rate limiter or the `get_developer_velocity` endpoint.
* **Do not** alter `db/models.py`. The `APIKey` schema is already absolute.
* Ensure all database operations in the webhook remain fully asynchronous to prevent blocking the ASGI event loop during a surge of MoR transactions.

Iteratively draft the `api/main.py` mutation and present it for human verification before drafting the Kubernetes YAML.