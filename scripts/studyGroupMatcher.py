import sys
import psycopg2
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QCheckBox, QMessageBox, QTextEdit
)
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv


# === FIXED INTERESTS ===
FIXED_INTERESTS = ["math", "physics", "chemistry", "cs", "biology", "english"]

# === DATABASE CONNECTION ===
import psycopg2
from dotenv import load_dotenv
import os

def get_conn():
    load_dotenv()
    db_url = os.getenv("DB_URL")
    return psycopg2.connect(db_url)


# === INIT INTEREST TABLE IF NEEDED ===
def init_interests():
    conn = get_conn()
    cur = conn.cursor()
    for interest in FIXED_INTERESTS:
        cur.execute("INSERT INTO interests (interest) VALUES (%s) ON CONFLICT DO NOTHING;", (interest,))
    conn.commit()
    cur.close()
    conn.close()

# === REGISTER STUDENT ===
def register_student(name, email, selected_interests):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name, email) VALUES (%s, %s) RETURNING id;", (name, email))
    student_id = cur.fetchone()[0]

    for interest in selected_interests:
        cur.execute("SELECT id FROM interests WHERE interest = %s;", (interest,))
        interest_id = cur.fetchone()[0]
        cur.execute(
            "INSERT INTO student_interests (student_id, interest_id) VALUES (%s, %s);",
            (student_id, interest_id)
        )

    conn.commit()
    cur.close()
    conn.close()
    return student_id

# === GET STUDENT-INTEREST MATRIX ===
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

# === SVD + RECOMMENDATION ===
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

# === PYQT5 GUI ===
class StudyMatcher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Study Group Matcher")
        self.setGeometry(100, 100, 400, 500)

        self.layout = QVBoxLayout()
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter your name")
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Enter your email")

        self.checkboxes = [QCheckBox(interest, self) for interest in FIXED_INTERESTS]

        self.submit_button = QPushButton("Register and Match", self)
        self.submit_button.clicked.connect(self.submit_form)

        self.results = QTextEdit(self)
        self.results.setReadOnly(True)

        self.layout.addWidget(QLabel("Name:"))
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(QLabel("Email:"))
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(QLabel("Select your interests:"))
        for cb in self.checkboxes:
            self.layout.addWidget(cb)

        self.layout.addWidget(self.submit_button)
        self.layout.addWidget(QLabel("Top Matches:"))
        self.layout.addWidget(self.results)
        self.setLayout(self.layout)

    def submit_form(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        interests = [cb.text() for cb in self.checkboxes if cb.isChecked()]

        if not name or not email or not interests:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        try:
            student_id = register_student(name, email, interests)
            matches = find_similar_students(student_id)
            if not matches:
                self.results.setText("No similar students found yet.")
            else:
                out = "\n".join([f"{name} (Similarity: {score})" for name, score in matches])
                self.results.setText(out)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

# === MAIN ENTRY POINT ===
if __name__ == "__main__":
    init_interests()  # one-time
    app = QApplication(sys.argv)
    window = StudyMatcher()
    window.show()
    sys.exit(app.exec_())
