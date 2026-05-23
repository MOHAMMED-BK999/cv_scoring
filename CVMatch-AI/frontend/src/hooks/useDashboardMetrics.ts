import { useMemo } from 'react';

import type { Candidate } from '@/types/app';
import { normalizePercent, normalizePercentDecimal } from '@/utils/scores';

interface RadarDatum {
  subject: string;
  candidat: number;
  requis: number;
}

interface ScoreDistributionDatum {
  range: string;
  count: number;
}

export const useDashboardMetrics = (candidates: Candidate[], selectedCandidate: Candidate | null) => {
  const avgScore = useMemo(() => {
    if (candidates.length === 0) {
      return 0;
    }

    const sum = candidates.reduce((acc, candidate) => acc + normalizePercentDecimal(candidate.score), 0);
    return Math.round(sum / candidates.length);
  }, [candidates]);

  const matchedCount = useMemo(
    () => candidates.filter((candidate) => candidate.status === 'matched').length,
    [candidates],
  );

  const scoreDistribution = useMemo<ScoreDistributionDatum[]>(() => {
    const scores = candidates.map((candidate) => normalizePercentDecimal(candidate.score));

    return [
      { range: '90-100%', count: scores.filter((score) => score >= 90).length },
      { range: '75-89%', count: scores.filter((score) => score >= 75 && score < 90).length },
      { range: '60-74%', count: scores.filter((score) => score >= 60 && score < 75).length },
      { range: '<60%', count: scores.filter((score) => score < 60).length },
    ];
  }, [candidates]);

  const radarData = useMemo<RadarDatum[]>(() => {
    if (!selectedCandidate) {
      return [];
    }

    return [
      { subject: 'Technique', candidat: normalizePercent(selectedCandidate.matchDetails.technical), requis: 85 },
      { subject: 'Expérience', candidat: normalizePercent(selectedCandidate.matchDetails.experience), requis: 80 },
      { subject: 'Éducation', candidat: normalizePercent(selectedCandidate.matchDetails.education), requis: 85 },
      { subject: 'Soft Skills', candidat: normalizePercent(selectedCandidate.matchDetails.softSkills), requis: 80 },
    ];
  }, [selectedCandidate]);

  return {
    avgScore,
    matchedCount,
    scoreDistribution,
    radarData,
  };
};
