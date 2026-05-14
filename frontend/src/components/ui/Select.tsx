interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  options: Array<{ value: string | number; label: string }>;
  error?: string;
}

export const Select = ({
  label,
  options,
  error,
  className = '',
  ...props
}: SelectProps) => {
  return (
    <div className="flex flex-col gap-2">
      {label && <label className="text-sm font-600 text-text-primary">{label}</label>}
      <select
        className={`h-11 appearance-none rounded-lg border border-border-primary bg-bg-tertiary px-4 text-text-primary cursor-pointer transition-all duration-200 focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/20 ${
          error ? 'border-danger/60 focus:ring-danger/20' : ''
        } ${className}`}
        {...props}
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {error && <span className="text-xs text-danger font-500">{error}</span>}
    </div>
  );
};
