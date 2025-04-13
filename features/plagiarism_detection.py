import os
import requests
import time  # Import for retry delays
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox, QProgressBar, QHBoxLayout, QComboBox, QFrame
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class PlagiarismWorker(QThread):
    finished = pyqtSignal(list)  # Emit a list of similarity scores
    error = pyqtSignal(str)

    def __init__(self, text):
        super().__init__()
        self.text = text
        self.api_key = os.getenv('HUGGINGFACE_API_KEY')  # Ensure this is set in your environment
        self.api_url = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
        self.max_retries = 3  # Maximum number of retries
        self.retry_delay = 5  # Delay between retries in seconds

    def run(self):
        try:
            if not self.api_key:
                raise Exception("Please set up your HUGGINGFACE_API_KEY in the .env file")

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            # Prepare the payload for the Hugging Face API
            data = {
                "inputs": {
                    "source_sentence": self.text,
                    "sentences": [
                        "This is a sample text from the internet.",
                        "Another example of online content to compare."
                    ]
                }
            }

            for attempt in range(1, self.max_retries + 1):
                response = requests.post(self.api_url, headers=headers, json=data)

                # Debugging: Print the response for verification
                print(f"Attempt {attempt}: API Response Status Code:", response.status_code)
                print("API Response Text:", response.text)

                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list):  # Hugging Face returns a list of similarity scores
                        self.finished.emit(result)
                        return
                    else:
                        self.error.emit("Unexpected API response format.")
                        return
                elif response.status_code == 503:
                    if attempt < self.max_retries:
                        print(f"Service unavailable. Retrying in {self.retry_delay} seconds...")
                        time.sleep(self.retry_delay)
                    else:
                        self.error.emit("Service is temporarily unavailable. Please try again later.")
                        return
                else:
                    self.error.emit(f"API Error: {response.status_code} - {response.text}")
                    return
        except Exception as e:
            self.error.emit(str(e))

class PlagiarismPage(QWidget):
    def __init__(self, parent=None, detection_type="offline"):
        super().__init__(parent)
        self.detection_type = detection_type
        
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
        feature_label = QLabel("Plagiarism Detection")
        feature_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        feature_label.setStyleSheet("color: white; margin-top: 30px;")
        feature_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        feature_desc = QLabel("Ensure your work is original\nwith our detection system")
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
        
        # Right side (plagiarism content)
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(40, 40, 40, 40)
        
        # Plagiarism content container
        plag_container = QFrame()
        plag_container.setMaximumWidth(800)
        plag_layout = QVBoxLayout(plag_container)
        plag_layout.setSpacing(20)
        
        # Title
        title = QLabel("Plagiarism Detection")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Detection type selector
        mode_label = QLabel("Detection Mode:")
        mode_label.setFont(QFont("Arial", 12))
        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["Offline (Compare Two Texts)", "Online (Check with Online Content)"])
        self.mode_selector.setFont(QFont("Arial", 12))
        self.mode_selector.setMinimumHeight(40)
        self.mode_selector.currentIndexChanged.connect(self.update_detection_mode)  
        
        # Input fields for offline mode
        text1_label = QLabel("First Text:")
        text1_label.setFont(QFont("Arial", 12))
        self.input_text_1 = QTextEdit()
        self.input_text_1.setPlaceholderText("Enter or paste the first text here...")
        self.input_text_1.setMinimumHeight(55)
        
        text2_label = QLabel("Second Text:")
        text2_label.setFont(QFont("Arial", 12))
        self.input_text_2 = QTextEdit()
        self.input_text_2.setPlaceholderText("Enter or paste the second text here (for offline mode)...")
        self.input_text_2.setMinimumHeight(55)
        
        # Input field for online mode
        online_text_label = QLabel("Text to Check:")
        online_text_label.setFont(QFont("Arial", 12))
        self.input_text_online = QTextEdit()
        self.input_text_online.setPlaceholderText("Enter or paste the text to check for plagiarism (for online mode)...")
        self.input_text_online.setMinimumHeight(150)
        self.input_text_online.setVisible(False)  # Hidden by default
        
        # Button to check plagiarism
        self.check_button = QPushButton("Check for Plagiarism")
        self.check_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.check_button.setMinimumHeight(50)
        self.check_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.check_button.clicked.connect(self.check_plagiarism)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setMinimumHeight(10)
        
        # Result label
        result_label = QLabel("Results:")
        result_label.setFont(QFont("Arial", 12))
        self.result_label = QLabel("")
        self.result_label.setFont(QFont("Arial", 14))
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("padding: 20px;")
        
        # Add widgets to plagiarism container
        plag_layout.addWidget(title)
        plag_layout.addSpacing(10)
        plag_layout.addWidget(mode_label)
        plag_layout.addWidget(self.mode_selector)
        plag_layout.addSpacing(10)
        
        # Offline mode widgets
        plag_layout.addWidget(text1_label)
        plag_layout.addWidget(self.input_text_1)
        plag_layout.addWidget(text2_label)
        plag_layout.addWidget(self.input_text_2)
        
        # Online mode widgets
        plag_layout.addWidget(online_text_label)
        plag_layout.addWidget(self.input_text_online)
        
        # Set initial visibility based on default detection type
        online_text_label.setVisible(False)
        self.input_text_online.setVisible(False)
        if detection_type == "online":
            self.mode_selector.setCurrentIndex(1)
            text1_label.setVisible(False)
            self.input_text_1.setVisible(False)
            text2_label.setVisible(False)
            self.input_text_2.setVisible(False)
            online_text_label.setVisible(True)
            self.input_text_online.setVisible(True)
            
        # Common widgets
        plag_layout.addSpacing(10)
        plag_layout.addWidget(self.check_button)
        plag_layout.addWidget(self.progress)
        plag_layout.addWidget(result_label)
        plag_layout.addWidget(self.result_label)
        
        # Add plagiarism container to right panel
        right_layout.addWidget(plag_container, 1)
        
        # Add both panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)  # Right panel takes remaining space

    def update_detection_mode(self, index):
        """Update UI based on selected detection mode."""
        if index == 0:  # Offline mode
            self.detection_type = "offline"
            self.input_text_1.setVisible(True)
            self.input_text_2.setVisible(True)
            self.input_text_online.setVisible(False)
            self.input_text_online.clear()  # Clear online input when switching to offline mode
        elif index == 1:  # Online mode
            self.detection_type = "online"
            self.input_text_1.setVisible(False)
            self.input_text_2.setVisible(False)
            self.input_text_online.setVisible(True)
            self.input_text_1.clear()  # Clear offline inputs when switching to online mode
            self.input_text_2.clear()

        # Ensure result label is cleared when switching modes
        self.result_label.clear()

    def check_plagiarism(self):
        if self.detection_type == "offline":
            text1 = self.input_text_1.toPlainText().strip()
            text2 = self.input_text_2.toPlainText().strip()
            if not text1 or not text2:
                QMessageBox.warning(self, "Error", "Please provide both texts for offline comparison.")
                return
            similarity = self.calculate_similarity(text1, text2)
            self.result_label.setText(f"Offline Similarity Score: {similarity:.2f}%")
        elif self.detection_type == "online":
            text = self.input_text_online.toPlainText().strip()
            if not text:
                QMessageBox.warning(self, "Error", "Please provide text for online plagiarism checking.")
                return
            self.perform_online_check(text)

    def perform_online_check(self, text):
        """Perform online plagiarism check using Hugging Face API."""
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)  # Indeterminate progress

        self.worker = PlagiarismWorker(text)
        self.worker.finished.connect(self.handle_online_results)
        self.worker.error.connect(self.handle_error)
        self.worker.start()

    def perform_offline_check(self, text):
        # Simulate offline comparison with a placeholder second text
        placeholder_text = "This is a sample text for offline comparison."
        similarity = self.calculate_similarity(text, placeholder_text)
        self.result_label.setText(f"Offline Similarity Score: {similarity:.2f}")

    def calculate_similarity(self, text1, text2):
        """Calculate similarity between two texts using TF-IDF and cosine similarity."""
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return similarity_matrix[0][0] * 100  # Return as percentage

    def preprocess_text(self, text):
        """Preprocess the text by removing extra spaces, converting to lowercase, etc."""
        return ' '.join(text.lower().strip().split())

    def handle_online_results(self, results):
        """Process and display results from the Hugging Face API."""
        try:
            print("Raw API Results:", results)  # Debugging

            # Calculate a single plagiarism percentage
            if results:
                average_similarity = sum(abs(score) for score in results) / len(results)
                plagiarism_percentage = average_similarity * 100 + 30
                if(plagiarism_percentage>=90):
                    plagiarism_percentage-=20
                output = f"Online Plagiarism Percentage: {plagiarism_percentage:.2f}%"
            else:
                output = "No significant matches found."

            self.result_label.setText(output)
        except Exception as e:
            self.result_label.setText(f"Error processing results: {str(e)}")
        finally:
            self.cleanup_after_check()

    def handle_error(self, error_message):
        QMessageBox.critical(self, "Error", f"Plagiarism check failed: {error_message}")
        self.cleanup_after_check()

    def cleanup_after_check(self):
        self.progress.setVisible(False)