import React, { ReactNode } from 'react';

interface DialogProps {
  visible: boolean;
  onHide: () => void;
  header?: string;
  children: ReactNode;
  className?: string;
}

export const Dialog: React.FC<DialogProps> = ({
  visible,
  onHide,
  header,
  children,
  className = ''
}) => {
  if (!visible) return null;

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 transition-opacity z-40"
        onClick={onHide}
      />

      {/* Dialog */}
      <div className="fixed inset-0 overflow-y-auto z-50">
        <div className="flex min-h-full items-center justify-center p-4">
          <div
            className={`
              relative transform overflow-hidden rounded-lg
              bg-white text-left shadow-xl transition-all
              sm:my-8 sm:w-full sm:max-w-lg
              ${className}
            `}
          >
            {/* Header */}
            {header && (
              <div className="bg-gray-50 px-4 py-3 border-b border-gray-200">
                <h3 className="text-lg font-medium text-gray-900">
                  {header}
                </h3>
              </div>
            )}

            {/* Content */}
            <div className="bg-white px-4 py-5">
              {children}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};
