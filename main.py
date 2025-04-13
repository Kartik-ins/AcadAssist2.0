import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QComboBox, QToolBar, QMessageBox
from auth.login import LoginPage
from auth.register import RegisterPage
from auth.reset_password import ResetPasswordPage
from features.schedule_management import SchedulePage
from features.study_group_matcher import StudyGroupPage
from features.ai_chatbot import ChatbotPage
from features.resource_management import ResourcePage
from features.notes_summarization import NotesPage
from features.plagiarism_detection import PlagiarismPage
from features.teacher_subject_page import TeacherSubjectPage
from models.teacher import Teacher
from features.plagiarism_detection import PlagiarismPage 
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  

class MainWindow(QMainWindow): 

    def __init__(self):
        super().__init__()
        self.user_email = None
        self.student_id = None
        self.drive_folder_id = "1uIH-yuDQAITSjMyzhxXhjGUdQ7m_MN6F"  # Correct folder ID
        self.is_teacher = False
        print(f"MainWindow initialized with drive_folder_id: {self.drive_folder_id}")  # Debugging
        
        self.setWindowTitle("EduAssist")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #121212; color: white;")
        
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

            "plagiarism": PlagiarismPage(self, detection_type="offline"),  #
            }

        
        # Add pages to the stack
        for page in self.pages.values():
            self.stack.addWidget(page)
        
        self.setCentralWidget(self.stack)
        
        # Add feature selection toolbar
        self.init_toolbar()
        
        # Show login page first and disable navigation initially
        self.set_page("login")
        self.feature_selector.setEnabled(False)

    def init_toolbar(self):
        toolbar = QToolBar("Feature Selection")
        self.addToolBar(toolbar)
        
        self.feature_selector = QComboBox()
        self.feature_selector.addItems([
            "Login", 
            "Register", 
            "Reset Password", 
            "Schedule", 
            "Study Group", 
            "Chatbot", 
            "Resource",
            "Notes Summarization",
            "Plagiarism Detection"
        ])
        self.feature_selector.currentIndexChanged.connect(self.on_feature_selected)
        
        toolbar.addWidget(self.feature_selector)

    def on_feature_selected(self, index):
        """Handle feature selection with proper page name mapping"""
        feature_text = self.feature_selector.currentText()
        # Map the display text to the correct page name
        page_mapping = {
            "Login": "login",
            "Register": "register",
            "Reset Password": "reset_password",
            "Schedule": "schedule",
            "Study Group": "study_group",
            "Chatbot": "chatbot",
            "Resource": "resource",
            "Notes Summarization": "notes_summarization",
            "Plagiarism Detection": "plagiarism"
        }
        page_name = page_mapping.get(feature_text)
        
        # Check if user is a teacher trying to access non-resource and non-login pages
        if self.is_teacher and page_name not in ["resource", "login"]:
            QMessageBox.warning(self, "Access Denied", "Teachers can only access the Login and Resource pages.")
            # Reset the selector to Resource
            self.feature_selector.setCurrentText("Resource")
            return
            
        if page_name == "plagiarism":
            # Allow user to choose detection type dynamically
            detection_type = self.get_plagiarism_detection_type()
            new_page = PlagiarismPage(self, detection_type=detection_type)
            self.stack.addWidget(new_page)  # Add the new page to the stack
            self.pages["plagiarism"] = new_page  # Update the reference
            self.stack.setCurrentWidget(new_page)  # Set the new page as current
        else:
            self.set_page(page_name)

    def set_page(self, page_name):
        """Sets the current page and enables navigation after login."""
        print(f"Switching to page: {page_name}")  # Debugging
        if page_name in self.pages:
            if page_name == "resource" and self.user_email:
                print(f"Using drive_folder_id for ResourcePage: {self.drive_folder_id}")  # Debugging
                if self.pages["resource"] not in self.stack.children():
                    self.stack.addWidget(self.pages["resource"])
                self.stack.setCurrentWidget(self.pages["resource"])
            elif page_name == "teacher_subject":
                print(f"Using drive_folder_id for TeacherSubjectPage: {self.drive_folder_id}")  # Debugging
                if "teacher_subject" not in self.pages:
                    print(f"Initializing TeacherSubjectPage with folder ID: {self.drive_folder_id}")  # Debugging
                    self.pages["teacher_subject"] = TeacherSubjectPage(self, self.drive_folder_id)
                    self.stack.addWidget(self.pages["teacher_subject"])
                self.stack.setCurrentWidget(self.pages["teacher_subject"])
            else:
                self.stack.setCurrentWidget(self.pages[page_name])
            
            # Enable feature selection after login
            if page_name == "login":
                self.feature_selector.setEnabled(False)
            else:
                self.feature_selector.setEnabled(True)
        elif page_name == "teacher_subject":            
            teacher = Teacher.get_teacher_by_email(self.user_email)
            if teacher:
                subject_page = TeacherSubjectPage(self, self.drive_folder_id)  # Use the correct folder ID
                self.stack.addWidget(subject_page)
                self.stack.setCurrentWidget(subject_page)
                
    def set_user_details(self, email, student_id):
        """Set user details after successful login"""
        self.user_email = email
        self.student_id = student_id
        # Check if the user is a teacher
        self.is_teacher = Teacher.get_teacher_by_email(email) is not None
        
        # Update StudyGroupPage with user's email
        # Create a new instance with the user's email
        self.pages["study_group"] = StudyGroupPage(self, user_email=email)
        # Add the new page to the stack
        self.stack.addWidget(self.pages["study_group"])
        
        # If teacher, set the feature selector to Resource
        if self.is_teacher:
            self.feature_selector.setCurrentText("Resource")

    def get_plagiarism_detection_type(self):
        """Prompt user to select plagiarism detection type (online or offline)."""
        return "online"  # Default to online detection for demonstration

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
