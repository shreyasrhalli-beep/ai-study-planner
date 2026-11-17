import json
import os
from datetime import date, datetime
from pathlib import Path

import streamlit as st
import urllib.request
import urllib.error

# ---------------- CONFIGURATION ----------------
APP_NAME = "StudyFlow AI"
DEFAULT_MODEL = "gemini-2.5-flash"
DATA_FILE = Path("studyflow_data.json")

BG = "#0B1020"
SIDEBAR = "#10182B"
PANEL = "#151F35"
CARD = "#1B2942"
BLUE = "#718CFF"
PURPLE = "#A78BFA"
GREEN = "#42D6A4"
ORANGE = "#FFB86B"
RED = "#FF7185"
WHITE = "#F3F5FF"
MUTED = "#93A1BC"
BORDER = "#293753"

# ---------------- PAGE + STYLING ----------------
st.set_page_config(
    page_title=APP_NAME,
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

html, body, [class*="css"] { font-family: Inter, sans-serif; }
.stApp {
  color: #ECF5FF;
  background:
    linear-gradient(rgba(28,53,82,.10) 1px, transparent 1px),
    linear-gradient(90deg, rgba(28,53,82,.10) 1px, transparent 1px),
    radial-gradient(ellipse at 12% 5%, rgba(0,207,255,.17), transparent 32%),
    radial-gradient(ellipse at 88% 18%, rgba(119,91,255,.19), transparent 30%),
    radial-gradient(ellipse at 55% 100%, rgba(0,255,190,.09), transparent 35%),
    #070D18;
  background-size: 42px 42px, 42px 42px, auto, auto, auto, auto;
  background-attachment: fixed;
}
[data-testid="stHeader"] { background: rgba(5,12,23,.72); }
[data-testid="stSidebar"] {
  background: linear-gradient(165deg, rgba(13,29,48,.97), rgba(8,15,29,.98));
  border-right: 1px solid rgba(91,211,255,.20);
  box-shadow: 12px 0 45px rgba(0,0,0,.22);
}
[data-testid="stSidebar"] * { color: #EAF5FF; }
h1,h2,h3,h4,p,label { color: #ECF5FF; }
.brand { font-family: 'Space Grotesk',sans-serif; font-size: 25px; font-weight: 700; letter-spacing: -.8px; }
.muted { color: #9EB5CC; }
.eyebrow { color: #56DFFF; font-size: 10px; font-weight: 800; letter-spacing: 2px; }

.glass-hero {
  position: relative; overflow: hidden; isolation: isolate;
  padding: 31px 34px; margin: 2px 0 25px; border-radius: 23px;
  border: 1px solid rgba(104,220,255,.38);
  background: linear-gradient(112deg, rgba(12,79,111,.74), rgba(30,48,91,.72) 54%, rgba(57,42,111,.70));
  box-shadow: 0 18px 55px rgba(0,0,0,.34), 0 0 34px rgba(0,194,255,.10), inset 0 1px 0 rgba(255,255,255,.17);
  backdrop-filter: blur(28px) saturate(150%); -webkit-backdrop-filter: blur(28px) saturate(150%);
  animation: riseIn .6s ease both;
}
.glass-hero:before {
  content:""; position:absolute; z-index:-1; width:260px; height:260px; right:7%; top:-175px;
  border-radius:50%; background:rgba(68,226,255,.20); filter:blur(5px);
}
.glass-hero:after {
  content:""; position:absolute; right:-30px; bottom:-85px; width:250px; height:180px;
  border:1px solid rgba(89,222,255,.30); border-radius:50%;
  box-shadow:0 0 0 18px rgba(89,222,255,.035), 0 0 0 38px rgba(89,222,255,.025);
  transform:rotate(-18deg); z-index:-1;
}
.hero-label { color:#62E4FF; font-size:10px; font-weight:800; letter-spacing:2.4px; }
.hero-heading { font-family:'Space Grotesk',sans-serif; color:#FFFFFF; font-size:32px; font-weight:700; letter-spacing:-1.2px; margin:8px 0 5px; }
.hero-caption { color:#C2D9ED; font-size:13px; }
.hero-status { display:inline-block; margin-top:16px; padding:6px 11px; border-radius:30px; border:1px solid rgba(78,235,195,.35); background:rgba(25,190,155,.10); color:#71F2C9; font-size:10px; letter-spacing:1px; font-weight:700; }

.stat-card {
  position:relative; overflow:hidden; isolation:isolate; min-height:146px; padding:21px;
  border-radius:18px; border:1px solid rgba(135,207,239,.25); border-top-color:rgba(215,246,255,.38);
  background:linear-gradient(145deg, rgba(31,65,91,.70), rgba(15,27,48,.82));
  box-shadow:0 14px 34px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.09);
  backdrop-filter:blur(24px) saturate(145%); -webkit-backdrop-filter:blur(24px) saturate(145%);
  transition:transform .22s ease,border-color .22s ease,box-shadow .22s ease;
  animation:riseIn .55s ease both;
}
.stat-card:after { content:""; position:absolute; z-index:-1; right:-48px; top:-62px; width:140px; height:140px; border-radius:50%; background:rgba(0,208,255,.13); filter:blur(4px); }
.stat-card:hover { transform:translateY(-5px); border-color:rgba(70,224,255,.65); box-shadow:0 18px 42px rgba(0,165,220,.13),inset 0 1px 0 rgba(255,255,255,.13); }
.stat-label { color:#9FC5D9; font-size:10px; font-weight:800; letter-spacing:1.5px; }
.stat-value { font-family:'Space Grotesk',sans-serif; color:#F4FBFF; font-size:34px; font-weight:700; margin:10px 0 4px; }
.stat-sub { color:#92AFC4; font-size:12px; }

[data-testid="stVerticalBlockBorderWrapper"] > div {
  border:1px solid rgba(130,203,232,.23) !important; border-radius:19px !important;
  background:linear-gradient(145deg,rgba(27,53,77,.72),rgba(13,24,42,.82)) !important;
  box-shadow:0 13px 32px rgba(0,0,0,.24),inset 0 1px 0 rgba(255,255,255,.055);
  backdrop-filter:blur(23px) saturate(140%); -webkit-backdrop-filter:blur(23px) saturate(140%);
}
[data-testid="stMetric"] { background:rgba(20,48,70,.68); border:1px solid rgba(119,204,234,.22); border-radius:15px; padding:15px; }
[data-testid="stMetricLabel"] { color:#9FC5D9 !important; }
[data-testid="stMetricValue"] { color:#F4FBFF !important; font-family:'Space Grotesk',sans-serif; }
div[data-testid="stForm"] { background:rgba(16,35,56,.78); border:1px solid rgba(130,203,232,.24); border-radius:18px; padding:18px; backdrop-filter:blur(20px); }
.task-row { background:rgba(24,51,73,.62); border:1px solid rgba(130,203,232,.20); border-radius:13px; padding:14px 17px; margin:8px 0; }
div.stButton > button { border-radius:10px; border:1px solid rgba(91,215,255,.32); font-weight:700; min-height:41px; transition:all .18s ease; }
div.stButton > button:hover { transform:translateY(-2px); border-color:#5CE4FF; box-shadow:0 0 18px rgba(0,198,255,.20); }
.stProgress > div > div > div > div { background:linear-gradient(90deg,#00CFFF,#6A9BFF,#9C7BFF); }
.stTextInput input,.stTextArea textarea,.stNumberInput input,.stDateInput input {
  background:rgba(8,22,38,.88); color:#ECF5FF; border:1px solid rgba(130,203,232,.26); border-radius:10px;
}
[data-baseweb="select"] > div { background:rgba(8,22,38,.90); border-color:rgba(130,203,232,.26); border-radius:10px; }
.stChatMessage { background:rgba(22,47,69,.72); border:1px solid rgba(130,203,232,.22); border-radius:16px; backdrop-filter:blur(18px); }
hr { border-color:rgba(130,203,232,.14); }

/* Futuristic startup loader + branded activity indicator */
.startup-loader {
  position:fixed; inset:0; z-index:999999; display:flex; align-items:center;
  justify-content:center; flex-direction:column; gap:17px;
  background:radial-gradient(circle at 50% 45%,rgba(0,197,255,.15),transparent 28%),
  radial-gradient(circle at 50% 55%,rgba(126,91,255,.13),transparent 38%),rgba(5,11,21,.97);
  backdrop-filter:blur(18px); animation:loaderFadeOut .8s ease 2.4s forwards;
  pointer-events:none;
}
.loader-core { position:relative; width:94px; height:94px; display:grid; place-items:center; }
.loader-ring,.loader-core:before,.loader-core:after {
  content:""; position:absolute; border-radius:50%; border:2px solid transparent;
}
.loader-ring { inset:0; border-top-color:#43E5FF; border-right-color:rgba(67,229,255,.35);
  box-shadow:0 0 20px rgba(0,205,255,.20); animation:loaderSpin 1.35s linear infinite; }
.loader-core:before { inset:11px; border-bottom-color:#A68BFF; border-left-color:rgba(166,139,255,.4);
  box-shadow:0 0 18px rgba(166,139,255,.18); animation:loaderSpinReverse 1.05s linear infinite; }
.loader-core:after { inset:25px; border:1px solid rgba(91,224,255,.55);
  background:radial-gradient(circle,rgba(76,221,255,.23),rgba(65,112,255,.06));
  box-shadow:0 0 28px rgba(50,206,255,.22),inset 0 0 15px rgba(50,206,255,.18);
  animation:loaderPulse 1.4s ease-in-out infinite; }
.loader-star { position:relative; z-index:2; color:#F1FCFF; font-size:22px;
  text-shadow:0 0 14px #54DFFF; animation:loaderPulse 1.4s ease-in-out infinite; }
.loader-title { font-family:'Space Grotesk',sans-serif; color:#F1FAFF; font-size:16px;
  font-weight:700; letter-spacing:3px; }
.loader-subtitle { color:#8EABC2; font-size:9px; font-weight:700; letter-spacing:2.2px; }
.loader-track { width:145px; height:2px; overflow:hidden; border-radius:5px; background:rgba(119,190,220,.16); }
.loader-track:after { content:""; display:block; height:100%; width:42%;
  background:linear-gradient(90deg,transparent,#45E5FF,#A68BFF,transparent);
  box-shadow:0 0 12px #45DFFF; animation:loaderProgress 1.15s ease-in-out infinite; }
[data-testid="stSpinner"] > div > div {
  border-top-color:#45E5FF !important; border-right-color:rgba(166,139,255,.65) !important;
}
@keyframes loaderSpin { to { transform:rotate(360deg); } }
@keyframes loaderSpinReverse { to { transform:rotate(-360deg); } }
@keyframes loaderPulse { 0%,100% { transform:scale(.94); opacity:.78; } 50% { transform:scale(1.06); opacity:1; } }
@keyframes loaderProgress { 0% { transform:translateX(-120%); } 100% { transform:translateX(360%); } }
@keyframes loaderFadeOut { to { opacity:0; visibility:hidden; } }
@media(prefers-reduced-motion:reduce) {
  .startup-loader,.loader-ring,.loader-core:before,.loader-core:after,.loader-star,.loader-track:after { animation:none !important; }
  .startup-loader { display:none; }
}

@keyframes riseIn { from { opacity:0; transform:translateY(10px); } to { opacity:1; transform:translateY(0); } }
@media(prefers-reduced-motion:reduce) { *,*:before,*:after { animation:none !important; transition:none !important; } }
"""

# Light theme styles, injected only when the in-app toggle is on.
LIGHT_CSS = """
.stApp {
  color:#18263A !important;
  background:
    radial-gradient(ellipse at 10% 4%,rgba(68,180,230,.15),transparent 32%),
    radial-gradient(ellipse at 92% 10%,rgba(151,126,238,.13),transparent 30%),
    linear-gradient(135deg,#F4F8FC,#EAF1F8 55%,#F7F9FD) !important;
  background-attachment:fixed !important;
}
[data-testid="stHeader"] {
  background:rgba(245,249,253,.78) !important;
  border-bottom:1px solid rgba(80,115,150,.10);
}
[data-testid="stSidebar"] {
  background:linear-gradient(165deg,rgba(239,247,252,.97),rgba(226,237,247,.98)) !important;
  border-right:1px solid rgba(89,133,165,.20) !important;
  box-shadow:10px 0 35px rgba(35,65,95,.08) !important;
}
[data-testid="stSidebar"] * { color:#20364D !important; }
h1,h2,h3,h4,p,label,[data-testid="stMarkdownContainer"] { color:#1B2D42; }
.muted { color:#62758A !important; }
.eyebrow { color:#167C9D !important; }
.glass-hero {
  background:linear-gradient(112deg,rgba(220,245,252,.94),rgba(226,232,255,.94) 55%,rgba(239,229,255,.94)) !important;
  border:1px solid rgba(90,151,184,.30) !important;
  box-shadow:0 16px 38px rgba(49,91,125,.12),inset 0 1px 0 rgba(255,255,255,.95) !important;
}
.hero-label { color:#167C9D !important; }
.hero-heading { color:#172E46 !important; }
.hero-caption { color:#526B80 !important; }
.hero-status {
  color:#147D69 !important; background:rgba(36,178,145,.10) !important;
  border-color:rgba(36,150,125,.28) !important;
}
.glass-hero:before { background:rgba(65,190,220,.13) !important; }
.glass-hero:after {
  border-color:rgba(73,151,185,.22) !important;
  box-shadow:0 0 0 18px rgba(73,151,185,.025),0 0 0 38px rgba(73,151,185,.018) !important;
}
.stat-card {
  background:linear-gradient(145deg,rgba(255,255,255,.91),rgba(232,242,250,.91)) !important;
  border:1px solid rgba(106,145,173,.24) !important;
  border-top-color:rgba(255,255,255,.98) !important;
  box-shadow:0 10px 28px rgba(42,75,105,.09),inset 0 1px 0 #fff !important;
}
.stat-card:hover {
  border-color:rgba(47,155,190,.50) !important;
  box-shadow:0 16px 34px rgba(42,116,150,.13) !important;
}
.stat-label { color:#627A8F !important; }
.stat-value { color:#1B344D !important; }
.stat-sub { color:#6D8193 !important; }
[data-testid="stVerticalBlockBorderWrapper"] > div {
  background:linear-gradient(145deg,rgba(255,255,255,.88),rgba(239,245,250,.92)) !important;
  border:1px solid rgba(112,147,173,.23) !important;
  box-shadow:0 10px 28px rgba(40,70,100,.08),inset 0 1px 0 #fff !important;
}
[data-testid="stMetric"] {
  background:rgba(255,255,255,.78) !important;
  border-color:rgba(112,147,173,.22) !important;
}
[data-testid="stMetricLabel"] { color:#63798D !important; }
[data-testid="stMetricValue"] { color:#1B344D !important; }
div[data-testid="stForm"] {
  background:rgba(255,255,255,.80) !important;
  border-color:rgba(112,147,173,.25) !important;
  box-shadow:0 8px 24px rgba(40,70,100,.06);
}
.task-row {
  background:rgba(255,255,255,.78) !important;
  border-color:rgba(112,147,173,.22) !important;
  color:#263D53 !important;
}
div.stButton > button {
  color:#25435D !important;
  background:rgba(255,255,255,.76) !important;
  border:1px solid rgba(98,143,174,.30) !important;
}
div.stButton > button:hover {
  color:#126D8B !important; border-color:#48A9C8 !important;
  box-shadow:0 6px 18px rgba(45,143,176,.14) !important;
}
div.stButton > button[kind="primary"] {
  color:#FFFFFF !important;
  background:linear-gradient(105deg,#247FA5,#586EC4) !important;
  border-color:transparent !important;
}
.stTextInput input,.stTextArea textarea,.stNumberInput input,.stDateInput input {
  color:#20364D !important; background:rgba(255,255,255,.92) !important;
  border:1px solid rgba(101,140,169,.32) !important;
}
[data-baseweb="select"] > div {
  color:#20364D !important; background:rgba(255,255,255,.94) !important;
  border-color:rgba(101,140,169,.32) !important;
}
[data-baseweb="select"] * { color:#20364D !important; }
.stChatMessage {
  background:rgba(255,255,255,.82) !important;
  border-color:rgba(112,147,173,.23) !important;
}
.startup-loader {
  background:radial-gradient(circle at 50% 45%,rgba(0,197,255,.12),transparent 28%),
  radial-gradient(circle at 50% 55%,rgba(126,91,255,.10),transparent 38%),rgba(238,246,252,.97) !important;
}
.loader-title { color:#18364F !important; }
.loader-subtitle { color:#5F7D93 !important; }
.loader-star { color:#2B6C8F !important; text-shadow:0 0 14px rgba(84,223,255,.6) !important; }
hr { border-color:rgba(83,120,150,.18) !important; }
"""

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Dark"

st.markdown(
    f"<style>{BASE_CSS}</style>"
    + (f"<style>{LIGHT_CSS}</style>" if st.session_state.theme_mode == "Light" else ""),
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="startup-loader">
      <div class="loader-core">
        <div class="loader-ring"></div>
        <div class="loader-star">✦</div>
      </div>
      <div class="loader-title">STUDYFLOW AI</div>
      <div class="loader-subtitle">INITIALIZING YOUR WORKSPACE</div>
      <div class="loader-track"></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- DATA ----------------
def load_data():
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            return data.get("tasks", [])
        except (OSError, json.JSONDecodeError):
            return []
    return []

def save_data():
    try:
        DATA_FILE.write_text(
            json.dumps({"tasks": st.session_state.tasks}, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )
    except OSError as error:
        st.error(f"Could not save tasks: {error}")

if "tasks" not in st.session_state:
    st.session_state.tasks = load_data()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
def get_api_key() -> str:
    return str(st.session_state.get("api_key", "")).strip()

def get_model() -> str:
    return str(st.session_state.get("model", DEFAULT_MODEL)).strip() or DEFAULT_MODEL

if "model" not in st.session_state:
    st.session_state.model = DEFAULT_MODEL

# ---------------- AI ----------------
def ask_ai(prompt: str) -> str:
    key = get_api_key()
    if not key:
        return "Add your Gemini API key in the sidebar under AI Settings to use the AI features."
    model = get_model()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 3500},
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        return f"Gemini API error ({error.code}):\n\n{details[:1500]}"
    except (urllib.error.URLError, TimeoutError, KeyError, IndexError, json.JSONDecodeError) as error:
        return f"Something went wrong while contacting Gemini: {error}"

def get_stats():
    tasks = st.session_state.tasks
    total = len(tasks)
    completed = sum(1 for task in tasks if task.get("done", False))
    pending = total - completed
    minutes = sum(int(task.get("minutes", 0)) for task in tasks if task.get("done", False))
    percentage = round(completed / total * 100) if total else 0
    return total, completed, pending, minutes, percentage

def page_header(title, subtitle):
    st.markdown(f"## {title}")
    st.markdown(f"<p class='muted'>{subtitle}</p>", unsafe_allow_html=True)

def stat_card(label, value, subtitle, color):
    st.markdown(
        f"""<div class="stat-card">
        <div class="stat-label">{label}</div>
        <div class="stat-value" style="color:{color}">{value}</div>
        <div class="stat-sub">{subtitle}</div></div>""",
        unsafe_allow_html=True,
    )

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("<div class='brand'>✦ StudyFlow</div>", unsafe_allow_html=True)
    st.caption("YOUR PERSONAL STUDY WORKSPACE")
    st.markdown("---")
    st.markdown("<div class='eyebrow'>WORKSPACE</div>", unsafe_allow_html=True)

    pages = ["Dashboard", "My Tasks", "AI Planner", "AI Tutor"]
    for page in pages:
        if st.button(
            ("▣  " if page == st.session_state.page else "›  ") + page,
            key=f"nav_{page}",
            use_container_width=True,
            type="primary" if page == st.session_state.page else "secondary",
        ):
            st.session_state.page = page
            st.rerun()

    st.markdown("---")
    st.markdown("<div class='eyebrow'>APPEARANCE</div>", unsafe_allow_html=True)

    def _on_theme_change():
        st.session_state.theme_mode = "Light" if st.session_state.theme_toggle else "Dark"
        st.rerun()

    st.toggle(
        "Light background",
        key="theme_toggle",
        value=st.session_state.theme_mode == "Light",
        on_change=_on_theme_change,
    )

    st.markdown("---")
    st.markdown("<div class='eyebrow'>AI SETTINGS</div>", unsafe_allow_html=True)
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    st.text_input(
        "Gemini API Key",
        type="password",
        key="api_key",
        placeholder="Paste your Gemini API key",
        help="Your key is used by this local app to connect to Gemini."
    )
    st.selectbox(
        "AI Model",
        ["gemini-2.5-flash", "gemini-2.5-pro"],
        key="model"
    )

    st.markdown("---")
    st.markdown("<div class='eyebrow'>YOUR ACCOUNT</div>", unsafe_allow_html=True)
    st.markdown("**Student**")
    st.caption("Personal workspace")
    st.markdown("<div class='eyebrow'>POWERED BY GEMINI</div>", unsafe_allow_html=True)

# ---------------- DASHBOARD ----------------
if st.session_state.page == "Dashboard":
    st.markdown(
        """<div class="glass-hero">
        <div class="hero-label">STUDYFLOW // PERSONAL LEARNING SYSTEM</div>
        <div class="hero-heading">Your focus. Your future.</div>
        <div class="hero-caption">Your study command centre is ready. Track progress, organise tasks, and keep moving forward.</div>
        <div class="hero-status">● SYSTEM ONLINE &nbsp; | &nbsp; READY TO LEARN</div>
        </div>""",
        unsafe_allow_html=True,
    )
    total, completed, pending, minutes, percentage = get_stats()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        stat_card("TOTAL TASKS", total, "All your study goals", BLUE)
    with c2:
        stat_card("COMPLETED", completed, "Tasks finished", GREEN)
    with c3:
        stat_card("PENDING", pending, "Still to complete", ORANGE)
    with c4:
        stat_card("STUDY TIME", f"{minutes // 60}h {minutes % 60}m", "Time from completed tasks", PURPLE)

    st.write("")
    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.markdown("### Study Progress")
            st.caption("Your overall completion rate")
            st.markdown(f"<div style='font-size:42px;font-weight:800;color:{GREEN}'>{percentage}%</div>", unsafe_allow_html=True)
            st.progress(percentage / 100 if percentage else 0)
            st.caption(f"{completed} of {total} tasks completed")
    with right:
        with st.container(border=True):
            st.markdown("### Upcoming Tasks")
            st.caption("Your next study goals")
            upcoming = [task for task in st.session_state.tasks if not task.get("done", False)][:5]
            if not upcoming:
                st.success("You're all caught up! Add a task to get started.")
            else:
                for task in upcoming:
                    st.markdown(f"**○ {task['name']}**")
                    st.caption(f"{task.get('subject', 'General')} · {task.get('minutes', 0)} min · {task.get('deadline', 'Not set')}")

    if st.button("+ Add a task", type="primary"):
        st.session_state.page = "My Tasks"
        st.rerun()

# ---------------- TASKS ----------------
elif st.session_state.page == "My Tasks":
    page_header("My Tasks", "Keep track of everything you need to study.")
    tasks = st.session_state.tasks
    st.caption(f"{len(tasks)} tasks in total")

    with st.expander("+ New Task", expanded=not tasks):
        with st.form("new_task_form", clear_on_submit=True):
            task_name = st.text_input("Task name")
            subject = st.text_input("Subject")
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=1440, value=30)
            priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=1)
            deadline = st.date_input("Deadline (optional)", value=None)
            submitted = st.form_submit_button("Create Task", type="primary", use_container_width=True)
            if submitted:
                if not task_name.strip() or not subject.strip():
                    st.warning("Enter a task name and subject.")
                else:
                    due = deadline.isoformat() if deadline else "Not set"
                    st.session_state.tasks.append({
                        "name": task_name.strip(),
                        "subject": subject.strip(),
                        "minutes": int(duration),
                        "priority": priority,
                        "deadline": due,
                        "done": False,
                        "created": date.today().isoformat(),
                    })
                    save_data()
                    st.success("Task created!")
                    st.rerun()

    if not tasks:
        st.info("No tasks yet. Create your first study task above.")
    else:
        for index, task in enumerate(tasks):
            with st.container(border=True):
                col1, col2, col3 = st.columns([6, 2, 2])
                with col1:
                    mark = "✅" if task.get("done") else "◯"
                    st.markdown(f"**{mark} {task['name']}**")
                    st.caption(
                        f"{task.get('subject', 'General')} · {task.get('minutes', 0)} min · "
                        f"{task.get('priority', 'Medium')} priority · Due: {task.get('deadline', 'Not set')}"
                    )
                with col2:
                    st.caption("Completed" if task.get("done") else "Pending")
                    if st.button("Toggle status", key=f"toggle_{index}", use_container_width=True):
                        st.session_state.tasks[index]["done"] = not task.get("done", False)
                        save_data()
                        st.rerun()
                with col3:
                    st.caption(" ")
                    if st.button("Delete", key=f"delete_{index}", use_container_width=True):
                        st.session_state.tasks.pop(index)
                        save_data()
                        st.rerun()

# ---------------- AI PLANNER ----------------
elif st.session_state.page == "AI Planner":
    page_header("AI Study Planner", "Build a study routine that actually works for you.")
    with st.container(border=True):
        st.markdown("### Plan your study")
        with st.form("planner_form"):
            grade = st.text_input("Grade", placeholder="e.g. 8")
            subjects = st.text_input("Subjects", placeholder="Maths, Science, English...")
            weak_topics = st.text_area("Weak topics", placeholder="Topics you need to improve")
            available_hours = st.number_input("Daily available hours", min_value=0.5, max_value=16.0, value=3.0, step=0.5)
            exam_date = st.date_input("Exam date", value=date.today())
            generate_plan = st.form_submit_button("✦ Generate My Study Plan", type="primary", use_container_width=True)

    if generate_plan:
        if not all([grade.strip(), subjects.strip(), weak_topics.strip()]):
            st.warning("Please fill in Grade, Subjects and Weak topics.")
        else:
            prompt = f"""
You are StudyFlow AI, an expert student study planner.
Create a practical personalised study plan.

STUDENT:
Grade: {grade}
Subjects: {subjects}
Weak topics: {weak_topics}
Daily available hours: {available_hours}
Exam date: {exam_date.isoformat()}

CURRENT TASKS:
{json.dumps(st.session_state.tasks, ensure_ascii=False)}

REQUIREMENTS:
1. Create a realistic daily timetable.
2. Give extra time to weak topics.
3. Include breaks.
4. Include active recall and practice questions.
5. Include revision sessions.
6. Make a weekly progress checklist.
7. Avoid unrealistic study hours.
8. Clearly mention what to study in each session.
9. Format using headings and easy-to-read tables.
10. Keep the plan student-friendly.
"""
            with st.spinner("✦ Gemini is creating your study plan..."):
                answer = ask_ai(prompt)
            st.markdown("### Your Personal Study Plan")
            st.markdown(answer)

# ---------------- AI TUTOR ----------------
elif st.session_state.page == "AI Tutor":
    page_header("AI Tutor", "Your personal AI learning assistant.")
    st.markdown(
        f"<div class='panel'><b>✦ StudyFlow AI</b><span style='float:right;color:{GREEN}'>Gemini powered</span><br><span class='muted'>Ask me to explain a topic, solve a practice question or organise your revision.</span></div>",
        unsafe_allow_html=True,
    )

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask StudyFlow AI a question...")
    if question:
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        history = "\n".join(
            f"{'YOU' if item['role'] == 'user' else 'STUDYFLOW AI'}: {item['content']}"
            for item in st.session_state.chat_history[-12:]
        )
        prompt = f"""
You are StudyFlow AI, a friendly school tutor.
Help students understand concepts, solve academic questions,
prepare for exams and improve study habits.
Explain difficult concepts step by step.
Use simple language and examples.
Do not just give answers; explain the reasoning.
Be accurate and encouraging.

Conversation:
{history}

Answer the latest question.
"""
        with st.chat_message("assistant"):
            with st.spinner("StudyFlow AI is thinking..."):
                answer = ask_ai(prompt)
            st.markdown(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

    st.caption("AI can make mistakes. Check important academic information.")
