import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import * as ImageManipulator from 'expo-image-manipulator';

const ProcessingSection = ({ photo }) => {
  const [mood, setMood] = useState('neutral');

  useEffect(() => {
    if (photo) {
      console.log('ProcessingSection: Processing photo:', photo.uri);
      processImage(photo);
    }
  }, [photo]);

  const processImage = async (photoData) => {
    try {
      // Resize image for processing
      console.log('ProcessingSection: Resizing image');
      const manipulatedImage = await ImageManipulator.manipulateAsync(
        photoData.uri,
        [{ resize: { width: 224, height: 224 } }],
        { compress: 0.7, format: ImageManipulator.SaveFormat.JPEG }
      );

      // Simulate mood detection
      const detectedMood = detectMood(manipulatedImage.uri);
      console.log('ProcessingSection: Detected mood:', detectedMood);
      setMood(detectedMood);
    } catch (error) {
      console.error('ProcessingSection: Image processing error:', error);
    }
  };

  const detectMood = (imageUri) => {
    // Placeholder for mood detection (replace with ML model)
    console.log('ProcessingSection: Simulating mood detection for:', imageUri);
    const randomMood = Math.random();
    if (randomMood < 0.33) return 'happy';
    if (randomMood < 0.66) return 'sad';
    return 'neutral';
  };

  return (
    <View style={styles.container}>
      <Text style={styles.text}>Mood: {mood}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    marginVertical: 20,
  },
  text: {
    fontSize: 16,
    color: '#2e7d32',
    marginVertical: 5,
  },
});

export default ProcessingSection;