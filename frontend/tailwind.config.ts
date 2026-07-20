import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        mono: ['var(--font-jetbrains-mono)', 'monospace'],
        sans: ['var(--font-inter)', 'sans-serif'],
      },
      colors: {
        trueblack: "#000000",
        sterilewhite: "#E5E7EB",
        phosphoramber: "#FFB000",
        crtgreen: "#00FF41",
      },
    },
  },
  plugins: [],
};
export default config;
