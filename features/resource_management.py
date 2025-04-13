from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QFileDialog, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from utils.google_drive_utils import list_files, upload_file, download_file, remove_file
from models.teacher import Teacher

class ResourcePage(QWidget):
    def __init__(self, parent, drive_folder_id):
        super().__init__()
        self.parent = parent
        self.drive_folder_id = drive_folder_id
        print(f"ResourcePage initialized with drive_folder_id: {self.drive_folder_id}")  # Debugging

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel("Resource Management")
        label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.resource_list = QListWidget()
        self.resource_list.itemDoubleClicked.connect(self.download_resource)

        # Check if the current user is a teacher
        self.is_teacher = Teacher.get_teacher_by_email(self.parent.user_email) is not None

        # Add upload button for all users
        self.upload_button = QPushButton("Upload Resource")
        self.upload_button.clicked.connect(self.upload_resource)
        layout.addWidget(self.upload_button)

        # Only show remove button for teachers
        if self.is_teacher:
            self.remove_button = QPushButton("Remove Selected Resource")
            self.remove_button.clicked.connect(self.remove_resource)
            layout.addWidget(self.remove_button)

        layout.addWidget(label)
        layout.addWidget(self.resource_list)
        self.setLayout(layout)

        self.load_resources()

    def load_resources(self):
        """Load resources from Google Drive."""
        try:
            print(f"Loading resources from folder ID: {self.drive_folder_id}")  # Debugging
            files = list_files(self.drive_folder_id)
            self.resource_list.clear()
            for file in files:
                self.resource_list.addItem(f"{file['name']} (ID: {file['id']})")
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def upload_resource(self):
        """Upload a resource to Google Drive."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Upload")
        if file_path:
            try:
                file_name = file_path.split("/")[-1]
                upload_file(file_path, file_name, self.drive_folder_id)
                QMessageBox.information(self, "Success", "File uploaded successfully.")
                self.load_resources()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to upload file: {str(e)}")

    def remove_resource(self):
        """Remove a selected resource."""
        if not self.is_teacher:
            QMessageBox.warning(self, "Permission Denied", "Only teachers can remove resources.")
            return

        selected_item = self.resource_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Error", "Please select a resource to remove.")
            return

        try:
            file_id = selected_item.text().split("(ID: ")[1][:-1]
            remove_file(file_id)
            QMessageBox.information(self, "Success", "Resource removed successfully.")
            self.load_resources()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to remove resource: {str(e)}")

    def download_resource(self, item):
        """Download a selected resource."""
        try:
            file_id = item.text().split("(ID: ")[1][:-1]
            destination_path = f"./downloads/{item.text().split(' (ID: ')[0]}"
            download_file(file_id, destination_path)
            QMessageBox.information(self, "Success", f"File downloaded to {destination_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to download file: {str(e)}")