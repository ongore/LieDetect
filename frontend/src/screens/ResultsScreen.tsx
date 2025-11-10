import { SafeAreaView, StyleSheet, View, Text, TouchableOpacity } from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { CameraStackParamList } from '@/navigation/CameraStack';
import { colors } from '@/theme/colors';
import { spacing } from '@/theme/spacing';
import { typography } from '@/theme/typography';

type Props = NativeStackScreenProps<CameraStackParamList, 'Results'>;

export const ResultsScreen = ({ route, navigation }: Props) => {
  const { summary, sessionId } = route.params;

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>LieDetect Analysis</Text>
      <Text style={styles.subtitle}>A composite of audio, macro, and micro emotion signals.</Text>

      <View style={styles.card}>
        <Text style={styles.cardLabel}>Lie probability</Text>
        <Text style={styles.cardValue}>{Math.round(summary.lieProbability * 100)}%</Text>
        <Text style={styles.sessionId}>Session: {sessionId}</Text>
      </View>

      <View style={styles.grid}>
        <View style={styles.statBox}>
          <Text style={styles.statLabel}>Audio score</Text>
          <Text style={styles.statValue}>{Math.round(summary.audioScore * 100)}%</Text>
        </View>
        <View style={styles.statBox}>
          <Text style={styles.statLabel}>Macro score</Text>
          <Text style={styles.statValue}>{Math.round(summary.macroScore * 100)}%</Text>
        </View>
        <View style={styles.statBox}>
          <Text style={styles.statLabel}>Micro score</Text>
          <Text style={styles.statValue}>{Math.round(summary.microScore * 100)}%</Text>
        </View>
      </View>

      <View style={styles.vectorBox}>
        <Text style={styles.vectorLabel}>Comparison vector</Text>
        <View style={styles.vectorChips}>
          {summary.comparisonVector.map((value, index) => (
            <View key={index} style={styles.chip}>
              <Text style={styles.chipText}>{value.toFixed(2)}</Text>
            </View>
          ))}
        </View>
      </View>

      {summary.llmVector && (
        <View style={styles.vectorBox}>
          <Text style={styles.vectorLabel}>LLM emotion weights</Text>
          <View style={styles.vectorChips}>
            {Object.entries(summary.llmVector).map(([emotion, value]) => (
              <View key={emotion} style={styles.chip}>
                <Text style={styles.chipText}>{`${emotion}: ${Number(value).toFixed(2)}`}</Text>
              </View>
            ))}
          </View>
        </View>
      )}

      {typeof summary.alignmentScore === 'number' && (
        <View style={styles.metricBox}>
          <Text style={styles.statLabel}>LLM alignment</Text>
          <Text style={styles.statValue}>{Math.round(summary.alignmentScore * 100)}%</Text>
        </View>
      )}

      {summary.transcript && (
        <View style={styles.transcriptBox}>
          <Text style={styles.transcriptLabel}>Transcript</Text>
          <Text style={styles.transcriptText}>{summary.transcript}</Text>
        </View>
      )}

      <View style={styles.actions}>
        <TouchableOpacity style={styles.secondaryButton} onPress={() => navigation.navigate('Camera')}>
          <Text style={styles.secondaryButtonText}>Run again</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.primaryButton}
          onPress={() => navigation.getParent()?.navigate('GetStarted')}
        >
          <Text style={styles.primaryButtonText}>Back to home</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
    padding: spacing.lg,
    gap: spacing.lg
  },
  title: {
    ...typography.titleLarge,
    color: colors.textPrimary
  },
  subtitle: {
    ...typography.body,
    color: colors.textSecondary
  },
  card: {
    backgroundColor: colors.surface,
    padding: spacing.xl,
    borderRadius: 16,
    alignItems: 'center'
  },
  cardLabel: {
    ...typography.caption,
    color: colors.textSecondary,
    marginBottom: spacing.sm
  },
  cardValue: {
    ...typography.titleLarge,
    color: colors.accent
  },
  sessionId: {
    ...typography.caption,
    color: colors.textSecondary,
    marginTop: spacing.sm
  },
  grid: {
    flexDirection: 'row',
    gap: spacing.md
  },
  statBox: {
    flex: 1,
    backgroundColor: '#182544',
    borderRadius: 12,
    padding: spacing.md,
    gap: spacing.xs
  },
  statLabel: {
    ...typography.caption,
    color: colors.textSecondary
  },
  statValue: {
    ...typography.titleMedium,
    color: colors.textPrimary
  },
  vectorBox: {
    backgroundColor: colors.surface,
    borderRadius: 16,
    padding: spacing.md,
    gap: spacing.sm
  },
  vectorLabel: {
    ...typography.caption,
    color: colors.textSecondary
  },
  vectorChips: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.sm
  },
  chip: {
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.xs,
    borderRadius: 999,
    backgroundColor: '#13213F'
  },
  chipText: {
    ...typography.caption,
    color: colors.textPrimary
  },
  metricBox: {
    backgroundColor: colors.surface,
    borderRadius: 16,
    padding: spacing.md,
    gap: spacing.xs
  },
  transcriptBox: {
    backgroundColor: '#101F3D',
    borderRadius: 16,
    padding: spacing.md,
    gap: spacing.sm
  },
  transcriptLabel: {
    ...typography.caption,
    color: colors.textSecondary
  },
  transcriptText: {
    ...typography.body,
    color: colors.textPrimary,
    lineHeight: 22
  },
  actions: {
    flexDirection: 'row',
    gap: spacing.md,
    marginTop: 'auto'
  },
  secondaryButton: {
    flex: 1,
    borderRadius: 16,
    paddingVertical: spacing.md,
    borderWidth: 1,
    borderColor: colors.textSecondary,
    alignItems: 'center'
  },
  secondaryButtonText: {
    ...typography.button,
    color: colors.textSecondary
  },
  primaryButton: {
    flex: 1,
    borderRadius: 16,
    paddingVertical: spacing.md,
    backgroundColor: colors.primary,
    alignItems: 'center'
  },
  primaryButtonText: {
    ...typography.button,
    color: colors.textPrimary
  }
});

