import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { GetStartedScreen } from '@/screens/GetStartedScreen';
import { AuthStack } from '@/navigation/AuthStack';
import { CameraStack } from '@/navigation/CameraStack';

export type RootStackParamList = {
  GetStarted: undefined;
  Auth: undefined;
  Capture: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export const AppNavigator = () => {
  return (
    <Stack.Navigator
      initialRouteName="GetStarted"
      screenOptions={{
        headerShown: false,
        animation: 'fade'
      }}
    >
      <Stack.Screen name="GetStarted" component={GetStartedScreen} />
      <Stack.Screen name="Auth" component={AuthStack} />
      <Stack.Screen name="Capture" component={CameraStack} />
    </Stack.Navigator>
  );
};

