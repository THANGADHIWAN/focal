import React, { ReactNode } from 'react';

interface TabPanelProps {
  header: string;
  children: ReactNode;
  active?: boolean;
}

export const TabPanel: React.FC<TabPanelProps> = ({ children, active }) => {
  if (!active) return null;
  return <div className="p-4">{children}</div>;
};

interface TabViewProps {
  children: ReactNode;
  activeIndex: number;
  onTabChange: (e: { index: number }) => void;
  className?: string;
}

export const TabView: React.FC<TabViewProps> = ({
  children,
  activeIndex,
  onTabChange,
  className = ''
}) => {
  // Filter only TabPanel children
  const tabs = React.Children.toArray(children).filter(
    (child) => React.isValidElement(child) && child.type === TabPanel
  );

  const headers = tabs.map((tab, index) => {
    if (!React.isValidElement(tab)) return null;
    
    const isActive = index === activeIndex;
    return (
      <button
        key={index}
        onClick={() => onTabChange({ index })}
        className={`px-4 py-2 font-medium text-sm focus:outline-none
          ${isActive
            ? 'text-blue-600 border-b-2 border-blue-600'
            : 'text-gray-500 hover:text-gray-700 hover:border-gray-300 border-b-2 border-transparent'
          }`}
      >
        {tab.props.header}
      </button>
    );
  });

  return (
    <div className={`w-full ${className}`}>
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8" aria-label="Tabs">
          {headers}
        </nav>
      </div>
      <div className="mt-4">
        {React.Children.map(tabs, (child, index) => {
          if (!React.isValidElement(child)) return null;
          return React.cloneElement(child, {
            active: index === activeIndex
          });
        })}
      </div>
    </div>
  );
};
