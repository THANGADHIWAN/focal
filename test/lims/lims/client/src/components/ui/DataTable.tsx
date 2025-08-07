import React from 'react';

interface Column {
  field: string;
  header: string;
  sortable?: boolean;
  body?: (rowData: any) => React.ReactNode;
}

interface DataTableProps {
  value: any[];
  columns?: Column[];
  loading?: boolean;
  paginator?: boolean;
  rows?: number;
  onPage?: (event: { page: number; pageSize: number }) => void;
  className?: string;
}

export const DataTable: React.FC<DataTableProps> = ({
  value,
  columns,
  loading,
  paginator,
  rows = 10,
  onPage,
  className = ''
}) => {
  const [currentPage, setCurrentPage] = React.useState(0);

  const handlePageChange = (newPage: number) => {
    setCurrentPage(newPage);
    onPage?.({ page: newPage, pageSize: rows });
  };

  const totalPages = Math.ceil(value.length / rows);
  const startIndex = currentPage * rows;
  const endIndex = Math.min(startIndex + rows, value.length);
  const displayedData = value.slice(startIndex, endIndex);

  const getValue = (row: any, field: string) => {
    return field.split('.').reduce((obj, key) => obj?.[key], row);
  };

  return (
    <div className={`overflow-x-auto ${className}`}>
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            {columns?.map((col, index) => (
              <th
                key={index}
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {loading ? (
            <tr>
              <td
                colSpan={columns?.length || 1}
                className="px-6 py-4 text-center text-sm text-gray-500"
              >
                Loading...
              </td>
            </tr>
          ) : displayedData.length === 0 ? (
            <tr>
              <td
                colSpan={columns?.length || 1}
                className="px-6 py-4 text-center text-sm text-gray-500"
              >
                No records found
              </td>
            </tr>
          ) : (
            displayedData.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {columns?.map((col, colIndex) => (
                  <td key={colIndex} className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {col.body ? col.body(row) : getValue(row, col.field)}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>

      {paginator && totalPages > 1 && (
        <div className="flex items-center justify-between px-4 py-3 bg-white border-t border-gray-200 sm:px-6">
          <div className="flex justify-between w-full">
            <div>
              <p className="text-sm text-gray-700">
                Showing <span className="font-medium">{startIndex + 1}</span> to{' '}
                <span className="font-medium">{endIndex}</span> of{' '}
                <span className="font-medium">{value.length}</span> results
              </p>
            </div>
            <div>
              <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                <button
                  onClick={() => handlePageChange(currentPage - 1)}
                  disabled={currentPage === 0}
                  className={`
                    relative inline-flex items-center px-2 py-2 rounded-l-md border
                    text-sm font-medium
                    ${currentPage === 0
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      : 'bg-white text-gray-500 hover:bg-gray-50'
                    }
                  `}
                >
                  Previous
                </button>
                <button
                  onClick={() => handlePageChange(currentPage + 1)}
                  disabled={currentPage >= totalPages - 1}
                  className={`
                    relative inline-flex items-center px-2 py-2 rounded-r-md border
                    text-sm font-medium
                    ${currentPage >= totalPages - 1
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      : 'bg-white text-gray-500 hover:bg-gray-50'
                    }
                  `}
                >
                  Next
                </button>
              </nav>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
