import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_database/firebase_database.dart';

class FirebaseConfig {
  static Future<void> initialize() async {
    await Firebase.initializeApp(
      options: const FirebaseOptions(
        apiKey: "AIzaSyC0IJ_QO2fvfQBWfDHJx22K_jydLYSG5l0",
        appId: "1:866448388045:android:650f17d33b6ec7d4e61e84",
        messagingSenderId: "866448388045",
        projectId: "mood-sync-lamp",
        databaseURL: "https://mood-sync-lamp-default-rtdb.asia-southeast1.firebasedatabase.app",
        storageBucket: "mood-sync-lamp.firebasestorage.app",
      ),
    );
  }

  static Future<Map<String, dynamic>> signupWithEmail(
      String email, String password) async {
    try {
      UserCredential userCredential =
          await FirebaseAuth.instance.createUserWithEmailAndPassword(
        email: email,
        password: password,
      );
      String uid = userCredential.user!.uid;
      await FirebaseDatabase.instance.ref('users/$uid').set({
        'email': email,
        'createdAt': DateTime.now().toIso8601String(),
      });
      return {'success': true};
    } catch (error) {
      return {'success': false, 'error': error.toString()};
    }
  }

  static Future<Map<String, dynamic>> loginWithEmail(
      String email, String password) async {
    try {
      await FirebaseAuth.instance.signInWithEmailAndPassword(
        email: email,
        password: password,
      );
      return {'success': true};
    } catch (error) {
      return {'success': false, 'error': error.toString()};
    }
  }

  static Future<void> signOut() async {
    await FirebaseAuth.instance.signOut();
  }
}