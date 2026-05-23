interface WeightRowProps {
  label: string;
  value: number;
  className?: string;
}

const WeightRow = ({ label, value, className = '' }: WeightRowProps) => {
  return (
    <div className={className}>
      <div className="flex items-center justify-between mb-2">
        <label className="text-sm font-semibold text-gray-700">{label}</label>
        <span className="text-sm text-emerald-600 font-bold">{value}%</span>
      </div>
      <input type="range" value={value} readOnly className="w-full accent-emerald-600" />
    </div>
  );
};

export default WeightRow;
