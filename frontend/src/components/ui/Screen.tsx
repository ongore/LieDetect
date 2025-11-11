import React, { PropsWithChildren } from 'react';
import { SafeAreaView, StyleProp, StyleSheet, ViewStyle } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { colors } from '@/theme/colors';
import { spacing } from '@/theme/spacing';

type ScreenProps = PropsWithChildren<{
  style?: StyleProp<ViewStyle>;
  padded?: boolean;
}>;

export const Screen = ({ children, style, padded = true }: ScreenProps) => {
  return (
    <LinearGradient colors={['#060C1F', '#0B1530']} style={styles.gradient}>
      <SafeAreaView style={[styles.container, padded && styles.padded, style]}>{children}</SafeAreaView>
    </LinearGradient>
  );
};

const styles = StyleSheet.create({
  gradient: {
    flex: 1
  },
  container: {
    flex: 1
  },
  padded: {
    padding: spacing.lg
  }
});


