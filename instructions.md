# Antigravity Agent Directives: Phase 4 - Enterprise Documentation Gateway

## 0. The Architectural Objective
The backend Data-as-a-Service (DaaS) pipeline is fully operational on an isolated edge node. You are tasked with engineering the B2B client conversion interface. This will be a strictly static Next.js frontend functioning as a technical documentation gateway. It must translate global traffic into Merchant of Record (MoR) checkout conversions.

## 1. The Technology Stack Constraints
**Thesis:** Modern frontends bloat with unnecessary client-side state and server-side rendering logic.
**Anti-Thesis:** Complex frontends increase deployment costs and latency.
**Synthesis:** Enforce absolute minimalism.
* **Framework:** Next.js (App Router configured strictly for `output: 'export'` static HTML generation).
* **Language:** TypeScript (Strict typing enforced).
* **Styling:** Tailwind CSS. The aesthetic must be brutalist, terminal-inspired, and highly technical.
* **State:** Zero global state management (No Redux, no Zustand).

## 2. The Required Page Topology
You will engineer a single, high-fidelity landing page (`app/page.tsx`) partitioned into three distinct conversion nodes:

1. **The Value Proposition (Hero):**
   * Communicate the arbitrage: "Institutional-Grade AI Developer Velocity API."
   * Highlight the core metrics: Real-time tracking of top 50 AI repositories, contributor churn, and commit velocity.

2. **The Integration Ledger (Documentation):**
   * Provide brutalist, copy-pasteable code blocks for B2B developers.
   * Display a `curl` request targeting `https://api.[yourdomain].com/api/v1/ai-developer-velocity/pytorch/pytorch` demonstrating the required `X-API-Key` header.
   * Display a standard JSON response payload mapped from the `repository_metrics` PostgreSQL schema.

3. **The Financial Gateway (Conversion):**
   * A direct Call-to-Action (CTA) button labeled "Provision API Access."
   * This button must contain a hardcoded `href` to the Lemon Squeezy checkout link. 
   * **CRITICAL:** Do not build a custom checkout cart. The MoR handles all financial compliance off-site.

## 3. The Execution Protocol
1. Initialize the Next.js matrix utilizing standard deployment templates.
2. Ensure the `next.config.js` explicitly defines `output: "export"` to guarantee the build produces a purely static `/out` directory.
3. You are strictly forbidden from writing API routes (`app/api/...`) or attempting to connect to the PostgreSQL database from this codebase. All state is managed by the K3s edge node.

Execute the generation of the UI components and await structural verification.