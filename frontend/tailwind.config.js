/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}"
  ],
  safelist: [
    'bg-primary',
    'bg-secondary',
    'bg-light',
    'bg-accent',
    'bg-dark',
    'text-primary',
    'text-secondary',
    'text-light',
    'text-accent',
    'text-dark',
  ],
  theme: {
    extend: {
      colors: {
        primary: "#1E3A8A",
        secondary: "#3B82F6",
        light: "#BFDBFE",
        accent: "#60A5FA",
        dark: "#1E40AF",
      },
    },
  },
  plugins: [],
}