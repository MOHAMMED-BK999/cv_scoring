import type { Candidate } from '@/types/app';

interface CandidateBadgeProps {
  status: Candidate['status'];
}

const CandidateBadge = ({ status }: CandidateBadgeProps) => {
  const text = status === 'matched' ? 'Matché' : status === 'pending' ? 'En attente' : 'Examiné';
  const classes = status === 'matched'
    ? 'bg-emerald-100 text-emerald-700'
    : status === 'pending'
      ? 'bg-blue-100 text-blue-700'
      : 'bg-gray-100 text-gray-700';

  return <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-medium ${classes}`}>{text}</span>;
};

export default CandidateBadge;
