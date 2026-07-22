/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        surface: "rgb(var(--surface) / <alpha-value>)",
        base: "rgb(var(--base) / <alpha-value>)",
        ink: "rgb(var(--ink) / <alpha-value>)",
        muted: "rgb(var(--muted) / <alpha-value>)",
        line: "rgb(var(--line) / <alpha-value>)",
        accentblue: "rgb(var(--accent-blue) / <alpha-value>)",
        accentgreen: "rgb(var(--accent-green) / <alpha-value>)",
        accentwarm: "rgb(var(--accent-warm) / <alpha-value>)",
      },
      fontFamily: {
        display: ["'Space Grotesk'", "sans-serif"],
        body: ["'Inter'", "sans-serif"],
        mono: ["'JetBrains Mono'", "monospace"],
      },
      backdropBlur: {
        xs: "2px",
      },
      boxShadow: {
        glass: "0 8px 32px -8px rgba(0,0,0,0.18), inset 0 1px 0 0 rgba(255,255,255,0.12)",
        "glass-sm": "0 4px 16px -6px rgba(0,0,0,0.14), inset 0 1px 0 0 rgba(255,255,255,0.1)",
        glow: "0 0 0 1px rgb(var(--accent-blue) / 0.35), 0 0 24px -4px rgb(var(--accent-blue) / 0.45)",
      },
      keyframes: {
        pulseRing: {
          "0%": { boxShadow: "0 0 0 0 rgb(var(--ring-color) / 0.55)" },
          "70%": { boxShadow: "0 0 0 14px rgb(var(--ring-color) / 0)" },
          "100%": { boxShadow: "0 0 0 0 rgb(var(--ring-color) / 0)" },
        },
        floatSlow: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-10px)" },
        },
        shimmer: {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
      },
      animation: {
        pulseRing: "pulseRing 1.8s cubic-bezier(0.4,0,0.6,1) infinite",
        floatSlow: "floatSlow 6s ease-in-out infinite",
        shimmer: "shimmer 2.5s linear infinite",
      },
    },
  },
  plugins: [],
}
