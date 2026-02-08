/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#EC4899',
        secondary: '#F472B6',
        cta: '#06B6D4',
        background: '#FDF2F8',
        text: '#831843',
      },
      fontFamily: {
        sans: ['"Baloo 2"', '"Comic Neue"', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
