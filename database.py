import hashlib
import sqlite3
from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./career_copilot.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class DatabaseManager:
    def __init__(self, db_name="intervai_data.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.setup_tables()

    def create_auth_tables(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    def register_user(self, username, password):
        if not username or not password:
            return False, "Username and password cannot be empty."

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        clean_username = username.lower().strip()
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (clean_username, password_hash),
            )
            user_id = self.cursor.lastrowid
            self.cursor.execute(
                "INSERT INTO user_stats "
                "(user_id, questions_answered, sessions_completed, "
                "current_streak, last_active_date) VALUES (?, 0, 0, 0, ?)",
                (user_id, str(date.today())),
            )
            self.conn.commit()
            return True, "Registration successful!"
        except sqlite3.IntegrityError:
            return False, "Username already taken."

    def authenticate_user(self, username, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute(
            "SELECT id FROM users WHERE username = ? AND password_hash = ?",
            (username.lower().strip(), password_hash),
        )
        user = self.cursor.fetchone()
        return (True, user[0]) if user else (False, None)

    def setup_tables(self):
        self.create_auth_tables()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                questions_answered INTEGER DEFAULT 0,
                sessions_completed INTEGER DEFAULT 0,
                current_streak INTEGER DEFAULT 0,
                last_active_date TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS interview_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                session_date TEXT DEFAULT CURRENT_TIMESTAMP,
                topic TEXT,
                overall_score REAL,
                ai_feedback TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """
        )
        self.conn.commit()

    def get_user_stats(self, user_id):
        self.cursor.execute(
            "SELECT questions_answered, sessions_completed, current_streak "
            "FROM user_stats WHERE user_id = ?",
            (user_id,),
        )
        result = self.cursor.fetchone()
        if result:
            return result

        self.cursor.execute(
            "INSERT INTO user_stats "
            "(user_id, questions_answered, sessions_completed, "
            "current_streak, last_active_date) VALUES (?, 0, 0, 0, ?)",
            (user_id, str(date.today())),
        )
        self.conn.commit()
        return (0, 0, 0)

    def get_average_score(self, user_id):
        self.cursor.execute(
            "SELECT AVG(overall_score) FROM interview_history WHERE user_id = ?",
            (user_id,),
        )
        average = self.cursor.fetchone()[0]
        return round(average, 1) if average else 0.0

    def get_user_analytics(self, user_id):
        self.cursor.execute(
            """
            SELECT COUNT(*), COALESCE(ROUND(AVG(overall_score), 1), 0.0)
            FROM interview_history
            WHERE user_id = ?
            """,
            (user_id,),
        )
        total_sessions, average_score = self.cursor.fetchone()
        questions_answered, _, current_streak = self.get_user_stats(user_id)
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
        return {
            "total_sessions": total_sessions,
            "questions_answered": questions_answered,
            "current_streak": current_streak,
            "avg_overall": average_score,
            "recent_sessions": self.cursor.fetchall(),
        }

    def get_interview_type_analytics(self, user_id):
        self.cursor.execute(
            """
            SELECT topic, COUNT(*), COALESCE(ROUND(AVG(overall_score), 1), 0.0)
            FROM interview_history
            WHERE user_id = ?
            GROUP BY topic
            """,
            (user_id,),
        )
        return {
            topic: {"sessions": session_count, "average_score": average_score}
            for topic, session_count, average_score in self.cursor.fetchall()
        }

    def save_interview_session(
        self, user_id, topic, score, feedback="", feedback_json=None
    ):
        actual_feedback = feedback or feedback_json or ""
        self.cursor.execute(
            "INSERT INTO interview_history "
            "(user_id, topic, overall_score, ai_feedback) VALUES (?, ?, ?, ?)",
            (user_id, topic, score, actual_feedback),
        )
        self.cursor.execute(
            "UPDATE user_stats SET questions_answered = questions_answered + 1, "
            "sessions_completed = sessions_completed + 1 WHERE user_id = ?",
            (user_id,),
        )
        self.conn.commit()

    def close(self):
        self.conn.close()