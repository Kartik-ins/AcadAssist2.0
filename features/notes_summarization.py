from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QFileDialog, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

class NotesPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        label = QLabel("Notes Summarization")
        label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Paste your notes here...")
        
        self.upload_button = QPushButton("Upload Notes")
        self.upload_button.clicked.connect(self.upload_notes)
        
        self.summarize_button = QPushButton("Summarize Notes")
        self.summarize_button.clicked.connect(self.summarize_notes)
        
        self.summary_output = QTextEdit()
        self.summary_output.setReadOnly(True)
        
        layout.addWidget(label)
        layout.addWidget(self.notes_input)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.summarize_button)
        layout.addWidget(self.summary_output)
        self.setLayout(layout)
    
    def upload_notes(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Notes File")
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