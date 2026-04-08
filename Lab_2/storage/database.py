import sqlite3
import uuid

DB_PATH = 'messenger_pro.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    # Користувачі
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id TEXT PRIMARY KEY, 
                        username TEXT UNIQUE, 
                        password TEXT)''')
    # Чати
    cursor.execute('''CREATE TABLE IF NOT EXISTS conversations (
                        id TEXT PRIMARY KEY, 
                        name TEXT, 
                        is_group INTEGER)''')
    # Учасники
    cursor.execute('''CREATE TABLE IF NOT EXISTS participants (
                        conversation_id TEXT, 
                        user_id TEXT)''')
    # Повідомлення
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                        id TEXT PRIMARY KEY, 
                        conversation_id TEXT, 
                        sender_id TEXT, 
                        text TEXT, 
                        timestamp TEXT,
                        status TEXT DEFAULT 'sent')''')
    conn.commit()
    conn.close()