import React from 'react';

export const PageContainer = ({ children, title, subtitle, action, className = '' }) => {
  return (
    <div className={`space-y-6 max-w-7xl mx-auto pb-12 ${className}`}>
      {(title || subtitle || action) && (
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2">
          <div>
            {title && (
              <h2 className="font-creepster text-3xl sm:text-4xl text-boneWhite tracking-wide drop-shadow-md">
                {title}
              </h2>
            )}
            {subtitle && (
              <p className="text-xs font-mono text-cryptGray mt-1 leading-relaxed">
                {subtitle}
              </p>
            )}
          </div>
          {action && <div className="flex-shrink-0">{action}</div>}
        </div>
      )}
      {children}
    </div>
  );
};

export default PageContainer;

