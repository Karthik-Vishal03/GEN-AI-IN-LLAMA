import sqlite3

DB_PATH = "study_bot.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Single user profile table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY CHECK (id = 1),  -- ensure only one row
            name TEXT,
            goals TEXT,
            subjects TEXT,
            study_style TEXT
        )
    ''')

    # Chat messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Ensure user_profile row exists with id=1
    cursor.execute("INSERT OR IGNORE INTO user_profile (id) VALUES (1)")
    conn.commit()
    conn.close()

def get_user_profile():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, goals, subjects, study_style FROM user_profile WHERE id=1")
    row = cursor.fetchone()
    conn.close()
    if row and any(row):
        return {
            "name": row[0] or "",
            "goals": row[1] or "",
            "subjects": row[2] or "",
            "study_style": row[3] or ""
        }
    return {}

def update_user_profile(name=None, goals=None, subjects=None, study_style=None):
    profile = get_user_profile()
    # Merge existing data with new data if provided
    new_name = name if name else profile.get("name", "")
    new_goals = goals if goals else profile.get("goals", "")
    new_study_style = study_style if study_style else profile.get("study_style", "")

    # For subjects, append new ones to existing list avoiding duplicates
    existing_subjects = set(map(str.strip, profile.get("subjects", "").split(","))) if profile.get("subjects") else set()
    new_subjects = set(map(str.strip, subjects.split(","))) if subjects else set()
    merged_subjects = ", ".join(sorted(existing_subjects.union(new_subjects)))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE user_profile
        SET name=?, goals=?, subjects=?, study_style=?
        WHERE id=1
    """, (new_name, new_goals, merged_subjects, new_study_style))
    conn.commit()
    conn.close()

def save_chat_message(role, content):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO chat_history (role, content) VALUES (?, ?)
    """, (role, content))
    conn.commit()
    conn.close()

def get_chat_history(limit=20):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT role, content FROM chat_history ORDER BY id DESC LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    # Return in chronological order
    return [{"role": r[0], "content": r[1]} for r in reversed(rows)]
