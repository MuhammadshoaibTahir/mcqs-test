import streamlit as st
import pandas as pd
import random
from datetime import datetime
import os
import time

# ================== CONFIGURATION ==================
EXAM_DURATION_MINUTES = 20

# Exam Structure:
# - 10 MCQs (Multiple Choice Questions)
# - 2 Comprehension Paragraphs (5 questions each = 10 questions)
# Total: 20 Questions

TOTAL_MCQS = 10
TOTAL_COMPREHENSION = 10  # 2 paragraphs × 5 questions each
TOTAL_QUESTIONS = TOTAL_MCQS + TOTAL_COMPREHENSION  # 20 total

ADMIN_SECRET_KEY = "shoaib123"
RESULTS_CSV = "results.csv"
RESULTS_XLSX = "results.xlsx"
TAB_SWITCH_WARNING_SECONDS = 5

# Note: Questions are shuffled ONCE per student session using random.sample()
# This ensures each student gets a unique question order, but the order
# remains consistent throughout their individual exam session

# ================== STUDENT DATABASE ==================
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

# ================== QUESTION BANK - 20 QUESTIONS TOTAL ==================

# ========== SECTION 1: 10 MOST IMPORTANT MCQs (From PDFs) ==========
MCQ_QUESTIONS = [
    # ================= CL & NLP =================
    {
        "question": "Computational Linguistics is a field that combines:",
        "options": ["Biology and Chemistry", "Linguistics and Computer Science", "Physics and Math", "History and AI"],
        "correct": "Linguistics and Computer Science",
        "type": "mcq"
    },
    {
        "question": "Natural Language Processing mainly focuses on:",
        "options": ["Hardware design", "Human language understanding and generation", "Networking", "Database storage"],
        "correct": "Human language understanding and generation",
        "type": "mcq"
    },
    {
        "question": "Tokenization means:",
        "options": ["Removing stopwords", "Splitting text into units", "Assigning tags", "Parsing sentences"],
        "correct": "Splitting text into units",
        "type": "mcq"
    },
    {
        "question": "Which NLP stage assigns grammatical categories?",
        "options": ["Tokenization", "POS Tagging", "Parsing", "NER"],
        "correct": "POS Tagging",
        "type": "mcq"
    },
    {
        "question": "Which tag represents a noun?",
        "options": ["VB", "JJ", "NN", "RB"],
        "correct": "NN",
        "type": "mcq"
    },
    {
        "question": "The Viterbi algorithm is used to:",
        "options": ["Tokenize text", "Find most probable tag sequence", "Remove noise", "Build vocabulary"],
        "correct": "Find most probable tag sequence",
        "type": "mcq"
    },
    {
        "question": "A language model assigns:",
        "options": ["Grammar rules", "Probabilities to sequences", "POS tags", "Syntax trees"],
        "correct": "Probabilities to sequences",
        "type": "mcq"
    },
    {
        "question": "Bigram model considers:",
        "options": ["No context", "One previous word", "Two previous words", "Whole sentence"],
        "correct": "One previous word",
        "type": "mcq"
    },
    {
        "question": "The main problem in n-gram models is:",
        "options": ["Parsing error", "Sparse data problem", "Tokenization issue", "Overfitting"],
        "correct": "Sparse data problem",
        "type": "mcq"
    },
    {
        "question": "Information Extraction is used to:",
        "options": ["Translate text", "Extract structured information", "Parse syntax", "Tokenize text"],
        "correct": "Extract structured information",
        "type": "mcq"
    },

    # ================= PYTHON BASICS =================
    {
        "question": "In Python, list indexing starts from:",
        "options": ["1", "-1", "0", "Depends on list"],
        "correct": "0",
        "type": "mcq"
    },
    {
        "question": "What does list[::-1] do?",
        "options": ["Sort list", "Reverse list", "Delete elements", "Copy list"],
        "correct": "Reverse list",
        "type": "mcq"
    },
    {
        "question": "Negative indexing in Python means:",
        "options": ["Error", "Counting from end", "Looping", "Skipping values"],
        "correct": "Counting from end",
        "type": "mcq"
    },
    {
        "question": "In slicing list[1:4], which indices are included?",
        "options": ["1,2,3", "1,2,3,4", "2,3,4", "Only 1"],
        "correct": "1,2,3",
        "type": "mcq"
    },
    {
        "question": "What does list[::2] return?",
        "options": ["All elements", "Every second element", "Reverse list", "First element only"],
        "correct": "Every second element",
        "type": "mcq"
    },
    {
        "question": "Which operation replaces an element in a list?",
        "options": ["append()", "remove()", "list[index] = value", "pop()"],
        "correct": "list[index] = value",
        "type": "mcq"
    },
    {
        "question": "What does append() do?",
        "options": ["Removes element", "Adds element at end", "Sorts list", "Replaces element"],
        "correct": "Adds element at end",
        "type": "mcq"
    },
    {
        "question": "What does pop() do?",
        "options": ["Adds element", "Removes last element", "Sorts list", "Duplicates list"],
        "correct": "Removes last element",
        "type": "mcq"
    },
    {
        "question": "What will len([1,2,3,4]) return?",
        "options": ["3", "4", "5", "Error"],
        "correct": "4",
        "type": "mcq"
    },
    {
        "question": "Which data type is used to store ordered elements?",
        "options": ["Set", "Dictionary", "List", "Tuple"],
        "correct": "List",
        "type": "mcq"
    }
]

# Combine all questions into one unified bank
QUESTION_BANK = MCQ_QUESTIONS.copy()

# Add comprehension questions
for passage in COMPREHENSION_PASSAGES:
    for question in passage["questions"]:
        question["passage_id"] = passage["passage_id"]
        question["passage_title"] = passage["title"]
        question["passage_text"] = passage["passage"]
    QUESTION_BANK.extend(passage["questions"])


# ================== HELPER FUNCTIONS ==================

def load_results():
    """Load existing results from CSV"""
    if os.path.exists(RESULTS_CSV):
        return pd.read_csv(RESULTS_CSV)
    return pd.DataFrame(columns=["Name", "Roll", "Score", "Timestamp"])

def save_results(name, roll, score):
    """Save exam results to CSV and Excel"""
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
    """Check if student has already taken the exam"""
    df = load_results()
    return roll in df["Roll"].values

def initialize_exam():
    """Initialize exam session with shuffled questions and options"""
    if "exam_initialized" not in st.session_state:
        # Shuffle questions ONCE
        shuffled_questions = random.sample(QUESTION_BANK, len(QUESTION_BANK))
        
        # Shuffle options for each question ONCE (only for MCQ and Comprehension)
        for q in shuffled_questions:
            question_type = q.get("type", "mcq")
            
            if question_type in ["mcq", "comprehension"]:
                # MCQ and Comprehension questions have options to shuffle
                options = q["options"].copy()
                random.shuffle(options)
                q["shuffled_options"] = options
            elif question_type == "true_false":
                # True/False questions don't need shuffling
                q["shuffled_options"] = ["True", "False"]
        
        st.session_state.shuffled_questions = shuffled_questions
        st.session_state.answers = {}  # Store answers: {question_index: selected_answer}
        st.session_state.current_question = 0
        st.session_state.exam_initialized = True
        st.session_state.start_time = time.time()
        st.session_state.exam_submitted = False
        st.session_state.tab_switch_detected = False

def calculate_score():
    """Calculate the final score"""
    score = 0
    for idx, question in enumerate(st.session_state.shuffled_questions):
        selected = st.session_state.answers.get(idx)
        if selected == question["correct"]:
            score += 1
    return score

def inject_anti_cheat_js():
    """Inject JavaScript for tab switch and window close detection"""
    js_code = f"""
    <script>
    // Tab Switch Detection
    let tabSwitchWarningTimer = null;
    let warningShown = false;
    
    document.addEventListener('visibilitychange', function() {{
        if (document.hidden) {{
            // User left the tab
            if (!warningShown) {{
                warningShown = true;
                alert('⚠️ WARNING: Return to the exam immediately!\\n\\nYou have {TAB_SWITCH_WARNING_SECONDS} seconds to return or your exam will be auto-submitted.');
                
                // Start countdown timer
                tabSwitchWarningTimer = setTimeout(function() {{
                    // Auto-submit exam after {TAB_SWITCH_WARNING_SECONDS} seconds
                    alert('Exam Auto-Submitted due to tab switch!');
                    
                    // Trigger Streamlit rerun with submit flag
                    const submitBtn = document.querySelector('[data-testid="baseButton-secondary"]');
                    if (submitBtn && submitBtn.innerText.includes('Submit')) {{
                        submitBtn.click();
                    }}
                    
                    // Force form submission
                    window.parent.postMessage({{type: 'streamlit:setComponentValue', value: 'AUTO_SUBMIT'}}, '*');
                }}, {TAB_SWITCH_WARNING_SECONDS * 1000});
            }}
        }} else {{
            // User returned to tab
            if (tabSwitchWarningTimer) {{
                clearTimeout(tabSwitchWarningTimer);
                tabSwitchWarningTimer = null;
                warningShown = false;
            }}
        }}
    }});
    
    // Window Close/Refresh Detection
    window.addEventListener('beforeunload', function(e) {{
        e.preventDefault();
        e.returnValue = '⚠️ WARNING: Do not leave the exam! Your progress may be lost.';
        return e.returnValue;
    }});
    </script>
    """
    st.components.v1.html(js_code, height=0)

# ================== ADMIN DASHBOARD ==================

def show_admin_dashboard():
    """Display admin dashboard with all results"""
    st.title("🔐 Admin Dashboard")
    st.markdown("---")
    
    df = load_results()
    
    if df.empty:
        st.info("No exam results yet.")
    else:
        st.success(f"Total Students Attempted: {len(df)}")
        st.dataframe(df, use_container_width=True)
        
        # Download Excel button
        with open(RESULTS_XLSX, "rb") as file:
            st.download_button(
                label="📥 Download Results (Excel)",
                data=file,
                file_name="exam_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

# ================== MAIN APPLICATION ==================

def main():
    st.set_page_config(page_title="MCQ Examination System", page_icon="📝", layout="centered")
    
    # Check for admin access
    query_params = st.query_params
    if "admin" in query_params and query_params["admin"] == ADMIN_SECRET_KEY:
        show_admin_dashboard()
        return
    
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.student_name = ""
        st.session_state.student_roll = ""
    
    # ================== LOGIN SCREEN ==================
    if not st.session_state.logged_in:
        st.title("📝 MCQ Examination System")
        st.markdown("### Student Login")
        st.markdown("---")
        
        roll_number = st.text_input("Enter Your Roll Number:").strip().upper()
        
        if st.button("Login", type="primary"):
            if roll_number not in STUDENTS:
                st.error("❌ Invalid Roll Number! Please check and try again.")
            elif has_student_attempted(roll_number):
                st.error("❌ You have already attempted this exam. Only ONE attempt is allowed.")
            else:
                st.session_state.logged_in = True
                st.session_state.student_name = STUDENTS[roll_number]
                st.session_state.student_roll = roll_number
                st.rerun()
        
        st.markdown("---")
        st.info("ℹ️ Enter your roll number to start the exam. You have only ONE attempt.")
        return
    
    # ================== EXAM SCREEN ==================
    
    # Initialize exam
    initialize_exam()
    
    # Inject anti-cheat JavaScript
    inject_anti_cheat_js()
    
    # Check if exam already submitted
    if st.session_state.exam_submitted:
        st.success("✅ Exam Submitted Successfully!")
        st.balloons()
        st.info(f"Thank you, **{st.session_state.student_name}**! Your answers have been recorded.")
        st.markdown("---")
        st.markdown("You may now close this window.")
        return
    
    # Timer calculation
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = (EXAM_DURATION_MINUTES * 60) - elapsed_time
    
    # Auto-submit if time expired
    if remaining_time <= 0:
        score = calculate_score()
        save_results(st.session_state.student_name, st.session_state.student_roll, score)
        st.session_state.exam_submitted = True
        st.rerun()
    
    # Display header
    st.title("📝 MCQ Examination")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"**Student:** {st.session_state.student_name}")
        st.markdown(f"**Roll Number:** {st.session_state.student_roll}")
    with col2:
        mins, secs = divmod(int(remaining_time), 60)
        timer_color = "red" if remaining_time < 60 else "green"
        st.markdown(f"**⏱️ Time Left:** <span style='color:{timer_color}; font-size:20px;'>{mins:02d}:{secs:02d}</span>", unsafe_allow_html=True)
    with col3:
        current_q = st.session_state.current_question + 1
        st.markdown(f"**Question:** {current_q}/{TOTAL_QUESTIONS}")
    
    st.markdown("---")
    
    # Get current question
    current_idx = st.session_state.current_question
    question = st.session_state.shuffled_questions[current_idx]
    
    # Check question type and display accordingly
    question_type = question.get("type", "mcq")
    
    # Display comprehension passage if applicable
    if question_type == "comprehension":
        st.markdown("### 📖 Comprehension Passage")
        st.info(f"**{question.get('passage_title', 'Reading Passage')}**")
        
        # Display passage text in a text area for better visibility
        st.text_area(
            "Read the passage carefully:",
            value=question['passage_text'],
            height=300,
            disabled=True,
            key=f"passage_{current_idx}"
        )
        st.markdown("---")
    
    # Display question
    st.markdown(f"### Q{current_idx + 1}. {question['question']}")
    st.markdown("")
    
    # Display options based on question type
    if question_type == "true_false":
        # True/False question
        selected_answer = st.radio(
            "Select your answer:",
            options=["True", "False"],
            index=None if current_idx not in st.session_state.answers else (0 if st.session_state.answers[current_idx] == "True" else 1),
            key=f"q_{current_idx}"
        )
    else:
        # MCQ or Comprehension question (both have multiple options)
        selected_answer = st.radio(
            "Select your answer:",
            options=question["shuffled_options"],
            index=None if current_idx not in st.session_state.answers else question["shuffled_options"].index(st.session_state.answers[current_idx]),
            key=f"q_{current_idx}"
        )
    
    # Store answer
    if selected_answer:
        st.session_state.answers[current_idx] = selected_answer
    
    st.markdown("---")
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if current_idx > 0:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()
    
    with col2:
        if current_idx < TOTAL_QUESTIONS - 1:
            if st.button("Next ➡️", use_container_width=True, type="primary"):
                st.session_state.current_question += 1
                st.rerun()
    
    with col3:
        if st.button("✅ Submit Exam", use_container_width=True, type="secondary"):
            # Calculate score
            score = calculate_score()
            
            # Save results
            save_results(st.session_state.student_name, st.session_state.student_roll, score)
            
            # Mark as submitted
            st.session_state.exam_submitted = True
            st.rerun()
    
    # Progress indicator
    answered = len(st.session_state.answers)
    progress = answered / TOTAL_QUESTIONS
    st.progress(progress)
    st.caption(f"Answered: {answered}/{TOTAL_QUESTIONS} questions")
    
    # Auto-refresh every second for timer
    st.markdown(
        f"""
        <script>
        setTimeout(function() {{
            window.parent.location.reload();
        }}, 1000);
        </script>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
