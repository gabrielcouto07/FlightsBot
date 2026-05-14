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
      className={`bg-bg-secondary border border-border-primary rounded-lg p-4 ${
        hoverable ? 'cursor-pointer hover:bg-bg-tertiary transition-colors' : ''
      } ${className}`}
      onClick={onClick}
    >
      {children}
    </div>
  );
};
