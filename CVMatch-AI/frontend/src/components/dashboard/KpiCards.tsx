interface KpiCardsProps {
  total: number;
  matched: number;
  average: number;
  pending: number;
}

const KpiCards = ({ total, matched, average, pending }: KpiCardsProps) => {
  return (
    <div className="grid grid-cols-4 gap-6">
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <p className="text-3xl font-bold text-gray-800">{total}</p>
        <p className="text-sm text-gray-500">CV analysés</p>
      </div>
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <p className="text-3xl font-bold text-gray-800">{matched}</p>
        <p className="text-sm text-gray-500">Candidats matchés</p>
      </div>
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <p className="text-3xl font-bold text-gray-800">{average}%</p>
        <p className="text-sm text-gray-500">Score moyen</p>
      </div>
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <p className="text-3xl font-bold text-gray-800">{pending}</p>
        <p className="text-sm text-gray-500">En attente</p>
      </div>
    </div>
  );
};

export default KpiCards;
