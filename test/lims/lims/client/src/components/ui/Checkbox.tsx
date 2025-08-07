import React from 'react';

interface CheckboxProps {
  checked: boolean;
  onChange: (e: { checked: boolean }) => void;
  label?: string;
  disabled?: boolean;
  className?: string;
}

export const Checkbox: React.FC<CheckboxProps> = ({
  checked,
  onChange,
  label,
  disabled,
  className = ''
}) => {
  return (
    <label className={`inline-flex items-center ${disabled ? 'cursor-not-allowed' : 'cursor-pointer'} ${className}`}>
      <div className="relative">
        <input
          type="checkbox"
          className="sr-only"
          checked={checked}
          onChange={() => !disabled && onChange({ checked: !checked })}
          disabled={disabled}
        />
        <div
          className={`
            w-5 h-5 border rounded
            transition-colors duration-200
            ${checked ? 'bg-blue-600 border-blue-600' : 'bg-white border-gray-300'}
            ${disabled ? 'opacity-50' : ''}
          `}
        >
          {checked && (
            <svg
              className="w-full h-full text-white"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                clipRule="evenodd"
              />
            </svg>
          )}
        </div>
      </div>
      {label && (
        <span className={`ml-2 ${disabled ? 'text-gray-400' : 'text-gray-700'}`}>
          {label}
        </span>
      )}
    </label>
  );
};
