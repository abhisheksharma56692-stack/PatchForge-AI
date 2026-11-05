import React, { useEffect } from 'react';
import { X } from 'lucide-react';

export const Modal = ({
  isOpen,
  onClose,
  title,
  subtitle,
  children,
  maxWidth = 'max-w-2xl',
}) => {
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    if (isOpen) {
      document.body.style.overflow = 'hidden';
      window.addEventListener('keydown', handleKeyDown);
    }
    return () => {
      document.body.style.overflow = 'unset';
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 overflow-y-auto">
      {/* Darkened Backdrop Blur */}
      <div
        className="fixed inset-0 bg-midnightBlack/80 backdrop-blur-md transition-opacity"
        onClick={onClose}
      />

      {/* Coffin/Gothic Framed Container */}
      <div
        className={`relative z-10 w-full ${maxWidth} bg-[#140b1f] border-2 border-coffinBorder rounded-2xl shadow-coffin p-6 my-8 text-boneWhite transition-all transform animate-in fade-in zoom-in-95 duration-200`}
      >
        {/* Modal Header */}
        <div className="flex items-start justify-between pb-4 border-b border-coffinBorder/60">
          <div>
            <h3 className="font-creepster text-2xl text-pumpkinOrange tracking-wide drop-shadow-md">
              {title}
            </h3>
            {subtitle && <p className="text-xs font-mono text-cryptGray mt-1">{subtitle}</p>}
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-cryptGray hover:text-boneWhite hover:bg-coffinPurple transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Content */}
        <div className="py-4 max-h-[75vh] overflow-y-auto pr-1">{children}</div>
      </div>
    </div>
  );
};

export default Modal;

