import React, { useState } from 'react';

export const Tooltip = ({ content, children, position = 'top' }) => {
  const [isVisible, setIsVisible] = useState(false);

  const positionStyles = {
    top: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
    bottom: 'top-full left-1/2 -translate-x-1/2 mt-2',
    left: 'right-full top-1/2 -translate-y-1/2 mr-2',
    right: 'left-full top-1/2 -translate-y-1/2 ml-2',
  };

  return (
    <div
      className="relative inline-flex"
      onMouseEnter={() => setIsVisible(true)}
      onMouseLeave={() => setIsVisible(false)}
    >
      {children}
      {isVisible && (
        <div
          className={`absolute z-50 whitespace-nowrap px-2.5 py-1 text-[11px] font-mono rounded bg-[#1f1130] text-boneWhite border border-coffinBorder shadow-pumpkin pointer-events-none transition-opacity duration-150 ${positionStyles[position]}`}
        >
          {content}
        </div>
      )}
    </div>
  );
};

export default Tooltip;

