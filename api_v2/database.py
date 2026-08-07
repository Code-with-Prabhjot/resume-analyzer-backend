import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'v2_history.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            provider TEXT NOT NULL,
            provider_token TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    
    # Analysis History Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            analysis_id TEXT NOT NULL UNIQUE,
            timestamp TEXT NOT NULL,
            overall_score REAL NOT NULL,
            skills_found TEXT NOT NULL,
            skills_missing TEXT NOT NULL,
            roadmap TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_or_create_user(provider, token):
    """
    Creates a new user if the token doesn't exist, otherwise returns existing user_id.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT user_id FROM users WHERE provider_token = ?', (token,))
    row = cursor.fetchone()
    
    if row:
        user_id = row['user_id']
    else:
        import uuid
        user_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + "Z"
        cursor.execute('''
            INSERT INTO users (user_id, provider, provider_token, created_at)
            VALUES (?, ?, ?, ?)
        ''', (user_id, provider, token, timestamp))
        conn.commit()
    
    conn.close()
    return user_id

def get_missing_skills_for_analysis(analysis_id):
    """
    Fetches the skills_missing array for a specific analysis run.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT skills_missing FROM analysis_history WHERE analysis_id = ?', (analysis_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return json.loads(row['skills_missing'])
    return []

def save_analysis_result(user_id, data):
    """
    Saves an analysis result to the database.
    'data' should be a dict containing:
    - analysis_id
    - overall_score
    - skills_found (list)
    - skills_missing (list)
    - roadmap (dict)
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    cursor.execute('''
        INSERT INTO analysis_history (user_id, analysis_id, timestamp, overall_score, skills_found, skills_missing, roadmap)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        data['analysis_id'],
        timestamp,
        data['overall_score'],
        json.dumps(data['skills_found']),
        json.dumps(data['skills_missing']),
        json.dumps(data['roadmap'])
    ))
    
    conn.commit()
    conn.close()

def get_user_history_from_db(user_id):
    """
    Fetches chronological history for a user from the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT analysis_id, timestamp as date, overall_score 
        FROM analysis_history 
        WHERE user_id = ? 
        ORDER BY timestamp DESC
    ''', (user_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]
    
# Initialize database table on module load
init_db()
