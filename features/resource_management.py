from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QFileDialog, 
    QMessageBox, QHBoxLayout, QFrame, QScrollArea, QGridLayout, QSizePolicy,
    QListWidgetItem, QInputDialog
)
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize
from utils.google_drive_utils import list_files, upload_file, download_file, remove_file
from models.teacher import Teacher
import os

class ResourceCard(QFrame):
    def __init__(self, file_name, file_id, parent=None):
        super().__init__(parent)
        self.file_id = file_id
        self.file_name = file_name
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        self.setFixedHeight(100)
        self.setStyleSheet("""
            QFrame {
                background-color: #282828;
                border-radius: 8px;
                border: 1px solid #333;
            }
            QFrame:hover {
                border: 1px solid #4CAF50;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        
        # File icon based on extension
        icon_label = QLabel()
        icon_label.setFixedSize(40, 40)
        
        extension = self.file_name.split(".")[-1].lower() if "." in self.file_name else ""
        icon_path = self.get_file_icon(extension)
        
        if icon_path and os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            icon_label.setPixmap(pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            icon_label.setText("📄")
            icon_label.setStyleSheet("font-size: 24px;")
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # File details
        details_layout = QVBoxLayout()
        
        name_label = QLabel(self.file_name)
        name_label.setStyleSheet("font-weight: bold; font-size: 14px; color: white;")
        
        id_label = QLabel(f"ID: {self.file_id}")
        id_label.setStyleSheet("color: #AAAAAA; font-size: 10px;")
        
        details_layout.addWidget(name_label)
        details_layout.addWidget(id_label)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        
        download_btn = QPushButton("Download")
        download_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        download_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        download_btn.clicked.connect(self.download)
        
        remove_btn = QPushButton("Remove")
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        """)
        remove_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        remove_btn.clicked.connect(self.remove)
        
        # Show remove button only for teachers
        if self.parent and self.parent.is_teacher:
            buttons_layout.addWidget(download_btn)
            buttons_layout.addWidget(remove_btn)
        else:
            buttons_layout.addStretch()
            buttons_layout.addWidget(download_btn)
            
        # Add all sections to main layout
        layout.addWidget(icon_label)
        layout.addLayout(details_layout, 1)
        layout.addLayout(buttons_layout)
    
    def get_file_icon(self, extension):
        # Return appropriate icon path based on file extension
        # Replace these paths with actual paths to your icons if you have them
        extensions = {
            'pdf': 'icons/pdf.png',
            'doc': 'icons/doc.png',
            'docx': 'icons/doc.png',
            'ppt': 'icons/ppt.png',
            'pptx': 'icons/ppt.png',
            'xls': 'icons/xls.png',
            'xlsx': 'icons/xls.png',
            'txt': 'icons/txt.png',
            'jpg': 'icons/img.png',
            'jpeg': 'icons/img.png',
            'png': 'icons/img.png',
        }
        return extensions.get(extension, 'icons/generic.png')
    
    def download(self):
        try:
            # Open file dialog to select download directory
            download_dir = QFileDialog.getExistingDirectory(self, "Select Download Location", os.path.expanduser("~"))
            
            if download_dir:  # If user selected a directory
                destination_path = os.path.join(download_dir, self.file_name)
                download_file(self.file_id, destination_path)
                QMessageBox.information(self, "Success", f"File downloaded to {destination_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to download file: {str(e)}")
    
    def remove(self):
        if not self.parent.is_teacher:
            QMessageBox.warning(self, "Permission Denied", "Only teachers can remove resources.")
            return
        
        reply = QMessageBox.question(
            self, 
            "Confirm Deletion", 
            f"Are you sure you want to delete {self.file_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                remove_file(self.file_id)
                QMessageBox.information(self, "Success", "Resource removed successfully.")
                self.parent.load_resources()  # Refresh the list
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to remove resource: {str(e)}")

class ResourcePage(QWidget):
    def __init__(self, parent, drive_folder_id):
        super().__init__()
        self.parent = parent
        self.drive_folder_id = drive_folder_id
        print(f"ResourcePage initialized with drive_folder_id: {self.drive_folder_id}")  # Debugging

        # Check if the current user is a teacher
        self.is_teacher = parent.user_email and Teacher.get_teacher_by_email(parent.user_email) is not None
        
        # Main layout with centering
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
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
        
        # Feature highlight
        feature_label = QLabel("Resource Management")
        feature_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        feature_label.setStyleSheet("color: white; margin-top: 30px;")
        feature_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        feature_desc = QLabel("Access and share educational\nresources seamlessly")
        feature_desc.setFont(QFont("Arial", 12))
        feature_desc.setStyleSheet("color: #90CAF9;")
        feature_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        left_layout.addStretch()
        left_layout.addWidget(app_label)
        left_layout.addWidget(subtitle)
        left_layout.addSpacing(40)
        left_layout.addWidget(feature_label)
        left_layout.addWidget(feature_desc)
        left_layout.addStretch()
        
        # Right side (resource content)
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setStyleSheet("background-color: #1E1E1E;")
        header.setFixedHeight(80)
        header_layout = QHBoxLayout(header)
        
        title = QLabel("Resource Management")
        title.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        
        header_layout.addWidget(title)
        
        if self.is_teacher:
            header_layout.addStretch(1)
            create_folder_btn = QPushButton("Create Folder")
            create_folder_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #388E3C;
                }
            """)
            create_folder_btn.clicked.connect(self.create_folder)
            header_layout.addWidget(create_folder_btn)
        
        right_layout.addWidget(header)
        
        # Content area
        content_area = QFrame()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # Resource actions
        actions_frame = QFrame()
        actions_frame.setStyleSheet("background-color: #282828; border-radius: 8px;")
        actions_layout = QHBoxLayout(actions_frame)
        
        # Upload button - available to all users
        self.upload_button = QPushButton("Upload Resource")
        self.upload_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.upload_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.upload_button.clicked.connect(self.upload_resource)
        
        actions_layout.addWidget(self.upload_button)
        actions_layout.addStretch()
        
        # Resources container with scroll area
        resources_scroll = QScrollArea()
        resources_scroll.setWidgetResizable(True)
        resources_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #2A2A2A;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #616161;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        self.resources_container = QWidget()
        self.resources_layout = QVBoxLayout(self.resources_container)
        self.resources_layout.setSpacing(12)
        self.resources_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        resources_scroll.setWidget(self.resources_container)
        
        # Empty state message
        self.empty_message = QLabel("No resources found. Upload resources to get started.")
        self.empty_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_message.setStyleSheet("color: #AAAAAA; font-size: 16px; margin: 40px;")
        self.resources_layout.addWidget(self.empty_message)
        
        content_layout.addWidget(actions_frame)
        content_layout.addWidget(resources_scroll, 1)
        
        right_layout.addWidget(content_area, 1)
        
        # Add both panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)  # Right panel takes remaining space
        
        self.load_resources()

    def load_resources(self):
        """Load resources from Google Drive with modern card-based UI."""
        try:
            print(f"Loading resources from folder ID: {self.drive_folder_id}")
            files = list_files(self.drive_folder_id)
            
            # Clear existing resources
            while self.resources_layout.count():
                item = self.resources_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            
            # Show empty message if no files
            if not files:
                self.empty_message = QLabel("No resources found. Upload resources to get started.")
                self.empty_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.empty_message.setStyleSheet("color: #AAAAAA; font-size: 16px; margin: 40px;")
                self.resources_layout.addWidget(self.empty_message)
                return
            
            # Add resource cards
            for file in files:
                card = ResourceCard(file['name'], file['id'], self)
                self.resources_layout.addWidget(card)
                
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def upload_resource(self):
        """Upload a resource to Google Drive."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Upload")
        if file_path:
            try:
                file_name = file_path.split("/")[-1].split("\\")[-1]  # Handle both path formats
                upload_file(file_path, file_name, self.drive_folder_id)
                QMessageBox.information(self, "Success", "File uploaded successfully.")
                self.load_resources()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to upload file: {str(e)}")
    
    def create_folder(self):
        """Create a new folder (available only to teachers)"""
        if not self.is_teacher:
            QMessageBox.warning(self, "Permission Denied", "Only teachers can create folders.")
            return
        
        folder_name, ok = QInputDialog.getText(
            self, "Create Folder", "Enter folder name:"
        )
        
        if ok and folder_name:
            # This is a placeholder - the actual folder creation would require modifying 
            # the Google Drive utilities to support folder creation functionality
            QMessageBox.information(self, "Feature Coming Soon", 
                                   "Folder creation will be available in a future update.")