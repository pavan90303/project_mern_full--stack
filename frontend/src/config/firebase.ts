/**
 * Firebase Client Configuration & Authentication Service
 * Edu Track - Student Academic Management System
 *
 * Configured for Firebase Authentication (Google Sign-In for Administrator portal).
 */

import { initializeApp, getApps, getApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut } from 'firebase/auth';

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || "AIzaSyA8rKIsbAhfHDfn0BVjTevheu6cShHi_a0",
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || "vbus-eeded.firebaseapp.com",
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || "vbus-eeded",
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || "vbus-eeded.firebasestorage.app",
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || "1027440700569",
  appId: import.meta.env.VITE_FIREBASE_APP_ID || "1:1027440700569:web:4c9d0329c8fac591641c08",
  measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID || "G-DS2FGS8F2T"
};

// Initialize Firebase App
export const firebaseApp = getApps().length === 0 ? initializeApp(firebaseConfig) : getApp();

// Initialize Firebase Auth
export const auth = getAuth(firebaseApp);

// Configure Google Auth Provider
export const googleProvider = new GoogleAuthProvider();
googleProvider.setCustomParameters({
  prompt: 'select_account'
});

/**
 * Trigger Firebase Google Sign-In popup for Administrator authentication
 * Returns the verified Firebase ID Token string
 */
export async function signInAdminWithGoogle(): Promise<{ idToken: string; email: string | null; name: string | null }> {
  try {
    const result = await signInWithPopup(auth, googleProvider);
    const user = result.user;
    const idToken = await user.getIdToken();
    return {
      idToken,
      email: user.email,
      name: user.displayName
    };
  } catch (error: any) {
    if (error.code === 'auth/popup-closed-by-user') {
      throw new Error('Google sign-in popup was closed before completing authentication. Please try again.');
    }
    if (error.code === 'auth/cancelled-popup-request') {
      throw new Error('Another Google authentication popup was already in progress.');
    }
    if (error.code === 'auth/network-request-failed') {
      throw new Error('Network error connecting to Google Authentication. Please check your internet connection.');
    }
    if (error.code === 'auth/unauthorized-domain') {
      throw new Error(
        `This domain (${window.location.hostname}) is not authorized in Firebase. Please add "${window.location.hostname}" to Firebase Console -> Authentication -> Settings -> Authorized domains.`
      );
    }
    throw new Error(error.message || 'Failed to authenticate with Google.');
  }
}

/**
 * Sign out from Firebase Authentication
 */
export async function firebaseSignOut(): Promise<void> {
  try {
    await signOut(auth);
  } catch (error) {
    console.warn('[Firebase Auth] Sign out warning:', error);
  }
}
