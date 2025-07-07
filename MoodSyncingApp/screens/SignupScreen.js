import React, { useState } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { signupWithEmail } from '../firebaseAuth';


export default function SignupScreen({ navigation }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const isValidEmail = (email) => {
    return /\S+@\S+\.\S+/.test(email);
  };

  const handleSignup = async () => {
    if (!isValidEmail(email)) {
      alert('Please enter a valid email address.');
      return;
    }
    if (password !== confirmPassword) {
      alert("Passwords do not match!");
      return;
    }

    const result = await signupWithEmail(email, password);
    if (result.success) {
      navigation.navigate('Login');
    } else {
      alert(result.error);
    }
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
  wavePattern: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    pointerEvents: 'none', // ⬅️ This allows touches to pass through
  },

  title: {
    fontSize: 32,
    fontWeight: '600',
    marginBottom: 30,
    textAlign: 'center',
    color: '#2e7d32',
  },
  input: {
    height: 50,
    borderColor: '#a5d6a7',
    borderWidth: 2,
    marginBottom: 20,
    padding: 15,
    borderRadius: 12,
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
  },
  button: {
    borderRadius: 12,
    overflow: 'hidden',
    marginTop: 10,
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
