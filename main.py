import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
import time

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
# 2. Global CSS — Full Cosmic Theme (Image 2 Fixed)
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

[data-testid="stHeader"] {
    background: transparent !important;
    border-bottom: none !important;
}

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
    z-index: 1; /* Pushed into clear view background */
    pointer-events: none;
    background-image:
        /* Image 2 Exact Big Bright White Stars */
        radial-gradient(circle at 15% 20%, #ffffff 0%, rgba(255,255,255,0.8) 2px, transparent 5px),
        radial-gradient(circle at 85% 15%, #ffffff 0%, rgba(255,255,255,0.9) 3px, transparent 6px),
        radial-gradient(circle at 75% 75%, #ffffff 0%, rgba(255,255,255,0.8) 2px, transparent 5px),
        radial-gradient(circle at 20% 80%, #ffffff 0%, rgba(255,255,255,0.9) 3px, transparent 6px),
        
        /* Clear Constellation Main Blue-White Nodes */
        radial-gradient(circle at 10% 47%, #a8d8ff 0%, #a8d8ff 2px, transparent 4px),
        radial-gradient(circle at 13% 52%, #a8d8ff 0%, #a8d8ff 2px, transparent 4px),
        radial-gradient(circle at 17% 48%, #a8d8ff 0%, #a8d8ff 2px, transparent 4px),
        radial-gradient(circle at 14% 44%, #a8d8ff 0%, #a8d8ff 2px, transparent 4px),
        
        radial-gradient(circle at 71% 10%, #a8d8ff 0%, #a8d8ff 2px, transparent 4px),
        radial-gradient(circle at 76% 14%, #a8d8ff 0%, #a8d8ff 2px, transparent 4px),
        radial-gradient(circle at 81% 9%,  #a8d8ff 0%, #a8d8ff 2px, transparent 4px),
        radial-gradient(circle at 85% 13%, #a8d8ff 0%, #a8d8ff 2px, transparent 4px),
        
        /* Premium Ambient Scattered Stars (Sharp) */
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
    margin: 5rem auto 6rem auto !important; /* Perfect Top Spacing Fix */
    padding-top: 2.5rem !important;
    padding-bottom: 2.5rem !important;
    position: relative !important;
    z-index: 10 !important; /* High Z-index ensures cards sit above celestial layer */
    background: rgba(10, 12, 20, 0.85) !important;
    border: 1px solid #1c2535 !important;
    border-radius: 16px !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
    box-shadow: 0 0 60px rgba(0, 0, 0, 0.9) !important;
}

/* Internal overrides to enforce content stacking */
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlock"],
[data-testid="element-container"] {
    position: relative !important;
    z-index: 10 !important;
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

.subtitle {
    text-align: center;
    color: #8a9ab8;
    font-size: 0.88rem;
    line-height: 1.5;
    margin-bottom: 1.5rem;
}

hr {
    border: none !important;
    border-top: 1px solid #1c2535 !important;
    margin: 1.5rem 0 !important;
}

[data-testid="stTextInput"] label, label {
    color: #8aa4be !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
}

[data-testid="stTextInput"] input {
    background-color: rgba(8, 10, 18, 0.95) !important;
    border: 1px solid #1e3250 !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-size: 0.94rem !important;
    padding: 0.65rem 1rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #00F2FE !important;
    box-shadow: 0 0 0 2px rgba(0, 242, 254, 0.15) !important;
}

[data-testid="stButton"] > button {
    background: linear-gradient(90deg, #004f68 0%, #006e90 40%, #00a8c4 100%) !important;
    color: #ffffff !important;
    border: 1px solid #00b4cc !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 0.98rem !important;
    padding: 0.72rem 1.5rem !important;
    width: 100% !important;
    box-shadow: 0 0 20px rgba(0, 180, 204, 0.28) !important;
}
[data-testid="stButton"] > button:hover {
    box-shadow: 0 0 36px rgba(0, 242, 254, 0.55) !important;
}

/* ── AGENT CARDS BLOCK ───────────────────── */
.agent-card {
    background: rgba(10, 13, 22, 0.90);
    border-radius: 10px;
    margin-bottom: 1.1rem;
    overflow: hidden;
    border: 1px solid #1c2a3e;
}
.agent-header {
    padding: 0.5rem 1rem;
    font-size: 0.80rem;
    font-weight: 700;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.agent-body {
    background: rgba(14, 17, 26, 0.95);
    padding: 0.85rem 1rem;
    font-size: 0.91rem;
    line-height: 1.68;
    color: #c4d0e0;
}
.agent-alpha .agent-header { background: #00F2FE; color: #000; }
.agent-alpha               { border-color: #00b8cc; }
.agent-beta .agent-header  { background: #f5a623; color: #000; }
.agent-beta                { border-color: #cc8800; }
.agent-prime .agent-header { background: #10b981; color: #000; }
.agent-prime               { border-color: #0a7a55; }

[data-testid="stStatusWidget"] {
    background: rgba(8, 11, 20, 0.92) !important;
    border: 1px solid #00b4cc !important;
    border-radius: 8px !important;
}

.complete-banner {
    padding: 13px 20px;
    background: rgba(0, 242, 254, 0.06);
    border: 1px solid #00b4cc;
    border-radius: 10px;
    text-align: center;
    color: #00F2FE;
    margin-top: 1.2rem;
    font-weight: 700;
    font-size: 0.85rem;
    text-transform: uppercase;
}

/* ── FOOTER ───────────────────────────────── */
.footer {
    position: fixed;
    left: 0; bottom: 0;
    width: 100%;
    background: rgba(3, 4, 8, 0.97);
    color: #3d4f62;
    text-align: center;
    padding: 10px 0 8px;
    border-top: 1px solid #0e1420;
    font-size: 11px;
    z-index: 999;
}
.footer a { color: #3d5468; text-decoration: none; margin: 0 10px; }
.footer a:hover { color: #00F2FE; }

#MainMenu, [data-testid="stToolbar"],
footer[data-testid="stBottom"],
[data-testid="stDecoration"] {
    visibility: hidden !important;
    height: 0 !important;
}

[data-testid="stAlert"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
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

<div class="footer">
    © 2026 VR Digital Hub AI. Advanced Boardroom Protocol v1.0. | Jaipur, India
    &nbsp;&nbsp;
    <a href="#">Subscription Plan</a> &nbsp;|&nbsp;
    <a href="#">Terms &amp; Conditions</a> &nbsp;|&nbsp;
    <a href="#">AI Ethics Policy</a>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 4. Main Body Content
# ─────────────────────────────────────────────
st.title("The AI Creative Boardroom")
st.markdown(
    "<div class='subtitle'>"
    "Gate AI creative creator, replication agents, innovative, and brilliant responses,<br>"
    "suitable and other focused cards orientation to the AI Creative Boardroom."
    "</div>",
    unsafe_allow_html=True,
)
st.divider()

client_brief = st.text_input(
    "Enter your target business brief:",
    placeholder="e.g., Brand strategy for a luxury electric car launching in India…",
)

launch = st.button("Initialize Boardroom Protocol 🚀", use_container_width=True)

# ─────────────────────────────────────────────
# 5. Agent Execution Logic
# ─────────────────────────────────────────────
if launch:
    if not client_brief.strip():
        st.error("⚠️ Command Error: A business brief is required to initialise the protocol.")
    elif not api_key:
        st.error("⚠️ Security Error: GROQ_API_KEY not found. Ensure your .env file is configured.")
    else:
        try:
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1",
            )

            with st.status("Initializing Strategic Subroutines…", expanded=True) as status:
                st.write("🔗 Establishing secure neural uplink…")
                time.sleep(0.35)
                st.write("🤖 Loading Agent 1 — Gen-Z Trendsetter…")
                time.sleep(0.30)
                st.write("💼 Loading Agent 2 — Corporate Boomer…")
                time.sleep(0.30)
                st.write("👑 Loading Agent 3 — Creative Director…")
                time.sleep(0.30)
                st.write("🧠 Engaging LLaMA-3.1 liveness checks…")
                time.sleep(0.35)
                st.write("⚙️ Debate algorithm active — compiling results…")
                time.sleep(0.20)
                status.update(
                    label="✅ Strategic Blueprint Synthesized — Boardroom Online.",
                    state="complete",
                    expanded=False,
                )

            st.divider()

            # AGENT 1
            resp1 = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                max_tokens=200,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are Agent 1, a Gen-Z marketing expert obsessed with TikTok, "
                            "viral trends, and social-first strategies. Give a punchy, energetic "
                            "pitch in maximum 3 sentences. Use Gen-Z slang naturally."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"Pitch a viral idea for this business: {client_brief}",
                    },
                ],
            )
            alpha_text = resp1.choices[0].message.content.strip()

            st.markdown(
                f"""<div class="agent-card agent-alpha">
                    <div class="agent-header">AGENT 1: Gen-Z Trendsetter</div>
                    <div class="agent-body">{alpha_text}</div>
                </div>""",
                unsafe_allow_html=True,
            )
            time.sleep(0.25)

            # AGENT 2
            resp2 = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                max_tokens=200,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are Agent 2, a seasoned corporate executive (Corporate Boomer). "
                            "You prioritise ROI, brand equity, and professional credibility. "
                            "Respond with a measured, data-aware counter-pitch in maximum 3 sentences."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"The Gen-Z agent pitched a viral-first idea for '{client_brief}'. "
                            "Give a professional, ROI-driven counter-pitch."
                        ),
                    },
                ],
            )
            beta_text = resp2.choices[0].message.content.strip()

            st.markdown(
                f"""<div class="agent-card agent-beta">
                    <div class="agent-header">AGENT 2: Corporate Boomer</div>
                    <div class="agent-body">{beta_text}</div>
                </div>""",
                unsafe_allow_html=True,
            )
            time.sleep(0.25)

            # AGENT 3
            resp3 = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                max_tokens=350,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are Agent 3, the Creative Director. "
                            "Synthesize the Gen-Z and corporate perspectives "
                            "into a decisive, actionable 3-step final strategy. "
                            "Number the steps clearly. Be bold and specific."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Business: {client_brief}\n\n"
                            f"Gen-Z pitch: {alpha_text}\n\n"
                            f"Corporate pitch: {beta_text}\n\n"
                            "Synthesize a final 3-step winning strategy."
                        ),
                    },
                ],
            )
            prime_text = resp3.choices[0].message.content.strip()

            st.markdown(
                f"""<div class="agent-card agent-prime">
                    <div class="agent-header">AGENT 3: Creative Director</div>
                    <div class="agent-body">{prime_text}</div>
                </div>""",
                unsafe_allow_html=True,
            )

            # Completion Banner
            st.markdown(
                "<div class='complete-banner'>"
                "✅ &nbsp; Strategy Synthesis Protocol Complete // Strategic Blueprint Generated"
                "</div>",
                unsafe_allow_html=True,
            )

        except Exception as e:
            st.error(f"⚠️ System Exception during protocol execution:\n\n`{e}`")
          

