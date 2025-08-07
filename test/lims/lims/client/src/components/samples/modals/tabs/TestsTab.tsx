import React from 'react';
import { Plus, FlaskConical, CheckCircle2, XCircle, Clock3, AlertCircle, Beaker, Eye } from 'lucide-react';
import { Sample, Aliquot, Test } from '../../../../context/SampleContext';
import { useNavigate, useLocation } from 'react-router-dom';

interface TestsTabProps {
  sample: Sample;
  allTests: Test[];
  onAddTest: (testData: any) => void;
  onTestClick: (testId: string) => void;
  selectedAliquotId?: string | null;
}

export default function TestsTab({
  sample,
  allTests,
  onAddTest,
  onTestClick,
  selectedAliquotId,
}: TestsTabProps) {
  const navigate = useNavigate();
  const location = useLocation();
  
  // Collect all tests from all aliquots
  const allSampleTests = sample.aliquots?.flatMap(aliquot => 
    aliquot.tests?.map(test => ({
      ...test,
      aliquotId: aliquot.id,
      aliquotCode: aliquot.aliquot_code,
      aliquotVolume: aliquot.volume_ml || aliquot.volume,
      aliquotLocation: aliquot.location
    })) || []
  ) || [];

  // Filter tests by selected aliquot if specified
  const displayTests = selectedAliquotId 
    ? allSampleTests.filter(test => test.aliquotId === selectedAliquotId)
    : allSampleTests;

  const handleViewTest = (testId: string) => {
    onTestClick(testId);
  };

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

  // Get status color and icon
  const getStatusInfo = (status: string) => {
    switch (status?.toLowerCase()) {
      case 'completed':
        return { color: 'bg-green-100 text-green-800', icon: CheckCircle2 };
      case 'failed':
        return { color: 'bg-red-100 text-red-800', icon: XCircle };
      case 'in_progress':
      case 'in progress':
        return { color: 'bg-blue-100 text-blue-800', icon: Clock3 };
      case 'pending':
        return { color: 'bg-yellow-100 text-yellow-800', icon: AlertCircle };
      default:
        return { color: 'bg-gray-100 text-gray-800', icon: AlertCircle };
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h3 className="text-lg font-medium text-gray-900">Tests</h3>
          <p className="text-sm text-gray-500 mt-1">
            {selectedAliquotId 
              ? `Tests for selected aliquot` 
              : `All tests for this sample (${displayTests.length} total)`
            }
          </p>
        </div>
        {selectedAliquotId && (
          <button
            onClick={() => onAddTest({ aliquot_id: selectedAliquotId })}
            className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 flex items-center transition-colors"
          >
            <Plus className="w-4 h-4 mr-2" />
            Add Test
          </button>
        )}
      </div>

      {displayTests.length === 0 ? (
        <div className="text-center py-12">
          <FlaskConical className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Tests Added</h3>
          <p className="text-gray-500">
            {selectedAliquotId 
              ? 'This aliquot has no tests. Click "Add Test" to add one.'
              : 'This sample has no tests.'
            }
          </p>
        </div>
      ) : (
        <div className="bg-white rounded-lg border border-gray-200">
          <div className="px-4 py-3 border-b border-gray-200">
            <div className="grid grid-cols-7 gap-4 text-sm font-medium text-gray-500">
              <div>Test ID</div>
              <div>Test Name</div>
              <div>Aliquot</div>
              <div>Status</div>
              <div>Analyst</div>
              <div>Scheduled Date</div>
              <div>Actions</div>
            </div>
          </div>
          <div className="divide-y divide-gray-200">
            {displayTests.map((test) => {
              const statusInfo = getStatusInfo(test.status);
              const StatusIcon = statusInfo.icon;

              return (
                <div
                  key={test.id}
                  className="px-4 py-3 grid grid-cols-7 gap-4 hover:bg-gray-50 cursor-pointer transition-colors"
                >
                  <div className="flex items-center">
                    <FlaskConical className="w-4 h-4 text-gray-400 mr-2" />
                    <span className="text-sm font-medium text-gray-900">{test.id}</span>
                  </div>
                  <div className="text-sm text-gray-900">
                    {test.test_name || test.name || 'Unnamed Test'}
                  </div>
                  <div className="text-sm text-gray-500">
                    <div className="flex items-center">
                      <Beaker className="w-4 h-4 mr-1 text-gray-400" />
                      <span>{test.aliquotCode || test.aliquotId}</span>
                    </div>
                    <div className="text-xs text-gray-400 mt-1">
                      {test.aliquotVolume} mL • {test.aliquotLocation || 'No location'}
                    </div>
                  </div>
                  <div>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${statusInfo.color}`}>
                      <StatusIcon className="w-3 h-3 mr-1" />
                      {test.status}
                    </span>
                  </div>
                  <div className="text-sm text-gray-500">
                    {test.analyst_id || 'Not assigned'}
                  </div>
                  <div className="text-sm text-gray-500">
                    {test.scheduled_date ? formatDate(test.scheduled_date) : 'Not scheduled'}
                  </div>
                  <div className="flex items-center justify-center">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleViewTest(test.id);
                      }}
                      className="p-1 text-blue-600 hover:text-blue-800 rounded-full hover:bg-blue-50 transition-colors"
                    >
                      <Eye className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Test Summary */}
      {displayTests.length > 0 && (
        <div className="bg-gray-50 rounded-lg p-4">
          <h4 className="text-sm font-medium text-gray-700 mb-3">Test Summary</h4>
          <div className="grid grid-cols-4 gap-4 text-sm">
            <div>
              <span className="text-gray-500">Total Tests:</span>
              <span className="ml-2 font-medium">{displayTests.length}</span>
            </div>
            <div>
              <span className="text-gray-500">Completed:</span>
              <span className="ml-2 font-medium">
                {displayTests.filter(t => t.status?.toLowerCase() === 'completed').length}
              </span>
            </div>
            <div>
              <span className="text-gray-500">In Progress:</span>
              <span className="ml-2 font-medium">
                {displayTests.filter(t => t.status?.toLowerCase().includes('progress')).length}
              </span>
            </div>
            <div>
              <span className="text-gray-500">Pending:</span>
              <span className="ml-2 font-medium">
                {displayTests.filter(t => t.status?.toLowerCase() === 'pending').length}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}