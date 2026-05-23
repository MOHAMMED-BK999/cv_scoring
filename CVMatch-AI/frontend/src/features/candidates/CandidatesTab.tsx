import { CheckCircle, MapPin, XCircle } from 'lucide-react';

import type { Candidate } from '@/types/app';
import { normalizePercent, normalizePercentDecimal } from '@/utils/scores';

interface CandidatesTabProps {
  candidates: Candidate[];
  filteredCandidates: Candidate[];
  filterStatus: string;
  onFilterStatusChange: (status: string) => void;
  onSelectCandidate: (candidate: Candidate) => void;
  getScoreColor: (score: number) => string;
  getScoreBgColor: (score: number) => string;
}

const CandidatesTab = ({
  candidates,
  filteredCandidates,
  filterStatus,
  onFilterStatusChange,
  onSelectCandidate,
  getScoreColor,
  getScoreBgColor,
}: CandidatesTabProps) => {
  const getSafeCandidate = (candidate: Candidate): Candidate => ({
    ...candidate,
    score: normalizePercentDecimal(candidate.score),
    matchDetails: {
      technical: normalizePercent(candidate.matchDetails.technical),
      experience: normalizePercent(candidate.matchDetails.experience),
      education: normalizePercent(candidate.matchDetails.education),
      softSkills: normalizePercent(candidate.matchDetails.softSkills),
    },
    hardSkills: candidate.hardSkills.map((skill) => ({
      ...skill,
      level: normalizePercent(skill.level),
    })),
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4 flex-wrap">
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => onFilterStatusChange('all')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${filterStatus === 'all' ? 'bg-slate-900 text-white' : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'}`}
          >
            Tous ({candidates.length})
          </button>
          <button
            type="button"
            onClick={() => onFilterStatusChange('matched')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${filterStatus === 'matched' ? 'bg-emerald-600 text-white' : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'}`}
          >
            Matchés ({candidates.filter((candidate) => candidate.status === 'matched').length})
          </button>
          <button
            type="button"
            onClick={() => onFilterStatusChange('pending')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${filterStatus === 'pending' ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'}`}
          >
            En attente ({candidates.filter((candidate) => candidate.status === 'pending').length})
          </button>
          <button
            type="button"
            onClick={() => onFilterStatusChange('reviewed')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${filterStatus === 'reviewed' ? 'bg-gray-600 text-white' : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'}`}
          >
            Examinés ({candidates.filter((candidate) => candidate.status === 'reviewed').length})
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        {filteredCandidates.map((candidate) => {
          const safeCandidate = getSafeCandidate(candidate);

          return (
            <div
              key={safeCandidate.id}
              onClick={() => onSelectCandidate(safeCandidate)}
              className={`bg-white rounded-xl shadow-sm border-2 p-6 cursor-pointer hover:shadow-lg transition-all ${getScoreBgColor(safeCandidate.score)}`}
            >
              <div className="flex items-start justify-between gap-4 mb-4">
                <div className="flex items-center gap-4 min-w-0">
                  <div className="w-14 h-14 shrink-0 rounded-full bg-gradient-to-br from-slate-700 to-slate-900 flex items-center justify-center text-white font-bold text-lg">
                    {safeCandidate.name.split(' ').map((part) => part[0]).join('')}
                  </div>
                  <div className="min-w-0">
                    <h4 className="font-bold text-lg text-gray-800 break-words">{safeCandidate.name}</h4>
                    <p className="text-sm text-gray-500">{safeCandidate.education}</p>
                    <div className="flex items-center gap-2 mt-1">
                      <MapPin className="w-3 h-3 text-gray-400" />
                      <span className="text-xs text-gray-500">{safeCandidate.location}</span>
                    </div>
                  </div>
                </div>
                <div className="text-right shrink-0">
                  <p className={`text-3xl font-bold ${getScoreColor(safeCandidate.score)}`}>{safeCandidate.score}%</p>
                  <span className={`inline-block mt-1 px-2 py-0.5 rounded-full text-xs font-medium ${safeCandidate.status === 'matched' ? 'bg-emerald-100 text-emerald-700' : safeCandidate.status === 'pending' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-700'}`}>
                    {safeCandidate.status === 'matched' ? 'Matché' : safeCandidate.status === 'pending' ? 'En attente' : 'Examiné'}
                  </span>
                </div>
              </div>

              <div className="mb-4">
                <p className="text-xs font-semibold text-gray-500 mb-2">Correspondance</p>
                <div className="grid grid-cols-4 gap-2">
                  <div className="text-center">
                    <p className="text-xs text-gray-500">Tech</p>
                    <p className="font-bold text-blue-600">{safeCandidate.matchDetails.technical}%</p>
                  </div>
                  <div className="text-center">
                    <p className="text-xs text-gray-500">Exp</p>
                    <p className="font-bold text-emerald-600">{safeCandidate.matchDetails.experience}%</p>
                  </div>
                  <div className="text-center">
                    <p className="text-xs text-gray-500">Édu</p>
                    <p className="font-bold text-amber-600">{safeCandidate.matchDetails.education}%</p>
                  </div>
                  <div className="text-center">
                    <p className="text-xs text-gray-500">Soft</p>
                    <p className="font-bold text-teal-600">{safeCandidate.matchDetails.softSkills}%</p>
                  </div>
                </div>
              </div>

              <div>
                <p className="text-xs font-semibold text-gray-500 mb-2">Compétences clés</p>
                <div className="flex flex-wrap gap-1.5">
                  {safeCandidate.hardSkills.filter((skill) => skill.match).slice(0, 4).map((skill) => (
                    <span key={skill.name} className="px-2 py-1 bg-emerald-100 text-emerald-700 rounded text-xs font-medium flex items-center gap-1">
                      <CheckCircle className="w-3 h-3" />
                      {skill.name}
                    </span>
                  ))}
                  {safeCandidate.hardSkills.filter((skill) => !skill.match).slice(0, 2).map((skill) => (
                    <span key={skill.name} className="px-2 py-1 bg-red-100 text-red-700 rounded text-xs font-medium flex items-center gap-1">
                      <XCircle className="w-3 h-3" />
                      {skill.name}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default CandidatesTab;
