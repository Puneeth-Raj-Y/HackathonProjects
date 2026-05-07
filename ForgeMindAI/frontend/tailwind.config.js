/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        bg: '#050816',
        panel: 'rgba(11, 18, 32, 0.72)',
        line: 'rgba(125, 211, 252, 0.16)',
        neon: {
          cyan: '#4fd1ff',
          aqua: '#22d3ee',
          blue: '#3b82f6',
          magenta: '#ec4899',
          lime: '#a3e635',
          amber: '#f59e0b',
          red: '#f87171',
        },
      },
      boxShadow: {
        glow: '0 0 0 1px rgba(79, 209, 255, 0.18), 0 20px 80px rgba(3, 105, 161, 0.28)',
      },
      backgroundImage: {
        'grid-faint':
          'linear-gradient(rgba(148, 163, 184, 0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(148, 163, 184, 0.08) 1px, transparent 1px)',
      },
      keyframes: {
        floaty: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% center' },
          '100%': { backgroundPosition: '200% center' },
        },
      },
      animation: {
        floaty: 'floaty 8s ease-in-out infinite',
        shimmer: 'shimmer 3s linear infinite',
      },
    },
  },
  plugins: [],
};
