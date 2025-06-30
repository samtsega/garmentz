import React, { useEffect } from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function SplashScreen({ navigation }) {
  useEffect(() => {
    const timer = setTimeout(() => {
      if (navigation && typeof navigation.replace === 'function') {
        navigation.replace('Main'); // Navigate to the BottomTabs navigator
      }
    }, 2000);

    return () => clearTimeout(timer); // Clean up on unmount
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.logo}>Garmentz</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#000', justifyContent: 'center', alignItems: 'center' },
  logo: { fontFamily: 'Staatliches', fontSize: 48, color: '#fff' }
});
