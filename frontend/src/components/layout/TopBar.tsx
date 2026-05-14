import { AlertCircle, RefreshCw } from 'lucide-react';
import { Button } from '../ui';

export const TopBar = () => {
  return (
    <div className="bg-bg-secondary border-b border-border-primary px-6 py-4 sticky top-0 z-40">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-primary">Flight Bot</h1>
          <p className="text-sm text-tertiary">Real-time flight deal discovery</p>
        </div>
        <div className="flex items-center gap-4">
          <button className="text-tertiary hover:text-primary transition-colors">
            <RefreshCw size={20} />
          </button>
          <div className="flex items-center gap-2 px-3 py-1.5 bg-bg-tertiary rounded-lg">
            <AlertCircle size={16} className="text-warning" />
            <span className="text-xs text-secondary">Demo Mode</span>
          </div>
        </div>
      </div>
    </div>
  );
};
