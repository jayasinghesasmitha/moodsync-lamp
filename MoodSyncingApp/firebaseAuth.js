import firebase from './firebaseConfig';

export const signupWithEmail = async (email, password) => {
  try {
    const userCredential = await firebase.auth().createUserWithEmailAndPassword(email, password);
    const uid = userCredential.user.uid;

    // Store user in Realtime Database
    await firebase.database().ref('users/' + uid).set({
      email: email,
      createdAt: new Date().toISOString()
    });

    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
};

// 🔑 Login function
export const loginWithEmail = async (email, password) => {
  try {
    const userCredential = await firebase.auth().signInWithEmailAndPassword(email, password);
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
};
