import fs from 'node:fs';
import path from 'node:path';

const DB_FILE = path.resolve(process.cwd(), 'launchpad.db');
const BACKUPS_DIR = path.resolve(process.cwd(), 'backups');

export function ensureBackupDir(): void {
  if (!fs.existsSync(BACKUPS_DIR)) {
    fs.mkdirSync(BACKUPS_DIR, { recursive: true });
  }
}

export function rotateBackups(keep = 10): void {
  ensureBackupDir();
  try {
    const files = fs
      .readdirSync(BACKUPS_DIR)
      .filter((f) => f.startsWith('launchpad_backup_') && f.endsWith('.db'))
      .sort();

    if (files.length > keep) {
      const toDelete = files.slice(0, files.length - keep);
      for (const f of toDelete) {
        try {
          fs.unlinkSync(path.join(BACKUPS_DIR, f));
        } catch {}
      }
    }
  } catch {}
}

export function createBackup(): {
  success: boolean;
  filename?: string;
  filepath?: string;
  size_bytes?: number;
  timestamp?: string;
  error?: string;
} {
  ensureBackupDir();

  if (!fs.existsSync(DB_FILE)) {
    return { success: false, error: 'Database file does not exist' };
  }

  const now = new Date();
  const pad = (n: number) => String(n).padStart(2, '0');
  const timestamp = `${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}_${pad(now.getHours())}${pad(now.getMinutes())}${pad(now.getSeconds())}`;
  const backupFilename = `launchpad_backup_${timestamp}.db`;
  const backupFilepath = path.join(BACKUPS_DIR, backupFilename);

  try {
    fs.copyFileSync(DB_FILE, backupFilepath);
    const stat = fs.statSync(backupFilepath);

    rotateBackups(10);

    return {
      success: true,
      filename: backupFilename,
      filepath: backupFilepath,
      size_bytes: stat.size,
      timestamp
    };
  } catch (err: any) {
    if (fs.existsSync(backupFilepath)) {
      try {
        fs.unlinkSync(backupFilepath);
      } catch {}
    }
    return { success: false, error: err.message };
  }
}

export function listBackups(): Array<{
  filename: string;
  size_bytes: number;
  modified: string;
}> {
  ensureBackupDir();
  try {
    const files = fs
      .readdirSync(BACKUPS_DIR)
      .filter((f) => f.startsWith('launchpad_backup_') && f.endsWith('.db'))
      .sort()
      .reverse();

    return files.map((f) => {
      const fullPath = path.join(BACKUPS_DIR, f);
      const stat = fs.statSync(fullPath);
      return {
        filename: f,
        size_bytes: stat.size,
        modified: stat.mtime.toISOString().replace('T', ' ').slice(0, 19)
      };
    });
  } catch {
    return [];
  }
}
