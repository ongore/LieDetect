export type ParticipantRole = 'questioner' | 'answerer';

export type UploadMediaResponse = {
  sessionId: string;
  videoKey: string;
  audioKey?: string;
};

export type LieDetectSummary = {
  lieProbability: number;
  audioScore: number;
  macroScore: number;
  microScore: number;
  comparisonVector: number[];
  audioVector?: number[];
  macroVector?: number[];
  llmVector?: Record<string, number>;
  alignmentScore?: number;
  transcript?: string;
};

export type LieDetectResponse = {
  summary: LieDetectSummary;
  sessionId: string;
};

export type TranscriptResponse = {
  sessionId: string;
  transcript: string;
  summary?: LieDetectSummary | null;
};

