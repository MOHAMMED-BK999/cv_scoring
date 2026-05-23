import { Award, ChevronRight, Clock, FileText, Star, Target, TrendingUp, Users, Zap } from 'lucide-react';
import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts';

import type { Candidate, JobDescription } from '@/types/app';

interface DashboardTabProps {
  candidates: Candidate[];
  filteredCandidates: Candidate[];
  matchedCount: number;
  avgScore: number;
  jobDesc: JobDescription;
  onSelectCandidate: (candidate: Candidate) => void;
  onGoCandidates: () => void;
  onGoJob: () => void;
  getScoreColor: (score: number) => string;
  getScoreBarColor: (score: number) => string;
}

const COLORS_STATUS = ['#10b981', '#3b82f6', '#6b7280'];

const DashboardTab = ({
  candidates,
  filteredCandidates,
  matchedCount,
  avgScore,
  jobDesc,
  onSelectCandidate,
  onGoCandidates,
  onGoJob,
  getScoreColor,
  getScoreBarColor,
}: DashboardTabProps) => {
  const safeText = (value: string) => value.trim().length > 0 ? value : 'Non renseigné';

  const statusData = [
    { name: 'Matchés', value: candidates.filter((candidate) => candidate.status === 'matched').length },
    { name: 'En attente', value: candidates.filter((candidate) => candidate.status === 'pending').length },
    { name: 'Examinés', value: candidates.filter((candidate) => candidate.status === 'reviewed').length },
  ];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-4 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 bg-blue-100 rounded-lg">
              <Users className="w-6 h-6 text-blue-600" />
            </div>
            <span className="text-emerald-600 text-sm font-medium flex items-center gap-1">
              <TrendingUp className="w-4 h-4" /> +12%
            </span>
          </div>
          <p className="text-3xl font-bold text-gray-800">{candidates.length}</p>
          <p className="text-sm text-gray-500">CV analysés</p>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 bg-emerald-100 rounded-lg">
              <Award className="w-6 h-6 text-emerald-600" />
            </div>
            <span className="text-emerald-600 text-sm font-medium flex items-center gap-1">
              <TrendingUp className="w-4 h-4" /> +8%
            </span>
          </div>
          <p className="text-3xl font-bold text-gray-800">{matchedCount}</p>
          <p className="text-sm text-gray-500">Candidats matchés</p>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 bg-amber-100 rounded-lg">
              <Target className="w-6 h-6 text-amber-600" />
            </div>
            <span className="text-emerald-600 text-sm font-medium flex items-center gap-1">
              <TrendingUp className="w-4 h-4" /> +5%
            </span>
          </div>
          <p className="text-3xl font-bold text-gray-800">{avgScore}%</p>
          <p className="text-sm text-gray-500">Score moyen</p>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 bg-red-100 rounded-lg">
              <Clock className="w-6 h-6 text-red-600" />
            </div>
            <span className="text-amber-600 text-sm font-medium flex items-center gap-1">
              <Clock className="w-4 h-4" /> En cours
            </span>
          </div>
          <p className="text-3xl font-bold text-gray-800">{candidates.filter((candidate) => candidate.status === 'pending').length}</p>
          <p className="text-sm text-gray-500">En attente</p>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-2 bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-bold text-gray-800">Classement des candidats</h3>
            <button
              onClick={onGoCandidates}
              className="text-sm text-emerald-600 hover:text-emerald-700 font-medium flex items-center gap-1"
            >
              Voir tout <ChevronRight className="w-4 h-4" />
            </button>
          </div>
          <div className="space-y-4">
            {filteredCandidates.slice(0, 5).map((candidate, index) => (
              <div
                key={candidate.id}
                onClick={() => onSelectCandidate(candidate)}
                className="flex items-center gap-4 p-4 rounded-lg border border-gray-100 hover:bg-gray-50 hover:border-emerald-200 transition-all cursor-pointer group"
              >
                <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm ${index === 0 ? 'bg-amber-400 text-amber-900' : index === 1 ? 'bg-gray-300 text-gray-700' : index === 2 ? 'bg-orange-400 text-orange-900' : 'bg-gray-100 text-gray-500'}`}>
                  {index + 1}
                </div>
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-emerald-400 to-emerald-600 flex items-center justify-center text-white font-bold">
                  {candidate.name.split(' ').map((part) => part[0]).join('')}
                </div>
                <div className="flex-1">
                  <p className="font-semibold text-gray-800 group-hover:text-emerald-700 transition-colors">{candidate.name}</p>
                  <p className="text-sm text-gray-500">{candidate.education}</p>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-32 h-2 bg-gray-100 rounded-full overflow-hidden">
                    <div className={`h-full rounded-full transition-all duration-500 ${getScoreBarColor(candidate.score)}`} style={{ width: `${candidate.score}%` }} />
                  </div>
                  <span className={`text-xl font-bold ${getScoreColor(candidate.score)} min-w-16 text-right`}>
                    {candidate.score}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h3 className="text-lg font-bold text-gray-800 mb-6">Distribution par statut</h3>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie data={statusData} cx="50%" cy="50%" innerRadius={50} outerRadius={80} paddingAngle={5} dataKey="value">
                {statusData.map((_entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS_STATUS[index % COLORS_STATUS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
          <div className="space-y-2 mt-4">
            {statusData.map((item, index) => (
              <div key={item.name} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: COLORS_STATUS[index] }} />
                  <span className="text-sm text-gray-600">{item.name}</span>
                </div>
                <span className="font-semibold">{item.value}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-bold text-gray-800">Profil recherché</h3>
          <button
            onClick={onGoJob}
            className="flex items-center gap-2 px-4 py-2 bg-slate-900 text-white rounded-lg hover:bg-slate-800 transition-colors text-sm font-medium"
          >
            <FileText className="w-4 h-4" />
            Modifier la fiche
          </button>
        </div>
        <div className="grid grid-cols-3 gap-6">
          <div>
            <p className="text-2xl font-bold text-gray-800">{safeText(jobDesc.title)}</p>
            <p className="text-gray-500">{safeText(jobDesc.company)}</p>
            <p className="text-sm text-gray-600 mt-3">{safeText(jobDesc.description)}</p>
          </div>
          <div>
            <p className="font-semibold text-gray-700 mb-3 flex items-center gap-2">
              <Zap className="w-4 h-4 text-emerald-600" />
              Compétences techniques requises
            </p>
            <div className="flex flex-wrap gap-2">
              {jobDesc.requiredHardSkills.length === 0 && (
                <span className="px-3 py-1.5 bg-gray-100 text-gray-600 rounded-full text-sm font-medium">
                  Aucune compétence renseignée
                </span>
              )}
              {jobDesc.requiredHardSkills.map((skill) => (
                <span key={skill} className="px-3 py-1.5 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
                  {skill}
                </span>
              ))}
            </div>
            <p className="font-semibold text-gray-700 mt-4 mb-3 flex items-center gap-2">
              <Star className="w-4 h-4 text-amber-600" />
              Expérience minimum
            </p>
            <p className="text-gray-600">{jobDesc.minExperience} ans</p>
          </div>
          <div>
            <p className="font-semibold text-gray-700 mb-3 flex items-center gap-2">
              <Users className="w-4 h-4 text-teal-600" />
              Soft skills requis
            </p>
            <div className="flex flex-wrap gap-2">
              {jobDesc.requiredSoftSkills.length === 0 && (
                <span className="px-3 py-1.5 bg-gray-100 text-gray-600 rounded-full text-sm font-medium">
                  Aucune compétence renseignée
                </span>
              )}
              {jobDesc.requiredSoftSkills.map((skill) => (
                <span key={skill} className="px-3 py-1.5 bg-teal-100 text-teal-700 rounded-full text-sm font-medium">
                  {skill}
                </span>
              ))}
            </div>
            <p className="font-semibold text-gray-700 mt-4 mb-3 flex items-center gap-2">
              <FileText className="w-4 h-4 text-purple-600" />
              Niveau d'études requis
            </p>
            <p className="text-gray-600">{safeText(jobDesc.educationLevel)}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardTab;
