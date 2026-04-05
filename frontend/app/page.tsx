"use client";

export default function Page() {
  const copyToClipboard = () => {
    navigator.clipboard.writeText(
      `curl -X GET "https://api.yourdomain.com/api/v1/ai-developer-velocity/pytorch/pytorch" \\
-H "X-API-Key: YOUR_API_KEY"`
    );
    const btn = document.getElementById("copy-btn");
    if (btn) {
      btn.innerText = "[COPIED]";
      // Anti-vibe execution: Do not utilize a setTimeout to revert back to '[COPY]'.
      // Leave it starkly locked at '[COPIED]'.
    }
  };

  return (
    <main className="min-h-screen bg-trueblack text-sterilewhite flex flex-col p-8 lg:p-16 uppercase tracking-widest text-sm max-w-7xl mx-auto border-x border-gray-800">
      
      {/* 1. THE HERO PROTOCOL */}
      <section className="border-b border-gray-800 pb-16 pt-8">
        <pre className="text-crtgreen text-xs md:text-sm whitespace-pre border-none font-bold mb-8">
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
          Institutional-Grade AI Developer Velocity API
          <span className="blinking-cursor"></span>
        </h1>
        <p className="text-gray-400 max-w-2xl leading-relaxed mt-6">
          Real-time execution telemetry mapping the top 50 artificial intelligence repositories.
          Strict tracking of contributor churn, fork velocity, and temporal commits. No marketing. No UI bloat. Only raw data matrix.
        </p>
      </section>

      {/* 2. THE INTEGRATION LEDGER */}
      <section className="border-b border-gray-800 py-16 flex flex-col lg:flex-row gap-12">
        <div className="flex-1 border-r border-gray-800 pr-0 lg:pr-12 relative">
          <h2 className="text-xl font-bold mb-6 text-crtgreen border-b border-gray-800 pb-2">REQUEST ARBITRAGE</h2>
          <div className="relative group border border-gray-800 bg-black p-4">
            <button 
              id="copy-btn"
              onClick={copyToClipboard}
              className="absolute top-0 right-0 bg-gray-900 border-l border-b border-gray-800 px-3 py-1 text-xs text-crtgreen uppercase hover:bg-gray-800 cursor-pointer"
            >
              [COPY]
            </button>
            <pre className="text-gray-300 text-xs overflow-x-auto mt-2">
{`curl -X GET \\
"https://api.yourdomain.com/api/v1/ai-developer-velocity/pytorch/pytorch" \\
-H "X-API-Key: YOUR_API_KEY"`}
            </pre>
          </div>
        </div>

        <div className="flex-1">
          <h2 className="text-xl font-bold mb-6 text-phosphoramber border-b border-gray-800 pb-2">RESPONSE PAYLOAD</h2>
          <pre className="border border-gray-800 bg-gray-950 p-4 text-xs overflow-x-auto text-phosphoramber">
{`{
  "repo_name": "pytorch/pytorch",
  "commit_velocity_24h": 142,
  "open_issues_delta": -5,
  "fork_velocity_24h": 38,
  "contributor_churn": 0.824,
  "timestamp": "2026-04-05T00:00:00Z"
}`}
          </pre>
        </div>
      </section>

      {/* 3. THE FINANCIAL GATEWAY */}
      <section className="py-16">
        <h2 className="text-xl font-bold text-gray-500 mb-8 border-b border-gray-800 pb-2">SECURE PERIMETER ACCESS</h2>
        <div className="flex flex-col sm:flex-row items-center gap-6">
          <div className="border border-gray-800 p-4 w-full sm:w-auto bg-gray-950">
            <p className="text-gray-400 text-xs mb-2">ALLOCATION: 10,000 API CALLS</p>
            <p className="text-2xl font-bold">$499.00 USD</p>
          </div>
          <a
            href="https://[your-store].lemonsqueezy.com/checkout/buy/00000000-0000-0000-0000-000000000000"
            className="w-full sm:w-auto border border-crtgreen bg-transparent text-crtgreen px-8 py-4 text-center font-bold hover:bg-crtgreen hover:text-black uppercase tracking-widest block"
          >
            PROVISION API ACCESS
          </a>
        </div>
        <p className="text-xs text-gray-600 mt-6 max-w-lg">
          WARNING: ALL TRANSACTIONS ARE PROCESSED VIA LEMON SQUEEZY MERCHANT OF RECORD. 
          CRYPTOGRAPHIC TOKENS ARE DISPATCHED VIA EMAIL POST-AUTHENTICATION. ALL SALES FINAL.
        </p>
      </section>

    </main>
  );
}
