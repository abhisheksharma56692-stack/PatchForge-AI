import React from 'react';

export const Button = ({
  children,
  variant = 'pumpkin', // 'pumpkin' | 'blood' | 'ghost' | 'outline' | 'ghost-outline'
  size = 'md',        // 'sm' | 'md' | 'lg'
  icon: Icon,
  disabled = false,
  className = '',
  onClick,
  ...props
}) => {
  const baseStyles = 'inline-flex items-center justify-center font-mono font-medium transition-all duration-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-midnightBlack disabled:opacity-50 disabled:cursor-not-allowed select-none';

  const sizeStyles = {
    sm: 'text-xs px-2.5 py-1.5 gap-1.5',
    md: 'text-sm px-4 py-2 gap-2',
    lg: 'text-base px-5 py-2.5 gap-2.5',
  };

  const variantStyles = {
    pumpkin: 'bg-pumpkinOrange hover:bg-pumpkinAmber text-midnightBlack font-semibold shadow-pumpkin hover:shadow-[0_0_25px_rgba(255,106,0,0.6)] focus:ring-pumpkinOrange',
    blood: 'bg-bloodRed hover:bg-bloodVibrant text-boneWhite shadow-blood hover:shadow-[0_0_25px_rgba(220,38,38,0.7)] focus:ring-bloodRed',
    ghost: 'bg-ghostGreen hover:bg-emerald-400 text-midnightBlack font-semibold shadow-ghost hover:shadow-[0_0_25px_rgba(0,255,157,0.6)] focus:ring-ghostGreen',
    outline: 'border border-coffinBorder bg-coffinDark/80 hover:bg-coffinPurple text-boneWhite hover:border-pumpkinOrange hover:text-pumpkinOrange focus:ring-pumpkinOrange',
    'ghost-outline': 'border border-coffinBorder bg-transparent hover:bg-coffinPurple/40 text-cryptGray hover:text-boneWhite',
  };

  return (
    <button
      type="button"
      disabled={disabled}
      onClick={onClick}
      className={`${baseStyles} ${sizeStyles[size]} ${variantStyles[variant]} ${className}`}
      {...props}
    >
      {Icon && <Icon className={size === 'sm' ? 'w-3.5 h-3.5' : size === 'lg' ? 'w-5 h-5' : 'w-4 h-4'} />}
      {children}
    </button>
  );
};

export default Button;

