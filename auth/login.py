from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from models.user import User
from models.teacher import Teacher  # Import Teacher model
import psycopg2
import os

class LoginPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel("Login")
        label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Login as Student")
        self.login_button.clicked.connect(self.attempt_login)

        self.teacher_login_button = QPushButton("Login as Teacher")
        self.teacher_login_button.clicked.connect(self.attempt_teacher_login)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.go_to_register)

        self.reset_password_button = QPushButton("Reset Password")
        self.reset_password_button.clicked.connect(self.go_to_reset_password)

        layout.addWidget(label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.teacher_login_button)
        layout.addWidget(self.register_button)
        layout.addWidget(self.reset_password_button)
        self.setLayout(layout)

    def attempt_teacher_login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if Teacher.authenticate(email, password):
            teacher = Teacher.get_teacher_by_email(email)
            if teacher:
                # Use hardcoded drive folder ID
                self.parent.drive_folder_id = "1uIH-yuDQAITSjMyzhxXhjGUdQ7m_MN6F"
                print(f"Teacher login successful. Using folder ID: {self.parent.drive_folder_id}")  # Debugging
                self.parent.set_user_details(email, None)
                self.parent.set_page("resource")  # Redirect to resource page
            else:
                QMessageBox.warning(self, "Login Failed", "Teacher record not found.")
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid email or password.")

    def attempt_login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if User.authenticate(email, password):  # Check if it's a student login
            # Get student details from database
            conn = psycopg2.connect(os.getenv("DB_URL"))
            cur = conn.cursor()
            cur.execute("SELECT id FROM students WHERE email = %s;", (email,))
            result = cur.fetchone()
            cur.close()
            conn.close()
            
            if result:
                student_id = result[0]
                # Set user details in main window and use hardcoded drive folder ID
                self.parent.drive_folder_id = "1uIH-yuDQAITSjMyzhxXhjGUdQ7m_MN6F"
                print(f"Student login successful. Using folder ID: {self.parent.drive_folder_id}")  # Debugging
                self.parent.set_user_details(email, student_id)
                self.parent.set_page("resource")  # Redirect to resource page
            else:
                QMessageBox.warning(self, "Login Failed", "Student record not found.")
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid email or password.")

    def go_to_register(self):
        self.parent.set_page("register")

    def go_to_reset_password(self):
        self.parent.set_page("reset_password")
