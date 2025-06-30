import React from 'react';
import { View, Text, StyleSheet, SafeAreaView, StatusBar } from 'react-native';

export default function SettingsScreen() {
  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#000" />
      <View style={styles.center}>
        <Text style={styles.title}>SETTINGS</Text>
        <Text style={styles.subtitle}>Customize your app preferences.</Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#000' },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
  title: {
    fontFamily: 'Staatliches-Regular',
    fontSize: 32,
    color: '#fff',
    letterSpacing: 2,
    marginBottom: 10,
  },
  subtitle: {
    fontFamily: 'Staatliches-Regular',
    fontSize: 14,
    color: '#ccc',
    textAlign: 'center',
    letterSpacing: 1,
  },
});
