import type { ReactNode } from 'react';

interface AppCardProps {
  title?: string;
  children: ReactNode;
  className?: string;
}

const AppCard = ({ title, children, className = '' }: AppCardProps) => {
  return (
    <div className={`bg-white rounded-xl shadow-sm border border-gray-100 p-6 ${className}`}>
      {title && <h3 className="text-lg font-bold text-gray-800 mb-4">{title}</h3>}
      {children}
    </div>
  );
};

export default AppCard;
