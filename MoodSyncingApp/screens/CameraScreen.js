import React, { useState, useEffect, useRef } from 'react';
import { StyleSheet, Text, View, TouchableOpacity } from 'react-native';
import { Camera } from 'expo-camera';
import { LinearGradient } from 'expo-linear-gradient';
import ProcessingSection from '../Sections/ProcessingSection';

export default function CameraScreen({ navigation }) {
  const [hasPermission, setHasPermission] = useState(null);
  const [cameraRef, setCameraRef] = useState(null);
  const [photo, setPhoto] = useState(null); // Store captured photo
  const [isCapturing, setIsCapturing] = useState(false); // Control capture interval
  const [isFrozen, setIsFrozen] = useState(false); // Control freeze/unfreeze
  const intervalRef = useRef(null); // Store interval reference

  useEffect(() => {
    // Request camera permissions
    (async () => {
      console.log('CameraScreen: Requesting camera permissions');
      const { status } = await Camera.requestCameraPermissionsAsync();
      console.log('CameraScreen: Permission status:', status);
      setHasPermission(status === 'granted');
    })();

    // Start/stop capturing images every 5 seconds
    if (hasPermission && cameraRef && isCapturing && !isFrozen) {
      console.log('CameraScreen: Starting auto-capture interval');
      intervalRef.current = setInterval(() => {
        takePicture();
      }, 5000);
    } else {
      console.log('CameraScreen: Stopping auto-capture interval');
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    }

    // Cleanup interval on unmount or state change
    return () => {
      console.log('CameraScreen: Clearing auto-capture interval');
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [hasPermission, cameraRef, isCapturing, isFrozen]);

  const takePicture = async () => {
    if (cameraRef) {
      console.log('CameraScreen: Taking picture');
      let photoData = await cameraRef.takePictureAsync();
      console.log('CameraScreen: Photo captured:', photoData.uri);
      setPhoto(photoData); // Pass photo to ProcessingSection
    } else {
      console.log('CameraScreen: Camera ref not available');
    }
  };

  if (hasPermission === null) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.errorText}>Loading camera...</Text>
      </View>
    );
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
          ref={ref => {
            console.log('CameraScreen: Camera ref set:', !!ref);
            setCameraRef(ref);
          }}
        />
      </View>

      <ProcessingSection photo={photo} isFrozen={isFrozen} />

      <TouchableOpacity style={styles.button} onPress={() => {
        console.log('CameraScreen: Toggling capture state');
        setIsCapturing(!isCapturing);
      }}>
        <LinearGradient colors={['#4dd0e1', '#4dd0e1']} style={styles.buttonGradient}>
          <Text style={styles.buttonText}>{isCapturing ? 'Stop' : 'Start'}</Text>
        </LinearGradient>
      </TouchableOpacity>

      <TouchableOpacity style={styles.button} onPress={() => {
        console.log('CameraScreen: Toggling freeze state');
        setIsFrozen(!isFrozen);
      }}>
        <LinearGradient colors={['#4dd0e1', '#4dd0e1']} style={styles.buttonGradient}>
          <Text style={styles.buttonText}>{isFrozen ? 'Unfreeze' : 'Freeze'}</Text>
        </LinearGradient>
      </TouchableOpacity>

      <TouchableOpacity style={styles.button} onPress={() => {
        console.log('CameraScreen: Navigating to VoiceRecord');
        navigation.navigate('VoiceRecord');
      }}>
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