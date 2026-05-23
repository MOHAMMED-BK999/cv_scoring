import { X } from 'lucide-react';
import type { FormEvent } from 'react';

import type { JobDescription } from '@/types/app';

interface JobFormModalProps {
  open: boolean;
  jobDesc: JobDescription;
  onClose: () => void;
  onSubmit: (payload: JobDescription) => void;
}

const JobFormModal = ({ open, jobDesc, onClose, onSubmit }: JobFormModalProps) => {
  if (!open) {
    return null;
  }

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);

    const parseCsv = (raw: FormDataEntryValue | null) => String(raw ?? '')
      .split(',')
      .map((value) => value.trim())
      .filter((value, index, array) => value.length > 0 && array.indexOf(value) === index);

    onSubmit({
      title: String(formData.get('title') ?? '').trim(),
      company: String(formData.get('company') ?? '').trim(),
      description: String(formData.get('description') ?? '').trim(),
      requiredHardSkills: parseCsv(formData.get('requiredHardSkills')),
      requiredSoftSkills: parseCsv(formData.get('requiredSoftSkills')),
      minExperience: Number(formData.get('minExperience') ?? 0),
      educationLevel: String(formData.get('educationLevel') ?? '').trim(),
    });
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div className="p-6 border-b border-gray-100 flex items-center justify-between sticky top-0 bg-white z-10 rounded-t-2xl">
          <h3 className="text-xl font-bold text-gray-800">Modifier la fiche de poste</h3>
          <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-lg">
            <X className="w-5 h-5" />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-1">Titre du poste</label>
              <input name="title" type="text" defaultValue={jobDesc.title} className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none" required />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-1">Entreprise</label>
              <input name="company" type="text" defaultValue={jobDesc.company} className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none" required />
            </div>
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-1">Description</label>
            <textarea name="description" defaultValue={jobDesc.description} rows={3} className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none resize-none" required />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-1">Compétences techniques (séparées par virgules)</label>
              <input name="requiredHardSkills" type="text" defaultValue={jobDesc.requiredHardSkills.join(', ')} className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none" placeholder="" />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-1">Soft skills (séparés par virgules)</label>
              <input name="requiredSoftSkills" type="text" defaultValue={jobDesc.requiredSoftSkills.join(', ')} className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none" placeholder="" />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-1">Expérience minimum (années)</label>
              <input name="minExperience" type="number" min={0} defaultValue={jobDesc.minExperience} className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none" />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-1">Niveau d'études</label>
              <select name="educationLevel" defaultValue={jobDesc.educationLevel || ''} className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none bg-white">
                <option value="">Non spécifié</option>
                <option value="Licence">Licence</option>
                <option value="Master">Master</option>
                <option value="Doctorat">Doctorat</option>
                <option value="Autre">Autre</option>
              </select>
            </div>
          </div>
          <div className="flex justify-end gap-3 pt-4">
            <button type="button" onClick={onClose} className="px-4 py-2 border border-gray-200 text-gray-600 rounded-lg hover:bg-gray-50 font-medium">
              Annuler
            </button>
            <button type="submit" className="px-6 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 font-medium shadow-sm">
              Enregistrer
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default JobFormModal;
