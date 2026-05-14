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
    <div className="flex flex-col gap-1">
      {label && <label className="text-sm font-medium text-primary">{label}</label>}
      <select
        className={`bg-bg-tertiary border border-border-primary rounded-lg px-3 py-2 text-primary focus:outline-none focus:border-teal transition-colors cursor-pointer ${className}`}
        {...props}
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {error && <span className="text-xs text-danger">{error}</span>}
    </div>
  );
};
