import sqlite3

def create_db():
    conn = sqlite3.connect('MASTER.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            password TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Messages (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            thread_id TEXT,
            role TEXT,
            message TEXT,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES Users(user_id)
        )
    """)
    conn.commit()
    conn.close()

def write_to_messages_db(thread_id, role, message):
    conn = sqlite3.connect('MASTER.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Messages (thread_id, role, message) VALUES (?, ?, ?)", (thread_id, role, message))
    conn.commit()
    conn.close()

def get_all_thread_messages(thread_id):
    conn = sqlite3.connect('MASTER.db')
    cursor = conn.cursor()
    cursor.execute("SELECT message FROM Messages WHERE thread_id = ? ORDER BY message_id", (thread_id,))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

def get_unique_thread_ids():
    conn = sqlite3.connect('MASTER.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT thread_id FROM Messages")
    unique_thread_ids = reversed([row[0] for row in cursor.fetchall()])
    conn.close()
    return list(unique_thread_ids)

def add_user_to_db(email, password):
    conn = sqlite3.connect('MASTER.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (email, password) VALUES (?, ?)", (email, password))
    conn.commit()
    conn.close()

def authenticate_user(email, password):
    conn = sqlite3.connect('MASTER.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None