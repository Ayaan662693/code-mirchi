import os
import sqlite3
import shutil
import glob
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "launchpad.db")
BACKUPS_DIR = os.path.join(BASE_DIR, "backups")

def ensure_backup_dir():
    if not os.path.exists(BACKUPS_DIR):
        os.makedirs(BACKUPS_DIR, exist_ok=True)

def create_backup():
    """
    Safely creates an online, non-blocking backup of SQLite database using
    the official sqlite3 backup API. This ensures active transactions are
    safely handled without locking or corrupting the database.
    """
    ensure_backup_dir()

    if not os.path.exists(DB_FILE):
        return {"success": False, "error": "Database file does not exist"}

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"launchpad_backup_{timestamp}.db"
    backup_filepath = os.path.join(BACKUPS_DIR, backup_filename)

    try:
        # Connect to source database in read-only mode to prevent write locks
        src_conn = sqlite3.connect(f"file:{DB_FILE}?mode=ro", uri=True)
        dest_conn = sqlite3.connect(backup_filepath)

        with dest_conn:
            src_conn.backup(dest_conn, pages=100, sleep=0.01)

        dest_conn.close()
        src_conn.close()

        # Verify integrity of the backup
        verify_conn = sqlite3.connect(backup_filepath)
        cursor = verify_conn.cursor()
        cursor.execute("PRAGMA integrity_check;")
        integrity = cursor.fetchone()[0]
        verify_conn.close()

        if integrity != "ok":
            os.remove(backup_filepath)
            return {"success": False, "error": f"Backup integrity check failed: {integrity}"}

        size_bytes = os.path.getsize(backup_filepath)
        rotate_backups(keep=10)

        return {
            "success": True,
            "filename": backup_filename,
            "filepath": backup_filepath,
            "size_bytes": size_bytes,
            "timestamp": timestamp,
            "integrity": integrity
        }
    except Exception as e:
        if os.path.exists(backup_filepath):
            try:
                os.remove(backup_filepath)
            except OSError:
                pass
        return {"success": False, "error": str(e)}

def rotate_backups(keep=10):
    """
    Maintains a rolling window of recent backups, removing older ones
    to conserve storage space while preserving disaster recovery.
    """
    ensure_backup_dir()
    pattern = os.path.join(BACKUPS_DIR, "launchpad_backup_*.db")
    files = sorted(glob.glob(pattern))

    if len(files) > keep:
        to_delete = files[:len(files) - keep]
        for f in to_delete:
            try:
                os.remove(f)
            except OSError:
                pass

def list_backups():
    ensure_backup_dir()
    pattern = os.path.join(BACKUPS_DIR, "launchpad_backup_*.db")
    files = sorted(glob.glob(pattern), reverse=True)

    backups = []
    for f in files:
        fname = os.path.basename(f)
        size = os.path.getsize(f)
        mtime = datetime.fromtimestamp(os.path.getmtime(f)).strftime("%Y-%m-%d %H:%M:%S")
        backups.append({
            "filename": fname,
            "size_bytes": size,
            "modified": mtime
        })
    return backups

def restore_backup(backup_filepath):
    """
    Restores database from a verified backup snapshot.
    """
    if not os.path.exists(backup_filepath):
        return {"success": False, "error": "Specified backup file does not exist"}

    try:
        # Check integrity of backup before restoring
        test_conn = sqlite3.connect(backup_filepath)
        cur = test_conn.cursor()
        cur.execute("PRAGMA integrity_check;")
        check = cur.fetchone()[0]
        test_conn.close()

        if check != "ok":
            return {"success": False, "error": "Backup file failed integrity check"}

        # Create temporary pre-restore fallback copy
        temp_pre_restore = DB_FILE + ".pre_restore"
        if os.path.exists(DB_FILE):
            shutil.copy2(DB_FILE, temp_pre_restore)

        # Copy backup over current db
        shutil.copy2(backup_filepath, DB_FILE)

        if os.path.exists(temp_pre_restore):
            os.remove(temp_pre_restore)

        return {"success": True, "restored_from": backup_filepath}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import sys
    if "--backup" in sys.argv:
        res = create_backup()
        print("Backup Result:", res)
    elif "--list" in sys.argv:
        print("Existing Backups:")
        for b in list_backups():
            print(f" - {b['filename']} ({b['size_bytes']} bytes, {b['modified']})")
    elif "--restore" in sys.argv:
        if len(sys.argv) < 3:
            print("Usage: python3 backup.py --restore <filepath>")
        else:
            print("Restore Result:", restore_backup(sys.argv[2]))
    else:
        print("SQLite Automated Backup Utility")
        print("Commands: --backup, --list, --restore <file>")
