import { ReactNode } from 'react';

interface TableProps {
  columns: Array<{ key: string; label: string; width?: string }>;
  data: Array<Record<string, any>>;
  rowKey: string;
  onRowClick?: (row: Record<string, any>) => void;
  loading?: boolean;
  emptyMessage?: string;
}

export const Table = ({
  columns,
  data,
  rowKey,
  onRowClick,
  loading = false,
  emptyMessage = 'No data available',
}: TableProps) => {
  if (loading) {
    return <div className="text-center py-8 text-tertiary">Loading...</div>;
  }

  if (data.length === 0) {
    return <div className="text-center py-8 text-tertiary">{emptyMessage}</div>;
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead className="bg-bg-tertiary border-b border-border-primary">
          <tr>
            {columns.map((column) => (
              <th
                key={column.key}
                className="px-4 py-3 text-left font-medium text-secondary"
                style={{ width: column.width }}
              >
                {column.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, idx) => (
            <tr
              key={row[rowKey] || idx}
              className="border-b border-border-primary hover:bg-bg-tertiary cursor-pointer transition-colors"
              onClick={() => onRowClick?.(row)}
            >
              {columns.map((column) => (
                <td key={column.key} className="px-4 py-3 text-primary">
                  {row[column.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
