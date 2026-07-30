import Link from "next/link";

export default function PoliciesPage() {
  return (
    <main className="min-h-screen bg-trueblack text-sterilewhite flex flex-col font-sans uppercase tracking-widest text-sm w-full">
      
      {/* NAVIGATION HEADER */}
      <div className="w-full border-b border-zinc-900 py-6 px-6 sm:px-10 lg:px-16 xl:px-24">
        <div className="max-w-[1600px] mx-auto flex items-center justify-between font-mono text-xs text-zinc-400">
          <Link href="/" className="hover:text-crtgreen transition-colors flex items-center gap-2 font-bold">
            <span>&lt;</span> RETURN TO TERMINAL
          </Link>
          <span className="text-crtgreen font-bold">[DATA GOVERNANCE &amp; PRIVACY POLICY]</span>
        </div>
      </div>

      {/* HERO / THESIS */}
      <section className="w-full border-b border-zinc-900 py-12 lg:py-16 px-6 sm:px-10 lg:px-16 xl:px-24">
        <div className="max-w-[1600px] mx-auto">
          <p className="text-crtgreen text-xs font-mono mb-2">[GOVERNANCE MANUAL // DATA TRANSPARENCY]</p>
          <h1 className="text-3xl lg:text-4xl font-black mb-4">PRIVACY, SECURITY &amp; DATA USAGE GOVERNANCE</h1>
          <p className="text-zinc-400 max-w-3xl leading-relaxed mt-4 lowercase normal-case tracking-normal text-base font-sans">
            Institutional standards governing public registry telemetry collection, zero-synthetic-data guarantees, data retention windows, and subscriber confidentiality.
          </p>
        </div>
      </section>

      {/* SECTION 1: DATA SOURCING & INTEGRITY */}
      <section className="w-full border-b border-zinc-900 py-12 px-6 sm:px-10 lg:px-16 xl:px-24">
        <div className="max-w-[1600px] mx-auto">
          <h2 className="text-xl font-bold text-crtgreen mb-6 font-mono">1. PUBLIC REGISTRY DATA SOURCING &amp; ZERO-SYNTHETIC GUARANTEE</h2>
          <div className="space-y-4 text-zinc-300 text-sm lowercase normal-case tracking-normal font-sans leading-relaxed">
            <p>
              AgentRisk DaaS ingests telemetry exclusively from authoritative, public registry endpoints and version control metadata interfaces across the AI software supply chain, including the npm Registry REST API, PyPI JSON API, and GitHub GraphQL API v4.
            </p>
            <p>
              <strong className="text-sterilewhite uppercase font-mono">Zero-Synthetic-Data Commitment:</strong> We do not generate, synthesize, or estimate zero-valued metric placeholders to obscure cache misses or unresolvable repositories. If a package exists in a registry but lacks a linked public version control repository, the API returns an explicit, honest <code className="text-crtgreen font-mono bg-zinc-950 px-2 py-1 border border-zinc-800">HTTP 404</code> response detailing untrackability.
            </p>
          </div>
        </div>
      </section>

      {/* SECTION 2: SUBSCRIBER PRIVACY & CRYPTOGRAPHIC SECURITY */}
      <section className="w-full border-b border-zinc-900 py-12 px-6 sm:px-10 lg:px-16 xl:px-24 bg-zinc-950/40">
        <div className="max-w-[1600px] mx-auto">
          <h2 className="text-xl font-bold text-zinc-400 mb-6 font-mono">2. SUBSCRIBER CONFIDENTIALITY &amp; KEY STORAGE</h2>
          <div className="space-y-4 text-zinc-300 text-sm lowercase normal-case tracking-normal font-sans leading-relaxed">
            <p>
              Subscriber API keys are generated cryptographically upon subscription verification and stored strictly in one-way <strong className="text-sterilewhite font-mono">SHA-256 hashed digest</strong> format within PostgreSQL. Plaintext API keys are dispatched once via transactional email and cannot be recovered or retrieved by AgentRisk personnel.
            </p>
            <p>
              We do not sell, license, or expose subscriber query logs or package lookup histories to third parties. Query logs are utilized exclusively for rate-limiting enforcement and internal infrastructure performance tuning.
            </p>
          </div>
        </div>
      </section>

      {/* SECTION 3: DATA RETENTION & TIME-SERIES SNAPSHOTS */}
      <section className="w-full border-b border-zinc-900 py-12 px-6 sm:px-10 lg:px-16 xl:px-24">
        <div className="max-w-[1600px] mx-auto">
          <h2 className="text-xl font-bold text-crtgreen mb-6 font-mono">3. TELEMETRY RETENTION &amp; TIME-SERIES SNAPSHOTS</h2>
          <div className="space-y-4 text-zinc-300 text-sm lowercase normal-case tracking-normal font-sans leading-relaxed">
            <p>
              Historical telemetry snapshots (<code className="text-crtgreen font-mono bg-zinc-950 px-2 py-1">PackageRiskMetric</code>) are retained in Neon PostgreSQL for a maximum window of 30 days per package to support time-series velocity and anomalous activity calculations.
            </p>
            <p>
              Stale telemetry records (older than <code className="text-crtgreen font-mono bg-zinc-950 px-2 py-1">CACHE_TTL_HOURS = 6</code>) trigger background revalidation tasks upon consumer request to ensure fresh risk data without blocking main thread execution.
            </p>
          </div>
        </div>
      </section>

      {/* SECTION 4: GOVERNANCE SUPPORT CONTACT */}
      <section className="w-full py-12 px-6 sm:px-10 lg:px-16 xl:px-24 font-mono text-xs">
        <div className="max-w-[1600px] mx-auto">
          <h2 className="text-xl font-bold text-zinc-400 mb-4">4. GOVERNANCE ENQUIRIES &amp; DPO CONTACT</h2>
          <p className="text-zinc-400 lowercase normal-case tracking-normal font-sans leading-relaxed mb-4 text-sm">
            For data governance inquiries, vulnerability disclosures, or privacy requests, please contact our engineering team directly:
          </p>
          <a 
            href="mailto:asteriostech@gmail.com" 
            className="inline-block border border-crtgreen bg-zinc-950 text-crtgreen px-6 py-4 font-bold hover:bg-crtgreen hover:text-black transition-colors lowercase tracking-normal text-sm"
          >
            asteriostech@gmail.com
          </a>
        </div>
      </section>

    </main>
  );
}
