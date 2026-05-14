import { ReactNode } from 'react';
import { X } from 'lucide-react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: ReactNode;
  size?: 'sm' | 'md' | 'lg';
}

export const Modal = ({
  isOpen,
  onClose,
  title,
  children,
  size = 'md',
}: ModalProps) => {
  if (!isOpen) return null;

  const sizeClasses = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
  };

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50">
      <div className={`bg-gradient-to-br from-bg-secondary to-bg-tertiary border border-border-primary rounded-xl w-full ${sizeClasses[size]} max-h-[90vh] overflow-y-auto shadow-2xl`}>
        {title && (
          <div className="flex items-center justify-between p-5 border-b border-border-primary">
            <h2 className="text-lg font-700 text-text-primary">{title}</h2>
            <button onClick={onClose} className="text-text-secondary hover:text-text-primary transition-colors p-1 hover:bg-bg-quaternary rounded-lg">
              <X size={20} strokeWidth={2} />
            </button>
          </div>
        )}
        <div className="p-5">{children}</div>
      </div>
    </div>
  );
};
