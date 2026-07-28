"""
AI Video Assistant — Next-Gen Streamlit UI (Top 1% Design Edition)
A state-of-the-art, glassmorphism-powered frontend with smooth animations,
interactive video workspace, searchable transcripts, action item manager,
and context-aware RAG AI assistant.

Run with:  streamlit run app.py
"""

import time
import streamlit as st
from dotenv import load_dotenv

# ---- Core Pipeline Imports ----
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question

load_dotenv()

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="VideoAgent — AI Video Intelligence Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# TOP-TIER DESIGN SYSTEM & CSS ANIMATIONS
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-main: #06080d;
    --bg-card: rgba(15, 19, 32, 0.7);
    --bg-card-hover: rgba(22, 28, 45, 0.85);
    --bg-input: rgba(20, 26, 42, 0.6);
    --border-glass: rgba(255, 255, 255, 0.08);
    --border-glow: rgba(139, 92, 246, 0.4);
    
    --accent-purple: #8b5cf6;
    --accent-cyan: #06b6d4;
    --accent-pink: #ec4899;
    --accent-emerald: #10b981;
    --accent-amber: #f59e0b;
    
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
}

/* Global Reset & Base Typography */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif !important;
}

.stApp {
    background: 
        radial-gradient(circle at 15% 10%, rgba(139, 92, 246, 0.15) 0%, transparent 45%),
        radial-gradient(circle at 85% 20%, rgba(6, 182, 212, 0.12) 0%, transparent 40%),
        radial-gradient(circle at 50% 80%, rgba(236, 72, 153, 0.08) 0%, transparent 50%),
        var(--bg-main) !important;
    color: var(--text-primary);
}

/* Hide Default Elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 1.8rem;
    padding-bottom: 4rem;
    max-width: 1280px;
}

/* ==========================================
   ANIMATIONS
   ========================================== */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes floatSlow {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-7px); }
}

@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 15px rgba(139, 92, 246, 0.3); }
    50% { box-shadow: 0 0 30px rgba(139, 92, 246, 0.6); }
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes spinRing {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.animate-fade-in { animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
.animate-float { animation: floatSlow 4s ease-in-out infinite; }

/* ==========================================
   HEADER & HERO SECTION
   ========================================== */
.brand-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.6rem 1.2rem;
    background: var(--bg-card);
    backdrop-filter: blur(16px);
    border: 1px solid var(--border-glass);
    border-radius: 20px;
    margin-bottom: 2rem;
}

.brand-logo {
    display: flex;
    align-items: center;
    gap: 12px;
    font-family: 'Outfit', sans-serif;
    font-size: 1.25rem;
    font-weight: 800;
    color: var(--text-primary);
}

.brand-badge {
    background: linear-gradient(135deg, rgba(139,92,246,0.2), rgba(6,182,212,0.2));
    border: 1px solid var(--border-glow);
    color: #a78bfa;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.hero-container {
    text-align: center;
    padding: 1rem 0 2rem 0;
}

.hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(139, 92, 246, 0.1);
    border: 1px solid rgba(139, 92, 246, 0.3);
    color: #c4b5fd;
    padding: 6px 18px;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 600;
    margin-bottom: 1rem;
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.15);
}

.hero-title {
    font-size: 3.2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin: 0.5rem 0;
    background: linear-gradient(135deg, #ffffff 20%, #a78bfa 50%, #38bdf8 80%, #ffffff);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: gradientShift 8s ease infinite;
}

.hero-subtitle {
    color: var(--text-secondary);
    font-size: 1.1rem;
    max-width: 680px;
    margin: 0 auto 1.5rem auto;
    line-height: 1.6;
}

/* ==========================================
   GLASS CARDS & METRIC TILES
   ========================================== */
.glass-card {
    background: var(--bg-card);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--border-glass);
    border-radius: 20px;
    padding: 1.5rem;
    transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    position: relative;
    overflow: hidden;
}

.glass-card:hover {
    border-color: var(--border-glow);
    transform: translateY(-4px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 0 0 20px rgba(139, 92, 246, 0.15);
}

.card-header-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: 'Outfit', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 1rem;
}

.card-header-icon {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, rgba(139,92,246,0.2), rgba(6,182,212,0.1));
    border: 1px solid rgba(139,92,246,0.3);
    font-size: 1.1rem;
}

.summary-content {
    color: var(--text-secondary);
    font-size: 0.96rem;
    line-height: 1.7;
    white-space: pre-wrap;
}

/* ==========================================
   ACTION ITEMS & PILLS
   ========================================== */
.action-item-box {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 16px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--border-glass);
    border-radius: 14px;
    margin-bottom: 10px;
    transition: all 0.25s ease;
}

.action-item-box:hover {
    background: rgba(139, 92, 246, 0.06);
    border-color: rgba(139, 92, 246, 0.3);
}

.action-checkbox {
    width: 18px;
    height: 18px;
    border-radius: 6px;
    border: 2px solid var(--accent-purple);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 2px;
    flex-shrink: 0;
}

.tag-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 0.83rem;
    font-weight: 600;
    margin: 4px;
    border: 1px solid var(--border-glass);
    background: rgba(255, 255, 255, 0.04);
    color: var(--text-primary);
    transition: all 0.2s ease;
}

.tag-pill:hover {
    transform: translateY(-2px);
    border-color: var(--border-glow);
}

.tag-pill.cyan {
    background: rgba(6, 182, 212, 0.1);
    border-color: rgba(6, 182, 212, 0.3);
    color: #67e8f9;
}

.tag-pill.pink {
    background: rgba(236, 72, 153, 0.1);
    border-color: rgba(236, 72, 153, 0.3);
    color: #f472b6;
}

.tag-pill.emerald {
    background: rgba(16, 185, 129, 0.1);
    border-color: rgba(16, 185, 129, 0.3);
    color: #6ee7b7;
}

/* ==========================================
   SIDEBAR & INPUTS
   ========================================== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #090c15 0%, #05070a 100%) !important;
    border-right: 1px solid var(--border-glass) !important;
}

.stTextInput input {
    background: var(--bg-input) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: 14px !important;
    color: var(--text-primary) !important;
    padding: 12px 16px !important;
    transition: all 0.3s ease !important;
}

.stTextInput input:focus {
    border-color: var(--accent-purple) !important;
    box-shadow: 0 0 15px rgba(139, 92, 246, 0.3) !important;
}

.stButton button {
    background: linear-gradient(135deg, var(--accent-purple), #6366f1) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.75rem 1.6rem !important;
    box-shadow: 0 10px 25px rgba(139, 92, 246, 0.3) !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    width: 100%;
}

.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 15px 35px rgba(139, 92, 246, 0.5) !important;
}

.stButton button:active {
    transform: translateY(0px) !important;
}

/* ==========================================
   STEP TRACKER & LOADER
   ========================================== */
.step-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    margin: 2rem 0;
    padding: 0 1rem;
}

.step-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    z-index: 2;
    flex: 1;
}

.step-node {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    background: var(--bg-card);
    border: 2px solid var(--border-glass);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    font-size: 0.9rem;
    color: var(--text-muted);
    transition: all 0.4s ease;
}

.step-item.active .step-node {
    background: linear-gradient(135deg, var(--accent-purple), #6366f1);
    border-color: #a78bfa;
    color: #ffffff;
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.6);
    animation: pulseGlow 1.5s infinite;
}

.step-item.done .step-node {
    background: rgba(16, 185, 129, 0.2);
    border-color: var(--accent-emerald);
    color: var(--accent-emerald);
}

.step-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--text-muted);
}

.step-item.active .step-label, .step-item.done .step-label {
    color: var(--text-primary);
}

.orbit-loader {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2.5rem 0;
    gap: 16px;
}

.ring-outer {
    position: relative;
    width: 72px;
    height: 72px;
}

.ring-inner {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    border: 3px solid transparent;
    border-top-color: var(--accent-purple);
    border-right-color: var(--accent-cyan);
    animation: spinRing 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
}

.loader-status-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9rem;
    color: var(--text-secondary);
    letter-spacing: 0.02em;
}

/* ==========================================
   CHAT BUBBLES
   ========================================== */
.chat-user-bubble {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(99, 102, 241, 0.1));
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-radius: 18px 18px 4px 18px;
    padding: 12px 18px;
    color: var(--text-primary);
    max-width: 82%;
    margin-left: auto;
    margin-bottom: 12px;
    font-size: 0.95rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.chat-assistant-bubble {
    background: var(--bg-card);
    border: 1px solid var(--border-glass);
    border-radius: 18px 18px 18px 4px;
    padding: 14px 18px;
    color: var(--text-secondary);
    max-width: 85%;
    margin-bottom: 12px;
    font-size: 0.95rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

/* Glow Line Divider */
.glow-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.4), transparent);
    margin: 2rem 0;
    border: none;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE INITIALIZATION
# =========================================================
defaults = {
    "result": None,
    "processing": False,
    "chat_history": [],
    "language": "english",
    "active_tab": 0,
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


# =========================================================
# UI RENDER HELPER FUNCTIONS
# =========================================================
def render_brand_header():
    st.markdown("""
    <div class="brand-header animate-fade-in">
        <div class="brand-logo">
            <span>⚡ VideoAgent</span>
            <span class="brand-badge">PRO EDITION</span>
        </div>
        <div style="display:flex; gap:12px; align-items:center;">
            <span style="font-size:0.82rem; color:var(--text-muted);">Status: <strong style="color:var(--accent-emerald);">● RAG Engine Online</strong></span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_hero():
    st.markdown("""
    <div class="hero-container animate-fade-in">
        <div class="hero-pill animate-float">
            <span>✨ Powered by Whisper & RAG Intelligence</span>
        </div>
        <h1 class="hero-title">Turn Videos into Actionable Intelligence</h1>
        <p class="hero-subtitle">
            Extract transcriptions, executive summaries, key decisions, action items, 
            and chat interactively with any YouTube video or audio recording in seconds.
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_step_progress(current_step_idx: int, steps_list):
    html = '<div class="step-container">'
    for idx, label in enumerate(steps_list):
        if idx < current_step_idx:
            status_cls = "done"
            icon = "✓"
        elif idx == current_step_idx:
            status_cls = "active"
            icon = str(idx + 1)
        else:
            status_cls = ""
            icon = str(idx + 1)

        html += f"""
        <div class="step-item {status_cls}">
            <div class="step-node">{icon}</div>
            <div class="step-label">{label}</div>
        </div>
        """
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def execute_pipeline(source: str, language: str):
    """Executes the video processing pipeline with real-time animated step updates."""
    steps = ["Ingest", "Transcribe", "Title", "Summarize", "Extract", "RAG Index"]
    tracker_ph = st.empty()
    loader_ph = st.empty()

    def update_stage(step_index: int, message: str):
        with tracker_ph.container():
            render_step_progress(step_index, steps)
        loader_ph.markdown(f"""
        <div class="orbit-loader animate-fade-in">
            <div class="ring-outer"><div class="ring-inner"></div></div>
            <div class="loader-status-text">⚡ {message}</div>
        </div>
        """, unsafe_allow_html=True)

    update_stage(0, "Fetching video source & extracting audio stream…")
    chunks = process_input(source)

    update_stage(1, "Transcribing audio with OpenAI Whisper…")
    transcript = transcribe_all(chunks, language)

    update_stage(2, "Synthesizing executive title…")
    title = generate_title(transcript)

    update_stage(3, "Generating comprehensive summary…")
    summary = summarize(transcript)

    update_stage(4, "Extracting action items, key decisions & questions…")
    action_items = extract_action_items(transcript)
    decisions = extract_key_decisions(transcript)
    questions = extract_questions(transcript)

    update_stage(5, "Building Chroma vector embeddings for RAG chat…")
    rag_chain = build_rag_chain(transcript)

    tracker_ph.empty()
    loader_ph.empty()

    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_items,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain": rag_chain,
    }


# =========================================================
# SIDEBAR CONTROLS
# =========================================================
with st.sidebar:
    st.markdown("### 🎬 Video Ingestion")
    st.caption("Enter a YouTube URL or upload a local audio file.")

    st.markdown("<hr class='glow-divider'>", unsafe_allow_html=True)

    source_input = st.text_input(
        "Source URL / File Path",
        placeholder="https://www.youtube.com/watch?v=...",
        help="Paste YouTube link or path to .mp4 / .mp3 file",
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Transcription Language**")
    language_choice = st.radio(
        "Language",
        options=["english", "hinglish"],
        horizontal=True,
        label_visibility="collapsed",
    )

    st.markdown("<hr class='glow-divider'>", unsafe_allow_html=True)
    run_btn = st.button("🚀 Process Video", use_container_width=True)

    if st.session_state.result:
        st.markdown("<hr class='glow-divider'>", unsafe_allow_html=True)
        if st.button("🗑️ Reset Workspace", use_container_width=True):
            st.session_state.result = None
            st.session_state.chat_history = []
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.caption("⚡ Powered by Whisper · LangChain · ChromaDB")


# =========================================================
# MAIN APP BODY
# =========================================================
render_brand_header()

if not st.session_state.result and not run_btn:
    render_hero()

# Handle Pipeline Execution
if run_btn:
    if not source_input.strip():
        st.warning("⚠️ Please provide a valid YouTube URL or local file path in the sidebar.")
    else:
        st.session_state.processing = True
        st.session_state.language = language_choice
        try:
            with st.spinner(""):
                result_data = execute_pipeline(source_input.strip(), language_choice)
            st.session_state.result = result_data
            st.session_state.chat_history = []
            st.toast("Pipeline complete! Insights ready. 🎉", icon="✅")
        except Exception as err:
            st.error(f"❌ Error executing pipeline: `{err}`")
        finally:
            st.session_state.processing = False


# =========================================================
# RESULTS WORKSPACE DASHBOARD
# =========================================================
if st.session_state.result:
    res = st.session_state.result

    # Executive Title Banner
    st.markdown(f"""
    <div class="glass-card animate-fade-in" style="margin-bottom: 1.8rem; background: linear-gradient(135deg, rgba(139,92,246,0.15), rgba(6,182,212,0.08)); border-color: var(--border-glow);">
        <div style="display:flex; align-items:center; gap:14px;">
            <div style="font-size: 2rem;">🎬</div>
            <div>
                <span style="font-size:0.75rem; font-weight:700; color:var(--accent-purple); text-transform:uppercase; letter-spacing:0.05em;">Generated Title</span>
                <h2 style="margin:2px 0 0 0; font-size:1.6rem; color:var(--text-primary);">{res['title']}</h2>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Workspace Tabs
    tab_overview, tab_transcript, tab_chat = st.tabs([
        "📋 Executive Overview",
        "📝 Full Transcript",
        "💬 Interactive RAG Chat"
    ])

    # ---------------- TAB 1: EXECUTIVE OVERVIEW ----------------
    with tab_overview:
        col_left, col_right = st.columns([1, 1], gap="large")

        with col_left:
            # Summary Glass Card
            st.markdown(f"""
            <div class="glass-card animate-fade-in">
                <div class="card-header-title">
                    <div class="card-header-icon">📑</div>
                    Executive Summary
                </div>
                <div class="summary-content">{res['summary']}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Key Decisions Box
            decisions_list = res["key_decisions"]
            if isinstance(decisions_list, str):
                decisions_list = [d.strip() for d in decisions_list.split("\n") if d.strip()]
            
            pills_html = "".join([f'<span class="tag-pill cyan">🔑 {d}</span>' for d in decisions_list]) or '<span style="color:var(--text-muted);">None extracted</span>'
            st.markdown(f"""
            <div class="glass-card animate-fade-in">
                <div class="card-header-title">
                    <div class="card-header-icon">🔑</div>
                    Key Decisions
                </div>
                <div>{pills_html}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            # Action Items Box
            actions_list = res["action_items"]
            if isinstance(actions_list, str):
                actions_list = [a.strip("- *") for a in actions_list.split("\n") if a.strip()]

            items_html = ""
            for item in actions_list:
                items_html += f"""
                <div class="action-item-box">
                    <div class="action-checkbox">✓</div>
                    <div style="font-size:0.93rem; color:var(--text-primary);">{item}</div>
                </div>
                """
            if not items_html:
                items_html = '<div style="color:var(--text-muted);">No action items detected.</div>'

            st.markdown(f"""
            <div class="glass-card animate-fade-in">
                <div class="card-header-title">
                    <div class="card-header-icon">✅</div>
                    Action Items
                </div>
                <div>{items_html}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Open Questions Box
            questions_list = res["open_questions"]
            if isinstance(questions_list, str):
                questions_list = [q.strip() for q in questions_list.split("\n") if q.strip()]

            q_pills_html = "".join([f'<span class="tag-pill pink">❓ {q}</span>' for q in questions_list]) or '<span style="color:var(--text-muted);">None detected</span>'
            st.markdown(f"""
            <div class="glass-card animate-fade-in">
                <div class="card-header-title">
                    <div class="card-header-icon">❓</div>
                    Open Questions
                </div>
                <div>{q_pills_html}</div>
            </div>
            """, unsafe_allow_html=True)

    # ---------------- TAB 2: TRANSCRIPT ----------------
    with tab_transcript:
        st.markdown("""
        <div class="glass-card animate-fade-in">
            <div class="card-header-title">
                <div class="card-header-icon">📝</div>
                Full Audio Transcription
            </div>
        """, unsafe_allow_html=True)

        # Download / Copy controls
        col_t1, col_t2 = st.columns([3, 1])
        with col_t1:
            st.caption(f"Word count: {len(res['transcript'].split())} words")
        with col_t2:
            st.download_button(
                "📥 Download Transcript",
                data=res["transcript"],
                file_name="transcript.txt",
                mime="text/plain",
                use_container_width=True,
            )

        st.text_area(
            "Transcript Text",
            value=res["transcript"],
            height=460,
            label_visibility="collapsed",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- TAB 3: RAG CHAT ASSISTANT ----------------
    with tab_chat:
        st.markdown("""
        <div class="glass-card animate-fade-in">
            <div class="card-header-title">
                <div class="card-header-icon">💬</div>
                Interrogate Video via RAG AI
            </div>
            <p style="color:var(--text-muted); font-size:0.88rem; margin-bottom: 1.2rem;">
                Ask any specific questions about timestamps, quotes, speaker points, or details mentioned in the video.
            </p>
        """, unsafe_allow_html=True)

        # Quick Suggested Prompts
        st.caption("Suggested Questions:")
        s_col1, s_col2, s_col3 = st.columns(3)
        suggested_q = None
        with s_col1:
            if st.button("💡 What were the key conclusions?", use_container_width=True):
                suggested_q = "What were the main conclusions reached in this video?"
        with s_col2:
            if st.button("📋 List all assigned tasks", use_container_width=True):
                suggested_q = "List all tasks and action items mentioned in detail."
        with s_col3:
            if st.button("❓ What questions remained unanswered?", use_container_width=True):
                suggested_q = "What open questions were left unanswered?"

        st.markdown("<hr class='glow-divider'>", unsafe_allow_html=True)

        # Render Chat History
        chat_box = st.container()
        with chat_box:
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.markdown(f'<div class="chat-user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-assistant-bubble">🤖 {message["content"]}</div>', unsafe_allow_html=True)

        # Input box handling
        user_query = st.chat_input("Ask a question about the video...") or suggested_q

        if user_query:
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            with st.spinner("🤖 Searching video context vector store..."):
                try:
                    answer_text = ask_question(res["rag_chain"], user_query)
                except Exception as ex:
                    answer_text = f"⚠️ Could not retrieve answer: {ex}"

            st.session_state.chat_history.append({"role": "assistant", "content": answer_text})
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)