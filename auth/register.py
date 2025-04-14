from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                         QMessageBox, QHBoxLayout, QFrame, QStackedWidget)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from models.user import User
from utils.otp_utils import otp_manager

class RegisterPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.temp_user_data = None  
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: #0D47A1;")
        left_panel.setFixedWidth(400)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        app_label = QLabel("AcadAssist")
        app_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        app_label.setStyleSheet("color: white;")
        app_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("Your Academic Assistant")
        subtitle.setFont(QFont("Arial", 16))
        subtitle.setStyleSheet("color: #90CAF9;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        features_label = QLabel(
            "• AI Study Assistant\n"
            "• Resource Management\n"
            "• Schedule Organization\n"
            "• Notes Summarization\n"
            "• Plagiarism Detection\n"
            "• Study Group Matching\n"
            "• Text to Speech\n"
            "• Feedback"
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
        
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.setContentsMargins(40, 40, 40, 40)
        
        self.stack = QStackedWidget()
        
        register_container = QFrame()
        register_container.setMaximumWidth(400)
        register_layout = QVBoxLayout(register_container)
        register_layout.setSpacing(16)
        
        register_title = QLabel("Register New Account")
        register_title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        register_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        name_label = QLabel("Full Name")
        name_label.setFont(QFont("Arial", 12))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your full name")
        self.name_input.setMinimumHeight(40)
        
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
        self.password_input.setPlaceholderText("Create a password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(40)
        
        # Register button
        self.register_button = QPushButton("Continue")
        self.register_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.register_button.setMinimumHeight(50)
        self.register_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.register_button.clicked.connect(self.start_registration)
        
        # Login link
        login_layout = QHBoxLayout()
        login_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        login_label = QLabel("Already have an account?")
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("""
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
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.clicked.connect(self.go_to_login)
        login_layout.addWidget(login_label)
        login_layout.addWidget(self.login_button)
        
       
        register_layout.addWidget(register_title)
        register_layout.addSpacing(20)
        register_layout.addWidget(name_label)
        register_layout.addWidget(self.name_input)
        register_layout.addSpacing(10)
        register_layout.addWidget(email_label)
        register_layout.addWidget(self.email_input)
        register_layout.addSpacing(10)
        register_layout.addWidget(password_label)
        register_layout.addWidget(self.password_input)
        register_layout.addSpacing(20)
        register_layout.addWidget(self.register_button)
        register_layout.addSpacing(20)
        register_layout.addLayout(login_layout)
        
        # OTP verification container (Step 2)
        otp_container = QFrame()
        otp_container.setMaximumWidth(400)
        otp_layout = QVBoxLayout(otp_container)
        otp_layout.setSpacing(16)
        
        # OTP title
        otp_title = QLabel("Email Verification")
        otp_title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        otp_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # OTP description
        otp_desc = QLabel("We've sent a verification code to your email.")
        otp_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        otp_desc.setWordWrap(True)
        
        # OTP input
        self.otp_input = QLineEdit()
        self.otp_input.setPlaceholderText("Enter verification code")
        self.otp_input.setMinimumHeight(40)
        self.otp_input.setMaxLength(6)
        self.otp_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Verify button
        self.verify_button = QPushButton("Verify & Complete Registration")
        self.verify_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.verify_button.setMinimumHeight(50)
        self.verify_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.verify_button.clicked.connect(self.verify_otp)
        
        # Resend OTP button
        self.resend_button = QPushButton("Resend Code")
        self.resend_button.setStyleSheet("""
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
        self.resend_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.resend_button.clicked.connect(self.resend_otp)
        
        # Back button
        self.back_button = QPushButton("← Back")
        self.back_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #666;
                padding: 0;
            }
            QPushButton:hover {
                color: #333;
            }
        """)
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        
        otp_layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignLeft)
        otp_layout.addWidget(otp_title)
        otp_layout.addSpacing(10)
        otp_layout.addWidget(otp_desc)
        otp_layout.addSpacing(20)
        otp_layout.addWidget(self.otp_input)
        otp_layout.addSpacing(20)
        otp_layout.addWidget(self.verify_button)
        otp_layout.addSpacing(10)
        otp_layout.addWidget(self.resend_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.stack.addWidget(register_container)
        self.stack.addWidget(otp_container)
        
        right_layout.addWidget(self.stack)
        
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1) 

    def start_registration(self):
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        if not name or not email or not password:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return
            
        self.temp_user_data = {
            'name': name,
            'email': email,
            'password': password
        }
        
        # Generate and send OTP
        otp = otp_manager.generate_otp()
        if otp_manager.send_otp_email(email, otp, "registration"):
            otp_manager.save_otp(email, otp)
            self.stack.setCurrentIndex(1)  
        else:
            QMessageBox.critical(self, "Error", "Failed to send verification code. Please try again.")

    def verify_otp(self):
        if not self.temp_user_data:
            QMessageBox.critical(self, "Error", "Registration data not found. Please try again.")
            self.stack.setCurrentIndex(0)
            return
            
        otp = self.otp_input.text()
        if not otp:
            QMessageBox.warning(self, "Error", "Please enter the verification code.")
            return
            
        if otp_manager.verify_otp(self.temp_user_data['email'], otp):
            # Create and save user
            user = User(
                self.temp_user_data['name'],
                self.temp_user_data['email'],
                self.temp_user_data['password']
            )
            try:
                user.save()
                QMessageBox.information(self, "Success", "Registration successful!")
                self.go_to_login()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Registration failed:\n{str(e)}")
        else:
            QMessageBox.warning(self, "Error", "Invalid or expired verification code.")

    def resend_otp(self):
        if not self.temp_user_data:
            QMessageBox.critical(self, "Error", "Registration data not found. Please try again.")
            self.stack.setCurrentIndex(0)
            return
            
        otp = otp_manager.generate_otp()
        if otp_manager.send_otp_email(self.temp_user_data['email'], otp, "registration"):
            otp_manager.save_otp(self.temp_user_data['email'], otp)
            QMessageBox.information(self, "Success", "Verification code resent!")
        else:
            QMessageBox.critical(self, "Error", "Failed to resend verification code. Please try again.")

    def go_to_login(self):
        self.parent.set_page("login")
