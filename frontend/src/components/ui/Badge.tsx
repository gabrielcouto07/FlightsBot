import { ReactNode } from 'react';

interface BadgeProps {
  children: ReactNode;
  variant?: 'default' | 'success' | 'warning' | 'danger' | 'info' | 'accent';
  size?: 'sm' | 'md';
}

export const Badge = ({ children, variant = 'default', size = 'sm' }: BadgeProps) => {
  const variantClasses = {
    default: 'bg-bg-quaternary text-text-primary border border-border-primary',
    success: 'bg-success/15 text-success border border-success/30',
    warning: 'bg-warning/15 text-warning border border-warning/30',
    danger: 'bg-danger/15 text-danger border border-danger/30',
    info: 'bg-info/15 text-info border border-info/30',
    accent: 'bg-accent/15 text-accent border border-accent/30',
  };

  const sizeClasses = {
    sm: 'px-2.5 py-1 text-xs font-500',
    md: 'px-3.5 py-1.5 text-sm font-500',
  };

  return (
    <span
      className={`inline-flex items-center rounded-lg ${variantClasses[variant]} ${sizeClasses[size]}`}
    >
      {children}
    </span>
  );
};
