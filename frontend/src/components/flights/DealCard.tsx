import { Deal } from '../../api/search';
import { Card, Badge } from '../ui';
import { Plane, Clock, MapPin, TrendingDown } from 'lucide-react';
import { format } from 'date-fns';

interface DealCardProps {
  deal: Deal;
  onSelect?: (deal: Deal) => void;
}

export const DealCard = ({ deal, onSelect }: DealCardProps) => {
  const formatPrice = (price: number) => {
    return `R$ ${price.toLocaleString('pt-BR', { maximumFractionDigits: 0 })}`;
  };

  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}m`;
  };

  const departureTime = new Date(deal.departure_at);
  const formattedDate = format(departureTime, 'dd/MM/yyyy');
  const formattedTime = format(departureTime, 'HH:mm');

  return (
    <Card hoverable onClick={() => onSelect?.(deal)}>
      <div className="space-y-4">
        {/* Header with Deal Badge */}
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <span className="font-bold text-xl text-primary">
                {deal.origin} → {deal.destination}
              </span>
              {deal.is_deal && (
                <Badge variant="teal" size="sm">
                  {deal.deal_badge || 'Hot Deal'}
                </Badge>
              )}
            </div>
            <p className="text-sm text-secondary">
              {deal.origin_city}, {deal.origin_country} → {deal.destination_city}, {deal.destination_country}
            </p>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-teal">{formatPrice(deal.price)}</div>
            <p className="text-xs text-tertiary">{deal.currency}</p>
          </div>
        </div>

        {/* Flight Details */}
        <div className="grid grid-cols-3 gap-3 py-3 border-y border-border-primary">
          <div className="flex items-center gap-2 text-sm">
            <Clock size={16} className="text-tertiary" />
            <div>
              <p className="text-xs text-tertiary">Departure</p>
              <p className="font-medium">{formattedTime}</p>
            </div>
          </div>

          <div className="flex items-center gap-2 text-sm">
            <Plane size={16} className="text-tertiary" />
            <div>
              <p className="text-xs text-tertiary">Duration</p>
              <p className="font-medium">{formatDuration(deal.duration_minutes)}</p>
            </div>
          </div>

          <div className="flex items-center gap-2 text-sm">
            <TrendingDown size={16} className="text-tertiary" />
            <div>
              <p className="text-xs text-tertiary">Stops</p>
              <p className="font-medium">{deal.stops}</p>
            </div>
          </div>
        </div>

        {/* Airline and Date */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            {deal.airline_logo_url && (
              <img
                src={deal.airline_logo_url}
                alt={deal.airline}
                className="w-6 h-6 rounded"
                onError={(e) => {
                  e.currentTarget.style.display = 'none';
                }}
              />
            )}
            <div className="text-sm">
              <p className="font-medium text-primary">{deal.airline}</p>
              <p className="text-xs text-tertiary">{formattedDate}</p>
            </div>
          </div>

          {deal.is_deal && (
            <div className="text-right">
              <p className="text-xs text-teal font-semibold">✨ Best Price</p>
            </div>
          )}
        </div>
      </div>
    </Card>
  );
};
