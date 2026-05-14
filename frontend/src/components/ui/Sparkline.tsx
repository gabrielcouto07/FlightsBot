import { useMemo } from 'react';

interface SparklineProps {
  values: number[];
  className?: string;
}

export const Sparkline = ({ values, className = '' }: SparklineProps) => {
  const points = useMemo(() => {
    if (values.length < 2) {
      return '';
    }

    const width = 80;
    const height = 28;
    const min = Math.min(...values);
    const max = Math.max(...values);
    const range = max - min || 1;

    return values
      .map((value, index) => {
        const x = (index / (values.length - 1)) * width;
        const y = height - ((value - min) / range) * height;
        return `${x},${y}`;
      })
      .join(' ');
  }, [values]);

  if (!points) {
    return <div className={`h-7 w-20 rounded-full bg-[rgba(255,255,255,0.06)] ${className}`} />;
  }

  return (
    <svg viewBox="0 0 80 28" className={`h-7 w-20 overflow-visible ${className}`} fill="none" aria-hidden="true">
      <polyline
        points={points}
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
};
