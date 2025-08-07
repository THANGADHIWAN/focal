import React from 'react';
import { Edit2, CheckCircle2, ChevronRight } from 'lucide-react';
import { Sample } from '../../../../context/SampleContext';
import { useMetadata } from '../../../../context/MetadataContext';

interface SampleDetailsTabProps {
  sample: Sample;
  isEditingMetadata: boolean;
  isEditingStatus: boolean;
  isEditingLocation: boolean;
  selectedType: string;
  selectedOwner: string;
  selectedStatus: string;
  selectedLocation: string;
  onEditMetadata: () => void;
  onEditStatus: () => void;
  onEditLocation: () => void;
  onTypeChange: (value: string) => void;
  onOwnerChange: (value: string) => void;
  onStatusChange: (value: string) => void;
  onLocationChange: (value: string) => void;
  onSaveMetadata: () => void;
  onSaveStatus: () => void;
  onSaveLocation: () => void;
}

// Sample stages for progress tracking
const SAMPLE_STAGES = [
  {
    id: 'Logged_In',
    name: 'Sample Logged In',
    description: 'Sample has been registered in the system'
  },
  {
    id: 'In_Progress',
    name: 'In Progress',
    description: 'Sample is being processed'
  },
  {
    id: 'Testing',
    name: 'Testing',
    description: 'Sample is undergoing testing'
  },
  {
    id: 'Completed',
    name: 'Completed',
    description: 'All tests have been completed'
  },
  {
    id: 'Archived',
    name: 'Archived',
    description: 'Sample has been archived in storage'
  }
];

export default function SampleDetailsTab({
  sample,
  isEditingMetadata,
  isEditingStatus,
  isEditingLocation,
  selectedType,
  selectedOwner,
  selectedStatus,
  selectedLocation,
  onEditMetadata,
  onEditStatus,
  onEditLocation,
  onTypeChange,
  onOwnerChange,
  onStatusChange,
  onLocationChange,
  onSaveMetadata,
  onSaveStatus,
  onSaveLocation,
}: SampleDetailsTabProps) {
  // Use API data instead of hardcoded constants
  const { sampleTypes, sampleStatuses, labLocations, users, storageLocations } = useMetadata();

  // Format dates for display
  const formatDate = (dateString?: string) => {
    if (!dateString) return 'Not specified';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  // Get current stage index for progress calculation
  const currentStageIndex = SAMPLE_STAGES.findIndex(stage => stage.id === sample.status);
  const progressPercentage = currentStageIndex >= 0 ? ((currentStageIndex + 1) / SAMPLE_STAGES.length) * 100 : 0;

  // Sample Information
  const sampleInfo = [
    { label: 'Sample Code', value: sample.sample_code },
    { label: 'Sample Name', value: sample.sample_name },
    { label: 'Type', value: sample.type_name || `Type ${sample.sample_type_id}` },
    { label: 'Created By', value: sample.created_by },
    { label: 'Created At', value: formatDate(sample.created_at) },
    { label: 'Updated At', value: sample.updated_at ? formatDate(sample.updated_at) : 'Not updated' },
  ];

  // Volume Information
  const volumeInfo = [
    { label: 'Total Volume (mL)', value: sample.volume_ml || 0 },
    { label: 'Aliquots Created', value: sample.number_of_aliquots || sample.aliquots?.length || 0 },
    { label: 'Volume Left (mL)', value: sample.volume_ml ? sample.volume_ml - (sample.aliquots?.reduce((sum, a) => sum + (a.volume_ml || 0), 0) || 0) : 0 },
  ];

  // Storage Information
  const storageInfo = [
    { label: 'Box ID', value: sample.box_id || 'Not assigned' },
    { label: 'Priority', value: sample.priority || 'Not set' },
    { label: 'Status', value: sample.status },
    { label: 'Quantity', value: sample.quantity || 'Not specified' },
  ];

  return (
    <div className="space-y-6">
      {/* Sample Metadata */}
      <div className="bg-gray-50 rounded-lg p-4">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-medium text-gray-700">
            Sample Information
          </h3>
          <button
            onClick={onEditMetadata}
            className="text-sm text-blue-600 hover:text-blue-700 flex items-center transition-colors"
          >
            <Edit2 className="w-4 h-4 mr-1" />
            {isEditingMetadata ? 'Cancel' : 'Edit'}
          </button>
        </div>
        <div className="grid grid-cols-3 gap-4">
          <div>
            <label className="block text-xs text-gray-500 mb-1">
              Sample Code
            </label>
            <span className="text-sm font-medium">
              {sample.sample_code}
            </span>
          </div>
          <div>
            <label className="block text-xs text-gray-500 mb-1">
              Sample Name
            </label>
            {isEditingMetadata ? (
              <input
                type="text"
                value={selectedType || sample.sample_name}
                onChange={(e) => onTypeChange(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter sample name"
              />
            ) : (
              <span className="text-sm font-medium">
                {sample.sample_name}
              </span>
            )}
          </div>
          <div>
            <label className="block text-xs text-gray-500 mb-1">
              Sample Type
            </label>
            <span className="text-sm font-medium">
              {sample.type_name || `Type ${sample.sample_type_id}`}
            </span>
          </div>
        </div>
        <div className="grid grid-cols-3 gap-4 mt-4">
          <div>
            <label className="block text-xs text-gray-500 mb-1">
              Created By
            </label>
            {isEditingMetadata ? (
              <select
                value={selectedOwner || sample.created_by}
                onChange={(e) => onOwnerChange(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Select user...</option>
                {users.map(user => (
                  <option key={user.id} value={user.name}>{user.name}</option>
                ))}
              </select>
            ) : (
              <span className="text-sm font-medium">
                {sample.created_by}
              </span>
            )}
          </div>
          <div>
            <label className="block text-xs text-gray-500 mb-1">
              Created Date
            </label>
            <span className="text-sm font-medium">
              {formatDate(sample.created_at)}
            </span>
          </div>
          <div>
            <label className="block text-xs text-gray-500 mb-1">
              Last Updated
            </label>
            <span className="text-sm font-medium">
              {sample.updated_at ? formatDate(sample.updated_at) : 'Not updated'}
            </span>
          </div>
        </div>
        {isEditingMetadata && (
          <div className="flex justify-end mt-4">
            <button
              onClick={onSaveMetadata}
              className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
            >
              Save Changes
            </button>
          </div>
        )}
      </div>

      {/* Status Update */}
      <div className="bg-gray-50 rounded-lg p-4">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-lg font-medium text-gray-900">
            Sample Progress
          </h3>
        </div>

        <div className="relative mt-8">
          {/* Progress Bar */}
          <div className="absolute top-4 left-0 right-0 h-1 bg-gray-200">
            <div
              className="h-full bg-green-500 transition-all duration-300"
              style={{
                width: `${progressPercentage}%`
              }}
            />
          </div>

          {/* Stages */}
          <div className="relative flex justify-between">
            {SAMPLE_STAGES.map((stage, index) => {
              const isCompleted = currentStageIndex >= index;
              const isCurrent = stage.id === sample.status;

              return (
                <div
                  key={stage.id}
                  className="flex flex-col items-center relative"
                  style={{ width: '20%' }}
                >
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center border-2 ${
                      isCompleted
                        ? 'bg-green-500 border-green-500 text-white'
                        : 'bg-white border-gray-300'
                    }`}
                  >
                    {isCompleted && <CheckCircle2 className="w-5 h-5" />}
                  </div>
                  <span className={`mt-2 text-sm font-medium text-center ${
                    isCompleted ? 'text-green-600' : 'text-gray-500'
                  }`}>
                    {stage.name}
                  </span>
                </div>
              );
            })}
          </div>

          {/* Complete Button */}
          {sample.status !== 'Archived' && (
            <div className="flex justify-end mt-8">
              <button
                onClick={async () => {
                  const currentIndex = SAMPLE_STAGES.findIndex(s => s.id === sample.status);
                  const nextStage = SAMPLE_STAGES[currentIndex + 1];
                  if (nextStage) {
                    await onStatusChange(nextStage.id);
                    await onSaveStatus();
                  }
                }}
                className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 flex items-center transition-colors"
              >
                Mark Stage as Complete
                <ChevronRight className="w-4 h-4 ml-1" />
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Volume Information */}
      <div className="bg-gray-50 rounded-lg p-4">
        <div className="flex items-center mb-3">
          <h3 className="text-sm font-medium text-gray-700">
            Volume Information
          </h3>
        </div>
        <div className="grid grid-cols-3 gap-4">
          <div>
            <label className="block text-xs text-gray-500">
              Total Volume
            </label>
            <span className="text-sm font-medium">
              {sample.volume_ml ? `${sample.volume_ml} mL` : 'Not specified'}
            </span>
          </div>
          <div>
            <label className="block text-xs text-gray-500">
              Aliquots Created
            </label>
            <span className="text-sm font-medium">
              {sample.number_of_aliquots || sample.aliquots?.length || 0}
            </span>
          </div>
          <div>
            <label className="block text-xs text-gray-500">
              Volume Left
            </label>
            <span className="text-sm font-medium">
              {sample.volume_ml ? sample.volume_ml - (sample.aliquots?.reduce((sum, a) => sum + (a.volume_ml || 0), 0) || 0) : 0}
            </span>
          </div>
        </div>
        {sample.purpose && (
          <div className="mt-4">
            <label className="block text-xs text-gray-500 mb-1">
              Purpose
            </label>
            <span className="text-sm font-medium">
              {sample.purpose}
            </span>
          </div>
        )}
      </div>

      {/* Storage Information */}
      <div className="bg-gray-50 rounded-lg p-4">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-medium text-gray-700">
            Storage Location
          </h3>
          <button
            onClick={onEditLocation}
            className="text-sm text-blue-600 hover:text-blue-700 flex items-center transition-colors"
          >
            <Edit2 className="w-4 h-4 mr-1" />
            {isEditingLocation ? 'Cancel' : 'Update Location'}
          </button>
        </div>
        <div className={`grid grid-cols-5 gap-4 ${isEditingLocation ? 'opacity-50' : ''}`}>
          <div className="bg-white rounded-lg p-3 border border-gray-200">
            <label className="block text-xs text-gray-500 mb-1">Lab</label>
            <span className="text-sm font-medium text-gray-900">
              {sample.location || 'Not specified'}
            </span>
          </div>
          <div className="bg-white rounded-lg p-3 border border-gray-200">
            <label className="block text-xs text-gray-500 mb-1">Box ID</label>
            <span className="text-sm font-medium text-gray-900">
              {sample.box_id || 'Not assigned'}
            </span>
          </div>
          <div className="bg-white rounded-lg p-3 border border-gray-200">
            <label className="block text-xs text-gray-500 mb-1">Priority</label>
            <span className="text-sm font-medium text-gray-900">
              {sample.priority || 'Medium'}
            </span>
          </div>
          <div className="bg-white rounded-lg p-3 border border-gray-200">
            <label className="block text-xs text-gray-500 mb-1">Status</label>
            <span className="text-sm font-medium text-gray-900">
              {sample.status}
            </span>
          </div>
          <div className="bg-white rounded-lg p-3 border border-gray-200">
            <label className="block text-xs text-gray-500 mb-1">Quantity</label>
            <span className="text-sm font-medium text-gray-900">
              {sample.quantity ? `${sample.quantity}` : 'Not specified'}
            </span>
          </div>
        </div>
        {isEditingLocation && (
          <div className="mt-4 space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm text-gray-700 mb-1">
                  Box ID
                </label>
                <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option value="">Select box...</option>
                  {storageLocations && storageLocations.map(location => (
                    <option key={location.id} value={location.id}>{location.name}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm text-gray-700 mb-1">
                  Lab Location
                </label>
                <select
                  value={selectedLocation || sample.location}
                  onChange={(e) => onLocationChange(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Select lab...</option>
                  {labLocations.map((lab) => (
                    <option key={lab.id} value={lab.name}>{lab.name}</option>
                  ))}
                </select>
              </div>
            </div>
            <div className="flex justify-end">
              <button
                onClick={onSaveLocation}
                className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
              >
                Update Location
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}