import { useCallback, useState } from 'react';
import { uploadSessionMedia, runLieDetect, getTranscript } from '@/services/api';
import { LieDetectResponse, ParticipantRole } from '@/types/lieDetection';

type UseLieDetectionOptions = {
  onComplete?: (response: LieDetectResponse) => void;
  onError?: (error: Error) => void;
};

export const useLieDetection = ({ onComplete, onError }: UseLieDetectionOptions = {}) => {
  const [isUploading, setIsUploading] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const submit = useCallback(
    async (videoUri: string, role: ParticipantRole) => {
      const sessionId = `${Date.now()}-${Math.floor(Math.random() * 1_000_000)}`;

      try {
        setIsUploading(true);
        await uploadSessionMedia(videoUri, role, sessionId);
      } catch (error) {
        setIsUploading(false);
        const wrapped = error instanceof Error ? error : new Error('Upload failed');
        onError?.(wrapped);
        throw wrapped;
      }

      try {
        setIsUploading(false);
        setIsAnalyzing(true);

        const [analysis, transcript] = await Promise.all([
          runLieDetect(sessionId),
          getTranscript(sessionId)
        ]);

        const summary = transcript.summary ?? analysis.summary;
        const fullResponse: LieDetectResponse = {
          sessionId,
          summary: {
            ...summary,
            transcript: transcript.transcript
          }
        };

        onComplete?.(fullResponse);
        return fullResponse;
      } catch (error) {
        const wrapped = error instanceof Error ? error : new Error('Analysis failed');
        onError?.(wrapped);
        throw wrapped;
      } finally {
        setIsAnalyzing(false);
      }
    },
    [onComplete, onError]
  );

  return {
    submit,
    isUploading,
    isAnalyzing,
    isBusy: isUploading || isAnalyzing
  };
};

