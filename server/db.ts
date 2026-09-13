import { DatabaseSync } from 'node:sqlite';
import path from 'node:path';
import fs from 'node:fs';

const DB_PATH = path.resolve(process.cwd(), 'launchpad.db');

let dbInstance: DatabaseSync | null = null;

export function getDb(): DatabaseSync {
  if (!dbInstance) {
    dbInstance = new DatabaseSync(DB_PATH);
    dbInstance.exec('PRAGMA foreign_keys = ON;');
  }
  return dbInstance;
}

// --- Events Operations ---

export interface EventItem {
  id: string;
  name: string;
  organizer: string;
  city: string;
  mode: string;
  start: string;
  end: string;
  tags: string[];
  note: string;
  url: string;
}

export function getAllEvents(): EventItem[] {
  const db = getDb();
  const rows = db.prepare('SELECT * FROM events ORDER BY start_date ASC').all() as any[];
  return rows.map((r) => {
    let tags: string[] = [];
    try {
      tags = JSON.parse(r.tags || '[]');
    } catch {
      tags = [r.tags || 'Hackathon'];
    }
    return {
      id: r.id,
      name: r.name,
      organizer: r.organizer,
      city: r.city,
      mode: r.mode,
      start: r.start_date,
      end: r.end_date,
      tags,
      note: r.note || '',
      url: r.url || '#'
    };
  });
}

export function addEvent(data: Partial<EventItem>): string {
  const db = getDb();
  let eventId = data.id;
  if (!eventId) {
    const raw = (data.name || 'event').replace(/[^a-zA-Z0-9]/g, '-').toLowerCase().replace(/^-+|-+$/g, '');
    eventId = raw;
    const existing = db.prepare('SELECT id FROM events WHERE id = ?').get(eventId);
    if (existing) {
      eventId = `${eventId}-${Date.now()}`;
    }
  }

  let tagsArr = data.tags || [];
  if (typeof tagsArr === 'string') {
    tagsArr = (tagsArr as string).split(',').map((s) => s.trim()).filter(Boolean);
  }

  db.prepare(`
    INSERT INTO events (id, name, organizer, city, mode, start_date, end_date, tags, note, url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `).run(
    eventId,
    data.name || 'Untitled Event',
    data.organizer || 'Independent',
    data.city || 'Online',
    data.mode || 'Online',
    data.start || '',
    data.end || '',
    JSON.stringify(tagsArr),
    data.note || '',
    data.url || '#'
  );

  return eventId;
}

export function getSavedEventIds(): string[] {
  const db = getDb();
  const rows = db.prepare('SELECT event_id FROM saved_events').all() as any[];
  return rows.map((r) => r.event_id);
}

export function toggleSavedEvent(eventId: string): boolean {
  const db = getDb();
  const existing = db.prepare('SELECT event_id FROM saved_events WHERE event_id = ?').get(eventId);
  if (existing) {
    db.prepare('DELETE FROM saved_events WHERE event_id = ?').run(eventId);
    return false;
  } else {
    db.prepare('INSERT INTO saved_events (event_id) VALUES (?)').run(eventId);
    return true;
  }
}

// --- Squad Posts Operations ---

export interface SquadPost {
  id: string;
  hackathon_id: string;
  hackathon_name: string;
  project_title: string;
  leader_name: string;
  leader_college: string;
  roles_needed: string[];
  current_members: number;
  team_size: number;
  tech_stack: string[];
  description: string;
  contact_type: string;
  contact_value: string;
  status: string;
  created_at: string;
}

export function getAllSquads(roleFilter?: string | null, hackathonFilter?: string | null): SquadPost[] {
  const db = getDb();
  let query = 'SELECT * FROM squad_posts WHERE 1=1';
  const params: string[] = [];

  if (hackathonFilter && hackathonFilter.toLowerCase() !== 'all') {
    query += ' AND (LOWER(hackathon_id) LIKE ? OR LOWER(hackathon_name) LIKE ?)';
    const pat = `%${hackathonFilter.toLowerCase()}%`;
    params.push(pat, pat);
  }

  query += ' ORDER BY created_at DESC';
  const rows = (db.prepare(query).all(...params) as any[]);

  const results: SquadPost[] = [];
  for (const r of rows) {
    let rolesNeeded: string[] = [];
    let techStack: string[] = [];
    try {
      rolesNeeded = JSON.parse(r.roles_needed || '[]');
    } catch {
      rolesNeeded = [];
    }
    try {
      techStack = JSON.parse(r.tech_stack || '[]');
    } catch {
      techStack = [];
    }

    if (roleFilter && roleFilter.toLowerCase() !== 'all') {
      const rf = roleFilter.toLowerCase();
      const matches = rolesNeeded.some((role) => role.toLowerCase().includes(rf));
      if (!matches) continue;
    }

    results.push({
      id: r.id,
      hackathon_id: r.hackathon_id,
      hackathon_name: r.hackathon_name,
      project_title: r.project_title,
      leader_name: r.leader_name,
      leader_college: r.leader_college,
      roles_needed: rolesNeeded,
      current_members: r.current_members,
      team_size: r.team_size,
      tech_stack: techStack,
      description: r.description,
      contact_type: r.contact_type,
      contact_value: r.contact_value,
      status: r.status,
      created_at: r.created_at
    });
  }

  return results;
}

export function addSquadPost(data: any): string {
  const db = getDb();
  const postId = `squad-${Date.now()}`;
  const rolesJson = JSON.stringify(data.roles_needed || []);
  const techJson = JSON.stringify(data.tech_stack || []);

  db.prepare(`
    INSERT INTO squad_posts (
      id, hackathon_id, hackathon_name, project_title, leader_name,
      leader_college, roles_needed, current_members, team_size,
      tech_stack, description, contact_type, contact_value, status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `).run(
    postId,
    data.hackathon_id || '',
    data.hackathon_name || 'Open Hackathon',
    data.project_title || 'Untitled Project',
    data.leader_name || 'Student Leader',
    data.leader_college || 'Campus Developer',
    rolesJson,
    Number(data.current_members) || 1,
    Number(data.team_size) || 4,
    techJson,
    data.description || '',
    data.contact_type || 'Discord',
    data.contact_value || '',
    data.status || 'Open'
  );

  return postId;
}

export function toggleSquadStatus(squadId: string): string | null {
  const db = getDb();
  const row = db.prepare('SELECT status FROM squad_posts WHERE id = ?').get(squadId) as any;
  if (!row) return null;

  const newStatus = row.status === 'Open' ? 'Filled' : 'Open';
  db.prepare('UPDATE squad_posts SET status = ? WHERE id = ?').run(newStatus, squadId);
  return newStatus;
}

// --- Opportunities Operations ---

export interface OpportunityItem {
  id: string;
  company: string;
  role_title: string;
  opportunity_type: string;
  eligible_batches: string[];
  role_category: string;
  location: string;
  stipend_or_ctc: string;
  apply_url: string;
  deadline: string;
  description: string;
  skills: string[];
  selection_process: string;
  status: string;
  featured: number;
  created_at: string;
  title?: string;
  type?: string;
  category?: string;
  stipend?: string;
  rounds?: string;
}

function formatOpportunityRow(r: any): OpportunityItem {
  let eligibleBatches: string[] = [];
  let skills: string[] = [];
  try {
    eligibleBatches = JSON.parse(r.eligible_batches || '[]');
  } catch {
    eligibleBatches = [r.eligible_batches || '2026'];
  }
  try {
    skills = JSON.parse(r.skills || '[]');
  } catch {
    skills = [r.skills || 'DSA'];
  }

  return {
    ...r,
    eligible_batches: eligibleBatches,
    skills,
    title: r.role_title,
    type: r.opportunity_type,
    category: r.role_category,
    stipend: r.stipend_or_ctc,
    rounds: r.selection_process
  };
}

export function getAllOpportunities(
  typeFilter?: string | null,
  batchFilter?: string | null,
  categoryFilter?: string | null,
  searchQuery?: string | null
): OpportunityItem[] {
  const db = getDb();
  let query = 'SELECT * FROM opportunities WHERE 1=1';
  const params: string[] = [];

  if (typeFilter && typeFilter !== 'all') {
    query += ' AND LOWER(opportunity_type) LIKE LOWER(?)';
    params.push(`%${typeFilter}%`);
  }

  if (batchFilter && batchFilter !== 'all') {
    query += ' AND eligible_batches LIKE ?';
    params.push(`%${batchFilter}%`);
  }

  if (categoryFilter && categoryFilter !== 'all') {
    query += ' AND LOWER(role_category) LIKE LOWER(?)';
    params.push(`%${categoryFilter}%`);
  }

  if (searchQuery && searchQuery.trim()) {
    const term = `%${searchQuery.trim()}%`;
    query += ' AND (company LIKE ? OR role_title LIKE ? OR skills LIKE ? OR location LIKE ?)';
    params.push(term, term, term, term);
  }

  query += ' ORDER BY featured DESC, created_at DESC';
  const rows = db.prepare(query).all(...params) as any[];
  return rows.map(formatOpportunityRow);
}

export function getOpportunityById(oppId: string): OpportunityItem | null {
  const db = getDb();
  const row = db.prepare('SELECT * FROM opportunities WHERE id = ?').get(oppId) as any;
  if (!row) return null;
  return formatOpportunityRow(row);
}

export function addOpportunity(data: any): string {
  const db = getDb();
  const oppId = `opp-${Date.now()}`;
  let batches = data.eligible_batches || data.batches || ['2026'];
  if (typeof batches === 'string') {
    batches = batches.split(',').map((s: string) => s.trim()).filter(Boolean);
  }

  let skills = data.skills || ['DSA', 'Problem Solving'];
  if (typeof skills === 'string') {
    skills = skills.split(',').map((s: string) => s.trim()).filter(Boolean);
  }

  db.prepare(`
    INSERT INTO opportunities (
      id, company, role_title, opportunity_type, eligible_batches,
      role_category, location, stipend_or_ctc, apply_url, deadline,
      description, skills, selection_process, status, featured
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `).run(
    oppId,
    data.company || 'Tech Company',
    data.role_title || data.title || 'Software Engineering Intern',
    data.opportunity_type || data.type || 'Summer Internship',
    JSON.stringify(batches),
    data.role_category || data.category || 'Software Engineering',
    data.location || 'Pan-India / Remote',
    data.stipend_or_ctc || data.stipend || 'Competitive',
    data.apply_url || '#',
    data.deadline || 'Rolling Apply',
    data.description || '',
    JSON.stringify(skills),
    data.selection_process || data.rounds || 'Online Assessment + Technical Interview',
    data.status || 'Active',
    data.featured ? 1 : 0
  );

  return oppId;
}

export function getSavedOpportunities(): string[] {
  const db = getDb();
  const rows = db.prepare('SELECT opportunity_id FROM saved_opportunities ORDER BY saved_at DESC').all() as any[];
  return rows.map((r) => r.opportunity_id);
}

export function toggleSavedOpportunity(oppId: string): boolean {
  const db = getDb();
  const existing = db.prepare('SELECT opportunity_id FROM saved_opportunities WHERE opportunity_id = ?').get(oppId);
  if (existing) {
    db.prepare('DELETE FROM saved_opportunities WHERE opportunity_id = ?').run(oppId);
    return false;
  } else {
    db.prepare('INSERT INTO saved_opportunities (opportunity_id) VALUES (?)').run(oppId);
    return true;
  }
}

// --- Projects Operations ---

export interface ProjectItem {
  id: string;
  title: string;
  tagline: string;
  level: string;
  domain: string;
  problem_statement: string;
  target_audience: string;
  tech_stack: string[];
  architecture_diagram: string;
  components: any[];
  data_flow: string[];
  database_schema: string;
  interview_qa: any[];
  milestones: any[];
  github_starter_url: string;
  stars: number;
  featured: number;
  created_at: string;
  stack?: string[];
  diagram?: string;
  schema?: string;
  qa?: any[];
}

function formatProjectRow(r: any): ProjectItem {
  const parseJsonField = (val: any) => {
    if (typeof val === 'string') {
      try {
        return JSON.parse(val);
      } catch {
        return [];
      }
    }
    return val || [];
  };

  const techStack = parseJsonField(r.tech_stack);
  const components = parseJsonField(r.components);
  const dataFlow = parseJsonField(r.data_flow);
  const interviewQa = parseJsonField(r.interview_qa);
  const milestones = parseJsonField(r.milestones);

  return {
    ...r,
    tech_stack: techStack,
    components,
    data_flow: dataFlow,
    interview_qa: interviewQa,
    milestones,
    stack: techStack,
    diagram: r.architecture_diagram || '',
    schema: r.database_schema || '',
    qa: interviewQa
  };
}

export function getAllProjects(level?: string | null, domain?: string | null, search?: string | null): ProjectItem[] {
  const db = getDb();
  let query = 'SELECT * FROM projects WHERE 1=1';
  const params: string[] = [];

  if (level && !['all', 'all levels'].includes(level.toLowerCase())) {
    query += ' AND LOWER(level) = LOWER(?)';
    params.push(level);
  }

  if (domain && !['all', 'all domains'].includes(domain.toLowerCase())) {
    query += ' AND LOWER(domain) LIKE ?';
    params.push(`%${domain.toLowerCase()}%`);
  }

  if (search && search.trim()) {
    const pat = `%${search.toLowerCase().trim()}%`;
    query += ` AND (
      LOWER(title) LIKE ? OR
      LOWER(tagline) LIKE ? OR
      LOWER(problem_statement) LIKE ? OR
      LOWER(tech_stack) LIKE ? OR
      LOWER(domain) LIKE ?
    )`;
    params.push(pat, pat, pat, pat, pat);
  }

  query += ' ORDER BY featured DESC, stars DESC, created_at DESC';
  const rows = db.prepare(query).all(...params) as any[];
  return rows.map(formatProjectRow);
}

export function getProjectById(projectId: string): ProjectItem | null {
  const db = getDb();
  const row = db.prepare('SELECT * FROM projects WHERE id = ?').get(projectId) as any;
  if (!row) return null;
  return formatProjectRow(row);
}

export function addProject(data: any): string {
  const db = getDb();
  const projId = `proj-${Date.now()}`;

  let techStack = data.tech_stack || data.stack || ['React', 'Node.js'];
  if (typeof techStack === 'string') {
    techStack = techStack.split(',').map((s: string) => s.trim()).filter(Boolean);
  }

  let components = data.components || [];
  if (typeof components === 'string') {
    try {
      components = JSON.parse(components);
    } catch {
      components = [{ name: 'Core Service', role: components, tech: 'Standard' }];
    }
  }

  let dataFlow = data.data_flow || [];
  if (typeof dataFlow === 'string') {
    try {
      dataFlow = JSON.parse(dataFlow);
    } catch {
      dataFlow = dataFlow.split('\n').map((s: string) => s.trim()).filter(Boolean);
    }
  }

  let interviewQa = data.interview_qa || data.qa || [];
  if (typeof interviewQa === 'string') {
    try {
      interviewQa = JSON.parse(interviewQa);
    } catch {
      interviewQa = [];
    }
  }

  let milestones = data.milestones || [];
  if (typeof milestones === 'string') {
    try {
      milestones = JSON.parse(milestones);
    } catch {
      milestones = [{ phase: 'Phase 1', desc: milestones }];
    }
  }

  const tagline = data.tagline || data.summary || 'Production-grade distributed system blueprint';
  const archDiagram = data.architecture_diagram || data.diagram || data.system_diagram || '[Client] ---> [API Gateway] ---> [Microservice] ---> [Database]';
  const dbSchema = data.database_schema || data.schema || data.db_schema || '-- Primary schema\nCREATE TABLE records (id TEXT PRIMARY KEY);';
  const githubStarter = data.github_starter_url || data.github_sample || 'https://github.com';

  if (!components || components.length === 0) {
    components = [
      { name: 'Client Interface', role: 'Interactive user dashboard', tech: techStack[0] || 'React' },
      { name: 'Backend Service', role: 'Business logic execution and APIs', tech: techStack[1] || 'Node.js' },
      { name: 'Data Storage', role: 'Persistent storage and indexing', tech: techStack[2] || 'PostgreSQL' }
    ];
  }

  if (!dataFlow || dataFlow.length === 0) {
    dataFlow = [
      'Client issues authenticated request over HTTPS / WebSocket.',
      'API Gateway validates request, verifies rate limits, and routes to backend.',
      'Backend executes business logic and updates persistent storage.'
    ];
  }

  if (!milestones || milestones.length === 0) {
    milestones = [
      { phase: 'Phase 1', desc: 'Architecture design, schema definition, and container environment.' },
      { phase: 'Phase 2', desc: 'Core logic implementation and integration test suite.' },
      { phase: 'Phase 3', desc: 'Caching, worker queues, and performance benchmarking.' },
      { phase: 'Phase 4', desc: 'CI/CD pipeline and documentation deployment.' }
    ];
  }

  db.prepare(`
    INSERT INTO projects (
      id, title, tagline, level, domain, problem_statement,
      target_audience, tech_stack, architecture_diagram, components,
      data_flow, database_schema, interview_qa, milestones,
      github_starter_url, stars, featured
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `).run(
    projId,
    data.title || 'Untitled Architecture Blueprint',
    tagline,
    data.level || 'Intermediate',
    data.domain || 'Full-Stack',
    data.problem_statement || '',
    data.target_audience || 'Engineering Students & Freshers',
    JSON.stringify(techStack),
    archDiagram,
    JSON.stringify(components),
    JSON.stringify(dataFlow),
    dbSchema,
    JSON.stringify(interviewQa),
    JSON.stringify(milestones),
    githubStarter,
    0,
    data.featured ? 1 : 0
  );

  return projId;
}

export function getSavedProjects(): string[] {
  const db = getDb();
  const rows = db.prepare('SELECT project_id FROM saved_projects ORDER BY saved_at DESC').all() as any[];
  return rows.map((r) => r.project_id);
}

export function toggleSavedProject(projectId: string): boolean {
  const db = getDb();
  const existing = db.prepare('SELECT project_id FROM saved_projects WHERE project_id = ?').get(projectId);
  if (existing) {
    db.prepare('DELETE FROM saved_projects WHERE project_id = ?').run(projectId);
    return false;
  } else {
    db.prepare('INSERT INTO saved_projects (project_id) VALUES (?)').run(projectId);
    return true;
  }
}

// --- Resources Operations ---

export function getAllResources(category?: string | null): any[] {
  const db = getDb();
  if (category && category !== 'all') {
    return db.prepare('SELECT * FROM resources WHERE category = ? ORDER BY id ASC').all(category) as any[];
  }
  return db.prepare('SELECT * FROM resources ORDER BY id ASC').all() as any[];
}

export function likeResource(resourceId: number): number {
  const db = getDb();
  db.prepare('UPDATE resources SET likes = likes + 1 WHERE id = ?').run(resourceId);
  const row = db.prepare('SELECT likes FROM resources WHERE id = ?').get(resourceId) as any;
  return row ? row.likes : 0;
}

// --- Degree & Semester Roadmap Operations ---

export function getDegrees(): any[] {
  const db = getDb();
  return db.prepare('SELECT * FROM degrees').all() as any[];
}

export function getDegreeRoadmap(degreeId = 'btech_cse', semesterNum?: string | number | null): any {
  const db = getDb();

  let degreeRow = db.prepare('SELECT * FROM degrees WHERE id = ?').get(degreeId) as any;
  if (!degreeRow) {
    degreeId = 'btech_cse';
    degreeRow = db.prepare('SELECT * FROM degrees WHERE id = ?').get(degreeId) as any;
  }

  const semesterRows = db.prepare(`
    SELECT * FROM roadmap_semesters
    WHERE degree_id = ?
    ORDER BY semester_number ASC
  `).all(degreeId) as any[];

  const allTasks = db.prepare(`
    SELECT t.*, rs.degree_id, rs.semester_number
    FROM roadmap_tasks t
    JOIN roadmap_semesters rs ON t.semester_id = rs.id
    WHERE rs.degree_id = ?
    ORDER BY t.task_order ASC
  `).all(degreeId) as any[];

  const progressRows = db.prepare('SELECT task_id, completed FROM user_progress').all() as any[];
  const progressMap: Record<string, boolean> = {};
  for (const r of progressRows) {
    progressMap[r.task_id] = Boolean(r.completed);
  }

  const totalDegreeTasks = allTasks.length;
  const completedDegreeTasks = allTasks.filter((t) => progressMap[t.id]).length;

  const semesters: any[] = [];
  for (const sRow of semesterRows) {
    const semTasks: any[] = [];
    for (const t of allTasks) {
      if (t.semester_id === sRow.id) {
        semTasks.append ? null : semTasks.push({
          id: t.id,
          order: t.task_order,
          text: t.task_text,
          category: t.category,
          completed: Boolean(progressMap[t.id])
        });
      }
    }

    const semCompleted = semTasks.filter((st) => st.completed).length;
    const semTotal = semTasks.length;
    const semPercent = semTotal > 0 ? Math.round((semCompleted / semTotal) * 100) : 0;

    let focusAreas: string[] = [];
    try {
      focusAreas = JSON.parse(sRow.focus_areas || '[]');
    } catch {
      focusAreas = [];
    }

    semesters.push({
      id: sRow.id,
      year: sRow.year,
      semester_number: sRow.semester_number,
      title: sRow.title,
      focus_areas: focusAreas,
      academic_core: sRow.academic_core,
      industry_prep: sRow.industry_prep,
      milestone: sRow.milestone,
      tasks: semTasks,
      tasks_count: semTotal,
      completed_count: semCompleted,
      progress_percent: semPercent
    });
  }

  const overallProgress = totalDegreeTasks > 0 ? Math.round((completedDegreeTasks / totalDegreeTasks) * 100) : 0;

  let activeSemester: any = null;
  if (semesterNum) {
    const sNum = Number(semesterNum);
    if (!isNaN(sNum)) {
      activeSemester = semesters.find((s) => s.semester_number === sNum);
    }
  }

  if (!activeSemester && semesters.length > 0) {
    activeSemester = semesters[0];
  }

  return {
    degree: degreeRow,
    semesters,
    active_semester: activeSemester,
    overall_stats: {
      total_tasks: totalDegreeTasks,
      completed_tasks: completedDegreeTasks,
      progress_percent: overallProgress
    }
  };
}

export function toggleTask(taskId: string, completed?: boolean | null): boolean {
  const db = getDb();
  const row = db.prepare('SELECT completed FROM user_progress WHERE task_id = ?').get(taskId) as any;

  let newVal: boolean;
  if (!row) {
    newVal = completed === undefined || completed === null ? true : Boolean(completed);
    db.prepare('INSERT INTO user_progress (task_id, completed) VALUES (?, ?)').run(taskId, newVal ? 1 : 0);
  } else {
    newVal = completed === undefined || completed === null ? !row.completed : Boolean(completed);
    db.prepare('UPDATE user_progress SET completed = ?, updated_at = CURRENT_TIMESTAMP WHERE task_id = ?').run(
      newVal ? 1 : 0,
      taskId
    );
  }

  return newVal;
}

// --- Preferences Operations ---

export function setUserPreference(key: string, value: any): void {
  const db = getDb();
  db.prepare(`
    INSERT INTO user_preferences (key, value) VALUES (?, ?)
    ON CONFLICT(key) DO UPDATE SET value = excluded.value
  `).run(key, String(value));
}

export function getUserPreferences(): Record<string, string> {
  const db = getDb();
  const rows = db.prepare('SELECT key, value FROM user_preferences').all() as any[];
  const prefs: Record<string, string> = {};
  for (const r of rows) {
    prefs[r.key] = r.value;
  }
  return prefs;
}

// --- Global Stats ---

export function getStats(degreeId = 'btech_cse') {
  const db = getDb();
  const totalEvents = (db.prepare('SELECT COUNT(*) as count FROM events').get() as any).count;
  const savedCount = (db.prepare('SELECT COUNT(*) as count FROM saved_events').get() as any).count;

  const degreeData = getDegreeRoadmap(degreeId);
  const overallStats = degreeData.overall_stats;

  return {
    total_events: totalEvents,
    saved_count: savedCount,
    total_tasks: overallStats.total_tasks,
    completed_tasks: overallStats.completed_tasks,
    progress_percent: overallStats.progress_percent,
    degree_id: degreeId
  };
}
