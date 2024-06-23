import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        sky: {
          50: "#d9f0ff", // Darkened from #f0f9ff
          100: "#c3e4fe", // Darkened from #e0f2fe
          200: "#a3d4fd", // Darkened from #bae6fd
          300: "#5cbdfc", // Darkened from #7dd3fc
          400: "#2aa3f8", // Darkened from #38bdf8
          500: "#0b8edc", // Darkened from #0ea5e9
          600: "#026baa", // Darkened from #0284c7
          700: "#015a89", // Darkened from #0369a1
          800: "#054b6e", // Darkened from #075985
          900: "#083857", // Darkened from #0c4a6e
          950: "#062338", // Darkened from #082f49
        },
        orange: {
          100: "#f8d5c7",
          200: "#f1ac9a",
          300: "#ea836d",
          400: "#e35a40",
          500: "#d77a61",
          600: "#c45b3f",
          700: "#b23a1b",
          800: "#D18829", // Orange from logo
        },
      },
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
    },
  },
  plugins: [],
};

export default config;
