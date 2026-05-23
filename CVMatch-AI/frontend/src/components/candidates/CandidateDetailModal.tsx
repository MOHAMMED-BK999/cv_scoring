import { Brain, Briefcase, CheckCircle, Download, GraduationCap, Mail, MapPin, Phone, X, XCircle } from 'lucide-react';
import { Legend, PolarAngleAxis, PolarGrid, PolarRadiusAxis, Radar, RadarChart, ResponsiveContainer, Tooltip } from 'recharts';

import type { Candidate } from '@/types/app';
import { normalizePercent, normalizePercentDecimal } from '@/utils/scores';

interface CandidateDetailModalProps {
  candidate: Candidate | null;
  radarData: Array<{ subject: string; candidat: number; requis: number }>;
  onClose: () => void;
  onUpdateCandidateStatus: (candidateId: number, status: Candidate['status']) => void;
  getScoreColor: (score: number) => string;
  getScoreBgColor: (score: number) => string;
}

const CandidateDetailModal = ({
  candidate,
  radarData,
  onClose,
  onUpdateCandidateStatus,
  getScoreColor,
  getScoreBgColor,
}: CandidateDetailModalProps) => {
  if (!candidate) {
    return null;
  }

  const score = normalizePercentDecimal(candidate.score);
  const safeRadarData = radarData.map((item) => ({
    ...item,
    candidat: normalizePercent(item.candidat),
    requis: normalizePercent(item.requis),
  }));
  const matchRows = [
    { label: 'Compétences Techniques', value: normalizePercent(candidate.matchDetails.technical), color: 'bg-blue-500' },
    { label: 'Expérience', value: normalizePercent(candidate.matchDetails.experience), color: 'bg-emerald-500' },
    { label: 'Niveau d’études', value: normalizePercent(candidate.matchDetails.education), color: 'bg-amber-500' },
    { label: 'Soft Skills', value: normalizePercent(candidate.matchDetails.softSkills), color: 'bg-teal-500' },
  ];
  const hardSkills = candidate.hardSkills.map((skill) => ({
    ...skill,
    level: normalizePercent(skill.level),
  }));

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-6xl max-h-[90vh] overflow-y-auto">
        <div className="p-6 border-b border-gray-100 flex items-center justify-between sticky top-0 bg-white z-10 rounded-t-2xl">
          <h3 className="text-xl font-bold text-gray-800">Détails du candidat</h3>
          <button type="button" onClick={onClose} className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6">
          <div className="flex flex-col lg:flex-row lg:items-center gap-6 mb-8">
            <div className="w-20 h-20 shrink-0 rounded-full bg-gradient-to-br from-slate-700 to-slate-900 flex items-center justify-center text-white font-bold text-2xl">
              {candidate.name.split(' ').map((part) => part[0]).join('')}
            </div>
            <div className="flex-1 min-w-0">
              <h4 className="text-2xl font-bold text-gray-800 break-words">{candidate.name}</h4>
              <p className="text-gray-500">{candidate.education}</p>
              <div className="flex items-center gap-4 mt-2 flex-wrap">
                <div className="flex items-center gap-1 text-sm text-gray-500"><Mail className="w-4 h-4" />{candidate.email}</div>
                <div className="flex items-center gap-1 text-sm text-gray-500"><Phone className="w-4 h-4" />{candidate.phone}</div>
                <div className="flex items-center gap-1 text-sm text-gray-500"><MapPin className="w-4 h-4" />{candidate.location}</div>
              </div>
            </div>
            <div className={`text-center p-4 rounded-xl border-2 self-start lg:self-center ${getScoreBgColor(score)}`}>
              <p className={`text-4xl font-bold ${getScoreColor(score)}`}>{score}%</p>
              <p className="text-sm text-gray-500">Score de matching</p>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-gray-50 rounded-xl p-6">
              <h5 className="font-bold text-gray-800 mb-4">Comparaison Radar</h5>
              <ResponsiveContainer width="100%" height={280}>
                <RadarChart data={safeRadarData}>
                  <PolarGrid stroke="#e2e8f0" />
                  <PolarAngleAxis dataKey="subject" />
                  <PolarRadiusAxis domain={[0, 100]} />
                  <Radar name="Candidat" dataKey="candidat" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.4} />
                  <Radar name="Profil requis" dataKey="requis" stroke="#10b981" fill="#10b981" fillOpacity={0.2} />
                  <Legend />
                  <Tooltip />
                </RadarChart>
              </ResponsiveContainer>
            </div>

            <div className="space-y-4">
              <h5 className="font-bold text-gray-800">Détails de la correspondance</h5>
              {matchRows.map((item) => (
                <div key={item.label}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm text-gray-600">{item.label}</span>
                    <span className={`text-sm font-bold ${item.value >= 70 ? 'text-emerald-600' : 'text-amber-600'}`}>{item.value}%</span>
                  </div>
                  <div className="w-full h-3 bg-gray-100 rounded-full overflow-hidden">
                    <div className={`h-full rounded-full transition-all duration-700 ${item.color}`} style={{ width: `${item.value}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {candidate.ollamaJudgement && (
            <div className="mt-6 rounded-xl border border-violet-200 bg-violet-50 p-5">
              <h5 className="font-bold text-violet-900 mb-2 flex items-center gap-2">
                <Brain className="w-5 h-5 text-violet-700" />
                Jugement IA en cas d'égalité
              </h5>
              <p className="text-sm leading-6 text-violet-900 whitespace-pre-line">
                {candidate.ollamaJudgement}
              </p>
            </div>
          )}

          <div className="mt-6">
            <h5 className="font-bold text-gray-800 mb-4">Compétences techniques</h5>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {hardSkills.map((skill) => (
                <div key={skill.name} className={`p-4 rounded-lg border ${skill.match ? 'bg-emerald-50 border-emerald-200' : 'bg-gray-50 border-gray-200'}`}>
                  <div className="flex items-center justify-between gap-3 mb-2">
                    <div className="flex items-center gap-2 min-w-0">
                      {skill.match ? <CheckCircle className="w-4 h-4 shrink-0 text-emerald-600" /> : <XCircle className="w-4 h-4 shrink-0 text-gray-400" />}
                      <span className="font-medium text-gray-800 break-words">{skill.name}</span>
                    </div>
                    <span className={`text-sm font-bold shrink-0 ${skill.level >= 70 ? 'text-emerald-600' : skill.level >= 40 ? 'text-amber-600' : 'text-red-600'}`}>{skill.level}%</span>
                  </div>
                  <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                    <div className={`h-full rounded-full transition-all duration-700 ${skill.level >= 70 ? 'bg-emerald-500' : skill.level >= 40 ? 'bg-amber-500' : 'bg-red-500'}`} style={{ width: `${skill.level}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
            <div>
              <h5 className="font-bold text-gray-800 mb-4 flex items-center gap-2"><Briefcase className="w-5 h-5 text-blue-600" />Expériences professionnelles</h5>
              <div className="space-y-3">
                {candidate.experiences.map((experience, index) => (
                  <div key={index} className="p-4 bg-blue-50 rounded-lg border border-blue-100">
                    <p className="font-semibold text-gray-800">{experience.title}</p>
                    <p className="text-sm text-gray-600">{experience.company}</p>
                    <p className="text-xs text-gray-500 mt-1">{experience.duration}</p>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <h5 className="font-bold text-gray-800 mb-4 flex items-center gap-2"><GraduationCap className="w-5 h-5 text-emerald-600" />Formation</h5>
              <div className="space-y-3">
                {candidate.educations.map((education, index) => (
                  <div key={index} className="p-4 bg-emerald-50 rounded-lg border border-emerald-100">
                    <p className="font-semibold text-gray-800">{education.degree}</p>
                    <p className="text-sm text-gray-600">{education.school}</p>
                    <p className="text-xs text-gray-500 mt-1">{education.year}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="mt-6">
            <h5 className="font-bold text-gray-800 mb-4">Soft Skills</h5>
            <div className="flex flex-wrap gap-2">
              {candidate.softSkills.map((skill) => (
                <span key={skill.name} className={`px-4 py-2 rounded-full text-sm font-medium ${skill.match ? 'bg-teal-100 text-teal-700' : 'bg-gray-100 text-gray-400'}`}>
                  {skill.match ? '✓' : '○'} {skill.name}
                </span>
              ))}
            </div>
          </div>

          <div className="mt-8 pt-6 border-t border-gray-100 flex items-center justify-end gap-3 flex-wrap">
            <button type="button" className="px-4 py-2 border border-gray-200 text-gray-600 rounded-lg hover:bg-gray-50 transition-colors font-medium">
              <span className="flex items-center gap-2"><Download className="w-4 h-4" /> Télécharger CV</span>
            </button>
            <a
              href={`mailto:${candidate.email}`}
              className="px-4 py-2 border border-gray-200 text-gray-600 rounded-lg hover:bg-gray-50 transition-colors font-medium"
            >
              <span className="flex items-center gap-2"><Mail className="w-4 h-4" /> Contacter</span>
            </a>
            <button
              type="button"
              onClick={() => onUpdateCandidateStatus(candidate.id, 'pending')}
              className="px-4 py-2 border border-blue-200 text-blue-700 rounded-lg hover:bg-blue-50 transition-colors font-medium"
            >
              En attente
            </button>
            <button
              type="button"
              onClick={() => onUpdateCandidateStatus(candidate.id, 'reviewed')}
              className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-100 transition-colors font-medium"
            >
              Examiné
            </button>
            <button
              type="button"
              onClick={() => onUpdateCandidateStatus(candidate.id, 'matched')}
              className="px-6 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors font-medium shadow-sm"
            >
              <span className="flex items-center gap-2"><CheckCircle className="w-4 h-4" /> Marquer comme matché</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CandidateDetailModal;
