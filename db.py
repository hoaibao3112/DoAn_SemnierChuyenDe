# Copilot Directives:
# - SQLite file "sentiments.db".
# - Create table IF NOT EXISTS with columns:
#   (id INTEGER PK AUTOINCREMENT, text TEXT NOT NULL,
#    sentiment TEXT NOT NULL, score REAL, timestamp TEXT NOT NULL)
# - Functions:
#   add_record(text, sentiment, score) -> None
#   list_latest(limit:int=50) -> List[Tuple]
#   clear_all() -> None
# - Always use parameterized queries (?) and context managers.

import sqlite3
from datetime import datetime
from typing import List, Tuple

DB_FILE = "sentiments.db"

def init_db():
    """
    Initialize the SQLite database and create the table if it doesn't exist.
    """
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sentiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                sentiment TEXT NOT NULL,
                score REAL NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        conn.commit()


def add_record(text: str, sentiment: str, score: float) -> None:
    """
    Add a new sentiment record to the database.
    
    Args:
        text: Normalized input text
        sentiment: Predicted sentiment (POSITIVE/NEUTRAL/NEGATIVE)
        score: Confidence score
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sentiments (text, sentiment, score, timestamp) VALUES (?, ?, ?, ?)",
            (text, sentiment, score, timestamp)
        )
        conn.commit()


def list_latest(limit: int = 50) -> List[Tuple]:
    """
    Retrieve the latest N records from the database.
    
    Args:
        limit: Maximum number of records to return
        
    Returns:
        List of tuples (id, text, sentiment, score, timestamp)
    """
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, text, sentiment, score, timestamp FROM sentiments ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        return cursor.fetchall()


def clear_all() -> None:
    """
    Delete all records from the database (for testing purposes).
    """
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sentiments")
        conn.commit()
