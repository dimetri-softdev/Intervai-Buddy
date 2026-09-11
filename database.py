import hashlib
import sqlite3
from datetime import date


class DatabaseManager:

    def __init__(self, db_name="intervai_data.db"):
        # check_same_thread=False allows multi-threaded database calls from UI background threads
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.setup_tables()

    def create_auth_tables(self):
        """Creates the users table if it doesn't exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def register_user(self, username, password):
        """Hashes the password and registers a new user, initializing their stats row."""
        if not username or not password:
            return False, "Username and password cannot be empty."

        pwd_hash = hashlib.sha256(password.encode()).hexdigest()
        clean_username = username.lower().strip()
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (clean_username, pwd_hash),
            )
            user_id = self.cursor.lastrowid

            # Initialize individual user stats
            self.cursor.execute(
                "INSERT INTO user_stats (user_id, questions_answered,"
                " sessions_completed, current_streak, last_active_date) VALUES"
                " (?, 0, 0, 0, ?)",
                (user_id, str(date.today())),
            )
            self.conn.commit()
            return True, "Registration successful!"
        except sqlite3.IntegrityError:
            return False, "Username already taken."

    def authenticate_user(self, username, password):
        """Verifies credentials against the stored hash."""
        pwd_hash = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute(
            "SELECT id FROM users WHERE username = ? AND password_hash = ?",
            (username.lower().strip(), pwd_hash),
        )
        user = self.cursor.fetchone()
        if user:
            return True, user[0]
        return False, None

    def setup_tables(self):
        """Initializes all database tables mapped to user accounts."""
        self.create_auth_tables()

        # User Stats linked to user_id
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                questions_answered INTEGER DEFAULT 0,
                sessions_completed INTEGER DEFAULT 0,
                current_streak INTEGER DEFAULT 0,
                last_active_date TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)

        # Session Performance History linked to user_id
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS interview_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                session_date TEXT DEFAULT CURRENT_TIMESTAMP,
                topic TEXT,
                overall_score REAL,
                ai_feedback TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        self.conn.commit()

    def get_user_stats(self, user_id):
        """Fetches stats for the specified user."""
        self.cursor.execute(
            "SELECT questions_answered, sessions_completed, current_streak"
            " FROM user_stats WHERE user_id = ?",
            (user_id,),
        )
        result = self.cursor.fetchone()
        if not result:
            # Fallback insertion if user was created before schema update
            self.cursor.execute(
                "INSERT INTO user_stats (user_id, questions_answered,"
                " sessions_completed, current_streak, last_active_date) VALUES"
                " (?, 0, 0, 0, ?)",
                (user_id, str(date.today())),
            )
            self.conn.commit()
            return (0, 0, 0)
        return result

    def get_average_score(self, user_id):
        """Calculates average interview score for the user."""
        self.cursor.execute(
            "SELECT AVG(overall_score) FROM interview_history WHERE user_id ="
            " ?",
            (user_id,),
        )
        res = self.cursor.fetchone()[0]
        return round(res, 1) if res else 0.0

    def get_user_analytics(self, user_id):
        """Fetches aggregate metrics and recent session history mapped to interview_history."""
        # Query overall stats
        self.cursor.execute(
            """
            SELECT 
                COUNT(*), 
                COALESCE(ROUND(AVG(overall_score), 1), 0.0)
            FROM interview_history
            WHERE user_id = ?
        """,
            (user_id,),
        )
        total_sessions, avg_overall = self.cursor.fetchone()

        # Query stats totals from user_stats
        q_answered, s_completed, streak = self.get_user_stats(user_id)

        # Recent sessions history (last 5 entries)
        self.cursor.execute(
            """
            SELECT topic, overall_score, session_date 
            FROM interview_history 
            WHERE user_id = ?
            ORDER BY id DESC 
            LIMIT 5
        """,
            (user_id,),
        )
        recent_sessions = self.cursor.fetchall()

        return {
            "total_sessions": total_sessions,
            "questions_answered": q_answered,
            "current_streak": streak,
            "avg_overall": avg_overall,
            "recent_sessions": recent_sessions,
        }

    def save_interview_session(
        self, user_id, topic, score, feedback="", feedback_json=None
    ):
        """Saves a completed interview session and updates user stats.

        Accepts either 'feedback' or 'feedback_json' keyword arguments.
        """
        # Fallback to feedback_json if passed positionally or via legacy kwarg
        actual_feedback = feedback if feedback else (feedback_json or "")

        try:
            # 1. Insert the new session record
            self.cursor.execute(
                "INSERT INTO interview_history (user_id, topic, overall_score,"
                " ai_feedback) VALUES (?, ?, ?, ?)",
                (user_id, topic, score, actual_feedback),
            )

            # 2. Update the user's aggregate stats
            self.cursor.execute(
                "UPDATE user_stats SET questions_answered = questions_answered"
                " + 1, sessions_completed = sessions_completed + 1 WHERE"
                " user_id = ?",
                (user_id,),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database error during session save: {e}")

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    db = DatabaseManager()
    print("Database initialized successfully!")