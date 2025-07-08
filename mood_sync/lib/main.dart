import 'package:flutter/material.dart';
import 'package:mood_sync/firebase_config.dart';
import 'package:mood_sync/screens/home_screen.dart';
import 'package:mood_sync/screens/login_screen.dart';
import 'package:mood_sync/screens/signup_screen.dart';
import 'package:mood_sync/screens/camera_screen.dart';
import 'package:mood_sync/screens/voice_record_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await FirebaseConfig.initialize();
  runApp(const MoodSyncApp());
}

class MoodSyncApp extends StatelessWidget {
  const MoodSyncApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Mood Sync',
      theme: ThemeData(
        primarySwatch: Colors.green,
        useMaterial3: true,
      ),
      initialRoute: '/home',
      routes: {
        '/home': (context) => const HomeScreen(),
        '/login': (context) => const LoginScreen(),
        '/signup': (context) => const SignupScreen(),
        '/camera': (context) => const CameraScreen(),
        '/voice': (context) => const VoiceRecordScreen(),
      },
    );
  }
}