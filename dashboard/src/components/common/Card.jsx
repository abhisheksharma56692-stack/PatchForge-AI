import React from 'react';

export const Card = ({
  children,
  title,
  subtitle,
  icon: Icon,
  action,
  glow = false,
  className = '',
  cornerCobweb = false,
}) => {
  return (
    <div
      className={`relative rounded-xl border border-coffinBorder/80 bg-coffinDark/90 backdrop-blur-md p-5 shadow-coffin transition-all duration-300 ${
        glow ? 'border-pumpkinOrange/70 shadow-[0_0_20px_rgba(255,106,0,0.2)]' : 'hover:border-coffinBorder'
      } ${className}`}
    >
      {cornerCobweb && (
        <div
          className="absolute top-0 right-0 w-16 h-16 pointer-events-none opacity-30 bg-no-repeat bg-right-top"
          style={{ backgroundImage: `url('/assets/textures/cobweb-corner.svg')` }}
        />
      )}

      {(title || Icon || action) && (
        <div className="flex items-center justify-between pb-3 mb-4 border-b border-coffinBorder/50">
          <div className="flex items-center gap-2.5">
            {Icon && <Icon className="w-5 h-5 text-pumpkinOrange" />}
            <div>
              {title && <h3 className="font-mono text-sm font-semibold text-boneWhite tracking-wide">{title}</h3>}
              {subtitle && <p className="text-xs font-mono text-cryptGray mt-0.5">{subtitle}</p>}
            </div>
          </div>
          {action && <div>{action}</div>}
        </div>
      )}

      <div className="relative z-10">{children}</div>
    </div>
  );
};

export default Card;

