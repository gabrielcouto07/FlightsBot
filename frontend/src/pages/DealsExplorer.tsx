import { useEffect, useState } from 'react';
import { AlertTriangle, PlaneLanding } from 'lucide-react';

import { Deal, SearchResponse, searchAPI } from '../api/search';
import {
  DealCard,
  DealCardSkeleton,
  KpiStrip,
  SearchBar,
  SearchBarValues,
  defaultSearchValues,
} from '../components/flights';
import { Button } from '../components/ui';
import { Layout } from '../components/layout/Layout';

const getDealKey = (deal: Deal) =>
  [
    deal.provider_itinerary_id ?? 'no-provider-id',
    deal.origin,
    deal.destination,
    deal.departure_at,
    deal.airline_iata,
    deal.price,
  ].join(':');

const buildSearchHeadline = (searchMeta: SearchResponse['search_meta'] | null) => {
  if (!searchMeta) {
    return 'Ofertas';
  }

  return `${searchMeta.fly_from} para ${searchMeta.fly_to}`;
};

const buildSearchDescription = (searchMeta: SearchResponse['search_meta'] | null) => {
  if (!searchMeta) {
    return 'Pesquise tarifas em tempo real e abra a melhor opcao de reserva disponivel.';
  }

  if (searchMeta.source === 'demo-curated') {
    return 'As tarifas exibidas sao do modo demonstracao. Os links ainda preservam rota e datas para facilitar a validacao da experiencia.';
  }

  return 'Resultados ao vivo com prioridade para links mais profundos de reserva e contexto de rota preservado.';
};

export const DealsExplorer = () => {
  const [deals, setDeals] = useState<Deal[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchMeta, setSearchMeta] = useState<SearchResponse['search_meta'] | null>(null);
  const [kpis, setKpis] = useState<SearchResponse['kpis'] | null>(null);

  const runSearch = async (filters: SearchBarValues) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await searchAPI.searchDeals(filters);
      setDeals(response.results);
      setSearchMeta(response.search_meta);
      setKpis(response.kpis);
    } catch (searchError) {
      console.error('Falha na busca', searchError);
      setDeals([]);
      setError(searchError instanceof Error ? searchError.message : 'Nao foi possivel concluir a busca.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    void runSearch(defaultSearchValues);
  }, []);

  return (
    <Layout>
      <div className="space-y-6">
        <SearchBar onSearch={runSearch} isLoading={isLoading} />

        <section className="space-y-4">
          <KpiStrip kpis={kpis} resultCount={deals.length} isLoading={isLoading} />

          <div className="flex flex-col gap-2 lg:flex-row lg:items-end lg:justify-between">
            <div>
              <h2 className="text-2xl font-bold text-primary">{buildSearchHeadline(searchMeta)}</h2>
              <p className="mt-1 max-w-3xl text-sm text-secondary">{buildSearchDescription(searchMeta)}</p>
            </div>

            {searchMeta ? (
              <div className="text-sm text-secondary">
                {deals.length} oferta{deals.length === 1 ? '' : 's'} · {searchMeta.actionable_link_rate}% de cobertura profunda
              </div>
            ) : null}
          </div>

          {error ? (
            <div className="flex flex-col items-center justify-center rounded-xl border border-border-primary bg-bg-tertiary px-6 py-12 text-center">
              <AlertTriangle size={48} className="text-warning" />
              <h3 className="mt-4 text-[16px] font-semibold text-primary">Falha na busca</h3>
              <p className="mt-2 max-w-md text-sm text-secondary">{error}</p>
              <Button variant="primary" className="mt-5 rounded-[10px]" onClick={() => void runSearch(defaultSearchValues)}>
                Tentar novamente
              </Button>
            </div>
          ) : isLoading ? (
            <section className="grid gap-4 lg:grid-cols-2">
              {[1, 2, 3, 4].map((item) => (
                <DealCardSkeleton key={item} />
              ))}
            </section>
          ) : deals.length === 0 ? (
            <div className="flex flex-col items-center justify-center rounded-xl border border-border-primary bg-bg-tertiary px-6 py-14 text-center">
              <PlaneLanding size={48} className="text-faint" />
              <h3 className="mt-4 text-[18px] font-semibold text-primary">Nenhuma oferta encontrada</h3>
              <p className="mt-2 text-sm text-secondary">Tente outra origem, destino ou um intervalo maior de datas.</p>
              <Button variant="outline" className="mt-5 rounded-[10px] text-teal" onClick={() => void runSearch(defaultSearchValues)}>
                Limpar filtros
              </Button>
            </div>
          ) : (
            <section className="results-grid grid gap-4 lg:grid-cols-2">
              {deals.map((deal) => (
                <DealCard key={getDealKey(deal)} deal={deal} />
              ))}
            </section>
          )}
        </section>
      </div>
    </Layout>
  );
};
