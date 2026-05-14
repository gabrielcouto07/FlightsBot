import { FormEvent, useEffect, useMemo, useState } from 'react';
import { ArrowRight, Search } from 'lucide-react';

import { AirportOption, SearchParams, searchAPI } from '../../api/search';
import { airportOptions as fallbackAirports } from '../../lib/airports';
import { Button, Combobox, ComboboxOption, DatePicker, TripToggle } from '../ui';

type TripType = 'oneway' | 'roundtrip';

export interface SearchBarValues extends SearchParams {
  fly_from: string;
  fly_to: string;
  date_from: string;
  date_to: string;
  trip_type: TripType;
  max_price?: number;
  nights_min: number;
  nights_max: number;
  adults: number;
  limit: number;
}

interface SearchBarProps {
  onSearch: (filters: SearchBarValues) => void;
  isLoading?: boolean;
}

interface SearchPreset {
  label: string;
  fly_from: string;
  fly_to: string;
  max_price?: number;
}

const formatDateInput = (value: Date) => {
  const year = value.getFullYear();
  const month = `${value.getMonth() + 1}`.padStart(2, '0');
  const day = `${value.getDate()}`.padStart(2, '0');
  return `${year}-${month}-${day}`;
};

const addDays = (dateValue: string, days: number) => {
  const nextDate = new Date(`${dateValue}T00:00:00`);
  nextDate.setDate(nextDate.getDate() + days);
  return formatDateInput(nextDate);
};

const today = formatDateInput(new Date());

export const defaultSearchValues: SearchBarValues = {
  fly_from: 'GRU',
  fly_to: 'anywhere',
  date_from: today,
  date_to: addDays(today, 60),
  trip_type: 'oneway',
  max_price: undefined,
  nights_min: 0,
  nights_max: 0,
  adults: 1,
  limit: 12,
};

const quickPresets: SearchPreset[] = [
  { label: 'Praia no fim de semana', fly_from: 'GRU', fly_to: 'SSA', max_price: 600 },
  { label: 'Sol em Recife', fly_from: 'GRU', fly_to: 'REC', max_price: 700 },
  { label: 'Qualquer lugar ate R$ 800', fly_from: 'GRU', fly_to: 'anywhere', max_price: 800 },
  { label: 'Europa', fly_from: 'GRU', fly_to: 'LIS', max_price: 3200 },
  { label: 'Miami', fly_from: 'GRU', fly_to: 'MIA', max_price: 3400 },
];

const mapFallbackAirports = fallbackAirports.map((airport) => ({
  ...airport,
  flag: airport.country === 'Brazil' ? '🇧🇷' : '',
}));

const sortAirports = (options: AirportOption[]) =>
  [...options].sort((left, right) => {
    const leftBrazil = left.country === 'Brazil';
    const rightBrazil = right.country === 'Brazil';

    if (leftBrazil !== rightBrazil) {
      return leftBrazil ? -1 : 1;
    }

    return left.city.localeCompare(right.city, 'pt-BR');
  });

const buildAirportOption = (airport: AirportOption): ComboboxOption => ({
  value: airport.code,
  label: `${airport.flag ? `${airport.flag} ` : ''}${airport.code} - ${airport.city}`,
  description: `${airport.city}, ${airport.country}`,
  flag: airport.flag,
  searchText: `${airport.code} ${airport.city} ${airport.country}`,
});

export const SearchBar = ({ onSearch, isLoading = false }: SearchBarProps) => {
  const [values, setValues] = useState<SearchBarValues>(defaultSearchValues);
  const [airports, setAirports] = useState<AirportOption[]>(sortAirports(mapFallbackAirports));
  const [errors, setErrors] = useState<{ fly_from?: string }>({});

  useEffect(() => {
    const loadAirports = async () => {
      try {
        const response = await searchAPI.listAirports();
        if (response.length > 0) {
          setAirports(sortAirports(response));
        }
      } catch (error) {
        console.error('Falha ao carregar aeroportos, usando lista local.', error);
      }
    };

    void loadAirports();
  }, []);

  const originOptions = useMemo(() => airports.map(buildAirportOption), [airports]);
  const destinationOptions = useMemo(
    () => [
      {
        value: 'anywhere',
        label: 'Qualquer lugar',
        description: 'Destino flexivel',
        searchText: 'qualquer lugar anywhere destino flexivel',
      },
      ...airports.map(buildAirportOption),
    ],
    [airports]
  );

  const update = (patch: Partial<SearchBarValues>) => {
    setValues((current) => ({ ...current, ...patch }));
  };

  const validate = () => {
    const nextErrors: { fly_from?: string } = {};
    if (!values.fly_from) {
      nextErrors.fly_from = 'Selecione um aeroporto de origem.';
    }

    setErrors(nextErrors);
    return Object.keys(nextErrors).length === 0;
  };

  const submitValues = (nextValues: SearchBarValues) => {
    if (!nextValues.fly_from) {
      setErrors({ fly_from: 'Selecione um aeroporto de origem.' });
      return;
    }

    const computedDateTo =
      nextValues.trip_type === 'roundtrip'
        ? nextValues.date_to
        : addDays(nextValues.date_from, 60);

    const nights =
      nextValues.trip_type === 'roundtrip'
        ? Math.max(
            1,
            Math.round(
              (new Date(`${computedDateTo}T00:00:00`).getTime() -
                new Date(`${nextValues.date_from}T00:00:00`).getTime()) /
                (1000 * 60 * 60 * 24)
            )
          )
        : 0;

    onSearch({
      ...nextValues,
      fly_to: nextValues.fly_to || 'anywhere',
      date_to: computedDateTo,
      max_price: nextValues.max_price || undefined,
      nights_min: nights,
      nights_max: nights,
    });
  };

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    if (!validate()) {
      return;
    }

    submitValues(values);
  };

  const applyPreset = (preset: SearchPreset) => {
    const nextValues: SearchBarValues = {
      ...values,
      fly_from: preset.fly_from,
      fly_to: preset.fly_to,
      max_price: preset.max_price,
    };
    setValues(nextValues);
    setErrors({});
    submitValues(nextValues);
  };

  return (
    <div className="mx-auto w-full max-w-[900px]">
      <form
        onSubmit={handleSubmit}
        className="rounded-2xl border border-border-primary bg-bg-tertiary p-5 shadow-sm lg:p-6"
      >
        <div className="space-y-4">
          <div className="grid gap-4 xl:grid-cols-[220px_minmax(0,1fr)_32px_minmax(0,1fr)] xl:items-end">
            <div className="min-w-0">
              <label className="mb-2 block text-[13px] font-medium text-secondary">Tipo de viagem</label>
              <TripToggle
                value={values.trip_type}
                onChange={(trip_type) =>
                  update({
                    trip_type,
                    date_to:
                      trip_type === 'roundtrip'
                        ? values.date_to <= values.date_from
                          ? addDays(values.date_from, 7)
                          : values.date_to
                        : values.date_to,
                  })
                }
              />
            </div>

            <Combobox
              label="Origem"
              value={values.fly_from}
              options={originOptions}
              placeholder="Escolha a origem"
              onChange={(option) => {
                update({ fly_from: option?.value ?? '' });
                if (errors.fly_from) {
                  setErrors({});
                }
              }}
              error={errors.fly_from}
            />

            <div className="hidden h-12 items-center justify-center text-secondary xl:flex">
              <ArrowRight size={18} />
            </div>

            <Combobox
              label="Destino"
              value={values.fly_to}
              options={destinationOptions}
              placeholder="Escolha o destino"
              onChange={(option) => update({ fly_to: option?.value ?? '' })}
            />
          </div>

          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-[minmax(0,1fr)_minmax(0,1fr)_124px_148px_180px] xl:items-end">
            <DatePicker
              label="Data de ida"
              value={values.date_from}
              onChange={(date_from) =>
                update({
                  date_from,
                  date_to:
                    values.trip_type === 'roundtrip'
                      ? values.date_to <= date_from
                        ? addDays(date_from, 7)
                        : values.date_to
                      : values.date_to,
                })
              }
              minDate={today}
              rangeStart={values.trip_type === 'roundtrip' ? values.date_from : undefined}
              rangeEnd={values.trip_type === 'roundtrip' ? values.date_to : undefined}
            />

            <DatePicker
              label="Data de volta"
              value={values.trip_type === 'roundtrip' ? values.date_to : undefined}
              onChange={(date_to) => update({ date_to })}
              minDate={values.date_from}
              rangeStart={values.trip_type === 'roundtrip' ? values.date_from : undefined}
              rangeEnd={values.trip_type === 'roundtrip' ? values.date_to : undefined}
              disabled={values.trip_type === 'oneway'}
            />

            <div>
              <label className="mb-2 block text-[13px] font-medium text-secondary">Adultos</label>
              <div className="field-shell flex h-12 items-center rounded-xl border border-border-primary bg-bg-quaternary px-2">
                <button
                  type="button"
                  onClick={() => update({ adults: Math.max(1, values.adults - 1) })}
                  className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-secondary transition-colors hover:bg-bg-tertiary hover:text-primary"
                  aria-label="Diminuir adultos"
                >
                  -
                </button>
                <span className="min-w-0 flex-1 text-center text-sm font-semibold text-primary">{values.adults}</span>
                <button
                  type="button"
                  onClick={() => update({ adults: Math.min(9, values.adults + 1) })}
                  className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-secondary transition-colors hover:bg-bg-tertiary hover:text-primary"
                  aria-label="Aumentar adultos"
                >
                  +
                </button>
              </div>
            </div>

            <div>
              <label className="mb-2 block text-[13px] font-medium text-secondary">Preco maximo</label>
              <div className="field-shell relative">
                <span className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-sm font-medium text-secondary">
                  R$
                </span>
                <input
                  type="number"
                  min="0"
                  value={values.max_price ?? ''}
                  onChange={(event) =>
                    update({ max_price: event.target.value ? Number(event.target.value) : undefined })
                  }
                  placeholder="Qualquer preco"
                  className="h-12 w-full rounded-xl border border-border-primary bg-bg-quaternary pl-12 pr-4 text-sm font-medium text-primary outline-none transition-[border-color,box-shadow] duration-150 placeholder:font-normal placeholder:text-faint focus:border-teal focus:shadow-[0_0_0_2px_rgba(88,166,255,0.18)]"
                />
              </div>
            </div>

            <Button
              type="submit"
              variant="primary"
              isLoading={isLoading}
              className="h-12 w-full rounded-[10px] font-semibold"
            >
              <Search size={16} />
              {isLoading ? 'Buscando...' : 'Buscar voos'}
            </Button>
          </div>
        </div>
      </form>

      <div className="mt-4 flex flex-wrap gap-2">
        {quickPresets.map((preset) => (
          <button
            key={preset.label}
            type="button"
            onClick={() => applyPreset(preset)}
            className="rounded-full border border-[rgba(88,166,255,0.38)] bg-bg-secondary px-3 py-1.5 text-sm font-medium text-primary transition-colors hover:bg-[rgba(88,166,255,0.14)]"
          >
            {preset.label}
          </button>
        ))}
      </div>
    </div>
  );
};
