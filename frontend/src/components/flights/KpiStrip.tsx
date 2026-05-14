import { SearchResponse } from '../../api/search';

interface KpiStripProps {
  kpis: SearchResponse['kpis'] | null;
  resultCount: number;
  isLoading?: boolean;
}

const loadingItems = [1, 2, 3, 4];

export const KpiStrip = ({ kpis, resultCount, isLoading = false }: KpiStripProps) => {
  const items = kpis
    ? [
        {
          label: 'Escaneado hoje',
          value: kpis.total_scanned_24h.toLocaleString('pt-BR'),
          meta: `${resultCount} tarifas na tela`,
        },
        {
          label: 'Alertas ativos',
          value: kpis.active_alerts.toLocaleString('pt-BR'),
          meta: 'monitoramento em execucao',
        },
        {
          label: 'CPM medio',
          value: kpis.average_cpm ? kpis.average_cpm.toFixed(3) : 'n/a',
          meta: 'mix atual de resultados',
        },
        {
          label: 'Melhor economia',
          value: `${kpis.top_saving_percent.toFixed(1)}%`,
          meta: 'vs media de 30 dias',
        },
      ]
    : [];

  if (isLoading && !kpis) {
    return (
      <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        {loadingItems.map((item) => (
          <div key={item} className="h-20 rounded-xl border border-border-primary bg-bg-tertiary animate-surface-shimmer" />
        ))}
      </section>
    );
  }

  return (
    <section className="overflow-hidden rounded-xl border border-border-primary bg-bg-tertiary">
      <div className="grid md:grid-cols-2 xl:grid-cols-4">
        {items.map((item, index) => (
          <div
            key={item.label}
            className={`min-h-20 px-4 py-4 ${index > 0 ? 'border-t border-border-primary md:border-t-0 xl:border-l' : ''}`}
          >
            <div className="text-[11px] font-medium uppercase tracking-[0.06em] text-secondary">{item.label}</div>
            <div className="mt-2 text-[22px] font-bold leading-none text-primary">{item.value}</div>
            <div className="mt-2 text-[11px] text-secondary">{item.meta}</div>
          </div>
        ))}
      </div>
    </section>
  );
};
