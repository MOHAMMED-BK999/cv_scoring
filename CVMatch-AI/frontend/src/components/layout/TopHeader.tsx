import { Search, Zap } from 'lucide-react';

import type { ActiveTab } from '@/types/app';

interface TopHeaderProps {
  activeTab: ActiveTab;
  candidatesCount: number;
  filteredCount: number;
  uploadedCount: number;
  jobTitle: string;
  searchTerm: string;
  onSearchTermChange: (value: string) => void;
  apiStatus: 'unknown' | 'online' | 'offline';
  apiModel: string;
}

const titleByTab: Record<ActiveTab, string> = {
  dashboard: 'Tableau de bord',
  job: 'Gestion des fiches de poste',
  upload: 'Upload des CV',
  candidates: 'Liste des candidats',
  analytics: 'Analytiques',
  settings: 'Paramètres',
};

const subtitleByTab = (tab: ActiveTab, values: { candidatesCount: number; filteredCount: number; uploadedCount: number; jobTitle: string }) => {
  if (tab === 'dashboard') {
    const jobLabel = values.jobTitle.trim().length > 0 ? `"${values.jobTitle}"` : 'non renseigné';
    return `Analyse de ${values.candidatesCount} candidats pour le poste ${jobLabel}`;
  }
  if (tab === 'job') return 'Définissez le profil recherché';
  if (tab === 'upload') return `${values.uploadedCount} fichiers uploadés`;
  if (tab === 'candidates') return `${values.filteredCount} candidats trouvés`;
  if (tab === 'analytics') return 'Statistiques détaillées du processus';
  return 'Configuration de l\'application';
};

const TopHeader = ({
  activeTab,
  candidatesCount,
  filteredCount,
  uploadedCount,
  jobTitle,
  searchTerm,
  onSearchTermChange,
  apiStatus,
  apiModel,
}: TopHeaderProps) => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-30">
      <div className="px-8 py-4 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">{titleByTab[activeTab]}</h2>
          <p className="text-sm text-gray-500">
            {subtitleByTab(activeTab, { candidatesCount, filteredCount, uploadedCount, jobTitle })}
          </p>
        </div>
        <div className="flex items-center gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Rechercher..."
              value={searchTerm}
              onChange={(event) => onSearchTermChange(event.target.value)}
              className="pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none w-64"
            />
          </div>
          <div className="flex items-center gap-2 px-4 py-2 bg-emerald-50 border border-emerald-200 rounded-lg">
            <Zap className="w-4 h-4 text-emerald-600" />
            <span className="text-sm font-medium text-emerald-700">
              {apiStatus === 'online' ? `IA Active (${apiModel})` : 'IA hors ligne'}
            </span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default TopHeader;
