"""
Database module for Account Service
Handles user data storage and retrieval using SQLite
"""

import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'users.db')


def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with the users table"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def find_user_by_username(username):
    """Find a user by their username"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    conn.close()

    if user:
        return {
            'id': user['id'],
            'username': user['username'],
            'password': user['password']
        }
    return None


def add_user(username, password):
    """Add a new user to the database"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO users (username, password) VALUES (?, ?)',
        (username, password)
    )

    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {
        'id': user_id,
        'username': username,
        'password': password
    }


def get_all_users():
    """Get all users from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    conn.close()

    return [
        {
            'id': user['id'],
            'username': user['username'],
            'password': user['password']
        }
        for user in users
    ]


# Initialize the database when the module is imported
init_db()
