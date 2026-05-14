import { useState, useEffect } from 'react';
import { Layout } from '../components/layout/Layout';
import { Card, Button, EmptyState } from '../components/ui';
import { alertsAPI, UserAlert } from '../api/alerts';

export const AlertsManager = () => {
  const [alerts, setAlerts] = useState<UserAlert[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadAlerts();
  }, []);

  const loadAlerts = async () => {
    setIsLoading(true);
    try {
      const data = await alertsAPI.listAlerts();
      setAlerts(data);
    } catch (error) {
      console.error('Load error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (alertId: string) => {
    if (confirm('Delete this alert?')) {
      try {
        await alertsAPI.deleteAlert(alertId);
        await loadAlerts();
      } catch (error) {
        console.error('Delete error:', error);
      }
    }
  };

  const columns = [
    { key: 'origin_iata', label: 'From', width: '80px' },
    { key: 'destination_iata', label: 'To', width: '80px' },
    { key: 'max_price', label: 'Max Price', width: '100px' },
    { key: 'date_from', label: 'Date From', width: '150px' },
    { key: 'date_to', label: 'Date To', width: '150px' },
  ];

  return (
    <Layout>
      <div className="p-6 max-w-6xl mx-auto space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Alerts Manager</h1>
          <p className="text-tertiary mt-1">View and manage user flight price alerts</p>
        </div>

        <Card>
          {isLoading ? (
            <div className="text-center py-8">Loading...</div>
          ) : alerts.length === 0 ? (
            <EmptyState
              icon="🔔"
              title="No alerts yet"
              description="Users haven't created any price alerts"
            />
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-bg-tertiary border-b border-border-primary">
                  <tr>
                    {columns.map((col) => (
                      <th
                        key={col.key}
                        className="px-4 py-3 text-left font-medium text-secondary"
                      >
                        {col.label}
                      </th>
                    ))}
                    <th className="px-4 py-3 text-right font-medium text-secondary">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {alerts.map((alert) => (
                    <tr key={alert.id} className="border-b border-border-primary hover:bg-bg-tertiary">
                      <td className="px-4 py-3">{alert.origin_iata || '-'}</td>
                      <td className="px-4 py-3">{alert.destination_iata || '-'}</td>
                      <td className="px-4 py-3">R${alert.max_price}</td>
                      <td className="px-4 py-3">{alert.date_from || '-'}</td>
                      <td className="px-4 py-3">{alert.date_to || '-'}</td>
                      <td className="px-4 py-3 text-right">
                        <Button
                          size="sm"
                          variant="danger"
                          onClick={() => handleDelete(alert.id)}
                        >
                          Delete
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Card>
      </div>
    </Layout>
  );
};
