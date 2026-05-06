/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#050505',
        surface: '#0f0f0f',
        primary: '#00f2ff', // Cyan Neon
        secondary: '#7000ff', // Purple Neon
        accent: '#ff00c8', // Pink Neon
        success: '#00ff88',
        warning: '#ffbb00',
        error: '#ff3333',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'glass-gradient': 'linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.01))',
      },
      boxShadow: {
        'neon-blue': '0 0 15px rgba(0, 242, 255, 0.3)',
        'neon-purple': '0 0 15px rgba(112, 0, 255, 0.3)',
      }
    },
  },
  plugins: [],
}
