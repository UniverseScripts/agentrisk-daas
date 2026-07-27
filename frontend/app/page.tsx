"use client";

import { useState } from "react";

export default function Page() {
  const [copied, setCopied] = useState(false);
  const [flash, setFlash] = useState(false);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(
      `curl -X GET "https://agentrisk-daas.onrender.com/api/v1/analytics/package-risk/npm/react" \\\n-H "X-API-Key: YOUR_API_KEY"`
    );
    setCopied(true);
    setFlash(true);
    setTimeout(() => setFlash(false), 150);
  };

  // Sample 30-day time series data points for visualizer
  const timeSeriesPoints = [
    { day: "D1", mci: 10.0, asi: 2.1 },
    { day: "D5", mci: 10.0, asi: 2.3 },
    { day: "D10", mci: 8.5, asi: 3.1 },
    { day: "D15", mci: 8.5, asi: 4.8 },
    { day: "D20", mci: 10.0, asi: 7.2 },
    { day: "D25", mci: 10.0, asi: 8.0 },
    { day: "D30", mci: 10.0, asi: 8.0 }
  ];

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

STATUS: ACTIVE (REV 3.0 CATALOG-WIDE)
NODE: EDGE INFRASTRUCTURE DAAS
ENCRYPTION: HMAC-SHA256 HMAC VERIFIED`}
        </pre>
        <h1 className="text-2xl md:text-4xl font-black mb-4">
          Maintainer & Dormancy Risk Signal DaaS
          <span className="blinking-cursor"></span>
        </h1>
        <p className="text-zinc-400 max-w-2xl leading-relaxed mt-6 lowercase normal-case tracking-normal text-base">
          On-demand maintainer concentration (MCI), dormancy/reactivation (DRI), anomalous activity (ASI), and typosquatting detection.
          Sourced live from public registry metadata across the AI agent supply chain (MCP, npm, PyPI).
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
"https://agentrisk-daas.onrender.com/api/v1/analytics/package-risk/npm/@modelcontextprotocol/sdk" \\
-H "X-API-Key: YOUR_API_KEY"`}
            </pre>
          </div>
        </div>

        <div className="p-8 lg:p-16 flex flex-col bg-zinc-950/50">
          <h2 className="text-xl font-bold mb-6 text-zinc-500 border-b border-zinc-900 pb-2">RESPONSE PAYLOAD</h2>
          <pre className="border border-zinc-900 bg-black p-4 text-xs overflow-x-auto text-zinc-400 font-mono flex-1">
{`{
  "package_name": "npm/@modelcontextprotocol/sdk",
  "timestamp": "2026-07-27T18:50:00Z",
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

      {/* 3. TIME-SERIES TELEMETRY & TYPOSQUAT LEDGER */}
      <section className="border-b border-zinc-900 p-8 lg:p-16 bg-black animate-reveal delay-150">
        <h2 className="text-xl font-bold mb-6 text-crtgreen border-b border-zinc-900 pb-2">HISTORICAL TELEMETRY & TYPOSQUAT GUARD</h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="border border-zinc-900 p-6 bg-zinc-950 font-mono text-xs">
            <p className="text-zinc-500 mb-4 tracking-widest">GET /api/v1/package-risk/{`{package_name}`}/history?limit=30</p>
            <div className="h-40 flex items-end justify-between gap-2 border-b border-l border-zinc-800 p-4 pt-8">
              {timeSeriesPoints.map((pt, i) => (
                <div key={i} className="flex flex-col items-center flex-1 h-full justify-end gap-1">
                  <div 
                    className="w-full bg-crtgreen/80 hover:bg-crtgreen transition-all"
                    style={{ height: `${(pt.asi / 10) * 100}%` }}
                    title={`ASI: ${pt.asi}`}
                  />
                  <span className="text-[10px] text-zinc-600 mt-1">{pt.day}</span>
                </div>
              ))}
            </div>
            <div className="flex justify-between items-center mt-3 text-[11px]">
              <span className="text-crtgreen">■ ANOMALOUS SPIKE INDEX (ASI) TREND</span>
              <span className="text-zinc-500">30-DAY RETENTION</span>
            </div>
          </div>

          <div className="border border-zinc-900 p-6 bg-zinc-950 font-mono text-xs flex flex-col justify-between">
            <div>
              <p className="text-zinc-500 mb-2 tracking-widest">SLOPSQUATTING / TYPOSQUAT DETECTOR</p>
              <pre className="text-amber-400 bg-black p-4 border border-zinc-900 overflow-x-auto text-[11px]">
{`{
  "detail": "Package identity 'npm/reaact' does not exist in registry.",
  "status": "not_found",
  "possible_typosquat_of": "npm/react",
  "similarity": 0.91
}`}
              </pre>
            </div>
            <p className="text-zinc-500 text-[11px] mt-4 leading-normal normal-case">
              Calculates edit distance against known registry targets to flag hallucinated dependencies propagated by LLM agents.
            </p>
          </div>
        </div>
      </section>

      {/* 4. THE FINANCIAL GATEWAY */}
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
