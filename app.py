import streamlit as st

from backend.transcript import get_transcript, format_timestamp
from backend.text_splitter import create_chunks
from backend.embeddings import create_embeddings
from backend.vector_store import create_vector_store
from backend.retrieval import search_similar_chunks
from backend.llm import (
    generate_answer,
    contextualize_question,
    generate_video_summary
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="YouTubeMind AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 10% 10%, #172554 0%, transparent 40%),
        radial-gradient(ellipse at 90% 80%, #312e81 0%, transparent 35%),
        #080d19;

    color: #f8fafc;
    background-size: 150% 150%;
    animation: backgroundMove 18s ease-in-out infinite alternate;
}

@keyframes backgroundMove {
    0% { background-position: 0% 0%; }
    100% { background-position: 100% 100%; }
}

.block-container,
[data-testid="stMainBlockContainer"] {
    max-width: 100% !important;
    width: 100% !important;
    padding: 3rem 2.5rem 3rem 2.5rem !important;
    box-sizing: border-box !important;
}

/* HEADER */

header[data-testid="stHeader"] {
    background: transparent !important;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #0d1424;
    border-right: 1px solid #263248;
}

section[data-testid="stSidebar"] .block-container {
    padding: 2rem 1rem !important;
}

/* HERO */

.hero-card {
    position: relative;
    overflow: hidden;
    background: linear-gradient(
        120deg,
        #172554,
        #312e81,
        #4c1d95,
        #1e3a8a
    );
    background-size: 300% 300%;
    animation: gradientFlow 9s ease infinite, fadeUp 0.8s ease both;
    padding: 48px;
    border-radius: 22px;
    border: 1px solid rgba(165,180,252,0.3);
    margin-bottom: 35px;
    width: 100%;
    box-sizing: border-box;
}

@keyframes gradientFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.hero-title {
    font-size: clamp(32px, 4vw, 48px);
    font-weight: 800;
    color: white;
    letter-spacing: -1.5px;
    margin-bottom: 12px;
}

.hero-subtitle {
    color: #dbeafe;
    font-size: 16px;
    line-height: 1.8;
    max-width: 750px;
}

.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.14);
    color: #ddd6fe;
    padding: 8px 16px;
    border-radius: 30px;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 18px;
    animation: badgeFloat 3s ease-in-out infinite;
}

@keyframes badgeFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
}

@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* MAIN URL INPUT */

.url-heading {
    text-align: center;
    font-size: 25px;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 8px;
}

.url-description {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 22px;
}

.url-card {
    background: linear-gradient(145deg, #111c30, #17243b);
    border: 1px solid #334155;
    border-radius: 18px;
    padding: 25px;
    margin-bottom: 35px;
}

/* BUTTONS */

.stButton > button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    background-size: 200% auto;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 11px 20px;
    font-weight: 700;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background-position: right center;
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(99,102,241,0.35);
    color: white;
    border: none;
}

/* INPUTS */

.stTextInput input,
.stSelectbox div[data-baseweb="select"] {
    background: #111c30 !important;
    border-radius: 10px !important;
    border-color: #334155 !important;
    color: white !important;
}

/* FEATURE CARDS */

.feature-card {
    background: linear-gradient(145deg, #111c30, #17243b);
    border: 1px solid #334155;
    border-radius: 16px;
    overflow: hidden;
    height: 100%;
    transition: all 0.35s ease;
    animation: fadeUp 0.8s ease both;
}

.feature-card:hover {
    transform: translateY(-8px);
    border-color: #818cf8;
    box-shadow: 0 12px 30px rgba(99,102,241,0.18);
}

.feature-card img {
    width: 100%;
    height: 165px;
    object-fit: cover;
    display: block;
}

.feature-content {
    padding: 20px;
}

.feature-content h3 {
    color: white;
    font-size: 20px;
    margin-bottom: 10px;
}

.feature-content p {
    color: #a5b4c8;
    font-size: 14px;
    line-height: 1.7;
}

/* METRICS */

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #111c30, #17243b);
    border: 1px solid #263650;
    padding: 20px;
    border-radius: 15px;
    transition: all 0.3s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    border-color: #818cf8;
}

[data-testid="stMetricValue"] {
    color: #a5b4fc !important;
    font-weight: 800;
}

/* TABS */

.stTabs [data-baseweb="tab-list"] {
    gap: 15px;
    border-bottom: 1px solid #263650;
}

.stTabs [data-baseweb="tab"] {
    color: #94a3b8;
    font-weight: 600;
    padding: 12px 18px;
}

.stTabs [aria-selected="true"] {
    color: #a5b4fc !important;
}

/* CHAT */

[data-testid="stChatMessage"] {
    background: #111c30;
    border: 1px solid #263650;
    border-radius: 14px;
    padding: 15px;
    animation: fadeUp 0.4s ease both;
}

/* EXPANDER */

div[data-testid="stExpander"] {
    background: #111c30;
    border: 1px solid #263650;
    border-radius: 12px;
}

/* FOOTER */

.footer {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    padding: 30px;
}

/* RESPONSIVE */

@media (max-width: 768px) {

    .hero-card {
        padding: 25px;
    }

    .block-container {
        padding: 1.5rem 1rem !important;
    }

}

/* ACCESSIBILITY */

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SESSION STATE
# ==========================================

defaults = {
    "transcript": None,
    "chunks": None,
    "vector_index": None,
    "chat_history": [],
    "video_summary": None,
    "summary_type": None,
    "current_video_url": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("# 🎬 YouTubeMind")

    st.caption("AI VIDEO INTELLIGENCE PLATFORM")

    st.divider()

    st.markdown("### ✨ Platform Features")

    st.markdown("""
    - 🧠 AI-powered video chat
    - 💬 Conversational memory
    - 📝 Intelligent summaries
    - 🔍 Semantic search
    - 📚 Transcript extraction
    """)

    st.divider()

    st.markdown("### ⚙️ Workspace")

    if st.session_state.vector_index is not None:

        st.success("Video processed and ready!")

        if st.button("🗑️ Clear Chat", use_container_width=True):

            st.session_state.chat_history = []
            st.rerun()

    else:

        st.info("Your workspace is ready.")

    st.divider()

    st.markdown("""
    <div style="text-align:center;color:#64748b;font-size:12px;">
        Powered by Gemini + FAISS
        <br><br>
        YouTubeMind AI © 2026
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# HERO SECTION
# ==========================================

st.html("""
<div class="hero-card">

    <div class="hero-badge">
        ✨ AI-POWERED VIDEO INTELLIGENCE
    </div>

    <div class="hero-title">
        YouTubeMind AI
    </div>

    <div class="hero-subtitle">
        Transform YouTube videos into knowledge.
        <br>
        Chat with videos, generate intelligent summaries,
        and discover insights using artificial intelligence.
    </div>

</div>
""")


# ==========================================
# CENTRAL VIDEO INPUT
# ==========================================

st.html("""
<div class="url-heading">
    🎬 Start With Your YouTube Video
</div>

<div class="url-description">
    Paste a video link and let AI transform it into knowledge.
</div>
""")

url_col1, url_col2, url_col3 = st.columns([1, 5, 1])

with url_col2:

    video_url = st.text_input(
        "YouTube Video URL",
        placeholder="https://www.youtube.com/watch?v=...",
        label_visibility="collapsed"
    )

    process_button = st.button(
        "🚀 Process Video",
        use_container_width=True,
        key="main_process_video"
    )


# ==========================================
# PROCESS VIDEO
# ==========================================

if process_button:

    if not video_url:

        st.warning("Please enter a YouTube URL.")

    else:

        try:

            with st.spinner("Extracting YouTube transcript..."):

                transcript = get_transcript(video_url)

            if not transcript:

                st.error("Unable to extract transcript.")

            else:

                with st.spinner("Creating intelligent text chunks..."):

                    chunks = create_chunks(transcript)

                with st.spinner("Generating embeddings..."):

                    embeddings = create_embeddings(chunks)

                with st.spinner("Building FAISS vector database..."):

                    vector_index = create_vector_store(embeddings)

                st.session_state.transcript = transcript
                st.session_state.chunks = chunks
                st.session_state.vector_index = vector_index

                st.session_state.chat_history = []
                st.session_state.video_summary = None
                st.session_state.summary_type = None
                st.session_state.current_video_url = video_url

                st.success("Video processed successfully!")

        except Exception as error:

            st.error(f"Processing Error: {error}")


# ==========================================
# WELCOME SCREEN
# ==========================================

if st.session_state.vector_index is None:

    st.markdown("## 🚀 Explore What You Can Do")

    st.caption(
        "Everything you need to understand and explore YouTube videos."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.html("""
        <div class="feature-card">

            <img src="https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800"
                 alt="Artificial Intelligence">

            <div class="feature-content">

                <h3>🧠 AI Chat</h3>

                <p>
                    Ask questions and get intelligent answers
                    directly from your video content.
                </p>

            </div>
        </div>
        """)

    with col2:

        st.html("""
        <div class="feature-card">

            <img src="https://images.unsplash.com/photo-1455390582262-044cdead277a?w=800"
                 alt="Writing and summaries">

            <div class="feature-content">

                <h3>📝 Smart Summary</h3>

                <p>
                    Generate short summaries, detailed explanations
                    and important takeaways.
                </p>

            </div>
        </div>
        """)

    with col3:

        st.html("""
        <div class="feature-card">

            <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800"
                 alt="Data analytics">

            <div class="feature-content">

                <h3>🔍 Semantic Search</h3>

                <p>
                    Discover relevant information from
                    thousands of transcript segments.
                </p>

            </div>
        </div>
        """)


# ==========================================
# DASHBOARD
# ==========================================

else:

    st.divider()

    st.markdown("## 📊 Video Analytics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Transcript Segments",
        len(st.session_state.transcript)
    )

    col2.metric(
        "Text Chunks",
        len(st.session_state.chunks)
    )

    col3.metric(
        "FAISS Vectors",
        st.session_state.vector_index.ntotal
    )

    col4.metric(
        "Dimensions",
        st.session_state.vector_index.d
    )

    st.divider()

    # ======================================
    # MAIN WORKSPACE TABS
    # ======================================

    tab1, tab2, tab3 = st.tabs([
        "📝 AI Summary",
        "💬 Chat with Video",
        "📄 Transcript"
    ])


    # ======================================
    # TAB 1: SUMMARY
    # ======================================

    with tab1:

        st.subheader("AI Video Summarizer")

        st.caption(
            "Convert lengthy videos into easy-to-understand knowledge."
        )

        summary_option = st.selectbox(
            "Select Summary Type",
            ["Short", "Detailed", "Key Takeaways"]
        )

        if st.button("✨ Generate Summary"):

            try:

                with st.spinner("Gemini is analyzing your video..."):

                    summary = generate_video_summary(
                        st.session_state.chunks,
                        summary_option
                    )

                st.session_state.video_summary = summary
                st.session_state.summary_type = summary_option

            except Exception as error:

                st.error(f"Summary Error: {error}")


        if st.session_state.video_summary:

            st.divider()

            st.markdown(
                f"### 📌 {st.session_state.summary_type} Summary"
            )

            st.markdown(st.session_state.video_summary)

            st.download_button(
                "⬇️ Download Summary",
                data=st.session_state.video_summary,
                file_name="youtube_summary.txt",
                mime="text/plain"
            )

        else:

            st.info(
                "Choose a summary type and click Generate Summary."
            )


    # ======================================
    # TAB 2: AI CHAT
    # ======================================
    with tab2:

        st.subheader("💬 Chat with Your Video")

        st.caption(
            "Ask questions and get intelligent answers "
            "based on your video."
        )

        # ==================================
        # QUESTION INPUT AT THE TOP
        # ==================================

        with st.form(key="chat_form", clear_on_submit=True):

            question = st.text_input(
                "Ask your question",
                placeholder="Ask anything about this video..."
            )

            send_button = st.form_submit_button(
                "🚀 Send Question",
                use_container_width=True
            )

        # ==================================
        # PROCESS NEW QUESTION
        # ==================================

        if send_button and question.strip():

            previous_history = st.session_state.chat_history.copy()

            try:

                with st.spinner("Understanding your question..."):

                    standalone_question = contextualize_question(
                        question,
                        previous_history
                    )

                with st.spinner("Searching video information..."):

                    results = search_similar_chunks(
                        standalone_question,
                        st.session_state.vector_index,
                        st.session_state.chunks,
                        top_k=3
                    )

                if results:

                    context = "\n\n".join(
                        [result["chunk"] for result in results]
                    )

                    with st.spinner("Gemini is generating your answer..."):

                        answer = generate_answer(
                            question,
                            context,
                            chat_history=previous_history
                        )

                else:

                    answer = (
                        "I couldn't find relevant information "
                        "in this video's transcript."
                    )

                # SAVE NEW CONVERSATION

                st.session_state.chat_history.append({
                    "role": "user",
                    "content": question
                })

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer
                })

                # Save retrieved sources for this interaction
                st.session_state.last_retrieved_sources = results

                # Refresh to display newest conversation at the top
                st.rerun()

            except Exception as error:

                st.error(f"AI Error: {error}")

        # ==================================
        # CONVERSATION HISTORY
        # NEWEST FIRST
        # ==================================

        st.divider()

        st.markdown("### 🕒 Conversation History")

        if st.session_state.chat_history:

            history = st.session_state.chat_history

            # Group messages into question-answer pairs
            conversations = []

            for i in range(0, len(history), 2):

                user_message = history[i]

                assistant_message = (
                    history[i + 1]
                    if i + 1 < len(history)
                    else None
                )

                conversations.append(
                    (user_message, assistant_message)
                )

            # Display newest conversation first
            for user_message, assistant_message in reversed(conversations):

                # QUESTION FIRST
                st.markdown(
                    f"""
                    <div style="
                        background:#17243b;
                        border:1px solid #334155;
                        border-radius:12px;
                        padding:18px;
                        margin-top:15px;
                        margin-bottom:10px;
                    ">
                        <span style="color:#a5b4fc;font-weight:700;">
                            👤 YOU
                        </span>
                        <br><br>
                        {user_message["content"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # ANSWER SECOND
                if assistant_message:

                    st.markdown(
                        f"""
                        <div style="
                            background:#102b2a;
                            border:1px solid #25635b;
                            border-radius:12px;
                            padding:18px;
                            margin-bottom:20px;
                        ">
                            <span style="color:#6ee7b7;font-weight:700;">
                                🤖 YOUTUBEMIND AI
                            </span>
                            <br><br>
                            {assistant_message["content"]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            st.divider()

            if st.button("🗑️ Clear Conversation"):

                st.session_state.chat_history = []
                st.rerun()

        else:

            st.info("👋 No conversations yet. Ask your first question!")

    # ======================================
    # TAB 3: TRANSCRIPT
    # ======================================

    with tab3:

        st.subheader("Video Transcript")

        st.caption(
            f"{len(st.session_state.transcript)} transcript segments available."
        )

        search_transcript = st.text_input(
            "Search Transcript",
            placeholder="Search for a word or phrase..."
        )

        for item in st.session_state.transcript:

            text = item["text"]

            if (
                not search_transcript
                or search_transcript.lower() in text.lower()
            ):

                timestamp = format_timestamp(item["start"])

                with st.container():

                    st.markdown(f"**⏱️ {timestamp}**")

                    st.write(text)

                    st.divider()


# ==========================================
# FOOTER
# ==========================================

st.html("""
<div class="footer">
    <h4 style="color:#a5b4fc;">🎬 YouTubeMind AI</h4>

    Built with Python · Streamlit · FAISS · Google Gemini

    <br><br>

    Turning videos into knowledge.
</div>
""")