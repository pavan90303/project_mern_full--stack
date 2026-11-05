import express from 'express';
import path from 'path';
import fs from 'fs';
import cors from 'cors';
import cookieParser from 'cookie-parser';
import dotenv from 'dotenv';
import { createServer as createViteServer } from 'vite';
import { connectDB, isDbConnected } from './server/db/connection';
import { dbStore } from './server/store/storage';
import { authMiddleware } from './server/middleware/auth';
import apiRouter from './server/routes/index';

import http from 'http';
import { initSocket } from './server/socket';

dotenv.config();

const PORT = Number(process.env.PORT) || 3000;
const isProduction = process.env.NODE_ENV === 'production';

async function startServer() {
  const app = express();
  const server = http.createServer(app);

  // Initialize real-time Socket.IO communication
  initSocket(server);

  // Middleware configuration
  app.use(cors({
    origin: true,
    credentials: true
  }));
  app.use(express.json({ limit: '10mb' }));
  app.use(express.urlencoded({ extended: true, limit: '10mb' }));
  app.use(cookieParser());
  app.use(authMiddleware);

  // Initialize database connection
  await connectDB();
  if (isDbConnected()) {
    console.log('[EduTrack Database] Synchronizing initial datasets to MongoDB collections...');
    await dbStore.syncToMongoDB();
  }

  // Mount API endpoints
  app.use('/api', apiRouter);

  // Root welcome & health route for standalone backend deployment
  app.get('/', (req, res) => {
    res.json({
      status: 'online',
      service: 'EduTrack Academic Core API (MERN Full-Stack Backend)',
      version: '1.0.0',
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

  // Frontend integration: Vite middleware in dev, static files in prod (if dist exists)
  if (!isProduction) {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'spa'
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.resolve(process.cwd(), 'dist');
    if (fs.existsSync(distPath)) {
      app.use(express.static(distPath));
      app.get('*', (req, res) => {
        res.sendFile(path.join(distPath, 'index.html'));
      });
    }
  }

  server.listen(PORT, '0.0.0.0', () => {
    console.log(`[EduTrack Full-Stack Server] Server listening on http://0.0.0.0:${PORT}`);
    console.log(`[EduTrack Full-Stack Server] API endpoints available at http://0.0.0.0:${PORT}/api`);
    console.log(`[EduTrack Full-Stack Server] Real-time Socket.IO initialized`);
  });
}

startServer().catch((err) => {
  console.error('[EduTrack Full-Stack Server] Fatal startup error:', err);
  process.exit(1);
});
