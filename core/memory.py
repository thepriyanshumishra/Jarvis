import sqlite3
import datetime
from typing import List, Dict, Optional

class Memory:
    def __init__(self, db_path: str = "jarvis.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        # Interaction Logs
        c.execute('''CREATE TABLE IF NOT EXISTS logs
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      timestamp TEXT,
                      role TEXT,
                      content TEXT)''')
        # Key-Value Store for Preferences
        c.execute('''CREATE TABLE IF NOT EXISTS kv_store
                     (key TEXT PRIMARY KEY,
                      value TEXT)''')
        conn.commit()
        conn.close()

    def add_log(self, role: str, content: str):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        timestamp = datetime.datetime.now().isoformat()
        c.execute("INSERT INTO logs (timestamp, role, content) VALUES (?, ?, ?)",
                  (timestamp, role, content))
        conn.commit()
        conn.close()

    def get_recent_logs(self, limit: int = 5) -> List[Dict[str, str]]:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT role, content FROM logs ORDER BY id DESC LIMIT ?", (limit,))
        rows = c.fetchall()
        conn.close()
        # Return in chronological order
        return [{"role": r[0], "content": r[1]} for r in reversed(rows)]

    def set_value(self, key: str, value: str):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO kv_store (key, value) VALUES (?, ?)", (key, value))
        conn.commit()
        conn.close()

    def get_value(self, key: str) -> Optional[str]:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT value FROM kv_store WHERE key=?", (key,))
        row = c.fetchone()
        conn.close()
        return row[0] if row else None
