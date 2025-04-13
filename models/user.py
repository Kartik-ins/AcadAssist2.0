import psycopg2
import bcrypt
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

# PostgreSQL connection
load_dotenv()
db_url = os.getenv("DB_URL")
conn =psycopg2.connect(db_url)
cursor = conn.cursor(cursor_factory=RealDictCursor)

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = self._hash_password(password)

    @staticmethod
    def _hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def _check_password(password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    def save(self):
        # Insert into students table
        cursor.execute("INSERT INTO students (name, email) VALUES (%s, %s);", (self.name, self.email))
        conn.commit()

        # Insert into user_credentials
        cursor.execute("INSERT INTO user_credentials (email, password_hash) VALUES (%s, %s);", (self.email, self.password))
        conn.commit()

    @staticmethod
    def authenticate(email, password):
        try:
            cursor.execute("SELECT password_hash FROM user_credentials WHERE email = %s;", (email,))
            result = cursor.fetchone()
            if result and User._check_password(password, result['password_hash']):
                return True
            return False
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Database error: {e}")
            return False

    @staticmethod
    def get_user_by_email(email):
        cursor.execute("SELECT * FROM user_credentials WHERE email = %s;", (email,))
        return cursor.fetchone()

    @staticmethod
    def update_password(email, new_password):
        hashed = User._hash_password(new_password)
        cursor.execute("UPDATE user_credentials SET password_hash = %s WHERE email = %s;", (hashed, email))
        conn.commit()
