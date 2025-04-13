from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QListWidget, QCheckBox, QMessageBox
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

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Study Group Matcher")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.info_label = QLabel("Loading user info...")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.checkboxes = [QCheckBox(interest) for interest in FIXED_INTERESTS]

        self.save_button = QPushButton("Save / Update Interests")
        self.save_button.clicked.connect(self.save_interests)

        self.match_button = QPushButton("Find Matching Students")
        self.match_button.clicked.connect(self.find_groups)

        self.group_list = QListWidget()

        layout.addWidget(title)
        layout.addWidget(self.info_label)
        for cb in self.checkboxes:
            layout.addWidget(cb)
        layout.addWidget(self.save_button)
        layout.addWidget(self.match_button)
        layout.addWidget(QLabel("Top Matches:"))
        layout.addWidget(self.group_list)

        self.setLayout(layout)

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
