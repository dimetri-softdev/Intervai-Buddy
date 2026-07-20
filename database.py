import hashlib
import sqlite3
from datetime import date

class DatabaseManager:
    def __init__(self, db_name="intervai_data.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.setup_tables()

    def create_auth_tables(self):
        """Creates the users table if it doesn't exist."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def register_user(self, username, password):
        """Hashes the password and saves the user to the database."""
        if not username or not password:
            return False, "Username and password cannot be empty."
            
        pwd_hash = hashlib.sha256(password.encode()).hexdigest()
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)", 
                (username.lower().strip(), pwd_hash)
            )
            self.conn.commit()
            return True, "Registration successful!"
        except sqlite3.IntegrityError:
            return False, "Username already taken."

    def authenticate_user(self, username, password):
        """Verifies credentials against the stored hash."""
        pwd_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id FROM users WHERE username = ? AND password_hash = ?", 
            (username.lower().strip(), pwd_hash)
        )
        user = cursor.fetchone()
        if user:
            return True, user[0]  # Returns True and the user_id
        return False, None

    def setup_tables(self):
        """Initializes all database tables at once."""
        # Call our new auth table creator
        self.create_auth_tables()
        
        # Table for overall user stats
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_stats (
                id INTEGER PRIMARY KEY,
                questions_answered INTEGER DEFAULT 0,
                sessions_completed INTEGER DEFAULT 0,
                current_streak INTEGER DEFAULT 0,
                last_active_date TEXT
            )
        ''')
        
        # Table for individual interview performance
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS interview_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_date TEXT,
                topic TEXT,
                overall_score REAL,
                ai_feedback TEXT
            )
        ''')
        
        # Initialize default user if table is empty
        self.cursor.execute("SELECT COUNT(*) FROM user_stats")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute(
                "INSERT INTO user_stats (questions_answered, sessions_completed, current_streak, last_active_date) VALUES (0, 0, 0, ?)",
                (str(date.today()),)
            )
        self.conn.commit()

    def get_user_stats(self):
        self.cursor.execute("SELECT questions_answered, sessions_completed, current_streak FROM user_stats WHERE id = 1")
        return self.cursor.fetchone()
        
    def close(self):
        self.conn.close()

# Test the setup when running this file directly
if __name__ == "__main__":
    db = DatabaseManager()
    print("Database initialized successfully!")
    print("Current Stats:", db.get_user_stats())
    db.close()