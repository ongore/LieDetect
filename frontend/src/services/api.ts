import { env } from '@/config/env';
import { LieDetectResponse, ParticipantRole, UploadMediaResponse } from '@/types/lieDetection';

const jsonHeaders = {
  Accept: 'application/json',
  'Content-Type': 'application/json'
};

const handleResponse = async (response: Response) => {
  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(`API ${response.status}: ${errorBody}`);
  }
  return response.json();
};

export const uploadSessionMedia = async (
  videoUri: string,
  role: ParticipantRole,
  sessionId: string
): Promise<UploadMediaResponse> => {
  const formData = new FormData();
  formData.append('sessionId', sessionId);
  formData.append('role', role);
  formData.append('video', {
    uri: videoUri,
    name: `session-${sessionId}.mp4`,
    type: 'video/mp4'
  } as unknown as any);

  const response = await fetch(`${env.apiBaseUrl}/upload`, {
    method: 'POST',
    headers: {
      Accept: 'application/json'
    },
    body: formData
  });

  return handleResponse(response);
};

export const runLieDetect = async (sessionId: string): Promise<LieDetectResponse> => {
  const response = await fetch(`${env.apiBaseUrl}/liedetect`, {
    method: 'POST',
    headers: jsonHeaders,
    body: JSON.stringify({ sessionId })
  });

  return handleResponse(response);
};

export const getTranscript = async (sessionId: string): Promise<{ transcript: string }> => {
  const response = await fetch(`${env.apiBaseUrl}/transcript`, {
    method: 'POST',
    headers: jsonHeaders,
    body: JSON.stringify({ sessionId })
  });

  return handleResponse(response);
};

