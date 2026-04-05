# Agent Execution Directives: Static DaaS Documentation Gateway

## 0. The Prime Directive
You are engineering a B2B enterprise documentation gateway, not a consumer web application. Your sole objective is to mathematically translate inbound technical traffic into Merchant of Record (MoR) conversions. You will execute this with absolute dependency minimalism, enforcing a brutalist, zero-state static architecture. 

## I. Zero-State & Static Exclusivity
**Thesis:** Modern React frameworks encourage dynamic server rendering and complex client-side state management.
**Anti-Thesis:** Deploying a dynamic Node.js server to host a landing page violates the zero-compute infrastructure mandate and introduces unnecessary latency to global clients.
**Synthesis:** Enforce strict Static Site Generation (SSG).

1. **The Export Mandate:** The `next.config.js` must explicitly contain `output: 'export'`. You are strictly forbidden from utilizing Next.js API routes (`app/api/...`), middleware, or server actions.
2. **State Eradication:** You will not install or utilize Redux, Zustand, Context API, or any global state managers. The page possesses no dynamic state. It is a static ledger of documentation and a routing gateway to the MoR.
3. **Hydration Minimization:** Do not use `useEffect` or `useState` unless absolutely mathematically necessary for a minor UI toggle (e.g., copying a `curl` snippet to the clipboard). 

## II. The Brutalist Aesthetic (UI/UX)
**Thesis:** Agents default to consumer-friendly, soft aesthetics with rounded corners and heavy animation libraries.
**Anti-Thesis:** Quantitative analysts and senior engineers distrust "fluffy" consumer marketing. It signals a lack of technical rigor.
**Synthesis:** Enforce a brutalist, terminal-inspired, data-dense aesthetic using exclusively Tailwind CSS.

1. **Typography:** Utilize strict monospaced or highly geometric sans-serif fonts (e.g., Inter, JetBrains Mono, Roboto Mono). 
2. **Color Palette:** High-contrast, mathematically sterile. Default to a dark-mode terminal aesthetic (slate/zinc/black backgrounds) with a single, highly visible accent color strictly reserved for the conversion CTA and code syntax highlighting.
3. **No UI Bloatware:** You are strictly forbidden from installing heavy component libraries (Material UI, Chakra UI, Ant Design) or animation libraries (Framer Motion). Construct all components utilizing native HTML elements and utility classes.

## III. The Financial Conversion Perimeter
**Thesis:** Standard e-commerce templates assume a localized shopping cart and native payment processor integration.
**Anti-Thesis:** Building a checkout flow on a static site requires complex, insecure client-side logic that breaks MoR compliance.
**Synthesis:** Delegate all financial cryptography and compliance entirely to the off-site MoR portal.

1. **The Air-Gapped Checkout:** The "Provision API Access" Call-to-Action (CTA) must be a standard HTML anchor tag (`<a>`) containing the hardcoded URL to the Lemon Squeezy hosted checkout page. 
2. **No SDKs:** You will not install the `@lemonsqueezy/lemonsqueezy.js` library or any Stripe client-side SDKs. The frontend does not process transactions; it merely routes traffic.

## IV. B2B Documentation Rigor
1. **Code Snippet Fidelity:** The `curl` integration examples must be technically flawless. They must explicitly demonstrate the `X-API-Key` header injection and the precise structure of the PostgreSQL JSON response payload.
2. **The "Copy-to-Clipboard" Mandate:** Every code block must feature a zero-dependency, native JavaScript `navigator.clipboard.writeText()` implementation. Frictionless integration is the primary driver of B2B conversions.