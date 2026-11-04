/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        midnightBlack: '#0d0d0d',
        coffinPurple: '#1a0a2e',
        deepGrave: '#120720',
        pumpkinOrange: '#ff6b00',
        pumpkinGlow: '#ff8c33',
        bloodRed: '#8b0000',
        bloodVibrant: '#ff1a1a',
        ghostGreen: '#00ff88',
        slimeGreen: '#39ff14',
        cauldronYellow: '#ffd700',
        boneWhite: '#e0d8cc',
        cobwebGray: '#3a3440',
      },
      fontFamily: {
        creepster: ['"Creepster"', 'cursive'],
        mono: ['"JetBrains Mono"', 'monospace'],
        body: ['"Inter"', 'sans-serif'],
      },
      boxShadow: {
        'pumpkin-glow': '0 0 15px rgba(255, 107, 0, 0.4)',
        'ghost-glow': '0 0 15px rgba(0, 255, 136, 0.4)',
        'blood-glow': '0 0 15px rgba(255, 26, 26, 0.4)',
      }
    },
  },
  plugins: [],
}

