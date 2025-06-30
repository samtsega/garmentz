import React from 'react';
import { createStackNavigator, TransitionPresets } from '@react-navigation/stack';
import { LinearGradient } from 'expo-linear-gradient';

// Screens
import SplashScreenComponent from '../screens/SplashScreen';
import HomeScreen from '../screens/HomeScreen';
import CameraScreen from '../screens/CameraScreen';
import DetailsScreen from '../screens/DetailsScreen';
import ResultsScreen from '../screens/ResultsScreen';
import HistoryScreen from '../screens/HistoryScreen';
import SettingsScreen from '../screens/SettingsScreen';
import EbayScreen from '../screens/EbayScreen';

import BottomTabs from './TabNavigator'; // We will create this next

const Stack = createStackNavigator();

export default function StackNavigator() {
  return (
    <Stack.Navigator
      initialRouteName="Splash"
      screenOptions={{
        headerBackground: () => (
          <LinearGradient colors={['#1a1a1a', '#000000']} style={{ flex: 1 }} />
        ),
        headerTintColor: '#fff',
        headerTitleStyle: {
          fontFamily: 'Staatliches',
          fontSize: 26,
          letterSpacing: 1,
        },
        headerTitleAlign: 'center',
        ...TransitionPresets.SlideFromRightIOS,
      }}
    >
      <Stack.Screen name="Splash" component={SplashScreenComponent} options={{ headerShown: false }} />
      <Stack.Screen name="Main" component={BottomTabs} options={{ headerShown: false }} />
      <Stack.Screen name="Camera" component={CameraScreen} options={{ title: 'Scan Garment' }} />
      <Stack.Screen name="Details" component={DetailsScreen} options={{ title: 'Details' }} />
      <Stack.Screen name="Results" component={ResultsScreen} options={{ title: 'Results' }} />
      <Stack.Screen name="eBay Listings" component={EbayScreen} />
    </Stack.Navigator>
  );
}
