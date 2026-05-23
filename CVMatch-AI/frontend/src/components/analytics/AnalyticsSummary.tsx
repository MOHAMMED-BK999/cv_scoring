interface AnalyticsSummaryProps {
  label: string;
  value: string;
}

const AnalyticsSummary = ({ label, value }: AnalyticsSummaryProps) => {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
      <p className="text-xs text-gray-500">{label}</p>
      <p className="text-lg font-bold text-gray-800">{value}</p>
    </div>
  );
};

export default AnalyticsSummary;
