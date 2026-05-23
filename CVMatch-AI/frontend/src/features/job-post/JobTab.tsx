import { FileSearch, Plus, Target, Zap } from 'lucide-react';

import type { JobDescription } from '@/types/app';

interface JobTabProps {
  jobDesc: JobDescription;
  onOpenForm: () => void;
}

const JobTab = ({ jobDesc, onOpenForm }: JobTabProps) => {
  const safeText = (value: string) => value.trim().length > 0 ? value : 'Non renseigné';

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-bold text-gray-800">Fiche de poste actuelle</h3>
          <button
            onClick={onOpenForm}
            className="flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors font-medium"
          >
            <Plus className="w-4 h-4" />
            Modifier
          </button>
        </div>

        <div className="grid grid-cols-2 gap-8">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-gray-500 mb-1">Titre du poste</label>
              <p className="text-xl font-bold text-gray-800">{safeText(jobDesc.title)}</p>
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-500 mb-1">Entreprise</label>
              <p className="text-gray-800">{safeText(jobDesc.company)}</p>
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-500 mb-1">Description</label>
              <p className="text-gray-600">{safeText(jobDesc.description)}</p>
            </div>
          </div>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-gray-500 mb-2">Compétences techniques requises</label>
              <div className="flex flex-wrap gap-2">
                {jobDesc.requiredHardSkills.length === 0 && (
                  <span className="px-3 py-2 bg-gray-100 text-gray-600 rounded-lg text-sm font-medium">Aucune compétence renseignée</span>
                )}
                {jobDesc.requiredHardSkills.map((skill) => (
                  <span key={skill} className="px-3 py-2 bg-blue-100 text-blue-700 rounded-lg text-sm font-medium">{skill}</span>
                ))}
              </div>
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-500 mb-2">Soft skills requis</label>
              <div className="flex flex-wrap gap-2">
                {jobDesc.requiredSoftSkills.length === 0 && (
                  <span className="px-3 py-2 bg-gray-100 text-gray-600 rounded-lg text-sm font-medium">Aucune compétence renseignée</span>
                )}
                {jobDesc.requiredSoftSkills.map((skill) => (
                  <span key={skill} className="px-3 py-2 bg-teal-100 text-teal-700 rounded-lg text-sm font-medium">{skill}</span>
                ))}
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-semibold text-gray-500 mb-1">Expérience min.</label>
                <p className="font-semibold text-gray-800">{jobDesc.minExperience} ans</p>
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-500 mb-1">Niveau d'études</label>
                <p className="font-semibold text-gray-800">{safeText(jobDesc.educationLevel)}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6">
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-6 border border-blue-200">
          <div className="p-3 bg-white rounded-lg w-fit mb-4 shadow-sm">
            <FileSearch className="w-6 h-6 text-blue-600" />
          </div>
          <h4 className="font-bold text-blue-900 mb-2">Centralisation des candidatures</h4>
          <p className="text-sm text-blue-700">Regroupez les CV et standardisez l'analyse quel que soit le métier ciblé.</p>
        </div>
        <div className="bg-gradient-to-br from-emerald-50 to-emerald-100 rounded-xl p-6 border border-emerald-200">
          <div className="p-3 bg-white rounded-lg w-fit mb-4 shadow-sm">
            <Target className="w-6 h-6 text-emerald-600" />
          </div>
          <h4 className="font-bold text-emerald-900 mb-2">Évaluation multicritère</h4>
          <p className="text-sm text-emerald-700">Comparez compétences, expérience et soft skills selon vos exigences métier.</p>
        </div>
        <div className="bg-gradient-to-br from-amber-50 to-amber-100 rounded-xl p-6 border border-amber-200">
          <div className="p-3 bg-white rounded-lg w-fit mb-4 shadow-sm">
            <Zap className="w-6 h-6 text-amber-600" />
          </div>
          <h4 className="font-bold text-amber-900 mb-2">Aide à la décision</h4>
          <p className="text-sm text-amber-700">Priorisez rapidement les meilleurs profils pour accélérer votre recrutement.</p>
        </div>
      </div>
    </div>
  );
};

export default JobTab;
