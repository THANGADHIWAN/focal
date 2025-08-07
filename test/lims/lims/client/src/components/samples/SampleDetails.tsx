import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { ArrowLeft, Loader, AlertCircle } from 'lucide-react';
import { useSamples } from '../../context/SampleContext';
import { useTests } from '../../context/TestContext';
import SampleDetailsTab from './modals/tabs/SampleDetailsTab';
import TimelineTab from './modals/tabs/TimelineTab';
import NotesTab from './modals/tabs/NotesTab';
import AttachmentsTab from './modals/tabs/AttachmentsTab';
import AliquotsTab from './modals/tabs/AliquotsTab';
import TestsTab from './modals/tabs/TestsTab';
import CreateAliquotModal from './modals/CreateAliquotModal';

// Mock data for timeline, notes, and attachments
const mockSampleData = {
  timeline: [
    {
      event: 'Sample registered',
      date: '2025-01-15 09:00',
      user: 'John Doe'
    },
    {
      event: 'Processing started',
      date: '2025-01-15 10:30',
      user: 'Jane Smith'
    },
    {
      event: 'Moved to Testing',
      date: '2025-01-16 14:15',
      user: 'Mike Johnson'
    }
  ],
  notes: [
    {
      id: '1',
      user: 'John Doe',
      date: '2025-01-15 09:00',
      content: 'Sample received in good condition'
    },
    {
      id: '2',
      user: 'Jane Smith',
      date: '2025-01-15 10:30',
      content: 'Initial processing completed, ready for analysis'
    }
  ],
  attachments: [
    {
      id: '1',
      name: 'sample_report.pdf',
      size: '2.4 MB',
      date: '2025-01-15 09:00'
    },
    {
      id: '2',
      name: 'analysis_results.xlsx',
      size: '1.8 MB',
      date: '2025-01-16 14:15'
    }
  ]
};

export default function SampleDetails() {
  const { sampleId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const { samples, updateSample, addAliquot, addTest, refreshSamples, loading: samplesLoading, error: samplesError, setSamples, getSampleById } = useSamples();
  const { tests: allTests } = useTests();
  
  const [activeTab, setActiveTab] = useState<'details' | 'timeline' | 'notes' | 'attachments' | 'aliquots' | 'tests'>('details');
  const [isEditingMetadata, setIsEditingMetadata] = useState(false);
  const [isEditingStatus, setIsEditingStatus] = useState(false);
  const [isEditingLocation, setIsEditingLocation] = useState(false);
  const [selectedType, setSelectedType] = useState('');
  const [selectedOwner, setSelectedOwner] = useState('');
  const [isCreatingAliquot, setIsCreatingAliquot] = useState(false);
  const [newAliquotVolume, setNewAliquotVolume] = useState(1);
  const [selectedAliquotBoxId, setSelectedAliquotBoxId] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('');
  const [selectedLocation, setSelectedLocation] = useState('');
  const [selectedAliquotId, setSelectedAliquotId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [updating, setUpdating] = useState(false);

  const boxLocations = {
    'box1': {
      drawer: 'D1',
      rack: 'R1',
      shelf: 'S1',
      freezer: 'F1',
      lab: 'Lab 1'
    },
    'box2': {
      drawer: 'D2',
      rack: 'R2',
      shelf: 'S2',
      freezer: 'F2',
      lab: 'Lab 2'
    }
  };

  // Load samples if not already loaded
  useEffect(() => {
    const loadSamples = async () => {
      if (samples.length === 0 && !samplesLoading) {
        setLoading(true);
        try {
          await refreshSamples();
        } catch (err) {
          console.error('Failed to load samples:', err);
          setError('Failed to load samples. Please try again.');
        } finally {
          setLoading(false);
        }
      } else {
        setLoading(false);
      }
    };

    loadSamples();
  }, [samples.length, samplesLoading, refreshSamples]);

  // Find the sample by ID - handle both string and number IDs
  const sample = samples.find(s => {
    // Convert both to strings for comparison
    const sampleIdStr = String(s.id);
    const urlSampleIdStr = String(sampleId);
    return sampleIdStr === urlSampleIdStr;
  });

  // If sample not found in loaded samples, try to fetch it directly
  useEffect(() => {
    const fetchSampleDirectly = async () => {
      if (!sample && sampleId && !loading && !samplesLoading) {
        try {
          setLoading(true);
          const fetchedSample = await getSampleById(sampleId);
          if (fetchedSample) {
            // Add the fetched sample to the samples array
            setSamples(prev => [...prev, fetchedSample]);
          }
        } catch (err) {
          console.error('Failed to fetch sample directly:', err);
          setError('Failed to load sample details. Please try again.');
        } finally {
          setLoading(false);
        }
      }
    };

    fetchSampleDirectly();
  }, [sample, sampleId, loading, samplesLoading, getSampleById, setSamples]);

  // Show loading state
  if (loading || samplesLoading) {
    return (
      <div className="p-6 flex items-center justify-center min-h-screen">
        <div className="flex items-center space-x-2">
          <Loader className="w-6 h-6 animate-spin text-blue-600" />
          <span className="text-gray-600">Loading sample details...</span>
        </div>
      </div>
    );
  }

  // Show error state
  if (error || samplesError) {
    return (
      <div className="p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center">
            <button
              onClick={() => navigate('/')}
              className="mr-4 text-gray-500 hover:text-gray-700"
            >
              <ArrowLeft className="w-6 h-6" />
            </button>
            <div>
              <h1 className="text-2xl font-semibold text-gray-900">
                Error Loading Sample
              </h1>
              <p className="text-sm text-gray-500 mt-1">
                {error || samplesError}
              </p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center space-x-2 text-red-600 mb-4">
            <AlertCircle className="w-5 h-5" />
            <span className="font-medium">Error</span>
          </div>
          <p className="text-gray-600 mb-4">
            There was an error loading the sample details. Please try again.
          </p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  // Show not found state
  if (!sample) {
    return (
      <div className="p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center">
            <button
              onClick={() => navigate('/')}
              className="mr-4 text-gray-500 hover:text-gray-700"
            >
              <ArrowLeft className="w-6 h-6" />
            </button>
            <div>
              <h1 className="text-2xl font-semibold text-gray-900">
                Sample Not Found
              </h1>
              <p className="text-sm text-gray-500 mt-1">
                The requested sample could not be found.
              </p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center space-x-2 text-yellow-600 mb-4">
            <AlertCircle className="w-5 h-5" />
            <span className="font-medium">Not Found</span>
          </div>
          <p className="text-gray-600 mb-4">
            The sample you're looking for doesn't exist or you don't have permission to view it.
          </p>
          <button
            onClick={() => navigate('/')}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Back to Samples
          </button>
        </div>
      </div>
    );
  }

  // Handler for navigating to test details
  const handleTestClick = (testId: string) => {
    if (selectedAliquotId) {
      navigate(`/samples/${sampleId}/aliquots/${selectedAliquotId}/tests/${testId}`);
    }
  };

  const selectedAliquot = selectedAliquotId ? sample?.aliquots?.find((a: any) => a.id === parseInt(selectedAliquotId)) || null : null;

  const TabButton = ({ tab, label }: { tab: 'details' | 'timeline' | 'notes' | 'attachments' | 'aliquots' | 'tests'; label: string }) => (
    <button
      onClick={() => setActiveTab(tab)}
      className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
        activeTab === tab
          ? 'bg-blue-50 text-blue-600'
          : 'text-gray-600 hover:text-gray-900'
      }`}
    >
      {label}
    </button>
  );

  const handleUpdateSample = async (updates: any) => {
    setUpdating(true);
    try {
      await updateSample(String(sample.id), updates);
    } catch (err) {
      console.error('Failed to update sample:', err);
      setError('Failed to update sample. Please try again.');
    } finally {
      setUpdating(false);
    }
  };

  const handleCreateAliquot = async (volume: number, purpose?: string) => {
    setUpdating(true);
    try {
      await addAliquot(String(sample.id), { volume, purpose });
      setIsCreatingAliquot(false);
      setNewAliquotVolume(1);
      setSelectedAliquotBoxId('');
    } catch (err) {
      console.error('Failed to create aliquot:', err);
      setError('Failed to create aliquot. Please try again.');
    } finally {
      setUpdating(false);
    }
  };

  return (
    <div className="p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center">
          <button
            onClick={() => navigate('/')}
            className="mr-4 text-gray-500 hover:text-gray-700 transition-colors"
          >
            <ArrowLeft className="w-6 h-6" />
          </button>
          <div>
            <h1 className="text-2xl font-semibold text-gray-900">
              Sample Details
            </h1>
            <p className="text-sm text-gray-500 mt-1">
              {sample.sample_code} - {sample.sample_name}
            </p>
          </div>
        </div>
        {updating && (
          <div className="flex items-center space-x-2 text-blue-600">
            <Loader className="w-4 h-4 animate-spin" />
            <span className="text-sm">Updating...</span>
          </div>
        )}
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex space-x-2">
            <TabButton tab="details" label="Details" />
            <TabButton tab="aliquots" label="Aliquots" />
            <TabButton tab="tests" label="Tests" />
            <TabButton tab="timeline" label="Timeline" />
            <TabButton tab="notes" label="Notes" />
            <TabButton tab="attachments" label="Attachments" />
          </div>
        </div>

        <div className="p-6">
          {activeTab === 'details' && (
            <SampleDetailsTab
              sample={sample}
              isEditingMetadata={isEditingMetadata}
              isEditingStatus={isEditingStatus}
              isEditingLocation={isEditingLocation}
              selectedType={selectedType}
              selectedOwner={selectedOwner}
              selectedStatus={selectedStatus}
              selectedLocation={selectedLocation}
              onEditMetadata={() => setIsEditingMetadata(!isEditingMetadata)}
              onEditStatus={() => setIsEditingStatus(!isEditingStatus)}
              onEditLocation={() => setIsEditingLocation(!isEditingLocation)}
              onTypeChange={setSelectedType}
              onOwnerChange={setSelectedOwner}
              onStatusChange={(status) => {
                setSelectedStatus(status);
                handleUpdateSample({ status });
              }}
              onLocationChange={setSelectedLocation}
              onSaveMetadata={() => {
                if (selectedType || selectedOwner) {
                  handleUpdateSample({
                    sample_name: selectedType || sample.sample_name,
                    created_by: selectedOwner || sample.created_by,
                  });
                }
                setIsEditingMetadata(false);
              }}
              onSaveStatus={() => {
                if (selectedStatus) {
                  handleUpdateSample({ status: selectedStatus });
                }
                setIsEditingStatus(false);
              }}
              onSaveLocation={() => {
                if (selectedLocation) {
                  handleUpdateSample({ location: selectedLocation });
                }
                setIsEditingLocation(false);
              }}
            />
          )}
          {activeTab === 'aliquots' && (
            <AliquotsTab
              sample={sample}
              onAddAliquot={() => setIsCreatingAliquot(true)}
              onAliquotClick={(aliquotId) => setSelectedAliquotId(aliquotId)}
              selectedAliquotId={selectedAliquotId}
            />
          )}
          {activeTab === 'tests' && (
            <TestsTab
              sample={sample}
              allTests={allTests}
              onAddTest={(testData) => {
                if (selectedAliquotId) {
                  addTest(String(sample.id), selectedAliquotId, testData);
                }
              }}
              onTestClick={handleTestClick}
              selectedAliquotId={selectedAliquotId}
            />
          )}
          {activeTab === 'timeline' && (
            <TimelineTab 
              sampleId={String(sample.id)}
              onTimelineLoad={(events) => {
                console.log('Timeline loaded:', events);
              }}
            />
          )}
          {activeTab === 'notes' && (
            <NotesTab notes={mockSampleData.notes} />
          )}
          {activeTab === 'attachments' && (
            <AttachmentsTab attachments={mockSampleData.attachments} />
          )}
        </div>
      </div>

      {/* Create Aliquot Modal */}
      <CreateAliquotModal
        isOpen={isCreatingAliquot}
        onClose={() => setIsCreatingAliquot(false)}
        onConfirm={handleCreateAliquot}
        volume={newAliquotVolume}
        onVolumeChange={setNewAliquotVolume}
        boxId={selectedAliquotBoxId}
        onBoxIdChange={setSelectedAliquotBoxId}
        maxVolume={sample.volume_ml || 0}
      />
    </div>
  );
}