from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, 
    QHBoxLayout, QFrame
)
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt
from models.user import User
from models.teacher import Teacher
import psycopg2
import os

class LoginPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        # Main layout with centering
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Left side (logo/branding)
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: #0D47A1;")
        left_panel.setFixedWidth(400)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # App logo/title
        app_label = QLabel("AcadAssist 2.0")
        app_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        app_label.setStyleSheet("color: white;")
        app_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # App subtitle
        subtitle = QLabel("Your Academic Assistant")
        subtitle.setFont(QFont("Arial", 16))
        subtitle.setStyleSheet("color: #90CAF9;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # App features bullet points
        features_label = QLabel(
            "• AI Study Assistant\n"
            "• Resource Management\n"
            "• Schedule Organization\n"
            "• Notes Summarization\n"
            "• Plagiarism Detection\n"
            "• Study Group Matching"
        )
        features_label.setFont(QFont("Arial", 14))
        features_label.setStyleSheet("color: white; margin-top: 30px;")
        features_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        left_layout.addStretch()
        left_layout.addWidget(app_label)
        left_layout.addWidget(subtitle)
        left_layout.addSpacing(40)
        left_layout.addWidget(features_label)
        left_layout.addStretch()
        
        # Right side (login form)
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.setContentsMargins(40, 40, 40, 40)
        
        # Login form container
        login_container = QFrame()
        login_container.setMaximumWidth(400)
        login_layout = QVBoxLayout(login_container)
        login_layout.setSpacing(16)
        
        # Login title
        login_title = QLabel("Login to Your Account")
        login_title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        login_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Email field
        email_label = QLabel("Email")
        email_label.setFont(QFont("Arial", 12))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setMinimumHeight(40)
        
        # Password field
        password_label = QLabel("Password")
        password_label.setFont(QFont("Arial", 12))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(40)
        
        # Forgot password link styled as button
        self.reset_password_button = QPushButton("Forgot Password?")
        self.reset_password_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #2196F3;
                text-align: right;
                font-size: 10pt;
                padding: 0;
            }
            QPushButton:hover {
                color: #0D47A1;
                text-decoration: underline;
            }
        """)
        self.reset_password_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_password_button.clicked.connect(self.go_to_reset_password)
        
        # Login buttons
        self.login_button = QPushButton("Login as Student")
        self.login_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.login_button.setMinimumHeight(50)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.clicked.connect(self.attempt_login)
        
        self.teacher_login_button = QPushButton("Login as Teacher")
        self.teacher_login_button.setFont(QFont("Arial", 12))
        self.teacher_login_button.setMinimumHeight(50)
        self.teacher_login_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        self.teacher_login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.teacher_login_button.clicked.connect(self.attempt_teacher_login)
        
        # Register link
        register_layout = QHBoxLayout()
        register_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        register_label = QLabel("Don't have an account?")
        self.register_button = QPushButton("Sign up")
        self.register_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #2196F3;
                font-weight: bold;
                padding: 0;
            }
            QPushButton:hover {
                color: #0D47A1;
                text-decoration: underline;
            }
        """)
        self.register_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.register_button.clicked.connect(self.go_to_register)
        register_layout.addWidget(register_label)
        register_layout.addWidget(self.register_button)
        
        # Add widgets to login container
        login_layout.addWidget(login_title)
        login_layout.addSpacing(20)
        login_layout.addWidget(email_label)
        login_layout.addWidget(self.email_input)
        login_layout.addSpacing(10)
        login_layout.addWidget(password_label)
        login_layout.addWidget(self.password_input)
        login_layout.addSpacing(20)
        login_layout.addWidget(self.login_button)
        login_layout.addWidget(self.teacher_login_button)
        login_layout.addSpacing(20)
        login_layout.addLayout(register_layout)
        
        # Add login container to right panel
        right_layout.addStretch()
        right_layout.addWidget(login_container)
        right_layout.addStretch()
        
        # Add both panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)  # Right panel takes remaining space
        
    def attempt_teacher_login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Login Failed", "Please enter both email and password.")
            return

        if Teacher.authenticate(email, password):
            teacher = Teacher.get_teacher_by_email(email)
            if teacher:
                # Use hardcoded drive folder ID
                self.parent.drive_folder_id = "1uIH-yuDQAITSjMyzhxXhjGUdQ7m_MN6F"
                print(f"Teacher login successful. Using folder ID: {self.parent.drive_folder_id}")
                self.parent.set_user_details(email, None)
                self.parent.set_page("resource")  # Redirect to resource page
            else:
                QMessageBox.warning(self, "Login Failed", "Teacher record not found.")
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid email or password.")

    def attempt_login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Login Failed", "Please enter both email and password.")
            return

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
                print(f"Student login successful. Using folder ID: {self.parent.drive_folder_id}")
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
