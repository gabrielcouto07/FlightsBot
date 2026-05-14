import { useEffect, useMemo, useState } from 'react';
import { ArrowDown, ArrowRight, Star, Zap } from 'lucide-react';
import { differenceInSeconds, format, formatDistanceToNow } from 'date-fns';
import { ptBR } from 'date-fns/locale';

import { Deal } from '../../api/search';
import { Button, Sparkline } from '../ui';

interface DealCardProps {
  deal: Deal;
}

const formatCurrency = (value: number) =>
  `R$ ${value.toLocaleString('pt-BR', { maximumFractionDigits: 0 })}`;

const formatDuration = (minutes: number) => {
  const hours = Math.floor(minutes / 60);
  const remainder = minutes % 60;
  return `${hours}h ${remainder}m`;
};

const formatLastSeen = (value: string) => {
  const lastSeenAt = new Date(value);

  if (Number.isNaN(lastSeenAt.getTime())) {
    return 'agora';
  }

  const secondsAgo = Math.abs(differenceInSeconds(new Date(), lastSeenAt));
  if (secondsAgo < 60) {
    return 'agora';
  }

  return formatDistanceToNow(lastSeenAt, { locale: ptBR, addSuffix: true });
};

const getBadge = (deal: Deal) => {
  if ((deal.deal_badge ?? '').toLowerCase().includes('error')) {
    return {
      icon: <Zap size={12} />,
      label: 'Tarifa erro',
      tone: 'text-gold',
    };
  }

  if (deal.price <= deal.historical_low_price) {
    return {
      icon: <Star size={12} />,
      label: 'Menor preco em 45 dias',
      tone: 'text-info',
    };
  }

  if (deal.savings_percent >= 10) {
    return {
      icon: <ArrowDown size={12} />,
      label: `${Math.round(deal.savings_percent)}% abaixo da media`,
      tone: 'text-success',
    };
  }

  return {
    icon: null,
    label: 'Melhor opcao agora',
    tone: 'text-secondary',
  };
};

export const DealCard = ({ deal }: DealCardProps) => {
  const [logoFailed, setLogoFailed] = useState(false);

  useEffect(() => {
    if (!deal.deeplink_url) {
      console.warn('Oferta sem deeplink_url', {
        origin: deal.origin,
        destination: deal.destination,
        airline: deal.airline,
      });
    }
  }, [deal.airline, deal.deeplink_url, deal.destination, deal.origin]);

  const departureDate = new Date(deal.departure_at);
  const badge = useMemo(() => getBadge(deal), [deal]);
  const footerSource =
    deal.booking_source === 'direct_airline'
      ? `direto: ${deal.provider_name}`
      : deal.booking_source === 'kiwi'
        ? 'via kiwi.com'
        : 'via Google Flights';
  const sparklineTone =
    deal.trend_change_7d < 0 ? 'text-success' : deal.trend_change_7d > 0 ? 'text-warning' : 'text-secondary';
  const stopTone =
    deal.stops === 0 ? 'text-success' : deal.stops === 1 ? 'text-warning' : 'text-danger';
  const stopLabel =
    deal.stops === 0 ? 'Direto' : `${deal.stops} escala${deal.stops > 1 ? 's' : ''}`;

  return (
    <article className="w-full rounded-xl border border-border-primary bg-gradient-to-br from-bg-secondary to-bg-tertiary p-5 transition-all duration-300 hover:-translate-y-0.5 hover:border-accent/50 hover:shadow-lg hover:shadow-accent/10">
      <div className="grid gap-5 lg:grid-cols-[auto_minmax(0,1fr)_auto] lg:items-center">
        <div className="flex min-w-0 items-center gap-3 lg:items-center">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-bg-quaternary border border-border-primary text-xs font-600 text-text-primary">
            {!logoFailed && deal.airline_logo_url ? (
              <img
                src={deal.airline_logo_url}
                alt={deal.airline}
                className="h-8 w-8 object-contain"
                onError={() => setLogoFailed(true)}
              />
            ) : (
              <span>{deal.airline_iata || deal.provider_code || 'AIR'}</span>
            )}
          </div>

          <div className="min-w-0">
            <div className="truncate text-sm font-600 text-text-primary">{deal.airline}</div>
            <div className="mt-1 truncate text-xs text-text-secondary">{deal.provider_code || deal.airline_iata}</div>
          </div>
        </div>

        <div className="min-w-0 text-center lg:text-left">
          <div className="flex items-center justify-center gap-2 text-lg font-700 text-text-primary lg:justify-start">
            <span>{deal.origin}</span>
            <ArrowRight size={16} className="shrink-0 text-text-secondary" strokeWidth={2.5} />
            <span>{deal.destination}</span>
          </div>
          <div className="mt-1 truncate text-xs text-text-secondary">
            {deal.origin_city} <span className="text-text-muted">·</span> {deal.destination_city}
          </div>
          <div className="mt-3 text-sm text-text-secondary">
            {format(departureDate, "EEE, d 'de' MMM", { locale: ptBR })}
          </div>
          <div className="mt-1 text-sm">
            <span className="text-text-secondary">{formatDuration(deal.duration_minutes)} · </span>
            <span className={stopTone}>{stopLabel}</span>
          </div>
        </div>

        <div className="min-w-0 text-center lg:text-right">
          <div className="text-2xl font-700 text-accent">{formatCurrency(deal.price)}</div>
          <div className={`mt-2 inline-flex max-w-full items-center gap-1.5 text-xs font-500 ${badge.tone}`}>
            {badge.icon}
            <span className="truncate">{badge.label}</span>
          </div>
          <div className={`mt-3 flex justify-center ${sparklineTone} lg:justify-end`}>
            <Sparkline values={deal.price_history_7d} />
          </div>
          <a href={deal.deeplink_url} target="_blank" rel="noopener noreferrer" className="mt-4 block">
            <Button variant="primary" className="h-9 w-full rounded-lg font-600 lg:ml-auto lg:max-w-[190px]">
              Reservar
            </Button>
          </a>
          <div
            className={`mt-2 text-xs ${deal.booking_source === 'direct_airline' ? 'text-success' : 'text-text-muted'}`}
          >
            {footerSource} · {formatLastSeen(deal.fare_last_seen_at)}
          </div>
        </div>
      </div>
    </article>
  );
};
