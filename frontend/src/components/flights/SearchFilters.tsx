import { FormEvent, useEffect, useMemo, useRef, useState } from 'react';
import { Filter, Search, SlidersHorizontal } from 'lucide-react';

import { Button, Input, Select, AutocompleteInput } from '../ui';
import {
  airlinePresets,
  airportOptions,
  budgetPresets,
  featuredRoutes,
  popularDestinations,
  popularOrigins,
} from '../../lib/airports';

interface SearchFiltersProps {
  onSearch: (filters: SearchFiltersType) => void;
  isLoading?: boolean;
}

export interface SearchFiltersType {
  fly_from: string;
  fly_to: string;
  date_from: string;
  date_to: string;
  max_price: number;
  trip_type: 'oneway' | 'roundtrip';
  adults: number;
  airline: string;
  limit: number;
}

export const defaultSearchFilters: SearchFiltersType = {
  fly_from: 'GRU',
  fly_to: 'anywhere',
  date_from: new Date().toISOString().split('T')[0],
  date_to: new Date(Date.now() + 21 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
  max_price: 900,
  trip_type: 'oneway',
  adults: 1,
  airline: 'ALL',
  limit: 12,
};

const airportLookup = new Map(
  airportOptions.flatMap((airport) => [
    [airport.code.toUpperCase(), airport.code],
    [`${airport.city} (${airport.code})`.toUpperCase(), airport.code],
  ])
);

const parseAirportValue = (value: string) => {
  const normalized = value.trim().toUpperCase();
  if (!normalized) {
    return '';
  }

  const explicitCode = normalized.match(/\(([A-Z]{3})\)$/);
  if (explicitCode) {
    return explicitCode[1];
  }

  if (normalized === 'ANYWHERE') {
    return 'anywhere';
  }

  return airportLookup.get(normalized) ?? normalized.slice(0, 3);
};

export const SearchFilters = ({ onSearch, isLoading = false }: SearchFiltersProps) => {
  const [filters, setFilters] = useState<SearchFiltersType>(defaultSearchFilters);
  const [originInput, setOriginInput] = useState(defaultSearchFilters.fly_from);
  const [destinationInput, setDestinationInput] = useState(defaultSearchFilters.fly_to.toUpperCase());
  const [activeAutocomplete, setActiveAutocomplete] = useState<'origin' | 'destination' | null>(null);
  const formRef = useRef<HTMLFormElement>(null);

  const airportHints = useMemo(
    () =>
      airportOptions.map((airport) => `${airport.city} (${airport.code})`),
    []
  );

  const autocompleteOptions = useMemo(() => {
    if (!activeAutocomplete) return [];

    const baseOptions = activeAutocomplete === 'destination' ? ['Anywhere', ...airportHints] : airportHints;
    const rawValue = activeAutocomplete === 'origin' ? originInput : destinationInput;
    const query = rawValue.trim().toUpperCase().replace(/^🇧🇷\s*/, '');
    const expandedQuery = query
      .replace(/^ANYWHERE$/, 'ANYWHERE')
      .replace(/^([A-Z]{3})$/, (_, code) => code)
      .trim();

    if (!expandedQuery) {
      return baseOptions.slice(0, 8);
    }

    return baseOptions.filter((option) => option.toUpperCase().includes(expandedQuery)).slice(0, 8);
  }, [activeAutocomplete, airportHints, originInput, destinationInput]);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (formRef.current && !formRef.current.contains(event.target as Node)) {
        setActiveAutocomplete(null);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const update = (patch: Partial<SearchFiltersType>) => {
    setFilters((current) => ({ ...current, ...patch }));
  };

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    onSearch({
      ...filters,
      fly_from: parseAirportValue(originInput),
      fly_to: parseAirportValue(destinationInput),
    });
  };

  const applyScenario = (index: number) => {
    const route = featuredRoutes[index % featuredRoutes.length];
    const next = {
      ...filters,
      fly_from: route.fly_from,
      fly_to: route.fly_to,
      max_price: route.max_price,
    };
    setFilters(next);
    setOriginInput(route.fly_from);
    setDestinationInput(route.fly_to.toUpperCase());
    onSearch(next);
  };

  return (
    <div className="sticky top-[5.1rem] z-30 space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-border-primary bg-gradient-to-r from-bg-secondary/80 to-bg-tertiary/50 px-4 py-3 backdrop-blur-md">
        <div className="flex items-center gap-2.5 text-xs font-600 uppercase tracking-wider text-text-tertiary">
          <Filter size={16} className="text-accent" strokeWidth={2} />
          Filtros Rápidos
        </div>
        <div className="flex flex-wrap gap-2">
          {featuredRoutes.map((route, index) => (
            <button
              key={route.label}
              type="button"
              onClick={() => applyScenario(index)}
              className="rounded-lg border border-border-primary bg-bg-tertiary px-3 py-1.5 text-xs font-500 text-text-secondary transition-all duration-200 hover:border-accent/50 hover:bg-accent/10 hover:text-accent"
            >
              {route.label}
            </button>
          ))}
        </div>
      </div>

      <form
        ref={formRef}
        onSubmit={handleSubmit}
        className="rounded-xl border border-border-primary bg-gradient-to-br from-bg-secondary/40 to-bg-tertiary/40 p-5 backdrop-blur-md shadow-lg"
      >
        <div className="grid gap-3 xl:grid-cols-2">
          <AutocompleteInput
            label="Origin"
            value={originInput}
            placeholder="GRU or Sao Paulo"
            onChange={(value) => {
              setOriginInput(value);
              setActiveAutocomplete('origin');
            }}
            onFocus={() => setActiveAutocomplete('origin')}
          />
          <AutocompleteInput
            label="Destination"
            value={destinationInput}
            placeholder="Anywhere or MIA"
            onChange={(value) => {
              setDestinationInput(value);
              setActiveAutocomplete('destination');
            }}
            onFocus={() => setActiveAutocomplete('destination')}
          />
        </div>

        {activeAutocomplete && autocompleteOptions.length > 0 && (
          <div className="w-full rounded-xl border border-accent/30 bg-gradient-to-b from-bg-secondary to-bg-tertiary shadow-lg overflow-hidden">
            <div className="flex items-center justify-between border-b border-border-primary/40 px-4 py-3">
              <div className="text-xs font-600 uppercase tracking-wider text-text-tertiary">
                {activeAutocomplete === 'origin' ? 'Sugestões de origem' : 'Sugestões de destino'}
              </div>
              <button
                type="button"
                onClick={() => setActiveAutocomplete(null)}
                className="text-xs font-500 text-text-muted transition-colors hover:text-text-primary"
              >
                Fechar
              </button>
            </div>
            <div className="max-h-[240px] overflow-y-auto">
              {autocompleteOptions.map((option, idx) => (
                <button
                  key={`${option}-${idx}`}
                  type="button"
                  onClick={() => {
                    if (activeAutocomplete === 'origin') {
                      setOriginInput(option);
                    } else {
                      setDestinationInput(option);
                    }
                    setActiveAutocomplete(null);
                  }}
                  className="flex w-full items-center justify-between border-b border-border-primary/30 px-4 py-2.5 text-left text-sm text-text-primary transition-colors duration-150 hover:bg-accent/15 hover:text-accent last:border-b-0"
                >
                  <span>{option}</span>
                  <span className="text-xs text-text-muted">→</span>
                </button>
              ))}
            </div>
          </div>
        )}

        <div className="grid gap-3 xl:grid-cols-[0.9fr_0.9fr_0.85fr_0.8fr_0.7fr]">
          <Input
            label="Window Start"
            type="date"
            value={filters.date_from}
            onChange={(event) => update({ date_from: event.target.value })}
          />
          <Input
            label="Window End"
            type="date"
            value={filters.date_to}
            onChange={(event) => update({ date_to: event.target.value })}
          />
          <Input
            label="Max Price"
            type="number"
            min="100"
            value={filters.max_price}
            onChange={(event) => update({ max_price: Number(event.target.value || 0) })}
            helpText={budgetPresets.map((value) => `R$${value}`).join(' / ')}
          />
          <Select
            label="Airline"
            value={filters.airline}
            options={airlinePresets.map((code) => ({
              value: code,
              label: code === 'ALL' ? 'All carriers' : code,
            }))}
            onChange={(event) => update({ airline: event.target.value })}
          />
          <Input
            label="Passengers"
            type="number"
            min="1"
            max="9"
            value={filters.adults}
            onChange={(event) => update({ adults: Number(event.target.value || 1) })}
          />
        </div>

        <div className="flex items-end gap-2">
          <Button type="submit" variant="primary" size="md" isLoading={isLoading} className="w-full">
            <Search size={16} strokeWidth={2} />
            Search
          </Button>
          <Button
            type="button"
            variant="ghost"
            size="md"
            className="px-4"
            onClick={() => {
              setFilters(defaultSearchFilters);
              setOriginInput(defaultSearchFilters.fly_from);
              setDestinationInput(defaultSearchFilters.fly_to.toUpperCase());
              setActiveAutocomplete(null);
              onSearch(defaultSearchFilters);
            }}
          >
            <SlidersHorizontal size={16} strokeWidth={2} />
          </Button>
        </div>
      </form>

      <div className="flex flex-wrap gap-2">
        {popularOrigins.map((origin) => (
          <button
            key={origin}
            type="button"
            onClick={() => setOriginInput(origin)}
            className="rounded-lg border border-border-primary bg-bg-secondary px-3 py-1.5 text-xs font-500 text-text-secondary transition-all duration-200 hover:border-accent/50 hover:bg-accent/10 hover:text-accent"
          >
            {origin}
          </button>
        ))}
        {popularDestinations.map((destination) => (
          <button
            key={destination}
            type="button"
            onClick={() => setDestinationInput(destination.toUpperCase())}
            className="rounded-lg border border-border-primary bg-bg-secondary px-3 py-1.5 text-xs font-500 text-text-secondary transition-all duration-200 hover:border-accent/50 hover:bg-accent/10 hover:text-accent"
          >
            {destination.toUpperCase()}
          </button>
        ))}
      </div>
    </div>
  );
};
