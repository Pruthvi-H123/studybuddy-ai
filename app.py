import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
from utils.ai_helper import get_summary, get_mcqs, get_flashcards, get_important_topics

# ── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="StudyBuddy AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0a0f1a 0%, #0d1117 50%, #0a1628 100%);
    color: #e8e9ff;
}

/* Hide default header */
#MainMenu, footer, header { visibility: hidden; }

/* Hero Section */
.hero-wrap {
    background: linear-gradient(135deg, #1a1d3a 0%, #13152a 100%);
    border: 1px solid #252848;
    border-radius: 20px;
    padding: 3rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at center, #7c6bff15 0%, transparent 60%);
    pointer-events: none;
}
.hero-badge {
    display: inline-block;
    background: #7c6bff22;
    border: 1px solid #7c6bff44;
    color: #7c6bff;
    font-size: 0.75rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.1em;
    padding: 6px 16px;
    border-radius: 100px;
    margin-bottom: 1.5rem;
}
.hero-title {
    font-size: 3rem;
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, #ffffff 0%, #7c6bff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1.1rem;
    color: #7b7ea8;
    max-width: 600px;
    margin: 0 auto 2rem;
    line-height: 1.7;
}
.hero-stats {
    display: flex;
    justify-content: center;
    gap: 2rem;
    flex-wrap: wrap;
}
.stat-pill {
    background: #13152a;
    border: 1px solid #252848;
    border-radius: 12px;
    padding: 0.75rem 1.5rem;
    text-align: center;
}
.stat-num {
    font-size: 1.5rem;
    font-weight: 700;
    color: #7c6bff;
    font-family: 'JetBrains Mono', monospace;
    display: block;
}
.stat-label {
    font-size: 0.75rem;
    color: #7b7ea8;
    margin-top: 2px;
}

/* Feature Cards */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.feature-card {
    background: #13152a;
    border: 1px solid #252848;
    border-radius: 14px;
    padding: 1.25rem;
    text-align: center;
    transition: all 0.2s;
}
.feature-card:hover {
    border-color: #7c6bff;
    transform: translateY(-2px);
}
.feature-icon { font-size: 2rem; margin-bottom: 0.75rem; display: block; }
.feature-title { font-size: 0.95rem; font-weight: 600; color: #e8e9ff; margin-bottom: 6px; }
.feature-desc { font-size: 0.8rem; color: #7b7ea8; line-height: 1.5; }

/* Upload Area */
.upload-wrap {
    background: #13152a;
    border: 2px dashed #252848;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
}
.upload-wrap:hover { border-color: #7c6bff; }

/* Result Cards */
.result-card {
    background: #13152a;
    border: 1px solid #252848;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.result-card h4 {
    color: #7c6bff;
    font-size: 0.85rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}

/* MCQ Cards */
.mcq-card {
    background: #1a1d3a;
    border: 1px solid #252848;
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
}
.mcq-question { font-weight: 600; color: #e8e9ff; margin-bottom: 0.75rem; font-size: 0.95rem; }
.mcq-option { color: #7b7ea8; font-size: 0.88rem; padding: 4px 0; }
.mcq-answer { color: #00d97e; font-size: 0.82rem; margin-top: 0.5rem; font-weight: 600; }
.mcq-explanation { color: #7b7ea8; font-size: 0.8rem; margin-top: 4px; font-style: italic; }

/* Flashcards */
.flashcard {
    background: linear-gradient(135deg, #1a1d3a, #13152a);
    border: 1px solid #7c6bff44;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 0.75rem;
    display: flex;
    gap: 1rem;
    align-items: flex-start;
}
.fc-term {
    background: #7c6bff22;
    border: 1px solid #7c6bff44;
    color: #7c6bff;
    font-weight: 700;
    font-size: 0.85rem;
    padding: 0.4rem 0.85rem;
    border-radius: 8px;
    white-space: nowrap;
    font-family: 'JetBrains Mono', monospace;
    min-width: 120px;
    text-align: center;
}
.fc-def { color: #c8cae8; font-size: 0.9rem; line-height: 1.6; }

/* Topic Cards */
.topic-high {
    background: #1a1d3a;
    border: 1px solid #7c6bff44;
    border-left: 4px solid #7c6bff;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
}
.topic-medium {
    background: #1a1d3a;
    border: 1px solid #f59e0b44;
    border-left: 4px solid #f59e0b;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
}
.topic-name { font-weight: 700; color: #e8e9ff; font-size: 0.95rem; margin-bottom: 4px; }
.topic-badge-high {
    display: inline-block;
    background: #7c6bff22;
    color: #7c6bff;
    font-size: 0.68rem;
    font-family: 'JetBrains Mono', monospace;
    padding: 2px 8px;
    border-radius: 100px;
    margin-bottom: 6px;
    font-weight: 600;
}
.topic-badge-medium {
    display: inline-block;
    background: #f59e0b22;
    color: #f59e0b;
    font-size: 0.68rem;
    font-family: 'JetBrains Mono', monospace;
    padding: 2px 8px;
    border-radius: 100px;
    margin-bottom: 6px;
    font-weight: 600;
}
.topic-desc { color: #7b7ea8; font-size: 0.85rem; line-height: 1.5; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0d0f1a !important;
    border-right: 1px solid #252848;
}
[data-testid="stSidebar"] * { color: #e8e9ff !important; }

/* Buttons */
.stButton > button {
    background: #7c6bff !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.5rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stButton > button:hover { opacity: 0.9 !important; transform: translateY(-1px) !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #13152a;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #252848;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #7b7ea8 !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
    background: #7c6bff !important;
    color: white !important;
}

/* Progress */
.stProgress > div > div { background: #7c6bff !important; }

/* Spinner */
.stSpinner > div { border-top-color: #7c6bff !important; }

/* Summary points */
.summary-point {
    background: #1a1d3a;
    border: 1px solid #252848;
    border-left: 3px solid #7c6bff;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
    color: #c8cae8;
    font-size: 0.9rem;
    line-height: 1.6;
}

/* Score box */
.score-box {
    background: linear-gradient(135deg, #7c6bff22, #13152a);
    border: 1px solid #7c6bff44;
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    margin-bottom: 1rem;
}
.score-num {
    font-size: 3rem;
    font-weight: 700;
    color: #7c6bff;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1;
}
</style>
""", unsafe_allow_html=True)


# ── Session State ─────────────────────────────────────────────
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = None
if 'filename' not in st.session_state:
    st.session_state.filename = None
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'mcqs' not in st.session_state:
    st.session_state.mcqs = None
if 'flashcards' not in st.session_state:
    st.session_state.flashcards = None
if 'topics' not in st.session_state:
    st.session_state.topics = None
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:1rem 0 1.5rem;'>
        <div style='font-size:2.5rem;margin-bottom:0.5rem;'>🎓</div>
        <div style='font-size:1.2rem;font-weight:700;'>StudyBuddy AI</div>
        <div style='font-size:0.75rem;color:#7b7ea8;margin-top:4px;font-family:JetBrains Mono,monospace;'>v1.0 · Powered by Groq</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**📚 How to use:**")
    st.markdown("1. Upload your PDF notes")
    st.markdown("2. Click Generate Study Material")
    st.markdown("3. Read the Summary")
    st.markdown("4. Practice MCQ Quiz")
    st.markdown("5. Review Flashcards")
    st.markdown("6. Check Important Topics")

    st.markdown("---")
    st.markdown("**⚡ Supported:**")
    st.markdown("📄 PDF textbooks")
    st.markdown("📝 Lecture notes")
    st.markdown("📖 Study guides")
    st.markdown("📑 Research papers")

    st.markdown("---")
    if st.session_state.filename:
        st.markdown(f"**✅ Loaded:** <span style='color:#60a5fa'>{st.session_state.filename}</span>", unsafe_allow_html=True)

        st.markdown(f"**📊 Text:** <span style='color:#60a5fa'>{len(st.session_state.extracted_text)} chars</span>", unsafe_allow_html=True)
        if st.button("🗑️ Clear & Upload New"):
            for key in ['extracted_text','filename','summary','mcqs','flashcards','topics','quiz_answers','quiz_score']:
                st.session_state[key] = None
            st.session_state.quiz_score = 0
            st.session_state.quiz_answers = {}
            st.rerun()

# ── HERO SECTION ──────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">⚡ AI-POWERED · FREE · INSTANT</div>
    <div class="hero-title">Study Smarter,<br>Not Harder</div>
    <div class="hero-sub">
        Upload any PDF — lecture notes, textbooks, or study guides.
        Get AI-generated summaries, MCQs, flashcards, and exam topics in seconds.
    </div>
    <div class="hero-stats">
        <div class="stat-pill">
            <span class="stat-num">10x</span>
            <span class="stat-label">Faster Revision</span>
        </div>
        <div class="stat-pill">
            <span class="stat-num">4</span>
            <span class="stat-label">Study Tools</span>
        </div>
        <div class="stat-pill">
            <span class="stat-num">∞</span>
            <span class="stat-label">PDFs Supported</span>
        </div>
        <div class="stat-pill">
            <span class="stat-num">Free</span>
            <span class="stat-label">Always</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── FEATURE CARDS ─────────────────────────────────────────────
st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <span class="feature-icon">📝</span>
        <div class="feature-title">Smart Summary</div>
        <div class="feature-desc">Key points extracted and simplified for quick revision</div>
    </div>
    <div class="feature-card">
        <span class="feature-icon">❓</span>
        <div class="feature-title">MCQ Quiz</div>
        <div class="feature-desc">10 auto-generated questions with answers to test yourself</div>
    </div>
    <div class="feature-card">
        <span class="feature-icon">🃏</span>
        <div class="feature-title">Flashcards</div>
        <div class="feature-desc">Term-definition pairs for memory-based learning</div>
    </div>
    <div class="feature-card">
        <span class="feature-icon">🎯</span>
        <div class="feature-title">Exam Topics</div>
        <div class="feature-desc">HIGH and MEDIUM priority topics to focus on for exams</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── UPLOAD SECTION ────────────────────────────────────────────
if not st.session_state.extracted_text:
    st.markdown("### 📤 Upload Your Study Material")
    st.markdown("#### 📄 Select PDF File")
    uploaded_file = st.file_uploader(
    "",
    type=["pdf"],
    label_visibility="collapsed"
)

    if uploaded_file:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Generate Study Material", use_container_width=True):
                with st.spinner("📖 Reading your PDF..."):
                    text, error = extract_text_from_pdf(uploaded_file)

                if error:
                    st.error(f"Could not read PDF: {error}")
                elif not text or len(text) < 100:
                    st.error("PDF appears to be empty or scanned. Please upload a text-based PDF.")
                else:
                    st.session_state.extracted_text = text
                    st.session_state.filename = uploaded_file.name
                    st.success(f"✅ Successfully read **{uploaded_file.name}** — {len(text)} characters extracted!")
                    st.rerun()

    st.markdown("""
    <div style='text-align:center;padding:2rem;color:#3a3d6b;font-size:0.85rem;margin-top:1rem;'>
        <div style='font-size:2rem;margin-bottom:0.5rem;'>📄</div>
        Upload a PDF above to get started
    </div>
    """, unsafe_allow_html=True)

# ── RESULTS SECTION ───────────────────────────────────────────
else:
    st.markdown(f"""
    <div style='background:#13152a;border:1px solid #252848;border-radius:12px;padding:1rem 1.5rem;margin-bottom:1.5rem;display:flex;align-items:center;gap:12px;'>
        <span style='font-size:1.5rem;'>📄</span>
        <div>
            <div style='font-weight:600;color:#e8e9ff;'>{st.session_state.filename}</div>
            <div style='font-size:0.78rem;color:#7b7ea8;font-family:JetBrains Mono,monospace;'>{len(st.session_state.extracted_text):,} characters extracted · Ready to study</div>
        </div>
        <span style='margin-left:auto;background:#00d97e22;color:#00d97e;font-size:0.75rem;padding:4px 12px;border-radius:100px;border:1px solid #00d97e44;font-weight:600;'>✓ LOADED</span>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📝 Summary", "❓ MCQ Quiz", "🃏 Flashcards", "🎯 Exam Topics"])

    # ── TAB 1: SUMMARY ──────────────────────────────────────
    with tab1:
        st.markdown("### 📝 Smart Summary")
        st.markdown("<p style='color:#7b7ea8;font-size:0.9rem;'>Key points from your study material — simplified for quick revision</p>", unsafe_allow_html=True)

        if not st.session_state.summary:
            if st.button("✨ Generate Summary", use_container_width=True):
                with st.spinner("🤖 AI is reading and summarizing..."):
                    try:
                        st.session_state.summary = get_summary(st.session_state.extracted_text)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        else:
            lines = st.session_state.summary.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and len(line) > 5:
                    clean = line.lstrip('0123456789.-) ').strip()
                    if clean:
                        st.markdown(f'<div class="summary-point">📌 {clean}</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Regenerate Summary"):
                st.session_state.summary = None
                st.rerun()

    # ── TAB 2: MCQ QUIZ ─────────────────────────────────────
    with tab2:
        st.markdown("### ❓ MCQ Quiz")
        st.markdown("<p style='color:#7b7ea8;font-size:0.9rem;'>Test your knowledge with AI-generated questions</p>", unsafe_allow_html=True)

        if not st.session_state.mcqs:
            if st.button("✨ Generate MCQ Quiz", use_container_width=True):
                with st.spinner("🤖 Creating quiz questions..."):
                    try:
                        st.session_state.mcqs = get_mcqs(st.session_state.extracted_text)
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_score = 0
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        else:
            questions = st.session_state.mcqs.get('questions', [])
            submitted = len(st.session_state.quiz_answers) == len(questions) and len(questions) > 0

            if submitted:
                score = st.session_state.quiz_score
                total = len(questions)
                pct = int((score / total) * 100) if total > 0 else 0
                color = '#00d97e' if pct >= 70 else '#f59e0b' if pct >= 40 else '#ef4444'
                st.markdown(f"""
                <div class="score-box">
                    <div class="score-num" style="color:{color};">{score}/{total}</div>
                    <div style="font-size:1.1rem;color:#e8e9ff;margin-top:8px;font-weight:600;">Score: {pct}%</div>
                    <div style="font-size:0.85rem;color:#7b7ea8;margin-top:4px;">
                        {'🎉 Excellent! Keep it up!' if pct >= 70 else '📚 Good effort! Review the material.' if pct >= 40 else '💪 Keep studying! You can do it!'}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            for i, q in enumerate(questions):
                correct = q.get('answer', '')
                user_ans = st.session_state.quiz_answers.get(i)
                is_correct = user_ans == correct if user_ans else None

                border = '#00d97e' if is_correct == True else '#ef4444' if is_correct == False else '#252848'
                st.markdown(f"""
                <div class="mcq-card" style="border-color:{border};">
                    <div class="mcq-question">Q{i+1}. {q.get('question','')}</div>
                """, unsafe_allow_html=True)

                for opt in q.get('options', []):
                    opt_color = '#00d97e' if (submitted and opt == correct) else '#ef4444' if (submitted and opt == user_ans and opt != correct) else '#7b7ea8'
                    st.markdown(f'<div class="mcq-option" style="color:{opt_color};">{"✓ " if submitted and opt==correct else "✗ " if submitted and opt==user_ans and opt!=correct else "• "}{opt}</div>', unsafe_allow_html=True)

                if submitted:
                    st.markdown(f'<div class="mcq-answer">✅ Answer: {correct}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="mcq-explanation">💡 {q.get("explanation","")}</div>', unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

                if not submitted:
                    answer = st.radio(
                        f"Your answer for Q{i+1}:",
                        q.get('options', []),
                        key=f"q_{i}",
                        label_visibility="collapsed"
                    )
                    st.session_state.quiz_answers[i] = answer

            if not submitted and questions:
                if st.button("✅ Submit Quiz", use_container_width=True):
                    score = 0
                    for i, q in enumerate(questions):
                        if st.session_state.quiz_answers.get(i) == q.get('answer'):
                            score += 1
                    st.session_state.quiz_score = score
                    st.rerun()

            if submitted:
                if st.button("🔄 Retake Quiz"):
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_score = 0
                    st.rerun()

    # ── TAB 3: FLASHCARDS ───────────────────────────────────
    with tab3:
        st.markdown("### 🃏 Flashcards")
        st.markdown("<p style='color:#7b7ea8;font-size:0.9rem;'>Term-definition pairs for memory-based learning</p>", unsafe_allow_html=True)

        if not st.session_state.flashcards:
            if st.button("✨ Generate Flashcards", use_container_width=True):
                with st.spinner("🤖 Creating flashcards..."):
                    try:
                        st.session_state.flashcards = get_flashcards(st.session_state.extracted_text)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        else:
            cards = st.session_state.flashcards.get('flashcards', [])
            st.markdown(f"<p style='color:#7b7ea8;font-size:0.85rem;margin-bottom:1rem;'>{len(cards)} flashcards generated</p>", unsafe_allow_html=True)

            for i, card in enumerate(cards):
                st.markdown(f"""
                <div class="flashcard">
                    <div class="fc-term">#{i+1} {card.get('term','')}</div>
                    <div class="fc-def">{card.get('definition','')}</div>
                </div>
                """, unsafe_allow_html=True)

            if st.button("🔄 Regenerate Flashcards"):
                st.session_state.flashcards = None
                st.rerun()

    # ── TAB 4: EXAM TOPICS ──────────────────────────────────
    with tab4:
        st.markdown("### 🎯 Important Exam Topics")
        st.markdown("<p style='color:#7b7ea8;font-size:0.9rem;'>Focus on these topics for your exam</p>", unsafe_allow_html=True)

        if not st.session_state.topics:
            if st.button("✨ Find Important Topics", use_container_width=True):
                with st.spinner("🤖 Analyzing exam-important topics..."):
                    try:
                        st.session_state.topics = get_important_topics(st.session_state.extracted_text)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        else:
            topics = st.session_state.topics.get('topics', [])
            high = [t for t in topics if t.get('importance','').upper() == 'HIGH']
            medium = [t for t in topics if t.get('importance','').upper() == 'MEDIUM']

            if high:
                st.markdown("<div style='font-size:0.8rem;color:#7c6bff;font-weight:600;margin-bottom:0.75rem;font-family:JetBrains Mono,monospace;letter-spacing:0.08em;'>🔴 HIGH PRIORITY</div>", unsafe_allow_html=True)
                for t in high:
                    st.markdown(f"""
                    <div class="topic-high">
                        <span class="topic-badge-high">HIGH PRIORITY</span>
                        <div class="topic-name">📌 {t.get('topic','')}</div>
                        <div class="topic-desc">{t.get('description','')}</div>
                    </div>
                    """, unsafe_allow_html=True)

            if medium:
                st.markdown("<div style='font-size:0.8rem;color:#f59e0b;font-weight:600;margin:1rem 0 0.75rem;font-family:JetBrains Mono,monospace;letter-spacing:0.08em;'>🟡 MEDIUM PRIORITY</div>", unsafe_allow_html=True)
                for t in medium:
                    st.markdown(f"""
                    <div class="topic-medium">
                        <span class="topic-badge-medium">MEDIUM PRIORITY</span>
                        <div class="topic-name">📎 {t.get('topic','')}</div>
                        <div class="topic-desc">{t.get('description','')}</div>
                    </div>
                    """, unsafe_allow_html=True)

            if st.button("🔄 Regenerate Topics"):
                st.session_state.topics = None
                st.rerun()