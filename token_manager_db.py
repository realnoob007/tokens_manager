import sqlite3
import datetime

DATABASE_FILE = 'tokens.db'

def init_db():
    with sqlite3.connect(DATABASE_FILE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS tokens
                     (token TEXT PRIMARY KEY, expiration_date DATE)''')

def add_token(token, validity_days):
    expiration_date = (datetime.date.today() + datetime.timedelta(days=validity_days)).isoformat()
    with sqlite3.connect(DATABASE_FILE) as conn:
        conn.execute("INSERT OR REPLACE INTO tokens (token, expiration_date) VALUES (?, ?)", 
                     (token, expiration_date))

def delete_token(token):
    with sqlite3.connect(DATABASE_FILE) as conn:
        conn.execute("DELETE FROM tokens WHERE token = ?", (token,))

def get_tokens_details():
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.execute("SELECT token, expiration_date FROM tokens")
        today = datetime.date.today()
        return {row[0]: {"created_at": row[1], "expires_in": (datetime.date.fromisoformat(row[1]) - today).days} for row in cursor}

def get_token_detail(token):
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.execute("SELECT token, expiration_date FROM tokens WHERE token = ?", (token,))
        row = cursor.fetchone()
        if row:
            today = datetime.date.today()
            return {"token": row[0], "created_at": row[1], "expires_in": (datetime.date.fromisoformat(row[1]) - today).days}
        return None

def cleanup_tokens():
    with sqlite3.connect(DATABASE_FILE) as conn:
        today = datetime.date.today().isoformat()
        conn.execute("DELETE FROM tokens WHERE expiration_date < ?", (today,))

# Initialize the database when the module is loaded
init_db()
