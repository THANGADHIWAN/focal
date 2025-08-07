import { createContext, useContext, useState, ReactNode, useEffect, useCallback } from 'react';
import API from '../api';
import { Sample, Aliquot, Test } from '../types/api';
import { TimelineEvent } from '../api/services/timelineService';

// Re-export types for consumers
export type { Sample, Aliquot, Test };

interface SampleContextType {
  samples: Sample[];
  loading: boolean;
  error: string | null;
  setSamples: React.Dispatch<React.SetStateAction<Sample[]>>;
  addSample: (sample: {
    name: string;
    type: number;
    owner: string;
    box_id?: number;
    volume: number;
    notes?: string;
  }) => Promise<Sample>;
  getSampleById: (id: string) => Promise<Sample | null>;
  deleteSample: (id: string) => Promise<void>;
  updateSample: (id: string, updates: Partial<Sample>) => Promise<Sample>;
  addAliquot: (sampleId: string, aliquot: { volume: number, purpose?: string }) => Promise<Aliquot>;
  addTest: (sampleId: string, aliquotId: string, test: { test_master_id: number, analyst_id?: string, instrument_id?: number, scheduled_date?: string, remarks?: string }) => Promise<Test>;
  refreshSamples: (filters?: {
    type?: string[],
    status?: string[],
    location?: string[],
    owner?: string[],
    search?: string
  }) => Promise<void>;
  exportSamples: (filters?: {
    type?: string[],
    status?: string[],
    location?: string[],
    owner?: string[],
    search?: string
  }) => Promise<void>;
  getSampleTimeline: (sampleId: string) => Promise<TimelineEvent[]>;
  getAliquotTimeline: (sampleId: string, aliquotId: string) => Promise<TimelineEvent[]>;
  getTestTimeline: (sampleId: string, testId: string) => Promise<TimelineEvent[]>;
}

const SampleContext = createContext<SampleContextType | undefined>(undefined);

export function SampleProvider({ children }: { children: ReactNode }) {
  const [samples, setSamples] = useState<Sample[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [page] = useState<number>(1);
  const [limit] = useState<number>(100); // Default limit, can be adjusted

  const refreshSamples = useCallback(async (filters?: {
    type?: string[],
    status?: string[],
    location?: string[],
    owner?: string[],
    search?: string
  }) => {
    try {
      setLoading(true);
      setError(null);
      
      // Test API connection first
      const isConnected = await API.samples.testConnection();
      if (!isConnected) {
        throw new Error('Unable to connect to the API server. Please check if the server is running.');
      }
      
      console.log('[SampleContext] Refreshing samples with filters:', filters);
      const response = await API.samples.getAllSamples(page, limit, filters);
      console.log('[SampleContext] Samples loaded:', response);
      setSamples(response.data);
    } catch (err) {
      console.error('[SampleContext] Failed to fetch samples:', err);
      setError(err instanceof Error ? err.message : 'Failed to load samples. Please try again later.');
    } finally {
      setLoading(false);
    }
  }, [page, limit]);

  // Don't load samples automatically when the component mounts
  // They will be loaded when a specific component needs them

  const addSample = async (sampleData: {
    name: string;
    type: number;
    owner: string;
    box_id?: number;
    volume: number;
    notes?: string;
  }): Promise<Sample> => {
    try {
      const { name, type, owner, box_id, volume, notes = '' } = sampleData;

      const newSample = await API.samples.createSample({
        name,
        type,
        owner,
        box_id,
        volume,
        notes
      });

      setSamples(prev => [...prev, newSample]);
      return newSample;
    } catch (err) {
      console.error('Failed to add sample:', err);
      setError('Failed to add sample. Please try again later.');
      throw err;
    }
  };

  const deleteSample = async (id: string): Promise<void> => {
    try {
      await API.samples.deleteSample(id);
      setSamples(prev => prev.filter(sample => sample.id.toString() !== id));
    } catch (err) {
      console.error('Failed to delete sample:', err);
      setError('Failed to delete sample. Please try again later.');
      throw err;
    }
  };

  const updateSample = async (id: string, updates: Partial<Sample>): Promise<Sample> => {
    try {
      const updatedSample = await API.samples.updateSample(id, updates);
      setSamples(prev => prev.map(sample => 
        sample.id.toString() === id ? updatedSample : sample
      ));
      return updatedSample;
    } catch (err) {
      console.error('Failed to update sample:', err);
      setError('Failed to update sample. Please try again later.');
      throw err;
    }
  };

  const addAliquot = async (sampleId: string, aliquotData: { volume: number, purpose?: string }): Promise<Aliquot> => {
    try {
      const newAliquot = await API.aliquots.createAliquot(sampleId, aliquotData);

      // Update the sample's aliquots list
      setSamples(prev => prev.map(sample => {
        if (sample.id.toString() === sampleId) {
          return {
            ...sample,
            aliquots: [...sample.aliquots, newAliquot]
          };
        }
        return sample;
      }));

      return newAliquot;
    } catch (err) {
      console.error('Failed to add aliquot:', err);
      setError('Failed to add aliquot. Please try again later.');
      throw err;
    }
  };

  const addTest = async (
    sampleId: string,
    aliquotId: string,
    testData: { test_master_id: number, analyst_id?: string, instrument_id?: number, scheduled_date?: string, remarks?: string }
  ): Promise<Test> => {
    try {
      const newTest = await API.tests.createTest(sampleId, aliquotId, testData);

      // Update the sample's aliquots with the new test
      setSamples(prev => prev.map(sample => {
        if (sample.id.toString() === sampleId) {
          return {
            ...sample,
            aliquots: sample.aliquots.map(aliquot => {
              if (aliquot.id.toString() === aliquotId) {
                return {
                  ...aliquot,
                  tests: [...aliquot.tests, newTest]
                };
              }
              return aliquot;
            })
          };
        }
        return sample;
      }));

      return newTest;
    } catch (err) {
      console.error('Failed to add test:', err);
      setError('Failed to add test. Please try again later.');
      throw err;
    }
  };

  const exportSamples = async (filters?: {
    type?: string[],
    status?: string[],
    location?: string[],
    owner?: string[],
    search?: string
  }): Promise<void> => {
    try {
      const blob = await API.samples.exportSamples(filters);
      
      // Create a download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'samples_export.csv';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      console.error('Failed to export samples:', err);
      setError('Failed to export samples. Please try again later.');
      throw err;
    }
  };

  const getSampleTimeline = async (sampleId: string): Promise<TimelineEvent[]> => {
    try {
      const timeline = await API.timeline.getSampleTimeline(sampleId);
      return timeline.data;
    } catch (err) {
      console.error('Failed to get sample timeline:', err);
      throw err;
    }
  };

  const getAliquotTimeline = async (sampleId: string, aliquotId: string): Promise<TimelineEvent[]> => {
    try {
      const timeline = await API.timeline.getAliquotTimeline(sampleId, aliquotId);
      return timeline.data;
    } catch (err) {
      console.error('Failed to get aliquot timeline:', err);
      throw err;
    }
  };

  const getTestTimeline = async (sampleId: string, testId: string): Promise<TimelineEvent[]> => {
    try {
      const timeline = await API.timeline.getTestTimeline(sampleId, testId);
      return timeline.data;
    } catch (err) {
      console.error('Failed to get test timeline:', err);
      throw err;
    }
  };

  const getSampleById = async (id: string): Promise<Sample | null> => {
    try {
      const sample = await API.samples.getSampleById(id);
      return sample.data;
    } catch (err) {
      console.error('Failed to get sample by ID:', err);
      return null;
    }
  };

  const value = {
    samples,
    loading,
    error,
    setSamples,
    addSample,
    deleteSample,
    updateSample,
    addAliquot,
    addTest,
    refreshSamples,
    exportSamples,
    getSampleTimeline,
    getAliquotTimeline,
    getTestTimeline,
    getSampleById,
  };

  return (
    <SampleContext.Provider value={value}>
      {children}
    </SampleContext.Provider>
  );
}

export function useSamples() {
  const context = useContext(SampleContext);
  if (context === undefined) {
    throw new Error('useSamples must be used within a SampleProvider');
  }
  return context;
}