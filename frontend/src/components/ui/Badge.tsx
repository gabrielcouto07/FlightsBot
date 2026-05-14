import { ReactNode } from 'react';

interface BadgeProps {
  children: ReactNode;
  variant?: 'default' | 'success' | 'warning' | 'danger' | 'info' | 'teal';
  size?: 'sm' | 'md';
}

export const Badge = ({ children, variant = 'default', size = 'sm' }: BadgeProps) => {
  const variantClasses = {
    default: 'bg-bg-tertiary text-secondary',
    success: 'bg-green-900 text-green-200',
    warning: 'bg-yellow-900 text-yellow-200',
    danger: 'bg-red-900 text-red-200',
    info: 'bg-blue-900 text-blue-200',
    teal: 'bg-teal-900 text-teal-200',
  };

  const sizeClasses = {
    sm: 'px-2 py-1 text-xs',
    md: 'px-3 py-1.5 text-sm',
  };

  return (
    <span className={`rounded-full inline-block font-medium ${variantClasses[variant]} ${sizeClasses[size]}`}>
      {children}
    </span>
  );
};
