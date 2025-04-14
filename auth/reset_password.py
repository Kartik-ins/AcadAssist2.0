from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QFrame
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from models.user import User

class ResetPasswordPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        
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
        
        # Right side (reset password form)
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.setContentsMargins(40, 40, 40, 40)
        
        # Reset password form container
        reset_container = QFrame()
        reset_container.setMaximumWidth(400)
        reset_layout = QVBoxLayout(reset_container)
        reset_layout.setSpacing(16)
        
        # Reset title
        reset_title = QLabel("Reset Your Password")
        reset_title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        reset_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Email field
        email_label = QLabel("Email")
        email_label.setFont(QFont("Arial", 12))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setMinimumHeight(40)
        
        # New Password field
        new_password_label = QLabel("New Password")
        new_password_label.setFont(QFont("Arial", 12))
        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Enter new password")
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password_input.setMinimumHeight(40)
        
        # Confirm Password field
        confirm_password_label = QLabel("Confirm Password")
        confirm_password_label.setFont(QFont("Arial", 12))
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
        
        # Back to login button
        self.back_button = QPushButton("Back to Login")
        self.back_button.setFont(QFont("Arial", 12))
        self.back_button.setMinimumHeight(40)
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #2196F3;
                color: #2196F3;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: rgba(33, 150, 243, 0.1);
            }
        """)
        self.back_button.clicked.connect(self.go_to_login)
        
        # Add widgets to reset container
        reset_layout.addWidget(reset_title)
        reset_layout.addSpacing(20)
        reset_layout.addWidget(email_label)
        reset_layout.addWidget(self.email_input)
        reset_layout.addSpacing(10)
        reset_layout.addWidget(new_password_label)
        reset_layout.addWidget(self.new_password_input)
        reset_layout.addSpacing(10)
        reset_layout.addWidget(confirm_password_label)
        reset_layout.addWidget(self.confirm_password_input)
        reset_layout.addSpacing(20)
        reset_layout.addWidget(self.reset_button)
        reset_layout.addSpacing(10)
        reset_layout.addWidget(self.back_button)
        
        # Add reset container to right panel
        right_layout.addStretch()
        right_layout.addWidget(reset_container)
        right_layout.addStretch()
        
        # Add both panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)  # Right panel takes remaining space

    def reset_password(self):
        email = self.email_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not email or not new_password or not confirm_password:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        user = User.get_user_by_email(email)
        if user:
            User.update_password(email, new_password)
            QMessageBox.information(self, "Success", "Password reset successful!")
            self.go_to_login()
        else:
            QMessageBox.warning(self, "Error", "User not found.")

    def go_to_login(self):
        self.parent.set_page("login")
