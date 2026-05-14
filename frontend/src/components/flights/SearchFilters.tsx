import { useState } from 'react';
import { Input, Select, Button } from '../ui';
import { Card } from '../ui';
import { Search } from 'lucide-react';

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
  limit: number;
}

const MAJOR_AIRPORTS = [
  { value: 'GRU', label: 'São Paulo (GRU)' },
  { value: 'SDU', label: 'Rio de Janeiro (SDU)' },
  { value: 'MIA', label: 'Miami (MIA)' },
  { value: 'LIS', label: 'Lisbon (LIS)' },
  { value: 'BCN', label: 'Barcelona (BCN)' },
  { value: 'NYC', label: 'New York (NYC)' },
  { value: 'LHR', label: 'London (LHR)' },
];

export const SearchFilters = ({ onSearch, isLoading }: SearchFiltersProps) => {
  const [filters, setFilters] = useState<SearchFiltersType>({
    fly_from: 'GRU',
    fly_to: 'anywhere',
    date_from: new Date().toISOString().split('T')[0],
    date_to: new Date(Date.now() + 60 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    max_price: 5000,
    trip_type: 'oneway',
    adults: 1,
    limit: 20,
  });

  const handleChange = (field: keyof SearchFiltersType, value: any) => {
    setFilters({ ...filters, [field]: value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(filters);
  };

  return (
    <Card className="space-y-4">
      <h3 className="text-lg font-semibold">Search Flights</h3>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <Select
            label="From"
            options={MAJOR_AIRPORTS}
            value={filters.fly_from}
            onChange={(e) => handleChange('fly_from', e.target.value)}
          />
          <Select
            label="To"
            options={[
              { value: 'anywhere', label: 'Anywhere' },
              ...MAJOR_AIRPORTS,
            ]}
            value={filters.fly_to}
            onChange={(e) => handleChange('fly_to', e.target.value)}
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <Input
            label="Depart"
            type="date"
            value={filters.date_from}
            onChange={(e) => handleChange('date_from', e.target.value)}
          />
          <Input
            label="Return"
            type="date"
            value={filters.date_to}
            onChange={(e) => handleChange('date_to', e.target.value)}
          />
        </div>

        <div className="grid grid-cols-3 gap-4">
          <Select
            label="Trip Type"
            options={[
              { value: 'oneway', label: 'One-way' },
              { value: 'roundtrip', label: 'Roundtrip' },
            ]}
            value={filters.trip_type}
            onChange={(e) => handleChange('trip_type', e.target.value as 'oneway' | 'roundtrip')}
          />
          <Input
            label="Passengers"
            type="number"
            min="1"
            max="9"
            value={filters.adults}
            onChange={(e) => handleChange('adults', parseInt(e.target.value))}
          />
          <Input
            label="Max Price"
            type="number"
            value={filters.max_price}
            onChange={(e) => handleChange('max_price', parseFloat(e.target.value))}
          />
        </div>

        <Button type="submit" variant="primary" size="md" isLoading={isLoading} className="w-full">
          <Search size={18} />
          Search Deals
        </Button>
      </form>
    </Card>
  );
};
