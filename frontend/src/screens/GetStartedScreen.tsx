import { LinearGradient } from 'expo-linear-gradient';
import { StyleSheet, View, Text, TouchableOpacity } from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '@/navigation/AppNavigator';
import { colors } from '@/theme/colors';
import { spacing } from '@/theme/spacing';
import { typography } from '@/theme/typography';

type Props = NativeStackScreenProps<RootStackParamList, 'GetStarted'>;

export const GetStartedScreen = ({ navigation }: Props) => {
  return (
    <LinearGradient colors={[colors.background, '#0B1630']} style={styles.container}>
      <View style={styles.hero}>
        <View style={styles.logo}>
          <Text style={styles.logoText}>LD</Text>
        </View>
        <Text style={styles.title}>LieDetect</Text>
        <Text style={styles.subtitle}>
          AI-driven truth analysis using emotion vectors, audio signals, and LLM comparison.
        </Text>
      </View>

      <View style={styles.actions}>
        <TouchableOpacity
          style={styles.primaryButton}
          onPress={() => navigation.navigate('Auth')}
        >
          <Text style={styles.primaryButtonText}>Login / Sign up</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.secondaryButton}
          onPress={() => navigation.navigate('Capture')}
        >
          <Text style={styles.secondaryButtonText}>Enter Lie Detect Mode</Text>
        </TouchableOpacity>
      </View>
    </LinearGradient>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.xl,
    justifyContent: 'space-between'
  },
  hero: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center'
  },
  logo: {
    width: 96,
    height: 96,
    borderRadius: 48,
    backgroundColor: colors.surface,
    marginBottom: spacing.lg,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: colors.primary
  },
  logoText: {
    ...typography.titleMedium,
    color: colors.primary
  },
  title: {
    ...typography.titleLarge,
    color: colors.textPrimary,
    marginBottom: spacing.md
  },
  subtitle: {
    ...typography.body,
    color: colors.textSecondary,
    textAlign: 'center',
    lineHeight: 24
  },
  actions: {
    gap: spacing.md
  },
  primaryButton: {
    backgroundColor: colors.primary,
    borderRadius: 16,
    paddingVertical: spacing.md,
    alignItems: 'center'
  },
  primaryButtonText: {
    ...typography.button,
    color: colors.textPrimary
  },
  secondaryButton: {
    borderRadius: 16,
    paddingVertical: spacing.md,
    borderWidth: 1,
    borderColor: colors.textSecondary,
    alignItems: 'center'
  },
  secondaryButtonText: {
    ...typography.button,
    color: colors.textSecondary
  }
});

