import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
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
