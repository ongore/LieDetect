import { SafeAreaView, StyleSheet, View, Text } from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { CameraStackParamList } from '@/navigation/CameraStack';
import { colors } from '@/theme/colors';
import { spacing } from '@/theme/spacing';
import { typography } from '@/theme/typography';
import { Button } from '@/components/ui/Button';

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
        <Button title="Run again" variant="secondary" onPress={() => navigation.navigate('Camera')} />
        <Button title="Back to home" onPress={() => navigation.getParent()?.navigate('GetStarted')} />
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
    alignItems: 'center',
    shadowColor: '#000',
    shadowOpacity: 0.25,
    shadowRadius: 16,
    shadowOffset: { width: 0, height: 10 },
    elevation: 10
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
    backgroundColor: '#162547',
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
    gap: spacing.sm,
    shadowColor: '#000',
    shadowOpacity: 0.2,
    shadowRadius: 12,
    shadowOffset: { width: 0, height: 8 },
    elevation: 8
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
    backgroundColor: '#13213F',
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.08)'
  },
  chipText: {
    ...typography.caption,
    color: colors.textPrimary
  },
  metricBox: {
    backgroundColor: colors.surface,
    borderRadius: 16,
    padding: spacing.md,
    gap: spacing.xs,
    shadowColor: '#000',
    shadowOpacity: 0.2,
    shadowRadius: 12,
    shadowOffset: { width: 0, height: 6 },
    elevation: 8
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
  // Buttons now come from shared Button component; no extra styles
});

