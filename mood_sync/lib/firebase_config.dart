import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_database/firebase_database.dart';

class FirebaseConfig {
  static Future<void> initialize() async {
    await Firebase.initializeApp();
  }

  static Future<Map<String, dynamic>> signupWithEmail(String email, String password) async {
    try {
      UserCredential userCredential = await FirebaseAuth.instance.createUserWithEmailAndPassword(
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

  static Future<Map<String, dynamic>> loginWithEmail(String email, String password) async {
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
}