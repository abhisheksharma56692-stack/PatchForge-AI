import React from 'react';

export const Tabs = ({ tabs, activeTab, onChange, className = '' }) => {
  return (
    <div className={`flex items-center gap-1 border-b border-coffinBorder/60 ${className}`}>
      {tabs.map((tab) => {
        const isActive = activeTab === tab.id;
        const Icon = tab.icon;
        return (
          <button
            key={tab.id}
            onClick={() => onChange(tab.id)}
            className={`relative flex items-center gap-2 px-4 py-2.5 text-xs font-mono font-medium transition-all duration-200 border-b-2 -mb-px ${
              isActive
                ? 'border-pumpkinOrange text-pumpkinOrange bg-coffinPurple/40'
                : 'border-transparent text-cryptGray hover:text-boneWhite hover:bg-coffinPurple/20'
            }`}
          >
            {Icon && <Icon className={`w-4 h-4 ${isActive ? 'text-pumpkinOrange' : 'text-cryptGray'}`} />}
            <span>{tab.label}</span>
            {tab.badge !== undefined && (
              <span
                className={`ml-1.5 px-1.5 py-0.2 rounded-full text-[10px] font-mono ${
                  isActive ? 'bg-pumpkinOrange/20 text-pumpkinOrange' : 'bg-coffinBorder/60 text-cryptGray'
                }`}
              >
                {tab.badge}
              </span>
            )}
          </button>
        );
      })}
    </div>
  );
};

export default Tabs;

