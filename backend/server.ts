/**
 * Edu Track - Academic Management System
 * Standalone Backend Server Entrypoint
 *
 * Designed to run reliably as a standalone Node/Express service (e.g. Render with Root Directory: server)
 * or as the backend core within the full-stack MERN repository.
 */

import express from 'express';
import path from 'path';
import fs from 'fs';
import cors from 'cors';
import cookieParser from 'cookie-parser';
import dotenv from 'dotenv';
import http from 'http';
import { fileURLToPath } from 'url';

import { connectDB, isDbConnected } from './db/connection';
import { dbStore } from './store/storage';
import { authMiddleware } from './middleware/auth';
import apiRouter from './routes/index';
import { initSocket } from './socket';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load environment variables (.env in server/ or repository root)
dotenv.config();
const rootEnvPath = path.resolve(__dirname, '../.env');
if (fs.existsSync(rootEnvPath)) {
  dotenv.config({ path: rootEnvPath });
}

const PORT = Number(process.env.PORT) || 3000;
const HOST = '0.0.0.0';
const isProduction = process.env.NODE_ENV === 'production';

export async function createBackendApp() {
  const app = express();
  const server = http.createServer(app);

  // Initialize real-time Socket.IO communication
  initSocket(server);

  // Middleware configuration - Enable CORS for Vercel, localhost, and configured domains
  const corsOptions: cors.CorsOptions = {
    origin: (origin, callback) => {
      // Allow requests with no origin (mobile apps, server-to-server, curl)
      if (!origin) return callback(null, true);

      // Allow localhost in development
      if (origin.includes('localhost') || origin.includes('127.0.0.1')) {
        return callback(null, true);
      }

      // Allow any Vercel domain (*.vercel.app)
      if (origin.endsWith('.vercel.app') || origin === 'https://vercel.app') {
        return callback(null, true);
      }

      // Allow explicit environment frontend origins
      if (
        (process.env.CLIENT_URL && origin === process.env.CLIENT_URL) ||
        (process.env.FRONTEND_URL && origin === process.env.FRONTEND_URL)
      ) {
        return callback(null, true);
      }

      // Fallback: allow origin with credentials
      return callback(null, true);
    },
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With', 'Accept', 'Origin']
  };

  app.use(cors(corsOptions));
  app.options('*', cors(corsOptions));
  app.use(express.json({ limit: '10mb' }));
  app.use(express.urlencoded({ extended: true, limit: '10mb' }));
  app.use(cookieParser());
  app.use(authMiddleware);

  // Initialize MongoDB database connection
  await connectDB();
  if (isDbConnected()) {
    console.log('[EduTrack Database] Synchronizing initial datasets to MongoDB collections...');
    await dbStore.syncToMongoDB();
  }

  // Mount API endpoints
  app.use('/api', apiRouter);

  // Root welcome & health route for standalone backend deployment
  app.get('/', (req, res, next) => {
    // If frontend dist directory exists, defer to static frontend handler below
    const possibleDistPaths = [
      path.resolve(process.cwd(), 'frontend/dist'),
      path.resolve(process.cwd(), 'dist'),
      path.resolve(__dirname, '../frontend/dist'),
      path.resolve(process.cwd(), '../dist'),
      path.resolve(__dirname, '../dist')
    ];
    const distPath = possibleDistPaths.find((p) => fs.existsSync(p));
    if (distPath && isProduction) {
      return next();
    }

    res.json({
      status: 'online',
      service: 'EduTrack Academic Core API (MERN Full-Stack Backend)',
      version: '1.0.0',
      port: PORT,
      host: HOST,
      endpoints: {
        health: '/api/health',
        databaseStatus: '/api/database/status',
        databaseData: '/api/database/data',
        auth: '/api/auth/login',
        adminGoogleAuth: '/api/auth/admin/google',
        students: '/api/students',
        faculty: '/api/faculty',
        exams: '/api/online-exams'
      }
    });
  });

  // Frontend integration: Vite dev middleware in local dev, static files in prod if dist exists
  if (!isProduction) {
    try {
      const { createServer: createViteServer } = await import('vite');
      const vite = await createViteServer({
        server: { middlewareMode: true },
        appType: 'spa'
      });
      app.use(vite.middlewares);
    } catch (e: any) {
      // In standalone backend dev, Vite is optional
    }
  } else {
    const possibleDistPaths = [
      path.resolve(process.cwd(), 'frontend/dist'),
      path.resolve(process.cwd(), 'dist'),
      path.resolve(__dirname, '../frontend/dist'),
      path.resolve(process.cwd(), '../dist'),
      path.resolve(__dirname, '../dist')
    ];
    const distPath = possibleDistPaths.find((p) => fs.existsSync(p));
    if (distPath) {
      app.use(express.static(distPath));
      app.get('*', (req, res, next) => {
        if (req.path.startsWith('/api') || req.path.startsWith('/socket.io')) {
          return next();
        }
        res.sendFile(path.join(distPath, 'index.html'));
      });
    }
  }

  return { app, server };
}

export async function startServer() {
  const { app, server } = await createBackendApp();

  server.listen(PORT, HOST, () => {
    console.log(`[EduTrack Backend Server] Server listening on http://${HOST}:${PORT}`);
    console.log(`[EduTrack Backend Server] Health check available at http://${HOST}:${PORT}/api/health`);
    console.log(`[EduTrack Backend Server] Real-time Socket.IO service initialized`);
  });

  return server;
}

// Start immediately when executed directly
startServer().catch((err) => {
  console.error('[EduTrack Backend Server] Fatal startup error:', err);
  process.exit(1);
});
