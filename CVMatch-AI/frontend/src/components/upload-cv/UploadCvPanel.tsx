import { FileText, Trash2, Upload, Zap } from 'lucide-react';

import type { IngestionJobStatusPayload } from '@/services/api';
import IngestionProgress from '@/components/upload-cv/IngestionProgress';

interface UploadCvPanelProps {
  uploadedFiles: string[];
  isUploading: boolean;
  isAnalyzing: boolean;
  apiError: string;
  ingestionMessage: string;
  ingestionStatus: IngestionJobStatusPayload | null;
  onFileUpload: (event: React.ChangeEvent<HTMLInputElement>) => void;
  onAnalyze: () => void;
  onDeleteFile: (index: number) => void;
}

const UploadCvPanel = ({
  uploadedFiles,
  isUploading,
  isAnalyzing,
  apiError,
  ingestionMessage,
  ingestionStatus,
  onFileUpload,
  onAnalyze,
  onDeleteFile,
}: UploadCvPanelProps) => {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8">
      <div className="text-center mb-8">
        <div className="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <Upload className="w-8 h-8 text-emerald-600" />
        </div>
        <h3 className="text-xl font-bold text-gray-800 mb-2">Téléchargement de CV</h3>
        <p className="text-gray-500">Formats supportés: PDF, DOCX (Téléchargement en masse supporté)</p>
      </div>

      <label className="flex flex-col items-center justify-center w-full h-48 border-2 border-dashed border-gray-300 rounded-xl cursor-pointer hover:border-emerald-500 hover:bg-emerald-50 transition-all">
        <div className="flex flex-col items-center justify-center pt-5 pb-6">
          <FileText className="w-12 h-12 text-gray-400 mb-3" />
          <p className="mb-2 text-sm text-gray-600"><span className="font-semibold">Cliquez pour uploader</span> ou glissez-déposez</p>
          <p className="text-xs text-gray-500">PDF, DOCX jusqu'à 10MB par fichier</p>
        </div>
        <input type="file" className="hidden" multiple accept=".pdf,.docx" onChange={onFileUpload} />
      </label>

      {isUploading && (
        <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="flex items-center gap-3">
            <div className="w-5 h-5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
            <p className="text-sm text-blue-700">Préparation des fichiers en cours...</p>
          </div>
        </div>
      )}

      {uploadedFiles.length > 0 && (
        <div className="mt-6">
          <div className="flex items-center justify-between mb-4">
            <h4 className="font-semibold text-gray-800">Fichiers uploadés ({uploadedFiles.length})</h4>
            <button
              onClick={onAnalyze}
              disabled={isAnalyzing}
              className="flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors text-sm font-medium disabled:opacity-60 disabled:cursor-not-allowed"
            >
              <Zap className="w-4 h-4" />
              {isAnalyzing ? 'Analyse en cours...' : 'Lancer l\'analyse'}
            </button>
          </div>
          <div className="space-y-2">
            {uploadedFiles.map((file, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-100 hover:bg-gray-100 transition-colors">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-red-100 rounded-lg">
                    <FileText className="w-4 h-4 text-red-600" />
                  </div>
                  <div>
                    <p className="font-medium text-gray-800 text-sm">{file}</p>
                    <p className="text-xs text-gray-500">Prêt à analyser</p>
                  </div>
                </div>
                <button onClick={() => onDeleteFile(index)} className="p-2 hover:bg-red-100 rounded-lg transition-colors">
                  <Trash2 className="w-4 h-4 text-gray-400 hover:text-red-600" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {apiError && (
        <div className="mt-4 rounded-lg border border-amber-300 bg-amber-50 px-4 py-3 text-sm text-amber-700">
          {apiError}
        </div>
      )}

      <IngestionProgress status={ingestionStatus} message={ingestionMessage} />

      {uploadedFiles.length === 0 && (
        <p className="mt-6 text-sm text-gray-500">
          Ajoutez au moins un CV pour lancer l'analyse IA.
        </p>
      )}
    </div>
  );
};

export default UploadCvPanel;
