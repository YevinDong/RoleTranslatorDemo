import sqlite3
import threading
from contextlib import contextmanager


class SqlManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._local = threading.local()
        self._lock = threading.Lock()
        self._migration()

    def _get_connection(self):
        """Get thread-local connection"""
        if not hasattr(self._local, 'connection'):
            self._local.connection = sqlite3.connect(
                self.db_path, check_same_thread=False)
        return self._local.connection

    @contextmanager
    def _get_cursor(self):
        """Context manager for database cursor"""
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()

    def _migration(self):
        """Initialize database schema"""
        with self._get_cursor() as cursor:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS role_classifier_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id  TEXT NOT NULL,
                json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            cursor.execute(
                'CREATE INDEX IF NOT EXISTS idx_thread ON role_classifier_history(thread_id)')

    def inset_role_classifier_history(self, thread_id: str, json: str):
        """Insert role classifier history"""
        with self._get_cursor() as cursor:
            cursor.execute('''
            INSERT INTO role_classifier_history (thread_id, json) VALUES (?, ?)
            ''', (thread_id, json))

    def get_role_classifier_history(self, thread_id: str, limit: int = 10):
        """Get role classifier history for a thread"""
        with self._get_cursor() as cursor:
            cursor.execute('''
            SELECT * FROM role_classifier_history WHERE thread_id = ? ORDER BY created_at DESC LIMIT ?
            ''', (thread_id, limit))
            return cursor.fetchall()


sql_manager = SqlManager("local_sql.db")
