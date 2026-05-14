import { ReactNode } from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: 'primary' | 'secondary' | 'danger' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

export const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  disabled,
  ...props
}: ButtonProps) => {
  const baseClasses =
    'font-medium rounded-lg transition-colors duration-200 flex items-center justify-center gap-2';

  const variantClasses = {
    primary: 'bg-teal text-bg-primary hover:bg-teal-light disabled:bg-border-primary',
    secondary: 'bg-bg-tertiary text-primary hover:bg-bg-quaternary disabled:bg-border-primary',
    danger: 'bg-danger text-white hover:bg-red-600 disabled:bg-border-primary',
    outline: 'border border-border-primary text-primary hover:bg-bg-secondary disabled:opacity-50',
  };

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]}`}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? <span className="animate-spin">⏳</span> : null}
      {children}
    </button>
  );
};
