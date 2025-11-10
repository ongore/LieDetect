from __future__ import annotations

from ml.common.emotions import EMOTIONS, EMOTION_TO_INDEX

EMOTION_CODE_MAP = {
    '01': 'neutral',
    '02': 'calm',
    '03': 'happy',
    '04': 'sad',
    '05': 'angry',
    '06': 'fearful',
    '07': 'disgust',
    '08': 'surprised'
}

BAD_EMOTIONS = {'angry', 'fearful', 'disgust', 'sad'}
GOOD_EMOTIONS = {'happy', 'surprised', 'calm', 'neutral'}

EMOTION_INDEX = EMOTION_TO_INDEX

AUDIO_EMOTIONS = EMOTIONS
