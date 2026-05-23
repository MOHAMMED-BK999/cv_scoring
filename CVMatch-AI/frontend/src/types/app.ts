export type ActiveTab = 'dashboard' | 'job' | 'upload' | 'candidates' | 'analytics' | 'settings';

export interface Candidate {
  id: number;
  name: string;
  email: string;
  phone: string;
  location: string;
  score: number;
  hardSkills: { name: string; match: boolean; level: number }[];
  softSkills: { name: string; match: boolean }[];
  experience: number;
  education: string;
  experiences: { title: string; company: string; duration: string }[];
  educations: { degree: string; school: string; year: string }[];
  status: 'matched' | 'pending' | 'reviewed';
  ollamaJudgement?: string | null;
  matchDetails: {
    technical: number;
    experience: number;
    education: number;
    softSkills: number;
  };
}

export interface JobDescription {
  title: string;
  company: string;
  description: string;
  requiredHardSkills: string[];
  requiredSoftSkills: string[];
  minExperience: number;
  educationLevel: string;
}
