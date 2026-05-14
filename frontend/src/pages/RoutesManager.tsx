import { useState, useEffect } from 'react';
import { Layout } from '../components/layout/Layout';
import { Card, Button, EmptyState } from '../components/ui';
import { routesAPI, Route } from '../api/routes';

export const RoutesManager = () => {
  const [routes, setRoutes] = useState<Route[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadRoutes();
  }, []);

  const loadRoutes = async () => {
    setIsLoading(true);
    try {
      const data = await routesAPI.listRoutes();
      setRoutes(data);
    } catch (error) {
      console.error('Load error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (routeId: string) => {
    if (confirm('Delete this route?')) {
      try {
        await routesAPI.deleteRoute(routeId);
        await loadRoutes();
      } catch (error) {
        console.error('Delete error:', error);
      }
    }
  };

  return (
    <Layout>
      <div className="p-6 max-w-4xl mx-auto space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Routes Manager</h1>
          <p className="text-tertiary mt-1">View and manage flight routes</p>
        </div>

        <Card>
          {isLoading ? (
            <div className="text-center py-8">Loading...</div>
          ) : routes.length === 0 ? (
            <EmptyState
              icon="🗺️"
              title="No routes yet"
              description="No flight routes have been added"
            />
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-bg-tertiary border-b border-border-primary">
                  <tr>
                    <th className="px-4 py-3 text-left font-medium text-secondary">Route</th>
                    <th className="px-4 py-3 text-left font-medium text-secondary">Threshold Price</th>
                    <th className="px-4 py-3 text-left font-medium text-secondary">Status</th>
                    <th className="px-4 py-3 text-right font-medium text-secondary">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {routes.map((route) => (
                    <tr key={route.id} className="border-b border-border-primary hover:bg-bg-tertiary">
                      <td className="px-4 py-3 font-semibold">
                        {route.origin_iata} → {route.destination_iata}
                      </td>
                      <td className="px-4 py-3">R${route.threshold_price}</td>
                      <td className="px-4 py-3">
                        <span className={`px-2 py-1 rounded text-xs font-medium ${route.is_active ? 'bg-green-900 text-green-200' : 'bg-red-900 text-red-200'}`}>
                          {route.is_active ? 'Active' : 'Inactive'}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-right">
                        <Button
                          size="sm"
                          variant="danger"
                          onClick={() => handleDelete(route.id)}
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
