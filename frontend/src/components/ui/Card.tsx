import { ReactNode } from 'react';

interface CardProps {
  children: ReactNode;
  className?: string;
  onClick?: () => void;
  hoverable?: boolean;
}

export const Card = ({ children, className = '', onClick, hoverable = false }: CardProps) => {
  return (
    <div
      className={`rounded-xl border border-border-primary bg-gradient-to-br from-bg-secondary to-bg-tertiary p-6 backdrop-blur-sm ${
        hoverable
          ? 'cursor-pointer transition-all duration-300 hover:border-accent/50 hover:shadow-lg hover:shadow-accent/10 hover:-translate-y-0.5'
          : ''
      } ${className}`}
      onClick={onClick}
    >
      {children}
    </div>
  );
};
