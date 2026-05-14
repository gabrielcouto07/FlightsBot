interface SkeletonProps {
  width?: string;
  height?: string;
  className?: string;
  circle?: boolean;
  count?: number;
}

export const Skeleton = ({
  width = '100%',
  height = '1rem',
  className = '',
  circle = false,
  count = 1,
}: SkeletonProps) => {
  const items = Array.from({ length: count });

  return (
    <>
      {items.map((_, idx) => (
        <div
          key={idx}
          className={`bg-bg-tertiary animate-pulse ${className} ${circle ? 'rounded-full' : 'rounded'}`}
          style={{ width, height }}
        />
      ))}
    </>
  );
};
