import { useState, useEffect, useCallback } from 'react';
import { getScoringSettings, updateScoringSettings, ScoringWeightsPayload } from '@/services/api';

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
  const [weights, setWeights] = useState<ScoringWeights>(DEFAULT_WEIGHTS);
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchSettings = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getScoringSettings();
      setWeights({
        skills: Math.round(data.skills * 100),
        experience: Math.round(data.experience * 100),
        education: Math.round(data.education * 100),
        softSkills: Math.round(data.soft_skills * 100),
      });
    } catch (err) {
      console.error('Failed to fetch settings, using defaults', err);
      // Fallback to defaults
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void fetchSettings();
  }, [fetchSettings]);

  const updateWeight = (key: keyof ScoringWeights, newValue: number) => {
    setWeights((prev) => {
      let clampedValue = Math.max(0, Math.min(100, newValue));
      const previousValue = prev[key];
      const difference = clampedValue - previousValue;

      if (difference === 0) return prev;

      // Adjust other weights proportionally
      const otherKeys = (Object.keys(prev) as Array<keyof ScoringWeights>).filter(k => k !== key);
      const remainingSum = otherKeys.reduce((sum, k) => sum + prev[k], 0);

      const newWeights = { ...prev, [key]: clampedValue };

      if (clampedValue === 100) {
        otherKeys.forEach(k => { newWeights[k] = 0; });
      } else if (remainingSum === 0) {
        // distribute the remainder evenly if others were 0
        const remainder = 100 - clampedValue;
        const part = Math.floor(remainder / otherKeys.length);
        let leftOver = remainder - (part * otherKeys.length);
        otherKeys.forEach(k => {
          newWeights[k] = part + (leftOver > 0 ? 1 : 0);
          leftOver = Math.max(0, leftOver - 1);
        });
      } else {
        const factor = (100 - clampedValue) / remainingSum;
        let runningTotal = clampedValue;
        
        // Compute adjusted for all but the last to handle rounding diffs
        for (let i = 0; i < otherKeys.length - 1; i++) {
          const k = otherKeys[i];
          const adjusted = Math.round(prev[k] * factor);
          newWeights[k] = adjusted;
          runningTotal += adjusted;
        }
        
        // Put exact remainder into the last key
        const lastKey = otherKeys[otherKeys.length - 1];
        newWeights[lastKey] = 100 - runningTotal;
      }

      // Ensure no negatives (edge cases with rounding)
      otherKeys.forEach(k => {
        if (newWeights[k] < 0) newWeights[k] = 0;
      });

      // Recalculate sum to ensure it's exactly 100 due to any clamping
      const finalSum = Object.values(newWeights).reduce((a, b) => a + b, 0);
      if (finalSum !== 100) {
        // Just adjust the last key to make it exactly 100
        const lastKey = otherKeys[otherKeys.length - 1];
        newWeights[lastKey] += (100 - finalSum);
      }

      return newWeights;
    });
  };

  const saveSettings = async () => {
    setIsSaving(true);
    setError(null);
    try {
      const payload: ScoringWeightsPayload = {
        skills: weights.skills / 100,
        experience: weights.experience / 100,
        education: weights.education / 100,
        soft_skills: weights.softSkills / 100,
      };
      await updateScoringSettings(payload);
    } catch (err) {
      setError('Erreur lors de la sauvegarde des paramètres.');
      throw err;
    } finally {
      setIsSaving(false);
    }
  };

  const resetToDefault = () => {
    setWeights(DEFAULT_WEIGHTS);
  };

  return { weights, updateWeight, saveSettings, resetToDefault, isLoading, isSaving, error };
};
