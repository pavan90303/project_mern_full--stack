import React, { useState } from 'react';
import {
  GraduationCap,
  ArrowLeft,
  Lock,
  Mail,
  User as UserIcon,
  AlertCircle,
  Shield,
  Eye,
  EyeOff,
  Loader2,
  CheckCircle2,
  KeyRound,
  ShieldCheck
} from 'lucide-react';
import { EduTrackApi } from '../../services/apiService';
import { User, UserRole } from '../../types';
import { signInWithGoogle } from '../../config/firebase';

interface LoginPageProps {
  onLoginSuccess: (user: User) => void;
  onBackToLanding: () => void;
  initialRole?: UserRole;
}

export const LoginPage: React.FC<LoginPageProps> = ({
  onLoginSuccess,
  onBackToLanding,
  initialRole = 'admin'
}) => {
  const [activeRole, setActiveRole] = useState<UserRole>(() => {
    try {
      const params = new URLSearchParams(window.location.search);
      const r = (params.get('role') || params.get('login'))?.toLowerCase();
      if (r === 'admin' || r === 'faculty' || r === 'student') return r;
    } catch {}
    return initialRole;
  });
  const [identifier, setIdentifier] = useState(() => {
    try {
      const params = new URLSearchParams(window.location.search);
      if (params.get('demo') === '1' || params.get('demo') === 'true' || params.get('autofill') === 'true') {
        const r = (params.get('role') || params.get('login') || initialRole)?.toLowerCase();
        if (r === 'faculty') return 'faculty@edutrack.edu';
        if (r === 'student') return '990000003';
        return 'pavan90303@gmail.com';
      }
    } catch {}
    return '';
  });
  const [password, setPassword] = useState(() => {
    try {
      const params = new URLSearchParams(window.location.search);
      if (params.get('demo') === '1' || params.get('demo') === 'true' || params.get('autofill') === 'true') {
        const r = (params.get('role') || params.get('login') || initialRole)?.toLowerCase();
        if (r === 'faculty') return 'faculty123';
        if (r === 'student') return 'student123';
        return 'Pavan90303';
      }
    } catch {}
    return '';
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [setupSuccessMessage, setSetupSuccessMessage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // First-time Google user password setup state
  const [googleSetupUser, setGoogleSetupUser] = useState<{
    email: string;
    name: string;
    role: UserRole;
  } | null>(null);
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const handleRoleChange = (role: UserRole) => {
    setActiveRole(role);
    setError(null);
    setSetupSuccessMessage(null);
    setGoogleSetupUser(null);
    setIdentifier('');
    setPassword('');
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSetupSuccessMessage(null);

    if (!identifier.trim()) {
      setError('Please enter your institutional email, register number, or employee ID.');
      return;
    }

    if (!password) {
      setError('Please enter your account password.');
      return;
    }

    setIsLoading(true);

    try {
      const res = await EduTrackApi.loginAsync(identifier, password, activeRole);
      setIsLoading(false);

      if (res.success && res.user) {
        onLoginSuccess(res.user);
      } else {
        setError(res.error || 'Invalid credentials or unprovisioned account. Contact your university administrator.');
      }
    } catch {
      setIsLoading(false);
      setError('Connection failure. Please verify network access or try again.');
    }
  };

  const handleGoogleLogin = async () => {
    setError(null);
    setSetupSuccessMessage(null);
    setIsLoading(true);

    try {
      const { idToken, email, name } = await signInWithGoogle();

      if (!email) {
        setIsLoading(false);
        setError('No email was returned from Google sign-in. Please try again.');
        return;
      }

      // 1. Admin login flow
      if (activeRole === 'admin') {
        const res = await EduTrackApi.loginWithGoogle(idToken, 'admin', email, name);
        setIsLoading(false);
        if (res.success && res.user) {
          onLoginSuccess(res.user);
        } else {
          setError(res.error || 'Could not complete Administrator authentication. Please try again.');
        }
        return;
      }

      // 2. Faculty & Student login flow
      const res = await EduTrackApi.loginWithGoogle(idToken, activeRole, email, name);
      setIsLoading(false);

      if (res.needsPasswordSetup) {
        // First-time login: show Create & Re-enter Password setup view
        setGoogleSetupUser({
          email: res.email || email,
          name: res.name || name || email.split('@')[0],
          role: activeRole
        });
        setNewPassword('');
        setConfirmPassword('');
      } else if (res.success && res.user) {
        // Returning user with existing password: login directly
        onLoginSuccess(res.user);
      } else {
        setError(res.error || 'Google authentication could not be completed. Please try again.');
      }
    } catch (err: any) {
      setIsLoading(false);
      setError(err.message || 'Google sign-in could not be completed. Please try again.');
    }
  };

  const handleSavePasswordSetup = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!googleSetupUser) return;

    if (!newPassword || newPassword.trim().length < 6) {
      setError('Please create a password with at least 6 characters.');
      return;
    }

    if (newPassword !== confirmPassword) {
      setError('Passwords do not match. Please re-enter your password to confirm.');
      return;
    }

    setIsLoading(true);

    try {
      const res = await EduTrackApi.setupPasswordForGoogleUser(
        googleSetupUser.email,
        googleSetupUser.name,
        newPassword.trim(),
        googleSetupUser.role
      );
      setIsLoading(false);

      if (res.success && res.user) {
        const role = googleSetupUser.role;
        const savedEmail = googleSetupUser.email;
        const savedPassword = newPassword.trim();

        // Redirect back to login for this role with pre-filled credentials
        setGoogleSetupUser(null);
        setActiveRole(role);
        setIdentifier(savedEmail);
        setPassword(savedPassword);
        setSetupSuccessMessage(
          `Google email verified and account password created! Click "${role === 'faculty' ? 'Access Faculty Portal' : 'Access Student Portal'}" below to log in, or use your email and password for future logins.`
        );
      } else {
        setError(res.error || 'Failed to save account password. Please try again.');
      }
    } catch (err: any) {
      setIsLoading(false);
      setError(err.message || 'Error occurred while saving password. Please try again.');
    }
  };

  // Role-specific labels, placeholders, and descriptions matching institutional specs
  const roleConfig = {
    admin: {
      tabLabel: 'Admin Login',
      inputLabel: 'Administrator Email',
      inputPlaceholder: 'admin@edutrack.edu or any administrator email',
      inputIcon: Mail,
      buttonText: 'Access Administrator Portal',
      infoTitle: 'System Administrator Portal Access',
      infoDesc: 'Sign in with any administrator email or click "Sign in with Google" with any Google account. Your account is verified and redirected directly to the Admin Dashboard.'
    },
    faculty: {
      tabLabel: 'Faculty Login',
      inputLabel: 'Faculty Email or Employee ID',
      inputPlaceholder: 'faculty@edutrack.edu or EMP-101',
      inputIcon: UserIcon,
      buttonText: 'Access Faculty Portal',
      infoTitle: 'Faculty Portal Access',
      infoDesc: 'First-time login: verify your institutional Google account and create a password. Second-time login: sign in directly via Google or using your verified email and created password.'
    },
    student: {
      tabLabel: 'Student Login',
      inputLabel: 'Student Register Number / Email',
      inputPlaceholder: '990000001 or student@edutrack.edu',
      inputIcon: UserIcon,
      buttonText: 'Access Student Portal',
      infoTitle: 'Student Portal Access',
      infoDesc: 'First-time login: verify your institutional Google account and create a password. Second-time login: sign in directly via Google or using your verified email and created password.'
    }
  }[activeRole];

  const InputIcon = roleConfig.inputIcon;

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 flex flex-col justify-center py-8 sm:py-14 px-4 sm:px-6 lg:px-8 selection:bg-indigo-500 selection:text-white">
      
      {/* Return Navigation */}
      <div className="w-full max-w-md mx-auto mb-4 text-center">
        <button
          onClick={onBackToLanding}
          className="inline-flex items-center gap-2 text-xs font-semibold text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200 transition-colors py-1.5 px-2 rounded-lg"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Return to University Overview</span>
        </button>
      </div>

      <div className="w-full max-w-md mx-auto">
        
        {/* Brand Header */}
        <div className="text-center mb-6">
          <div className="w-14 h-14 rounded-2xl bg-indigo-600 mx-auto flex items-center justify-center text-white shadow-md shadow-indigo-200 dark:shadow-none mb-4">
            <GraduationCap className="w-7 h-7" />
          </div>
          <h1 className="text-2xl sm:text-[26px] font-extrabold text-slate-900 dark:text-white tracking-tight">
            Edu Track Institutional Login
          </h1>
          <p className="mt-1.5 text-xs sm:text-[13px] text-slate-500 dark:text-slate-400 max-w-sm mx-auto leading-relaxed">
            Secure role-based authentication for University Administration, Faculty, and Students
          </p>
        </div>

        {/* Login Card */}
        <div className="bg-white dark:bg-slate-900 py-6 sm:py-8 px-5 sm:px-8 shadow-xl shadow-slate-200/60 dark:shadow-none rounded-3xl border border-slate-200/80 dark:border-slate-800">
          
          {/* Role Segmented Tabs Switcher */}
          <div className="bg-slate-100 dark:bg-slate-800/80 p-1 rounded-2xl flex gap-1 mb-6">
            <button
              type="button"
              onClick={() => handleRoleChange('admin')}
              className={`flex-1 py-2 sm:py-2.5 px-3 text-xs sm:text-sm font-bold rounded-xl transition-all text-center ${
                activeRole === 'admin'
                  ? 'bg-white dark:bg-slate-700 text-indigo-600 dark:text-indigo-300 shadow-sm'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              Admin Login
            </button>
            <button
              type="button"
              onClick={() => handleRoleChange('faculty')}
              className={`flex-1 py-2 sm:py-2.5 px-3 text-xs sm:text-sm font-bold rounded-xl transition-all text-center ${
                activeRole === 'faculty'
                  ? 'bg-white dark:bg-slate-700 text-indigo-600 dark:text-indigo-300 shadow-sm'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              Faculty Login
            </button>
            <button
              type="button"
              onClick={() => handleRoleChange('student')}
              className={`flex-1 py-2 sm:py-2.5 px-3 text-xs sm:text-sm font-bold rounded-xl transition-all text-center ${
                activeRole === 'student'
                  ? 'bg-white dark:bg-slate-700 text-indigo-600 dark:text-indigo-300 shadow-sm'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              Student Login
            </button>
          </div>

          {/* Success Banner */}
          {setupSuccessMessage && (
            <div className="mb-5 p-3.5 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-900/60 text-xs text-emerald-800 dark:text-emerald-300 flex items-start gap-2.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" />
              <span className="leading-snug">{setupSuccessMessage}</span>
            </div>
          )}

          {/* Error Banner */}
          {error && (
            <div className="mb-5 p-3.5 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900/60 text-xs text-rose-800 dark:text-rose-300 flex items-start gap-2.5">
              <AlertCircle className="w-4 h-4 text-rose-600 dark:text-rose-400 shrink-0 mt-0.5" />
              <span className="leading-snug">{error}</span>
            </div>
          )}

          {/* First-Time Google User Password Creation Form */}
          {googleSetupUser ? (
            <form onSubmit={handleSavePasswordSetup} className="space-y-4">
              <div className="p-3 rounded-2xl bg-indigo-50/70 dark:bg-indigo-950/30 border border-indigo-100 dark:border-indigo-900/50 mb-4">
                <div className="flex items-center gap-2 text-indigo-700 dark:text-indigo-300 font-bold text-xs mb-1">
                  <KeyRound className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
                  <span>First-Time {googleSetupUser.role.toUpperCase()} Account Setup</span>
                </div>
                <p className="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed">
                  Your Google email has been verified. Please create your institutional password to complete first-time registration.
                </p>
              </div>

              {/* Readonly Verified Username / Email */}
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5 flex items-center justify-between">
                  <span>Institutional Username (Verified Email)</span>
                  <span className="inline-flex items-center gap-1 text-[10px] font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/60 px-2 py-0.5 rounded-full border border-emerald-200 dark:border-emerald-800">
                    <ShieldCheck className="w-3 h-3" />
                    Verified
                  </span>
                </label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type="text"
                    readOnly
                    value={googleSetupUser.email}
                    className="w-full pl-10 pr-4 py-2.5 text-xs sm:text-sm rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-100 dark:bg-slate-800/80 text-slate-700 dark:text-slate-300 font-medium min-h-[44px] cursor-not-allowed select-all"
                  />
                </div>
              </div>

              {/* Create Password */}
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
                  Create Password
                </label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type={showNewPassword ? 'text' : 'password'}
                    required
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    placeholder="Create password (minimum 6 characters)"
                    autoComplete="new-password"
                    className="w-full pl-10 pr-10 py-2.5 text-xs sm:text-sm rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-800/50 text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600 font-mono min-h-[44px] transition-colors"
                  />
                  <button
                    type="button"
                    onClick={() => setShowNewPassword(!showNewPassword)}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 p-1 cursor-pointer"
                    aria-label={showNewPassword ? 'Hide password' : 'Show password'}
                  >
                    {showNewPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              {/* Re-enter Password */}
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
                  Re-enter Password
                </label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type={showConfirmPassword ? 'text' : 'password'}
                    required
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="Re-enter your password to confirm"
                    autoComplete="new-password"
                    className="w-full pl-10 pr-10 py-2.5 text-xs sm:text-sm rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-800/50 text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600 font-mono min-h-[44px] transition-colors"
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 p-1 cursor-pointer"
                    aria-label={showConfirmPassword ? 'Hide password' : 'Show password'}
                  >
                    {showConfirmPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              {/* Password Action Buttons */}
              <div className="pt-2 space-y-2">
                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full py-3 px-4 text-xs sm:text-sm font-bold text-white bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 disabled:bg-indigo-400 rounded-xl shadow-sm transition-all flex items-center justify-center gap-2 min-h-[46px] cursor-pointer"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>Saving Account Password...</span>
                    </>
                  ) : (
                    <span>Save Password & Go to {roleConfig.tabLabel}</span>
                  )}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setGoogleSetupUser(null);
                    setError(null);
                  }}
                  className="w-full py-2 px-3 text-xs font-semibold text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-slate-200 transition-colors"
                >
                  Cancel and return to login
                </button>
              </div>
            </form>
          ) : (
            <>
              {/* Email ID & Password Form */}
              <form onSubmit={handleLogin} className="space-y-4">
                
                {/* Primary Identifier */}
                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
                    {roleConfig.inputLabel}
                  </label>
                  <div className="relative">
                    <InputIcon className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                    <input
                      type="text"
                      required
                      value={identifier}
                      onChange={(e) => setIdentifier(e.target.value)}
                      placeholder={roleConfig.inputPlaceholder}
                      autoComplete="username"
                      className="w-full pl-10 pr-4 py-2.5 text-xs sm:text-sm rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-800/50 text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600 font-medium min-h-[44px] transition-colors"
                    />
                  </div>
                </div>

                {/* Password */}
                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
                    Account Password
                  </label>
                  <div className="relative">
                    <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                    <input
                      type={showPassword ? 'text' : 'password'}
                      required
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="••••••••"
                      autoComplete="current-password"
                      className="w-full pl-10 pr-10 py-2.5 text-xs sm:text-sm rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-800/50 text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600 font-mono min-h-[44px] transition-colors"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 p-1 cursor-pointer"
                      aria-label={showPassword ? 'Hide password' : 'Show password'}
                    >
                      {showPassword ? (
                        <EyeOff className="w-4 h-4" />
                      ) : (
                        <Eye className="w-4 h-4" />
                      )}
                    </button>
                  </div>
                </div>

                {/* Submit CTA Button */}
                <div className="pt-1">
                  <button
                    type="submit"
                    disabled={isLoading}
                    className="w-full py-3 px-4 text-xs sm:text-sm font-bold text-white bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 disabled:bg-indigo-400 rounded-xl shadow-sm transition-all flex items-center justify-center gap-2 min-h-[46px] cursor-pointer"
                  >
                    {isLoading ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        <span>Authenticating Identity...</span>
                      </>
                    ) : (
                      <span>{roleConfig.buttonText}</span>
                    )}
                  </button>
                </div>
              </form>

              {/* Google Sign-in Option for All Roles (Admin, Faculty, Student) */}
              <div className="mt-4 pt-3 border-t border-slate-200 dark:border-slate-800 space-y-3">
                <div className="relative">
                  <div className="absolute inset-0 flex items-center">
                    <div className="w-full border-t border-slate-200 dark:border-slate-700" />
                  </div>
                  <div className="relative flex justify-center text-xs">
                    <span className="bg-white dark:bg-slate-900 px-3 text-slate-400 font-semibold uppercase tracking-wider text-[10px]">
                      Or continue with Google
                    </span>
                  </div>
                </div>

                <button
                  type="button"
                  onClick={handleGoogleLogin}
                  disabled={isLoading}
                  className="w-full py-2.5 px-4 text-xs sm:text-sm font-bold text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 active:bg-slate-100 border border-slate-300 dark:border-slate-700 rounded-xl shadow-xs transition-all flex items-center justify-center gap-3 min-h-[46px] cursor-pointer"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin text-indigo-600" />
                      <span>Verifying Google Authorization...</span>
                    </>
                  ) : (
                    <>
                      <svg className="w-4 h-4 shrink-0" viewBox="0 0 24 24">
                        <path
                          fill="#4285F4"
                          d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                        />
                        <path
                          fill="#34A853"
                          d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                        />
                        <path
                          fill="#FBBC05"
                          d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
                        />
                        <path
                          fill="#EA4335"
                          d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"
                        />
                      </svg>
                      <span>
                        {activeRole === 'admin'
                          ? 'Sign in with Google'
                          : `Sign in with Google (${roleConfig.tabLabel})`}
                      </span>
                    </>
                  )}
                </button>
              </div>
            </>
          )}

          {/* Institutional Role Information Box (Replaces Initial Setup Credentials) */}
          <div className="mt-6 p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200/80 dark:border-slate-700/80 text-left">
            <div className="flex items-center gap-2 font-bold text-slate-800 dark:text-slate-200 text-xs sm:text-[13px] mb-1">
              <Shield className="w-4 h-4 text-indigo-600 dark:text-indigo-400 shrink-0" />
              <span>{roleConfig.infoTitle}</span>
            </div>
            <p className="text-[11px] sm:text-xs leading-relaxed text-slate-500 dark:text-slate-400">
              {roleConfig.infoDesc}
            </p>
          </div>

        </div>

      </div>

    </div>
  );
};
