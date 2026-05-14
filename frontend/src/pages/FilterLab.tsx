import { useState, useEffect } from 'react';
import { Layout } from '../components/layout/Layout';
import { Card, Button, Badge } from '../components/ui';
import { searchAPI, Deal } from '../api/search';
import { usersAPI, User } from '../api/users';

export const FilterLab = () => {
  const [deals, setDeals] = useState<Deal[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setIsLoading(true);
    try {
      const [dealsRes, usersRes] = await Promise.all([
        searchAPI.searchDeals({ fly_from: 'GRU', limit: 10 }),
        usersAPI.listUsers(),
      ]);
      setDeals(dealsRes.results);
      setUsers(usersRes);
    } catch (error) {
      console.error('Load error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Layout>
      <div className="p-6 max-w-4xl mx-auto space-y-6">
        <div>
          <h1 className="text-3xl font-bold mb-2">Filter Lab</h1>
          <p className="text-tertiary">
            Experiment with different search filters and see how deals match user alerts
          </p>
        </div>

        <div className="grid grid-cols-2 gap-6">
          {/* Deals Section */}
          <Card>
            <div className="space-y-4">
              <h2 className="text-xl font-semibold">Available Deals</h2>
              <p className="text-sm text-tertiary">{deals.length} deals loaded</p>
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {deals.map((deal) => (
                  <div
                    key={`${deal.origin}${deal.destination}${deal.departure_at}`}
                    className="p-2 bg-bg-tertiary rounded text-sm flex justify-between items-center"
                  >
                    <span>
                      {deal.origin} → {deal.destination}: R${deal.price}
                    </span>
                    {deal.is_deal && <Badge variant="teal" size="sm">Deal</Badge>}
                  </div>
                ))}
              </div>
              <Button
                variant="secondary"
                onClick={loadData}
                isLoading={isLoading}
                className="w-full"
              >
                Refresh Deals
              </Button>
            </div>
          </Card>

          {/* Users Section */}
          <Card>
            <div className="space-y-4">
              <h2 className="text-xl font-semibold">Test Users</h2>
              <p className="text-sm text-tertiary">{users.length} users available</p>
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {users.map((user) => (
                  <div
                    key={user.id}
                    className="p-2 bg-bg-tertiary rounded text-sm flex justify-between items-center"
                  >
                    <span>{user.name || 'Unknown'}</span>
                    <Badge variant={user.plan === 'paid' ? 'teal' : 'info'} size="sm">
                      {user.plan}
                    </Badge>
                  </div>
                ))}
              </div>
            </div>
          </Card>
        </div>

        <Card>
          <div className="space-y-4">
            <h2 className="text-xl font-semibold">Test Matching</h2>
            <p className="text-sm text-tertiary">
              Select a user and deals to see which ones match their alerts
            </p>
            <Button variant="primary" disabled className="w-full">
              Test Match Logic (Select users and deals)
            </Button>
          </div>
        </Card>
      </div>
    </Layout>
  );
};
