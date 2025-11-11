import { ActivityIndicator, StyleSheet, Text, View } from 'react-native';
import { colors } from '@/theme/colors';
import { spacing } from '@/theme/spacing';
import { typography } from '@/theme/typography';

type LoadingOverlayProps = {
  message?: string;
};

export const LoadingOverlay = ({ message = 'Processing LieDetect analysis…' }: LoadingOverlayProps) => (
  <View style={styles.overlay}>
    <View style={styles.box}>
      <ActivityIndicator size="large" color={colors.primary} />
      <Text style={styles.text}>{message}</Text>
    </View>
  </View>
);

const styles = StyleSheet.create({
  overlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(5, 10, 26, 0.8)',
    alignItems: 'center',
    justifyContent: 'center'
  },
  box: {
    backgroundColor: colors.surface,
    padding: spacing.xl,
    borderRadius: 16,
    alignItems: 'center',
    gap: spacing.md,
    shadowColor: '#000',
    shadowOpacity: 0.3,
    shadowRadius: 16,
    shadowOffset: { width: 0, height: 8 },
    elevation: 12
  },
  text: {
    ...typography.body,
    color: colors.textPrimary,
    textAlign: 'center'
  }
});

