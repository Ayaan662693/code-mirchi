import express, { Request, Response, NextFunction } from 'express';
import cors from 'cors';
import path from 'node:path';
import fs from 'node:fs';
import crypto from 'node:crypto';
import * as db from './server/db.js';
import * as backup from './server/backup.js';

const app = express();
const PORT = 3000;
const HOST = '0.0.0.0';

const ADMIN_API_KEY = process.env.ADMIN_API_KEY || 'launchpad-admin-secret-key-2026';

// --- Demo Credentials Configuration ---
const DEMO_USER = {
  id: 'admin',
  password: '1234',
  name: 'Demo Administrator',
  role: 'admin',
  avatar: '🛡️',
  title: 'Platform Administrator'
};

// --- In-Memory Human Verification (CAPTCHA) Store ---
interface CaptchaChallenge {
  id: string;
  code: string;
  expiresAt: number;
}
const captchaStore = new Map<string, CaptchaChallenge>();

// Clean up expired captchas every 2 minutes
setInterval(() => {
  const now = Date.now();
  for (const [k, v] of captchaStore.entries()) {
    if (now > v.expiresAt) captchaStore.delete(k);
  }
}, 120000);

function generateCaptchaCode(): string {
  // Clear, unambiguous alphanumeric characters (no 0/O, no 1/I/L)
  const pool = '23456789ABCDEFGHJKLMNPQRSTUVWXYZ';
  let code = '';
  for (let i = 0; i < 6; i++) {
    code += pool[Math.floor(Math.random() * pool.length)];
  }
  return code;
}

// --- In-Memory Auth Sessions Store ---
interface UserSession {
  token: string;
  id: string;
  username: string;
  name: string;
  role: string;
  avatar: string;
  title: string;
  loginTime: number;
  expiresAt: number;
}
const sessionStore = new Map<string, UserSession>();

// Clean up expired sessions every 10 minutes
setInterval(() => {
  const now = Date.now();
  for (const [k, v] of sessionStore.entries()) {
    if (now > v.expiresAt) sessionStore.delete(k);
  }
}, 600000);

// --- Basic Middlewares ---
app.use(cors());
app.use(express.json({ limit: '5mb' }));
app.use(express.urlencoded({ extended: true }));

// --- Security Headers Middleware ---
app.use((req: Request, res: Response, next: NextFunction) => {
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains; preload');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.setHeader('Permissions-Policy', 'camera=(), microphone=(), geolocation=()');
  next();
});

// --- Simple In-Memory Rate Limiter ---
interface RateLimitEntry {
  count: number;
  resetAt: number;
}
const rateLimits = new Map<string, RateLimitEntry>();

function rateLimit(maxRequests: number, windowSeconds: number) {
  return (req: Request, res: Response, next: NextFunction) => {
    const ip = (req.headers['x-forwarded-for'] as string)?.split(',')[0]?.trim() || req.socket.remoteAddress || '127.0.0.1';
    const key = `${ip}:${req.baseUrl || req.path}`;
    const now = Date.now();
    const windowMs = windowSeconds * 1000;

    let entry = rateLimits.get(key);
    if (!entry || now > entry.resetAt) {
      entry = { count: 1, resetAt: now + windowMs };
      rateLimits.set(key, entry);
      return next();
    }

    entry.count += 1;
    if (entry.count > maxRequests) {
      res.status(429).json({
        error: 'Too Many Requests. Please slow down.',
        retry_after_seconds: Math.ceil((entry.resetAt - now) / 1000)
      });
      return;
    }
    next();
  };
}

// Clean up expired rate limit entries every 5 minutes
setInterval(() => {
  const now = Date.now();
  for (const [k, v] of rateLimits.entries()) {
    if (now > v.resetAt) rateLimits.delete(k);
  }
}, 300000);

// --- Admin Auth Middleware ---
function requireAdmin(req: Request, res: Response, next: NextFunction) {
  const providedKey = req.headers['x-admin-key'] || req.query.api_key;
  if (providedKey && String(providedKey) === ADMIN_API_KEY) {
    return next();
  }

  // Also check Bearer auth token or x-auth-token header
  const authHeader = req.headers.authorization || (req.headers['x-auth-token'] as string);
  const token = authHeader?.startsWith('Bearer ') ? authHeader.substring(7).trim() : authHeader?.trim();
  if (token && sessionStore.has(token)) {
    const session = sessionStore.get(token)!;
    if (session.expiresAt > Date.now() && session.role === 'admin') {
      return next();
    }
  }

  res.status(401).json({ error: 'Unauthorized. Admin authorization required.' });
}

// --- Authentication & Human Verification Endpoints ---

// 1. Get new Human Text Verification (CAPTCHA) challenge
app.get('/api/auth/captcha', rateLimit(60, 60), (req: Request, res: Response) => {
  const id = crypto.randomUUID();
  const code = generateCaptchaCode();
  const expiresAt = Date.now() + 10 * 60 * 1000; // 10 minutes

  captchaStore.set(id, { id, code, expiresAt });

  res.json({
    captchaId: id,
    code: code, // returned for client-side animated canvas rendering & accessibility audio
    expiresInSeconds: 600
  });
});

// 2. Demo User Login with Human Text Verification
app.post('/api/auth/login', rateLimit(30, 60), (req: Request, res: Response) => {
  const { id, username, password, captchaId, captchaCode } = req.body || {};

  const inputId = String(id || username || '').trim().toLowerCase();
  const inputPassword = String(password || '').trim();
  const inputCaptchaCode = String(captchaCode || '').replace(/[^A-Za-z0-9]/g, '').toUpperCase();

  // Validate required fields
  if (!inputId) {
    res.status(400).json({ error: 'User ID is required.' });
    return;
  }
  if (!inputPassword) {
    res.status(400).json({ error: 'Password is required.' });
    return;
  }
  if (!captchaId || !inputCaptchaCode) {
    res.status(400).json({ error: 'Please enter the 6 human verification characters.', field: 'captcha' });
    return;
  }

  // Verify CAPTCHA challenge
  const isLocalFallback = typeof captchaId === 'string' && captchaId.startsWith('local-');
  const challenge = captchaStore.get(captchaId);
  if (!challenge && !isLocalFallback) {
    res.status(400).json({
      error: 'Verification code expired or not found. Please click Refresh to get a new code.',
      field: 'captcha',
      needsRefresh: true
    });
    return;
  }

  if (challenge) {
    if (Date.now() > challenge.expiresAt) {
      captchaStore.delete(captchaId);
      res.status(400).json({
        error: 'Verification code expired. Please refresh the code and try again.',
        field: 'captcha',
        needsRefresh: true
      });
      return;
    }

    // Check code case-insensitively
    if (challenge.code.replace(/[^A-Za-z0-9]/g, '').toUpperCase() !== inputCaptchaCode) {
      // Invalidate challenge upon failed attempt to prevent brute force
      captchaStore.delete(captchaId);
      res.status(400).json({
        error: 'Human verification failed. The characters entered did not match. Please try again with the new code.',
        field: 'captcha',
        needsRefresh: true
      });
      return;
    }

    // Once captcha is verified, consume it
    captchaStore.delete(captchaId);
  }

  // Validate Demo Credentials (id: admin, password: 1234)
  if (inputId !== DEMO_USER.id || inputPassword !== DEMO_USER.password) {
    res.status(401).json({
      error: 'Invalid credentials. Please use Demo ID: "admin" and Demo Password: "1234".',
      field: 'credentials'
    });
    return;
  }

  // Generate secure session token
  const token = `mirchi_${crypto.randomBytes(24).toString('hex')}`;
  const now = Date.now();
  const expiresAt = now + 7 * 24 * 3600 * 1000; // 7 days

  const sessionUser: UserSession = {
    token,
    id: DEMO_USER.id,
    username: DEMO_USER.id,
    name: DEMO_USER.name,
    role: DEMO_USER.role,
    avatar: DEMO_USER.avatar,
    title: DEMO_USER.title,
    loginTime: now,
    expiresAt
  };

  sessionStore.set(token, sessionUser);

  res.json({
    success: true,
    message: 'Login successful! Welcome, Administrator.',
    token,
    user: {
      id: sessionUser.id,
      username: sessionUser.username,
      name: sessionUser.name,
      role: sessionUser.role,
      avatar: sessionUser.avatar,
      title: sessionUser.title,
      loginTime: sessionUser.loginTime,
      expiresAt: sessionUser.expiresAt
    }
  });
});

// 3. Get Current Authenticated User Session
app.get('/api/auth/me', (req: Request, res: Response) => {
  const authHeader = req.headers.authorization || (req.headers['x-auth-token'] as string);
  const token = authHeader?.startsWith('Bearer ') ? authHeader.substring(7).trim() : authHeader?.trim();

  if (!token || !sessionStore.has(token)) {
    res.json({ authenticated: false, user: null });
    return;
  }

  const session = sessionStore.get(token)!;
  if (Date.now() > session.expiresAt) {
    sessionStore.delete(token);
    res.json({ authenticated: false, user: null });
    return;
  }

  res.json({
    authenticated: true,
    user: {
      id: session.id,
      username: session.username,
      name: session.name,
      role: session.role,
      avatar: session.avatar,
      title: session.title,
      loginTime: session.loginTime
    }
  });
});

// 4. Logout Endpoint
app.post('/api/auth/logout', (req: Request, res: Response) => {
  const authHeader = req.headers.authorization || (req.headers['x-auth-token'] as string);
  const token = authHeader?.startsWith('Bearer ') ? authHeader.substring(7).trim() : authHeader?.trim();

  if (token && sessionStore.has(token)) {
    sessionStore.delete(token);
  }

  res.json({ success: true, message: 'Logged out successfully.' });
});

// --- Health Check ---
app.get('/api/health', (req: Request, res: Response) => {
  res.json({ status: 'ok', service: 'CODE MIRCHI', version: '2.0' });
});

// --- Events API ---
app.get('/api/events', (req: Request, res: Response) => {
  const events = db.getAllEvents();
  res.json({ events, count: events.length });
});

app.post('/api/events', rateLimit(10, 60), (req: Request, res: Response) => {
  const data = req.body;
  if (!data) {
    res.status(400).json({ error: 'Invalid JSON payload' });
    return;
  }

  const name = String(data.name || '').trim();
  const start = String(data.start || '').trim();
  const end = String(data.end || '').trim();
  const url = String(data.url || '').trim();

  if (!name || !start || !end) {
    res.status(400).json({ error: 'Name, start date, and end date are required' });
    return;
  }

  if (name.length > 200) {
    res.status(400).json({ error: 'Event name exceeds 200 characters limit' });
    return;
  }

  if (url && url !== '#') {
    if (!url.startsWith('https://') && !url.startsWith('http://')) {
      res.status(400).json({ error: 'Event URL must start with http:// or https://' });
      return;
    }
    if (url.length > 500) {
      res.status(400).json({ error: 'Event URL exceeds 500 characters limit' });
      return;
    }
  }

  const cleanedData = {
    name,
    organizer: String(data.organizer || 'Student Chapter').trim().slice(0, 200),
    mode: String(data.mode || 'Offline').trim().slice(0, 50),
    city: String(data.city || 'Pan-India').trim().slice(0, 100),
    start: start.slice(0, 20),
    end: end.slice(0, 20),
    tags: data.tags || 'Innovation',
    url: url || '#',
    note: String(data.note || 'Verified opportunity').trim().slice(0, 500)
  };

  const eventId = db.addEvent(cleanedData);
  res.status(201).json({
    success: true,
    id: eventId,
    message: 'Hackathon added successfully'
  });
});

// --- Squad Up API ---
app.get('/api/squads', (req: Request, res: Response) => {
  const roleFilter = req.query.role as string | undefined;
  const hackathonFilter = req.query.hackathon as string | undefined;
  const squads = db.getAllSquads(roleFilter, hackathonFilter);
  res.json({ squads, count: squads.length });
});

app.post('/api/squads', rateLimit(10, 60), (req: Request, res: Response) => {
  const data = req.body;
  if (!data) {
    res.status(400).json({ error: 'Invalid JSON payload' });
    return;
  }

  const projectTitle = String(data.project_title || '').trim();
  const hackathonName = String(data.hackathon_name || '').trim();
  const leaderName = String(data.leader_name || '').trim();
  const description = String(data.description || '').trim();
  const contactValue = String(data.contact_value || '').trim();

  if (!projectTitle || !hackathonName || !leaderName || !description || !contactValue) {
    res.status(400).json({
      error: 'Project title, hackathon name, leader name, description, and contact info are required'
    });
    return;
  }

  if (projectTitle.length > 200) {
    res.status(400).json({ error: 'Project title exceeds 200 characters limit' });
    return;
  }
  if (hackathonName.length > 200) {
    res.status(400).json({ error: 'Hackathon name exceeds 200 characters limit' });
    return;
  }
  if (leaderName.length > 100) {
    res.status(400).json({ error: 'Leader name exceeds 100 characters limit' });
    return;
  }
  if (description.length > 1500) {
    res.status(400).json({ error: 'Description exceeds 1500 characters limit' });
    return;
  }

  let rolesNeeded = data.roles_needed;
  if (Array.isArray(rolesNeeded)) {
    rolesNeeded = rolesNeeded.map((r: any) => String(r).trim().slice(0, 50)).filter(Boolean).slice(0, 8);
  } else if (typeof rolesNeeded === 'string' && rolesNeeded.trim()) {
    rolesNeeded = rolesNeeded.split(',').map((r: string) => r.trim().slice(0, 50)).filter(Boolean).slice(0, 8);
  } else {
    rolesNeeded = ['Full-Stack Dev'];
  }

  let techStack = data.tech_stack;
  if (Array.isArray(techStack)) {
    techStack = techStack.map((t: any) => String(t).trim().slice(0, 50)).filter(Boolean).slice(0, 8);
  } else if (typeof techStack === 'string' && techStack.trim()) {
    techStack = techStack.split(',').map((t: string) => t.trim().slice(0, 50)).filter(Boolean).slice(0, 8);
  } else {
    techStack = ['React', 'Python'];
  }

  let currentMembers = Number(data.current_members) || 1;
  let teamSize = Number(data.team_size) || 4;
  currentMembers = Math.max(1, Math.min(10, currentMembers));
  teamSize = Math.max(currentMembers, Math.min(10, teamSize));

  let contactType = String(data.contact_type || 'Discord').trim();
  if (!['Discord', 'LinkedIn', 'Telegram', 'Email', 'GitHub', 'Twitter'].includes(contactType)) {
    contactType = 'Discord';
  }

  if (contactValue.toLowerCase().startsWith('javascript:') || contactValue.toLowerCase().startsWith('data:')) {
    res.status(400).json({ error: 'Invalid contact information provided' });
    return;
  }

  const cleanedData = {
    hackathon_id: String(data.hackathon_id || '').trim().slice(0, 100),
    hackathon_name: hackathonName,
    project_title: projectTitle,
    leader_name: leaderName,
    leader_college: String(data.leader_college || 'Campus Developer').trim().slice(0, 150),
    roles_needed: rolesNeeded,
    current_members: currentMembers,
    team_size: teamSize,
    tech_stack: techStack,
    description,
    contact_type: contactType,
    contact_value: contactValue.slice(0, 200),
    status: 'Open'
  };

  const squadId = db.addSquadPost(cleanedData);
  res.status(201).json({
    success: true,
    id: squadId,
    message: 'Squad pitch posted successfully'
  });
});

app.post('/api/squads/:squadId/toggle', rateLimit(30, 60), (req: Request, res: Response) => {
  const squadId = req.params.squadId;
  const newStatus = db.toggleSquadStatus(squadId);
  if (!newStatus) {
    res.status(404).json({ error: 'Squad post not found' });
    return;
  }
  res.json({ id: squadId, status: newStatus });
});

// --- Opportunities API ---
app.get('/api/opportunities', (req: Request, res: Response) => {
  const typeFilter = req.query.type as string | undefined;
  const batchFilter = req.query.batch as string | undefined;
  const categoryFilter = req.query.category as string | undefined;
  const searchQuery = req.query.q as string | undefined;
  const opps = db.getAllOpportunities(typeFilter, batchFilter, categoryFilter, searchQuery);
  res.json({ opportunities: opps, count: opps.length });
});

app.get('/api/opportunities/:oppId', (req: Request, res: Response) => {
  const opp = db.getOpportunityById(req.params.oppId);
  if (!opp) {
    res.status(404).json({ error: 'Opportunity not found' });
    return;
  }
  res.json(opp);
});

app.post('/api/opportunities', rateLimit(10, 60), (req: Request, res: Response) => {
  const data = req.body;
  if (!data) {
    res.status(400).json({ error: 'Invalid JSON payload' });
    return;
  }

  const company = String(data.company || '').trim();
  const roleTitle = String(data.role_title || data.title || '').trim();
  const applyUrl = String(data.apply_url || '').trim();
  const description = String(data.description || '').trim();

  if (!company || !roleTitle || !applyUrl) {
    res.status(400).json({ error: 'Company name, role title, and application URL are required' });
    return;
  }

  if (company.length > 100) {
    res.status(400).json({ error: 'Company name exceeds 100 characters' });
    return;
  }
  if (roleTitle.length > 200) {
    res.status(400).json({ error: 'Role title exceeds 200 characters' });
    return;
  }
  if (description.length > 2000) {
    res.status(400).json({ error: 'Description exceeds 2000 characters' });
    return;
  }

  if (!applyUrl.startsWith('http://') && !applyUrl.startsWith('https://')) {
    res.status(400).json({ error: 'Application URL must start with http:// or https://' });
    return;
  }

  let batches = data.eligible_batches || data.batches;
  if (Array.isArray(batches)) {
    batches = batches.map((b: any) => String(b).trim().slice(0, 30)).filter(Boolean).slice(0, 5);
  } else if (typeof batches === 'string' && batches.trim()) {
    batches = batches.split(',').map((b: string) => b.trim().slice(0, 30)).filter(Boolean).slice(0, 5);
  } else {
    batches = ['2026 Batch', '2027 Batch'];
  }

  let skills = data.skills;
  if (Array.isArray(skills)) {
    skills = skills.map((s: any) => String(s).trim().slice(0, 40)).filter(Boolean).slice(0, 8);
  } else if (typeof skills === 'string' && skills.trim()) {
    skills = skills.split(',').map((s: string) => s.trim().slice(0, 40)).filter(Boolean).slice(0, 8);
  } else {
    skills = ['DSA', 'Problem Solving'];
  }

  const cleanedData = {
    company,
    role_title: roleTitle,
    opportunity_type: String(data.opportunity_type || data.type || 'Summer Internship').trim().slice(0, 50),
    eligible_batches: batches,
    role_category: String(data.role_category || data.category || 'Software Engineering').trim().slice(0, 50),
    location: String(data.location || 'Pan-India / Remote').trim().slice(0, 100),
    stipend_or_ctc: String(data.stipend_or_ctc || data.stipend || 'Competitive').trim().slice(0, 50),
    apply_url: applyUrl.slice(0, 500),
    deadline: String(data.deadline || 'Rolling Apply').trim().slice(0, 50),
    description,
    skills,
    selection_process: String(data.selection_process || data.rounds || 'Online Assessment + Technical Interviews').trim().slice(0, 500),
    status: 'Active',
    featured: 0
  };

  const oppId = db.addOpportunity(cleanedData);
  res.status(201).json({
    success: true,
    id: oppId,
    message: 'Opportunity posted successfully'
  });
});

app.get('/api/saved-opportunities', (req: Request, res: Response) => {
  const savedIds = db.getSavedOpportunities();
  res.json({ saved: savedIds, saved_ids: savedIds, count: savedIds.length });
});

app.post('/api/saved-opportunities/:oppId/toggle', rateLimit(60, 60), (req: Request, res: Response) => {
  const saved = db.toggleSavedOpportunity(req.params.oppId);
  res.json({ opportunity_id: req.params.oppId, saved });
});

// --- Projects API ---
app.get('/api/projects', (req: Request, res: Response) => {
  const level = req.query.level as string | undefined;
  const domain = req.query.domain as string | undefined;
  const search = (req.query.search || req.query.q) as string | undefined;
  const projects = db.getAllProjects(level, domain, search);
  res.json({ projects, count: projects.length });
});

app.get('/api/projects/:projectId', (req: Request, res: Response) => {
  const proj = db.getProjectById(req.params.projectId);
  if (!proj) {
    res.status(404).json({ error: 'Project blueprint not found' });
    return;
  }
  res.json({ project: proj });
});

app.post('/api/projects', rateLimit(20, 60), (req: Request, res: Response) => {
  const data = req.body || {};
  const title = String(data.title || '').trim();
  const tagline = String(data.tagline || '').trim();
  const problem = String(data.problem_statement || '').trim();

  if (!title) {
    res.status(400).json({ error: 'Project title is required.' });
    return;
  }
  if (!problem && !tagline) {
    res.status(400).json({ error: 'Tagline or Problem Statement is required.' });
    return;
  }

  const newId = db.addProject(data);
  const created = db.getProjectById(newId);
  res.status(201).json({
    success: true,
    id: newId,
    project: created,
    message: 'Architecture Blueprint published to Community Vault!'
  });
});

app.get('/api/saved-projects', (req: Request, res: Response) => {
  const savedIds = db.getSavedProjects();
  res.json({ saved: savedIds, saved_ids: savedIds, count: savedIds.length });
});

app.post('/api/saved-projects/:projectId/toggle', rateLimit(60, 60), (req: Request, res: Response) => {
  const saved = db.toggleSavedProject(req.params.projectId);
  res.json({ project_id: req.params.projectId, saved });
});

// --- Bookmarks API ---
app.get('/api/saved-events', (req: Request, res: Response) => {
  const savedIds = db.getSavedEventIds();
  res.json({ saved: savedIds });
});

app.post('/api/saved-events/:eventId/toggle', rateLimit(60, 60), (req: Request, res: Response) => {
  const eventId = req.params.eventId;
  const saved = db.toggleSavedEvent(eventId);
  res.json({
    event_id: eventId,
    saved,
    message: saved ? 'Event saved' : 'Event removed from saved'
  });
});

// --- Resources API ---
app.get('/api/resources', (req: Request, res: Response) => {
  const category = (req.query.category as string) || 'all';
  const resources = db.getAllResources(category);
  res.json({ resources });
});

app.post('/api/resources/:resourceId/like', rateLimit(30, 60), (req: Request, res: Response) => {
  const resourceId = parseInt(req.params.resourceId, 10);
  const newLikes = db.likeResource(resourceId);
  res.json({ id: resourceId, likes: newLikes });
});

// --- Degrees & Roadmaps API ---
app.get('/api/degrees', (req: Request, res: Response) => {
  const degrees = db.getDegrees();
  const prefs = db.getUserPreferences();
  const selectedDegree = prefs.selected_degree || 'btech_cse';
  res.json({ degrees, selected_degree: selectedDegree });
});

app.get('/api/roadmap', (req: Request, res: Response) => {
  const prefs = db.getUserPreferences();
  const defaultDegree = prefs.selected_degree || 'btech_cse';
  const degreeId = (req.query.degree as string) || defaultDegree;
  const semesterNum = req.query.semester as string | undefined;

  const data = db.getDegreeRoadmap(degreeId, semesterNum);
  res.json(data);
});

app.post('/api/roadmap/toggle', rateLimit(60, 60), (req: Request, res: Response) => {
  const data = req.body || {};
  const taskId = data.task_id;
  const degreeId = data.degree_id || 'btech_cse';
  const semesterNum = data.semester_number;

  if (!taskId) {
    res.status(400).json({ error: 'task_id is required' });
    return;
  }

  const completed = data.completed;
  const newStatus = db.toggleTask(taskId, completed);
  const roadmapData = db.getDegreeRoadmap(degreeId, semesterNum);

  res.json({
    task_id: taskId,
    completed: newStatus,
    roadmap: roadmapData
  });
});

// --- Preferences API ---
app.all('/api/preferences', (req: Request, res: Response) => {
  if (req.method === 'POST') {
    const data = req.body || {};
    for (const [k, v] of Object.entries(data)) {
      db.setUserPreference(String(k).slice(0, 50), String(v).slice(0, 100));
    }
    res.json({ success: true, preferences: db.getUserPreferences() });
    return;
  }
  res.json(db.getUserPreferences());
});

// --- Global Stats API ---
app.get('/api/stats', (req: Request, res: Response) => {
  const degreeId = (req.query.degree as string) || 'btech_cse';
  const stats = db.getStats(degreeId);
  res.json(stats);
});

// --- Portfolio Samples & Builder API ---
app.get('/api/portfolio/sample', (req: Request, res: Response) => {
  const role = ((req.query.role as string) || 'fullstack').toLowerCase();
  const samples: Record<string, any> = {
    fullstack: {
      name: 'Arjun Mehta',
      role: 'Full-Stack & Distributed Systems Developer',
      tagline: 'Building high-throughput web architectures, real-time sync engines, and production APIs.',
      location: 'Bengaluru / Delhi NCR, India',
      available_for: 'Summer 2026 SDE Internship / 6-Month Co-op',
      github: 'https://github.com/arjunmehta-dev',
      linkedin: 'https://linkedin.com/in/arjunmehtadev',
      twitter: 'https://x.com/arjun_codes',
      email: 'arjun.mehta.codes@gmail.com',
      website: 'https://arjunmehta.dev',
      skills: {
        languages: ['TypeScript', 'Go (Golang)', 'Python', 'C++', 'SQL'],
        frameworks: ['React', 'Next.js', 'Node.js', 'FastAPI', 'TailwindCSS'],
        databases: ['PostgreSQL', 'Redis', 'MongoDB', 'ClickHouse'],
        devops: ['Docker', 'Kubernetes', 'AWS (S3/EC2)', 'Kafka', 'GitHub Actions', 'Prometheus']
      },
      projects: [
        {
          title: 'Distributed Rate Limiter & Reverse Proxy',
          description: 'High-throughput token-bucket & sliding-window edge proxy capable of throttling 100k+ req/sec with sub-millisecond atomic Lua operations in Redis.',
          stack: ['Go', 'Redis', 'Lua', 'Docker', 'Prometheus'],
          live_url: 'https://proxy.arjunmehta.dev',
          github_url: 'https://github.com/arjunmehta-dev/edge-rate-limiter',
          metric: 'Throttles 100k+ req/sec with p99 latency <1.4ms across 3 distributed nodes.'
        },
        {
          title: 'Real-Time Collaborative Canvas (CRDTs)',
          description: 'Multiplayer whiteboard supporting concurrent freehand drawing, sticky notes, and conflict-free real-time state synchronization using Yjs and WebSockets.',
          stack: ['TypeScript', 'React', 'Node.js', 'WebSockets', 'Yjs', 'Redis'],
          live_url: 'https://canvas.arjunmehta.dev',
          github_url: 'https://github.com/arjunmehta-dev/collab-canvas',
          metric: 'Maintains sub-50ms peer update propagation for 60+ simultaneous room participants.'
        },
        {
          title: 'UPI Microservices Payment Gateway Switch',
          description: 'Financial routing engine simulating high-availability UPI transactions with Saga distributed orchestrations, idempotency locks, and dead-letter queues.',
          stack: ['Java', 'Spring Boot', 'Kafka', 'PostgreSQL', 'Resilience4j'],
          live_url: 'https://pay.arjunmehta.dev',
          github_url: 'https://github.com/arjunmehta-dev/upi-switch',
          metric: 'Achieves zero double-debit anomalies across 50,000 simulated concurrent orders.'
        }
      ],
      education: {
        college: 'Delhi Technological University (DTU)',
        degree: 'B.Tech in Computer Science & Engineering',
        batch: '2022 - 2026',
        cgpa: '8.8 / 10.0',
        highlight: 'National Finalist, Smart India Hackathon 2024 • Top 1.5% in LeetCode (Knight, 1950+ Rating)'
      }
    },
    aiml: {
      name: 'Priya Sharma',
      role: 'AI/ML Systems & GenAI Research Engineer',
      tagline: 'Crafting cross-lingual RAG pipelines, fine-tuned transformer architectures, and low-latency inference endpoints.',
      location: 'Hyderabad / Pune, India',
      available_for: 'Summer 2027 AI Internship / Research Fellow',
      github: 'https://github.com/priyasharma-ai',
      linkedin: 'https://linkedin.com/in/priyasharma-ai',
      twitter: 'https://x.com/priya_ml',
      email: 'priya.sharma.ml@gmail.com',
      website: 'https://priyasharma.ai',
      skills: {
        languages: ['Python', 'C++', 'SQL', 'TypeScript'],
        frameworks: ['PyTorch', 'FastAPI', 'Hugging Face', 'LangChain', 'vLLM'],
        databases: ['pgvector', 'Qdrant', 'ChromaDB', 'PostgreSQL', 'Redis'],
        devops: ['Docker', 'Triton Server', 'MLflow', 'Weights & Biases', 'GCP Vertex AI']
      },
      projects: [
        {
          title: 'Multilingual Legal RAG Engine',
          description: 'Cross-lingual document question-answering system for Indian legal statutes & govt gazettes across Hindi, Tamil, Telugu, and English with verifiable citations.',
          stack: ['Python', 'FastAPI', 'pgvector', 'BGE-M3', 'Llama-3', 'Docker'],
          live_url: 'https://legal-rag.priyasharma.ai',
          github_url: 'https://github.com/priyasharma-ai/multilingual-rag',
          metric: 'Delivers 94.2% retrieval recall across 15,000 gazette pages with <850ms time-to-first-token.'
        },
        {
          title: 'Automated AST Code Vulnerability Auditor',
          description: 'Static analysis bot parsing syntax trees with Tree-sitter to detect OWASP security flaws, enriched with quantized local LLMs for suggested patches.',
          stack: ['Python', 'Tree-sitter', 'FastAPI', 'GitHub API', 'Ollama'],
          live_url: 'https://auditbot.priyasharma.ai',
          github_url: 'https://github.com/priyasharma-ai/ast-sec-bot',
          metric: 'Detected 32 zero-day regex injection risks in open-source collegiate repositories.'
        }
      ],
      education: {
        college: 'IIIT Hyderabad',
        degree: 'B.Tech in Artificial Intelligence & Machine Learning',
        batch: '2023 - 2027',
        cgpa: '9.1 / 10.0',
        highlight: 'Published undergraduate preprint on cross-lingual embedding quantization.'
      }
    }
  };
  res.json(samples[role] || samples.fullstack);
});

app.post('/api/portfolio/generate', rateLimit(30, 60), (req: Request, res: Response) => {
  const data = req.body || {};
  const name = data.name || 'Your Name';
  const role = data.role || 'Full-Stack Developer';
  const tagline = data.tagline || 'Building high-performance software and distributed systems.';
  const location = data.location || 'India';
  const github = data.github || 'https://github.com';
  const linkedin = data.linkedin || 'https://linkedin.com';
  const twitter = data.twitter || '';
  const email = data.email || 'developer@example.com';

  const skills = data.skills || {};
  const projects = data.projects || [];
  const education = data.education || {};

  const mdLines: string[] = [];
  mdLines.push(`# Hi there, I'm ${name} 👋`);
  mdLines.push(`### ${role} • 📍 ${location}\n`);
  mdLines.push(`> ${tagline}\n`);

  mdLines.push('## 📬 Connect With Me');
  const socialBadges: string[] = [];
  if (github) socialBadges.push(`[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](${github})`);
  if (linkedin) socialBadges.push(`[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](${linkedin})`);
  if (twitter) socialBadges.push(`[![X](https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white)](${twitter})`);
  if (email) socialBadges.push(`[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:${email})`);
  mdLines.push(socialBadges.join(' ') + '\n');

  mdLines.push('## 🛠️ Technical Skills');
  for (const [category, skillList] of Object.entries(skills)) {
    if (Array.isArray(skillList) && skillList.length > 0) {
      const formattedCat = category.charAt(0).toUpperCase() + category.slice(1);
      const skillsStr = skillList.map((s) => `\`${s}\``).join(' • ');
      mdLines.push(`- **${formattedCat}**: ${skillsStr}`);
    }
  }
  mdLines.push('');

  mdLines.push('## 🚀 Featured Engineering Projects');
  for (const p of projects) {
    const title = p.title || 'Project';
    const desc = p.description || '';
    const stackStr = Array.isArray(p.stack) ? p.stack.join(', ') : '';
    const metric = p.metric || '';
    const liveUrl = p.live_url || '';
    const repoUrl = p.github_url || '';

    mdLines.push(`### ⚡ [${title}](${liveUrl || repoUrl || '#'})`);
    mdLines.push(desc);
    if (metric) mdLines.push(`- 📈 **Key Metric / Impact**: ${metric}`);
    if (stackStr) mdLines.push(`- 🧩 **Tech Stack**: \`${stackStr}\``);

    const links: string[] = [];
    if (liveUrl) links.push(`[🌐 Live Demo](${liveUrl})`);
    if (repoUrl) links.push(`[💻 GitHub Repository](${repoUrl})`);
    if (links.length > 0) mdLines.push(`- 🔗 ${links.join(' | ')}`);
    mdLines.push('');
  }

  if (education && Object.keys(education).length > 0) {
    mdLines.push('## 🎓 Education & Credentials');
    const col = education.college || '';
    const deg = education.degree || '';
    const batch = education.batch || '';
    const cgpa = education.cgpa || '';
    const hl = education.highlight || '';
    mdLines.push(`- **${deg}** — ${col} (${batch})`);
    if (cgpa) mdLines.push(`- **Academic Score**: ${cgpa}`);
    if (hl) mdLines.push(`- **Notable Recognition**: ${hl}`);
    mdLines.push('');
  }

  mdLines.push('---\n*Generated with [CODE MIRCHI](https://launchpadindia.dev) • Built for ambitious Indian engineering students.*');

  res.json({
    success: true,
    markdown: mdLines.join('\n')
  });
});

// --- Resume ATS Analyzer API ---
app.post('/api/resume/analyze', rateLimit(40, 60), (req: Request, res: Response) => {
  const data = req.body || {};
  const text = String(data.text || '').trim();

  if (!text) {
    res.status(400).json({ error: 'No resume text provided for analysis' });
    return;
  }

  const lowerText = text.toLowerCase();
  const wordCount = text.split(/\s+/).filter(Boolean).length;

  // 1. Live URLs & Repos
  const hasGithub = /github\.com\/[a-zA-Z0-9_\-]+/.test(text);
  const hasLinkedin = /linkedin\.com\/in\/[a-zA-Z0-9_\-]+/.test(text);
  const liveDeployDomains = [
    'vercel.app', 'netlify.app', 'render.com', 'railway.app',
    'github.io', 'fly.dev', 'onrender.com', 'herokuapp.com', 'surge.sh', 'pages.dev'
  ];
  const foundLiveUrls = liveDeployDomains.filter((dom) => lowerText.includes(dom));
  const genericUrlMatches = text.match(/https?:\/\/[^\s<>"']+/g) || [];

  // 2. Action Verbs
  const strongVerbs = [
    'architected', 'engineered', 'designed', 'implemented', 'benchmarked',
    'containerized', 'reduced', 'accelerated', 'orchestrated', 'automated',
    'integrated', 'spearheaded', 'refactored', 'optimized', 'streamlined',
    'deployed', 'migrated', 'scaled', 'profiled', 'secured', 'constructed'
  ];
  const foundStrongVerbs = Array.from(new Set(strongVerbs.filter((v) => new RegExp(`\\b${v}\\b`).test(lowerText))));

  // Weak/Passive Verbs
  const weakVerbs = [
    'worked on', 'responsible for', 'helped in', 'assisted with',
    'learned', 'tried', 'participated in', 'involved in', 'handled basics', 'familiar with'
  ];
  const foundWeakVerbs = weakVerbs.filter((w) => lowerText.includes(w));

  // 3. Measurable Metrics (XYZ formula)
  const metricPatterns = [
    /\b\d+%\b/g,
    /\b\d+\+?\s?ms\b/g,
    /\b\d+k\+?\b/g,
    /\b\d+\s?(req\/s|rps|tps)\b/g,
    /\b(top\s\d+|rank\s\d+)\b/g,
    /\b\d+\+?\s?(users|teams|stars|forks|downloads)\b/g
  ];
  const foundMetrics: string[] = [];
  for (const pat of metricPatterns) {
    const matches = lowerText.match(pat);
    if (matches) foundMetrics.push(...matches);
  }

  // 4. Fresher Red Flags
  const redFlagTriggers: Record<string, RegExp[]> = {
    'High School Board / Roll No': [/\b(10th|12th|cbse|icse|matriculation|intermediate|ssc|hsc)\b/],
    'Declaration Clause': [/\bhereby declare\b/, /\btrue to the best of my knowledge\b/, /\bdeclaration\b/],
    'Personal Details Clutter': [/\bfather'?s? name\b/, /\bmarital status\b/, /\bdate of birth\b/, /\bd\.o\.b\b/, /\bpermanent address\b/],
    'Vague Hobbies': [/\bhobbies:? (listening to music|cricket|watching movies|reading books|travelling)\b/],
    'Skill Bars / Percentages': [/(proficiency:?\s?\d+%)/, /(rating:?\s?\d+\/10)/]
  };

  const foundRedFlags: string[] = [];
  for (const [label, patterns] of Object.entries(redFlagTriggers)) {
    for (const pat of patterns) {
      if (pat.test(lowerText)) {
        foundRedFlags.push(label);
        break;
      }
    }
  }

  // 5. ATS Section Headers
  const standardHeaders = ['education', 'experience', 'projects', 'skills', 'technical skills', 'achievements', 'certifications'];
  const foundHeaders = standardHeaders.filter((h) => lowerText.includes(h));

  // Score Calculation
  let scoreProof = 0;
  if (hasGithub) scoreProof += 10;
  if (hasLinkedin) scoreProof += 5;
  if (foundLiveUrls.length > 0 || genericUrlMatches.length >= 2) scoreProof += 10;
  scoreProof = Math.min(25, scoreProof);

  const scoreMetrics = Math.min(25, foundMetrics.length * 6 + (foundStrongVerbs.length >= 4 ? 5 : 0));
  let scoreVerbs = Math.min(25, foundStrongVerbs.length * 5 - foundWeakVerbs.length * 4);
  scoreVerbs = Math.max(0, scoreVerbs);

  let scoreStructure = 15;
  if (foundHeaders.length >= 3) scoreStructure += 10;
  if (foundRedFlags.length > 0) scoreStructure -= foundRedFlags.length * 5;
  scoreStructure = Math.max(0, Math.min(25, scoreStructure));

  let totalScore = scoreProof + scoreMetrics + scoreVerbs + scoreStructure;
  totalScore = Math.max(5, Math.min(100, totalScore));

  let grade = '';
  let badgeClass = '';
  let summary = '';

  if (totalScore >= 88) {
    grade = 'Top 5% Recruiter Magnet 🔥';
    badgeClass = 'grade-elite';
    summary = 'Exceptional fresher resume. Demonstrates live project proof, quantifiable XYZ impact metrics, and clean ATS parser formatting.';
  } else if (totalScore >= 72) {
    grade = 'Competitive Candidate ⚡';
    badgeClass = 'grade-competitive';
    summary = 'Solid baseline. Add 1-2 live deployed project URLs and replace passive phrasing with specific benchmarks.';
  } else if (totalScore >= 50) {
    grade = 'Needs Measurable Proof ⚠️';
    badgeClass = 'grade-warning';
    summary = 'Contains generic descriptions. Lacks verified live URLs or quantifiable scale metrics (%, ms, req/sec).';
  } else {
    grade = 'High ATS Rejection Risk 🚨';
    badgeClass = 'grade-danger';
    summary = 'Critical red flags detected. Contains high-school clutter or passive language that will get filtered out by modern ATS parsers.';
  }

  const bulletRewrites = [
    {
      weak: 'Worked on a food delivery app using React and Node.js.',
      strong: 'Architected a full-stack food delivery app with React and Node.js; cut checkout latency by 35% through Redis query caching.'
    },
    {
      weak: 'Responsible for machine learning model training and testing.',
      strong: 'Engineered a multilingual RAG pipeline using FastAPI and pgvector, achieving 94% retrieval accuracy across 5,000 documents.'
    },
    {
      weak: 'Made a chat application using socket programming.',
      strong: 'Implemented a real-time collaborative chat engine with WebSockets and Redis Pub/Sub, sustaining 1,500 concurrent connections at <45ms jitter.'
    }
  ];

  res.json({
    score: totalScore,
    grade,
    badge_class: badgeClass,
    summary,
    word_count: wordCount,
    breakdown: {
      proof_score: scoreProof,
      metrics_score: scoreMetrics,
      verbs_score: scoreVerbs,
      structure_score: scoreStructure
    },
    findings: {
      has_github: hasGithub,
      has_linkedin: hasLinkedin,
      live_urls_detected: foundLiveUrls.length > 0 || genericUrlMatches.length >= 2,
      strong_verbs_count: foundStrongVerbs.length,
      strong_verbs_list: foundStrongVerbs.slice(0, 6),
      weak_verbs_found: foundWeakVerbs,
      metrics_found_count: foundMetrics.length,
      red_flags: foundRedFlags
    },
    bullet_rewrites: bulletRewrites
  });
});

// --- Admin Database Backup Endpoints ---
app.post('/api/admin/backup', requireAdmin, rateLimit(5, 60), (req: Request, res: Response) => {
  const result = backup.createBackup();
  const statusCode = result.success ? 200 : 500;
  res.status(statusCode).json(result);
});

app.get('/api/admin/backups', requireAdmin, (req: Request, res: Response) => {
  const backups = backup.listBackups();
  res.json({ backups, count: backups.length });
});

// --- Redirects ---
app.get(['/roadmap', '/roadmap.html', '/roadmaps'], (req: Request, res: Response) => {
  res.redirect(302, '/degree-roadmaps');
});

// --- Specific SEO files ---
app.get('/robots.txt', (req: Request, res: Response) => {
  const p = path.resolve(process.cwd(), 'robots.txt');
  if (fs.existsSync(p)) {
    res.type('text/plain').sendFile(p);
  } else {
    res.type('text/plain').send('User-agent: *\nAllow: /\n');
  }
});

app.get('/sitemap.xml', (req: Request, res: Response) => {
  const p = path.resolve(process.cwd(), 'sitemap.xml');
  if (fs.existsSync(p)) {
    res.type('application/xml').sendFile(p);
  } else {
    res.status(404).send('Not found');
  }
});

// --- Static assets ---
const ALLOWED_EXTENSIONS = new Set(['.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.svg', '.webp', '.ico', '.json', '.xml', '.txt', '.woff', '.woff2']);
const DENIED_EXTENSIONS = new Set(['.db', '.py', '.sh', '.env', '.sqlite', '.sqlite3', '.bak', '.tar', '.gz', '.zip', '.md', '.log']);

app.get('*', (req: Request, res: Response) => {
  const reqPath = req.path.replace(/^\/+/, '');

  if (reqPath.startsWith('..') || reqPath.includes('backups') || reqPath.startsWith('.')) {
    res.status(403).json({ error: 'Access denied' });
    return;
  }

  const ext = path.extname(reqPath).toLowerCase();
  if (DENIED_EXTENSIONS.has(ext) || ['app.py', 'database.py', 'backup.py', 'run.sh', 'launchpad.db'].includes(reqPath)) {
    res.status(403).json({ error: 'Access to internal system files is forbidden' });
    return;
  }

  const localFilePath = path.resolve(process.cwd(), reqPath);

  if (ALLOWED_EXTENSIONS.has(ext) && fs.existsSync(localFilePath) && fs.statSync(localFilePath).isFile()) {
    res.sendFile(localFilePath);
    return;
  }

  // Fallback to index.html for SPA routing
  const indexPath = path.resolve(process.cwd(), 'index.html');
  if (fs.existsSync(indexPath)) {
    res.sendFile(indexPath);
  } else {
    res.status(404).send('Not found');
  }
});

// --- Background Backup Worker (every 12 hours) ---
setInterval(() => {
  try {
    backup.createBackup();
  } catch (e) {
    console.error('Scheduled backup error:', e);
  }
}, 12 * 3600 * 1000);

// --- Server Startup ---
app.listen(PORT, HOST, () => {
  console.log(`🌶️ CODE MIRCHI running on http://${HOST}:${PORT}`);
});
