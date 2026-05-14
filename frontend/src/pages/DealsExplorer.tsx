import { useState } from 'react';
import { SearchFilters, SearchFiltersType } from '../components/flights/SearchFilters';
import { DealCard, DealCardSkeleton } from '../components/flights';
import { MatchPreviewPanel } from '../components/flights/MatchPreviewPanel';
import { searchAPI, Deal } from '../api/search';
import { EmptyState } from '../components/ui';
import { Layout } from '../components/layout/Layout';

export const DealsExplorer = () => {
  const [deals, setDeals] = useState<Deal[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedDeal, setSelectedDeal] = useState<Deal | null>(null);

  const handleSearch = async (filters: SearchFiltersType) => {
    setIsLoading(true);
    try {
      const response = await searchAPI.searchDeals({
        fly_from: filters.fly_from,
        fly_to: filters.fly_to === 'anywhere' ? 'anywhere' : filters.fly_to,
        date_from: filters.date_from,
        date_to: filters.date_to,
        max_price: filters.max_price,
        trip_type: filters.trip_type,
        limit: filters.limit,
      });
      setDeals(response.results);
    } catch (error) {
      console.error('Search error:', error);
      setDeals([]);
    } finally {
      setIsLoading(false);
    }
  };

  const dealCount = deals.length;
  const matchedCount = deals.filter((d) => d.is_deal).length;

  return (
    <Layout>
      <div className="p-6 max-w-7xl mx-auto space-y-6">
        {/* Main Layout: Search + Preview */}
        <div className="grid grid-cols-3 gap-6">
          {/* Left: Search Filters */}
          <div className="col-span-1">
            <SearchFilters onSearch={handleSearch} isLoading={isLoading} />
          </div>

          {/* Center: Deal List */}
          <div className="col-span-2">
            <div className="space-y-4">
              {dealCount > 0 && (
                <div className="text-sm text-secondary">
                  Found {dealCount} flights • {matchedCount} deals
                </div>
              )}

              {isLoading ? (
                <div className="space-y-3">
                  {[1, 2, 3, 4, 5].map((i) => (
                    <DealCardSkeleton key={i} />
                  ))}
                </div>
              ) : dealCount === 0 ? (
                <EmptyState
                  icon="✈️"
                  title="No deals found"
                  description="Search for flights to discover amazing deals"
                />
              ) : (
                <div className="space-y-3">
                  {deals.map((deal) => (
                    <DealCard
                      key={`${deal.origin}${deal.destination}${deal.departure_at}`}
                      deal={deal}
                      onSelect={setSelectedDeal}
                    />
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Preview Panel for Selected Deal */}
        {selectedDeal && (
          <div className="mt-8 p-6 bg-bg-secondary border border-border-primary rounded-lg">
            <h2 className="text-2xl font-bold mb-4">Selected Deal</h2>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-tertiary">Route</p>
                <p className="text-lg font-semibold">
                  {selectedDeal.origin} → {selectedDeal.destination}
                </p>
              </div>
              <div>
                <p className="text-sm text-tertiary">Price</p>
                <p className="text-2xl font-bold text-teal">
                  R$ {selectedDeal.price.toLocaleString('pt-BR')}
                </p>
              </div>
              <div>
                <p className="text-sm text-tertiary">Airline</p>
                <p className="font-semibold">{selectedDeal.airline}</p>
              </div>
              <div>
                <p className="text-sm text-tertiary">Duration</p>
                <p className="font-semibold">
                  {Math.floor(selectedDeal.duration_minutes / 60)}h {selectedDeal.duration_minutes % 60}m
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
};
