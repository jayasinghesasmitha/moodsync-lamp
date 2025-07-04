import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, TouchableOpacity } from 'react-native';
import { Camera } from 'expo-camera';
import { LinearGradient } from 'expo-linear-gradient';

export default function CameraScreen() {
  const [hasPermission, setHasPermission] = useState(null);
  const [cameraRef, setCameraRef] = useState(null);
  const [type, setType] = useState(Camera.Constants.Type.back);

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
      <Camera 
        style={styles.camera} 
        type={type}
        ref={ref => setCameraRef(ref)}
      >
        <View style={styles.patternOverlay}>
          {[...Array(8)].map((_, index) => (
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
        <View style={styles.buttonContainer}>
          <TouchableOpacity
            style={styles.flipButton}
            onPress={() => {
              setType(
                type === Camera.Constants.Type.back
                  ? Camera.Constants.Type.front
                  : Camera.Constants.Type.back
              );
            }}
          >
            <LinearGradient
              colors={['#4caf50', '#81c784']}
              style={styles.flipButtonGradient}
            >
              <Text style={styles.text}>Flip</Text>
            </LinearGradient>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.captureButton}
            onPress={takePicture}
          >
            <LinearGradient
              colors={['#4caf50', '#81c784']}
              style={styles.captureButtonGradient}
            />
          </TouchableOpacity>
        </View>
      </Camera>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
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
  camera: {
    flex: 1,
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
    width: 15,
    height: 8,
    backgroundColor: '#4caf50',
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 2,
  },
  buttonContainer: {
    flex: 1,
    backgroundColor: 'transparent',
    flexDirection: 'row',
    margin: 30,
    justifyContent: 'center',
    alignItems: 'flex-end',
  },
  flipButton: {
    borderRadius: 10,
    overflow: 'hidden',
    marginRight: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
  },
  flipButtonGradient: {
    padding: 12,
    borderRadius: 10,
    alignItems: 'center',
    minWidth: 80,
  },
  captureButton: {
    width: 80,
    height: 80,
    borderRadius: 40,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
  },
  captureButtonGradient: {
    flex: 1,
    borderRadius: 40,
    borderWidth: 4,
    borderColor: '#fff',
  },
  text: {
    fontSize: 18,
    color: '#fff',
    fontWeight: '600',
  },
});