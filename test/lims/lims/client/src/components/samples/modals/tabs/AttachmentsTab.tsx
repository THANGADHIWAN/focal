import React, { useRef, useState } from 'react';
import { Paperclip, FileText, Download, Upload, X } from 'lucide-react';

interface Attachment {
  id: string;
  name: string;
  size: string;
  date: string;
}

interface AttachmentsTabProps {
  attachments: Attachment[];
  onUpload?: (files: FileList) => void;
  onDownload?: (fileId: string) => void;
}

export default function AttachmentsTab({
  attachments,
  onUpload,
  onDownload,
}: AttachmentsTabProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && onUpload) {
      setIsUploading(true);
      try {
        await onUpload(event.target.files);
      } catch (error) {
        console.error('Failed to upload files:', error);
      } finally {
        setIsUploading(false);
      }
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0] && onUpload) {
      setIsUploading(true);
      onUpload(e.dataTransfer.files).finally(() => {
        setIsUploading(false);
      });
    }
  };

  const handleDownload = async (fileId: string) => {
    if (onDownload) {
      try {
        await onDownload(fileId);
      } catch (error) {
        console.error('Failed to download file:', error);
      }
    }
  };

  return (
    <div className="space-y-4">
      <div className="mb-6">
        <h3 className="text-lg font-medium text-gray-900">Sample Attachments</h3>
        <p className="text-sm text-gray-500 mt-1">Upload and manage files related to this sample</p>
      </div>

      {/* Upload Section */}
      {onUpload && (
        <div 
          className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors ${
            dragActive 
              ? 'border-blue-400 bg-blue-50' 
              : 'border-gray-300 hover:border-gray-400'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            ref={fileInputRef}
            type="file"
            className="hidden"
            id="file-upload"
            multiple
            onChange={handleFileChange}
            disabled={isUploading}
          />
          <label
            htmlFor="file-upload"
            className={`cursor-pointer ${isUploading ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            {isUploading ? (
              <>
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-2"></div>
                <span className="text-sm font-medium text-blue-600">Uploading...</span>
              </>
            ) : (
              <>
                <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                <span className="text-sm font-medium text-blue-600">
                  Upload files
                </span>
                <span className="text-sm text-gray-500 block">
                  or drag and drop
                </span>
              </>
            )}
          </label>
        </div>
      )}

      {/* Attachments List */}
      {attachments.length === 0 ? (
        <div className="text-center py-12">
          <Paperclip className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Attachments</h3>
          <p className="text-gray-500">
            {onUpload 
              ? 'Upload files using the form above.'
              : 'No attachments have been added to this sample.'
            }
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {attachments.map((file) => (
            <div
              key={file.id}
              className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <div className="flex items-center space-x-3">
                <FileText className="w-5 h-5 text-gray-400" />
                <div>
                  <p className="text-sm font-medium text-gray-900">
                    {file.name}
                  </p>
                  <p className="text-xs text-gray-500">
                    {file.size} • {file.date}
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                {onDownload && (
                  <button 
                    onClick={() => handleDownload(file.id)}
                    className="p-2 text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded-full transition-colors"
                    title="Download file"
                  >
                    <Download className="w-4 h-4" />
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}