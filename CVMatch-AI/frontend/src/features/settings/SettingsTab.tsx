

import { useScoringSettings } from '@/hooks/useScoringSettings';

const SettingsTab = () => {
  const { weights, updateWeight } = useScoringSettings();

  const totalWeights = Object.values(weights).reduce((a, b) => a + b, 0);
  const isError = totalWeights !== 100;

  const weightKeys = [
    { key: 'skills' as const, label: 'Poids - Compétences Techniques' },
    { key: 'experience' as const, label: 'Poids - Expérience' },
    { key: 'education' as const, label: "Poids - Niveau d'études" },
    { key: 'softSkills' as const, label: 'Poids - Soft Skills' },
  ];

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-lg font-bold text-gray-800 border-l-4 border-emerald-500 pl-3">Configuration du Scoring</h3>
          <div className={`px-4 py-2 rounded-lg text-sm font-bold ${isError ? 'bg-red-50 text-red-600 border border-red-200' : 'bg-emerald-50 text-emerald-600 border border-emerald-200'}`}>
            Total : {totalWeights}%
          </div>
        </div>
        
        {isError && (
          <div className="mb-6 p-3 bg-red-50 border border-red-200 rounded-md text-red-600 text-sm">
            ⚠️ Le total des poids doit être exactement égal à 100%. Veuillez ajuster les valeurs.
          </div>
        )}

        <div className="space-y-6">
          {weightKeys.map(({ key, label }) => (
            <div key={key}>
              <div className="flex items-center justify-between mb-2">
                <label className="text-sm font-semibold text-gray-700">
                  {label}
                </label>
                <div className="flex items-center space-x-3">
                  <span className={`text-sm font-bold ${isError ? 'text-red-500' : 'text-emerald-600'}`}>{weights[key]}%</span>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={weights[key]}
                  onChange={(e) => updateWeight(key, Number(e.target.value))}
                  className={`flex-1 ${isError ? 'accent-red-500' : 'accent-emerald-600'}`}
                />
                <input 
                  type="number" 
                  min="0" 
                  max="100" 
                  value={weights[key]} 
                  onChange={(e) => updateWeight(key, Number(e.target.value))}
                  className={`w-16 p-1 text-center border rounded-md text-sm font-bold focus:outline-none focus:ring-2 ${isError ? 'border-red-300 focus:ring-red-500' : 'border-gray-200 focus:ring-emerald-500'}`}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h3 className="text-lg font-bold text-gray-800 mb-6">Seuils de scoring</h3>
        <div className="grid grid-cols-3 gap-4">
          <div className="p-4 bg-emerald-50 rounded-lg border border-emerald-200">
            <p className="font-bold text-emerald-700">Excellent match</p>
            <p className="text-2xl font-bold text-emerald-800">≥ 85%</p>
          </div>
          <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
            <p className="font-bold text-blue-700">Bon match</p>
            <p className="text-2xl font-bold text-blue-800">70-84%</p>
          </div>
          <div className="p-4 bg-amber-50 rounded-lg border border-amber-200">
            <p className="font-bold text-amber-700">À revoir</p>
            <p className="text-2xl font-bold text-amber-800">{'< 70%'}</p>
          </div>
        </div>
      </div>


    </div>
  );
};

export default SettingsTab;
