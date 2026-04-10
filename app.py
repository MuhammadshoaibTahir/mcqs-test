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
    "001": "FAIZ RASOOL",
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

# ===== CL & NLP =====
{"question":"Computational Linguistics combines:","options":["Math & Physics","Linguistics & Computer Science","Biology & AI","History & CS"],"correct":"Linguistics & Computer Science"},
{"question":"NLP is used for:","options":["Hardware design","Language processing","Circuit design","Networking"],"correct":"Language processing"},
{"question":"Tokenization splits:","options":["Sentences","Characters","Text into units","Tags"],"correct":"Text into units"},
{"question":"POS tagging assigns:","options":["Meaning","Grammar category","Syntax tree","Entities"],"correct":"Grammar category"},
{"question":"NN tag represents:","options":["Verb","Noun","Adjective","Adverb"],"correct":"Noun"},
{"question":"VB tag represents:","options":["Verb","Noun","Adjective","Determiner"],"correct":"Verb"},
{"question":"NER identifies:","options":["Verbs","Names","Syntax","Stopwords"],"correct":"Names"},
{"question":"Parsing determines:","options":["Meaning","Structure","Tokens","Tags"],"correct":"Structure"},
{"question":"Bigram uses:","options":["No context","1 previous word","2 previous words","Full sentence"],"correct":"1 previous word"},
{"question":"Trigram uses:","options":["1 word","2 words","3 words","No context"],"correct":"2 words"},
{"question":"Language model assigns:","options":["Tags","Probabilities","Trees","Rules"],"correct":"Probabilities"},
{"question":"Perplexity measures:","options":["Speed","Accuracy","Prediction quality","Size"],"correct":"Prediction quality"},
{"question":"Sparse data problem occurs in:","options":["Regex","N-grams","Parsing","POS"],"correct":"N-grams"},
{"question":"Add-k smoothing solves:","options":["Parsing","Zero probability","Tokenization","Tagging"],"correct":"Zero probability"},
{"question":"Corpus means:","options":["Algorithm","Dataset of text","Model","Tree"],"correct":"Dataset of text"},
{"question":"Token is:","options":["Unique word","Occurrence","Sentence","Tag"],"correct":"Occurrence"},
{"question":"Type is:","options":["Unique word","Occurrence","Sentence","Tag"],"correct":"Unique word"},
{"question":"TTR stands for:","options":["Type Token Ratio","Text Tag Ratio","Token Tree Ratio","Type Tag Rule"],"correct":"Type Token Ratio"},
{"question":"Morphology studies:","options":["Syntax","Word structure","Meaning","Sound"],"correct":"Word structure"},
{"question":"Morpheme is:","options":["Sentence","Word","Smallest unit","Phrase"],"correct":"Smallest unit"},

# ===== MORPHOLOGY =====
{"question":"Prefix example:","options":["-ing","un-","-ed","cat"],"correct":"un-"},
{"question":"Suffix example:","options":["un-","-ness","pre-","anti-"],"correct":"-ness"},
{"question":"Inflectional morphology:","options":["Changes meaning","Changes grammar","Creates new word","Deletes word"],"correct":"Changes grammar"},
{"question":"Derivational morphology:","options":["Grammar change","Meaning change","No change","Token change"],"correct":"Meaning change"},
{"question":"Lemmatization returns:","options":["Random form","Base form","Suffix","Prefix"],"correct":"Base form"},

# ===== LANGUAGE MODELLING =====
{"question":"MLE stands for:","options":["Max Likelihood Estimation","Mean Level Error","Model Logic Engine","Machine Learning Engine"],"correct":"Max Likelihood Estimation"},
{"question":"Chain rule is used in:","options":["Parsing","Language models","Regex","Tagging"],"correct":"Language models"},
{"question":"Log probabilities avoid:","options":["Overflow","Underflow","Errors","Loops"],"correct":"Underflow"},
{"question":"Good-Turing is:","options":["Parser","Smoothing","Tagger","Tokenizer"],"correct":"Smoothing"},
{"question":"Kneser-Ney is:","options":["Grammar","Smoothing","Parsing","Tokenization"],"correct":"Smoothing"},

# ===== INFORMATION EXTRACTION =====
{"question":"IE extracts:","options":["Grammar","Structured info","Syntax","Tokens"],"correct":"Structured info"},
{"question":"Regex is used for:","options":["Parsing","Pattern matching","Translation","Tagging"],"correct":"Pattern matching"},
{"question":"Email extraction uses:","options":["CFG","Regex","HMM","CRF"],"correct":"Regex"},
{"question":"NER is part of:","options":["IE","Parsing","Tokenization","Slicing"],"correct":"IE"},

# ===== PYTHON BASICS =====
{"question":"List indexing starts at:","options":["1","0","-1","Depends"],"correct":"0"},
{"question":"Negative index -1 means:","options":["First","Last","Middle","Error"],"correct":"Last"},
{"question":"list[::-1] gives:","options":["Sorted","Reversed","Deleted","Copied"],"correct":"Reversed"},
{"question":"list[1:4] includes:","options":["1,2,3","1,2,3,4","2,3,4","Only 1"],"correct":"1,2,3"},
{"question":"list[::2] gives:","options":["All","Every 2nd element","Reverse","First only"],"correct":"Every 2nd element"},
{"question":"append() does:","options":["Remove","Add end","Sort","Replace"],"correct":"Add end"},
{"question":"pop() does:","options":["Add","Remove last","Sort","Copy"],"correct":"Remove last"},
{"question":"len([1,2,3]) =","options":["2","3","4","Error"],"correct":"3"},
{"question":"list[0] gives:","options":["Last","First","Middle","Error"],"correct":"First"},
{"question":"replace element uses:","options":["append","pop","list[i]=x","remove"],"correct":"list[i]=x"},

# ===== ADVANCED PYTHON =====
{"question":"Which is mutable?","options":["Tuple","String","List","Integer"],"correct":"List"},
{"question":"Which is immutable?","options":["List","Dict","Tuple","Set"],"correct":"Tuple"},
{"question":"set removes:","options":["Order","Duplicates","Values","Keys"],"correct":"Duplicates"},
{"question":"Dictionary stores:","options":["Values only","Keys only","Key-value pairs","Indexes"],"correct":"Key-value pairs"},
{"question":"for loop is used for:","options":["Condition","Iteration","Function","Class"],"correct":"Iteration"},
{"question":"if statement is used for:","options":["Loop","Condition","List","Function"],"correct":"Condition"}

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
