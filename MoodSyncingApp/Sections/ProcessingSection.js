import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import * as ImageManipulator from 'expo-image-manipulator';

const ProcessingSection = ({ photo, isFrozen, onMoodDetected }) => {
  const [mood, setMood] = useState('neutral');
  const [lastPhoto, setLastPhoto] = useState(null); // Store last processed photo

  useEffect(() => {
    if (photo && !isFrozen) {
      console.log('ProcessingSection: Processing photo:', photo.uri);
      setLastPhoto(photo);
      processImage(photo);
    } else if (isFrozen) {
      console.log('ProcessingSection: Camera frozen, retaining mood:', mood);
    }
  }, [photo, isFrozen]);

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

        // Map mood to intensity (0-255)
        const intensity = mapMoodToIntensity(detectedMood);
        console.log('ProcessingSection: Intensity:', intensity);

        // Pass mood and intensity to parent component
        if (onMoodDetected) {
          onMoodDetected({ mood: detectedMood, intensity });
          console.log('ProcessingSection: Mood data sent to callback:', { mood: detectedMood, intensity });
        }
    } catch (error) {
      console.error('ProcessingSection: Image processing error:', error);
    }
  };

  const detectMood = (imageUri) => {
    console.log('ProcessingSection: Simulating mood detection for:', imageUri);
    const randomMood = Math.random();
    if (randomMood < 0.33) return 'happy';
    if (randomMood < 0.66) return 'sad';
    return 'neutral';
  };

  const mapMoodToIntensity = (mood) => {
    switch (mood) {
      case 'happy':
        return 255; // Full brightness
      case 'sad':
        return 50; // Dim
      case 'neutral':
        return 128; // Medium
      default:
        return 128;
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.text}>Mood: {mood}</Text>
      {isFrozen && <Text style={styles.text}>Camera Frozen</Text>}
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