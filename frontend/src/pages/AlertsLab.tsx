import { useEffect, useState } from 'react';
import { BellRing, Radar, Users } from 'lucide-react';

import { alertsAPI, UserAlert } from '../api/alerts';
import { usersAPI, User } from '../api/users';
import { Card, EmptyState } from '../components/ui';
import { Layout } from '../components/layout/Layout';

export const AlertsLab = () => {
  const [alerts, setAlerts] = useState<UserAlert[]>([]);
  const [users, setUsers] = useState<User[]>([]);

  useEffect(() => {
    void Promise.all([alertsAPI.listAlerts(), usersAPI.listUsers()]).then(([alertRows, userRows]) => {
      setAlerts(alertRows);
      setUsers(userRows);
    });
  }, []);

  const paidUsers = users.filter((user) => user.plan === 'paid').length;

  return (
    <Layout>
      <div className="mx-auto max-w-[1400px] space-y-6">
        <section className="grid gap-4 xl:grid-cols-3">
          <Card className="rounded-2xl border-border-primary bg-[rgba(22,27,34,0.92)]">
            <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-tertiary">Active Alerts</p>
            <div className="mt-3 text-3xl font-semibold text-primary">{alerts.length}</div>
          </Card>
          <Card className="rounded-2xl border-border-primary bg-[rgba(22,27,34,0.92)]">
            <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-tertiary">Paid Travelers</p>
            <div className="mt-3 text-3xl font-semibold text-primary">{paidUsers}</div>
          </Card>
          <Card className="rounded-2xl border-border-primary bg-[rgba(22,27,34,0.92)]">
            <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-tertiary">Average Ceiling</p>
            <div className="mt-3 text-3xl font-semibold text-primary">
              R$ {alerts.length ? Math.round(alerts.reduce((sum, alert) => sum + alert.max_price, 0) / alerts.length) : 0}
            </div>
          </Card>
        </section>

        <section className="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
          <Card className="rounded-2xl border-border-primary bg-[rgba(22,27,34,0.92)]">
            <div className="flex items-center gap-2">
              <Radar size={16} className="text-info" />
              <h2 className="text-xl font-semibold text-primary">Alert Screening Notes</h2>
            </div>
            <div className="mt-4 space-y-3 text-sm leading-6 text-secondary">
              <p>The lab is where you evaluate whether your active alerts are too wide, too narrow, or missing the best routes.</p>
              <p>Use the deals workspace to test real results, then return here to tighten thresholds and date windows.</p>
            </div>
          </Card>

          <Card className="rounded-2xl border-border-primary bg-[rgba(22,27,34,0.92)]">
            <div className="flex items-center gap-2">
              <BellRing size={16} className="text-info" />
              <h2 className="text-xl font-semibold text-primary">Current Alert Grid</h2>
            </div>
            <div className="mt-4">
              {alerts.length === 0 ? (
                <EmptyState
                  icon={<BellRing size={24} />}
                  title="No active alerts"
                  description="Seed demo data or create an alert to start pressure-testing the alert engine."
                />
              ) : (
                <div className="space-y-3">
                  {alerts.map((alert) => (
                    <div key={alert.id} className="rounded-xl border border-border-primary bg-[rgba(255,255,255,0.03)] p-4">
                      <div className="flex flex-wrap items-center justify-between gap-3">
                        <div>
                          <div className="text-lg font-semibold text-primary">
                            {alert.origin_iata || 'ANY'} {String.fromCharCode(8594)} {alert.destination_iata || 'ANY'}
                          </div>
                          <div className="mt-1 text-sm text-secondary">
                            {alert.date_from} to {alert.date_to}
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-xl font-semibold text-primary">R$ {alert.max_price}</div>
                          <div className="text-xs uppercase tracking-[0.14em] text-tertiary">
                            {alert.is_active ? 'Armed' : 'Paused'}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </Card>
        </section>

        <Card className="rounded-2xl border-border-primary bg-[rgba(22,27,34,0.92)]">
          <div className="flex items-center gap-2">
            <Users size={16} className="text-info" />
            <h2 className="text-xl font-semibold text-primary">Who is Covered</h2>
          </div>
          <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
            {users.slice(0, 6).map((user) => (
              <div key={user.id} className="rounded-xl border border-border-primary bg-[rgba(255,255,255,0.03)] p-4">
                <div className="text-lg font-semibold text-primary">{user.name || user.phone_number}</div>
                <div className="mt-1 text-sm text-secondary">{user.plan.toUpperCase()}</div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </Layout>
  );
};
