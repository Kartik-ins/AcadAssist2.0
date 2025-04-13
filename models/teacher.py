import psycopg2
import bcrypt
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

# PostgreSQL connection
load_dotenv()
db_url = os.getenv("DB_URL")
conn = psycopg2.connect(db_url)
cursor = conn.cursor(cursor_factory=RealDictCursor)

class Teacher:
    @staticmethod
    def authenticate(email, password):
        try:
            cursor.execute("SELECT password FROM teacher_credentials WHERE email = %s;", (email,))
            result = cursor.fetchone()
            if result:
                print(f"Database password: {result['password']}, Provided password: {password}")  # Debugging
                if password == result['password']:  # Direct string comparison
                    return True
            return False
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Database error: {e}")
            return False

    @staticmethod
    def get_teacher_by_email(email):
        cursor.execute("SELECT * FROM teacher_credentials WHERE email = %s;", (email,))
        return cursor.fetchone()
