import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QScrollArea,
    QFrame, QProgressBar, QMessageBox, QHBoxLayout, QSizePolicy,
    QSpacerItem
)
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
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
        self.setup_ui(text, is_user)
        
    def setup_ui(self, text, is_user):
        # Set up main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 12, 20, 12)
        
        if is_user:
            main_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        else:
            main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            
        # Create message bubble
        bubble = QFrame()
        bubble_layout = QVBoxLayout(bubble)
        bubble_layout.setContentsMargins(16, 12, 16, 12)
        
        # Style the message bubble based on who sent it
        max_width = 550
        if is_user:
            bubble.setStyleSheet("""
                background-color: #2196F3;
                border-radius: 18px;
                border-top-right-radius: 4px;
            """)
            bubble.setMaximumWidth(max_width)
        else:
            bubble.setStyleSheet("""
                background-color: #424242;
                border-radius: 18px;
                border-top-left-radius: 4px;
            """)
            bubble.setMaximumWidth(max_width)
        
        # Message text
        message = QLabel(text)
        message.setWordWrap(True)
        message.setTextFormat(Qt.TextFormat.MarkdownText)
        if is_user:
            message.setStyleSheet("color: white; font-size: 14px;")
        else:
            message.setStyleSheet("color: white; font-size: 14px;")
        
        bubble_layout.addWidget(message)
        
        # Add spacer on the appropriate side to push the bubble to the correct side
        if is_user:
            main_layout.addStretch(1)
            main_layout.addWidget(bubble)
        else:
            main_layout.addWidget(bubble)
            main_layout.addStretch(1)

class ChatbotPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
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
        feature_label = QLabel("AI Study Assistant")
        feature_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        feature_label.setStyleSheet("color: white; margin-top: 30px;")
        feature_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        feature_desc = QLabel("Get instant help with your studies\nand answers to academic questions")
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
        
        # Right side (chatbot content)
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 20)
        right_layout.setSpacing(20)
        
        # Header
        header = QFrame()
        header.setStyleSheet("background-color: #1E1E1E;")
        header.setFixedHeight(80)
        header_layout = QHBoxLayout(header)
        
        title = QLabel("AI Study Assistant")
        title.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        
        header_layout.addWidget(title)
        right_layout.addWidget(header)
        
        # Create chat messages area with container widget for messages
        self.chat_area = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_area)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_layout.setSpacing(16)
        self.chat_layout.setContentsMargins(0, 20, 0, 20)
        
        # Chat scroll area
        chat_scroll = QScrollArea()
        chat_scroll.setWidgetResizable(True)
        chat_scroll.setWidget(self.chat_area)
        chat_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        chat_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #121212;
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
        self.chat_scroll = chat_scroll
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setFixedHeight(3)
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: transparent;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
            }
        """)
        self.progress.setVisible(False)
        
        # Input container
        input_container = QFrame()
        input_container.setStyleSheet("background-color: #1E1E1E; border-radius: 8px;")
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(16, 10, 16, 10)
        
        # Chat text input
        self.chat_input = QTextEdit()
        self.chat_input.setStyleSheet("""
            QTextEdit {
                border: none;
                background-color: transparent;
                color: white;
                font-size: 14px;
            }
        """)
        self.chat_input.setPlaceholderText("Ask me anything about your studies...")
        self.chat_input.setMaximumHeight(100)
        self.chat_input.setMinimumHeight(50)
        
        # Send button
        self.send_button = QPushButton()
        self.send_button.setIcon(QIcon.fromTheme("document-send"))
        self.send_button.setIconSize(QSize(24, 24))
        self.send_button.setFixedSize(40, 40)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        self.send_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_button.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.chat_input, 1)
        input_layout.addWidget(self.send_button)
        
        # Bottom actions panel
        bottom_panel = QFrame()
        bottom_layout = QHBoxLayout(bottom_panel)
        
        # Reset chat button
        self.reset_button = QPushButton("New Chat")
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #424242;
                color: white;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        self.reset_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_button.clicked.connect(self.reset_chat)
        
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(self.reset_button)
        
        # Add widgets to layout
        right_layout.addWidget(chat_scroll, 1)
        right_layout.addWidget(self.progress)
        right_layout.addWidget(input_container)
        right_layout.addWidget(bottom_panel)
        
        # Add both panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)  # Right panel takes remaining space
        
        # Add initial welcome message
        welcome_msg = """👋 **Welcome to AI Study Assistant!**

I can help you with:
• Understanding difficult concepts
• Solving problems step by step
• Finding study resources
• Creating personalized study plans
• Answering your questions

How can I help you with your studies today?"""
        self.add_message(welcome_msg, is_user=False)

    def add_message(self, text, is_user=True):
        message = ChatMessage(text, is_user)
        self.chat_layout.addWidget(message)
        
        # Auto scroll to bottom
        QThread.msleep(100)  # Give time for layout to update
        self.chat_scroll.verticalScrollBar().setValue(
            self.chat_scroll.verticalScrollBar().maximum()
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
        welcome_msg = """👋 **Welcome to AI Study Assistant!**

I can help you with:
• Understanding difficult concepts
• Solving problems step by step
• Finding study resources
• Creating personalized study plans
• Answering your questions

How can I help you with your studies today?"""
        self.add_message(welcome_msg, is_user=False)
        
        # Clear input
        self.chat_input.clear()