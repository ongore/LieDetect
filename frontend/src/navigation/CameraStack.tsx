import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { CameraScreen } from '@/screens/CameraScreen';
import { ReviewScreen } from '@/screens/ReviewScreen';
import { ResultsScreen } from '@/screens/ResultsScreen';
import { LieDetectResponse, ParticipantRole } from '@/types/lieDetection';

export type CameraStackParamList = {
  Camera: undefined;
  Review: { videoUri: string; role: ParticipantRole };
  Results: LieDetectResponse;
};

const Stack = createNativeStackNavigator<CameraStackParamList>();

export const CameraStack = () => (
  <Stack.Navigator
    initialRouteName="Camera"
    screenOptions={{
      headerShown: false,
      animation: 'slide_from_right'
    }}
  >
    <Stack.Screen name="Camera" component={CameraScreen} />
    <Stack.Screen name="Review" component={ReviewScreen} />
    <Stack.Screen name="Results" component={ResultsScreen} />
  </Stack.Navigator>
);

