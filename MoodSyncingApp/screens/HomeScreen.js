import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

export default function HomeScreen({ navigation }) {
  return (
    <LinearGradient
      colors={['#e0f7fa', '#a5d6a7']}
      style={styles.container}
    >
      <View style={styles.patternOverlay}>
        {[...Array(10)].map((_, index) => (
          <View
            key={index}
            style={[styles.leaf, {
              top: `${Math.random() * 100}%`,
              left: `${Math.random() * 100}%`,
              transform: [{ rotate: `${Math.random() * 360}deg` }],
            }]}
          />
        ))}
      </View>
      <Text style={styles.title}>Mood Syncing</Text>
      <Text style={styles.subtitle}>A Mood Syncing Service</Text>
      
      <TouchableOpacity 
        style={styles.button}
        onPress={() => navigation.navigate('Login')}
        activeOpacity={0.7}
      >
        <LinearGradient
          colors={['#4caf50', '#81c784']}
          style={styles.buttonGradient}
        >
          <Text style={styles.buttonText}>Sync Your Moods</Text>
        </LinearGradient>
      </TouchableOpacity>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  patternOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    opacity: 0.1,
  },
  leaf: {
    position: 'absolute',
    width: 20,
    height: 10,
    backgroundColor: '#4caf50',
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 2,
  },
  title: {
    fontSize: 36,
    fontWeight: '600',
    marginBottom: 15,
    color: '#2e7d32',
    textShadowColor: 'rgba(0, 0, 0, 0.1)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 2,
  },
  subtitle: {
    fontSize: 20,
    marginBottom: 40,
    color: '#4a6360',
    fontStyle: 'italic',
  },
  button: {
    borderRadius: 30,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
  },
  buttonGradient: {
    paddingHorizontal: 40,
    paddingVertical: 15,
    borderRadius: 30,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 20,
    fontWeight: '700',
  },
});