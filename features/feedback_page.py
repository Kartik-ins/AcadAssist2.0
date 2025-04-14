from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, 
    QMessageBox, QFrame, QScrollArea, QComboBox, QHBoxLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

class FeedbackPage(QWidget):
    def __init__(self, parent, is_teacher=False):
        super().__init__()
        self.parent = parent
        self.is_teacher = is_teacher
        print(f"Initializing FeedbackPage. Is teacher: {is_teacher}")  # Debug print
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        
        # Title with different text for student/teacher
        title = QLabel("Submit Your Feedback" if not is_teacher else "View Student Feedbacks")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2196F3; margin-bottom: 20px;")
        main_layout.addWidget(title)

        # Create different layouts based on user type
        if not is_teacher:
            self.setup_student_view(main_layout)
        else:
            self.setup_teacher_view(main_layout)

    def setup_student_view(self, main_layout):
        """Setup the feedback submission interface for students"""
        description = QLabel("Your feedback helps us improve. All feedback is anonymous.")
        description.setFont(QFont("Arial", 12))
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setStyleSheet("color: #90CAF9; margin-bottom: 20px;")
        
        # Category selector
        category_label = QLabel("Select Category:")
        category_label.setFont(QFont("Arial", 12))
        
        self.category_selector = QComboBox()
        self.category_selector.addItems([
            "General Feedback",
            "Course Content",
            "Teaching Methods",
            "Technical Issues",
            "Suggestions"
        ])
        self.category_selector.setFont(QFont("Arial", 12))
        self.category_selector.setMinimumHeight(40)
        self.category_selector.setStyleSheet("""
            QComboBox {
                background-color: #1E1E1E;
                color: white;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 8px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #fff;
                margin-right: 8px;
            }
        """)
        
        # Feedback input
        self.feedback_input = QTextEdit()
        self.feedback_input.setPlaceholderText("Type your feedback here...")
        self.feedback_input.setMinimumHeight(200)
        self.feedback_input.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: white;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        
        # Submit button
        self.submit_button = QPushButton("Submit Feedback")
        self.submit_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.submit_button.setMinimumHeight(50)
        self.submit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.submit_button.clicked.connect(self.submit_feedback)
        
        # Guidelines
        guidelines = QLabel(
            "Guidelines:\n"
            "• Your feedback will be shared anonymously with teachers\n"
            "• Be constructive and specific\n"
            "• Focus on improvements"
        )
        guidelines.setStyleSheet("color: #90CAF9; padding: 15px;")
        guidelines.setFont(QFont("Arial", 11))
        guidelines.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add widgets to layout
        main_layout.addWidget(description)
        main_layout.addWidget(category_label)
        main_layout.addWidget(self.category_selector)
        main_layout.addWidget(self.feedback_input)
        main_layout.addWidget(self.submit_button)
        main_layout.addWidget(guidelines)

    def setup_teacher_view(self, main_layout):
        """Setup the feedback viewing interface for teachers"""
        description = QLabel("View and filter student feedback submissions")
        description.setFont(QFont("Arial", 12))
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setStyleSheet("color: #90CAF9; margin-bottom: 20px;")
        main_layout.addWidget(description)
        
        # Filter controls container
        filter_frame = QFrame()
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(0, 0, 0, 20)
        
        filter_label = QLabel("Filter by Category:")
        filter_label.setFont(QFont("Arial", 12))
        
        self.filter_selector = QComboBox()
        self.filter_selector.addItems([
            "All Feedbacks",
            "General Feedback",
            "Course Content",
            "Teaching Methods",
            "Technical Issues",
            "Suggestions"
        ])
        self.filter_selector.setFont(QFont("Arial", 12))
        self.filter_selector.setMinimumHeight(40)
        self.filter_selector.setStyleSheet("""
            QComboBox {
                background-color: #1E1E1E;
                color: white;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 8px;
                min-width: 200px;
            }
        """)
        self.filter_selector.currentTextChanged.connect(self.load_feedbacks)
        
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setFont(QFont("Arial", 12))
        self.refresh_button.setMinimumHeight(40)
        self.refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 8px;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.refresh_button.clicked.connect(self.load_feedbacks)
        
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_selector)
        filter_layout.addWidget(self.refresh_button)
        filter_layout.addStretch()
        
        main_layout.addWidget(filter_frame)
        
        # Feedback list area
        self.feedback_area = QScrollArea()
        self.feedback_area.setWidgetResizable(True)
        self.feedback_area.setStyleSheet("""
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
        """)
        
        feedback_content = QWidget()
        self.feedback_list_layout = QVBoxLayout(feedback_content)
        self.feedback_list_layout.setSpacing(10)
        self.feedback_area.setWidget(feedback_content)
        
        main_layout.addWidget(self.feedback_area)
        
        self.load_feedbacks()

    def submit_feedback(self):
        """Submit feedback (student only)"""
        if self.is_teacher:
            print("Teacher attempted to submit feedback - blocked") # Debug print
            return
            
        feedback_text = self.feedback_input.toPlainText().strip()
        category = self.category_selector.currentText()
        
        if not feedback_text:
            QMessageBox.warning(self, "Error", "Please enter your feedback before submitting.")
            return
        
        try:
            conn = psycopg2.connect(os.getenv("DB_URL"))
            cur = conn.cursor()
            
            cur.execute(
                "INSERT INTO feedbacks (feedback_text, category) VALUES (%s, %s);",
                (feedback_text, category)
            )
            conn.commit()
            
            cur.close()
            conn.close()
            
            QMessageBox.information(self, "Success", "Thank you for your feedback!")
            self.feedback_input.clear()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to submit feedback: {str(e)}")

    def load_feedbacks(self):
        """Load and display feedbacks (teacher only)"""
        if not self.is_teacher:
            print("Student attempted to load feedbacks - blocked") # Debug print
            return
            
        while self.feedback_list_layout.count():
            item = self.feedback_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        try:
            conn = psycopg2.connect(os.getenv("DB_URL"))
            cur = conn.cursor()
            
            selected_category = self.filter_selector.currentText()
            print(f"Loading feedbacks for category: {selected_category}")  # Debug print
            
            if selected_category == "All Feedbacks":
                cur.execute("SELECT feedback_text, category FROM feedbacks ORDER BY category;")
            else:
                cur.execute(
                    "SELECT feedback_text, category FROM feedbacks WHERE category = %s ORDER BY feedback_text;",
                    (selected_category,)
                )
            
            feedbacks = cur.fetchall()
            print(f"Found {len(feedbacks)} feedback(s)") 
            if not feedbacks:
                no_feedback_label = QLabel("No feedbacks available")
                no_feedback_label.setFont(QFont("Arial", 12))
                no_feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                no_feedback_label.setStyleSheet("color: #666;")
                self.feedback_list_layout.addWidget(no_feedback_label)
            else:
                current_category = None
                for feedback_text, category in feedbacks:
                    if selected_category == "All Feedbacks" and current_category != category:
                        # Add category header when showing all feedbacks
                        category_label = QLabel(category or "Uncategorized")
                        category_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
                        category_label.setStyleSheet("color: #2196F3; margin-top: 10px;")
                        self.feedback_list_layout.addWidget(category_label)
                        current_category = category
                    
                    feedback_frame = QFrame()
                    feedback_frame.setStyleSheet("""
                        QFrame {
                            background-color: #2A2A2A;
                            border-radius: 8px;
                            padding: 16px;
                            margin: 4px 0;
                        }
                    """)
                    
                    frame_layout = QVBoxLayout(feedback_frame)
                    feedback_label = QLabel(feedback_text)
                    feedback_label.setWordWrap(True)
                    feedback_label.setFont(QFont("Arial", 12))
                    feedback_label.setStyleSheet("color: white;")
                    frame_layout.addWidget(feedback_label)
                    
                    self.feedback_list_layout.addWidget(feedback_frame)
            
            cur.close()
            conn.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load feedbacks: {str(e)}")