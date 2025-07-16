import { useState, useEffect } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Audio } from 'expo-av';

const ProcessingSectionForVoice = ({ audioUri, isProcessing, onProcessingComplete }) => {
  const [mood, setMood] = useState('neutral');
  const [processingStatus, setProcessingStatus] = useState('Processing voice...');

  useEffect(() => {
    if (audioUri && isProcessing) {
      console.log('Processing voice recording:', audioUri);
      processAudio(audioUri);
    }
  }, [audioUri, isProcessing]);

  const processAudio = async (uri) => {
    try {
      setProcessingStatus('Analyzing voice features...');
      
      // First, get some basic info about the recording
      const soundObject = new Audio.Sound();
      await soundObject.loadAsync({ uri });
      const status = await soundObject.getStatusAsync();
      
      // Simulate processing time based on recording duration
      const processingTime = Math.min(Math.max(status.durationMillis / 1000, 2), 5);
      
      setTimeout(() => {
        // Simulate mood detection based on random selection
        const moods = ['happy', 'sad', 'neutral'];
        const randomMood = moods[Math.floor(Math.random() * moods.length)];
        
        setMood(randomMood);
        setProcessingStatus('Analysis complete');
        onProcessingComplete && onProcessingComplete();
        
        console.log(`Detected mood: ${randomMood}`);
      }, processingTime * 1000);
      
    } catch (error) {
      console.error('Audio processing error:', error);
      setProcessingStatus('Processing failed');
      onProcessingComplete && onProcessingComplete();
    }
  };

  const getMoodColor = () => {
    switch (mood) {
      case 'happy':
        return '#4CAF50'; // Green
      case 'sad':
        return '#2196F3'; // Blue
      case 'neutral':
        return '#9E9E9E'; // Gray
      default:
        return '#FFFFFF'; // White
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.statusText}>{processingStatus}</Text>
      {!isProcessing && mood && (
        <View style={[styles.moodContainer, { backgroundColor: getMoodColor() }]}>
          <Text style={styles.moodText}>Detected Mood: {mood}</Text>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    padding: 10,
  },
  statusText: {
    color: '#FFFFFF',
    fontSize: 16,
    marginBottom: 10,
  },
  moodContainer: {
    padding: 15,
    borderRadius: 8,
    marginTop: 10,
  },
  moodText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: 'bold',
  },
});

export default ProcessingSectionForVoice;