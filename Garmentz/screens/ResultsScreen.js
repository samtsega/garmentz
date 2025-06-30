import React from 'react';
import { View, Text, StyleSheet, Image } from 'react-native';

export default function ResultsScreen({ route }) {
  const { brand, fabric, age, image } = route.params;

  // Placeholder for now
  const depreciation = 0.68;

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Depreciation Score</Text>
      <Text style={styles.score}>{(depreciation * 100).toFixed(1)}%</Text>
      {image && <Image source={{ uri: image }} style={styles.image} />}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#000', justifyContent: 'center', alignItems: 'center' },
  title: { fontFamily: 'Staatliches', fontSize: 28, color: '#fff' },
  score: { fontFamily: 'Staatliches', fontSize: 64, color: '#fff', marginVertical: 20 },
  image: { width: 250, height: 250, marginTop: 10, borderRadius: 8 }
});
