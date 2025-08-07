import React from 'react';
import { ButtonHTMLAttributes } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  primary?: boolean;
  severity?: 'success' | 'warning' | 'danger' | 'info';
  label?: string;
  icon?: string;
}

export const Button: React.FC<ButtonProps> = ({
  primary,
  severity,
  label,
  icon,
  className = '',
  children,
  ...props
}) => {
  const getColorClasses = () => {
    if (primary) return 'bg-blue-600 hover:bg-blue-700 text-white';
    if (severity === 'success') return 'bg-green-600 hover:bg-green-700 text-white';
    if (severity === 'warning') return 'bg-yellow-600 hover:bg-yellow-700 text-white';
    if (severity === 'danger') return 'bg-red-600 hover:bg-red-700 text-white';
    if (severity === 'info') return 'bg-blue-500 hover:bg-blue-600 text-white';
    return 'bg-gray-100 hover:bg-gray-200 text-gray-700';
  };

  return (
    <button
      {...props}
      className={`
        px-4 py-2 rounded-md font-medium text-sm
        focus:outline-none focus:ring-2 focus:ring-offset-2
        transition-colors duration-200
        disabled:opacity-50 disabled:cursor-not-allowed
        ${getColorClasses()}
        ${className}
      `}
    >
      {icon && <i className={`pi ${icon} ${label || children ? 'mr-2' : ''}`} />}
      {label || children}
    </button>
  );
};
