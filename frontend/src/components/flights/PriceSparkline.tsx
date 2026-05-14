interface PriceSparklineProps {
  values: number[];
  stroke?: string;
}

export const PriceSparkline = ({
  values,
  stroke = '#58A6FF',
}: PriceSparklineProps) => {
  if (values.length < 2) {
    return <div className="h-10 w-full rounded-md bg-[rgba(255,255,255,0.03)]" />;
  }

  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min || 1;
  const points = values
    .map((value, index) => {
      const x = (index / (values.length - 1)) * 100;
      const y = 100 - ((value - min) / range) * 100;
      return `${x},${y}`;
    })
    .join(' ');

  return (
    <svg viewBox="0 0 100 100" preserveAspectRatio="none" className="h-10 w-full">
      <polyline
        fill="none"
        stroke={stroke}
        strokeWidth="4"
        strokeLinecap="round"
        strokeLinejoin="round"
        points={points}
      />
    </svg>
  );
};
