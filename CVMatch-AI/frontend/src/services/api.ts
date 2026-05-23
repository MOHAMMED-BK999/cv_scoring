import { api } from '@/lib/axios';

export interface JobCreatePayload {
  title: string;
  description: string;
  required_hard_skills: string[];
  required_soft_skills: string[];
  min_experience_years: number;
  required_degree?: string | null;
}

export interface JobResponsePayload {
  id: number;
  title: string;
  description: string;
  required_hard_skills?: string[];
  required_soft_skills?: string[];
  min_experience_years?: number;
  required_degree?: string | null;
}

export interface UploadResponsePayload {
  message: string;
  cv_id: number;
  score: number;
  global_score?: number;
  candidate_name?: string | null;
  recommendation?: string;
}

export interface RankingItemPayload {
  candidate_id: number;
  cv_id?: number;
  cv_filename: string;
  email: string | null;
  global_score: number;
  semantic_score: number;
  ollama_judgement?: string | null;
}

export interface JobRankingsPayload {
  job_id: number;
  rankings: RankingItemPayload[];
}

export interface CvScoreDetailPayload {
  candidate_id: number;
  global_score: number;
  semantic_score: number;
  skills_score?: number;
  experience_score?: number;
  education_score?: number;
  explanation: string;
  ollama_judgement?: string | null;
  matched_skills: string[];
  missing_skills: string[];
}

export interface HealthPayload {
  status: string;
  ready?: boolean;
  ai_model?: string;
}

export async function fetchApiHealth(): Promise<HealthPayload> {
  const response = await api.get<HealthPayload>('/health');
  return response.data;
}

export async function getAllJobs(): Promise<JobResponsePayload[]> {
  const response = await api.get<JobResponsePayload[]>('/api/v1/jobs');
  return response.data;
}

export async function createJob(payload: JobCreatePayload): Promise<JobResponsePayload> {
  const response = await api.post<JobResponsePayload>('/api/v1/jobs', payload);
  return response.data;
}

export async function uploadCvFile(jobId: number, file: File, weights?: { skills: number; experience: number; education: number; softSkills: number }): Promise<UploadResponsePayload> {
  const formData = new FormData();
  formData.append('file', file);
  if (weights) {
    formData.append('weight_skills', (weights.skills / 100).toString());
    formData.append('weight_experience', (weights.experience / 100).toString());
    formData.append('weight_education', (weights.education / 100).toString());
    formData.append('weight_soft_skills', (weights.softSkills / 100).toString());
  }
  
  const response = await api.post<UploadResponsePayload>(`/api/v1/jobs/${jobId}/cvs/upload`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
}

export async function getJobRankings(jobId: number): Promise<JobRankingsPayload> {
  const response = await api.get<JobRankingsPayload>(`/api/v1/jobs/${jobId}/scores`);
  return response.data;
}

export async function getCvScoreDetail(cvId: number): Promise<CvScoreDetailPayload> {
  const response = await api.get<CvScoreDetailPayload>(`/api/v1/cvs/${cvId}/score`);
  return response.data;
}
