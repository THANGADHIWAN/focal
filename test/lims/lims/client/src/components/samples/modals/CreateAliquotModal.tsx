import React, { useState } from 'react';
import { X } from 'lucide-react';
import { BoxLocation } from '../../../types/sample';

interface CreateAliquotModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: (volume: number, purpose?: string) => void;
  volume: number;
  onVolumeChange: (volume: number) => void;
  boxId: string;
  onBoxIdChange: (boxId: string) => void;
  maxVolume?: number;
}

export default function CreateAliquotModal({
  isOpen,
  onClose,
  onConfirm,
  volume,
  onVolumeChange,
  boxId,
  onBoxIdChange,
  maxVolume = 0,
}: CreateAliquotModalProps) {
  const [purpose, setPurpose] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async () => {
    if (volume <= 0 || volume > maxVolume) return;
    
    setIsSubmitting(true);
    try {
      await onConfirm(volume, purpose);
      setPurpose('');
    } catch (error) {
      console.error('Failed to create aliquot:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleClose = () => {
    setPurpose('');
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-medium text-gray-900">Create New Aliquot</h3>
          <button
            onClick={handleClose}
            className="text-gray-400 hover:text-gray-500 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Volume (mL)
            </label>
            <input
              type="number"
              min="0.1"
              max={maxVolume}
              step="0.1"
              value={volume}
              onChange={(e) => onVolumeChange(Number(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter volume in mL"
            />
            <p className="mt-1 text-sm text-gray-500">
              Available volume: {maxVolume} mL
            </p>
            {volume > maxVolume && (
              <p className="mt-1 text-sm text-red-500">
                Volume cannot exceed available volume
              </p>
            )}
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Purpose (Optional)
            </label>
            <textarea
              value={purpose}
              onChange={(e) => setPurpose(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter the purpose of this aliquot"
              rows={3}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Storage Box (Optional)
            </label>
            <select
              value={boxId}
              onChange={(e) => onBoxIdChange(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select a storage box...</option>
              <option value="box1">Box A1</option>
              <option value="box2">Box A2</option>
              <option value="box3">Box A3</option>
            </select>
          </div>
          
          {boxId && (
            <div className="bg-gray-50 rounded-lg p-3">
              <h4 className="text-sm font-medium text-gray-700 mb-2">Box Location</h4>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <span className="text-gray-500">Lab:</span>
                  <span className="ml-2 text-gray-900">Lab 1</span>
                </div>
                <div>
                  <span className="text-gray-500">Freezer:</span>
                  <span className="ml-2 text-gray-900">F1</span>
                </div>
                <div>
                  <span className="text-gray-500">Rack:</span>
                  <span className="ml-2 text-gray-900">R1</span>
                </div>
                <div>
                  <span className="text-gray-500">Shelf:</span>
                  <span className="ml-2 text-gray-900">S1</span>
                </div>
              </div>
            </div>
          )}
        </div>
        
        <div className="mt-6 flex justify-end space-x-3">
          <button
            onClick={handleClose}
            className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-800 transition-colors"
            disabled={isSubmitting}
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            disabled={volume <= 0 || volume > maxVolume || isSubmitting}
            className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center"
          >
            {isSubmitting ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Creating...
              </>
            ) : (
              'Create Aliquot'
            )}
          </button>
        </div>
      </div>
    </div>
  );
}