import express from 'express';
import { createProxyMiddleware } from 'http-proxy-middleware';
import { spawn } from 'child_process';

const app = express();
const PORT = 3000;

// Spawn Django subprocess on Port 8000
console.log('[Django Service] Spawning Django backend on 127.0.0.1:8000...');
const djangoProcess = spawn('python3', ['manage.py', 'runserver', '127.0.0.1:8000'], {
  stdio: 'inherit',
  shell: true,
});

djangoProcess.on('error', (err) => {
  console.error('[Django Service] Failed to start Django back-end process:', err);
});

djangoProcess.on('close', (code) => {
  console.log(`[Django Service] Django process exited with code ${code}`);
});

// Graceful cleanup of child process on server stop
process.on('exit', () => {
  try {
    djangoProcess.kill();
  } catch (e) {}
});
process.on('SIGINT', () => {
  try {
    djangoProcess.kill();
  } catch (e) {}
  process.exit();
});
process.on('SIGTERM', () => {
  try {
    djangoProcess.kill();
  } catch (e) {}
  process.exit();
});

// Proxy everything to Django running on localhost:8000
app.use('/', createProxyMiddleware({
  target: 'http://127.0.0.1:8000',
  changeOrigin: true,
  ws: true,
  xfwd: true,
  on: {
    proxyReq: (proxyReq, req, res) => {
      // Force X-Forwarded-Proto as 'https' if the client request was secure or proxied over HTTPS
      const rawProto = req.headers['x-forwarded-proto'];
      const isHttps = rawProto === 'https' || (req as any).secure || req.headers['x-forwarded-port'] === '443';
      
      proxyReq.setHeader('X-Forwarded-Proto', isHttps ? 'https' : 'http');
      
      // Ensure authorization, cookie, and host headers are transparently passed through
      if (req.headers['authorization']) {
        proxyReq.setHeader('Authorization', req.headers['authorization']);
      }
    }
  }
}));

app.listen(PORT, '0.0.0.0', () => {
  console.log(`[Django-Express Proxy] Listening on http://localhost:${PORT}, proxying to 127.0.0.1:8000`);
});
