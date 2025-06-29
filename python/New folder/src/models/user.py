import hashlib
from .database import Database
import sqlite3


class User:
    def __init__(self):
        self.db = Database()
    
    def authenticate(self, username, password):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute('''
            SELECT id, username, role FROM users 
            WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'role': user[2]
            }
        return None
    
    def create_user(self, username, password, role='user'):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            cursor.execute('''
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
            ''', (username, password_hash, role))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_all_users(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, username, role, created_at FROM users')
        users = cursor.fetchall()
        conn.close()
        
        return users
