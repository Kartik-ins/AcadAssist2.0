from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QFrame
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from models.user import User

class RegisterPage(QWidget):
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
        
        # Right side (registration form)
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.setContentsMargins(40, 40, 40, 40)
        
        # Registration form container
        register_container = QFrame()
        register_container.setMaximumWidth(400)
        register_layout = QVBoxLayout(register_container)
        register_layout.setSpacing(16)
        
        # Register title
        register_title = QLabel("Register New Account")
        register_title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        register_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Full Name field
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
        self.register_button = QPushButton("Register")
        self.register_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.register_button.setMinimumHeight(50)
        self.register_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.register_button.clicked.connect(self.register_user)
        
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
        
        # Add widgets to register container
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
        
        # Add register container to right panel
        right_layout.addStretch()
        right_layout.addWidget(register_container)
        right_layout.addStretch()
        
        # Add both panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)  # Right panel takes remaining space

    def register_user(self):
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        if not name or not email or not password:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        user = User(name, email, password)
        try:
            user.save()
            QMessageBox.information(self, "Success", "Registration successful!")
            self.go_to_login()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Registration failed:\n{str(e)}")

    def go_to_login(self):
        self.parent.set_page("login")
