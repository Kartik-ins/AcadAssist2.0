import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QLabel, QMessageBox, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QPixmap
from auth.login import LoginPage
from auth.register import RegisterPage
from auth.reset_password import ResetPasswordPage
from features.schedule_management import SchedulePage
from features.study_group_matcher import StudyGroupPage
from features.ai_chatbot import ChatbotPage
from features.resource_management import ResourcePage
from features.notes_summarization import NotesPage
from features.plagiarism_detection import PlagiarismPage
from features.text_to_speech import TextToSpeechPage
from features.teacher_subject_page import TeacherSubjectPage
from features.feedback_page import FeedbackPage
from models.teacher import Teacher
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Define global styles
GLOBAL_STYLESHEET = """
/* Global Styles */
QMainWindow, QWidget {
    background-color: #121212;
    color: #FFFFFF;
    font-family: 'Segoe UI', Arial, sans-serif;
}

QLabel {
    color: #FFFFFF;
}

QPushButton {
    background-color: #2196F3;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
    min-height: 36px;
}

QPushButton:hover {
    background-color: #1976D2;
}

QPushButton:pressed {
    background-color: #0D47A1;
}

QPushButton:disabled {
    background-color: #616161;
    color: #9E9E9E;
}

QLineEdit, QTextEdit {
    background-color: #1E1E1E;
    color: white;
    border: 1px solid #333;
    border-radius: 4px;
    padding: 8px;
    selection-background-color: #2196F3;
}

QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #2196F3;
}

QComboBox {
    background-color: #1E1E1E;
    color: white;
    border: 1px solid #333;
    border-radius: 4px;
    padding: 8px;
    min-height: 36px;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;
}

QListWidget {
    background-color: #1E1E1E;
    color: white;
    border: 1px solid #333;
    border-radius: 4px;
    padding: 4px;
}

QListWidget::item {
    padding: 8px;
    border-radius: 2px;
}

QListWidget::item:selected {
    background-color: #2196F3;
}

QCalendarWidget {
    background-color: #1E1E1E;
}

QSpinBox {
    background-color: #1E1E1E;
    color: white;
    border: 1px solid #333;
    border-radius: 4px;
    padding: 4px;
}

/* Style for sidebar navigation */
#sidebar {
    background-color: #1A1A1A;
    border-right: 1px solid #333;
}

#sidebar QPushButton {
    background-color: transparent;
    border: none;
    border-radius: 0;
    text-align: left;
    padding: 12px 16px;
    font-size: 14px;
    font-weight: normal;
    color: #B0BEC5;
}

#sidebar QPushButton:hover {
    background-color: #2C2C2C;
    color: white;
}

#sidebar QPushButton:checked {
    background-color: #2196F3;
    color: white;
    font-weight: bold;
}

#appTitle {
    color: #2196F3;
    font-size: 24px;
    font-weight: bold;
    padding: 16px;
}

#userLabel {
    color: #90CAF9;
    font-size: 13px;
    padding: 8px 16px;
    border-bottom: 1px solid #333;
    margin-bottom: 8px;
}
"""

class NavButton(QPushButton):
    """Custom navigation button for sidebar"""
    def __init__(self, text, icon_path=None):
        super().__init__(text)
        self.setCheckable(True)
        self.setFixedHeight(48)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(20, 20))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.user_email = None
        self.student_id = None
        self.drive_folder_id = "1uIH-yuDQAITSjMyzhxXhjGUdQ7m_MN6F" 
        self.is_teacher = False
        
        self.setWindowTitle("AcadAssist")
        self.setGeometry(100, 100, 1200, 800)  # Increased window size
        self.setStyleSheet(GLOBAL_STYLESHEET)
        
        # Main layout container
        main_container = QWidget()
        main_layout = QHBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar navigation
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(250)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # App title in sidebar
        app_title = QLabel("AcadAssist")
        app_title.setObjectName("appTitle")
        app_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(app_title)
        
        # User info display
        self.user_label = QLabel("Welcome, Guest")
        self.user_label.setObjectName("userLabel")
        sidebar_layout.addWidget(self.user_label)
        
        # Navigation buttons
        self.nav_buttons = {}
        
        # Auth buttons (initially visible)
        self.auth_buttons_container = QWidget()
        auth_layout = QVBoxLayout(self.auth_buttons_container)
        auth_layout.setContentsMargins(8, 8, 8, 8)
        auth_layout.setSpacing(8)
        
        self.nav_buttons["login"] = NavButton("Login")
        self.nav_buttons["login"].clicked.connect(lambda: self.set_page("login"))
        auth_layout.addWidget(self.nav_buttons["login"])
        
        self.nav_buttons["register"] = NavButton("Register")
        self.nav_buttons["register"].clicked.connect(lambda: self.set_page("register"))
        auth_layout.addWidget(self.nav_buttons["register"])
        
        self.nav_buttons["reset_password"] = NavButton("Reset Password")
        self.nav_buttons["reset_password"].clicked.connect(lambda: self.set_page("reset_password"))
        auth_layout.addWidget(self.nav_buttons["reset_password"])
        
        sidebar_layout.addWidget(self.auth_buttons_container)
        
        # Feature buttons (initially hidden)
        self.feature_buttons_container = QWidget()
        self.feature_buttons_container.setVisible(False)
        feature_layout = QVBoxLayout(self.feature_buttons_container)
        feature_layout.setContentsMargins(8, 8, 8, 8)
        feature_layout.setSpacing(8)
        
        # Add feature buttons
        for name, label in [
            ("schedule", "Schedule Management"),
            ("study_group", "Study Group Matcher"),
            ("chatbot", "AI Study Assistant"),
            ("resource", "Resource Management"),
            ("notes_summarization", "Notes Summarization"),
            ("plagiarism", "Plagiarism Detection"),
            ("text_to_speech", "Text to Speech"),
            ("feedback", "Feedback")
        ]:
            self.nav_buttons[name] = NavButton(label)
            self.nav_buttons[name].clicked.connect(lambda checked, n=name: self.set_page(n))
            feature_layout.addWidget(self.nav_buttons[name])
        
        # Add logout button at bottom of feature navigation
        feature_layout.addStretch()
        self.logout_button = NavButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        feature_layout.addWidget(self.logout_button)
        
        sidebar_layout.addWidget(self.feature_buttons_container)
        sidebar_layout.addStretch()
        
        # Content area using stacked widget
        self.stack = QStackedWidget()
        
        # Initialize pages
        self.pages = {
            "login": LoginPage(self),
            "register": RegisterPage(self),
            "reset_password": ResetPasswordPage(self),
            "schedule": SchedulePage(self),
            "study_group": StudyGroupPage(self, user_email=self.user_email),
            "chatbot": ChatbotPage(self),
            "resource": ResourcePage(self, self.drive_folder_id),
            "notes_summarization": NotesPage(self),
            "plagiarism": PlagiarismPage(self, detection_type="offline"),
            "text_to_speech": TextToSpeechPage(self),
        }
        
        # Add pages to the stack
        for page in self.pages.values():
            self.stack.addWidget(page)
        
        # Initialize feedback page (will be recreated on login)
        self.feedback_page = None
        
        # Add sidebar and stack to main layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack)
        
        self.setCentralWidget(main_container)
        
        # Show login page first
        self.set_page("login")
        self.nav_buttons["login"].setChecked(True)

    def set_page(self, page_name):
        """Sets the current page and handles navigation state."""
        print(f"Switching to page: {page_name}")  # Debugging
        
        # Uncheck all nav buttons first
        for button in self.nav_buttons.values():
            button.setChecked(False)
            
        # Check the current page's button
        if page_name in self.nav_buttons:
            self.nav_buttons[page_name].setChecked(True)
        
        # Special handling for teacher subject page
        if page_name == "teacher_subject":
            if "teacher_subject" not in self.pages:
                self.pages["teacher_subject"] = TeacherSubjectPage(self, self.drive_folder_id)
                self.stack.addWidget(self.pages["teacher_subject"])
            self.stack.setCurrentWidget(self.pages["teacher_subject"])
            return
            
        # Check if user is a teacher trying to access restricted pages
        if self.is_teacher and page_name not in ["login", "resource", "feedback", "register", "reset_password"]:
            QMessageBox.warning(self, "Access Denied", "Teachers can only access the Resource and Feedback pages.")
            # Reset to resource page
            page_name = "resource"
            self.nav_buttons["resource"].setChecked(True)
        
        # Handle plagiarism page special case
        if page_name == "plagiarism":
            # Allow user to choose detection type dynamically
            detection_type = self.get_plagiarism_detection_type()
            new_page = PlagiarismPage(self, detection_type=detection_type)
            self.stack.addWidget(new_page)  
            self.pages["plagiarism"] = new_page  
            self.stack.setCurrentWidget(new_page) 
        else:
            # Normal page handling
            if page_name in self.pages:
                self.stack.setCurrentWidget(self.pages[page_name])
            elif page_name == "feedback":
                self.stack.setCurrentWidget(self.feedback_page)
            
    def set_user_details(self, email, student_id):
        """Set user details after successful login"""
        self.user_email = email
        self.student_id = student_id
        
        # Check if the user is a teacher
        self.is_teacher = Teacher.get_teacher_by_email(email) is not None
        print(f"Setting user details. Is teacher: {self.is_teacher}")  # Debug print
        
        # Update the UI for logged-in user
        self.user_label.setText(f"Logged in as: {email}")
        self.auth_buttons_container.setVisible(False)
        self.feature_buttons_container.setVisible(True)
        
        # Update StudyGroupPage with user's email
        self.pages["study_group"] = StudyGroupPage(self, user_email=email)
        self.stack.addWidget(self.pages["study_group"])
        
        # Create new FeedbackPage with correct teacher status
        if self.feedback_page:
            self.stack.removeWidget(self.feedback_page)
            self.feedback_page.deleteLater()
        self.feedback_page = FeedbackPage(self, self.is_teacher)
        self.stack.addWidget(self.feedback_page)
        
        # Set appropriate page based on user type
        if self.is_teacher:
            self.set_page("resource")
            # Hide irrelevant navigation options for teachers
            # Allow access to resource and feedback pages only
            for name in ["schedule", "study_group", "notes_summarization", "plagiarism", "chatbot", "text_to_speech"]:
                self.nav_buttons[name].setVisible(False)
            # Make sure feedback button is visible for teachers
            self.nav_buttons["feedback"].setVisible(True)
        else:
            self.set_page("resource")  # Default landing page
    
    def logout(self):
        """Handle user logout"""
        self.user_email = None
        self.student_id = None
        self.is_teacher = False
        
        # Reset UI state
        self.user_label.setText("Welcome, Guest")
        self.auth_buttons_container.setVisible(True)
        self.feature_buttons_container.setVisible(False)
        
        # Clean up feedback page
        if self.feedback_page:
            self.stack.removeWidget(self.feedback_page)
            self.feedback_page.deleteLater()
            self.feedback_page = None
        
        # Make all navigation options visible again for next login
        for name in ["schedule", "study_group", "notes_summarization", "plagiarism", "chatbot", "text_to_speech"]:
            self.nav_buttons[name].setVisible(True)
            
        # Go back to login page
        self.set_page("login")

    def get_plagiarism_detection_type(self):
        """Prompt user to select plagiarism detection type (online or offline)."""
        return "online"  # Default to online detection for demonstration

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
