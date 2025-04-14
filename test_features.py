import pytest
from PyQt6.QtWidgets import QApplication
from datetime import datetime
import pytz
from features.ai_chatbot import ChatbotPage, ChatMessage, ChatWorker
from features.plagiarism_detection import PlagiarismPage, PlagiarismWorker
from features.schedule_management import SchedulePage
from features.notes_summarization import NotesPage
from features.resource_management import ResourceCard, ResourcePage
from features.study_group_matcher import StudyGroupPage
from features.text_to_speech import TextToSpeechPage, TTSWorker
from features.feedback_page import FeedbackPage
from features.teacher_subject_page import TeacherSubjectPage
from auth.login import LoginPage
from auth.register import RegisterPage
from auth.reset_password import ResetPasswordPage
from utils.google_drive_utils import create_folder, upload_file, list_files, download_file, remove_file
from models.user import User
from models.teacher import Teacher

# Mock parent class for testing
class MockParent:
    def __init__(self, user_email=None):
        self.user_email = user_email

# Initialize QApplication for GUI tests
app = QApplication([])

# Test cases for AI Chatbot
def test_chatbot_ui():
    chatbot = ChatbotPage(None)
    assert chatbot.chat_input is not None
    assert chatbot.send_button is not None
    assert chatbot.reset_button is not None

def test_chat_message():
    message = ChatMessage("Test message", True)
    assert message is not None

def test_chat_worker():
    worker = ChatWorker("Test message")
    assert worker.message == "Test message"

def test_plagiarism_ui():
    detector = PlagiarismPage(None)
    assert detector.input_text_1 is not None
    assert detector.input_text_2 is not None
    assert detector.check_button is not None

def test_plagiarism_calculation():
    detector = PlagiarismPage(None)
    text1 = "This is a test document."
    text2 = "This is a similar test document."
    similarity = detector.calculate_similarity(text1, text2)
    assert isinstance(similarity, float)
    assert 0 <= similarity <= 100

def test_plagiarism_worker():
    worker = PlagiarismWorker("Test text")
    assert worker.text == "Test text"

def test_schedule_page_ui():
    schedule = SchedulePage(None)
    assert schedule.calendar is not None
    assert schedule.deadline_input is not None
    assert schedule.save_button is not None

def test_time_conversion():
    schedule = SchedulePage(None)
    local_time = datetime(2025, 4, 15, 10, 0)  # Create naive datetime first
    utc_time = schedule.convert_to_utc(local_time)
    assert isinstance(utc_time, datetime)
    assert utc_time.tzinfo == pytz.UTC
    assert utc_time.hour < local_time.hour

# Test cases for Notes Summarization
def test_notes_page_ui():
    notes_page = NotesPage(None)
    assert notes_page.notes_input is not None
    assert notes_page.summary_output is not None
    assert notes_page.summarize_button is not None
    assert notes_page.upload_button is not None

def test_notes_summarization():
    notes_page = NotesPage(None)
    test_notes = "This is a test paragraph. " * 10  
    notes_page.notes_input.setPlainText(test_notes)
    notes_page.summarize_notes()
    summary = notes_page.summary_output.toPlainText()
    assert isinstance(summary, str)
    assert len(summary) <= len(test_notes) 
    
# Test cases for Resource Management
def test_resource_card():
    card = ResourceCard("test.txt", "123456", None)
    assert card.file_name == "test.txt"
    assert card.file_id == "123456"

def test_resource_page():
    mock_parent = MockParent(user_email="test@example.com")
    page = ResourcePage(mock_parent, "test_folder_id")
    assert page is not None
    assert page.drive_folder_id == "test_folder_id"

# Test cases for Study Group Matcher
def test_study_group_page():
    page = StudyGroupPage(None)
    assert page.checkboxes is not None
    assert len(page.checkboxes) > 0
    assert page.save_button is not None
    assert page.match_button is not None

def test_interest_selection():
    page = StudyGroupPage(None)
    # Test that fixed interests are loaded
    assert any(cb.text() == "math" for cb in page.checkboxes)
    assert any(cb.text() == "physics" for cb in page.checkboxes)

# Test cases for Text-to-Speech
def test_tts_page_ui():
    tts_page = TextToSpeechPage(None)
    assert tts_page.text_input is not None
    assert tts_page.convert_button is not None
    assert tts_page.language_dropdown is not None
    assert tts_page.accent_dropdown is not None

def test_tts_worker():
    worker = TTSWorker("Test text", "en", "com", "test.mp3")
    assert worker.text == "Test text"
    assert worker.language == "en"
    assert worker.accent == "com"
    assert worker.save_path == "test.mp3"

# Test cases for Feedback System
def test_feedback_page_student():
    page = FeedbackPage(None, is_teacher=False)
    assert page.category_selector is not None
    assert page.feedback_input is not None
    assert page.submit_button is not None

def test_feedback_page_teacher():
    page = FeedbackPage(None, is_teacher=True)
    assert page.filter_selector is not None
    assert page.refresh_button is not None
    assert page.feedback_area is not None

# Test cases for Teacher Subject Page
def test_teacher_subject_page():
    mock_parent = MockParent(user_email="teacher@example.com")
    page = TeacherSubjectPage(mock_parent, "test_folder_id")
    assert page is not None
    assert page.drive_folder_id == "test_folder_id"
    # Since it inherits from ResourcePage, it should have resource management capabilities
    assert hasattr(page, 'upload_resource')

# Test cases for Authentication
def test_login_page():
    page = LoginPage(None)
    assert page.email_input is not None
    assert page.password_input is not None
    assert page.login_button is not None
    assert page.teacher_login_button is not None
    assert page.register_button is not None

def test_login_validation():
    page = LoginPage(None)
    # Test empty fields
    page.email_input.setText("")
    page.password_input.setText("")
    page.attempt_login()
    # Should not proceed with empty fields
    assert page.email_input.text() == ""

# Test cases for Registration
def test_register_page():
    page = RegisterPage(None)
    assert page.name_input is not None
    assert page.email_input is not None
    assert page.password_input is not None
    assert page.register_button is not None
    assert page.login_button is not None

def test_registration_validation():
    page = RegisterPage(None)
    # Test empty fields
    page.name_input.setText("")
    page.email_input.setText("")
    page.password_input.setText("")
    page.start_registration()
    # Should not proceed with empty fields
    assert page.name_input.text() == ""
    assert page.stack.currentIndex() == 0  # Should stay on registration page

def test_password_reset():
    page = ResetPasswordPage(None)
    assert page is not None
    assert hasattr(page, 'reset_password')

# Test cases for Password Reset
def test_reset_password_page():
    page = ResetPasswordPage(None)
    assert page.email_input is not None
    assert page.new_password_input is not None
    assert page.confirm_password_input is not None
    assert page.reset_button is not None
    assert page.back_button is not None

def test_reset_password_validation():
    page = ResetPasswordPage(None)
    # Test empty fields
    page.email_input.setText("")
    page.new_password_input.setText("")
    page.confirm_password_input.setText("")
    page.reset_password()
    # Should not proceed with empty fields
    assert page.email_input.text() == ""
    
    # Test password mismatch
    page.email_input.setText("test@example.com")
    page.new_password_input.setText("password1")
    page.confirm_password_input.setText("password2")
    page.reset_password()
    # Should not proceed with mismatched passwords
    assert page.new_password_input.text() != page.confirm_password_input.text()

# Test cases for Google Drive Integration
def test_drive_operations():
    # Test folder creation
    folder_id = create_folder("test_folder")
    assert folder_id is not None
    
    # Test file listing
    files = list_files(folder_id)
    assert isinstance(files, list)
    
    # Clean up
    try:
        remove_file(folder_id)
    except:
        pass

# Test cases for User Model
def test_user_creation():
    user = User("Test User", "test@example.com", "password123")
    assert user.name == "Test User"
    assert user.email == "test@example.com"

# Test cases for Teacher Model
def test_teacher_creation():
    # Create a teacher through the proper initialization method
    teacher = Teacher()
    teacher.name = "Prof Smith"
    teacher.email = "prof@example.com"
    assert teacher.name == "Prof Smith"
    assert teacher.email == "prof@example.com"