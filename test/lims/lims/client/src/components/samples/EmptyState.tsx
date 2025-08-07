import React from 'react';
import { Beaker, Filter } from 'lucide-react';

interface EmptyStateProps {
  hasFilters?: boolean;
  onClearFilters?: () => void;
}

export default function EmptyState({ hasFilters = false, onClearFilters }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 px-4">
      <div className="text-center max-w-md">
        {/* Icon */}
        <div className="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-blue-100 mb-6">
          <Beaker className="h-8 w-8 text-blue-600" />
        </div>

        {/* Title */}
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          {hasFilters ? 'No samples found' : 'No samples found'}
        </h3>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          {hasFilters && onClearFilters ? (
            <button
              onClick={onClearFilters}
              className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <Filter className="h-4 w-4 mr-2" />
            </button>
          ) : null}
        </div>

        {/* Additional help text */}
        {!hasFilters && (
          <div className="mt-8 text-sm text-gray-400">
            <div className="flex items-center justify-center space-x-4 text-xs">
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
