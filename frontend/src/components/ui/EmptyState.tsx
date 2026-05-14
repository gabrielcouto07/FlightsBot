import { ReactNode } from 'react';

interface EmptyStateProps {
  icon?: ReactNode;
  title: string;
  description?: string;
  action?: ReactNode;
}

export const EmptyState = ({ icon, title, description, action }: EmptyStateProps) => {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-border-primary bg-bg-quaternary/50 px-6 py-16 text-center">
      {icon ? (
        <div className="mb-5 flex h-16 w-16 items-center justify-center rounded-lg border border-accent/20 bg-accent/10 text-3xl text-accent">
          {icon}
        </div>
      ) : null}
      <h3 className="mb-3 text-xl font-700 text-text-primary">{title}</h3>
      {description ? <p className="mb-6 max-w-md text-sm leading-6 text-text-secondary">{description}</p> : null}
      {action ? <div>{action}</div> : null}
    </div>
  );
};
