import { View, Text, StyleSheet, SafeAreaView, Alert } from 'react-native';
import { Video, ResizeMode } from 'expo-av';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { CameraStackParamList } from '@/navigation/CameraStack';
import { colors } from '@/theme/colors';
import { spacing } from '@/theme/spacing';
import { typography } from '@/theme/typography';
import { LoadingOverlay } from '@/components/LoadingOverlay';
import { useLieDetection } from '@/hooks/useLieDetection';
import { Button } from '@/components/ui/Button';

type Props = NativeStackScreenProps<CameraStackParamList, 'Review'>;

export const ReviewScreen = ({ route, navigation }: Props) => {
  const { videoUri, role } = route.params;
  const { submit, isBusy } = useLieDetection({
    onError: (error) => {
      Alert.alert('LieDetect failed', error.message);
    }
  });

  const handleLieDetect = async () => {
    try {
      const response = await submit(videoUri, role);
      navigation.navigate('Results', response);
    } finally {
      // noop, hook manages loading state
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.videoWrapper}>
        <Video
          style={styles.video}
          source={{ uri: videoUri }}
          useNativeControls
          shouldPlay
          isLooping
          resizeMode={ResizeMode.CONTAIN}
        />
      </View>

      <View style={styles.metaBox}>
        <Text style={styles.metaLabel}>Recording role</Text>
        <Text style={styles.metaValue}>{role === 'answerer' ? 'Answerer' : 'Questioner'}</Text>
      </View>

      <View style={styles.actions}>
        <Button title="Retake" variant="secondary" onPress={() => !isBusy && navigation.goBack()} disabled={isBusy} />
        <Button title="Run LieDetect" onPress={handleLieDetect} disabled={isBusy} />
      </View>

      {isBusy && <LoadingOverlay message="Uploading and analyzing session…" />}
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
    padding: spacing.lg
  },
  videoWrapper: {
    flex: 1,
    borderRadius: 16,
    overflow: 'hidden',
    backgroundColor: 'black'
  },
  video: {
    flex: 1
  },
  metaBox: {
    marginTop: spacing.lg,
    padding: spacing.md,
    borderRadius: 12,
    backgroundColor: colors.surface
  },
  metaLabel: {
    ...typography.caption,
    color: colors.textSecondary,
    marginBottom: spacing.xs
  },
  metaValue: {
    ...typography.titleMedium,
    color: colors.textPrimary
  },
  actions: {
    flexDirection: 'row',
    gap: spacing.md,
    marginTop: spacing.xl
  },
  disabledButton: {
    opacity: 0.6
  }
});

