import { useEffect, useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { StatusBar } from 'expo-status-bar';
import * as SplashScreen from 'expo-splash-screen';
import { AppNavigator } from '@/navigation/AppNavigator';

SplashScreen.preventAutoHideAsync().catch(() => {
  /* no-op */
});

export default function App() {
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    const init = async () => {
      try {
        // preload assets (fonts, icons) here when available
      } catch (error) {
        console.warn('Font load error', error);
      } finally {
        setIsReady(true);
        SplashScreen.hideAsync().catch(() => {
          /* no-op */
        });
      }
    };

    init();
  }, []);

  if (!isReady) {
    return null;
  }

  return (
    <NavigationContainer>
      <StatusBar style="light" />
      <AppNavigator />
    </NavigationContainer>
  );
}

