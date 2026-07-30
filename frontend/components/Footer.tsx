"use client";

import Link from "next/link";

export default function Footer() {
  return (
    <footer className="w-full bg-trueblack text-sterilewhite font-mono text-xs uppercase tracking-widest border-t border-zinc-900">
      
      {/* 1. TOP TITLE HEADER & SYSTEM STATUS STRIP (Synchronized px-6 lg:px-10 padding matching Column 1 below) */}
      <div className="w-full border-b border-zinc-900 py-4 px-6 lg:px-10 bg-black">
        <div className="w-full flex flex-row items-center justify-between gap-4 font-mono text-xs">
          <div className="flex items-center gap-3 whitespace-nowrap overflow-hidden text-ellipsis">
            <span className="h-2.5 w-2.5 rounded-full bg-crtgreen animate-pulse flex-shrink-0"></span>
            <p className="text-crtgreen font-bold text-xs sm:text-sm md:text-base tracking-wider whitespace-nowrap">
              AGENTRISK DAAS // INSTITUTIONAL TELEMETRY ENGINE
            </p>
          </div>
          <div className="flex items-center gap-4 sm:gap-6 text-zinc-400 text-[11px] font-mono whitespace-nowrap flex-shrink-0">
            <span>STATUS: <strong className="text-crtgreen font-bold">OPERATIONAL</strong></span>
            <span className="hidden sm:inline">LATENCY: &lt;45MS</span>
            <span className="hidden lg:inline">REGION: US-EAST-1</span>
          </div>
        </div>
      </div>

      {/* 2. 3-COLUMN VERTICALLY DIVIDED GRID (GOV | DOC | MOR side-by-side) */}
      <div className="w-full bg-trueblack border-b border-zinc-900">
        <div className="w-full grid grid-cols-1 sm:grid-cols-3 divide-y sm:divide-y-0 sm:divide-x divide-zinc-900">
          
          {/* COLUMN 1: GOV (Governance) */}
          <div className="p-6 lg:p-10 space-y-4">
            <div className="flex items-center gap-2 border-b border-zinc-900 pb-3">
              <span className="text-crtgreen font-bold text-sm lg:text-base">GOV</span>
              <span className="text-zinc-500 text-[10px] lg:text-[11px] font-mono">// DATA GOVERNANCE &amp; PRIVACY</span>
            </div>
            <ul className="space-y-3 pt-1 font-mono text-xs">
              <li>
                <Link href="/policies" className="text-zinc-300 hover:text-crtgreen transition-colors flex items-center gap-2">
                  <span className="text-zinc-600">&gt;</span> PRIVACY &amp; GOVERNANCE
                </Link>
              </li>
              <li>
                <Link href="/terms" className="text-zinc-300 hover:text-crtgreen transition-colors flex items-center gap-2">
                  <span className="text-zinc-600">&gt;</span> TERMS &amp; SLA
                </Link>
              </li>
              <li>
                <a 
                  href="mailto:asteriostech@gmail.com" 
                  className="text-zinc-400 hover:text-crtgreen transition-colors flex items-center gap-2 lowercase tracking-normal font-sans text-xs"
                >
                  <span className="text-zinc-600 uppercase font-mono">&gt;</span> asteriostech@gmail.com
                </a>
              </li>
            </ul>
          </div>

          {/* COLUMN 2: DOC (Documentation) */}
          <div className="p-6 lg:p-10 space-y-4">
            <div className="flex items-center gap-2 border-b border-zinc-900 pb-3">
              <span className="text-crtgreen font-bold text-sm lg:text-base">DOC</span>
              <span className="text-zinc-500 text-[10px] lg:text-[11px] font-mono">// API MANUAL &amp; ENDPOINTS</span>
            </div>
            <ul className="space-y-3 pt-1 font-mono text-xs">
              <li>
                <Link href="/docs" className="text-zinc-300 hover:text-crtgreen transition-colors flex items-center gap-2">
                  <span className="text-zinc-600">&gt;</span> API MANUAL &amp; DIRECTORY
                </Link>
              </li>
              <li>
                <Link href="/docs#authentication" className="text-zinc-300 hover:text-crtgreen transition-colors flex items-center gap-2">
                  <span className="text-zinc-600">&gt;</span> AUTHENTICATION (X-API-KEY)
                </Link>
              </li>
              <li>
                <Link href="/docs#rate-limits" className="text-zinc-300 hover:text-crtgreen transition-colors flex items-center gap-2">
                  <span className="text-zinc-600">&gt;</span> RATE LIMITS (60 REQ/MIN)
                </Link>
              </li>
              <li>
                <Link href="/docs#status-codes" className="text-zinc-300 hover:text-crtgreen transition-colors flex items-center gap-2">
                  <span className="text-zinc-600">&gt;</span> STATUS CODES &amp; ERRORS
                </Link>
              </li>
            </ul>
          </div>

          {/* COLUMN 3: MOR (Merchant of Record) */}
          <div className="p-6 lg:p-10 space-y-4 flex flex-col justify-between">
            <div>
              <div className="flex items-center gap-2 border-b border-zinc-900 pb-3 mb-3">
                <span className="text-crtgreen font-bold text-sm lg:text-base">MOR</span>
                <span className="text-zinc-500 text-[10px] lg:text-[11px] font-mono">// MERCHANT OF RECORD</span>
              </div>
              <p className="text-zinc-400 text-xs normal-case tracking-normal leading-relaxed font-sans mb-4">
                All subscription billing, tax calculation, and invoicing are securely conducted by Lemon Squeezy, our official Merchant of Record.
              </p>
            </div>
            <div className="border border-zinc-800 bg-black p-3 text-center">
              <span className="text-zinc-400 text-[10px] block font-mono">VERIFIED BY <strong className="text-sterilewhite font-bold">LEMON SQUEEZY MOR</strong></span>
            </div>
          </div>

        </div>
      </div>

      {/* 3. BOTTOM COPYRIGHT FOOTER STRIP */}
      <div className="w-full py-4 px-6 lg:px-10 bg-black text-center">
        <p className="text-[10px] text-zinc-600 font-mono">
          © {new Date().getFullYear()} AGENTRISK INC. ALL RIGHTS RESERVED.
        </p>
      </div>

    </footer>
  );
}
