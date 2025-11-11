import { useRef, useState } from 'react';
import { StyleSheet, View, Text, TouchableOpacity, SafeAreaView } from 'react-native';
import { Camera, CameraView } from 'expo-camera';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { CameraStackParamList } from '@/navigation/CameraStack';
import { colors } from '@/theme/colors';
import { spacing } from '@/theme/spacing';
import { typography } from '@/theme/typography';
import { ParticipantRole } from '@/types/lieDetection';

type Props = NativeStackScreenProps<CameraStackParamList, 'Camera'>;

export const CameraScreen = ({ navigation }: Props) => {
  const cameraRef = useRef<CameraView | null>(null);
  const [permissionGranted, setPermissionGranted] = useState(false);
  const [microphoneGranted, setMicrophoneGranted] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [cameraType, setCameraType] = useState<'front' | 'back'>('front');
  const [role, setRole] = useState<ParticipantRole>('answerer');

  const ensurePermissions = async () => {
    const cam = await Camera.requestCameraPermissionsAsync();
    setPermissionGranted(cam.granted);
    const mic = await Camera.requestMicrophonePermissionsAsync();
    setMicrophoneGranted(mic.granted);
  };

  const handleRecord = async () => {
    await ensurePermissions();
    const camera = cameraRef.current;
    if (!camera) {
      return;
    }

    if (isRecording) {
      camera.stopRecording();
      return;
    }

    try {
      setIsRecording(true);
      const video = await camera.recordAsync({
        maxDuration: 120
      });

      if (video?.uri) {
        navigation.navigate('Review', {
          videoUri: video.uri,
          role
        });
      } else {
        console.warn('Recording returned no video');
      }
    } catch (error) {
      console.warn('Recording failed', error);
    } finally {
      setIsRecording(false);
    }
  };

  const toggleCamera = () => {
    setCameraType((prev) => (prev === 'front' ? 'back' : 'front'));
    setRole((prev) => (prev === 'answerer' ? 'questioner' : 'answerer'));
  };

  if (!permissionGranted || !microphoneGranted) {
    return (
      <SafeAreaView style={styles.permissionContainer}>
        <Text style={styles.permissionTitle}>Camera & microphone required</Text>
        <Text style={styles.permissionBody}>
          LieDetect needs access to capture responses and analyze audio-visual cues.
        </Text>
        <TouchableOpacity style={styles.primaryButton} onPress={ensurePermissions}>
          <Text style={styles.primaryButtonText}>Grant permissions</Text>
        </TouchableOpacity>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.cameraWrapper}>
        <CameraView
          ref={cameraRef}
          style={StyleSheet.absoluteFill}
          facing={cameraType}
          mode="video"
          videoQuality="1080p"
        />
        <View style={styles.overlay}>
          <Text style={styles.roleLabel}>{role === 'answerer' ? 'Answerer' : 'Questioner'} mode</Text>
        </View>
      </View>

      <View style={styles.controls}>
        <TouchableOpacity style={styles.iconButton} onPress={toggleCamera}>
          <Text style={styles.iconButtonText}>Flip</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.recordButton, isRecording && styles.recordButtonActive]}
          onPress={handleRecord}
        >
          <Text style={styles.recordText}>{isRecording ? 'Stop' : 'Record'}</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.iconButton}
          onPress={() =>
            navigation.navigate('Results', {
              sessionId: 'preview-skip',
              summary: {
                lieProbability: 0,
                audioScore: 0,
                macroScore: 0,
                microScore: 0,
                comparisonVector: [],
                transcript: 'Transcript will appear here after analysis.'
              }
            })
          }
        >
          <Text style={styles.iconButtonText}>Skip</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background
  },
  cameraWrapper: {
    flex: 1,
    backgroundColor: 'black'
  },
  overlay: {
    position: 'absolute',
    top: spacing.lg,
    left: 0,
    right: 0,
    alignItems: 'center'
  },
  roleLabel: {
    ...typography.button,
    color: colors.textPrimary,
    backgroundColor: 'rgba(10, 18, 34, 0.7)',
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.xs,
    borderRadius: 999
  },
  controls: {
    flexDirection: 'row',
    justifyContent: 'space-evenly',
    alignItems: 'center',
    paddingVertical: spacing.lg,
    backgroundColor: colors.surface
  },
  iconButton: {
    padding: spacing.md,
    backgroundColor: '#182544',
    borderRadius: 12
  },
  iconButtonText: {
    ...typography.button,
    color: colors.textPrimary
  },
  recordButton: {
    width: 96,
    height: 96,
    borderRadius: 48,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.primary
  },
  recordButtonActive: {
    backgroundColor: colors.accent
  },
  recordText: {
    ...typography.button,
    color: colors.textPrimary
  },
  permissionContainer: {
    flex: 1,
    backgroundColor: colors.background,
    padding: spacing.lg,
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.md
  },
  permissionTitle: {
    ...typography.titleMedium,
    color: colors.textPrimary,
    textAlign: 'center'
  },
  permissionBody: {
    ...typography.body,
    color: colors.textSecondary,
    textAlign: 'center'
  },
  primaryButton: {
    backgroundColor: colors.primary,
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.lg,
    borderRadius: 12
  },
  primaryButtonText: {
    ...typography.button,
    color: colors.textPrimary
  }
});

