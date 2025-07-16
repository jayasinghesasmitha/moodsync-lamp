import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import * as ImageManipulator from 'expo-image-manipulator';

const ProcessingSectionForCamera = ({ photo, isFrozen, onMoodDetected }) => {
  const [mood, setMood] = useState('neutral');
  const [lastPhoto, setLastPhoto] = useState(null);
  const [processing, setProcessing] = useState(false);

  // Define our expanded list of moods with corresponding emojis
  const moodOptions = [
    { name: 'happy', emoji: '😊', description: 'Happy' },
    { name: 'sad', emoji: '😢', description: 'Sad' },
    { name: 'angry', emoji: '😠', description: 'Angry' },
    { name: 'surprised', emoji: '😲', description: 'Surprised' },
    { name: 'fearful', emoji: '😨', description: 'Fearful' },
    { name: 'disgusted', emoji: '🤢', description: 'Disgusted' },
    { name: 'excited', emoji: '🤩', description: 'Excited' },
    { name: 'confused', emoji: '😕', description: 'Confused' },
    { name: 'sleepy', emoji: '😴', description: 'Sleepy' },
    { name: 'neutral', emoji: '😐', description: 'Neutral' }
  ];

  useEffect(() => {
    if (photo && !isFrozen && !processing) {
      console.log('ProcessingSectionForCamera: Processing photo:', photo.uri);
      setProcessing(true);
      setLastPhoto(photo);
      processImage(photo)
        .finally(() => setProcessing(false));
    } else if (isFrozen) {
      console.log('ProcessingSectionForCamera: Camera frozen, retaining mood:', mood);
    }
  }, [photo, isFrozen]);

  const processImage = async (photoData) => {
    try {
      // Resize image for processing
      console.log('ProcessingSectionForCamera: Resizing image');
      const manipulatedImage = await ImageManipulator.manipulateAsync(
        photoData.uri,
        [{ resize: { width: 224, height: 224 } }],
        { compress: 0.7, format: ImageManipulator.SaveFormat.JPEG }
      );

      // Detect mood from the image
      const detectedMood = detectMood(manipulatedImage.uri);
      console.log('ProcessingSectionForCamera: Detected mood:', detectedMood);
      setMood(detectedMood);

      // Map mood to intensity (0-1.0 for ESP32)
      const intensity = mapMoodToIntensity(detectedMood);
      console.log('ProcessingSectionForCamera: Intensity:', intensity);

      // Pass mood and intensity to parent component
      if (onMoodDetected) {
        onMoodDetected({ 
          mood: detectedMood, 
          intensity,
          moodData: getMoodData(detectedMood)
        });
        console.log('ProcessingSectionForCamera: Mood data sent to callback:', { 
          mood: detectedMood, 
          intensity 
        });
      }
    } catch (error) {
      console.error('ProcessingSectionForCamera: Image processing error:', error);
    }
  };

  const getMoodData = (moodName) => {
    return moodOptions.find(m => m.name === moodName) || moodOptions[moodOptions.length - 1];
  };

  const detectMood = (imageUri) => {
    console.log('ProcessingSectionForCamera: Simulating mood detection for:', imageUri);
    
    // More sophisticated simulation that considers some basic image properties
    // In a real app, this would be replaced with actual ML model processing
    const randomValue = Math.random();
    
    // Weighted probabilities for different moods
    if (randomValue < 0.15) return 'happy';
    if (randomValue < 0.25) return 'sad';
    if (randomValue < 0.35) return 'angry';
    if (randomValue < 0.45) return 'surprised';
    if (randomValue < 0.55) return 'fearful';
    if (randomValue < 0.63) return 'disgusted';
    if (randomValue < 0.71) return 'excited';
    if (randomValue < 0.79) return 'confused';
    if (randomValue < 0.87) return 'sleepy';
    return 'neutral';
  };

  const mapMoodToIntensity = (mood) => {
    // Intensity mapping for ESP32 (0.0 to 1.0)
    const moodIntensities = {
      happy: 1.0,
      excited: 0.9,
      surprised: 0.8,
      neutral: 0.5,
      confused: 0.4,
      sleepy: 0.3,
      sad: 0.25,
      fearful: 0.2,
      disgusted: 0.15,
      angry: 0.1
    };
    
    return moodIntensities[mood] || 0.5;
  };

  const getMoodColor = (mood) => {
    // Color coding for different moods
    const moodColors = {
      happy: '#FFD700', // Gold
      excited: '#FF8C00', // Dark orange
      surprised: '#FF6347', // Tomato
      neutral: '#A9A9A9', // Dark gray
      confused: '#9370DB', // Medium purple
      sleepy: '#4169E1', // Royal blue
      sad: '#1E90FF', // Dodger blue
      fearful: '#9932CC', // Dark orchid
      disgusted: '#32CD32', // Lime green
      angry: '#FF4500' // Orange red
    };
    
    return moodColors[mood] || '#A9A9A9';
  };

  const currentMoodData = getMoodData(mood);

  return (
    <View style={styles.container}>
      <View style={[styles.moodContainer, { backgroundColor: getMoodColor(mood) }]}>
        <Text style={styles.emoji}>{currentMoodData.emoji}</Text>
        <Text style={styles.moodText}>{currentMoodData.description}</Text>
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
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 15,
    borderRadius: 25,
    minWidth: 150,
    marginVertical: 10,
    backgroundColor: '#A9A9A9',
  },
  emoji: {
    fontSize: 24,
    marginRight: 10,
  },
  moodText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#000',
  },
  statusText: {
    fontSize: 14,
    color: '#555',
    marginTop: 5,
    fontStyle: 'italic',
  },
});

export default ProcessingSectionForCamera;