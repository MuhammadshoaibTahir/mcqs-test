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

}

# ================== QUESTION BANK - 20 QUESTIONS TOTAL ==================

# ========== SECTION 1: 10 MOST IMPORTANT MCQs (From PDFs) ==========
MCQ_QUESTIONS = [
    # Most Important Questions from Functional English PDFs
    {
        "question": "The key principle for making polite requests is:",
        "options": ["Use fewer words", "The more words you use, the more polite it generally sounds", "Always use commands", "Avoid modal verbs"],
        "correct": "The more words you use, the more polite it generally sounds",
        "type": "mcq"
    },
    {
        "question": "A request gives the listener:",
        "options": ["No choice", "The option to decline", "A command", "An order"],
        "correct": "The option to decline",
        "type": "mcq"
    },
    {
        "question": "Which is a proper noun?",
        "options": ["city", "London", "book", "teacher"],
        "correct": "London",
        "type": "mcq"
    },
    {
        "question": "Which article is correct: '___ hour ago'?",
        "options": ["a", "an", "the", "no article"],
        "correct": "an",
        "type": "mcq"
    },
    {
        "question": "Which preposition indicates exact time: 'The class starts ___ 9 AM'?",
        "options": ["in", "on", "at", "by"],
        "correct": "at",
        "type": "mcq"
    },
    {
        "question": "What is the past tense of 'go'?",
        "options": ["goed", "went", "gone", "goes"],
        "correct": "went",
        "type": "mcq"
    },
    {
        "question": "Which is CORRECT?",
        "options": ["He don't like coffee", "He doesn't like coffee", "He doesn't likes coffee", "He not like coffee"],
        "correct": "He doesn't like coffee",
        "type": "mcq"
    },
    {
        "question": "'Affect' is usually a ___, while 'effect' is usually a ___.",
        "options": ["noun, verb", "verb, noun", "adjective, adverb", "adverb, adjective"],
        "correct": "verb, noun",
        "type": "mcq"
    },
    {
        "question": "Which sentence uses SUBJUNCTIVE mood?",
        "options": ["I am happy", "I wish I were taller", "She studies daily", "Close the door"],
        "correct": "I wish I were taller",
        "type": "mcq"
    },
    {
        "question": "An independent clause is:",
        "options": ["Cannot stand alone", "Expresses a complete thought", "Needs another clause", "Has no verb"],
        "correct": "Expresses a complete thought",
        "type": "mcq"
    }
]

# ========== SECTION 2: 2 COMPREHENSION PASSAGES (10 Questions Total) ==========
COMPREHENSION_PASSAGES = [
    {
        "passage_id": 1,
        "title": "The Rise of Artificial Intelligence",
        "passage": """Artificial intelligence (AI) has transformed numerous industries over the past decade. From healthcare to finance, AI systems are now capable of performing tasks that once required human expertise. Machine learning algorithms can analyze vast datasets to identify patterns that would take humans years to discover. In healthcare, AI-powered diagnostic tools have shown accuracy rates comparable to experienced physicians in detecting certain conditions. The financial sector uses AI for fraud detection, algorithmic trading, and customer service chatbots. However, the rapid advancement of AI has also raised significant ethical concerns. Questions about data privacy, job displacement, and algorithmic bias dominate public discourse. Critics argue that without proper regulation, AI could exacerbate existing social inequalities. Proponents counter that AI, when developed responsibly, has the potential to solve some of humanity's most pressing challenges, including climate change and disease prevention. The debate continues as governments worldwide work to establish frameworks for the ethical development and deployment of AI technology.""",
        "questions": [
            {
                "question": "According to the passage, which TWO industries are mentioned as benefiting from AI?",
                "options": ["Healthcare and Finance", "Education and Tourism", "Agriculture and Mining", "Entertainment and Sports"],
                "correct": "Healthcare and Finance",
                "type": "comprehension"
            },
            {
                "question": "What concern do critics raise about AI?",
                "options": ["It is too expensive", "It may worsen social inequalities", "It cannot process data", "It only works in healthcare"],
                "correct": "It may worsen social inequalities",
                "type": "comprehension"
            },
            {
                "question": "The word 'exacerbate' in the passage is closest in meaning to:",
                "options": ["Reduce", "Solve", "Worsen", "Maintain"],
                "correct": "Worsen",
                "type": "comprehension"
            },
            {
                "question": "According to the passage, AI in healthcare:",
                "options": ["Replaces all doctors", "Shows accuracy comparable to experienced physicians", "Is not effective", "Only works for minor conditions"],
                "correct": "Shows accuracy comparable to experienced physicians",
                "type": "comprehension"
            },
            {
                "question": "Governments worldwide are:",
                "options": ["Banning AI completely", "Working to establish frameworks for ethical AI development", "Ignoring AI development", "Only using AI in military"],
                "correct": "Working to establish frameworks for ethical AI development",
                "type": "comprehension"
            }
        ]
    },
    {
        "passage_id": 2,
        "title": "The Impact of Social Media on Communication",
        "passage": """Social media platforms have fundamentally altered the way people communicate with each other. While traditional forms of communication such as letters and telephone calls required dedicated time and effort, social media enables instant messaging across the globe. This has brought undeniable benefits, including the ability to maintain relationships across distances and access information in real time. Nevertheless, research suggests that excessive social media use may negatively impact interpersonal skills. Studies have found that individuals who spend more than three hours daily on social media are more likely to report feelings of loneliness and social isolation. Furthermore, the prevalence of abbreviated language and emojis in online communication has raised concerns about declining writing proficiency among young people. Educators note that students increasingly struggle with formal writing conventions, often mixing casual digital language with academic prose. Despite these challenges, social media remains an integral part of modern life, and the key lies in finding a healthy balance between digital and face-to-face interactions.""",
        "questions": [
            {
                "question": "What is the main idea of the passage?",
                "options": ["Social media should be banned", "Social media has both benefits and drawbacks for communication", "Traditional communication is better", "Emojis improve writing skills"],
                "correct": "Social media has both benefits and drawbacks for communication",
                "type": "comprehension"
            },
            {
                "question": "According to research mentioned in the passage, people spending more than three hours daily on social media:",
                "options": ["Become better communicators", "Improve their writing", "Report feeling lonely", "Earn more money"],
                "correct": "Report feeling lonely",
                "type": "comprehension"
            },
            {
                "question": "What do educators observe about students?",
                "options": ["Students write better essays", "Students mix casual and academic language", "Students avoid social media", "Students prefer letters"],
                "correct": "Students mix casual and academic language",
                "type": "comprehension"
            },
            {
                "question": "Traditional forms of communication mentioned include:",
                "options": ["Only emails", "Letters and telephone calls", "Only text messages", "Only video calls"],
                "correct": "Letters and telephone calls",
                "type": "comprehension"
            },
            {
                "question": "The passage suggests the solution is:",
                "options": ["Stop using social media completely", "Use social media more", "Find a healthy balance between digital and face-to-face interactions", "Only use social media for work"],
                "correct": "Find a healthy balance between digital and face-to-face interactions",
                "type": "comprehension"
            }
        ]
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
        
        roll_number = st.text_input("Enter Your Roll Number:", max_chars=3).strip()
        
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
