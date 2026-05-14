export const DealCardSkeleton = () => {
  return (
    <div className="rounded-xl border border-border-primary bg-bg-tertiary p-5">
      <div className="grid gap-5 lg:grid-cols-[20%_45%_35%] lg:items-center">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-lg animate-surface-shimmer" />
          <div className="space-y-2">
            <div className="h-3 w-24 rounded-full animate-surface-shimmer" />
            <div className="h-3 w-16 rounded-full animate-surface-shimmer" />
          </div>
        </div>

        <div className="space-y-3">
          <div className="h-5 w-32 rounded-full animate-surface-shimmer" />
          <div className="h-3 w-40 rounded-full animate-surface-shimmer" />
          <div className="h-3 w-28 rounded-full animate-surface-shimmer" />
          <div className="h-3 w-36 rounded-full animate-surface-shimmer" />
        </div>

        <div className="space-y-3 lg:ml-auto lg:w-[180px]">
          <div className="h-6 w-28 rounded-full animate-surface-shimmer" />
          <div className="h-3 w-32 rounded-full animate-surface-shimmer" />
          <div className="h-7 w-20 rounded-full animate-surface-shimmer" />
          <div className="h-9 rounded-[10px] animate-surface-shimmer" />
          <div className="h-3 w-24 rounded-full animate-surface-shimmer" />
        </div>
      </div>
    </div>
  );
};
