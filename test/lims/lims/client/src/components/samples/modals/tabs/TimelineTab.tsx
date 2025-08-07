import React, { useState, useEffect } from 'react';
import { Clock, User, Calendar } from 'lucide-react';
import { useSamples } from '../../../../context/SampleContext';
import { TimelineEvent } from '../../../../api/services/timelineService';

interface TimelineTabProps {
  sampleId: string;
  aliquotId?: string;
  testId?: string;
  onTimelineLoad?: (events: TimelineEvent[]) => void;
}

export default function TimelineTab({ sampleId, aliquotId, testId, onTimelineLoad }: TimelineTabProps) {
  const { getSampleTimeline, getAliquotTimeline, getTestTimeline } = useSamples();
  const [timeline, setTimeline] = useState<TimelineEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadTimeline = async () => {
      try {
        setLoading(true);
        setError(null);
        
        console.log('[TimelineTab] Loading timeline for:', { sampleId, aliquotId, testId });
        
        let events: TimelineEvent[] = [];
        
        if (testId) {
          console.log('[TimelineTab] Loading test timeline');
          events = await getTestTimeline(sampleId, testId);
        } else if (aliquotId) {
          console.log('[TimelineTab] Loading aliquot timeline');
          events = await getAliquotTimeline(sampleId, aliquotId);
        } else {
          console.log('[TimelineTab] Loading sample timeline');
          events = await getSampleTimeline(sampleId);
        }
        
        console.log('[TimelineTab] Timeline events loaded:', events);
        // Ensure events is always an array
        const timelineEvents = Array.isArray(events) ? events : [];
        setTimeline(timelineEvents);
        onTimelineLoad?.(timelineEvents);
      } catch (err) {
        console.error('[TimelineTab] Failed to load timeline:', err);
        setError(`Failed to load timeline events: ${err instanceof Error ? err.message : 'Unknown error'}`);
      } finally {
        setLoading(false);
      }
    };

    loadTimeline();
  }, [sampleId, aliquotId, testId, getSampleTimeline, getAliquotTimeline, getTestTimeline, onTimelineLoad]);

  const formatDate = (dateString: string) => {
    try {
      return new Date(dateString).toLocaleString();
    } catch {
      return dateString;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
          <span className="text-gray-600">Loading timeline...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <div className="text-red-600 mb-2">Error loading timeline</div>
        <p className="text-gray-600 text-sm">{error}</p>
        <button
          onClick={() => window.location.reload()}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!timeline || timeline.length === 0) {
    return (
      <div className="text-center py-8">
        <Clock className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No Timeline Events</h3>
        <p className="text-gray-600">No timeline events found for this item.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium text-gray-900">
          {testId ? 'Test Timeline' : aliquotId ? 'Aliquot Timeline' : 'Sample Timeline'}
        </h3>
        <span className="text-sm text-gray-500">{timeline.length} events</span>
      </div>
      
      <div className="space-y-4">
        {timeline.map((event, index) => (
          <div key={event.id || index} className="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg">
            <div className="flex-shrink-0">
              <div className="w-3 h-3 bg-blue-500 rounded-full mt-2"></div>
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between">
                <h4 className="text-sm font-medium text-gray-900">{event.event}</h4>
                <div className="flex items-center space-x-2 text-xs text-gray-500">
                  <Calendar className="w-3 h-3" />
                  <span>{formatDate(event.date)}</span>
                </div>
              </div>
              <div className="flex items-center space-x-2 mt-1">
                <User className="w-3 h-3 text-gray-400" />
                <span className="text-xs text-gray-600">{event.user}</span>
              </div>
              {event.justification && (
                <p className="text-xs text-gray-600 mt-2">{event.justification}</p>
              )}
              {event.new_value && (
                <div className="mt-2 p-2 bg-blue-50 rounded text-xs">
                  <span className="font-medium">Changes:</span> {JSON.stringify(event.new_value)}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}