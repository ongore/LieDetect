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
    fontSize: 28,
    fontWeight: '700'
  },
  titleMedium: {
    fontSize: 20,
    fontWeight: '600'
  },
  body: {
    fontSize: 16,
    fontWeight: '400'
  },
  button: {
    fontSize: 16,
    fontWeight: '600'
  },
  caption: {
    fontSize: 12,
    fontWeight: '400'
  }
};

