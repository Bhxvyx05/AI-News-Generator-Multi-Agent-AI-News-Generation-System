# ==========================================================
# AI News Generator — Modern Dashboard
# Frontend only. Backend/agent logic is untouched.
# ==========================================================

import os
import re
import html
import base64
import mimetypes
from datetime import datetime

import streamlit as st

from agents.search_agent import run_search_agent
from agents.article_agent import generate_article
from agents.image_agent import (
    load_pipeline,
    generate_image,
)

# fpdf2 is used only for the "Download as PDF" feature.
# Install with:  pip install fpdf2
try:
    from fpdf import FPDF
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="AI News Generator",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================================
# GLOBAL STYLE
# Every colored block below is either:
#   (a) fully self-contained in ONE st.markdown call, or
#   (b) a native Streamlit widget/container (theme-aware).
# This is what actually guarantees contrast — no more
# "open a div here, close it 10 lines later" tricks, which
# Streamlit does not render as real nesting.
# ==========================================================
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Merriweather:wght@400;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        #MainMenu, footer {visibility: hidden;}

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1150px;
        }

        /* ---------- Hero ---------- */
        .hero {
            background: linear-gradient(120deg, #4f46e5 0%, #7c3aed 50%, #db2777 100%);
            padding: 2.4rem 2.2rem;
            border-radius: 20px;
            color: #ffffff;
            margin-bottom: 1.6rem;
            box-shadow: 0 10px 30px rgba(79, 70, 229, 0.25);
        }
        .hero h1 {
            font-size: 2.3rem;
            font-weight: 800;
            margin: 0 0 0.4rem 0;
            color: #ffffff;
        }
        .hero p {
            font-size: 1.02rem;
            opacity: 0.95;
            margin: 0;
            color: #f5f3ff;
        }
        .pill-row { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 1rem; }
        .pill {
            background: rgba(255,255,255,0.18);
            border: 1px solid rgba(255,255,255,0.4);
            padding: 0.3rem 0.85rem;
            border-radius: 999px;
            font-size: 0.82rem;
            font-weight: 600;
            color: #ffffff;
        }

        /* ---------- Trending topic buttons ---------- */
        div[data-testid="column"] .stButton button {
            border-radius: 12px;
            font-weight: 600;
            padding: 0.5rem 0.6rem;
            transition: all 0.15s ease-in-out;
        }
        div[data-testid="column"] .stButton button:hover {
            border-color: #7c3aed;
            color: #7c3aed;
            transform: translateY(-1px);
        }

        /* ---------- Primary (Generate) button ---------- */
        .stButton>button[kind="primary"] {
            background: linear-gradient(120deg, #4f46e5, #db2777) !important;
            border: none !important;
            color: #ffffff !important;
            border-radius: 12px;
            font-weight: 700;
            padding: 0.7rem 1rem;
            box-shadow: 0 6px 16px rgba(124, 58, 237, 0.35);
        }

        /* ---------- Metrics ---------- */
        div[data-testid="stMetric"] {
            background: rgba(124, 58, 237, 0.08);
            border-radius: 14px;
            padding: 0.8rem 1rem;
            border: 1px solid rgba(124, 58, 237, 0.2);
        }

        /* ---------- Article "paper" block ----------
           Self-contained: background + text colors are
           declared together, so contrast never depends
           on whatever theme/background is behind it. */
        .paper {
            background: #fffdf8;
            border-radius: 20px;
            border: 1px solid #ece7db;
            padding: 2.6rem 3rem;
            box-shadow: 0 8px 26px rgba(15, 23, 42, 0.12);
        }
        .paper .meta {
            color: #6b7280;
            font-size: 0.88rem;
            margin-bottom: 1.4rem;
            border-bottom: 1px solid #ece7db;
            padding-bottom: 1.2rem;
        }
        .paper .headline {
            font-family: 'Merriweather', serif;
            font-size: 2.1rem;
            font-weight: 700;
            line-height: 1.25;
            color: #111827;
            margin-bottom: 0.3rem;
        }
        .paper .body-text {
            font-family: 'Merriweather', serif;
            font-size: 1.08rem;
            line-height: 1.9;
            color: #1f2937;
            text-align: justify;
        }
        .paper .body-text p { margin: 0 0 1.1rem 0; }
        .paper .body-text h3 {
            font-family: 'Merriweather', serif;
            color: #111827;
            margin: 1.2rem 0 0.6rem 0;
        }
        .paper img {
            width: 100%;
            border-radius: 14px;
            margin: 1.8rem 0 0.4rem 0;
            display: block;
        }
        .paper .img-caption {
            text-align: center;
            font-size: 0.85rem;
            color: #8a8a8a;
            margin-bottom: 1.8rem;
            font-style: italic;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================================
# CACHE IMAGE MODEL
# ==========================================================
@st.cache_resource
def get_pipeline():
    return load_pipeline()

pipe = get_pipeline()

# ==========================================================
# SESSION STATE DEFAULTS
# ==========================================================
for key, default in {
    "topic": "",
    "article": None,
    "image_path": None,
    "generated_at": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ==========================================================
# HELPERS
# ==========================================================
def reading_time(text: str) -> int:
    words = len(text.split())
    return max(1, round(words / 200))


def clean_markdown(text: str) -> str:
    """Strip markdown syntax so it reads cleanly as plain text (used for PDF)."""
    text = re.sub(r"#{1,6}\s*", "", text)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"`(.*?)`", r"\1", text)
    return text.strip()


def extract_headline(article_text: str, fallback: str) -> str:
    for line in article_text.splitlines():
        line = line.strip()
        if line.startswith("#"):
            return line.lstrip("#").strip()
        if line:
            return fallback
    return fallback


def split_body_for_image(article_text: str):
    """Split the article body into two halves so an image can sit in the middle."""
    paragraphs = [p for p in article_text.split("\n\n") if p.strip()]
    if paragraphs and paragraphs[0].strip().startswith("#"):
        paragraphs = paragraphs[1:]
    if len(paragraphs) <= 1:
        return paragraphs, []
    mid = max(1, len(paragraphs) // 2)
    return paragraphs[:mid], paragraphs[mid:]


def paragraphs_to_html(paragraphs) -> str:
    """Turn a list of markdown-ish paragraphs into safe, styled HTML.

    Escapes the text first (so raw AI output can't break the page or
    inject unwanted markup), then re-applies basic **bold** / *italic*
    / #-heading formatting on top of the escaped text.
    """
    chunks = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if para.startswith("#"):
            heading = html.escape(para.lstrip("#").strip())
            chunks.append(f"<h3>{heading}</h3>")
            continue
        text = html.escape(para)
        text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"\*(.*?)\*", r"<em>\1</em>", text)
        chunks.append(f"<p>{text}</p>")
    return "\n".join(chunks)


def image_to_base64(image_path: str) -> str:
    mime, _ = mimetypes.guess_type(image_path)
    mime = mime or "image/png"
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


def build_pdf(topic: str, article_text: str, image_path: str) -> bytes:
    """Build a formal-looking PDF with the image placed mid-article."""
    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    headline = extract_headline(article_text, topic)
    first_paras, second_paras = split_body_for_image(article_text)
    first_half = "\n\n".join(first_paras)
    second_half = "\n\n".join(second_paras)

    def safe(t: str) -> str:
        return t.encode("latin-1", "replace").decode("latin-1")

    pdf.set_font("Times", "B", 20)
    pdf.multi_cell(0, 10, safe(headline), align="C")
    pdf.ln(1)

    pdf.set_font("Times", "I", 11)
    pdf.set_text_color(110, 110, 110)
    pdf.cell(0, 8, safe(f"AI News Desk  |  {datetime.now().strftime('%B %d, %Y')}"), align="C", ln=True)
    pdf.ln(2)

    pdf.set_draw_color(210, 210, 210)
    y = pdf.get_y()
    pdf.line(20, y, 190, y)
    pdf.ln(8)

    pdf.set_text_color(20, 20, 20)
    pdf.set_font("Times", "", 12)
    pdf.multi_cell(0, 7, safe(clean_markdown(first_half)))
    pdf.ln(4)

    if image_path and os.path.exists(image_path):
        img_width = 130
        x_pos = (210 - img_width) / 2
        pdf.image(image_path, x=x_pos, w=img_width)
        pdf.ln(6)

    if second_half:
        pdf.multi_cell(0, 7, safe(clean_markdown(second_half)))

    return bytes(pdf.output())


# ==========================================================
# HERO / HEADER
# ==========================================================
st.markdown(
    """
    <div class="hero">
        <h1>📰 AI News Generator</h1>
        <p>Turn any topic into a fully written, illustrated news article — powered by web search, AI writing, and AI image generation.</p>
        <div class="pill-row">
            <span class="pill">🌐 Web Search</span>
            <span class="pill">🤖 AI Summarization</span>
            <span class="pill">📰 AI Writing</span>
            <span class="pill">🎨 AI Imagery</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==========================================================
# TRENDING TOPICS  (real Streamlit container, not a manual div)
# ==========================================================
with st.container(border=True):
    st.markdown("#### 🔥 Trending Topics")

    topics = [
        "Artificial Intelligence",
        "Climate Change",
        "IPL 2026",
        "Global Economy",
        "Online Gaming",
        "Cyber Security",
        "Space Exploration",
        "Electric Vehicles",
    ]

    cols = st.columns(4)
    for i, t in enumerate(topics):
        with cols[i % 4]:
            is_selected = st.session_state.get("topic") == t
            if st.button(t, key=f"topic_{i}", use_container_width=True,
                         type="primary" if is_selected else "secondary"):
                st.session_state["topic"] = t
                st.rerun()

# ==========================================================
# TOPIC INPUT + GENERATE  (real Streamlit container)
# ==========================================================
with st.container(border=True):
    st.markdown("#### ✍️ Your Topic")

    topic = st.text_input(
        "Enter Topic",
        value=st.session_state.get("topic", ""),
        placeholder="Example: Impact of Online Gaming",
        label_visibility="collapsed",
    )
    st.session_state["topic"] = topic

    generate_clicked = st.button("🚀 Generate News", use_container_width=True, type="primary")

# ==========================================================
# GENERATION PIPELINE
# ==========================================================
if generate_clicked:

    if not topic.strip():
        st.warning("Please enter a topic.")
        st.stop()

    try:
        with st.status("Generating your article...", expanded=True) as status:

            st.write("🔎 Searching the web...")
            summary_path = run_search_agent(topic)
            st.write("✅ Web search complete")

            st.write("📰 Writing the article...")
            article = generate_article(summary_path)
            st.write("✅ Article drafted")

            st.write("🎨 Generating the image...")
            image_path = generate_image(article, pipe)
            st.write("✅ Image generated")

            status.update(label="✅ Generation completed!", state="complete", expanded=False)

        st.session_state["article"] = article
        st.session_state["image_path"] = image_path
        st.session_state["generated_at"] = datetime.now()

    except Exception as e:
        st.error(f"Something went wrong: {e}")

# ==========================================================
# RESULTS
# ==========================================================
if st.session_state.get("article"):

    article = st.session_state["article"]
    image_path = st.session_state["image_path"]
    generated_at = st.session_state["generated_at"]

    st.divider()

    # ---- Stats row ----
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Topic", st.session_state.get("topic", "-"))
    m2.metric("Word Count", len(article.split()))
    m3.metric("Reading Time", f"{reading_time(article)} min")
    m4.metric("Generated At", generated_at.strftime("%H:%M:%S") if generated_at else "-")

    st.write("")

    # ---- Formal article, rendered as ONE self-contained HTML block ----
    headline = extract_headline(article, st.session_state.get("topic", "News Article"))
    first_paras, second_paras = split_body_for_image(article)
    first_html = paragraphs_to_html(first_paras)
    second_html = paragraphs_to_html(second_paras)

    image_tag = ""
    if image_path and os.path.exists(image_path):
        img_data_uri = image_to_base64(image_path)
        image_tag = (
            f'<img src="{img_data_uri}" alt="Article illustration" />'
            f'<div class="img-caption">AI-generated illustration for this article</div>'
        )

    article_html = f"""
    <div class="paper">
        <div class="headline">{html.escape(headline)}</div>
        <div class="meta">AI News Desk · {generated_at.strftime("%B %d, %Y — %H:%M") if generated_at else ""}</div>
        <div class="body-text">
            {first_html}
            {image_tag}
            {second_html}
        </div>
    </div>
    """
    st.markdown(article_html, unsafe_allow_html=True)

    st.write("")

    # ---- Downloads ----
    d1, d2, d3 = st.columns(3)

    with d1:
        st.download_button(
            "⬇ Download Article (Markdown)",
            article,
            file_name="final_article.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with d2:
        if PDF_AVAILABLE:
            pdf_bytes = build_pdf(st.session_state.get("topic", "News Article"), article, image_path)
            st.download_button(
                "⬇ Download Article (PDF)",
                pdf_bytes,
                file_name="final_article.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            st.button("⬇ PDF unavailable — run: pip install fpdf2", disabled=True, use_container_width=True)

    with d3:
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as file:
                st.download_button(
                    "⬇ Download Image",
                    file,
                    file_name="generated_news.png",
                    mime="image/png",
                    use_container_width=True,
                )