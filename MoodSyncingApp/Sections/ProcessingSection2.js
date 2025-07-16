import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, BackHandler } from 'react-native';
import * as ImageManipulator from 'expo-image-manipulator';
import * as Brightness from 'expo-brightness';

const ProcessingSection = ({ photo, isFrozen, onMoodDetected }) => {
  const [mood, setMood] = useState('neutral');
  const [lastPhoto, setLastPhoto] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [screenIntensity, setScreenIntensity] = useState(0.5); // Default screen brightness

  // Expanded mood dataset with intensity ranges
  const moodOptions = [
    { name: 'happy', emoji: '😊', description: 'Happy', intensityRange: [0.7, 1.0], color: '#FFD700' },
    { name: 'excited', emoji: '🤩', description: 'Excited', intensityRange: [0.8, 1.0], color: '#FF8C00' },
    { name: 'surprised', emoji: '😲', description: 'Surprised', intensityRange: [0.6, 0.9], color: '#FF6347' },
    { name: 'neutral', emoji: '😐', description: 'Neutral', intensityRange: [0.4, 0.6], color: '#A9A9A9' },
    { name: 'confused', emoji: '😕', description: 'Confused', intensityRange: [0.3, 0.5], color: '#9370DB' },
    { name: 'sleepy', emoji: '😴', description: 'Sleepy', intensityRange: [0.2, 0.4], color: '#4169E1' },
    { name: 'sad', emoji: '😢', description: 'Sad', intensityRange: [0.1, 0.3], color: '#1E90FF' },
    { name: 'fearful', emoji: '😨', description: 'Fearful', intensityRange: [0.1, 0.3], color: '#9932CC' },
    { name: 'disgusted', emoji: '🤢', description: 'Disgusted', intensityRange: [0.1, 0.2], color: '#32CD32' },
    { name: 'angry', emoji: '😠', description: 'Angry', intensityRange: [0.0, 0.2], color: '#FF4500' }
  ];

  useEffect(() => {
    // Request permission and set up brightness control
    (async () => {
      const { status } = await Brightness.requestPermissionsAsync();
      if (status === 'granted') {
        await Brightness.setSystemBrightnessAsync(screenIntensity);
      }
    })();

    return () => {
      // Reset brightness when component unmounts
      Brightness.setSystemBrightnessAsync(0.5);
    };
  }, []);

  useEffect(() => {
    if (photo && !isFrozen && !processing) {
      console.log('ProcessingSection: Processing photo:', photo.uri);
      setProcessing(true);
      setLastPhoto(photo);
      processImage(photo)
        .finally(() => setProcessing(false));
    } else if (isFrozen) {
      console.log('ProcessingSection: Camera frozen, retaining mood:', mood);
    }
  }, [photo, isFrozen]);

  useEffect(() => {
    // Update screen brightness when mood changes
    updateScreenIntensity();
  }, [mood]);

  const processImage = async (photoData) => {
    try {
      // Resize image for processing
      const manipulatedImage = await ImageManipulator.manipulateAsync(
        photoData.uri,
        [{ resize: { width: 224, height: 224 } }],
        { compress: 0.7, format: ImageManipulator.SaveFormat.JPEG }
      );

      // Detect mood from the image
      const detectedMood = detectMood(manipulatedImage.uri);
      setMood(detectedMood);

      // Get mood data including intensity range
      const moodData = getMoodData(detectedMood);
      const intensity = calculateIntensity(moodData.intensityRange);

      // Pass mood data to parent component
      if (onMoodDetected) {
        onMoodDetected({ 
          mood: detectedMood, 
          intensity,
          moodData
        });
      }
    } catch (error) {
      console.error('ProcessingSection: Image processing error:', error);
    }
  };

  const updateScreenIntensity = async () => {
    const moodData = getMoodData(mood);
    const intensity = calculateIntensity(moodData.intensityRange);
    
    try {
      await Brightness.setSystemBrightnessAsync(intensity);
      setScreenIntensity(intensity);
      console.log(`Screen intensity set to: ${intensity} for mood: ${mood}`);
    } catch (error) {
      console.error('Failed to set screen brightness:', error);
    }
  };

  const calculateIntensity = (range) => {
    // Calculate random intensity within the mood's range
    const [min, max] = range;
    return min + Math.random() * (max - min);
  };

  const getMoodData = (moodName) => {
    return moodOptions.find(m => m.name === moodName) || moodOptions[moodOptions.length - 1];
  };

  const detectMood = (imageUri) => {
    // Simulate mood detection with weighted probabilities
    const randomValue = Math.random();
    
    if (randomValue < 0.15) return 'happy';
    if (randomValue < 0.25) return 'excited';
    if (randomValue < 0.35) return 'surprised';
    if (randomValue < 0.45) return 'neutral';
    if (randomValue < 0.53) return 'confused';
    if (randomValue < 0.61) return 'sleepy';
    if (randomValue < 0.69) return 'sad';
    if (randomValue < 0.77) return 'fearful';
    if (randomValue < 0.85) return 'disgusted';
    return 'angry';
  };

  const currentMoodData = getMoodData(mood);

  return (
    <View style={styles.container}>
      <View style={[
        styles.moodContainer, 
        { 
          backgroundColor: currentMoodData.color,
          opacity: screenIntensity + 0.3 // Make container more visible even at low brightness
        }
      ]}>
        <Text style={styles.emoji}>{currentMoodData.emoji}</Text>
        <Text style={styles.moodText}>{currentMoodData.description}</Text>
        <Text style={styles.intensityText}>Intensity: {screenIntensity.toFixed(2)}</Text>
      </View>
      {isFrozen && <Text style={styles.statusText}>Analysis Frozen</Text>}
      {processing && <Text style={styles.statusText}>Processing...</Text>}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    marginVertical: 20,
  },
  moodContainer: {
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
    borderRadius: 25,
    minWidth: 180,
    marginVertical: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    elevation: 5,
  },
  emoji: {
    fontSize: 36,
    marginBottom: 8,
  },
  moodText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#000',
    marginBottom: 5,
  },
  intensityText: {
    fontSize: 14,
    color: '#333',
  },
  statusText: {
    fontSize: 14,
    color: '#555',
    marginTop: 5,
    fontStyle: 'italic',
  },
});

export default ProcessingSection;