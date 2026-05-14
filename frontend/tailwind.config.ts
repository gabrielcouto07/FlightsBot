import type { Config } from 'tailwindcss';

export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // Refined dark palette
        'bg-primary': '#0A0E13',
        'bg-secondary': '#10141C',
        'bg-tertiary': '#16202A',
        'bg-quaternary': '#1F2937',
        
        // Subtle borders and dividers
        'border-primary': '#2D3E4F',
        'border-secondary': '#4A5A6F',
        
        // Premium accent: Electric teal
        'accent': '#06D6D6',
        'accent-light': '#38F9F9',
        'accent-dark': '#059B9B',
        
        // Status colors (refined)
        'success': '#10B981',
        'warning': '#F59E0B',
        'danger': '#EF4444',
        'info': '#3B82F6',
      },
      textColor: {
        'text-primary': '#F0F4F8',
        'text-secondary': '#A8BAD4',
        'text-tertiary': '#7E8FA3',
        'text-muted': '#5A6B7F',
        // Legacy aliases for backwards compatibility
        'primary': '#F0F4F8',
        'secondary': '#A8BAD4',
        'tertiary': '#7E8FA3',
        'muted': '#5A6B7F',
      },
      backgroundColor: {
        'surface': '#10141C',
        'surface-hover': '#16202A',
        'surface-focus': '#1F2937',
      },
      borderColor: {
        'default': '#2D3E4F',
      },
      spacing: {
        'safe': 'env(safe-area-inset-bottom)',
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['Fira Code', 'JetBrains Mono', 'monospace'],
      },
      fontSize: {
        'xs': ['12px', '16px'],
        'sm': ['14px', '20px'],
        'base': ['15px', '24px'],
        'lg': ['17px', '28px'],
        'xl': ['20px', '28px'],
        '2xl': ['24px', '32px'],
        '3xl': ['32px', '40px'],
      },
      boxShadow: {
        'xs': '0 1px 2px rgba(0, 0, 0, 0.08)',
        'sm': '0 2px 4px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.04)',
        'md': '0 4px 8px rgba(0, 0, 0, 0.16), 0 2px 4px rgba(0, 0, 0, 0.08)',
        'lg': '0 8px 16px rgba(0, 0, 0, 0.2), 0 4px 8px rgba(0, 0, 0, 0.1)',
        'xl': '0 12px 24px rgba(0, 0, 0, 0.24), 0 6px 12px rgba(0, 0, 0, 0.12)',
      },
      keyframes: {
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        'slide-up': {
          '0%': { transform: 'translateY(8px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
      animation: {
        'fade-in': 'fade-in 0.3s ease-in-out',
        'slide-up': 'slide-up 0.3s ease-out',
      },
    },
  },
  plugins: [],
} satisfies Config;
