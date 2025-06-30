import React from 'react';
import { View, Image, StyleSheet } from 'react-native';

export default function DetailsScreen({ route }) {
  const { image } = route.params || {};

  if (!image) {
    return (
      <View style={styles.center}>
        <Text style={{ color: '#fff' }}>No image to display</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Image source={{ uri: image }} style={styles.image} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#000', justifyContent: 'center', alignItems: 'center' },
  image: { width: '100%', height: '100%', resizeMode: 'contain' },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#000' },
});
