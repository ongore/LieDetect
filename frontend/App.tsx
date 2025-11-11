import { useEffect, useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { StatusBar } from 'expo-status-bar';
import * as SplashScreen from 'expo-splash-screen';
import { AppNavigator } from '@/navigation/AppNavigator';
import { env } from '@/config/env';

SplashScreen.preventAutoHideAsync().catch(() => {
  /* no-op */
});

export default function App() {
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    // Log the resolved API base to help diagnose connectivity issues
    console.log('LieDetect API Base URL:', env.apiBaseUrl);
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

