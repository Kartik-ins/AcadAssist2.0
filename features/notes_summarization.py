from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QFileDialog, QMessageBox, QHBoxLayout, QFrame
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

class NotesPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        
       
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: #0D47A1;")
        left_panel.setFixedWidth(400)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
       
        app_label = QLabel("AcadAssist")
        app_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        app_label.setStyleSheet("color: white;")
        app_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
  
        subtitle = QLabel("Your Academic Assistant")
        subtitle.setFont(QFont("Arial", 16))
        subtitle.setStyleSheet("color: #90CAF9;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        feature_label = QLabel("Notes Summarization")
        feature_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        feature_label.setStyleSheet("color: white; margin-top: 30px;")
        feature_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        feature_desc = QLabel("Convert lengthy notes into\nconcise, actionable summaries")
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
        
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(40, 40, 40, 40)
        
        notes_container = QFrame()
        notes_container.setMaximumWidth(800)
        notes_layout = QVBoxLayout(notes_container)
        notes_layout.setSpacing(20)
        
        title = QLabel("Notes Summarization")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        input_label = QLabel("Your Notes")
        input_label.setFont(QFont("Arial", 12))
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Paste your notes here...")
        self.notes_input.setMinimumHeight(200)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        # Upload button
        self.upload_button = QPushButton("Upload Notes")
        self.upload_button.setFont(QFont("Arial", 12))
        self.upload_button.setMinimumHeight(40)
        self.upload_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.upload_button.clicked.connect(self.upload_notes)
        
        # Summarize button
        self.summarize_button = QPushButton("Summarize Notes")
        self.summarize_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.summarize_button.setMinimumHeight(40)
        self.summarize_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.summarize_button.clicked.connect(self.summarize_notes)
        
        buttons_layout.addWidget(self.upload_button)
        buttons_layout.addWidget(self.summarize_button)
        
        # Summary output area
        summary_label = QLabel("Summary")
        summary_label.setFont(QFont("Arial", 12))
        self.summary_output = QTextEdit()
        self.summary_output.setReadOnly(True)
        self.summary_output.setPlaceholderText("Summary will appear here...")
        self.summary_output.setMinimumHeight(150)
        
        # Add widgets to notes container
        notes_layout.addWidget(title)
        notes_layout.addSpacing(10)
        notes_layout.addWidget(input_label)
        notes_layout.addWidget(self.notes_input)
        notes_layout.addLayout(buttons_layout)
        notes_layout.addWidget(summary_label)
        notes_layout.addWidget(self.summary_output)
        
        right_layout.addWidget(notes_container, 1)
        
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)  
    
    def upload_notes(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Notes File", filter="Text Files (*.txt)")
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                self.notes_input.setPlainText(file.read())
    
    def summarize_notes(self):
        notes = self.notes_input.toPlainText()
        if not notes.strip():
            QMessageBox.warning(self, "Error", "Please enter or upload notes to summarize.")
            return

        try:
            # Use Sumy for summarization
            parser = PlaintextParser.from_string(notes, Tokenizer("english"))
            summarizer = TextRankSummarizer()  # Switched to TextRank for better results
            summary = summarizer(parser.document, 5)  # Summarize into 5 sentences
            summary_text = "\n".join(str(sentence) for sentence in summary)
            if not summary_text.strip():
                summary_text = "The summarizer could not generate a summary. Please try with different notes."
            self.summary_output.setPlainText(summary_text)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to summarize notes: {str(e)}")
