interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helpText?: string;
}

export const Input = ({ label, error, helpText, className = '', ...props }: InputProps) => {
  return (
    <div className="flex flex-col gap-1">
      {label && <label className="text-sm font-medium text-primary">{label}</label>}
      <input
        className={`bg-bg-tertiary border border-border-primary rounded-lg px-3 py-2 text-primary placeholder-tertiary focus:outline-none focus:border-teal transition-colors ${className}`}
        {...props}
      />
      {error && <span className="text-xs text-danger">{error}</span>}
      {helpText && <span className="text-xs text-tertiary">{helpText}</span>}
    </div>
  );
};
