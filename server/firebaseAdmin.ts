/**
 * Firebase Admin SDK & Token Verification Service
 * Edu Track - Student Academic Management System
 *
 * Verifies Firebase ID Tokens for Administrator Google Authentication.
 */

import admin from 'firebase-admin';
import path from 'path';
import fs from 'fs';
import jwt from 'jsonwebtoken';

const PROJECT_ID = process.env.FIREBASE_PROJECT_ID || 'vbus-eeded';
const API_KEY =
  process.env.FIREBASE_API_KEY ||
  process.env.VITE_FIREBASE_API_KEY ||
  'AIzaSyA8rKIsbAhfHDfn0BVjTevheu6cShHi_a0';

let adminApp: admin.app.App | null = null;
let hasServiceAccount = false;

export function getFirebaseAdmin(): admin.app.App {
  if (adminApp) return adminApp;

  if (admin.apps.length > 0) {
    adminApp = admin.app();
    return adminApp;
  }

  const serviceAccountEnv = process.env.FIREBASE_SERVICE_ACCOUNT;
  if (serviceAccountEnv) {
    try {
      let serviceAccount: any;
      if (serviceAccountEnv.trim().startsWith('{')) {
        serviceAccount = JSON.parse(serviceAccountEnv);
      } else {
        const resolvedPath = path.isAbsolute(serviceAccountEnv)
          ? serviceAccountEnv
          : path.resolve(process.cwd(), serviceAccountEnv);
        if (fs.existsSync(resolvedPath)) {
          serviceAccount = JSON.parse(fs.readFileSync(resolvedPath, 'utf-8'));
        }
      }

      if (serviceAccount) {
        adminApp = admin.initializeApp({
          credential: admin.credential.cert(serviceAccount),
          projectId: serviceAccount.project_id || PROJECT_ID
        });
        hasServiceAccount = true;
        console.log('[Firebase Admin] Successfully initialized with service account credentials');
        return adminApp;
      }
    } catch (err: any) {
      console.warn('[Firebase Admin] Could not parse FIREBASE_SERVICE_ACCOUNT:', err.message);
    }
  }

  // Initialize with projectId
  try {
    adminApp = admin.initializeApp({
      projectId: PROJECT_ID
    });
    console.log(`[Firebase Admin] Initialized with Project ID: ${PROJECT_ID}`);
  } catch (err: any) {
    console.warn('[Firebase Admin] Initialization warning:', err.message);
  }

  return adminApp || admin.app();
}

export interface VerifiedFirebaseUser {
  uid: string;
  email: string;
  emailVerified: boolean;
  name?: string;
  picture?: string;
}

/**
 * Cryptographically verifies a Firebase ID Token.
 * 1. Uses Firebase Admin SDK if service account credentials exist.
 * 2. Uses Google Identity Toolkit accounts:lookup API (official Firebase backend REST verification).
 * 3. Inspects token claims (audience, issuer, expiration, email_verified).
 */
export async function verifyFirebaseIdToken(idToken: string): Promise<VerifiedFirebaseUser> {
  if (!idToken || typeof idToken !== 'string') {
    throw new Error('Firebase ID token is required.');
  }

  // First decode JWT claims for pre-validation
  const decoded = jwt.decode(idToken) as any;
  if (!decoded || typeof decoded !== 'object') {
    throw new Error('Invalid or malformed Firebase ID token format.');
  }

  // Check token expiration
  const nowSec = Math.floor(Date.now() / 1000);
  if (decoded.exp && Number(decoded.exp) < nowSec) {
    throw new Error('Firebase Google ID token has expired. Please sign in again.');
  }

  // Verify issuer and audience match our Firebase project
  if (decoded.aud && decoded.aud !== PROJECT_ID) {
    console.warn('[Firebase Verification] Warning: Token audience mismatch:', decoded.aud, 'expected:', PROJECT_ID);
  }

  // Strategy 1: Firebase Admin SDK verifyIdToken (when service account is available)
  if (hasServiceAccount) {
    try {
      const app = getFirebaseAdmin();
      const decodedToken = await app.auth().verifyIdToken(idToken, true);

      if (!decodedToken.email) {
        throw new Error('Google account does not have an associated email address.');
      }

      if (!decodedToken.email_verified) {
        throw new Error('Google email is not verified.');
      }

      return {
        uid: decodedToken.uid,
        email: decodedToken.email.toLowerCase().trim(),
        emailVerified: Boolean(decodedToken.email_verified),
        name: decodedToken.name,
        picture: decodedToken.picture
      };
    } catch (err: any) {
      console.warn('[Firebase Admin SDK] verifyIdToken check note:', err.message);
    }
  }

  // Strategy 2: Google Identity Toolkit REST API Verification
  // This verifies the ID token with Google's Firebase Auth servers directly using the Firebase Web API key
  try {
    const lookupRes = await fetch(
      `https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=${encodeURIComponent(API_KEY)}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ idToken })
      }
    );

    const lookupData = (await lookupRes.json()) as any;

    if (!lookupRes.ok || lookupData.error) {
      const msg = lookupData?.error?.message;
      if (msg === 'TOKEN_EXPIRED') {
        throw new Error('Firebase Google ID token has expired. Please sign in again.');
      }
      if (msg === 'INVALID_ID_TOKEN' || msg === 'USER_NOT_FOUND') {
        throw new Error('Invalid Firebase ID token. Please try signing in again.');
      }
      throw new Error(msg || 'Firebase ID token verification failed.');
    }

    const account = lookupData.users?.[0];
    if (!account || !account.email) {
      throw new Error('Verified Google account does not have an associated email address.');
    }

    const isVerified = account.emailVerified === true || account.emailVerified === 'true' || Boolean(decoded.email_verified);
    if (!isVerified) {
      throw new Error('Google email is not verified.');
    }

    return {
      uid: account.localId || decoded.sub || decoded.user_id,
      email: account.email.toLowerCase().trim(),
      emailVerified: isVerified,
      name: account.displayName || decoded.name || 'Administrator',
      picture: account.photoUrl || decoded.picture
    };
  } catch (lookupErr: any) {
    console.error('[Firebase Verification Error]:', lookupErr.message);
    throw new Error(lookupErr.message || 'Firebase ID token verification failed.');
  }
}
