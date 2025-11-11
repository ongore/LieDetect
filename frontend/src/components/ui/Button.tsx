import React from 'react';
import { ActivityIndicator, GestureResponderEvent, StyleProp, StyleSheet, Text, TouchableOpacity, ViewStyle } from 'react-native';
import { colors } from '@/theme/colors';
import { spacing } from '@/theme/spacing';
import { typography } from '@/theme/typography';

type ButtonVariant = 'primary' | 'secondary';

type ButtonProps = {
  title: string;
  onPress?: (event: GestureResponderEvent) => void;
  disabled?: boolean;
  loading?: boolean;
  variant?: ButtonVariant;
  style?: StyleProp<ViewStyle>;
};

export const Button = ({ title, onPress, disabled, loading, variant = 'primary', style }: ButtonProps) => {
  const isSecondary = variant === 'secondary';
  const backgroundColor = isSecondary ? 'transparent' : colors.primary;
  const textColor = isSecondary ? colors.textSecondary : colors.textPrimary;
  const borderColor = isSecondary ? colors.textSecondary : 'transparent';

  return (
    <TouchableOpacity
      activeOpacity={0.85}
      onPress={onPress}
      disabled={disabled || loading}
      style={[styles.base, { backgroundColor, borderColor, opacity: disabled ? 0.6 : 1 }, style]}
    >
      {loading ? (
        <ActivityIndicator color={textColor} />
      ) : (
        <Text style={[typography.button, styles.text, { color: textColor }]}>{title}</Text>
      )}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  base: {
    paddingVertical: spacing.md,
    borderRadius: 16,
    alignItems: 'center',
    borderWidth: 1,
    shadowColor: '#000',
    shadowOpacity: 0.25,
    shadowRadius: 10,
    shadowOffset: { width: 0, height: 8 },
    elevation: 8
  },
  text: {
    letterSpacing: 0.2
  }
});


