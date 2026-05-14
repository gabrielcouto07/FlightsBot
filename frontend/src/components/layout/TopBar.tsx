import { CalendarDays, Plane, RefreshCw } from 'lucide-react';

export const TopBar = () => {
  const today = new Intl.DateTimeFormat('pt-BR', {
    month: 'short',
    day: 'numeric',
  }).format(new Date());

  return (
    <header className="fixed inset-x-0 top-0 z-50 border-b border-border-primary bg-gradient-to-r from-bg-primary to-bg-primary/80 backdrop-blur-xl">
      <div className="mx-auto flex h-14 max-w-[1600px] items-center justify-between px-4 lg:px-8">
        <div className="flex items-center gap-3">
          <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-br from-accent to-accent-dark text-bg-primary">
            <Plane size={18} strokeWidth={2.5} />
          </span>
          <span className="text-sm font-700 text-text-primary">FlightsBot</span>
        </div>

        <div className="hidden flex-1 lg:block" />

        <div className="flex items-center gap-3">
          <div className="hidden items-center gap-2.5 rounded-lg border border-border-primary bg-bg-tertiary px-3 py-1.5 text-xs font-500 text-text-secondary sm:flex hover:border-accent/50 transition-colors">
            <CalendarDays size={14} className="text-accent" />
            <span>{today}</span>
          </div>

          <button
            type="button"
            className="flex h-9 w-9 items-center justify-center rounded-lg border border-border-primary bg-bg-tertiary text-text-secondary transition-all duration-200 hover:border-accent/50 hover:text-accent hover:bg-bg-quaternary"
            onClick={() => window.location.reload()}
            aria-label="Refresh page"
          >
            <RefreshCw size={16} strokeWidth={2} />
          </button>

          <div className="rounded-lg border border-accent/30 bg-accent/10 px-3 py-1.5 text-xs font-600 text-accent uppercase tracking-wider">
            Demo
          </div>
        </div>
      </div>
    </header>
  );
};
