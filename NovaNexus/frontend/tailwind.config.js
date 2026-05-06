/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#020205',
        primary: '#00f2ff',
        secondary: '#7000ff',
        success: '#00ff88',
        warning: '#ffbb00',
        error: '#ff0055',
      },
      boxShadow: {
        'neon-blue': '0 0 15px rgba(0, 242, 255, 0.5)',
        'neon-purple': '0 0 15px rgba(112, 0, 255, 0.5)',
      }
    },
  },
  plugins: [],
}
