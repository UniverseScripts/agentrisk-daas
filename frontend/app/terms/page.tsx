import Link from "next/link";

export default function TermsPage() {
  return (
    <main className="min-h-screen bg-trueblack text-sterilewhite flex flex-col font-sans uppercase tracking-widest text-sm w-full">
      
      {/* NAVIGATION HEADER */}
      <div className="w-full border-b border-zinc-900 py-6 px-6 sm:px-10 lg:px-16 xl:px-24">
        <div className="max-w-[1600px] mx-auto flex items-center justify-between font-mono text-xs text-zinc-400">
          <Link href="/" className="hover:text-crtgreen transition-colors flex items-center gap-2 font-bold">
            <span>&lt;</span> RETURN TO TERMINAL
          </Link>
          <span className="text-crtgreen font-bold">[TERMS OF SERVICE &amp; SLA]</span>
        </div>
      </div>

      {/* HERO / THESIS */}
      <section className="w-full border-b border-zinc-900 py-12 lg:py-16 px-6 sm:px-10 lg:px-16 xl:px-24">
        <div className="max-w-[1600px] mx-auto">
          <p className="text-crtgreen text-xs font-mono mb-2">[LEGAL CONTRACT // SERVICE AGREEMENT]</p>
          <h1 className="text-3xl lg:text-4xl font-black mb-4">TERMS OF SERVICE &amp; SUBSCRIPTION AGREEMENT</h1>
          <p className="text-zinc-400 max-w-3xl leading-relaxed mt-4 lowercase normal-case tracking-normal text-base font-sans">
            Terms governing access to the AgentRisk Data-as-a-Service API, recurring subscriptions processed via Lemon Squeezy Merchant of Record, API key provisioning, and cancellation handling.
          </p>
        </div>
      </section>

      {/* SECTION 1: MERCHANT OF RECORD & BILLING */}
      <section className="w-full border-b border-zinc-900 py-12 px-6 sm:px-10 lg:px-16 xl:px-24">
        <div className="max-w-[1600px] mx-auto">
          <h2 className="text-xl font-bold text-crtgreen mb-6 font-mono">1. MERCHANT OF RECORD &amp; RECURRING SUBSCRIPTIONS</h2>
          <div className="space-y-4 text-zinc-300 text-sm lowercase normal-case tracking-normal font-sans leading-relaxed">
            <p>
              All financial transactions, customer billing, tax calculation, invoicing, and refund requests for AgentRisk DaaS subscriptions are conducted through our official Merchant of Record, <strong className="text-sterilewhite font-mono">Lemon Squeezy</strong>.
            </p>
            <p>
              By purchasing a recurring subscription ($15.00/month), you agree to Lemon Squeezy&apos;s Customer Terms of Service. Payments automatically renew monthly unless cancelled via your customer portal prior to the renewal billing cycle.
            </p>
          </div>
        </div>
      </section>

      {/* SECTION 2: PROVISIONING & CANCELLATION LIFECYCLE */}
      <section className="w-full border-b border-zinc-900 py-12 px-6 sm:px-10 lg:px-16 xl:px-24 bg-zinc-950/40">
        <div className="max-w-[1600px] mx-auto">
          <h2 className="text-xl font-bold text-zinc-400 mb-6 font-mono">2. API KEY PROVISIONING &amp; CANCELLATION POLICY</h2>
          <div className="space-y-4 text-zinc-300 text-sm lowercase normal-case tracking-normal font-sans leading-relaxed">
            <p>
              <strong className="text-sterilewhite font-mono uppercase">Instant Provisioning:</strong> Upon successful checkout verification via cryptographic HMAC-SHA256 webhook (<code className="text-crtgreen font-mono bg-zinc-950 px-2 py-1">subscription_created</code>), a unique API key is generated and dispatched immediately to your email.
            </p>
            <p>
              <strong className="text-sterilewhite font-mono uppercase">Cancellation &amp; Expiration Deactivation:</strong> You may cancel your subscription at any time via your billing receipt or customer dashboard. Upon receiving a <code className="text-crtgreen font-mono bg-zinc-950 px-2 py-1">subscription_cancelled</code> or <code className="text-crtgreen font-mono bg-zinc-950 px-2 py-1">subscription_expired</code> event, your provisioned API key is updated in our database to <code className="text-red-400 font-mono bg-zinc-950 px-2 py-1">is_active = False</code>, terminating API access immediately.
            </p>
          </div>
        </div>
      </section>

      {/* SECTION 3: ACCEPTABLE USE & LIMITATIONS */}
      <section className="w-full border-b border-zinc-900 py-12 px-6 sm:px-10 lg:px-16 xl:px-24">
        <div className="max-w-[1600px] mx-auto">
          <h2 className="text-xl font-bold text-crtgreen mb-6 font-mono">3. ACCEPTABLE USE &amp; RATE LIMIT COMPLIANCE</h2>
          <div className="space-y-4 text-zinc-300 text-sm lowercase normal-case tracking-normal font-sans leading-relaxed">
            <p>
              Subscriber API keys are non-transferable and intended exclusively for your organization or personal projects. Sharing, reselling, or attempting to bypass rate limits (60 requests/minute) is strictly prohibited.
            </p>
            <p>
              AgentRisk reserves the right to temporarily suspend or permanently revoke access for API keys attempting denial-of-service, credential brute-forcing, or infrastructure abuse.
            </p>
          </div>
        </div>
      </section>

      {/* SECTION 4: SUPPORT CONTACT */}
      <section className="w-full py-12 px-6 sm:px-10 lg:px-16 xl:px-24 font-mono text-xs">
        <div className="max-w-[1600px] mx-auto">
          <h2 className="text-xl font-bold text-zinc-400 mb-4">4. BILLING &amp; SUBSCRIPTION SUPPORT</h2>
          <p className="text-zinc-400 lowercase normal-case tracking-normal font-sans leading-relaxed mb-4 text-sm">
            For subscription assistance, key re-dispatch, or account support, contact our engineering team:
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
