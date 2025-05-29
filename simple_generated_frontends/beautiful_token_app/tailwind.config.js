/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'aleo-blue': '#0055FF',
        'aleo-dark': '#001133',
        'aleo-light': '#E6F0FF',
      }
    },
  },
  plugins: [],
}