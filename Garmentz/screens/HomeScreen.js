import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, SafeAreaView, StatusBar } from 'react-native';

export default function HomeScreen({ navigation }) {
  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#000" />
      
      <View style={styles.content}>
        <Text style={styles.title}>GARMENTZ</Text>
        <Text style={styles.subtitle}>AI-Powered Garment Analysis</Text>
        
        <TouchableOpacity 
          style={styles.primaryButton} 
          onPress={() => navigation.navigate('Scan')}
        >
          <Text style={styles.primaryButtonText}>SCAN GARMENT</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { 
    flex: 1, 
    backgroundColor: '#000' 
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  title: { 
    fontFamily: 'Staatliches-Regular', 
    fontSize: 48, 
    color: '#fff', 
    textAlign: 'center', 
    marginBottom: 10,
    letterSpacing: 2,
  },
  subtitle: {
    fontFamily: 'Staatliches-Regular',
    fontSize: 16,
    color: '#ccc',
    textAlign: 'center',
    marginBottom: 60,
    letterSpacing: 1,
  },
  primaryButton: {
    backgroundColor: '#fff',
    paddingVertical: 15,
    paddingHorizontal: 40,
    borderRadius: 0,
    width: '80%',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#fff',
  },
  primaryButtonText: {
    fontFamily: 'Staatliches-Regular',
    fontSize: 18,
    color: '#000',
    letterSpacing: 1,
  },
});
