# AudioLie Pipeline

This module contains data preparation, training, and inference helpers for the audio-based lie detection model.

## Steps

1. **Place Dataset** – Download the RAVDESS dataset and extract it into data/raw/ravdess (configurable via AUDIO_DATASET_DIR).
2. **Install Dependencies** – pip install -r ml/requirements.txt.
3. **Train Model** – Run python -m ml.audio_lie.train. The best checkpoint is saved to data/processed/audio/audio_emotion_net.pt.
4. **Export / Evaluate** – Use ml/audio_lie/inference.py helpers to generate emotion vectors and lie scores for new audio clips.

Environment variables in ml/audio_lie/config.py can be overridden to customize paths and training hyperparameters.
