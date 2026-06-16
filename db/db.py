import sqlite3

# right now it just creates the db inside of the server folder
# will fix later so the path is inside of the db folder
DB_NAME = "my.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with sqlite3.connect("my.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('Employee', 'Manager'))
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                description TEXT NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS approvals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expense_id INTEGER NOT NULL UNIQUE,
                status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'denied')),
                reviewer INTEGER,
                comment TEXT,
                review_date TEXT,
                FOREIGN KEY (expense_id) REFERENCES expenses(id),
                FOREIGN KEY (reviewer) REFERENCES users(id)
            )
        """)

        # these are the two default users:
        # Employee user: employee1
        # Employee pass: pass123
        # Manager user: manager1 
        # Manager pass: pass456
        conn.execute("""
            INSERT OR IGNORE INTO users (username, password, role)
            VALUES ('employee1', 'pass123', 'Employee')
        """)

        conn.execute("""
            INSERT OR IGNORE INTO users (username, password, role)
            VALUES ('manager1', 'pass456', 'Manager')
        """)

        print("Database initialized and defualt accounts created")

def get_user_by_username(username):
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        return dict(row) if row else None

