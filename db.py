import sqlite3

DATABASE = 'positive_log_db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS logs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                context TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()

def save_log(context):
    with get_db() as db:
        db.execute('INSERT INTO logs (context) VALUES (?)', (context,))
        db.commit()

def get_all_logs():
    with get_db() as db:
        return db.execute('SELECT * FROM logs ORDER BY created_at DESC').fetchall()
    
