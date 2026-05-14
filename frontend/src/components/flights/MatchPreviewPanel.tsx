import { Card, Badge, EmptyState } from '../ui';
import { CheckCircle, AlertCircle } from 'lucide-react';

interface MatchedAlert {
  id: string;
  origin_iata?: string;
  destination_iata?: string;
  matched_deal_count: number;
}

interface MatchPreviewPanelProps {
  userName: string;
  userPlan: string;
  matchedDeals: number;
  unmatchedDeals: number;
  matchedAlerts: MatchedAlert[];
  activeAlerts: number;
}

export const MatchPreviewPanel = ({
  userName,
  userPlan,
  matchedDeals,
  unmatchedDeals,
  matchedAlerts,
  activeAlerts,
}: MatchPreviewPanelProps) => {
  const totalDeals = matchedDeals + unmatchedDeals;
  const matchRate = totalDeals > 0 ? Math.round((matchedDeals / totalDeals) * 100) : 0;

  if (totalDeals === 0) {
    return (
      <Card>
        <EmptyState
          icon="🔍"
          title="No Deals to Analyze"
          description="Search for flights first to see how they match your alerts"
        />
      </Card>
    );
  }

  return (
    <Card className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">Match Preview</h3>
        <Badge variant={userPlan === 'paid' ? 'teal' : 'info'}>
          {userPlan.toUpperCase()}
        </Badge>
      </div>

      <div className="bg-bg-tertiary rounded-lg p-4 space-y-2">
        <p className="text-sm text-secondary">User: <span className="font-semibold text-primary">{userName}</span></p>
        <p className="text-sm text-secondary">Active Alerts: <span className="font-semibold text-primary">{activeAlerts}</span></p>
      </div>

      <div className="grid grid-cols-3 gap-3">
        <div className="bg-teal bg-opacity-10 border border-teal border-opacity-30 rounded-lg p-3 text-center">
          <p className="text-2xl font-bold text-teal">{matchedDeals}</p>
          <p className="text-xs text-secondary mt-1">Matched</p>
        </div>
        <div className="bg-warning bg-opacity-10 border border-warning border-opacity-30 rounded-lg p-3 text-center">
          <p className="text-2xl font-bold text-warning">{unmatchedDeals}</p>
          <p className="text-xs text-secondary mt-1">Unmatched</p>
        </div>
        <div className="bg-info bg-opacity-10 border border-info border-opacity-30 rounded-lg p-3 text-center">
          <p className="text-2xl font-bold text-info">{matchRate}%</p>
          <p className="text-xs text-secondary mt-1">Match Rate</p>
        </div>
      </div>

      {matchedAlerts.length > 0 && (
        <div className="space-y-2">
          <h4 className="text-sm font-semibold">Matched Alerts</h4>
          <div className="space-y-1">
            {matchedAlerts.map((alert) => (
              <div key={alert.id} className="flex items-center justify-between text-sm p-2 bg-bg-tertiary rounded">
                <div className="flex items-center gap-2">
                  <CheckCircle size={16} className="text-success" />
                  <span className="text-primary">
                    {alert.origin_iata || '∞'} → {alert.destination_iata || '∞'}
                  </span>
                </div>
                <Badge variant="success" size="sm">
                  {alert.matched_deal_count} deal{alert.matched_deal_count !== 1 ? 's' : ''}
                </Badge>
              </div>
            ))}
          </div>
        </div>
      )}

      {matchedAlerts.length === 0 && matchedDeals === 0 && (
        <div className="flex items-center gap-2 p-3 bg-warning bg-opacity-10 border border-warning border-opacity-30 rounded-lg">
          <AlertCircle size={18} className="text-warning flex-shrink-0" />
          <p className="text-sm text-warning">No alerts matched these deals</p>
        </div>
      )}
    </Card>
  );
};
