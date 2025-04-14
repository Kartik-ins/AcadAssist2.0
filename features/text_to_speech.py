import os
from gtts import gTTS
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox, QHBoxLayout, QFrame,
    QComboBox, QFileDialog, QProgressBar, QScrollArea
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QThread, pyqtSignal

class TTSWorker(QThread):
    """Worker thread for text-to-speech conversion to keep UI responsive"""
    finished = pyqtSignal(str)  # Signal emitted when completed with the file path
    error = pyqtSignal(str)     # Signal emitted on error with error message

    def __init__(self, text, language, accent, save_path):
        super().__init__()
        self.text = text
        self.language = language
        self.accent = accent
        self.save_path = save_path

    def run(self):
        try:
            # Create gTTS object
            tts = gTTS(text=self.text, lang=self.language, tld=self.accent)
            
            # Save the audio file
            tts.save(self.save_path)
            
            # Emit the finished signal with the file path
            self.finished.emit(self.save_path)
            
        except Exception as e:
            # Emit error signal if something goes wrong
            self.error.emit(str(e))

class TextToSpeechPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
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
        app_label = QLabel("AcadAssist")
        app_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        app_label.setStyleSheet("color: white;")
        app_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # App subtitle
        subtitle = QLabel("Your Academic Assistant")
        subtitle.setFont(QFont("Arial", 16))
        subtitle.setStyleSheet("color: #90CAF9;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Feature highlight
        feature_label = QLabel("Text to Speech")
        feature_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        feature_label.setStyleSheet("color: white; margin-top: 30px;")
        feature_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        feature_desc = QLabel("Convert your text into natural\nsounding speech audio")
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
        
        # Right side (text-to-speech content)
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(40, 40, 40, 40)
        
        # TTS content container
        tts_container = QFrame()
        tts_container.setMaximumWidth(800)
        tts_layout = QVBoxLayout(tts_container)
        tts_layout.setSpacing(20)
        
        # Title
        title = QLabel("Text to Speech Converter")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Text input area
        input_label = QLabel("Enter Text:")
        input_label.setFont(QFont("Arial", 12))
        
        # Create a scrollable text area
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Enter or paste the text you want to convert to speech...")
        self.text_input.setMinimumHeight(200)
        
        # Language and accent selection
        options_layout = QHBoxLayout()
        
        # Language dropdown
        language_layout = QVBoxLayout()
        language_label = QLabel("Language:")
        language_label.setFont(QFont("Arial", 12))
        self.language_dropdown = QComboBox()
        self.language_dropdown.setFont(QFont("Arial", 12))
        self.language_dropdown.setMinimumHeight(40)
        
        # Add language options (code, display name)
        language_options = [
            ("en", "English"),
            ("fr", "French"),
            ("es", "Spanish"),
            ("de", "German"),
            ("it", "Italian"),
            ("ja", "Japanese"),
            ("ko", "Korean"),
            ("zh-CN", "Chinese (Simplified)"),
            ("hi", "Hindi"),
            ("ar", "Arabic")
        ]
        
        for code, name in language_options:
            self.language_dropdown.addItem(name, code)
        
        language_layout.addWidget(language_label)
        language_layout.addWidget(self.language_dropdown)
        
        # Accent dropdown
        accent_layout = QVBoxLayout()
        accent_label = QLabel("Accent:")
        accent_label.setFont(QFont("Arial", 12))
        self.accent_dropdown = QComboBox()
        self.accent_dropdown.setFont(QFont("Arial", 12))
        self.accent_dropdown.setMinimumHeight(40)
        
        # Add accent options (tld, display name)
        accent_options = [
            ("com", "US"),
            ("co.uk", "UK"),
            ("co.in", "India"),
            ("com.au", "Australia"),
            ("ca", "Canada"),
            ("ie", "Ireland")
        ]
        
        for tld, name in accent_options:
            self.accent_dropdown.addItem(name, tld)
        
        # Default to Indian English
        self.accent_dropdown.setCurrentText("India")
        
        accent_layout.addWidget(accent_label)
        accent_layout.addWidget(self.accent_dropdown)
        
        # Add both dropdowns to the options layout
        options_layout.addLayout(language_layout)
        options_layout.addLayout(accent_layout)
        
        # Upload text button
        upload_layout = QHBoxLayout()
        self.upload_button = QPushButton("Upload Text File")
        self.upload_button.setFont(QFont("Arial", 12))
        self.upload_button.setMinimumHeight(40)
        self.upload_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.upload_button.clicked.connect(self.upload_text_file)
        upload_layout.addWidget(self.upload_button)
        upload_layout.addStretch()
        
        # Convert button
        self.convert_button = QPushButton("Convert to Speech")
        self.convert_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.convert_button.setMinimumHeight(50)
        self.convert_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.convert_button.clicked.connect(self.convert_to_speech)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setMinimumHeight(10)
        
        # Status message
        self.status_label = QLabel("")
        self.status_label.setFont(QFont("Arial", 12))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #4CAF50;")
        
        # Add widgets to TTS container
        tts_layout.addWidget(title)
        tts_layout.addSpacing(10)
        tts_layout.addWidget(input_label)
        tts_layout.addWidget(self.text_input)
        tts_layout.addLayout(upload_layout)
        tts_layout.addLayout(options_layout)
        tts_layout.addSpacing(10)
        tts_layout.addWidget(self.convert_button)
        tts_layout.addWidget(self.progress)
        tts_layout.addWidget(self.status_label)
        
        # Add TTS container to right panel
        right_layout.addWidget(tts_container, 1)
        
        # Add both panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)  # Right panel takes remaining space
    
    def upload_text_file(self):
        """Open a file dialog to select and upload a .txt file for text-to-speech conversion."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Upload Text File",
            "",
            "Text Files (*.txt)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()
                    self.text_input.setPlainText(file_content)
                self.status_label.setText(f"File loaded: {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to read file: {str(e)}")
    
    def convert_to_speech(self):
        """Convert text to speech and save the audio file."""
        # Get the text input
        text = self.text_input.toPlainText().strip()
        
        if not text:
            QMessageBox.warning(self, "Error", "Please enter or upload text to convert.")
            return
        
        # Get selected language and accent
        language_idx = self.language_dropdown.currentIndex()
        language_code = self.language_dropdown.itemData(language_idx)
        
        accent_idx = self.accent_dropdown.currentIndex()
        accent_tld = self.accent_dropdown.itemData(accent_idx)
        
        # Open file dialog to choose save location and filename
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save audio file as",
            "",
            "MP3 Files (*.mp3)"
        )
        
        if not file_path:
            self.status_label.setText("File save operation cancelled.")
            return
            
        # Add .mp3 extension if not already present
        if not file_path.lower().endswith('.mp3'):
            file_path += '.mp3'
            
        # Show progress bar
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)  # Indeterminate progress
        self.status_label.setText("Converting text to speech...")
        
        # Disable the convert button while processing
        self.convert_button.setEnabled(False)
        
        # Start worker thread for TTS conversion
        self.worker = TTSWorker(text, language_code, accent_tld, file_path)
        self.worker.finished.connect(self.handle_conversion_complete)
        self.worker.error.connect(self.handle_conversion_error)
        self.worker.start()
    
    def handle_conversion_complete(self, file_path):
        """Handle successful text-to-speech conversion."""
        self.progress.setVisible(False)
        self.convert_button.setEnabled(True)
        self.status_label.setText(f"Audio saved to: {os.path.basename(file_path)}")
        QMessageBox.information(self, "Success", f"Audio file successfully saved to: {file_path}")
    
    def handle_conversion_error(self, error_message):
        """Handle error during text-to-speech conversion."""
        self.progress.setVisible(False)
        self.convert_button.setEnabled(True)
        self.status_label.setText(f"Error: {error_message}")
        QMessageBox.critical(self, "Error", f"Conversion failed: {error_message}")