import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTextEdit, 
                           QPushButton, QScrollArea, QFrame, QProgressBar,
                           QMessageBox, QHBoxLayout)
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

chat_session = None

# Configure Gemini AI
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
    chat_session = model.start_chat(history=[])

class ChatWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, message):
        super().__init__()
        self.message = message

    def run(self):
        try:
            if not GOOGLE_API_KEY:
                raise Exception("Please set up your GOOGLE_API_KEY in the .env file")

            # Use global chat session to maintain context
            global chat_session
            if chat_session is None:
                # Start a new chat with initial educational system prompt
                system_context = (
                    "You are an educational AI assistant helping students with their studies. "
                    "Provide clear, accurate, and helpful responses. If appropriate, include examples "
                    "and break down complex topics into simpler parts."
                )
                chat_session = model.start_chat(history=[
                    {"role": "user", "parts": [system_context]}
                ])

            # Add the current user message to the ongoing chat
            response = chat_session.send_message(self.message)

            # Emit the assistant's reply
            self.finished.emit(response.text)

        except Exception as e:
            self.error.emit(str(e))

class ChatMessage(QFrame):
    def __init__(self, text, is_user=True):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Style the message bubble
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.setLineWidth(1)
        
        palette = self.palette()
        if is_user:
            palette.setColor(QPalette.ColorRole.Window, QColor("#E3F2FD"))
            self.setAutoFillBackground(True)
            self.setPalette(palette)
        else:
            palette.setColor(QPalette.ColorRole.Window, QColor("#F5F5F5"))
            self.setAutoFillBackground(True)
            self.setPalette(palette)

        # Message text
        message = QLabel(text)
        message.setWordWrap(True)
        message.setTextFormat(Qt.TextFormat.MarkdownText)
        layout.addWidget(message)

class ChatbotPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Title
        title = QLabel("AI Study Assistant")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Chat history area
        self.chat_area = QWidget()
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_area.setLayout(self.chat_layout)

        # Scroll area for chat
        scroll = QScrollArea()
        scroll.setWidget(self.chat_area)
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(400)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        
        # Input area
        self.chat_input = QTextEdit()
        self.chat_input.setPlaceholderText("Ask me anything about your studies...")
        self.chat_input.setMaximumHeight(100)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 5px;
                padding: 8px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        
        # Reset button
        self.reset_button = QPushButton("Reset Chat")
        self.reset_button.clicked.connect(self.reset_chat)
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border-radius: 5px;
                padding: 8px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        
        # Add buttons to layout
        buttons_layout.addWidget(self.send_button)
        buttons_layout.addWidget(self.reset_button)

        # Add initial welcome message
        welcome_msg = """Welcome! 👋 I'm your AI study assistant. I can help you with:
- Understanding difficult concepts
- Solving problems step by step
- Finding study resources
- Creating study plans
- Answering your questions

How can I help you today?"""
        self.add_message(welcome_msg, is_user=False)

        # Layout assembly
        layout.addWidget(title)
        layout.addWidget(scroll)
        layout.addWidget(self.progress)
        layout.addWidget(self.chat_input)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)

    def add_message(self, text, is_user=True):
        message = ChatMessage(text, is_user)
        self.chat_layout.addWidget(message)
        
        # Auto scroll to bottom
        QThread.msleep(100)  # Give time for layout to update
        scroll_area = self.chat_area.parent()
        if isinstance(scroll_area, QScrollArea):
            scroll_area.verticalScrollBar().setValue(
                scroll_area.verticalScrollBar().maximum()
            )

    def send_message(self):
        message = self.chat_input.toPlainText().strip()
        if not message:
            return

        # Disable input while processing
        self.chat_input.setReadOnly(True)
        self.send_button.setEnabled(False)
        self.reset_button.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)  # Infinite progress

        # Add user message to chat
        self.add_message(message, is_user=True)
        self.chat_input.clear()

        # Process in background
        self.worker = ChatWorker(message)
        self.worker.finished.connect(self.handle_response)
        self.worker.error.connect(self.handle_error)
        self.worker.start()

    def handle_response(self, response):
        self.add_message(response, is_user=False)
        self.cleanup_after_message()

    def handle_error(self, error_message):
        QMessageBox.critical(self, "Error", error_message)
        self.cleanup_after_message()

    def cleanup_after_message(self):
        self.chat_input.setReadOnly(False)
        self.send_button.setEnabled(True)
        self.reset_button.setEnabled(True)
        self.progress.setVisible(False)
        self.chat_input.setFocus()
        
    def reset_chat(self):
        # Clear all messages except the welcome message
        while self.chat_layout.count() > 0:
            item = self.chat_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Reset the model's conversation history
        global chat_session
        if GOOGLE_API_KEY:
            chat_session = model.start_chat(history=[])
        
        # Add welcome message again
        welcome_msg = """Welcome! 👋 I'm your AI study assistant. I can help you with:
- Understanding difficult concepts
- Solving problems step by step
- Finding study resources
- Creating study plans
- Answering your questions

How can I help you today?"""
        self.add_message(welcome_msg, is_user=False)
        
        # Clear input
        self.chat_input.clear()
        
        # Show confirmation
        QMessageBox.information(self, "Chat Reset", "Chat history has been cleared. You can start a new conversation.")