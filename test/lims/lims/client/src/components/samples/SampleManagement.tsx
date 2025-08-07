import React, { useState, useEffect } from 'react';
import { Plus, List, Columns, Search, Filter, Download, X, Trash2, Loader } from 'lucide-react';
import { useSamples } from '../../context/SampleContext';
import { useMetadata } from '../../context/MetadataContext';
import KanbanView from './views/KanbanView';
import TableView from './views/TableView';
import SampleRegistrationModal from './modals/SampleRegistrationModal';
import EmptyState from './EmptyState';

type ViewMode = 'kanban' | 'table';

interface FilterState {
  type: string[];
  status: string[];
  location: string[];
  owner: string[];
}

interface SampleManagementProps {
  onSampleClick: (sampleId: string) => void;
}

export default function SampleManagement({ onSampleClick }: SampleManagementProps) {
  const [viewMode, setViewMode] = useState<ViewMode>('table');
  const [isRegistrationModalOpen, setIsRegistrationModalOpen] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [sampleToDelete, setSampleToDelete] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState<FilterState>({
    type: [],
    status: [],
    location: [],
    owner: [],
  });

  const { samples, deleteSample, refreshSamples, exportSamples, loading } = useSamples();
  const { sampleTypes, sampleStatuses, labLocations, users, refreshMetadata, loading: metadataLoading } = useMetadata();

  // Load metadata when component mounts and handle filters
  useEffect(() => {
    // Load necessary metadata for filtering
    const loadData = async () => {
      try {
        console.log('Loading metadata...');
        await refreshMetadata();
        console.log('Loading samples...');
        await refreshSamples();
      } catch (error) {
        console.error('Error loading data:', error);
      }
    };

    loadData();
  }, [refreshMetadata, refreshSamples]);

  // Fetch samples whenever filters change
  useEffect(() => {
    // Convert string values to their corresponding IDs for API calls
    const typeIds = filters.type.map(typeValue => {
      const foundType = sampleTypes.find(t => t.value === typeValue);
      return foundType ? foundType.id.toString() : typeValue;
    });
    
    const statusIds = filters.status.map(statusValue => {
      const foundStatus = sampleStatuses.find(s => s.value === statusValue);
      return foundStatus ? foundStatus.id.toString() : statusValue;
    });
    
    const locationIds = filters.location.map(locationValue => {
      const foundLocation = labLocations.find(l => l.value === locationValue);
      return foundLocation ? foundLocation.id.toString() : locationValue;
    });
    
    const ownerIds = filters.owner.map(ownerValue => {
      const foundOwner = users.find(u => u.value === ownerValue);
      return foundOwner ? foundOwner.id.toString() : ownerValue;
    });
    
    const apiFilters = {
      type: typeIds,
      status: statusIds,
      location: locationIds,
      owner: ownerIds,
      search: searchQuery || undefined
    };

    // Use a flag to prevent excessive API calls
    const handler = setTimeout(() => {
      refreshSamples(apiFilters);
    }, 300); // Debounce for 300ms

    return () => clearTimeout(handler);
  }, [filters, searchQuery, refreshSamples, sampleTypes, sampleStatuses, labLocations, users]);

  // Since we're now fetching filtered data from the API, we don't need to filter again
  const filteredSamples = samples;

  const toggleFilter = (category: keyof FilterState, value: string) => {
    setFilters(prev => ({
      ...prev,
      [category]: prev[category].includes(value)
        ? prev[category].filter(v => v !== value)
        : [...prev[category], value]
    }));
  };

  const clearFilters = () => {
    setFilters({
      type: [],
      status: [],
      location: [],
      owner: [],
    });
    setSearchQuery('');
  };

  const handleDeleteSample = () => {
    if (sampleToDelete) {
      deleteSample(sampleToDelete);
      setShowDeleteModal(false);
      setSampleToDelete(null);
    }
  };

  const exportToCSV = async () => {
    try {
      await exportSamples();
    } catch (error) {
      console.error('Export failed:', error);
    }
  };

  const hasActiveFilters = Object.values(filters).some(arr => arr.length > 0) || searchQuery;

  // Check if we have any data loaded
  const hasMetadata = sampleTypes.length > 0 || sampleStatuses.length > 0 || labLocations.length > 0 || users.length > 0;
  const hasSamples = samples.length > 0;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Sample Management</h1>
        <div className="flex items-center space-x-4">
          <button
            onClick={() => setIsRegistrationModalOpen(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center space-x-2"
          >
            <Plus className="w-4 h-4" />
            <span>Add Sample</span>
          </button>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="bg-white p-4 rounded-lg shadow">
        <div className="flex flex-col lg:flex-row gap-4">
          {/* Search */}
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="Search samples..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>

          {/* Filter Toggle */}
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50"
          >
            <Filter className="w-4 h-4" />
            <span>Filters</span>
            {hasActiveFilters && (
              <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                {Object.values(filters).flat().length + (searchQuery ? 1 : 0)}
              </span>
            )}
          </button>
        </div>

        {/* Filters Panel */}
        {showFilters && (
          <div className="mt-4 pt-4 border-t border-gray-200">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Sample Type Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Sample Type</label>
                <div className="space-y-2 max-h-32 overflow-y-auto">
                  {metadataLoading ? (
                    <div className="flex items-center space-x-2 text-sm text-gray-500">
                      <Loader className="w-4 h-4 animate-spin" />
                      <span>Loading...</span>
                    </div>
                  ) : sampleTypes.length > 0 ? (
                    sampleTypes.map((type) => (
                      <label key={type.id} className="flex items-center">
                        <input
                          type="checkbox"
                          checked={filters.type.includes(type.value)}
                          onChange={() => toggleFilter('type', type.value)}
                          className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-700">{type.value}</span>
                      </label>
                    ))
                  ) : (
                    <div className="text-sm text-gray-500">No sample types available</div>
                  )}
                </div>
              </div>

              {/* Status Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Status</label>
                <div className="space-y-2 max-h-32 overflow-y-auto">
                  {metadataLoading ? (
                    <div className="flex items-center space-x-2 text-sm text-gray-500">
                      <Loader className="w-4 h-4 animate-spin" />
                      <span>Loading...</span>
                    </div>
                  ) : sampleStatuses.length > 0 ? (
                    sampleStatuses.map((status) => (
                      <label key={status.id} className="flex items-center">
                        <input
                          type="checkbox"
                          checked={filters.status.includes(status.value)}
                          onChange={() => toggleFilter('status', status.value)}
                          className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-700">{status.value}</span>
                      </label>
                    ))
                  ) : (
                    <div className="text-sm text-gray-500">No statuses available</div>
                  )}
                </div>
              </div>

              {/* Location Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
                <div className="space-y-2 max-h-32 overflow-y-auto">
                  {metadataLoading ? (
                    <div className="flex items-center space-x-2 text-sm text-gray-500">
                      <Loader className="w-4 h-4 animate-spin" />
                      <span>Loading...</span>
                    </div>
                  ) : labLocations.length > 0 ? (
                    labLocations.map((location) => (
                      <label key={location.id} className="flex items-center">
                        <input
                          type="checkbox"
                          checked={filters.location.includes(location.value)}
                          onChange={() => toggleFilter('location', location.value)}
                          className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-700">{location.value}</span>
                      </label>
                    ))
                  ) : (
                    <div className="text-sm text-gray-500">No locations available</div>
                  )}
                </div>
              </div>

              {/* Owner Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Owner</label>
                <div className="space-y-2 max-h-32 overflow-y-auto">
                  {metadataLoading ? (
                    <div className="flex items-center space-x-2 text-sm text-gray-500">
                      <Loader className="w-4 h-4 animate-spin" />
                      <span>Loading...</span>
                    </div>
                  ) : users.length > 0 ? (
                    users.map((user) => (
                      <label key={user.id} className="flex items-center">
                        <input
                          type="checkbox"
                          checked={filters.owner.includes(user.value)}
                          onChange={() => toggleFilter('owner', user.value)}
                          className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-700">{user.value}</span>
                      </label>
                    ))
                  ) : (
                    <div className="text-sm text-gray-500">No users available</div>
                  )}
                </div>
              </div>
            </div>

            {/* Clear Filters */}
            {hasActiveFilters && (
              <div className="mt-4 pt-4 border-t border-gray-200">
                <button
                  onClick={clearFilters}
                  className="flex items-center space-x-2 text-sm text-gray-600 hover:text-gray-800"
                >
                  <X className="w-4 h-4" />
                  <span>Clear all filters</span>
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* View Mode Toggle */}
      <div className="flex justify-between items-center">
        <div className="flex items-center space-x-2 bg-white p-1 rounded-lg shadow">
          <button
            onClick={() => setViewMode('table')}
            className={`px-3 py-1 rounded-md text-sm font-medium ${
              viewMode === 'table'
                ? 'bg-blue-100 text-blue-700'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            <List className="w-4 h-4" />
          </button>
          <button
            onClick={() => setViewMode('kanban')}
            className={`px-3 py-1 rounded-md text-sm font-medium ${
              viewMode === 'kanban'
                ? 'bg-blue-100 text-blue-700'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            <Columns className="w-4 h-4" />
          </button>
        </div>

        <button
          onClick={exportToCSV}
          className="flex items-center space-x-2 text-gray-600 hover:text-gray-800"
        >
          <Download className="w-4 h-4" />
          <span>Export CSV</span>
        </button>
      </div>

      {/* Content */}
      {loading ? (
        <div className="flex justify-center items-center py-12">
          <Loader className="w-8 h-8 animate-spin text-blue-600" />
        </div>
      ) : !hasSamples ? (
        <EmptyState
          onAddSample={() => setIsRegistrationModalOpen(true)}
          hasFilters={hasActiveFilters}
          onClearFilters={clearFilters}
        />
      ) : (
        <div className="bg-white rounded-lg shadow">
          {viewMode === 'table' ? (
            <TableView
              samples={filteredSamples}
              onSampleClick={onSampleClick}
              onDeleteSample={(id) => {
                setSampleToDelete(id);
                setShowDeleteModal(true);
              }}
            />
          ) : (
            <KanbanView
              onSampleClick={onSampleClick}
              onDeleteSample={(id) => {
                setSampleToDelete(id);
                setShowDeleteModal(true);
              }}
            />
          )}
        </div>
      )}

      {/* Sample Registration Modal */}
      <SampleRegistrationModal
        isOpen={isRegistrationModalOpen}
        onClose={() => setIsRegistrationModalOpen(false)}
        onSampleCreated={() => {
          setIsRegistrationModalOpen(false);
          refreshSamples();
        }}
      />

      {/* Delete Confirmation Modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Delete Sample</h3>
            <p className="text-gray-600 mb-6">
              Are you sure you want to delete this sample? This action cannot be undone.
            </p>
            <div className="flex justify-end space-x-3">
              <button
                onClick={() => setShowDeleteModal(false)}
                className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={handleDeleteSample}
                className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}