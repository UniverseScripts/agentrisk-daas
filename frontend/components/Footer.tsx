"use client";

import Link from "next/link";

export default function Footer() {
  return (
    <footer className="border-t border-zinc-900 bg-trueblack text-sterilewhite font-mono text-xs uppercase tracking-widest max-w-7xl mx-auto w-full">
      {/* 1. TOP TERMINAL STATUS STRIP */}
      <div className="border-b border-zinc-900 p-4 px-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 text-zinc-500 text-[11px]">
        <div className="flex items-center gap-3">
          <span className="h-2 w-2 rounded-full bg-crtgreen animate-pulse"></span>
          <span>SYSTEM STATUS: <span className="text-crtgreen font-bold">ALL ENDPOINTS OPERATIONAL</span></span>
        </div>
        <div className="flex items-center gap-6">
          <span>LATENCY: &lt;45MS</span>
          <span>REGION: US-EAST-1</span>
          <span>GATEWAY: RENDER EDGE</span>
        </div>
      </div>

      {/* 2. MAIN FOOTER DIRECTORY GRID */}
      <div className="grid grid-cols-1 md:grid-cols-4 border-b border-zinc-900">
        
        {/* COL 1: IDENTITY */}
        <div className="p-8 border-b md:border-b-0 md:border-r border-zinc-900 flex flex-col justify-between">
          <div>
            <p className="text-crtgreen font-bold text-sm mb-3">AGENTRISK DAAS</p>
            <p className="text-zinc-400 text-xs normal-case tracking-normal leading-relaxed mb-6 font-sans">
              Institutional maintainer concentration, dormancy reactivation, and typosquatting signal telemetry for AI agent supply chains.
            </p>
          </div>
          <p className="text-[10px] text-zinc-600">
            © {new Date().getFullYear()} AGENTRISK INC. ALL RIGHTS RESERVED.
          </p>
        </div>

        {/* COL 2: ENDPOINT DIRECTORY */}
        <div className="p-8 border-b md:border-b-0 md:border-r border-zinc-900">
          <p className="text-zinc-500 font-bold mb-4 tracking-widest text-[11px]">DOCUMENTATION</p>
          <ul className="space-y-3 text-zinc-300">
            <li>
              <Link href="/docs" className="hover:text-crtgreen transition-colors flex items-center gap-2">
                <span className="text-zinc-600">&gt;</span> API MANUAL &amp; ENDPOINTS
              </Link>
            </li>
            <li>
              <Link href="/docs#authentication" className="hover:text-crtgreen transition-colors flex items-center gap-2">
                <span className="text-zinc-600">&gt;</span> AUTHENTICATION (X-API-KEY)
              </Link>
            </li>
            <li>
              <Link href="/docs#rate-limits" className="hover:text-crtgreen transition-colors flex items-center gap-2">
                <span className="text-zinc-600">&gt;</span> RATE LIMITS (60 REQ/MIN)
              </Link>
            </li>
            <li>
              <Link href="/docs#status-codes" className="hover:text-crtgreen transition-colors flex items-center gap-2">
                <span className="text-zinc-600">&gt;</span> STATUS CODES &amp; ERRORS
              </Link>
            </li>
          </ul>
        </div>

        {/* COL 3: GOVERNANCE & POLICIES */}
        <div className="p-8 border-b md:border-b-0 md:border-r border-zinc-900">
          <p className="text-zinc-500 font-bold mb-4 tracking-widest text-[11px]">GOVERNANCE</p>
          <ul className="space-y-3 text-zinc-300">
            <li>
              <Link href="/policies" className="hover:text-crtgreen transition-colors flex items-center gap-2">
                <span className="text-zinc-600">&gt;</span> PRIVACY &amp; DATA GOVERNANCE
              </Link>
            </li>
            <li>
              <Link href="/terms" className="hover:text-crtgreen transition-colors flex items-center gap-2">
                <span className="text-zinc-600">&gt;</span> TERMS OF SERVICE &amp; SLA
              </Link>
            </li>
            <li>
              <a 
                href="mailto:asteriostech@gmail.com" 
                className="hover:text-crtgreen transition-colors flex items-center gap-2 lowercase tracking-normal"
              >
                <span className="text-zinc-600 uppercase font-mono">&gt;</span> asteriostech@gmail.com
              </a>
            </li>
          </ul>
        </div>

        {/* COL 4: MERCHANT OF RECORD */}
        <div className="p-8 flex flex-col justify-between bg-zinc-950/40">
          <div>
            <p className="text-zinc-500 font-bold mb-3 tracking-widest text-[11px]">MERCHANT OF RECORD</p>
            <p className="text-zinc-400 text-xs normal-case tracking-normal leading-relaxed font-sans mb-4">
              All subscription billing, invoicing, and tax compliance are securely processed by Lemon Squeezy, our official Merchant of Record.
            </p>
          </div>
          <div className="border border-zinc-800 p-3 bg-black text-center">
            <span className="text-zinc-400 text-[10px] block">POWERED BY LEMON SQUEEZY</span>
          </div>
        </div>

      </div>
    </footer>
  );
}
