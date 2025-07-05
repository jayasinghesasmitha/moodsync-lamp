import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, TouchableOpacity } from 'react-native';
import { Camera } from 'expo-camera';
import { LinearGradient } from 'expo-linear-gradient';

export default function CameraScreen({ navigation }) {
  const [hasPermission, setHasPermission] = useState(null);
  const [cameraRef, setCameraRef] = useState(null);

  useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === 'granted');
    })();
  }, []);

  const takePicture = async () => {
    if (cameraRef) {
      let photo = await cameraRef.takePictureAsync();
      console.log(photo);
    }
  };

  if (hasPermission === null) {
    return <View style={styles.loadingContainer} />;
  }

  if (hasPermission === false) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.errorText}>No access to camera</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.cameraContainer}>
        <Camera 
          style={styles.camera}
          ref={ref => setCameraRef(ref)}
        />
      </View>

      <TouchableOpacity style={styles.button} onPress={takePicture}>
        <LinearGradient colors={['#4dd0e1', '#4dd0e1']} style={styles.buttonGradient}>
          <Text style={styles.buttonText}>Start</Text>
        </LinearGradient>
      </TouchableOpacity>

      <TouchableOpacity style={styles.button}>
        <LinearGradient colors={['#4dd0e1', '#4dd0e1']} style={styles.buttonGradient}>
          <Text style={styles.buttonText}>Hold</Text>
        </LinearGradient>
      </TouchableOpacity>

      <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('VoiceRecord')}>
        <LinearGradient colors={['#4dd0e1', '#4dd0e1']} style={styles.buttonGradient}>
          <Text style={styles.buttonText}>Voice</Text>
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
  cameraContainer: {
    width: 300,
    height: 300,
    backgroundColor: '#000',
    borderRadius: 10,
    overflow: 'hidden',
    marginBottom: 30,
  },
  camera: {
    flex: 1,
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
