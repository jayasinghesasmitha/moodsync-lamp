import firebase from 'firebase/app';
import 'firebase/database';

const firebaseConfig = {
  apiKey: "AIzaSyD0dnMPqcdsZ2Eh9rGQ_2VKNDU_t2PWoj4",
  authDomain: "mood-sync-lamp.firebaseapp.com",
  projectId: "mood-sync-lamp",
  storageBucket: "mood-sync-lamp.firebasestorage.app",
  messagingSenderId: "866448388045",
  appId: "1:866448388045:web:6019405cff140fa3e61e84",
  measurementId: "G-Z0EM6LFS7Q"
};

if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig);
}

export default firebase;