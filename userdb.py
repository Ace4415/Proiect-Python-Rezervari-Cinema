import sqlite3

DB_NAME = "users.db"



def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                is_admin INTEGER DEFAULT 0,
                must_change_password INTEGER DEFAULT 0
            )
        """
        )
        conn.commit()

def create_default_admin(initial_hash: str):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        if not cursor.fetchone():
            cursor.execute(
                """
                INSERT INTO users (username, password_hash, is_admin, must_change_password)
                VALUES ('admin', ?, 1, 1)
            """,
                (initial_hash,),
            )
            conn.commit()

def create_user(username: str, password_hash: str) -> bool:
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash),
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False


def get_user_auth_data(username: str) -> tuple[str, bool, bool] | None:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT password_hash, is_admin, must_change_password 
            FROM users 
            WHERE username = ?
        """,
            (username,),
        )
        row = cursor.fetchone()
        if row:
            return (row[0], bool(row[1]), bool(row[2]))
        return None

def update_password(username: str, new_hash: str) -> bool:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE users 
            SET password_hash = ?, must_change_password = 0 
            WHERE username = ?
        """,
            (new_hash, username),
        )
        conn.commit()
        return cursor.rowcount > 0