/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cyber: {
          bg: '#030712',
          panel: '#0B132B',
          border: 'rgba(0, 240, 255, 0.2)',
          cyan: '#00F0FF',
          amber: '#F59E0B',
          emerald: '#10B981',
          magenta: '#F43F5E',
          darkBlue: '#0F172A',
          glass: 'rgba(11, 19, 43, 0.85)'
        }
      },
      fontFamily: {
        display: ['Space Grotesk', 'sans-serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace']
      },
      boxShadow: {
        'cyan-glow': '0 0 25px rgba(0, 240, 255, 0.25)',
        'amber-glow': '0 0 25px rgba(245, 158, 11, 0.25)',
        'magenta-glow': '0 0 25px rgba(244, 63, 94, 0.25)'
      }
    },
  },
  plugins: [],
}
