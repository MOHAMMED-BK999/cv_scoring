import type { IngestionJobStatusPayload } from '@/services/api';

interface IngestionProgressProps {
  status: IngestionJobStatusPayload | null;
  message: string;
}

const statusLabel: Record<IngestionJobStatusPayload['status'], string> = {
  queued: 'En attente',
  processing: 'Traitement',
  completed: 'Terminé',
  failed: 'Échec',
};

const IngestionProgress = ({ status, message }: IngestionProgressProps) => {
  if (!status && !message) {
    return null;
  }

  const total = status?.total_files ?? 0;
  const processed = status?.processed_files ?? 0;
  const percentage = total > 0 ? Math.min(100, Math.round((processed / total) * 100)) : 0;
  const isError = status?.status === 'failed';

  return (
    <div className={`mt-4 rounded-lg border px-4 py-3 text-sm ${isError ? 'border-red-300 bg-red-50 text-red-700' : 'border-blue-300 bg-blue-50 text-blue-700'}`}>
      <div className="flex items-center justify-between gap-3">
        <span>{message || (status ? `Job ${status.job_id.slice(0, 8)} - ${statusLabel[status.status]}` : '')}</span>
        {status && (
          <span className="font-semibold">{percentage}%</span>
        )}
      </div>
      {status && (
        <>
          <div className="mt-2 h-2 w-full rounded-full bg-blue-200 overflow-hidden">
            <div
              className={`h-full rounded-full transition-all duration-300 ${isError ? 'bg-red-500' : 'bg-blue-600'}`}
              style={{ width: `${percentage}%` }}
            />
          </div>
          <p className="mt-2 text-xs">{processed}/{total} fichiers traités</p>
        </>
      )}
    </div>
  );
};

export default IngestionProgress;
