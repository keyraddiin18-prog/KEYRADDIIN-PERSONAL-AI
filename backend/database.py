import sqlite3
import os

DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    os.path.join(os.path.dirname(__file__), "keyraddiin_ai.db")
)


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    # Chat history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # AI memory table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            memory_key TEXT NOT NULL,
            memory_value TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_message(session_id, role, message):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO chat_history
        (session_id, role, message)
        VALUES (?, ?, ?)
    """, (session_id, role, message))

    connection.commit()
    connection.close()


def get_chat_history(session_id, limit=50):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT role, message, created_at
        FROM chat_history
        WHERE session_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (session_id, limit))

    rows = cursor.fetchall()
    connection.close()

    return [dict(row) for row in reversed(rows)]


def save_memory(memory_key, memory_value):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO ai_memory
        (memory_key, memory_value)
        VALUES (?, ?)
    """, (memory_key, memory_value))

    connection.commit()
    connection.close()


def get_all_memories():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT memory_key, memory_value
        FROM ai_memory
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    connection.close()

    return [dict(row) for row in rows]


def delete_memory(memory_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM ai_memory WHERE id = ?",
        (memory_id,)
    )

    connection.commit()
    connection.close()