import { ReactNode } from 'react';

interface EmptyStateProps {
  icon?: ReactNode;
  title: string;
  description?: string;
  action?: ReactNode;
}

export const EmptyState = ({
  icon,
  title,
  description,
  action,
}: EmptyStateProps) => {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4">
      {icon && <div className="mb-4 text-4xl">{icon}</div>}
      <h3 className="text-lg font-semibold text-primary mb-2">{title}</h3>
      {description && <p className="text-tertiary text-center mb-6">{description}</p>}
      {action && <div>{action}</div>}
    </div>
  );
};
