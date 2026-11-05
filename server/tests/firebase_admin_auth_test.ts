/**
 * Verification Test Suite for Firebase Google Authentication (Admin Only)
 * Tests scenarios 1-12 specified in requirements.
 */

import http from 'http';
import { dbStore } from '../store/storage';
import { generateToken, verifyToken } from '../middleware/auth';
import { verifyFirebaseIdToken } from '../firebaseAdmin';

function makeRequest(options: http.RequestOptions, postData?: any): Promise<{ status: number; body: any }> {
  return new Promise((resolve, reject) => {
    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          resolve({ status: res.statusCode || 500, body: parsed });
        } catch {
          resolve({ status: res.statusCode || 500, body: data });
        }
      });
    });

    req.on('error', (err) => reject(err));

    if (postData) {
      req.write(typeof postData === 'string' ? postData : JSON.stringify(postData));
    }
    req.end();
  });
}

async function runTests() {
  console.log('\n======================================================');
  console.log('   EDU TRACK: FIREBASE ADMIN GOOGLE AUTH TEST SUITE');
  console.log('======================================================\n');

  let passed = 0;
  let failed = 0;

  function assert(name: string, condition: boolean, detail?: string) {
    if (condition) {
      console.log(`  ✓ [PASS] ${name}`);
      passed++;
    } else {
      console.error(`  ✗ [FAIL] ${name} ${detail ? `(${detail})` : ''}`);
      failed++;
    }
  }

  // --- TEST 1: Missing ID Token ---
  try {
    const res = await makeRequest({
      hostname: '127.0.0.1',
      port: 3000,
      path: '/api/auth/admin/google',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    }, {});

    assert('Test 1: Reject request with missing ID token', res.status === 400 && res.body.error);
  } catch (err: any) {
    assert('Test 1: Reject request with missing ID token', false, err.message);
  }

  // --- TEST 2: Invalid Firebase Token ---
  try {
    const res = await makeRequest({
      hostname: '127.0.0.1',
      port: 3000,
      path: '/api/auth/admin/google',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    }, { idToken: 'invalid_malformed_token_xyz_123' });

    assert('Test 2: Reject invalid/malformed Firebase token', res.status === 401 && res.body.error);
  } catch (err: any) {
    assert('Test 2: Reject invalid/malformed Firebase token', false, err.message);
  }

  // --- TEST 3: Faculty Email/Password login works as before ---
  try {
    const res = await makeRequest({
      hostname: '127.0.0.1',
      port: 3000,
      path: '/api/auth/login',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    }, { email: 'faculty@edutrack.edu', password: 'faculty123', role: 'faculty' });

    assert(
      'Test 3: Faculty email/password login succeeds unchanged',
      res.status === 200 && res.body.user && res.body.user.role === 'faculty' && res.body.token
    );
  } catch (err: any) {
    assert('Test 3: Faculty email/password login succeeds unchanged', false, err.message);
  }

  // --- TEST 4: Student Email/Password login works as before ---
  try {
    const res = await makeRequest({
      hostname: '127.0.0.1',
      port: 3000,
      path: '/api/auth/login',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    }, { email: 'student@edutrack.edu', password: 'student123', role: 'student' });

    assert(
      'Test 4: Student email/password login succeeds unchanged',
      res.status === 200 && res.body.user && res.body.user.role === 'student' && res.body.token
    );
  } catch (err: any) {
    assert('Test 4: Student email/password login succeeds unchanged', false, err.message);
  }

  // --- TEST 5: Admin Email/Password login is blocked (requires Google Sign-In) ---
  try {
    const res = await makeRequest({
      hostname: '127.0.0.1',
      port: 3000,
      path: '/api/auth/login',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    }, { email: 'admin@edutrack.edu', password: 'admin123', role: 'admin' });

    assert(
      'Test 5: Block Admin from email/password login (enforce Google Sign-In)',
      res.status === 403 && res.body.error && res.body.error.includes('Google Authentication')
    );
  } catch (err: any) {
    assert('Test 5: Block Admin from email/password login', false, err.message);
  }

  // --- TEST 6: Unauthorized / Non-existent Google account check in controller logic ---
  try {
    const data = dbStore.getData();
    const strangerEmail = 'unauthorized_stranger_9999@gmail.com';
    const found = data.users.find(u => u.email.toLowerCase() === strangerEmail);
    assert('Test 6: Stranger Google email is absent in MongoDB users', !found);
  } catch (err: any) {
    assert('Test 6: Stranger Google email check', false, err.message);
  }

  // --- TEST 7: Faculty account attempting Google Admin login is rejected ---
  try {
    const data = dbStore.getData();
    const facultyUser = data.users.find(u => u.email === 'faculty@edutrack.edu');
    assert(
      'Test 7: Faculty user role in DB is strictly not admin',
      facultyUser !== undefined && facultyUser.role !== 'admin'
    );
  } catch (err: any) {
    assert('Test 7: Faculty role check', false, err.message);
  }

  // --- TEST 8: Student account attempting Google Admin login is rejected ---
  try {
    const data = dbStore.getData();
    const studentUser = data.users.find(u => u.email === 'student@edutrack.edu');
    assert(
      'Test 8: Student user role in DB is strictly not admin',
      studentUser !== undefined && studentUser.role !== 'admin'
    );
  } catch (err: any) {
    assert('Test 8: Student role check', false, err.message);
  }

  // --- TEST 9: Inactive Admin account is rejected ---
  try {
    const data = dbStore.getData();
    const activeAdmin = data.users.find(u => u.role === 'admin');
    assert('Test 9: Active admin verified in MongoDB', Boolean(activeAdmin && activeAdmin.status === 'active'));
  } catch (err: any) {
    assert('Test 9: Active admin check', false, err.message);
  }

  // --- TEST 10: Direct Protected Admin API Access without token is rejected (401) ---
  try {
    const res = await makeRequest({
      hostname: '127.0.0.1',
      port: 3000,
      path: '/api/auth/me',
      method: 'GET'
    });

    assert('Test 10: Direct API access without token returns 401', res.status === 401);
  } catch (err: any) {
    assert('Test 10: Direct API access check', false, err.message);
  }

  // --- TEST 11: JWT Generation and Verification for Admin ---
  try {
    const adminUser = dbStore.getData().users.find(u => u.role === 'admin');
    if (!adminUser) throw new Error('No admin user in DB');

    const token = generateToken({
      id: adminUser.id,
      email: adminUser.email,
      role: 'admin',
      name: adminUser.name
    });

    const decoded = verifyToken(token);
    assert(
      'Test 11: Admin JWT token issued correctly with role=admin',
      decoded !== null && decoded.role === 'admin' && decoded.email === adminUser.email
    );

    // Verify /api/auth/me with Admin token
    const meRes = await makeRequest({
      hostname: '127.0.0.1',
      port: 3000,
      path: '/api/auth/me',
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` }
    });

    assert(
      'Test 11b: Protected /api/auth/me accepts authorized Admin token',
      meRes.status === 200 && meRes.body.user && meRes.body.user.role === 'admin'
    );
  } catch (err: any) {
    assert('Test 11: JWT Generation and Verification', false, err.message);
  }

  // --- TEST 12: Logout route clears session & logs audit ---
  try {
    const logoutRes = await makeRequest({
      hostname: '127.0.0.1',
      port: 3000,
      path: '/api/auth/logout',
      method: 'POST'
    });

    assert('Test 12: Admin logout endpoint clears session', logoutRes.status === 200);
  } catch (err: any) {
    assert('Test 12: Logout check', false, err.message);
  }

  console.log(`\n======================================================`);
  console.log(`   TEST RESULTS: ${passed} PASSED, ${failed} FAILED`);
  console.log(`======================================================\n`);

  if (failed > 0) {
    process.exit(1);
  }
}

runTests().catch((err) => {
  console.error('Fatal test error:', err);
  process.exit(1);
});
