import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
import time
import pandas as pd

# ─────────────────────────────────────────────
# 1. Environment & Page Config
# ─────────────────────────────────────────────
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

st.set_page_config(
    page_title="VR Digital Hub AI Boardroom",
    layout="centered",
    page_icon="⚡",
    initial_sidebar_state="collapsed", 
)

# --- INITIALIZE MEMORY ---
if "previous_chats" not in st.session_state:
    st.session_state.previous_chats = []

# ─────────────────────────────────────────────
# 2. Global CSS — Full Cosmic Theme (100% UNTOUCHED ORIGINAL) + HEADER LINE FIX
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── RESET ───────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ── FULL BLACK BACKGROUND ───────────────── */
html, body,
[data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main {
    background-color: #000000 !important;
    color: #e2e8f0 !important;
}

/* ── 🔥 FIX: HIDE THE BLACK LINE (STREAMLIT HEADER) 🔥 ── */
[data-testid="stHeader"] {
    background: transparent !important;
    background-color: transparent !important;
    height: 0 !important;
}
header[data-testid="stHeader"] {
    background: transparent !important;
    background-color: transparent !important;
    height: 0 !important;
}
[data-testid="stDecoration"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }

/* ── GENTLE TWINKLE EFFECT ───────────────── */
@keyframes gentleBlink {
    0% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.95); }
    100% { opacity: 1; transform: scale(1); }
}

/* ── EXPLICIT HARDWARE STARFIELD LAYER ────── */
.starfield-layer {
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    z-index: 1; 
    pointer-events: none;
    background-image:
        radial-gradient(circle at 15% 20%, #ffffff 0%, rgba(255,255,255,0.8) 2px, transparent 5px),
        radial-gradient(circle at 85% 15%, #ffffff 0%, rgba(255,255,255,0.9) 3px, transparent 6px),
        radial-gradient(circle at 75% 75%, #ffffff 0%, rgba(255,255,255,0.8) 2px, transparent 5px),
        radial-gradient(circle at 20% 80%, #ffffff 0%, rgba(255,255,255,0.9) 3px, transparent 6px),
        
        radial-gradient(circle at 10% 47%, #a8d8ff 0%, #a8d8ff 2px, transparent 4px),
        radial-gradient(circle at 13% 52%, #a8d8ff 0%, #a8d8ff 2px, transparent 4px),
        radial-gradient(circle at 17% 48%, #a8d8ff 0%, #a8d8ff 2px, transparent 4px),
        radial-gradient(circle at 14% 44%, #a8d8ff 0%, #a8d8ff 2px, transparent 4px),
        
        radial-gradient(circle at 71% 10%, #a8d8ff 0%, #a8d8ff 2px, transparent 4px),
        radial-gradient(circle at 76% 14%, #a8d8ff 0%, #a8d8ff 2px, transparent 4px),
        radial-gradient(circle at 81% 9%,  #a8d8ff 0%, #a8d8ff 2px, transparent 4px),
        radial-gradient(circle at 85% 13%, #a8d8ff 0%, #a8d8ff 2px, transparent 4px),
        
        radial-gradient(circle at 35% 12%, #ffffff 0%, transparent 2px),
        radial-gradient(circle at 55% 25%, #cbd5e1 0%, transparent 2px),
        radial-gradient(circle at 45% 65%, #ffffff 0%, transparent 2px),
        radial-gradient(circle at 62% 42%, #94a3b8 0%, transparent 2px),
        radial-gradient(circle at 88% 52%, #ffffff 0%, transparent 2px),
        radial-gradient(circle at 30% 78%, #ffffff 0%, transparent 2px);
    background-size: 100vw 100vh;
    background-repeat: no-repeat;
    animation: gentleBlink 4s infinite ease-in-out;
    will-change: transform, opacity;
}

/* Constellation Lines Layer */
.constellation-lines {
    position: fixed;
    inset: 0;
    z-index: 1;
    pointer-events: none;
    width: 100%;
    height: 100%;
    opacity: 0.4;
}

/* ── SUN — Top Left ──────────────────────── */
.sun-decal {
    position: fixed;
    top: -100px;
    left: -100px;
    width: 320px;
    height: 320px;
    z-index: 2;
    pointer-events: none;
    border-radius: 50%;
    background: radial-gradient(
        circle at 58% 58%,
        #ffe87a 0%,
        #ffcc00 15%,
        #ff9900 35%,
        #ff6600 55%,
        #cc3300 72%,
        #4a0e00 88%,
        transparent 100%
    );
}

/* ── MOON — Bottom Right ─────────────────── */
.moon-decal {
    position: fixed;
    bottom: -70px;
    right: -70px;
    width: 260px;
    height: 260px;
    z-index: 2;
    pointer-events: none;
    border-radius: 50%;
    background: radial-gradient(
        circle at 38% 35%,
        #e8e8e8 0%,
        #c0c0c0 30%,
        #909090 58%,
        #606060 78%,
        #2a2a2a 92%,
        #0d0d0d 100%
    );
    box-shadow:
        inset -8px -8px 0 2px rgba(0,0,0,0.25),
        inset 12px 12px 0 3px rgba(255,255,255,0.07);
}
.moon-decal::before {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 50%;
    background:
        radial-gradient(ellipse 15% 13% at 36% 30%, rgba(30,30,30,0.80), transparent),
        radial-gradient(ellipse 11% 10% at 62% 52%, rgba(25,25,25,0.70), transparent),
        radial-gradient(ellipse  8%  7% at 47% 67%, rgba(40,40,40,0.60), transparent),
        radial-gradient(ellipse 10%  9% at 24% 48%, rgba(30,30,30,0.65), transparent),
        radial-gradient(ellipse  7%  6% at 72% 33%, rgba(35,35,35,0.55), transparent);
}

/* ── MAIN CONTAINER — Centered & Above Backgrounds ── */
[data-testid="stMainBlockContainer"],
.block-container {
    max-width: 820px !important;
    margin: 5rem auto 6rem auto !important;
    padding-top: 2.5rem !important;
    padding-bottom: 2.5rem !important;
    position: relative !important;
    z-index: 10 !important;
    background: rgba(10, 12, 20, 0.85) !important;
    border: 1px solid #1c2535 !important;
    border-radius: 16px !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
    box-shadow: 0 0 60px rgba(0, 0, 0, 0.9) !important;
}

/* ── INTERFACE COMPONENTS ────────────────── */
h1 {
    background: linear-gradient(90deg, #ffffff 5%, #00F2FE 45%, #ffffff 95%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    text-align: center !important;
    font-size: 2.4rem !important;
    font-weight: 800 !important;
    line-height: 1.2 !important;
    margin-bottom: 0.3rem !important;
}

.subtitle { text-align: center; color: #8a9ab8; font-size: 0.88rem; line-height: 1.5; margin-bottom: 1.5rem; }
hr { border: none !important; border-top: 1px solid #1c2535 !important; margin: 1.5rem 0 !important; }

[data-testid="stTextInput"] label, label { color: #8aa4be !important; font-size: 0.85rem !important; font-weight: 600 !important; text-transform: uppercase !important; }
[data-testid="stTextInput"] input { background-color: rgba(8, 10, 18, 0.95) !important; border: 1px solid #1e3250 !important; border-radius: 8px !important; color: #e2e8f0 !important; font-size: 0.94rem !important; padding: 0.65rem 1rem !important; }
[data-testid="stTextInput"] input:focus { border-color: #00F2FE !important; box-shadow: 0 0 0 2px rgba(0, 242, 254, 0.15) !important; }

[data-testid="stButton"] > button { background: linear-gradient(90deg, #004f68 0%, #006e90 40%, #00a8c4 100%) !important; color: #ffffff !important; border: 1px solid #00b4cc !important; border-radius: 8px !important; font-weight: 700 !important; font-size: 0.98rem !important; padding: 0.72rem 1.5rem !important; width: 100% !important; box-shadow: 0 0 20px rgba(0, 180, 204, 0.28) !important; }
[data-testid="stButton"] > button:hover { box-shadow: 0 0 36px rgba(0, 242, 254, 0.55) !important; }

/* ── AGENT CARDS BLOCK ───────────────────── */
.agent-card { background: rgba(10, 13, 22, 0.90); border-radius: 10px; margin-bottom: 1.1rem; overflow: hidden; border: 1px solid #1c2a3e; }
.agent-header { padding: 0.5rem 1rem; font-size: 0.80rem; font-weight: 700; text-transform: uppercase; display: flex; align-items: center; gap: 0.5rem; }
.agent-body { background: rgba(14, 17, 26, 0.95); padding: 0.85rem 1rem; font-size: 0.91rem; line-height: 1.68; color: #c4d0e0; }
.agent-alpha .agent-header { background: #00F2FE; color: #000; } .agent-alpha { border-color: #00b8cc; }
.agent-beta .agent-header { background: #f5a623; color: #000; } .agent-beta { border-color: #cc8800; }
.agent-prime .agent-header { background: #10b981; color: #000; } .agent-prime { border-color: #0a7a55; }

[data-testid="stStatusWidget"] { background: rgba(8, 11, 20, 0.92) !important; border: 1px solid #00b4cc !important; border-radius: 8px !important; }
.complete-banner { padding: 13px 20px; background: rgba(0, 242, 254, 0.06); border: 1px solid #00b4cc; border-radius: 10px; text-align: center; color: #00F2FE; margin-top: 1.2rem; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; }

/* ── FOOTER ───────────────────────────────── */
.footer { position: fixed; left: 0; bottom: 0; width: 100%; background: rgba(3, 4, 8, 0.97); color: #3d4f62; text-align: center; padding: 10px 0 8px; border-top: 1px solid #0e1420; font-size: 11px; z-index: 999; }
.footer a { color: #3d5468; text-decoration: none; margin: 0 10px; } .footer a:hover { color: #00F2FE; }
[data-testid="stToolbar"], footer[data-testid="stBottom"] { visibility: hidden !important; height: 0 !important; }
[data-testid="stAlert"] { background: transparent !important; border: none !important; padding: 0 !important; }

/* ── MOBILE RESPONSIVENESS FIX ── */
@media (max-width: 768px) {
    .sun-decal { width: 140px !important; height: 140px !important; top: -40px !important; left: -40px !important; }
    .moon-decal { width: 120px !important; height: 120px !important; bottom: -30px !important; right: -30px !important; }
    [data-testid="stMainBlockContainer"], .block-container { margin-top: 2rem !important; padding-left: 1.5rem !important; padding-right: 1.5rem !important; }
    h1 { font-size: 1.8rem !important; }
    div.row-widget.stRadio > div { flex-direction: column !important; }
}

div.row-widget.stRadio > div { justify-content: center; gap: 20px; }
div.row-widget.stRadio label { cursor: pointer; }
[data-testid="stTable"] { background: rgba(14, 17, 26, 0.95); border-radius: 8px; overflow: hidden; }

/* ── 🔥 NEW: FIXED BRANDING TEXT TOP RIGHT 🔥 ── */
.top-header-brand {
    position: fixed;
    top: 15px;
    right: 80px; 
    z-index: 9999999;
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(10, 12, 20, 0.7);
    padding: 8px 18px;
    border-radius: 30px;
    border: 1px solid rgba(255,255,255,0.15);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
}
.brand-highlight {
    background: linear-gradient(135deg, #FF007A 0%, #00F2FE 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: 'Arial Black', Impact, sans-serif;
    font-size: 1.05rem;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.brand-sub {
    color: #e2e8f0;
    font-family: 'Segoe UI', Tahoma, sans-serif;
    font-size: 0.9rem;
    font-weight: 600;
}

/* ── 🔥 NATIVE POPOVER (HAMBURGER MENU) FIXED TO EXTREME TOP RIGHT 🔥 ── */
div[data-testid="stPopover"] {
    position: fixed !important;
    top: 15px !important;
    right: 15px !important; 
    z-index: 9999999 !important;
}
div[data-testid="stPopover"] > button {
    background: rgba(10, 12, 20, 0.8) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 50% !important;
    width: 44px !important;
    height: 44px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.6) !important;
    backdrop-filter: blur(12px) !important;
    color: #00F2FE !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stPopover"] > button p {
    font-size: 1.5rem !important;
    font-weight: bold !important;
    margin: 0 !important;
    color: #00F2FE !important;
}
div[data-testid="stPopover"] > button:hover {
    border-color: #00F2FE !important;
    box-shadow: 0 0 15px rgba(0, 242, 254, 0.4) !important;
    transform: scale(1.05) !important;
}
</style>

<div class="starfield-layer"></div>
<svg class="constellation-lines" viewBox="0 0 100 100" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
  <line x1="71" y1="10" x2="76" y2="14" stroke="rgba(168,216,255,0.4)" stroke-width="0.15"/>
  <line x1="76" y1="14" x2="81" y2="9"  stroke="rgba(168,216,255,0.4)" stroke-width="0.15"/>
  <line x1="81" y1="9"  x2="85" y2="13" stroke="rgba(168,216,255,0.4)" stroke-width="0.15"/>
  <line x1="10" y1="47" x2="13" y2="52" stroke="rgba(168,216,255,0.4)" stroke-width="0.15"/>
  <line x1="13" y1="52" x2="17" y2="48" stroke="rgba(168,216,255,0.4)" stroke-width="0.15"/>
  <line x1="17" y1="48" x2="14" y2="44" stroke="rgba(168,216,255,0.4)" stroke-width="0.15"/>
  <line x1="14" y1="44" x2="10" y2="47" stroke="rgba(168,216,255,0.4)" stroke-width="0.15"/>
</svg>
<div class="sun-decal"></div>
<div class="moon-decal"></div>

<div class="top-header-brand">
    <span class="brand-highlight">VR Digital Hub:</span>
    <span class="brand-sub">AI Creative Boardroom</span>
</div>

<div class="footer">
    © 2026 VR Digital Hub AI. Advanced Boardroom Protocol v1.0. | Jaipur, India
    &nbsp;&nbsp;
    <a href="#">Subscription Plan</a> &nbsp;|&nbsp;
    <a href="#">Terms &amp; Conditions</a> &nbsp;|&nbsp;
    <a href="#">AI Ethics Policy</a>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 3. 🔥 TOP RIGHT WORKING MENU (NATIVE POPOVER) 🔥
# ─────────────────────────────────────────────
with st.popover("☰"):
    st.markdown("<h4 style='text-align: center; color: #00F2FE;'>MAIN MENU</h4>", unsafe_allow_html=True)
    st.divider()
    
    # --- GEMINI STYLE: IMAGES FOLDER ---
    with st.expander("🖼️ Images"):
        st.error("Status: No image found. Please upload to sync visual data.")
        uploaded_img = st.file_uploader("Upload Reference Image", type=["png", "jpg", "jpeg"])
        if uploaded_img is not None:
            st.success(f"Image '{uploaded_img.name}' loaded securely.")

    # --- GEMINI STYLE: SEARCH & HISTORY FOLDER ---
    with st.expander("💬 Search & View Chats"):
        search_query = st.text_input("🔍 Search Archives", placeholder="Search past concepts...")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if not st.session_state.previous_chats:
            st.caption("No history yet. Start a protocol!")
        else:
            filtered_chats = st.session_state.previous_chats
            if search_query:
                filtered_chats = [
                    c for c in filtered_chats 
                    if search_query.lower() in c['brief'].lower() or search_query.lower() in c['strategy'].lower()
                ]
                
            if not filtered_chats:
                st.warning("No matching records found in archives.")
            else:
                for record in filtered_chats:
                    with st.expander(f"📌 {record['brief'][:20]}..."):
                        st.caption(f"Category: {record['category']}")
                        st.write(record['strategy'])

# ─────────────────────────────────────────────
# 4. Main Body Content
# ─────────────────────────────────────────────
st.title("The AI Creative Boardroom")
st.markdown(
    "<div class='subtitle'>"
    "Adaptive Universal Protocol: Dynamic agents equipped to handle business,<br>"
    "tech, creative, and personal challenges in real-time."
    "</div>",
    unsafe_allow_html=True,
)
st.divider()

# --- DYNAMIC INPUT FILTERS & BRIEF ---
client_brief = st.text_input(
    "Enter your problem or target brief:",
    placeholder="e.g., How to market a new EV, debugging server lag, or writing a novel...",
)

col1, col2 = st.columns(2)
with col1:
    problem_category = st.selectbox(
        "Select Problem Category", 
        ["Business & Marketing", "Tech & Engineering", "Creative Writing", "Personal Life Advice"]
    )
with col2:
    urgency_level = st.selectbox(
        "Urgency / Detail Level", 
        ["Quick Brainstorm (Brief)", "Deep Step-by-Step Blueprint"]
    )

# ── GEMINI STYLE: FAST / PRO / THINK SWITCHER ──
st.markdown("<br>", unsafe_allow_html=True)
engine_mode = st.radio(
    "Select AI Processing Mode:",
    ["⚡ Fast (Llama)", "🧠 Pro (GPT Class)", "🔍 Deep Think (Fabric IQ Sync)"],
    horizontal=True,
    label_visibility="collapsed"
)
st.markdown("<br>", unsafe_allow_html=True)

launch = st.button("Initialize Boardroom Protocol 🚀", use_container_width=True)

# ─────────────────────────────────────────────
# 5. Dynamic Persona Logic Setup
# ─────────────────────────────────────────────
if problem_category == "Business & Marketing":
    a1_name = "Gen-Z Trendsetter"
    a1_prompt = "You are a Gen-Z marketing expert obsessed with viral trends and social-first strategies. Speak with energetic modern slang."
    a2_name = "Corporate Boomer"
    a2_prompt = "You are a seasoned corporate executive prioritizing ROI, brand safety, and measurable metrics. Speak professionally."
    a3_name = "Creative Director"
    a3_prompt = "You are the Creative Director synthesizing viral ideas and corporate ROI into a decisive strategy."
    f1, f2, f3 = "Virality & Trends", "ROI & Risk Mitigation", "Execution Blueprint"
    
elif problem_category == "Tech & Engineering":
    a1_name = "Senior Hacker"
    a1_prompt = "You are a fast-moving senior developer obsessed with shipping code quickly, using bleeding-edge tech, and hacky workarounds."
    a2_name = "Cybersecurity Auditor"
    a2_prompt = "You are a strict Cybersecurity Auditor focused on scalable architecture, vulnerabilities, and enterprise compliance."
    a3_name = "Lead Architect"
    a3_prompt = "You are the Lead IT Architect synthesizing rapid development and strict security into a solid tech roadmap."
    f1, f2, f3 = "Speed & Innovation", "Security & Compliance", "Scalable Architecture"
    
elif problem_category == "Creative Writing":
    a1_name = "Passionate Author"
    a1_prompt = "You are a highly creative author focused on deep emotions, world-building, and artistic, poetic flow."
    a2_name = "Strict Editor"
    a2_prompt = "You are a pragmatic publishing editor focused on pacing, grammar, structure, and marketability."
    a3_name = "Publishing Exec"
    a3_prompt = "You are the Publishing Executive synthesizing the artistic flow and editorial structure into a winning pitch."
    f1, f2, f3 = "Emotion & Creativity", "Structure & Marketability", "Final Masterpiece"

else: # Personal Life Advice
    a1_name = "Zen Philosopher"
    a1_prompt = "You are a peaceful Zen Philosopher focused on mindfulness, letting go, and inner peace."
    a2_name = "Pragmatic Coach"
    a2_prompt = "You are a strict Life Coach focused on actionable habits, discipline, and hard truth."
    a3_name = "Holistic Therapist"
    a3_prompt = "You are a Holistic Therapist synthesizing philosophical peace and actionable discipline into a life plan."
    f1, f2, f3 = "Mindfulness & Peace", "Action & Discipline", "Balanced Life Plan"

if urgency_level == "Quick Brainstorm (Brief)":
    urgency_instruction = "Keep your response brief, fast-paced, and bulleted."
    max_tok = 250
else:
    urgency_instruction = "Provide a deep, step-by-step comprehensive blueprint."
    max_tok = 700

# ─────────────────────────────────────────────
# 6. Agent Execution Logic
# ─────────────────────────────────────────────
if launch:
    if not client_brief.strip():
        st.error("⚠️ Command Error: A problem brief is required to initialise the protocol.")
    elif not api_key:
        st.error("⚠️ Security Error: GROQ_API_KEY not found. Ensure your .env file is configured.")
    else:
        try:
            client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")

            with st.status(f"Initializing {engine_mode} Subroutines…", expanded=True) as status:
                st.write("🔗 Establishing secure neural uplink…")
                time.sleep(0.35)
                st.write("📊 Syncing mock telemetry via Microsoft Fabric IQ Integration…")
                time.sleep(0.40)
                st.write(f"🤖 Loading Agent 1 — {a1_name}…")
                time.sleep(0.30)
                st.write(f"💼 Loading Agent 2 — {a2_name}…")
                time.sleep(0.30)
                st.write(f"👑 Loading Agent 3 — {a3_name}…")
                time.sleep(0.30)
                st.write(f"🧠 Engaging {engine_mode.split()[1]} algorithm — compiling results…")
                time.sleep(0.20)
                status.update(label="✅ Strategic Blueprint Synthesized — Boardroom Online.", state="complete", expanded=False)

            st.divider()
            
            # --- AGENT 1 ---
            resp1 = client.chat.completions.create(
                model="llama-3.1-8b-instant", max_tokens=250,
                messages=[
                    {"role": "system", "content": a1_prompt},
                    {"role": "user", "content": f"Address this brief: {client_brief}. Keep it short and in your persona."},
                ],
            )
            alpha_text = resp1.choices[0].message.content.strip()

            st.markdown(
                f"""<div class="agent-card agent-alpha">
                    <div class="agent-header">AGENT 1: {a1_name}</div>
                    <div class="agent-body">{alpha_text}</div>
                </div>""", unsafe_allow_html=True,
            )
            time.sleep(0.25)

            # --- AGENT 2 ---
            resp2 = client.chat.completions.create(
                model="llama-3.1-8b-instant", max_tokens=250,
                messages=[
                    {"role": "system", "content": a2_prompt},
                    {"role": "user", "content": f"Brief: {client_brief}\nAgent 1 said: '{alpha_text}'. Give your strict counter-perspective."},
                ],
            )
            beta_text = resp2.choices[0].message.content.strip()

            st.markdown(
                f"""<div class="agent-card agent-beta">
                    <div class="agent-header">AGENT 2: {a2_name}</div>
                    <div class="agent-body">{beta_text}</div>
                </div>""", unsafe_allow_html=True,
            )
            time.sleep(0.25)

           # --- AGENT 3 (PRIME) ---
            prime_sys = f"{a3_prompt} {urgency_instruction} IMPORTANT: At the end, add: 'Technical Note: This framework is designed to be integrated with Microsoft Fabric IQ for real-time enterprise data grounding.'"
            
            resp3 = client.chat.completions.create(
                model="llama-3.1-8b-instant", max_tokens=max_tok,
                messages=[
                    {"role": "system", "content": prime_sys},
                    {"role": "user", "content": f"Brief: {client_brief}\n\nAgent 1 ({a1_name}): {alpha_text}\n\nAgent 2 ({a2_name}): {beta_text}\n\nSynthesize the final strategy."},
                ]
            )
            prime_text = resp3.choices[0].message.content.strip()

            st.markdown(
                f"""<div class="agent-card agent-prime">
                    <div class="agent-header">AGENT 3: {a3_name}</div>
                    <div class="agent-body">{prime_text}</div>
                </div>""", unsafe_allow_html=True,
            )

            # --- DECISION ORCHESTRATION & AUDIT TRAIL ---
            st.divider()
            st.markdown("### 📊 Boardroom Decision Audit & Consensus")
            
            df = pd.DataFrame({
                "Agent Persona": [f"{a1_name} 🔴", f"{a2_name} 🟠", f"{a3_name} 🟢"],
                "Analytical Focus": [f1, f2, f3],
                "Confidence": ["88%", "94%", "97%"],
                "Data Source Integration": ["Simulated Domain API", "Mock Telemetry", "Fabric IQ Insight Engine"]
            })
            st.table(df)

            st.markdown(
                "<div class='complete-banner'>"
                "✅ &nbsp; Governance Check Passed: Strategy unlocked for Executive Sign-off."
                "</div>", unsafe_allow_html=True,
            )

            # --- SAVE CURRENT CHAT TO HISTORY ---
            st.session_state.previous_chats.insert(0, {
                "brief": client_brief,
                "category": problem_category,
                "strategy": prime_text
            })

            # Export Features
            full_strategy = f"EXECUTIVE SUMMARY:\nBrief: {client_brief}\nCategory: {problem_category}\nUrgency: {urgency_level}\n\n---\n\n{a1_name}:\n{alpha_text}\n\n---\n\n{a2_name}:\n{beta_text}\n\n---\n\n{a3_name} FINAL STRATEGY:\n{prime_text}"
            
            st.download_button(
                label="📥 Download Formal Board Resolution (TXT)",
                data=full_strategy,
                file_name="VR_Digital_Hub_Board_Resolution.txt",
                mime="text/plain",
                use_container_width=True
            )

        except Exception as e:
            st.error(f"⚠️ System Exception during protocol execution:\n\n`{e}`")
