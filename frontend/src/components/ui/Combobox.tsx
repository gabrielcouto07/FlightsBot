import { useEffect, useMemo, useRef, useState } from 'react';
import { ChevronDown, MapPin, X } from 'lucide-react';

export interface ComboboxOption {
  value: string;
  label: string;
  description: string;
  flag?: string;
  searchText?: string;
}

interface ComboboxProps {
  label: string;
  value: string;
  options: ComboboxOption[];
  placeholder: string;
  onChange: (option: ComboboxOption | null) => void;
  error?: string;
}

export const Combobox = ({
  label,
  value,
  options,
  placeholder,
  onChange,
  error,
}: ComboboxProps) => {
  const rootRef = useRef<HTMLDivElement | null>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);
  const selectedOption = options.find((option) => option.value.toUpperCase() === value.toUpperCase()) ?? null;
  const [query, setQuery] = useState(selectedOption?.label ?? '');
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    setQuery(selectedOption?.label ?? '');
  }, [selectedOption]);

  useEffect(() => {
    const handlePointerDown = (event: MouseEvent) => {
      if (!rootRef.current?.contains(event.target as Node)) {
        setIsOpen(false);
        setQuery(selectedOption?.label ?? '');
      }
    };

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setIsOpen(false);
        setQuery(selectedOption?.label ?? '');
        inputRef.current?.blur();
      }
    };

    document.addEventListener('mousedown', handlePointerDown);
    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('mousedown', handlePointerDown);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [selectedOption]);

  const filteredOptions = useMemo(() => {
    const normalized = query.trim().toLowerCase();
    if (!normalized) {
      return options.slice(0, 10);
    }

    return options.filter((option) =>
      (option.searchText ?? `${option.label} ${option.description}`).toLowerCase().includes(normalized)
    );
  }, [options, query]);

  const selectOption = (option: ComboboxOption) => {
    onChange(option);
    setQuery(option.label);
    setIsOpen(false);
  };

  return (
    <div ref={rootRef} className="relative">
      <label className="mb-2 block text-[13px] font-medium text-secondary">{label}</label>
      <div
        className={`field-shell relative rounded-xl transition-all duration-150 ${
          isOpen ? 'scale-[1.01]' : 'scale-100'
        }`}
      >
        <div
          className={`flex h-12 items-center overflow-hidden rounded-xl border bg-bg-quaternary transition-[border-color,box-shadow] duration-150 ${
            error
              ? 'border-danger shadow-[0_0_0_1px_rgba(248,81,73,0.28)]'
              : isOpen
                ? 'border-teal shadow-[0_0_0_2px_rgba(88,166,255,0.18)]'
                : 'border-border-primary'
          }`}
        >
          <MapPin size={16} className="ml-4 shrink-0 text-secondary" />
          <input
            ref={inputRef}
            value={query}
            onChange={(event) => {
              setQuery(event.target.value);
              setIsOpen(true);
            }}
            onFocus={() => {
              if (selectedOption && query === selectedOption.label) {
                setQuery('');
              }
              setIsOpen(true);
            }}
            onKeyDown={(event) => {
              if (event.key === 'Enter' && filteredOptions.length > 0) {
                event.preventDefault();
                selectOption(filteredOptions[0]);
              }
            }}
            placeholder={placeholder}
            className="h-full min-w-0 flex-1 truncate bg-transparent px-3 pr-1 text-sm font-medium text-primary outline-none placeholder:font-normal placeholder:text-faint"
          />
          {selectedOption ? (
            <button
              type="button"
              onClick={() => {
                onChange(null);
                setQuery('');
                setIsOpen(false);
                inputRef.current?.focus();
              }}
              className="mr-1 flex h-9 w-9 shrink-0 items-center justify-center rounded-lg text-secondary transition-colors hover:bg-bg-tertiary hover:text-primary"
              aria-label={`Limpar ${label}`}
            >
              <X size={14} />
            </button>
          ) : null}
          <ChevronDown size={16} className="mr-4 shrink-0 text-secondary" />
        </div>
      </div>

      {error ? <div className="mt-2 text-xs text-danger">{error}</div> : null}

      {isOpen ? (
        <div
          data-state={isOpen ? 'open' : 'closed'}
          className="dropdown-panel mt-2 max-h-72 overflow-y-auto rounded-xl border border-border-primary bg-bg-quaternary shadow-md"
        >
          {filteredOptions.length > 0 ? (
            filteredOptions.map((option) => (
              <button
                key={option.value}
                type="button"
                onMouseDown={(event) => {
                  event.preventDefault();
                  selectOption(option);
                }}
                className="flex w-full items-start gap-3 border-b border-[rgba(58,66,77,0.7)] px-4 py-3 text-left transition-colors last:border-b-0 hover:bg-[rgba(88,166,255,0.12)]"
              >
                <span className="pt-0.5 text-sm">{option.flag ?? ''}</span>
                <div className="min-w-0">
                  <div className="truncate text-sm font-medium text-primary">{option.label}</div>
                  <div className="mt-1 truncate text-xs text-secondary">{option.description}</div>
                </div>
              </button>
            ))
          ) : (
            <div className="px-4 py-3 text-sm text-secondary">Nenhum aeroporto encontrado.</div>
          )}
        </div>
      ) : null}
    </div>
  );
};
