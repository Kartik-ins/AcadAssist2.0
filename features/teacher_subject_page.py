from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFileDialog, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from utils.google_drive_utils import upload_file
from features.resource_management import ResourcePage

class TeacherSubjectPage(ResourcePage):
    def __init__(self, parent, drive_folder_id):
        print(f"TeacherSubjectPage initialized with drive_folder_id: {drive_folder_id}")  # Debugging
        super().__init__(parent, drive_folder_id)
