import { BarChart3, Briefcase, FileSearch, Settings, TrendingUp, Upload, Users } from 'lucide-react';

import type { ActiveTab } from '@/types/app';

interface SidebarProps {
  activeTab: ActiveTab;
  onChangeTab: (tab: ActiveTab) => void;
}

const menu: Array<{ id: ActiveTab; label: string; icon: React.ComponentType<{ className?: string }> }> = [
  { id: 'dashboard', icon: BarChart3, label: 'Tableau de bord' },
  { id: 'job', icon: Briefcase, label: 'Fiche de poste' },
  { id: 'upload', icon: Upload, label: 'Upload CV' },
  { id: 'candidates', icon: Users, label: 'Candidats' },
  { id: 'analytics', icon: TrendingUp, label: 'Analytics' },
  { id: 'settings', icon: Settings, label: 'Paramètres' },
];

const Sidebar = ({ activeTab, onChangeTab }: SidebarProps) => {
  return (
    <div className="fixed left-0 top-0 h-full w-64 bg-slate-900 text-white shadow-xl z-40">
      <div className="p-6 border-b border-slate-700">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-emerald-600 rounded-lg">
            <FileSearch className="w-6 h-6" />
          </div>
          <div>
            <h1 className="font-bold text-lg">CV Analyzer</h1>
            <p className="text-xs text-slate-400">AI Scoring System</p>
          </div>
        </div>
      </div>

      <nav className="p-4 space-y-2">
        {menu.map((item) => (
          <button
            key={item.id}
            onClick={() => onChangeTab(item.id)}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 ${
              activeTab === item.id
                ? 'bg-emerald-600 text-white shadow-lg'
                : 'text-slate-300 hover:bg-slate-800 hover:text-white'
            }`}
          >
            <item.icon className="w-5 h-5" />
            <span className="font-medium">{item.label}</span>
          </button>
        ))}
      </nav>

      <div className="absolute bottom-0 left-0 right-0 p-4">
        <div className="bg-slate-800 rounded-lg p-4">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 rounded-full bg-emerald-600 flex items-center justify-center font-bold">DR</div>
            <div>
              <p className="font-medium text-sm">Dr. Robert</p>
              <p className="text-xs text-slate-400">Recruteur Senior</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
