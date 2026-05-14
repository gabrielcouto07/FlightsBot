import { ChevronDown } from 'lucide-react';

interface AutocompleteInputProps {
  label?: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  error?: string;
  onFocus?: () => void;
}

export const AutocompleteInput = ({
  label,
  value,
  onChange,
  placeholder = '',
  error,
  onFocus,
}: AutocompleteInputProps) => {
  return (
    <div className="relative flex flex-col gap-2">
      {label && <label className="text-sm font-600 text-text-primary">{label}</label>}
      <div className="relative">
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onFocus={onFocus}
          placeholder={placeholder}
          className={`w-full h-11 rounded-lg border border-border-primary bg-bg-tertiary px-4 text-text-primary placeholder:text-text-muted transition-all duration-200 focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/20 pr-10 ${
            error ? 'border-danger/60 focus:ring-danger/20' : ''
          }`}
        />
        <ChevronDown
          size={16}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-text-muted pointer-events-none"
        />
      </div>

      {error && <span className="text-xs text-danger font-500">{error}</span>}
    </div>
  );
};
