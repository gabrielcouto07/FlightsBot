import { Card, Skeleton } from '../ui';

export const DealCardSkeleton = () => {
  return (
    <Card>
      <div className="space-y-4">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <Skeleton width="60%" height="1.5rem" className="mb-2" />
            <Skeleton width="80%" height="1rem" />
          </div>
          <Skeleton width="100px" height="2rem" />
        </div>

        <div className="grid grid-cols-3 gap-3 py-3 border-y border-border-primary">
          <Skeleton height="3rem" />
          <Skeleton height="3rem" />
          <Skeleton height="3rem" />
        </div>

        <div className="flex items-center justify-between">
          <Skeleton width="40%" height="1rem" />
          <Skeleton width="30%" height="1rem" />
        </div>
      </div>
    </Card>
  );
};
