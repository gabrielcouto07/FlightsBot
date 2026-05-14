interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helpText?: string;
}

export const Input = ({ label, error, helpText, className = '', ...props }: InputProps) => {
  return (
    <div className="flex flex-col gap-2">
      {label && <label className="text-sm font-600 text-text-primary">{label}</label>}
      <input
        className={`h-11 rounded-lg border border-border-primary bg-bg-tertiary px-4 text-text-primary placeholder:text-text-muted transition-all duration-200 focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/20 ${
          error ? 'border-danger/60 focus:ring-danger/20' : ''
        } ${className}`}
        {...props}
      />
      {error && <span className="text-xs text-danger font-500">{error}</span>}
      {helpText && <span className="text-xs text-text-muted">{helpText}</span>}
    </div>
  );
};
