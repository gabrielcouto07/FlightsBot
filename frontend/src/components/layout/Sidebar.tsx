import { Link, useLocation } from 'react-router-dom';
import { Plane } from 'lucide-react';

import { navItems } from './navItems';

interface SidebarProps {
  currentPath?: string;
}

const mobileNavItems = navItems.slice(0, 4);

export const Sidebar = ({ currentPath }: SidebarProps) => {
  const location = useLocation();
  const pathname = currentPath ?? location.pathname;

  return (
    <>
      <aside className="sticky top-14 hidden h-[calc(100vh-56px)] w-[220px] shrink-0 overflow-y-auto border-r border-border-primary bg-gradient-to-b from-bg-secondary to-bg-tertiary lg:flex lg:flex-col">
        <div className="border-b border-border-primary px-4 py-5">
          <div className="flex items-center gap-3">
            <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-accent to-accent-dark text-bg-primary">
              <Plane size={20} strokeWidth={2.5} />
            </span>
            <div className="min-w-0">
              <div className="truncate text-sm font-700 text-text-primary">FlightsBot</div>
              <div className="mt-0.5 text-xs text-text-muted">Workspace</div>
            </div>
          </div>
        </div>

        <div className="px-4 pt-5 pb-2 text-xs font-600 text-text-tertiary uppercase tracking-wider">Navegação</div>

        <nav className="mt-1 flex-1 space-y-0.5 pr-3 px-4">
          {navItems.map(({ path, label, icon: Icon }) => {
            const isActive = pathname === path;

            return (
              <Link
                key={path}
                to={path}
                className={`relative flex h-9 items-center gap-2.5 px-3.5 rounded-lg text-sm font-500 transition-all duration-200 ${
                  isActive
                    ? 'bg-accent/20 text-accent border border-accent/40'
                    : 'text-text-secondary hover:bg-bg-quaternary hover:text-text-primary'
                }`}
                aria-current={isActive ? 'page' : undefined}
              >
                <Icon size={18} strokeWidth={1.5} />
                <span className="truncate">{label}</span>
              </Link>
            );
          })}
        </nav>

        <div className="mt-auto border-t border-border-primary px-4 py-4">
          <div className="flex items-center gap-2.5 text-xs text-text-secondary">
            <span className="h-2 w-2 rounded-full bg-success animate-pulse" />
            <span>Bot online</span>
          </div>
          <div className="mt-3 border-t border-border-primary pt-3 text-xs text-text-muted">v0.1.0 · demo</div>
        </div>
      </aside>

      <nav className="fixed inset-x-0 bottom-0 z-40 border-t border-border-primary bg-bg-secondary/95 backdrop-blur-lg lg:hidden">
        <div className="grid grid-cols-4">
          {mobileNavItems.map(({ path, label, icon: Icon }) => {
            const isActive = pathname === path;

            return (
              <Link
                key={path}
                to={path}
                className={`flex h-14 items-center justify-center ${isActive ? 'text-teal' : 'text-secondary'}`}
                aria-label={label}
                aria-current={isActive ? 'page' : undefined}
              >
                <Icon size={20} />
              </Link>
            );
          })}
        </div>
      </nav>
    </>
  );
};
