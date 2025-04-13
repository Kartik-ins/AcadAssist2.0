from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QListWidget, QCheckBox, QMessageBox, QHBoxLayout, QFrame, QScrollArea
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

import os
import psycopg2
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

# === FIXED INTERESTS ===
FIXED_INTERESTS = ["math", "physics", "chemistry", "cs", "biology", "english",
    "artificial intelligence", "machine learning", "data science",
    "algorithms", "data structures", "computer networks",
    "operating systems", "database systems", "software engineering",
    "web development", "mobile development", "cybersecurity",
    "cloud computing", "blockchain", "computer graphics",
    "human-computer interaction", "internet of things",
    "big data", "natural language processing", "computer vision"]

# === DB CONNECTION ===
def get_conn():
    load_dotenv()
    db_url = os.getenv("DB_URL")
    return psycopg2.connect(db_url)

# === INIT INTEREST TABLE ===
def init_interests():
    conn = get_conn()
    cur = conn.cursor()
    for interest in FIXED_INTERESTS:
        cur.execute("INSERT INTO interests (interest) VALUES (%s) ON CONFLICT DO NOTHING;", (interest,))
    conn.commit()
    cur.close()
    conn.close()

# === STUDENT-INTEREST MATRIX ===
def get_student_interest_matrix():
    conn = get_conn()
    query = """
        SELECT s.id AS student_id, i.interest
        FROM student_interests si
        JOIN students s ON si.student_id = s.id
        JOIN interests i ON si.interest_id = i.id;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return pd.crosstab(df['student_id'], df['interest'])

# === FIND SIMILAR STUDENTS ===
def find_similar_students(target_student_id, top_n=5):
    matrix = get_student_interest_matrix()
    if target_student_id not in matrix.index:
        return []

    svd = TruncatedSVD(n_components=min(5, matrix.shape[1]))
    reduced = svd.fit_transform(matrix)

    idx = list(matrix.index).index(target_student_id)
    sims = cosine_similarity([reduced[idx]], reduced)[0]
    sim_scores = list(zip(matrix.index, sims))
    sim_scores = sorted(sim_scores, key=lambda x: -x[1])
    top_matches = [(sid, score) for sid, score in sim_scores if sid != target_student_id][:top_n]

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM students WHERE id IN %s;", (tuple(s[0] for s in top_matches),))
    id_name_map = {row[0]: row[1] for row in cur.fetchall()}
    cur.close()
    conn.close()

    return [(id_name_map[sid], round(score, 2)) for sid, score in top_matches]


# === STUDY GROUP PAGE ===
class StudyGroupPage(QWidget):
    def __init__(self, parent=None, user_email=None):
        super().__init__()
        self.parent = parent
        self.user_email = user_email
        self.student_id = None  # Will be set in load_user_interests
        init_interests()
        
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
        feature_label = QLabel("Study Group Matcher")
        feature_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        feature_label.setStyleSheet("color: white; margin-top: 30px;")
        feature_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        feature_desc = QLabel("Find like-minded peers for\ncollaborative learning")
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
        
        # Right side (study group content)
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(40, 40, 40, 40)
        
        # Study group content container
        content_container = QFrame()
        content_container.setMaximumWidth(800)
        content_layout = QVBoxLayout(content_container)
        content_layout.setSpacing(20)
        
        # Title
        title = QLabel("Study Group Matcher")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # User info label
        self.info_label = QLabel("Loading user info...")
        self.info_label.setFont(QFont("Arial", 12))
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Interests section
        interests_label = QLabel("Select Your Academic Interests:")
        interests_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        
        # Create a scrollable area for checkboxes
        interests_scroll = QScrollArea()
        interests_scroll.setWidgetResizable(True)
        interests_scroll.setStyleSheet("""
            QScrollArea {
                border: 1px solid #333;
                border-radius: 4px;
                background-color: #1E1E1E;
            }
        """)
        
        interests_widget = QWidget()
        interests_layout = QVBoxLayout(interests_widget)
        interests_layout.setSpacing(10)
        
        self.checkboxes = []
        for interest in FIXED_INTERESTS:
            checkbox = QCheckBox(interest)
            checkbox.setFont(QFont("Arial", 12))
            checkbox.setStyleSheet("""
                QCheckBox {
                    color: white;
                    padding: 5px;
                }
                QCheckBox:hover {
                    background-color: #333;
                    border-radius: 4px;
                }
            """)
            self.checkboxes.append(checkbox)
            interests_layout.addWidget(checkbox)
        
        interests_scroll.setWidget(interests_widget)
        interests_scroll.setMinimumHeight(300)
        
        # Action buttons layout
        buttons_layout = QHBoxLayout()
        
        # Save button
        self.save_button = QPushButton("Save / Update Interests")
        self.save_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.save_button.setMinimumHeight(40)
        self.save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_button.clicked.connect(self.save_interests)
        
        # Find matches button
        self.match_button = QPushButton("Find Matching Students")
        self.match_button.setFont(QFont("Arial", 12))
        self.match_button.setMinimumHeight(40)
        self.match_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.match_button.clicked.connect(self.find_groups)
        
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.match_button)
        
        # Results section
        results_label = QLabel("Top Matches:")
        results_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        
        self.group_list = QListWidget()
        self.group_list.setFont(QFont("Arial", 12))
        self.group_list.setMinimumHeight(150)
        self.group_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #333;
                border-radius: 4px;
                background-color: #1E1E1E;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 2px;
            }
            QListWidget::item:selected {
                background-color: #2196F3;
            }
        """)
        
        # Add elements to container
        content_layout.addWidget(title)
        content_layout.addWidget(self.info_label)
        content_layout.addSpacing(10)
        content_layout.addWidget(interests_label)
        content_layout.addWidget(interests_scroll)
        content_layout.addLayout(buttons_layout)
        content_layout.addSpacing(10)
        content_layout.addWidget(results_label)
        content_layout.addWidget(self.group_list)
        
        # Add content container to right panel
        right_layout.addWidget(content_container, 1)
        
        # Add both panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)  # Right panel takes remaining space
        
        # Only load interests if we have a user email
        if self.user_email:
            self.load_user_interests()
        else:
            self.info_label.setText("Please log in to use the Study Group Matcher")
            self.save_button.setEnabled(False)
            self.match_button.setEnabled(False)
            for cb in self.checkboxes:
                cb.setEnabled(False)

    def load_user_interests(self):
        if not self.user_email:
            QMessageBox.critical(self, "Error", "No user email provided.")
            return

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM students WHERE email = %s;", (self.user_email,))
        result = cur.fetchone()

        if not result:
            return

        self.student_id = result[0]
        self.info_label.setText(f"Logged in as: {result[1]} ({self.user_email})")

        cur.execute("""
            SELECT i.interest
            FROM student_interests si
            JOIN interests i ON si.interest_id = i.id
            WHERE si.student_id = %s;
        """, (self.student_id,))
        selected = {row[0] for row in cur.fetchall()}

        for cb in self.checkboxes:
            cb.setChecked(cb.text() in selected)

        cur.close()
        conn.close()

    def save_interests(self):
        if not self.student_id:
            QMessageBox.critical(self, "Error", "Student ID not loaded.")
            return

        selected = [cb.text() for cb in self.checkboxes if cb.isChecked()]
        if not selected:
            QMessageBox.warning(self, "Input Error", "Please select at least one interest.")
            return

        try:
            conn = get_conn()
            cur = conn.cursor()

            cur.execute("DELETE FROM student_interests WHERE student_id = %s;", (self.student_id,))
            for interest in selected:
                cur.execute("SELECT id FROM interests WHERE interest = %s;", (interest,))
                interest_id = cur.fetchone()[0]
                cur.execute("INSERT INTO student_interests (student_id, interest_id) VALUES (%s, %s);", (self.student_id, interest_id))

            conn.commit()
            cur.close()
            conn.close()
            QMessageBox.information(self, "Success", "Your interests were updated successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def find_groups(self):
        if not self.student_id:
            QMessageBox.critical(self, "Error", "Student ID not loaded.")
            return

        try:
            matches = find_similar_students(self.student_id)
            self.group_list.clear()

            if not matches:
                self.group_list.addItem("No similar students found.")
            else:
                for m_name, score in matches:
                    self.group_list.addItem(f"{m_name} (Similarity: {score})")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
