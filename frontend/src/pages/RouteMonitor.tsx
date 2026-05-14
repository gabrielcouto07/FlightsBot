import { useEffect, useState } from 'react';
import { Activity, Map, Radar } from 'lucide-react';

import { routesAPI, Route } from '../api/routes';
import { Card, EmptyState } from '../components/ui';
import { Layout } from '../components/layout/Layout';

export const RouteMonitor = () => {
  const [routes, setRoutes] = useState<Route[]>([]);

  useEffect(() => {
    void routesAPI.listRoutes().then(setRoutes);
  }, []);

  const activeRoutes = routes.filter((route) => route.is_active).length;
  const avgThreshold =
    routes.length > 0 ? Math.round(routes.reduce((sum, route) => sum + route.threshold_price, 0) / routes.length) : 0;

  return (
    <Layout>
      <div className="mx-auto max-w-[1400px] space-y-6">
        <section className="grid gap-4 xl:grid-cols-3">
          <Card className="rounded-2xl border-border-primary bg-[rgba(22,27,34,0.92)]">
            <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-tertiary">Tracked Routes</p>
            <div className="mt-3 text-3xl font-semibold text-primary">{routes.length}</div>
          </Card>
          <Card className="rounded-2xl border-border-primary bg-[rgba(22,27,34,0.92)]">
            <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-tertiary">Monitoring Live</p>
            <div className="mt-3 text-3xl font-semibold text-primary">{activeRoutes}</div>
          </Card>
          <Card className="rounded-2xl border-border-primary bg-[rgba(22,27,34,0.92)]">
            <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-tertiary">Average Threshold</p>
            <div className="mt-3 text-3xl font-semibold text-primary">R$ {avgThreshold}</div>
          </Card>
        </section>

        <section className="grid gap-6 xl:grid-cols-[0.92fr_1.08fr]">
          <Card className="rounded-2xl border-border-primary bg-[rgba(22,27,34,0.92)]">
            <div className="flex items-center gap-2">
              <Radar size={16} className="text-info" />
              <h2 className="text-xl font-semibold text-primary">Monitor Notes</h2>
            </div>
            <div className="mt-4 space-y-3 text-sm leading-6 text-secondary">
              <p>Route Monitor is the persistent watchlist behind the deals terminal.</p>
              <p>Each threshold represents the price level at which the bot should escalate a route into a deal signal.</p>
            </div>
          </Card>

          <Card className="rounded-2xl border-border-primary bg-[rgba(22,27,34,0.92)]">
            <div className="flex items-center gap-2">
              <Map size={16} className="text-info" />
              <h2 className="text-xl font-semibold text-primary">Monitored Routes</h2>
            </div>
            <div className="mt-4">
              {routes.length === 0 ? (
                <EmptyState
                  icon={<Activity size={24} />}
                  title="No monitored routes"
                  description="Create monitored routes to populate the route intelligence layer."
                />
              ) : (
                <div className="space-y-3">
                  {routes.map((route) => (
                    <div key={route.id} className="rounded-xl border border-border-primary bg-[rgba(255,255,255,0.03)] p-4">
                      <div className="flex items-center justify-between gap-4">
                        <div>
                          <div className="text-lg font-semibold text-primary">
                            {route.origin_iata} {String.fromCharCode(8594)} {route.destination_iata}
                          </div>
                          <div className="mt-1 text-sm text-secondary">{route.is_active ? 'Scanning actively' : 'Paused from monitoring'}</div>
                        </div>
                        <div className="text-right">
                          <div className="text-xl font-semibold text-primary">R$ {route.threshold_price}</div>
                          <div className="text-xs uppercase tracking-[0.14em] text-tertiary">Trigger threshold</div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </Card>
        </section>
      </div>
    </Layout>
  );
};
