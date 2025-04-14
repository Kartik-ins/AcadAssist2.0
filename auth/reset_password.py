from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                         QMessageBox, QHBoxLayout, QFrame, QStackedWidget)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from models.user import User
from utils.otp_utils import otp_manager

class ResetPasswordPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.verified_email = None
        
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
        app_label = QLabel("AcadAssist")
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
        left_layout.addStretch()
        
        # Right side (reset password form)
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.setContentsMargins(40, 40, 40, 40)
        
        # Create stacked widget for reset password steps
        self.stack = QStackedWidget()
        
        # Step 1: Email entry
        email_container = QFrame()
        email_container.setMaximumWidth(400)
        email_layout = QVBoxLayout(email_container)
        email_layout.setSpacing(16)
        
        # Title
        title = QLabel("Reset Password")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Description
        desc = QLabel("Enter your email address to receive a verification code.")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setWordWrap(True)
        
        # Email field
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setMinimumHeight(40)
        
        # Send code button
        self.send_code_button = QPushButton("Send Verification Code")
        self.send_code_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.send_code_button.setMinimumHeight(50)
        self.send_code_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_code_button.clicked.connect(self.send_verification_code)
        
        # Back to login link
        back_layout = QHBoxLayout()
        back_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        back_label = QLabel("Remember your password?")
        self.back_button = QPushButton("Back to Login")
        self.back_button.setStyleSheet("""
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
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_button.clicked.connect(self.go_to_login)
        back_layout.addWidget(back_label)
        back_layout.addWidget(self.back_button)
        
        # Add widgets to email container
        email_layout.addWidget(title)
        email_layout.addSpacing(10)
        email_layout.addWidget(desc)
        email_layout.addSpacing(20)
        email_layout.addWidget(self.email_input)
        email_layout.addSpacing(20)
        email_layout.addWidget(self.send_code_button)
        email_layout.addSpacing(20)
        email_layout.addLayout(back_layout)
        
        # Step 2: OTP verification
        otp_container = QFrame()
        otp_container.setMaximumWidth(400)
        otp_layout = QVBoxLayout(otp_container)
        otp_layout.setSpacing(16)
        
        # OTP title
        otp_title = QLabel("Verify Your Email")
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
        self.verify_button = QPushButton("Verify")
        self.verify_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.verify_button.setMinimumHeight(50)
        self.verify_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.verify_button.clicked.connect(self.verify_otp)
        
        # Resend code button
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
        self.resend_button.clicked.connect(self.resend_verification_code)
        
        # Back button
        self.back_to_email_button = QPushButton("← Back")
        self.back_to_email_button.setStyleSheet("""
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
        self.back_to_email_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_to_email_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        
        # Add widgets to OTP container
        otp_layout.addWidget(self.back_to_email_button, alignment=Qt.AlignmentFlag.AlignLeft)
        otp_layout.addWidget(otp_title)
        otp_layout.addSpacing(10)
        otp_layout.addWidget(otp_desc)
        otp_layout.addSpacing(20)
        otp_layout.addWidget(self.otp_input)
        otp_layout.addSpacing(20)
        otp_layout.addWidget(self.verify_button)
        otp_layout.addSpacing(10)
        otp_layout.addWidget(self.resend_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Step 3: New password
        password_container = QFrame()
        password_container.setMaximumWidth(400)
        password_layout = QVBoxLayout(password_container)
        password_layout.setSpacing(16)
        
        # Password title
        password_title = QLabel("Create New Password")
        password_title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        password_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Password input
        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Enter new password")
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password_input.setMinimumHeight(40)
        
        # Confirm password input
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm new password")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input.setMinimumHeight(40)
        
        # Reset button
        self.reset_button = QPushButton("Reset Password")
        self.reset_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.reset_button.setMinimumHeight(50)
        self.reset_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_button.clicked.connect(self.reset_password)
        
        # Add widgets to password container
        password_layout.addWidget(password_title)
        password_layout.addSpacing(20)
        password_layout.addWidget(self.new_password_input)
        password_layout.addSpacing(10)
        password_layout.addWidget(self.confirm_password_input)
        password_layout.addSpacing(20)
        password_layout.addWidget(self.reset_button)
        
        # Add containers to stack
        self.stack.addWidget(email_container)
        self.stack.addWidget(otp_container)
        self.stack.addWidget(password_container)
        
        # Add stack to right panel
        right_layout.addWidget(self.stack)
        
        # Add both panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)  # Right panel takes remaining space

    def send_verification_code(self):
        email = self.email_input.text()
        if not email:
            QMessageBox.warning(self, "Error", "Please enter your email address.")
            return
            
        # Check if email exists in database
        user = User.get_user_by_email(email)
        if not user:
            QMessageBox.warning(self, "Error", "No account found with this email address.")
            return
            
        # Generate and send OTP
        otp = otp_manager.generate_otp()
        if otp_manager.send_otp_email(email, otp, "password reset"):
            otp_manager.save_otp(email, otp)
            self.stack.setCurrentIndex(1)  # Show OTP verification page
        else:
            QMessageBox.critical(self, "Error", "Failed to send verification code. Please try again.")

    def verify_otp(self):
        email = self.email_input.text()
        otp = self.otp_input.text()
        
        if not otp:
            QMessageBox.warning(self, "Error", "Please enter the verification code.")
            return
            
        if otp_manager.verify_otp(email, otp):
            self.verified_email = email
            self.stack.setCurrentIndex(2)  # Show new password page
        else:
            QMessageBox.warning(self, "Error", "Invalid or expired verification code.")

    def resend_verification_code(self):
        email = self.email_input.text()
        otp = otp_manager.generate_otp()
        if otp_manager.send_otp_email(email, otp, "password reset"):
            otp_manager.save_otp(email, otp)
            QMessageBox.information(self, "Success", "Verification code resent!")
        else:
            QMessageBox.critical(self, "Error", "Failed to resend verification code. Please try again.")

    def reset_password(self):
        if not self.verified_email:
            QMessageBox.critical(self, "Error", "Email verification required.")
            self.stack.setCurrentIndex(0)
            return
            
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        if not new_password or not confirm_password:
            QMessageBox.warning(self, "Error", "Please enter and confirm your new password.")
            return
            
        if new_password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return
            
        try:
            User.update_password(self.verified_email, new_password)
            QMessageBox.information(self, "Success", "Password reset successful!")
            self.go_to_login()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to reset password:\n{str(e)}")

    def go_to_login(self):
        self.parent.set_page("login")
