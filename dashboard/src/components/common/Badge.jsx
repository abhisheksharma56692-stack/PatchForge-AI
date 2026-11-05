import React from 'react';

export const Badge = ({
  children,
  variant = 'default', // 'critical' | 'high' | 'medium' | 'low' | 'neutralized' | 'default' | 'purple'
  size = 'md',        // 'sm' | 'md'
  icon: Icon,
  className = '',
}) => {
  const sizeStyles = {
    sm: 'text-[10px] px-1.5 py-0.5 gap-1',
    md: 'text-xs px-2.5 py-1 gap-1.5',
  };

  const variantStyles = {
    critical: 'bg-red-950/80 text-red-400 border border-red-700/60 shadow-[0_0_8px_rgba(220,38,38,0.4)]',
    high: 'bg-orange-950/80 text-orange-400 border border-orange-700/60 shadow-[0_0_8px_rgba(249,115,22,0.4)]',
    medium: 'bg-amber-950/80 text-amber-300 border border-amber-700/60',
    low: 'bg-cyan-950/80 text-cyan-300 border border-cyan-800/60',
    neutralized: 'bg-emerald-950/80 text-ghostGreen border border-ghostGreen/40 shadow-[0_0_8px_rgba(0,255,157,0.3)]',
    purple: 'bg-coffinPurple text-purple-300 border border-coffinBorder',
    default: 'bg-coffinDark text-cryptGray border border-coffinBorder',
  };

  return (
    <span
      className={`inline-flex items-center font-mono font-medium rounded-full uppercase tracking-wider ${sizeStyles[size]} ${variantStyles[variant]} ${className}`}
    >
      {Icon && <Icon className={size === 'sm' ? 'w-3 h-3' : 'w-3.5 h-3.5'} />}
      {children}
    </span>
  );
};

export default Badge;

