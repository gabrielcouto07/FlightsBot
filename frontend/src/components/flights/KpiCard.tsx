import { ReactNode } from 'react';
import { TrendingDown, TrendingUp } from 'lucide-react';

import { Card } from '../ui';

interface KpiCardProps {
  label: string;
  value: string;
  trend?: string;
  positive?: boolean;
  icon: ReactNode;
}

export const KpiCard = ({ label, value, trend, positive = true, icon }: KpiCardProps) => {
  return (
    <Card className="rounded-2xl border-border-primary bg-[rgba(22,27,34,0.94)] p-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-tertiary">{label}</p>
          <div className="mt-3 font-mono text-3xl font-semibold tracking-tight text-primary">{value}</div>
          {trend ? (
            <div className={`mt-3 inline-flex items-center gap-1 text-xs ${positive ? 'text-success' : 'text-warning'}`}>
              {positive ? <TrendingUp size={14} /> : <TrendingDown size={14} />}
              {trend}
            </div>
          ) : null}
        </div>
        <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-border-primary bg-bg-tertiary text-info">
          {icon}
        </div>
      </div>
    </Card>
  );
};
