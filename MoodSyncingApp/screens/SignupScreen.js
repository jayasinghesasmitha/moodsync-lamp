import React, { useState } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

export default function SignupScreen({ navigation }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSignup = () => {
    navigation.navigate('Camera');
  };

  return (
    <LinearGradient
      colors={['#b2ebf2', '#c8e6c9']}
      style={styles.container}
    >
      <View style={styles.wavePattern}>
        {[...Array(8)].map((_, index) => (
          <View
            key={index}
            style={[styles.wave, {
              top: `${10 + index * 12}%`,
              opacity: 0.1,
            }]}
          />
        ))}
      </View>
      <Text style={styles.title}>Sign Up</Text>
      
      <TextInput
        style={styles.input}
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
        autoCapitalize="none"
        placeholderTextColor="#78909c"
      />
      
      <TextInput
        style={styles.input}
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
        placeholderTextColor="#78909c"
      />
      
      <TextInput
        style={styles.input}
        placeholder="Confirm Password"
        value={confirmPassword}
        onChangeText={setConfirmPassword}
        secureTextEntry
        placeholderTextColor="#78909c"
      />
      
      <TouchableOpacity style={styles.button} onPress={handleSignup}>
        <LinearGradient
          colors={['#4caf50', '#81c784']}
          style={styles.buttonGradient}
        >
          <Text style={styles.buttonText}>Sign Up</Text>
        </LinearGradient>
      </TouchableOpacity>
      
      <TouchableOpacity onPress={() => navigation.navigate('Login')}>
        <Text style={styles.link}>Already have an account? Login</Text>
      </TouchableOpacity>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
  },
  wavePattern: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
  },
  wave: {
    position: 'absolute',
    width: '100%',
    height: 20,
    backgroundColor: '#4caf50',
    borderRadius: 10,
    transform: [{ skewY: '-5deg' }],
  },
  title: {
    fontSize: 32,
    fontWeight: '600',
    marginBottom: 30,
    textAlign: 'center',
    color: '#2e7d32',
    textShadowColor: 'rgba(0, 0, 0, 0.1)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 2,
  },
  input: {
    height: 50,
    borderColor: '#a5d6a7',
    borderWidth: 2,
    marginBottom: 20,
    padding: 15,
    borderRadius: 12,
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 3,
  },
  button: {
    borderRadius: 12,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
  },
  buttonGradient: {
    padding: 15,
    borderRadius: 12,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '700',
  },
  link: {
    color: '#2e7d32',
    textAlign: 'center',
    marginTop: 15,
    fontSize: 16,
    textDecorationLine: 'underline',
  },
});