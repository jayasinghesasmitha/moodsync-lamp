import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, TouchableOpacity } from 'react-native';
import { Audio } from 'expo-av';
import { LinearGradient } from 'expo-linear-gradient';

export default function VoiceRecorderScreen() {
  const [hasPermission, setHasPermission] = useState(null);
  const [recording, setRecording] = useState(null);
  const [recordingStatus, setRecordingStatus] = useState('');

  useEffect(() => {
    (async () => {
      const { status } = await Audio.requestPermissionsAsync();
      setHasPermission(status === 'granted');
    })();
  }, []);

  const startRecording = async () => {
    try {
      const { granted } = await Audio.requestPermissionsAsync();
      if (!granted) return;

      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });

      const newRecording = new Audio.Recording();
      await newRecording.prepareToRecordAsync(
        Audio.RECORDING_OPTIONS_PRESET_HIGH_QUALITY
      );
      await newRecording.startAsync();

      setRecording(newRecording);
      setRecordingStatus('Recording...');
    } catch (err) {
      console.error('Failed to start recording', err);
    }
  };

  const stopRecording = async () => {
    try {
      if (!recording) return;

      await recording.stopAndUnloadAsync();
      const uri = recording.getURI();
      console.log('Recording saved to:', uri);

      setRecording(null);
      setRecordingStatus('Recording saved');
    } catch (err) {
      console.error('Failed to stop recording', err);
    }
  };

  if (hasPermission === null) {
    return <View style={styles.loadingContainer} />;
  }

  if (hasPermission === false) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.errorText}>No access to microphone</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.recorderContainer}>
        <Text style={styles.recordingText}>
          {recordingStatus || 'Press start to record'}
        </Text>
      </View>

      <TouchableOpacity style={styles.button} onPress={startRecording}>
        <LinearGradient colors={['#4dd0e1', '#4dd0e1']} style={styles.buttonGradient}>
          <Text style={styles.buttonText}>Start</Text>
        </LinearGradient>
      </TouchableOpacity>

      <TouchableOpacity style={styles.button} onPress={stopRecording}>
        <LinearGradient colors={['#4dd0e1', '#4dd0e1']} style={styles.buttonGradient}>
          <Text style={styles.buttonText}>Hold</Text>
        </LinearGradient>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f9fafa',
    alignItems: 'center',
    justifyContent: 'center',
    paddingTop: 20,
    paddingBottom: 40,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#e0f7fa',
  },
  errorText: {
    fontSize: 20,
    color: '#2e7d32',
    textAlign: 'center',
  },
  recorderContainer: {
    width: 300,
    height: 300,
    backgroundColor: '#000',
    borderRadius: 10,
    overflow: 'hidden',
    marginBottom: 30,
    justifyContent: 'center',
    alignItems: 'center',
  },
  recordingText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  button: {
    width: 250,
    marginVertical: 10,
    borderRadius: 8,
    overflow: 'hidden',
  },
  buttonGradient: {
    paddingVertical: 14,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
});
