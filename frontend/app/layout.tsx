import type { Metadata } from "next";
import { JetBrains_Mono, Inter } from "next/font/google";
import Footer from "@/components/Footer";
import "./globals.css";

const jetbrainsMono = JetBrains_Mono({ 
  subsets: ["latin"],
  variable: "--font-jetbrains-mono"
});

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter"
});

export const metadata: Metadata = {
  title: "AgentRisk DaaS | Institutional Risk Telemetry",
  description: "Maintainer concentration, dormancy reactivation, and typosquatting telemetry for AI agent supply chains.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${jetbrainsMono.variable} ${inter.variable}`}>
      <body className="font-sans bg-trueblack text-sterilewhite min-h-screen flex flex-col justify-between">
        <div className="flex-1">
          {children}
        </div>
        <Footer />
      </body>
    </html>
  );
}
