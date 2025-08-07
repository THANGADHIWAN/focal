import React, { useEffect, useRef, useState } from 'react';

interface SelectOption {
  label: string;
  value: string | number;
}

interface SelectProps {
  options: SelectOption[];
  value?: string | number;
  onChange: (value: string | number) => void;
  placeholder?: string;
  className?: string;
  error?: string;
  disabled?: boolean;
}

export const Select: React.FC<SelectProps> = ({
  options,
  value,
  onChange,
  placeholder,
  className = '',
  error,
  disabled
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedOption, setSelectedOption] = useState<SelectOption | undefined>(
    options.find(opt => opt.value === value)
  );
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setSelectedOption(options.find(opt => opt.value === value));
  }, [value, options]);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelect = (option: SelectOption) => {
    setSelectedOption(option);
    onChange(option.value);
    setIsOpen(false);
  };

  return (
    <div className="relative w-full" ref={containerRef}>
      <button
        type="button"
        className={`
          w-full px-3 py-2 text-left rounded-md border
          focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
          ${error ? 'border-red-500' : 'border-gray-300'}
          ${disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white cursor-pointer'}
          ${className}
        `}
        onClick={() => !disabled && setIsOpen(!isOpen)}
        disabled={disabled}
      >
        {selectedOption ? selectedOption.label : (
          <span className="text-gray-400">{placeholder}</span>
        )}
      </button>

      {isOpen && !disabled && (
        <div className="
          absolute z-10 w-full mt-1 bg-white rounded-md shadow-lg
          max-h-60 overflow-auto border border-gray-200
        ">
          {options.map((option, index) => (
            <div
              key={index}
              className={`
                px-3 py-2 cursor-pointer hover:bg-gray-100
                ${option.value === selectedOption?.value ? 'bg-blue-50 text-blue-600' : ''}
              `}
              onClick={() => handleSelect(option)}
            >
              {option.label}
            </div>
          ))}
        </div>
      )}

      {error && (
        <p className="mt-1 text-sm text-red-500">
          {error}
        </p>
      )}
    </div>
  );
};
