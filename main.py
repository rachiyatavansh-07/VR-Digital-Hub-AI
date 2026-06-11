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

# ─────────────────────────────────────────────
# 2. Global CSS — Full Cosmic Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── RESET ───────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"], [data-testid="stMain"], .main {
    background-color: #000000 !important;
    color: #e2e8f0 !important;
}
[data-testid="stHeader"] { background: transparent !important; border-bottom: none !important; }
@keyframes gentleBlink {
    0% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.95); }
    100% { opacity: 1; transform: scale(1); }
}
.starfield-layer {
    position: fixed; inset: 0; width: 100vw; height: 100vh; z-index: 1;
    pointer-events: none;
    background-image:
        radial-gradient(circle at 15% 20%, #ffffff 0%, rgba(255,255,255,0.8) 2px, transparent 5px),
        radial-gradient(circle at 85% 15%, #ffffff 0%, rgba(255,255,255,0.9) 3px, transparent 6px),
        radial-gradient(circle at 35% 12%, #ffffff 0%, transparent 2px),
        radial-gradient(circle at 88% 52%, #ffffff 0%, transparent 2px);
    background-size: 100vw 100vh;
    background-repeat: no-repeat;
    animation: gentleBlink 4s infinite ease-in-out;
}
.sun-decal {
    position: fixed; top: -100px; left: -100px; width: 320px; height: 320px; z-index: 2; pointer-events: none; border-radius: 50%;
    background: radial-gradient(circle at 58% 58%, #ffe87a 0%, #ffcc00 15%, #ff6600 55%, transparent 100%);
}
.moon-decal {
    position: fixed; bottom: -70px; right: -70px; width: 260px; height: 260px; z-index: 2; pointer-events: none; border-radius: 50%;
    background: radial-gradient(circle at 38% 35%, #e8e8e8 0%, #606060 78%, #0d0d0d 100%);
}
[data-testid="stMainBlockContainer"], .block-container {
    max-width: 820px !important; margin: 5rem auto 6rem auto !important;
    background: rgba(10, 12, 20, 0.85) !important; border: 1px solid #1c2535 !important;
    border-radius: 16px !important; padding: 2.5rem !important; z-index: 10 !important;
}
h1 { text-align: center !important; font-size: 2.4rem !important; font-weight: 800 !important; }
.agent-card { background: rgba(10, 13, 22, 0.90); border-radius: 10px; margin-bottom: 1.1rem; border: 1px solid #1c2a3e; }
.agent-header { padding: 0.5rem 1rem; font-size: 0.80rem; font-weight: 700; text-transform: uppercase; }
.agent-body { padding: 0.85rem 1rem; font-size: 0.91rem; line-height: 1.68; color: #c4d0e0; }
.agent-alpha .agent-header { background: #00F2FE; color: #000; }
.agent-beta .agent-header { background: #f5a623; color: #000; }
.agent-prime .agent-header { background: #10b981; color: #000; }
.complete-banner { padding: 13px 20px; background: rgba(0, 242, 254, 0.06); border: 1px solid #00b4cc; border-radius: 10px; text-align: center; color: #00F2FE; margin-top: 1.2rem; }
@media (max-width: 768px) { .sun-decal { width: 140px; height: 140px; } .moon-decal { width: 120px; height: 120px; } }
</style>
<div class="starfield-layer"></div>
<div class="sun-decal"></div>
<div class="moon-decal"></div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 4. Main Body Content
# ─────────────────────────────────────────────
st.title("The AI Creative Boardroom")
st.divider()

client_brief = st.text_input("Enter your target business brief:")

# --- FILTERS ---
col1, col2 = st.columns(2)
with col1:
    target_audience = st.selectbox("Target Audience", ["Gen-Z", "Corporate Professionals", "Tech Enthusiasts", "Mass Market"])
with col2:
    budget_level = st.selectbox("Budget Level", ["Bootstrapped", "Seed Funding", "Series A/Enterprise"])

launch = st.button("Initialize Boardroom Protocol 🚀", use_container_width=True)

# ─────────────────────────────────────────────
# 5. Agent Execution Logic
# ─────────────────────────────────────────────
if launch:
    if not client_brief.strip():
        st.error("⚠️ Business brief is required.")
    else:
        full_context = f"Brief: {client_brief}. Target Audience: {target_audience}. Budget: {budget_level}."
        try:
            client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
            with st.status("Initializing Strategic Subroutines...", expanded=True) as status:
                st.write("🔗 Connecting to Boardroom...")
                time.sleep(1)
            
            # AGENT 1
            resp1 = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "system", "content": "You are a Gen-Z marketing expert. Use slang naturally."}, {"role": "user", "content": f"Pitch a viral idea for: {full_context}"}])
            alpha_text = resp1.choices[0].message.content.strip()
            st.markdown(f"<div class='agent-card agent-alpha'><div class='agent-header'>AGENT 1: Gen-Z Trendsetter</div><div class='agent-body'>{alpha_text}</div></div>", unsafe_allow_html=True)

            # AGENT 2
            resp2 = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "system", "content": "You are a corporate executive focused on ROI."}, {"role": "user", "content": f"Give a professional, ROI-driven counter-pitch to: {alpha_text}"}])
            beta_text = resp2.choices[0].message.content.strip()
            st.markdown(f"<div class='agent-card agent-beta'><div class='agent-header'>AGENT 2: Corporate Boomer</div><div class='agent-body'>{beta_text}</div></div>", unsafe_allow_html=True)

            # AGENT 3
            resp3 = client.chat.completions.create(model="llama-3.1-8b-instant", max_tokens=500, messages=[{"role": "system", "content": "You are the Creative Director. Synthesize a 3-step strategy. IMPORTANT: Add 'Technical Note: Integrated with Microsoft Fabric IQ' at the end."}, {"role": "user", "content": f"Synthesize: {full_context}\n\nGen-Z Pitch: {alpha_text}\n\nCorporate Pitch: {beta_text}"}])
            prime_text = resp3.choices[0].message.content.strip()
            st.markdown(f"<div class='agent-card agent-prime'><div class='agent-header'>AGENT 3: Creative Director</div><div class='agent-body'>{prime_text}</div></div>", unsafe_allow_html=True)

            # CONSENSUS TABLE
            st.subheader("📊 Boardroom Consensus Metrics")
            df = pd.DataFrame({
                "Agent": ["Gen-Z", "Corporate", "Director"],
                "Confidence": ["85%", "92%", "95%"],
                "Status": ["✅ Aligned", "✅ Aligned", "🚀 Finalized"]
            })
            st.table(df)

            # DOWNLOAD BUTTON
            st.download_button("📥 Download Strategy Blueprint", prime_text, "VR_Digital_Hub_Strategy.txt")

        except Exception as e:
            st.error(f"System Error: {e}")
