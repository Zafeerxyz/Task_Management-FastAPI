import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent.parent / "task.db"

def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def create_table():
    connection = get_connection()
    connection.execute("""
                                CREATE TABLE IF NOT EXISTS tasks(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT NOT NULL,
                                description  TEXT,
                                status TEXT NOT NULL DEFAULT 'pending',
                                priority TEXT NOT NULL DEFAULT 'medium',
                                due_date TEXT
                                )
                                 """
    )
    connection.commit()
    connection.close()

    