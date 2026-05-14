import { useEffect, useMemo, useRef, useState } from 'react';
import { ptBR } from 'date-fns/locale';
import {
  addDays,
  addMonths,
  endOfMonth,
  endOfWeek,
  format,
  isBefore,
  isSameDay,
  isSameMonth,
  isWithinInterval,
  startOfDay,
  startOfMonth,
  startOfToday,
  startOfWeek,
} from 'date-fns';
import { CalendarDays, ChevronLeft, ChevronRight } from 'lucide-react';

interface DatePickerProps {
  label: string;
  value?: string;
  onChange: (nextValue: string) => void;
  minDate?: string;
  rangeStart?: string;
  rangeEnd?: string;
  disabled?: boolean;
}

const toInputDate = (value: Date) => format(value, 'yyyy-MM-dd');

const buildCalendarDays = (month: Date) => {
  const monthStart = startOfMonth(month);
  const monthEnd = endOfMonth(month);
  const calendarStart = startOfWeek(monthStart, { weekStartsOn: 0 });
  const calendarEnd = endOfWeek(monthEnd, { weekStartsOn: 0 });

  const days: Date[] = [];
  let cursor = calendarStart;

  while (cursor <= calendarEnd) {
    days.push(cursor);
    cursor = addDays(cursor, 1);
  }

  return days;
};

export const DatePicker = ({
  label,
  value,
  onChange,
  minDate,
  rangeStart,
  rangeEnd,
  disabled = false,
}: DatePickerProps) => {
  const [open, setOpen] = useState(false);
  const rootRef = useRef<HTMLDivElement | null>(null);
  const selectedDate = value ? startOfDay(new Date(`${value}T00:00:00`)) : null;
  const minSelectableDate = minDate
    ? startOfDay(new Date(`${minDate}T00:00:00`))
    : startOfToday();
  const [visibleMonth, setVisibleMonth] = useState(selectedDate ?? minSelectableDate);

  const startDate = rangeStart ? startOfDay(new Date(`${rangeStart}T00:00:00`)) : null;
  const endDate = rangeEnd ? startOfDay(new Date(`${rangeEnd}T00:00:00`)) : null;
  const days = useMemo(() => buildCalendarDays(visibleMonth), [visibleMonth]);

  useEffect(() => {
    const handlePointerDown = (event: MouseEvent) => {
      if (rootRef.current && !rootRef.current.contains(event.target as Node)) {
        setOpen(false);
      }
    };

    document.addEventListener('mousedown', handlePointerDown);
    return () => document.removeEventListener('mousedown', handlePointerDown);
  }, []);

  return (
    <div ref={rootRef} className="relative">
      <div>
        <label className="mb-2 block text-[13px] font-medium text-secondary">{label}</label>
        <button
          type="button"
          disabled={disabled}
          onClick={() => setOpen((current) => !current)}
          className={`flex h-12 w-full items-center justify-between rounded-xl border bg-bg-quaternary px-4 text-left transition-[border-color,box-shadow] duration-150 ${
            disabled
              ? 'cursor-not-allowed border-border-primary text-faint opacity-70'
              : 'border-border-primary text-primary hover:border-border-secondary focus-visible:border-teal focus-visible:shadow-[0_0_0_2px_rgba(88,166,255,0.15)]'
          }`}
        >
          <span className={`flex items-center gap-3 text-sm ${value ? 'text-primary' : 'text-faint'}`}>
            <CalendarDays size={16} className="text-secondary" />
            <span className="truncate font-medium">
              {value
                ? format(new Date(`${value}T00:00:00`), "EEE, d 'de' MMM", { locale: ptBR })
                : 'Selecionar data'}
            </span>
          </span>
        </button>

        {open ? (
          <div className="mt-2 w-full rounded-2xl border border-border-primary bg-bg-tertiary p-4 shadow-lg">
            <div className="flex items-center justify-between">
              <button
                type="button"
                onClick={() => setVisibleMonth((current) => addMonths(current, -1))}
                className="flex h-8 w-8 items-center justify-center rounded-lg text-secondary transition-colors hover:bg-bg-quaternary hover:text-primary"
                aria-label="Previous month"
              >
                <ChevronLeft size={16} />
              </button>
              <div className="text-sm font-semibold text-primary">{format(visibleMonth, 'MMMM yyyy', { locale: ptBR })}</div>
              <button
                type="button"
                onClick={() => setVisibleMonth((current) => addMonths(current, 1))}
                className="flex h-8 w-8 items-center justify-center rounded-lg text-secondary transition-colors hover:bg-bg-quaternary hover:text-primary"
                aria-label="Next month"
              >
                <ChevronRight size={16} />
              </button>
            </div>

            <div className="mt-4 grid grid-cols-7 gap-1 text-center text-[11px] uppercase tracking-[0.06em] text-secondary">
              {['dom', 'seg', 'ter', 'qua', 'qui', 'sex', 'sab'].map((day) => (
                <div key={day} className="py-1">
                  {day}
                </div>
              ))}
            </div>

            <div className="mt-2 grid grid-cols-7 gap-1">
              {days.map((day) => {
                const isDisabled = isBefore(day, minSelectableDate);
                const isSelected = selectedDate ? isSameDay(day, selectedDate) : false;
                const isToday = isSameDay(day, startOfToday());
                const inRange =
                  startDate && endDate
                    ? isWithinInterval(day, { start: startDate, end: endDate })
                    : false;

                return (
                  <button
                    key={day.toISOString()}
                    type="button"
                    disabled={isDisabled}
                    onClick={() => {
                      onChange(toInputDate(day));
                      setVisibleMonth(day);
                      setOpen(false);
                    }}
                    className={`flex h-9 items-center justify-center rounded-lg text-sm transition-colors ${
                      !isSameMonth(day, visibleMonth)
                        ? 'text-faint'
                        : isDisabled
                          ? 'text-faint opacity-50'
                          : isSelected
                            ? 'bg-teal text-bg-primary'
                            : inRange
                              ? 'bg-[rgba(88,166,255,0.12)] text-primary'
                              : 'text-primary hover:bg-bg-quaternary'
                    } ${isToday && !isSelected ? 'border border-teal/50' : 'border border-transparent'}`}
                  >
                    {format(day, 'd')}
                  </button>
                );
              })}
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
};
