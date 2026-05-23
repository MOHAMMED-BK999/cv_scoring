import { useState } from 'react';

export interface ScoringWeights {
  skills: number;
  experience: number;
  education: number;
  softSkills: number;
}

const DEFAULT_WEIGHTS: ScoringWeights = {
  skills: 40,
  experience: 30,
  education: 20,
  softSkills: 10,
};

export const useScoringSettings = () => {
  const [weights, setWeights] = useState<ScoringWeights>(() => {
    try {
      const stored = localStorage.getItem('scoringWeights');
      return stored ? JSON.parse(stored) : DEFAULT_WEIGHTS;
    } catch {
      return DEFAULT_WEIGHTS;
    }
  });

  const updateWeight = (key: keyof ScoringWeights, value: number) => {
    setWeights((prev) => {
      const newWeights = { ...prev, [key]: value };
      localStorage.setItem('scoringWeights', JSON.stringify(newWeights));
      return newWeights;
    });
  };

  return { weights, updateWeight };
};
