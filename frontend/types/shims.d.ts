declare module 'react' {
  export const useState: any;
  export const useEffect: any;
  export const useRef: any;
  export type FC<P = any> = (props: P) => any;
  const React: any;
  export default React;
}

declare module 'react-native' {
  export const View: any;
  export const Text: any;
  export const StyleSheet: any;
  export const TouchableOpacity: any;
  export const SafeAreaView: any;
  export const ActivityIndicator: any;
  export type TextStyle = any;
}

declare module 'expo-camera' {
  export const Camera: any;
  export type CameraType = any;
}

declare module '@react-navigation/native' {
  export const NavigationContainer: any;
  export function useNavigation(): any;
}

declare module '@react-navigation/native-stack' {
  export function createNativeStackNavigator<T>(): any;
  export type NativeStackScreenProps<T, K extends keyof T> = any;
}
