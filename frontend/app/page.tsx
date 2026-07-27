"use client";

import { useState } from "react";

export default function Page() {
  const [copied, setCopied] = useState(false);
  const [flash, setFlash] = useState(false);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(
      `curl -X GET "https://api.yourdomain.com/api/v1/analytics/package-risk/npm/react" \\\n-H "X-API-Key: YOUR_API_KEY"`
    );
    setCopied(true);
    setFlash(true);
    setTimeout(() => setFlash(false), 150); // Matches flash animation duration
  };

  return (
    <main className="min-h-screen bg-trueblack text-sterilewhite flex flex-col font-sans uppercase tracking-widest text-sm max-w-7xl mx-auto border-x border-zinc-900">
      
      {/* 1. THE HERO PROTOCOL */}
      <section className="border-b border-zinc-900 p-8 lg:p-16 animate-reveal">
        <pre className="text-crtgreen text-xs md:text-sm whitespace-pre border-none font-bold mb-8 font-mono">
{`    ___  ___  ___  ___       ___   _____  __ 
   /   |/   |/   |/   |     /   | /  _  \\/ / 
  / /| / /| / /| / /| |    / /| | | | / / /  
 / /_// /_// /_// /_| |   / /_| | | |/ / /___
/_/  /_/  /_/  /_/  |_|  /_/  |_| |___/_____/

STATUS: ACTIVE
NODE: EDGE INFRASTRUCTURE DAAS
ENCRYPTION: VERIFIED`}
        </pre>
        <h1 className="text-2xl md:text-4xl font-black mb-4">
          Maintainer & Dormancy Risk Signal DaaS
          <span className="blinking-cursor"></span>
        </h1>
        <p className="text-zinc-400 max-w-2xl leading-relaxed mt-6 lowercase normal-case tracking-normal text-base">
          Maintainer concentration, dormancy/reactivation signal, anomalous activity flag.
          Sourced directly from public registry metadata across the AI agent supply chain (MCP, npm, PyPI).
          No CVEs, no static code analysis. Just the raw risk matrix.
        </p>
      </section>

      {/* 2. THE INTEGRATION LEDGER */}
      <section className="border-b border-zinc-900 grid grid-cols-1 lg:grid-cols-2 animate-reveal delay-100">
        <div className="border-r border-zinc-900 p-8 lg:p-16 relative flex flex-col">
          <h2 className="text-xl font-bold mb-6 text-crtgreen border-b border-zinc-900 pb-2">REQUEST ARBITRAGE</h2>
          <div className={`relative group border border-zinc-900 bg-black p-4 flex-1 transition-none ${flash ? 'animate-flash' : ''}`}>
            <button 
              onClick={copyToClipboard}
              className="absolute top-0 right-0 bg-zinc-950 border-l border-b border-zinc-900 px-3 py-1 text-xs text-crtgreen uppercase hover:bg-crtgreen hover:text-black transition-none cursor-pointer font-bold font-mono"
            >
              {copied ? "[COPIED]" : "[COPY]"}
            </button>
            <pre className="text-zinc-300 text-xs overflow-x-auto mt-2 font-mono">
{`curl -X GET \\
"https://api.yourdomain.com/api/v1/analytics/package-risk/npm/react" \\
-H "X-API-Key: YOUR_API_KEY"`}
            </pre>
          </div>
        </div>

        <div className="p-8 lg:p-16 flex flex-col bg-zinc-950/50">
          <h2 className="text-xl font-bold mb-6 text-zinc-500 border-b border-zinc-900 pb-2">RESPONSE PAYLOAD</h2>
          <pre className="border border-zinc-900 bg-black p-4 text-xs overflow-x-auto text-zinc-400 font-mono flex-1">
{`{
  "package_name": "npm/react",
  "timestamp": "2026-07-22T00:00:00Z",
  "maintainer_concentration_index": 10.0,
  "dormancy_reactivation_index": "insufficient data",
  "anomalous_spike_index": 8.0,
  "maintainer_count": 1,
  "single_maintainer_flag": true,
  "days_since_last_publish": 2,
  "publish_cadence_variance": null,
  "fork_spike_ratio": 3.5
}`}
          </pre>
        </div>
      </section>

      {/* 3. THE FINANCIAL GATEWAY */}
      <section className="p-8 lg:p-16 animate-reveal delay-200 bg-black">
        <h2 className="text-xl font-bold text-zinc-500 mb-8 border-b border-zinc-900 pb-2">SECURE PERIMETER ACCESS</h2>
        <div className="flex flex-col lg:flex-row items-stretch lg:items-center gap-6">
          <div className="border border-zinc-900 p-6 flex-1 bg-zinc-950">
            <p className="text-zinc-500 text-xs mb-2 font-mono tracking-widest">RECURRING SUBSCRIPTION</p>
            <p className="text-3xl font-black text-sterilewhite font-mono tracking-tighter">$15.00 / MO</p>
          </div>
          <a
            href="https://asteriostech07.lemonsqueezy.com/checkout/buy/a3dc2366-b80f-4c18-920b-2f608b7a063e"
            className="flex-1 border border-crtgreen bg-transparent text-crtgreen px-8 py-8 text-center text-lg font-black hover:bg-crtgreen hover:text-black uppercase tracking-widest block transition-none"
          >
            PROVISION API ACCESS
          </a>
        </div>
        <p className="text-xs text-zinc-600 mt-8 max-w-2xl font-mono">
          WARNING: ALL TRANSACTIONS ARE PROCESSED VIA LEMON SQUEEZY MERCHANT OF RECORD. 
          CRYPTOGRAPHIC TOKENS ARE DISPATCHED VIA EMAIL POST-AUTHENTICATION. CANCEL ANYTIME.
        </p>
      </section>

    </main>
  );
}
