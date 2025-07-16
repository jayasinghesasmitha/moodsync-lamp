import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import axios from 'axios';

const BuildConnection = ({ moodData }) => {
  const [ipAddress, setIpAddress] = useState('192.168.1.100');
  const [isConnected, setIsConnected] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState('Disconnected');
  const [lastCommand, setLastCommand] = useState('');

  useEffect(() => {
    if (moodData) {
      sendMoodCommand(moodData.mood);
    }
  }, [moodData]);

  const testConnection = async () => {
    try {
      setConnectionStatus('Connecting...');
      const response = await axios.get(`http://${ipAddress}/test`, { timeout: 3000 });
      setIsConnected(response.data === 'OK');
      setConnectionStatus(response.data === 'OK' ? 'Connected' : 'Failed');
    } catch (error) {
      setIsConnected(false);
      setConnectionStatus('Connection Failed');
      console.error('Connection test failed:', error);
    }
  };

  const sendMoodCommand = async (mood) => {
    if (!isConnected) return;

    let intensity;
    switch (mood) {
      case 'happy':
        intensity = 1.0;
        break;
      case 'neutral':
        intensity = 0.5;
        break;
      case 'sad':
        intensity = 0.25;
        break;
      default:
        intensity = 0.5;
    }

    try {
      const command = `led=${intensity}`;
      const response = await axios.get(`http://${ipAddress}/command?${command}`);
      setLastCommand(`Sent: ${mood} (${intensity}) - Response: ${response.data}`);
      console.log('Command sent successfully:', response.data);
    } catch (error) {
      setLastCommand(`Failed to send command for ${mood}`);
      console.error('Command send failed:', error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>ESP32 WiFi Connection</Text>
      
      <TextInput
        style={styles.input}
        value={ipAddress}
        onChangeText={setIpAddress}
        placeholder="Enter ESP32 IP Address"
        keyboardType="numeric"
      />

      <TouchableOpacity style={styles.button} onPress={testConnection}>
        <LinearGradient colors={['#4dd0e1', '#4dd0e1']} style={styles.buttonGradient}>
          <Text style={styles.buttonText}>Test Connection</Text>
        </LinearGradient>
      </TouchableOpacity>

      <Text style={styles.statusText}>Status: {connectionStatus}</Text>
      
      {isConnected && moodData && (
        <View style={styles.commandSection}>
          <Text style={styles.moodText}>Current Mood: {moodData.mood}</Text>
          <Text style={styles.commandText}>{lastCommand}</Text>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 20,
    backgroundColor: '#f5f5f5',
    borderRadius: 10,
    margin: 10,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
    textAlign: 'center',
    color: '#333',
  },
  input: {
    height: 40,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
    paddingHorizontal: 10,
    marginBottom: 15,
    backgroundColor: '#fff',
  },
  button: {
    width: '100%',
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
  statusText: {
    fontSize: 16,
    textAlign: 'center',
    marginVertical: 10,
    color: '#555',
  },
  commandSection: {
    marginTop: 15,
    padding: 10,
    backgroundColor: '#e0f7fa',
    borderRadius: 5,
  },
  moodText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2e7d32',
    marginBottom: 5,
  },
  commandText: {
    fontSize: 14,
    color: '#333',
  },
});

export default BuildConnection;