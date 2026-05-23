import { Bar, BarChart, CartesianGrid, Legend, PolarAngleAxis, PolarGrid, PolarRadiusAxis, Radar, RadarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

interface AnalyticsTabProps {
  scoreDistribution: Array<{ range: string; count: number }>;
}

const AnalyticsTab = ({ scoreDistribution }: AnalyticsTabProps) => {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h3 className="text-lg font-bold text-gray-800 mb-6">Distribution des scores</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={scoreDistribution}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="range" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#10b981" radius={[4, 4, 0, 0]} name="Nombre de candidats" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h3 className="text-lg font-bold text-gray-800 mb-6">Profil moyen vs Attendus</h3>
          <ResponsiveContainer width="100%" height={300}>
            <RadarChart data={[
              { subject: 'Technique', candidat: 78, requis: 85 },
              { subject: 'Expérience', candidat: 73, requis: 80 },
              { subject: 'Éducation', candidat: 83, requis: 85 },
              { subject: 'Soft Skills', candidat: 80, requis: 80 },
            ]}>
              <PolarGrid stroke="#e2e8f0" />
              <PolarAngleAxis dataKey="subject" />
              <PolarRadiusAxis domain={[0, 100]} />
              <Radar name="Moyenne candidats" dataKey="candidat" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.3} />
              <Radar name="Profil requis" dataKey="requis" stroke="#10b981" fill="#10b981" fillOpacity={0.3} />
              <Legend />
              <Tooltip />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        {/* <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h3 className="text-lg font-bold text-gray-800 mb-6">Taux de matching par compétence</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart layout="vertical" data={[
              { skill: 'Python', match: 92 },
              { skill: 'Machine Learning', match: 78 },
              { skill: 'SQL', match: 85 },
              { skill: 'TensorFlow', match: 45 },
              { skill: 'Deep Learning', match: 38 },
            ]}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis type="number" domain={[0, 100]} />
              <YAxis type="category" dataKey="skill" width={100} />
              <Tooltip />
              <Bar dataKey="match" fill="#3b82f6" radius={[0, 4, 4, 0]} name="Taux de match (%)" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h3 className="text-lg font-bold text-gray-800 mb-6">Plan de Travail PFE</h3>
          <div className="space-y-4">
            {[
              { phase: 'Phase I', title: 'État de l\'art', status: 'completed', desc: 'Étude des techniques de Parsing et algorithmes de similarité' },
              { phase: 'Phase II', title: 'Conception', status: 'completed', desc: 'Architecture de l\'application et base de données' },
              { phase: 'Phase III', title: 'IA & NLP', status: 'in-progress', desc: 'Moteur d\'extraction et algorithme de scoring' },
              { phase: 'Phase IV', title: 'Dev Web', status: 'pending', desc: 'Interface Frontend et API Backend' },
              { phase: 'Phase V', title: 'Validation', status: 'pending', desc: 'Tests sur jeu de données de CV réels' },
            ].map((phase, index) => (
              <div key={phase.phase} className="flex items-center gap-4">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${phase.status === 'completed' ? 'bg-emerald-500 text-white' : phase.status === 'in-progress' ? 'bg-blue-500 text-white animate-pulse' : 'bg-gray-200 text-gray-500'}`}>
                  {phase.status === 'completed' ? '✓' : index + 1}
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <p className="font-semibold text-gray-800">{phase.phase}: {phase.title}</p>
                    {phase.status === 'in-progress' && (
                      <span className="px-2 py-0.5 bg-blue-100 text-blue-700 rounded text-xs font-medium">En cours</span>
                    )}
                  </div>
                  <p className="text-sm text-gray-500">{phase.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div> */}
      </div>
    </div>
  );
};

export default AnalyticsTab;
