interface TripToggleProps {
  value: 'oneway' | 'roundtrip';
  onChange: (value: 'oneway' | 'roundtrip') => void;
}

export const TripToggle = ({ value, onChange }: TripToggleProps) => {
  return (
    <div className="inline-flex w-full max-w-[260px] rounded-full border border-border-primary bg-bg-quaternary p-1">
      {([
        { label: 'Só ida', value: 'oneway' },
        { label: 'Ida e volta', value: 'roundtrip' },
      ] as const).map((option) => {
        const active = option.value === value;

        return (
          <button
            key={option.value}
            type="button"
            onClick={() => onChange(option.value)}
            className={`min-w-0 flex-1 rounded-full px-4 py-2 text-sm font-semibold transition-all duration-200 ${
              active
                ? 'bg-white text-[#0D1117] shadow-sm shadow-[rgba(1,4,9,0.16)]'
                : 'text-secondary hover:text-primary'
            }`}
          >
            {option.label}
          </button>
        );
      })}
    </div>
  );
};
