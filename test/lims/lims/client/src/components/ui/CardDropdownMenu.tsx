import React, { useState, useRef, useEffect } from 'react';
import { MoreVertical, Trash2, Loader2, Pencil } from 'lucide-react';

interface CardDropdownMenuProps {
  onDelete: () => void;
  onEdit: () => void;
  itemName: string;
  isDeleting?: boolean;
  className?: string;
}

export default function CardDropdownMenu({ 
  onDelete, 
  onEdit,
  itemName, 
  isDeleting = false,
  className = ""
}: CardDropdownMenuProps) {
  const [showMenu, setShowMenu] = useState(false);
  const [showConfirmation, setShowConfirmation] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  // Close menu when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setShowMenu(false);
        setShowConfirmation(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleMenuClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    setShowMenu(!showMenu);
  };

  const handleDeleteClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    setShowConfirmation(true);
  };

  const handleConfirmDelete = (e: React.MouseEvent) => {
    e.stopPropagation();
    setShowConfirmation(false);
    setShowMenu(false);
    onDelete();
  };

  const handleCancelDelete = (e: React.MouseEvent) => {
    e.stopPropagation();
    setShowConfirmation(false);
  };

  return (
    <div className={`relative ${className}`} ref={menuRef}>
      <button
        onClick={handleMenuClick}
        disabled={isDeleting}
        className="p-1 text-gray-400 hover:text-gray-600 transition-colors rounded hover:bg-gray-100"
        title="More options"
      >
        {isDeleting ? (
          <Loader2 className="w-4 h-4 animate-spin" />
        ) : (
          <MoreVertical className="w-4 h-4" />
        )}
      </button>

      {showMenu && !showConfirmation && (
        <div className="absolute right-0 mt-1 w-32 bg-white rounded-lg shadow-lg py-1 z-20 border border-gray-200">
          <button
            onClick={(e) => {
              e.stopPropagation();
              setShowMenu(false);
              onEdit();
            }}
            className="w-full px-3 py-2 text-left text-sm text-gray-700 hover:bg-gray-50 flex items-center"
          >
            <Pencil className="w-3 h-3 mr-2" />
            Edit
          </button>
          <button
            onClick={handleDeleteClick}
            className="w-full px-3 py-2 text-left text-sm text-red-600 hover:bg-red-50 flex items-center"
          >
            <Trash2 className="w-3 h-3 mr-2" />
            Delete
          </button>
        </div>
      )}

      {showConfirmation && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl w-[400px] p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Delete Product</h3>
            <div className="mb-4 p-3 bg-gray-50 rounded-lg">
              <label className="block text-sm font-medium text-gray-700 mb-1">Product Name:</label>
              <p className="text-sm font-medium text-gray-900">{itemName}</p>
            </div>
            <p className="text-sm text-gray-600 mb-6">
              Are you sure you want to delete this product? This action cannot be undone.
            </p>
            <div className="flex space-x-3 justify-end">
              <button
                onClick={handleCancelDelete}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={handleConfirmDelete}
                className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 flex items-center"
              >
                {isDeleting ? (
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                ) : (
                  <Trash2 className="w-4 h-4 mr-2" />
                )}
                Delete Product
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}