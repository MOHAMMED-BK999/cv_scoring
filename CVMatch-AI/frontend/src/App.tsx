import React, { useEffect, useMemo, useState } from 'react';
import { fetchApiHealth } from './services/api';
import { useScoringWorkflow } from './hooks/useScoringWorkflow';
import { useDashboardMetrics } from './hooks/useDashboardMetrics';
import Sidebar from './components/layout/Sidebar';
import TopHeader from './components/layout/TopHeader';
import UploadCvPanel from './components/upload-cv/UploadCvPanel';
import DashboardTab from './features/dashboard/DashboardTab';
import JobTab from './features/job-post/JobTab';
import CandidatesTab from './features/candidates/CandidatesTab';
import AnalyticsTab from './features/analytics/AnalyticsTab';
import SettingsTab from './features/settings/SettingsTab';
import CandidateDetailModal from './components/candidates/CandidateDetailModal';
import JobFormModal from './components/job-post/JobFormModal';
import type { ActiveTab, Candidate, JobDescription } from './types/app';

const initialJobDescription: JobDescription = {
  title: '',
  company: '',
  description: '',
  requiredHardSkills: [],
  requiredSoftSkills: [],
  minExperience: 0,
  educationLevel: '',
};

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<ActiveTab>('dashboard');
  const [candidates, setCandidates] = useState<Candidate[]>(() => {
    try {
      const saved = localStorage.getItem('app_candidates');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });
  const [jobDesc, setJobDesc] = useState<JobDescription>(() => {
    try {
      const saved = localStorage.getItem('app_jobDesc');
      return saved ? JSON.parse(saved) : initialJobDescription;
    } catch {
      return initialJobDescription;
    }
  });
  const [selectedCandidate, setSelectedCandidate] = useState<Candidate | null>(null);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [uploadedFiles, setUploadedFiles] = useState<string[]>([]);
  const [uploadedCvFiles, setUploadedCvFiles] = useState<File[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [apiStatus, setApiStatus] = useState<'unknown' | 'online' | 'offline'>('unknown');
  const [apiModel, setApiModel] = useState<string>('N/A');
  const [healthError, setHealthError] = useState<string>('');
  const [showJobForm, setShowJobForm] = useState(false);

  const {
    isAnalyzing,
    analysisError,
    ingestionMessage,
    ingestionStatus,
    analyzeCandidates,
    clearAnalysisError,
  } = useScoringWorkflow({
    jobDesc,
    uploadedCvFiles,
    setCandidates,
    setSelectedCandidate,
    setActiveTab,
    setApiStatus,
  });

  const {
    avgScore,
    matchedCount,
    scoreDistribution,
    radarData,
  } = useDashboardMetrics(candidates, selectedCandidate);

  useEffect(() => {
    const loadHealth = async () => {
      try {
        const health = await fetchApiHealth();
        setApiStatus('online');
        setApiModel(health.ai_model ?? 'N/A');
        setHealthError('');
      } catch (_error) {
        setApiStatus('offline');
        setHealthError('Backend indisponible. Vérifiez FastAPI.');
      }
    };

    void loadHealth();
  }, []);

  useEffect(() => {
    localStorage.setItem('app_jobDesc', JSON.stringify(jobDesc));
  }, [jobDesc]);

  useEffect(() => {
    localStorage.setItem('app_candidates', JSON.stringify(candidates));
  }, [candidates]);

  const filteredCandidates = useMemo(
    () => candidates.filter((candidate) => {
      const normalizedSearch = searchTerm.toLowerCase().trim();
      const matchesSearch =
        candidate.name.toLowerCase().includes(normalizedSearch)
        || candidate.email.toLowerCase().includes(normalizedSearch);
      const matchesStatus = filterStatus === 'all' || candidate.status === filterStatus;
      return matchesSearch && matchesStatus;
    }).sort((a, b) => b.score - a.score),
    [candidates, filterStatus, searchTerm],
  );

  const getScoreColor = (score: number) => {
    if (score >= 85) return 'text-emerald-600';
    if (score >= 70) return 'text-blue-600';
    if (score >= 50) return 'text-amber-600';
    return 'text-red-600';
  };

  const getScoreBgColor = (score: number) => {
    if (score >= 85) return 'bg-emerald-50 border-emerald-200';
    if (score >= 70) return 'bg-blue-50 border-blue-200';
    if (score >= 50) return 'bg-amber-50 border-amber-200';
    return 'bg-red-50 border-red-200';
  };

  const getScoreBarColor = (score: number) => {
    if (score >= 85) return 'bg-emerald-500';
    if (score >= 70) return 'bg-blue-500';
    if (score >= 50) return 'bg-amber-500';
    return 'bg-red-500';
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const selectedFiles = Array.from(e.target.files);
      setIsUploading(true);
      clearAnalysisError();

      setTimeout(() => {
        setUploadedFiles(prev => [...prev, ...selectedFiles.map((f) => f.name)]);
        setUploadedCvFiles(prev => [...prev, ...selectedFiles]);
        setIsUploading(false);
      }, 600);

      e.target.value = '';
    }
  };

  const handleJobSubmit = (payload: JobDescription) => {
    setJobDesc(payload);
    clearAnalysisError();
    setShowJobForm(false);
  };

  const handleDeleteFile = (fileIndex: number) => {
    clearAnalysisError();
    setUploadedFiles(prev => prev.filter((_fileName, index) => index !== fileIndex));
    setUploadedCvFiles(prev => prev.filter((_file, index) => index !== fileIndex));
  };

  const handleUpdateCandidateStatus = (candidateId: number, status: Candidate['status']) => {
    setCandidates((prev) => prev.map((candidate) => (
      candidate.id === candidateId
        ? { ...candidate, status }
        : candidate
    )));

    setSelectedCandidate((prev) => {
      if (!prev || prev.id !== candidateId) {
        return prev;
      }
      return {
        ...prev,
        status,
      };
    });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar activeTab={activeTab} onChangeTab={setActiveTab} />

      {/* Main Content */}
      <div className="ml-64">
        <TopHeader
          activeTab={activeTab}
          candidatesCount={candidates.length}
          filteredCount={filteredCandidates.length}
          uploadedCount={uploadedFiles.length}
          jobTitle={jobDesc.title}
          searchTerm={searchTerm}
          onSearchTermChange={setSearchTerm}
          apiStatus={apiStatus}
          apiModel={apiModel}
        />

        {/* Content Area */}
        <main className="p-8">
          {/* Dashboard Tab */}
          {activeTab === 'dashboard' && (
            <DashboardTab
              candidates={candidates}
              filteredCandidates={filteredCandidates}
              matchedCount={matchedCount}
              avgScore={avgScore}
              jobDesc={jobDesc}
              onSelectCandidate={setSelectedCandidate}
              onGoCandidates={() => setActiveTab('candidates')}
              onGoJob={() => setActiveTab('job')}
              getScoreColor={getScoreColor}
              getScoreBarColor={getScoreBarColor}
            />
          )}

          {/* Job Tab */}
          {activeTab === 'job' && (
            <JobTab jobDesc={jobDesc} onOpenForm={() => setShowJobForm(true)} />
          )}

          {/* Upload Tab */}
          {activeTab === 'upload' && (
            <div className="space-y-6">
              <UploadCvPanel
                uploadedFiles={uploadedFiles}
                isUploading={isUploading}
                isAnalyzing={isAnalyzing}
                apiError={analysisError || healthError}
                ingestionMessage={ingestionMessage}
                ingestionStatus={ingestionStatus}
                onFileUpload={handleFileUpload}
                onAnalyze={analyzeCandidates}
                onDeleteFile={handleDeleteFile}
              />

              {/* Aide workflow */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
                <h3 className="text-lg font-bold text-gray-800 mb-6">Aperçu du workflow d'analyse</h3>
                <div className="grid grid-cols-4 gap-4">
                  {[
                    { name: '1. Définition du poste', desc: 'Saisissez les critères de votre secteur (santé, industrie, finance...)', color: 'bg-blue-50 text-blue-700 border-blue-200' },
                    { name: '2. Import des CV', desc: 'Chargez un ou plusieurs CV à analyser automatiquement', color: 'bg-emerald-50 text-emerald-700 border-emerald-200' },
                    { name: '3. Scoring intelligent', desc: 'Le système compare les profils selon vos exigences', color: 'bg-amber-50 text-amber-700 border-amber-200' },
                    { name: '4. Sélection finale', desc: 'Classez et suivez les candidats selon leur statut', color: 'bg-purple-50 text-purple-700 border-purple-200' },
                  ].map((step) => (
                    <div key={step.name} className={`p-4 rounded-lg border ${step.color} hover:shadow-md transition-shadow`}>
                      <p className="font-bold">{step.name}</p>
                      <p className="text-xs opacity-75">{step.desc}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Candidates Tab */}
          {activeTab === 'candidates' && (
            <CandidatesTab
              candidates={candidates}
              filteredCandidates={filteredCandidates}
              filterStatus={filterStatus}
              onFilterStatusChange={setFilterStatus}
              onSelectCandidate={setSelectedCandidate}
              getScoreColor={getScoreColor}
              getScoreBgColor={getScoreBgColor}
            />
          )}

          {/* Analytics Tab */}
          {activeTab === 'analytics' && (
            <AnalyticsTab scoreDistribution={scoreDistribution} />
          )}

          {/* Settings Tab */}
          {activeTab === 'settings' && (
            <SettingsTab />
          )}
        </main>
      </div>

      <CandidateDetailModal
        candidate={selectedCandidate}
        radarData={radarData}
        onClose={() => setSelectedCandidate(null)}
        onUpdateCandidateStatus={handleUpdateCandidateStatus}
        getScoreColor={getScoreColor}
        getScoreBgColor={getScoreBgColor}
      />

      {/* Job Form Modal */}
      <JobFormModal
        open={showJobForm}
        jobDesc={jobDesc}
        onClose={() => setShowJobForm(false)}
        onSubmit={handleJobSubmit}
      />
    </div>
  );
};

export default App;