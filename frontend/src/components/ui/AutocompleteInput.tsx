import { useState, useEffect, useRef, useLayoutEffect } from 'react';
import { createPortal } from 'react-dom';
import { ChevronDown } from 'lucide-react';

interface AutocompleteInputProps {
  label?: string;
  value: string;
  onChange: (value: string) => void;
  options: string[];
  placeholder?: string;
  error?: string;
}

export const AutocompleteInput = ({
  label,
  value,
  onChange,
  options,
  placeholder = '',
  error,
}: AutocompleteInputProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const [filteredOptions, setFilteredOptions] = useState<string[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const [coords, setCoords] = useState<{ top: number; left: number; width: number }>({ top: 0, left: 0, width: 0 });

  useEffect(() => {
    if (value.trim()) {
      const normalized = value.toUpperCase();
      const filtered = options.filter((opt) => opt.toUpperCase().includes(normalized)).slice(0, 8);
      setFilteredOptions(filtered);
      setIsOpen(filtered.length > 0);
    } else {
      setFilteredOptions(options.slice(0, 8));
      setIsOpen(false);
    }
  }, [value, options]);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      const target = e.target as Node;
      const clickedInsideInput = inputRef.current && inputRef.current.contains(target as Node);
      const clickedInsideDropdown = dropdownRef.current && dropdownRef.current.contains(target as Node);
      if (!clickedInsideInput && !clickedInsideDropdown) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const updateCoords = () => {
    const el = inputRef.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    setCoords({ top: rect.bottom + window.scrollY, left: rect.left + window.scrollX, width: rect.width });
  };

  useLayoutEffect(() => {
    if (isOpen) {
      updateCoords();
      window.addEventListener('resize', updateCoords);
      window.addEventListener('scroll', updateCoords, true);
    }
    return () => {
      window.removeEventListener('resize', updateCoords);
      window.removeEventListener('scroll', updateCoords, true);
    };
  }, [isOpen, value, filteredOptions]);


  const handleSelect = (option: string) => {
    onChange(option);
    setIsOpen(false);
    inputRef.current?.blur();
  };

  const handleFocus = () => {
    if (filteredOptions.length > 0) {
      setIsOpen(true);
    }
  };

  return (
    <div className="relative flex flex-col gap-2" ref={dropdownRef}>
      {label && <label className="text-sm font-600 text-text-primary">{label}</label>}
      <div className="relative">
        <input
          ref={inputRef}
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onFocus={handleFocus}
          placeholder={placeholder}
          className={`w-full h-11 rounded-lg border border-border-primary bg-bg-tertiary px-4 text-text-primary placeholder:text-text-muted transition-all duration-200 focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/20 pr-10 ${
            error ? 'border-danger/60 focus:ring-danger/20' : ''
          }`}
        />
        <ChevronDown
          size={16}
          className={`absolute right-3 top-1/2 -translate-y-1/2 text-text-muted pointer-events-none transition-transform ${
            isOpen ? 'rotate-180' : ''
          }`}
        />
      </div>

      {isOpen && filteredOptions.length > 0 &&
        typeof document !== 'undefined' &&
        createPortal(
          <div
            ref={dropdownRef}
            style={{ position: 'absolute', top: coords.top, left: coords.left, width: coords.width }}
            className="rounded-lg border border-accent/30 bg-gradient-to-b from-bg-secondary to-bg-tertiary shadow-lg overflow-hidden"
          >
            <div className="max-h-[240px] overflow-y-auto">
              {filteredOptions.map((option, idx) => (
                <button
                  key={`${option}-${idx}`}
                  type="button"
                  onClick={() => handleSelect(option)}
                  className="w-full px-4 py-2.5 text-left text-sm text-text-primary hover:bg-accent/15 hover:text-accent transition-colors duration-150 border-b border-border-primary/30 last:border-b-0 flex items-center justify-between group"
                >
                  <span>{option}</span>
                  <span className="text-text-muted group-hover:text-accent text-xs opacity-0 group-hover:opacity-100 transition-opacity">
                    →
                  </span>
                </button>
              ))}
            </div>
          </div>,
          document.body
        )}

      {error && <span className="text-xs text-danger font-500">{error}</span>}
    </div>
  );
};
