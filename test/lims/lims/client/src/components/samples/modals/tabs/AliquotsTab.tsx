import React from 'react';
import { Plus, Beaker } from 'lucide-react';
import { Sample, Aliquot } from '../../../../context/SampleContext';

interface AliquotsTabProps {
  sample: Sample;
  onAddAliquot: () => void;
  onAliquotClick: (aliquotId: string) => void;
  selectedAliquotId?: string | null;
}

export default function AliquotsTab({
  sample,
  onAddAliquot,
  onAliquotClick,
  selectedAliquotId,
}: AliquotsTabProps) {
  // Format date for display
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

  // Check if we can create more aliquots
  // Allow creating aliquots if we have volume or if number_of_aliquots is not set (unlimited)
  const canCreateAliquot = (sample.volume_ml || 0) > 0 || 
    !sample.number_of_aliquots || 
    (sample.aliquots?.length || 0) < (sample.number_of_aliquots || 0);

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-lg font-medium text-gray-900">Sample Aliquots</h3>
        <button
          onClick={onAddAliquot}
          className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 flex items-center transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          disabled={!canCreateAliquot}
        >
          <Plus className="w-4 h-4 mr-2" />
          Create Aliquot
        </button>
      </div>
      
      <div className="bg-white rounded-lg border border-gray-200">
        <div className="px-4 py-3 border-b border-gray-200">
          <div className="grid grid-cols-5 gap-4 text-sm font-medium text-gray-500">
            <div>Aliquot Code</div>
            <div>Volume (mL)</div>
            <div>Status</div>
            <div>Location</div>
            <div>Created At</div>
          </div>
        </div>
        <div className="divide-y divide-gray-200">
          {sample.aliquots && sample.aliquots.length > 0 ? (
            sample.aliquots.map((aliquot) => (
              <div
                key={aliquot.id}
                className={`px-4 py-3 grid grid-cols-5 gap-4 hover:bg-gray-50 cursor-pointer transition-colors ${
                  selectedAliquotId === aliquot.id ? 'bg-blue-50 border-l-4 border-blue-500' : ''
                }`}
                onClick={() => onAliquotClick(aliquot.id)}
              >
                <div className="flex items-center">
                  <Beaker className="w-4 h-4 text-gray-400 mr-2" />
                  <span className="text-sm font-medium text-gray-900">{aliquot.aliquot_code}</span>
                </div>
                <div className="text-sm text-gray-500">
                  {aliquot.volume_ml || aliquot.volume} mL
                </div>
                <div className="text-sm text-gray-500">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    aliquot.status === 'Active' ? 'bg-green-100 text-green-800' :
                    aliquot.status === 'Inactive' ? 'bg-gray-100 text-gray-800' :
                    'bg-yellow-100 text-yellow-800'
                  }`}>
                    {aliquot.status}
                  </span>
                </div>
                <div className="text-sm text-gray-500">
                  {aliquot.location || 'Not specified'}
                </div>
                <div className="text-sm text-gray-500">
                  {formatDate(aliquot.created_at)}
                </div>
              </div>
            ))
          ) : (
            <div className="px-4 py-8 text-center">
              <Beaker className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No Aliquots Created</h3>
              <p className="text-gray-500 mb-4">
                Create your first aliquot by clicking the button above.
              </p>
              {!canCreateAliquot && (
                <p className="text-sm text-yellow-600">
                  No volume available for creating aliquots.
                </p>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Summary Information */}
      <div className="bg-gray-50 rounded-lg p-4">
        <h4 className="text-sm font-medium text-gray-700 mb-3">Aliquot Summary</h4>
        <div className="grid grid-cols-3 gap-4 text-sm">
          <div>
            <span className="text-gray-500">Total Volume:</span>
            <span className="ml-2 font-medium">{sample.volume_ml || 0} mL</span>
          </div>
          <div>
            <span className="text-gray-500">Aliquots Created:</span>
            <span className="ml-2 font-medium">{sample.aliquots?.length || 0}</span>
          </div>
          <div>
            <span className="text-gray-500">Volume Left:</span>
            <span className="ml-2 font-medium">{sample.volume_left || sample.volume_ml || 0} mL</span>
          </div>
        </div>
      </div>
    </div>
  );
}