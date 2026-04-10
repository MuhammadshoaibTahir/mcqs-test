import streamlit as st
import pandas as pd
import random
from datetime import datetime
import os
import time

# ================== CONFIG ==================
EXAM_DURATION_MINUTES = 20

ADMIN_SECRET_KEY = "shoaib123"
RESULTS_CSV = "results.csv"
RESULTS_XLSX = "results.xlsx"

# ================== STUDENTS ==================
STUDENTS = {
    "FA22-BEN-001": "FAIZ RASOOL",
    "FA22-BEN-002": "EEMAN SALEEM",
    "FA22-BEN-004": "EISAL FATIMA",
    "FA22-BEN-005": "MUHAMMAD ARHAM FAISAL",
    "FA22-BEN-006": "SITARA FATIMA",
    "FA22-BEN-007": "LABIQA FATIMA",
    "FA22-BEN-008": "BAKHTAWER RAO",
    "FA22-BEN-009": "FATIMA SALABAT",
    "FA22-BEN-011": "SHAKIRA IQBAL",
    "FA22-BEN-012": "AYESHA SANA",
    "FA22-BEN-015": "MUHAMMAD BILAL",
    "FA22-BEN-017": "MUHAMMAD ABDULLAH",
    "FA22-BEN-019": "ABDULLAH BIN ASIF",
    "FA22-BEN-020": "MUHAMMAD ALI",
    "FA22-BEN-021": "AYESHA IRSHAD",
    "FA22-BEN-023": "MUHAMMAD AWAIS",
    "FA22-BEN-024": "AREEBA",
    "FA22-BEN-025": "AREEBA TARIQ",
    "FA22-BEN-027": "JAVERIA RAO",
    "FA22-BEN-028": "UMER BILAL",
    "FA22-BEN-031": "KHADIJA PERVAIZ",
    "FA22-BEN-032": "EMAN IJAZ",
    "FA22-BEN-033": "MUQADAS SHAHZADI"
}

# ================== MCQs ==================
MCQ_QUESTIONS = [
    {
        "question": "Computational Linguistics is a field that combines:",
        "options": ["Biology and Chemistry", "Linguistics and Computer Science", "Physics and Math", "History and AI"],
        "correct": "Linguistics and Computer Science"
    },
    {
        "question": "Tokenization means:",
        "options": ["Removing stopwords", "Splitting text into units", "Assigning tags", "Parsing sentences"],
        "correct": "Splitting text into units"
    },
    {
        "question": "Which NLP stage assigns grammatical categories?",
        "options": ["Tokenization", "POS Tagging", "Parsing", "NER"],
        "correct": "POS Tagging"
    },
    {
        "question": "Which tag represents a noun?",
        "options": ["VB", "JJ", "NN", "RB"],
        "correct": "NN"
    },
    {
        "question": "Bigram model considers:",
        "options": ["No context", "One previous word", "Two previous words", "Whole sentence"],
        "correct": "One previous word"
    },
    {
        "question": "The main problem in n-gram models is:",
        "options": ["Parsing error", "Sparse data problem", "Tokenization issue", "Overfitting"],
        "correct": "Sparse data problem"
    },
    {
        "question": "In Python, list indexing starts from:",
        "options": ["1", "-1", "0", "Depends on list"],
        "correct": "0"
    },
    {
        "question": "What does list[::-1] do?",
        "options": ["Sort list", "Reverse list", "Delete elements", "Copy list"],
        "correct": "Reverse list"
    },
    {
        "question": "Negative indexing means:",
        "options": ["Error", "Counting from end", "Looping", "Skipping values"],
        "correct": "Counting from end"
    },
    {
        "question": "What does append() do?",
        "options": ["Removes element", "Adds element at end", "Sorts list", "Replaces element"],
        "correct": "Adds element at end"
    }
]

TOTAL_QUESTIONS = len(MCQ_QUESTIONS)

# ================== FUNCTIONS ==================
def load_results():
    if os.path.exists(RESULTS_CSV):
        return pd.read_csv(RESULTS_CSV)
    return pd.DataFrame(columns=["Name", "Roll", "Score", "Timestamp"])

def save_results(name, roll, score):
    df = load_results()
    new_row = pd.DataFrame([{
        "Name": name,
        "Roll": roll,
        "Score": score,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(RESULTS_CSV, index=False)
    df.to_excel(RESULTS_XLSX, index=False)

def has_student_attempted(roll):
    df = load_results()
    return roll in df["Roll"].values

def initialize_exam():
    if "questions" not in st.session_state:
        st.session_state.questions = random.sample(MCQ_QUESTIONS, len(MCQ_QUESTIONS))
        st.session_state.answers = {}
        st.session_state.current = 0
        st.session_state.start_time = time.time()
        st.session_state.submitted = False

def calculate_score():
    score = 0
    for i, q in enumerate(st.session_state.questions):
        if st.session_state.answers.get(i) == q["correct"]:
            score += 1
    return score

# ================== ADMIN ==================
def show_admin():
    st.title("Admin Dashboard")
    df = load_results()
    st.dataframe(df)

# ================== MAIN ==================
def main():
    st.set_page_config(page_title="MCQ Exam", page_icon="📝")

    # Admin
    if "admin" in st.query_params and st.query_params["admin"] == ADMIN_SECRET_KEY:
        show_admin()
        return

    # Login
    if "login" not in st.session_state:
        st.session_state.login = False

    if not st.session_state.login:
        st.title("Student Login")
        roll = st.text_input("Enter Roll Number").strip().upper()

        if st.button("Login"):
            if roll not in STUDENTS:
                st.error("Invalid Roll Number")
            elif has_student_attempted(roll):
                st.error("Already attempted")
            else:
                st.session_state.login = True
                st.session_state.name = STUDENTS[roll]
                st.session_state.roll = roll
                st.rerun()
        return

    # Exam
    initialize_exam()

    if st.session_state.submitted:
        st.success("Exam Submitted!")
        return

    # Timer
    elapsed = time.time() - st.session_state.start_time
    remaining = EXAM_DURATION_MINUTES * 60 - elapsed

    if remaining <= 0:
        score = calculate_score()
        save_results(st.session_state.name, st.session_state.roll, score)
        st.session_state.submitted = True
        st.rerun()

    mins, secs = divmod(int(remaining), 60)
    st.markdown(f"⏱️ Time Left: {mins:02d}:{secs:02d}")

    # Question
    i = st.session_state.current
    q = st.session_state.questions[i]

    st.markdown(f"### Q{i+1}. {q['question']}")

    ans = st.radio("Select:", q["options"], index=None)

    if ans:
        st.session_state.answers[i] = ans

    # Navigation
    col1, col2, col3 = st.columns(3)

    with col1:
        if i > 0 and st.button("Previous"):
            st.session_state.current -= 1
            st.rerun()

    with col2:
        if i < TOTAL_QUESTIONS - 1 and st.button("Next"):
            st.session_state.current += 1
            st.rerun()

    with col3:
        if st.button("Submit"):
            score = calculate_score()
            save_results(st.session_state.name, st.session_state.roll, score)
            st.session_state.submitted = True
            st.rerun()

    st.progress(len(st.session_state.answers) / TOTAL_QUESTIONS)

if __name__ == "__main__":
    main()
