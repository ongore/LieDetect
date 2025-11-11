import { TextStyle } from 'react-native';

type TypographyScale = {
  titleLarge: TextStyle;
  titleMedium: TextStyle;
  body: TextStyle;
  button: TextStyle;
  caption: TextStyle;
};

export const typography: TypographyScale = {
  titleLarge: {
    fontSize: 30,
    lineHeight: 36,
    letterSpacing: 0.2,
    fontWeight: '700',
    fontFamily: 'System'
  },
  titleMedium: {
    fontSize: 22,
    lineHeight: 28,
    letterSpacing: 0.2,
    fontWeight: '600',
    fontFamily: 'System'
  },
  body: {
    fontSize: 16,
    lineHeight: 22,
    fontWeight: '400',
    fontFamily: 'System'
  },
  button: {
    fontSize: 16,
    letterSpacing: 0.3,
    fontWeight: '600',
    fontFamily: 'System'
  },
  caption: {
    fontSize: 12,
    lineHeight: 16,
    fontWeight: '400',
    fontFamily: 'System'
  }
};

