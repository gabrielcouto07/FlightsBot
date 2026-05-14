import type { Config } from 'tailwindcss';

export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // Dark theme - Linear.app inspired
        'bg-primary': '#0f0f0f',
        'bg-secondary': '#161616',
        'bg-tertiary': '#1c1c1c',
        'bg-quaternary': '#242424',
        'border-primary': '#2a2a2a',
        'border-secondary': '#333333',
        // Accent - Teal
        'teal': {
          DEFAULT: '#00b4b4',
          light: '#1ecccf',
          dark: '#009999',
        },
        // Semantic colors
        'success': '#10b981',
        'warning': '#f59e0b',
        'danger': '#ef4444',
        'info': '#3b82f6',
      },
      backgroundColor: {
        'surface': '#161616',
        'surface-hover': '#1c1c1c',
      },
      textColor: {
        'primary': '#ffffff',
        'secondary': '#a0a0a0',
        'tertiary': '#808080',
      },
      borderColor: {
        'default': '#2a2a2a',
      },
      spacing: {
        'safe': 'env(safe-area-inset-bottom)',
      },
      fontSize: {
        'xs': ['12px', '16px'],
        'sm': ['14px', '20px'],
        'base': ['16px', '24px'],
        'lg': ['18px', '28px'],
        'xl': ['20px', '28px'],
        '2xl': ['24px', '32px'],
        '3xl': ['30px', '36px'],
      },
      shadows: {
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
      },
    },
  },
  plugins: [],
} satisfies Config;
