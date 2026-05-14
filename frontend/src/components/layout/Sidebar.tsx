import { Link, useLocation } from 'react-router-dom';
import {
  Plane,
  Sliders,
  Users,
  Bell,
  Zap,
  Home,
} from 'lucide-react';

const navItems = [
  { path: '/deals', label: 'Deal Explorer', icon: Plane },
  { path: '/filter-lab', label: 'Filter Lab', icon: Sliders },
  { path: '/users', label: 'Users', icon: Users },
  { path: '/alerts', label: 'Alerts', icon: Bell },
  { path: '/routes', label: 'Routes', icon: Zap },
];

export const Sidebar = () => {
  const location = useLocation();

  return (
    <div className="w-64 bg-bg-secondary border-r border-border-primary h-screen sticky top-0 flex flex-col">
      {/* Logo */}
      <div className="px-6 py-6 border-b border-border-primary">
        <div className="flex items-center gap-2">
          <Plane className="text-teal" size={24} />
          <span className="font-bold text-lg text-primary">Flight Bot</span>
        </div>
        <p className="text-xs text-tertiary mt-2">Deal Explorer Demo</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto p-4">
        <div className="space-y-2">
          {navItems.map(({ path, label, icon: Icon }) => {
            const isActive = location.pathname === path;
            return (
              <Link
                key={path}
                to={path}
                className={`flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-teal text-bg-primary'
                    : 'text-secondary hover:bg-bg-tertiary'
                }`}
              >
                <Icon size={18} />
                {label}
              </Link>
            );
          })}
        </div>
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-border-primary text-xs text-tertiary">
        <p>Flight Bot v1.0.0</p>
        <p className="mt-1">Demo Mode Active</p>
      </div>
    </div>
  );
};
