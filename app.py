import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from gtts import gTTS
from io import BytesIO
import time

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG & GAMIFIED ACCESSIBLE DESIGN SYSTEM
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ROUTELESS // Kids, Students & Senior Transit Game",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

    /* Playful Animations & Glowing Buttons */
    @keyframes bounceGlow {
        0% { transform: translateY(0px); box-shadow: 0 0 0 0 rgba(79, 70, 229, 0.4); }
        50% { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(79, 70, 229, 0.2); }
        100% { transform: translateY(0px); box-shadow: 0 0 0 0 rgba(79, 70, 229, 0); }
    }

    .stApp {
        background: linear-gradient(135deg, #F0FDF4 0%, #EFF6FF 50%, #FAF5FF 100%);
        color: #0F172A;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}

    /* Highly Visible Side Panel / Sidebar */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 3.5px solid #0F172A;
        box-shadow: 6px 0px 25px rgba(15, 23, 42, 0.08);
    }
    [data-testid="stSidebar"] h3 {
        font-family: 'Fredoka', sans-serif !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        background: linear-gradient(135deg, #4F46E5 0%, #06B6D4 100%);
        padding: 12px 16px;
        border-radius: 12px;
        border: 2.5px solid #0F172A;
        box-shadow: 3px 3px 0px #0F172A;
        text-align: center;
        letter-spacing: 0.5px;
    }

    /* Chunky, Playful Command Banner */
    .command-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 26px 34px;
        background: linear-gradient(135deg, #6366F1 0%, #3B82F6 50%, #10B981 100%);
        border: 3.5px solid #0F172A;
        border-radius: 20px;
        margin-bottom: 24px;
        box-shadow: 6px 6px 0px #0F172A;
        animation: bounceGlow 4s ease-in-out infinite;
    }
    .command-title {
        font-family: 'Fredoka', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #FFFFFF !important;
        margin: 0;
        text-shadow: 2px 2px 0px rgba(15, 23, 42, 0.3);
    }
    .command-subtitle {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        color: #FEF08A !important;
        margin-top: 6px;
    }
    .status-badge {
        font-family: 'Fredoka', sans-serif;
        font-size: 1rem;
        padding: 12px 22px;
        border-radius: 999px;
        font-weight: 700;
        border: 3px solid #0F172A;
        box-shadow: 4px 4px 0px #0F172A;
        background: #FEF08A;
        color: #854D0E !important;
    }

    /* Oversized, Super-Clickable KPI Cards */
    .kpi-card {
        border: 3.5px solid #0F172A;
        border-radius: 18px;
        padding: 22px;
        box-shadow: 5px 5px 0px #0F172A;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        cursor: pointer;
    }
    .kpi-card:hover {
        transform: translateY(-4px) translateX(-2px);
        box-shadow: 9px 9px 0px #0F172A;
    }
    .kpi-emerald { background: linear-gradient(135deg, #ECFDF5 0%, #6EE7B7 100%); }
    .kpi-sky     { background: linear-gradient(135deg, #EFF6FF 0%, #93C5FD 100%); }
    .kpi-amber   { background: linear-gradient(135deg, #FEFCE8 0%, #FDE047 100%); }
    .kpi-indigo  { background: linear-gradient(135deg, #EEF2FF 0%, #A5B4FC 100%); }

    .kpi-label {
        font-family: 'Fredoka', sans-serif;
        font-size: 0.95rem;
        text-transform: uppercase;
        color: #1E293B !important;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-family: 'Fredoka', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #0F172A !important;
        line-height: 1.1;
    }
    .kpi-trend {
        font-size: 0.92rem;
        margin-top: 10px;
        font-weight: 800;
        color: #0F172A !important;
    }

    /* Chunky Clickable Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #F59E0B 0%, #EF4444 100%) !important;
        color: #FFFFFF !important;
        border: 3.5px solid #0F172A !important;
        border-radius: 14px !important;
        font-family: 'Fredoka', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        padding: 0.75rem 1.4rem !important;
        box-shadow: 4px 4px 0px #0F172A !important;
        transition: all 0.15s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) translateX(-2px);
        box-shadow: 7px 7px 0px #0F172A !important;
    }

    /* Big Clickable Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: #FFFFFF;
        padding: 12px;
        border-radius: 18px;
        border: 3.5px solid #0F172A;
        box-shadow: 5px 5px 0px #0F172A;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Fredoka', sans-serif;
        font-size: 1.05rem;
        color: #1E293B !important;
        border-radius: 12px;
        padding: 12px 20px;
        font-weight: 700;
        border: 2px solid transparent;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4F46E5 0%, #06B6D4 100%) !important;
        color: #FFFFFF !important;
        border: 2.5px solid #0F172A !important;
        box-shadow: 3px 3px 0px #0F172A;
    }

    /* Readable Headings & Form Inputs */
    h1, h2, h3, h4 {
        font-family: 'Fredoka', sans-serif !important;
        color: #0F172A !important;
        font-weight: 700 !important;
    }
    p, label, .stMarkdown {
        color: #0F172A !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 1.05rem;
        font-weight: 700;
    }
    [data-baseweb="select"] > div, [data-baseweb="input"] > div {
        background-color: #FFFFFF !important;
        border: 3px solid #0F172A !important;
        border-radius: 12px !important;
        color: #0F172A !important;
        font-weight: 700 !important;
    }
    [data-testid="stDataFrame"], [data-testid="stExpander"], [data-testid="stForm"] {
        background-color: #FFFFFF !important;
        border: 3.5px solid #0F172A !important;
        border-radius: 18px !important;
        box-shadow: 6px 6px 0px #0F172A !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. MULTILINGUAL VOICE & FRIENDLY STRINGS
# -----------------------------------------------------------------------------
LANG_CONFIG = {
    "English": {"code": "en"},
    "हिन्दी (Hindi)": {"code": "hi"},
    "ಕನ್ನಡ (Kannada)": {"code": "kn"},
}

UI_STRINGS = {
    "English": {
        "title": "🚌 ROUTELESS // Kids & Student Transit Game",
        "subtitle": "Help students catch buses, explore routes, and beat the weather challenge!",
        "guide_title": "🌟 Welcome! Click here for a Super-Easy 3-Step Guide",
        "guide_body": """
        * **1. Add & Send Students:** Click the **➕ Add & Send a Student** tab to put any student on a bus and send them straight to school!
        * **2. Try Fun Scenarios:** Use the **Big Colorful Buttons** on the left sidebar to test rainy days, heavy crowds, or broken buses.
        * **3. Listen & Ask AI:** Tap **🔊 Listen to Audio Guide** or chat with our friendly AI assistant in English, Hindi, or Kannada!
        """,
        "speak_btn": "🔊 Listen to Audio Guide (English)",
    },
    "हिन्दी (Hindi)": {
        "title": "🚌 रूटलेस // छात्र और बच्चों की बस यात्रा खेल",
        "subtitle": "छात्रों को समय पर स्कूल पहुंचाएं, बस मार्ग देखें और मजे करें!",
        "guide_title": "🌟 स्वागत है! आसान 3-चरण गाइड देखने के लिए यहाँ क्लिक करें",
        "guide_body": """
        * **1. छात्र जोड़ें और भेजें:** किसी भी छात्र को बस में बैठाकर सीधे स्कूल भेजने के लिए **➕ Add & Send a Student** टैब खोलें।
        * **2. मजेदार स्थितियां जांचें:** बाईं तरफ दिए गए चमकीले बटनों से बारिश या बस खराब होने की स्थिति का अभ्यास करें।
        * **3. सुनें और एआई से पूछें:** **🔊 ऑडियो गाइड सुनें** बटन दबाएं या अपनी भाषा में सवाल पूछें!
        """,
        "speak_btn": "🔊 ऑडियो गाइड सुनें (हिन्दी)",
    },
    "ಕನ್ನಡ (Kannada)": {
        "title": "🚌 ರೂಟ್‌ಲೆಸ್ // ವಿದ್ಯಾರ್ಥಿ ಮತ್ತು ಮಕ್ಕಳ ಬಸ್ ಆಟ",
        "subtitle": "ವಿದ್ಯಾರ್ಥಿಗಳನ್ನು ಸಮಯಕ್ಕೆ ಸರಿಯಾಗಿ ಶಾಲೆಗೆ ತಲುಪಿಸಿ, ಬಸ್ ಮಾರ್ಗಗಳನ್ನು ನೋಡಿ!",
        "guide_title": "🌟 ಸ್ವಾಗತ! ಸರಳ 3-ಹಂತಗಳ ಮಾರ್ಗದರ್ಶಿಗಾಗಿ ಇಲ್ಲಿ ಕ್ಲಿಕ್ ಮಾಡಿ",
        "guide_body": """
        * **1. ವಿದ್ಯಾರ್ಥಿಯನ್ನು ಕಳುಹಿಸಿ:** ವಿದ್ಯಾರ್ಥಿಯನ್ನು ಬಸ್‌ಗೆ ಹತ್ತಿಸಿ ನೇರವಾಗಿ ಶಾಲೆಗೆ ಕಳುಹಿಸಲು **➕ Add & Send a Student** ಟ್ಯಾಬ್ ತೆರೆಯಿರಿ.
        * **2. ಮೋಜಿನ ಪರಿಸ್ಥಿತಿಗಳನ್ನು ಪರೀಕ್ಷಿಸಿ:** ಎಡಭಾಗದಲ್ಲಿರುವ ಬಣ್ಣಬಣ್ಣದ ಬಟನ್‌ಗಳನ್ನು ಬಳಸಿ ಮಳೆ ಅಥವಾ ಬಸ್ ಕೆಟ್ಟುಹೋಗುವ ಸವಾಲುಗಳನ್ನು ನೋಡಿ.
        * **3. ಧ್ವನಿ ಕೇಳಿ ಮತ್ತು ಪ್ರಶ್ನಿಸಿ:** **🔊 ಆಡಿಯೋ ಮಾರ್ಗದರ್ಶಿ ಕೇಳಿ** ಬಟನ್ ಒತ್ತಿ ಕನ್ನಡದಲ್ಲಿ ಮಾಹಿತಿ ಪಡೆಯಿರಿ!
        """,
        "speak_btn": "🔊 ಆಡಿಯೋ ಮಾರ್ಗದರ್ಶಿ ಕೇಳಿ (ಕನ್ನಡ)",
    }
}

@st.cache_data(show_spinner=False)
def text_to_audio_bytes(text: str, lang_code: str):
    try:
        tts = gTTS(text=text, lang=lang_code, slow=False)
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except Exception:
        return None

# -----------------------------------------------------------------------------
# 3. NODES & BASE DATA
# -----------------------------------------------------------------------------
NODES = {
    "Kanakapura Edu Hub (Exam Center)": {"lat": 12.5460, "lon": 77.4190, "type": "HUB"},
    "Harohalli Sector": {"lat": 12.6780, "lon": 77.4410, "type": "VILLAGE"},
    "Maralawadi Cluster": {"lat": 12.6150, "lon": 77.5120, "type": "VILLAGE"},
    "Sathanur South": {"lat": 12.4480, "lon": 77.3850, "type": "VILLAGE"},
    "Kodihalli Creek": {"lat": 12.5120, "lon": 77.4890, "type": "VILLAGE"},
    "Uyyamballi Outpost": {"lat": 12.4850, "lon": 77.3320, "type": "VILLAGE"},
}

@st.cache_data
def generate_base_manifest():
    np.random.seed(42)
    villages = [k for k, v in NODES.items() if v["type"] == "VILLAGE"]
    n_students = 240
    first_names = ["Aarav", "Ananya", "Rohan", "Kavya", "Vikram", "Sneha", "Karthik", "Pooja", "Darshan", "Divya"]
    records = []
    for i in range(1, n_students + 1):
        v = np.random.choice(villages, p=[0.25, 0.22, 0.20, 0.18, 0.15])
        is_exam = np.random.choice([True, False], p=[0.45, 0.55])
        exam_mins = np.random.choice([45, 75, 110, 180]) if is_exam else 360
        dist_km = {"Harohalli Sector": 16.4, "Maralawadi Cluster": 14.8, "Sathanur South": 12.2, "Kodihalli Creek": 9.5, "Uyyamballi Outpost": 15.1}[v]
        journey_stage = np.random.choice(["Arrived at School", "Riding on Bus", "Waiting at Bus Stop"], p=[0.35, 0.45, 0.20])
        records.append({
            "Student_ID": f"RTL-{2026000 + i}",
            "Student_Name": f"{np.random.choice(first_names)} #{i}",
            "Origin_Village": v,
            "Exam_Candidate": is_exam,
            "Minutes_To_Gate_Close": exam_mins,
            "Distance_KM": dist_km,
            "Journey_Status": journey_stage,
            "Manual_Bus_Override": None
        })
    return pd.DataFrame(records)

# -----------------------------------------------------------------------------
# 4. SESSION STATE
# -----------------------------------------------------------------------------
if "broken_buses" not in st.session_state:
    st.session_state.broken_buses = 2
if "demand_surge" not in st.session_state:
    st.session_state.demand_surge = 40
if "flood_idx" not in st.session_state:
    st.session_state.flood_idx = 1
if "micro_feeders" not in st.session_state:
    st.session_state.micro_feeders = True
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "custom_students" not in st.session_state:
    st.session_state.custom_students = []

# -----------------------------------------------------------------------------
# 5. SIDEBAR: SUPER VISIBLE BUTTONS & CONTROLS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🌐 Select Language")
    selected_lang = st.selectbox(
        "Choose Language / भाषा / ಭಾಷೆ",
        list(LANG_CONFIG.keys()),
        index=0
    )
    lang_code = LANG_CONFIG[selected_lang]["code"]
    strings = UI_STRINGS[selected_lang]

    st.markdown("### 🎮 Fun Quick Scenarios")
    st.caption("Click a button to test challenges:")
    
    if st.button("🚨 Exam Rush & Rain Challenge", use_container_width=True):
        st.session_state.broken_buses = 2
        st.session_state.demand_surge = 40
        st.session_state.flood_idx = 1
        st.session_state.micro_feeders = True
    
    if st.button("☀️ Perfect Sunny Day", use_container_width=True):
        st.session_state.broken_buses = 0
        st.session_state.demand_surge = 0
        st.session_state.flood_idx = 0
        st.session_state.micro_feeders = False

    if st.button("🌊 Super Flood & Heavy Trouble", use_container_width=True):
        st.session_state.broken_buses = 4
        st.session_state.demand_surge = 60
        st.session_state.flood_idx = 2
        st.session_state.micro_feeders = True

    st.markdown("---")
    st.markdown("### 🎛️ Easy Sliders")
    broken_buses = st.slider("Broken Buses", 0, 4, key="broken_buses")
    demand_surge_pct = st.slider("Extra Crowd (%)", 0, 80, step=5, key="demand_surge")
    flood_options = [
        "None (All Roads Open)",
        "Maralawadi Bridge Flooded",
        "Harohalli Landslide"
    ]
    flood_corridor = st.selectbox(
        "Road Weather Status",
        flood_options,
        index=st.session_state.flood_idx
    )
    deploy_micro_feeders = st.toggle("Send Extra Auto-Rickshaws", key="micro_feeders")

# -----------------------------------------------------------------------------
# 6. SOLVER & DATA PROCESSING
# -----------------------------------------------------------------------------
total_fleet = 8
bus_capacity = 48
base_df = generate_base_manifest()

if demand_surge_pct > 0:
    n_extra = int(len(base_df) * (demand_surge_pct / 100.0))
    surge_sample = base_df.sample(n=n_extra, replace=True, random_state=99).copy()
    surge_sample["Student_ID"] = [f"RTL-SRG-{i:03d}" for i in range(1, n_extra + 1)]
    surge_sample["Student_Name"] = [f"Friend #{i}" for i in range(1, n_extra + 1)]
    surge_sample["Exam_Candidate"] = np.random.choice([True, False], size=n_extra, p=[0.65, 0.35])
    surge_sample["Minutes_To_Gate_Close"] = np.where(surge_sample["Exam_Candidate"], np.random.choice([50, 85, 115], size=n_extra), 360)
    df = pd.concat([base_df, surge_sample], ignore_index=True)
else:
    df = base_df.copy()

if st.session_state.custom_students:
    custom_df = pd.DataFrame(st.session_state.custom_students)
    df = pd.concat([custom_df, df], ignore_index=True)

affected_village = "Maralawadi Cluster" if "Maralawadi" in flood_corridor else ("Harohalli Sector" if "Harohalli" in flood_corridor else None)
df["Corridor_Status"] = np.where(df["Origin_Village"] == affected_village, "SAFE DETOUR (+18m)", "ALL CLEAR")

urgency_score = np.where(df["Exam_Candidate"], np.clip(100 - (df["Minutes_To_Gate_Close"] * 0.45), 45, 95), 15)
df["Criticality_Index"] = np.round(np.clip(urgency_score + np.where(df["Origin_Village"] == affected_village, 12, 0) + (df["Distance_KM"]/20)*10, 0, 100), 1)
df.loc[df["Manual_Bus_Override"].notna(), "Criticality_Index"] = 100.0

df = df.sort_values(by=["Criticality_Index", "Minutes_To_Gate_Close"], ascending=[False, True]).reset_index(drop=True)

active_buses = max(1, total_fleet - broken_buses)
primary_seat_pool = active_buses * bus_capacity
feeder_units = 14 if deploy_micro_feeders else 0
feeder_seat_pool = feeder_units * 6

def assign_transport(idx, row):
    if pd.notna(row["Manual_Bus_Override"]):
        return row["Manual_Bus_Override"]
    if idx < primary_seat_pool:
        return f"BUS-0{(idx // bus_capacity) + 1}"
    elif idx < (primary_seat_pool + feeder_seat_pool):
        return f"AUTO-0{(idx - primary_seat_pool) // 6 + 1}"
    else:
        return "NEXT BUS (WAVE 2)"

df["Assigned_Unit"] = [assign_transport(i, r) for i, r in df.iterrows()]

total_students = len(df)
exam_students = df[df["Exam_Candidate"]]
total_exam_students = len(exam_students)
rescued_exam_students = len(exam_students[~exam_students["Assigned_Unit"].str.contains("WAVE 2")])
exam_rescue_rate = (rescued_exam_students / total_exam_students * 100) if total_exam_students > 0 else 100.0
total_seated = len(df[~df["Assigned_Unit"].str.contains("WAVE 2")])
unseated_count = total_students - total_seated

# -----------------------------------------------------------------------------
# 7. HEADER & AUDIO GUIDE
# -----------------------------------------------------------------------------
is_crisis = (broken_buses > 0) or (demand_surge_pct >= 25) or (affected_village is not None)
st.markdown(f"""
<div class="command-header">
    <div>
        <div class="command-title">{strings['title']}</div>
        <div class="command-subtitle">{strings['subtitle']}</div>
    </div>
    <div class="status-badge">{'⚡ Challenge Active!' : '🌟 All Safe & Happy!'}</div>
</div>
""", unsafe_allow_html=True)

col_guide, col_voice = st.columns([1.8, 1.2])
with col_guide:
    with st.expander(strings["guide_title"], expanded=True):
        st.markdown(strings["guide_body"])

with col_voice:
    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
    if st.button(strings["speak_btn"], use_container_width=True):
        if lang_code == "hi":
            briefing = f"नमस्ते! कुल {total_students} छात्रों में से {rescued_exam_students} छात्रों को बस में सीट मिल गई है। {active_buses} बसें बच्चों को स्कूल ले जा रही हैं।"
        elif lang_code == "kn":
            briefing = f"ನಮಸ್ಕಾರ! ಒಟ್ಟು {total_students} ವಿದ್ಯಾರ್ಥಿಗಳಲ್ಲಿ {rescued_exam_students} ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ ಬಸ್ ಸೀಟ್ ಸಿಕ್ಕಿದೆ. {active_buses} ಬಸ್‌ಗಳು ಮಕ್ಕಳನ್ನು ಶಾಲೆಗೆ ಕರೆದೊಯ್ಯುತ್ತಿವೆ."
        else:
            briefing = f"Hello! Out of {total_students} total students, {rescued_exam_students} exam students have secured bus seats. {active_buses} buses and auto-rickshaws are actively transporting everyone safely to school!"
        audio_data = text_to_audio_bytes(briefing, lang_code)
        if audio_data:
            st.audio(audio_data, format="audio/mp3", autoplay=True)
        else:
            st.info(briefing)

# -----------------------------------------------------------------------------
# 8. BIG CLICKABLE KPI CARDS
# -----------------------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'''
    <div class="kpi-card kpi-emerald">
        <div class="kpi-label">🌟 Happy Students</div>
        <div class="kpi-value">{exam_rescue_rate:.0f}%</div>
        <div class="kpi-trend">✅ {rescued_exam_students} Got School Seats</div>
    </div>
    ''', unsafe_allow_html=True)
with c2:
    st.markdown(f'''
    <div class="kpi-card kpi-sky">
        <div class="kpi-label">🚌 Active Buses</div>
        <div class="kpi-value">{active_buses + feeder_units}</div>
        <div class="kpi-trend">⚡ Running on Roads Now</div>
    </div>
    ''', unsafe_allow_html=True)
with c3:
    st.markdown(f'''
    <div class="kpi-card kpi-amber">
        <div class="kpi-label">⚠️ Extra Crowd</div>
        <div class="kpi-value">+{demand_surge_pct}%</div>
        <div class="kpi-trend">👥 More Friends Joined Today</div>
    </div>
    ''', unsafe_allow_html=True)
with c4:
    st.markdown(f'''
    <div class="kpi-card kpi-indigo">
        <div class="kpi-label">🛡️ Safe & Sound</div>
        <div class="kpi-value">{total_seated}</div>
        <div class="kpi-trend">🎉 Ready for Class!</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 9. BIG COLORFUL TABS
# -----------------------------------------------------------------------------
tab_add, tab_people, tab_ai, tab_sim, tab_manifest = st.tabs([
    "➕ Add & Send a Student",
    "📊 Live People & Crowd Watch",
    "🤖 Friendly AI Voice Helper",
    "🎮 Interactive Bus Game Map",
    "📋 All Students List"
])

with tab_add:
    st.markdown("#### 🚌 Board a Student onto a Bus & Send Them to School!")
    st.markdown("Type any student's name, pick their bus, and click the big button to send them off on their journey!")

    form_col, feed_col = st.columns([1.3, 1.2])

    with form_col:
        with st.form("dispatch_student_form", clear_on_submit=True):
            s_name = st.text_input("Student's Friendly Name", placeholder="e.g., Rahul / Sneha")
            c_sub1, c_sub2 = st.columns(2)
            with c_sub1:
                s_village = st.selectbox("Village Stop", [k for k, v in NODES.items() if v["type"] == "VILLAGE"])
            with c_sub2:
                available_bus_list = [f"BUS-0{i}" for i in range(1, active_buses + 1)] + [f"AUTO-0{i}" for i in range(1, 6)]
                s_bus = st.selectbox("Pick Bus or Auto", available_bus_list)

            c_sub3, c_sub4 = st.columns(2)
            with c_sub3:
                s_exam = st.checkbox("Important Test Today?", value=True)
            with c_sub4:
                s_mins = st.number_input("Minutes Until Test", min_value=15, max_value=240, value=60, step=15)

            submitted = st.form_submit_button("🚀 Send Student to School!", use_container_width=True)

            if submitted:
                clean_name = s_name.strip() if s_name.strip() else f"Student #{len(st.session_state.custom_students) + 1}"
                new_id = f"VIP-{101 + len(st.session_state.custom_students)}"
                dist_map = {"Harohalli Sector": 16.4, "Maralawadi Cluster": 14.8, "Sathanur South": 12.2, "Kodihalli Creek": 9.5, "Uyyamballi Outpost": 15.1}
                
                new_record = {
                    "Student_ID": new_id,
                    "Student_Name": clean_name,
                    "Origin_Village": s_village,
                    "Exam_Candidate": s_exam,
                    "Minutes_To_Gate_Close": int(s_mins),
                    "Distance_KM": dist_map.get(s_village, 12.0),
                    "Journey_Status": "Traveling to School",
                    "Manual_Bus_Override": s_bus
                }
                st.session_state.custom_students.insert(0, new_record)
                st.success(f"🎉 Hooray! **{clean_name}** boarded **{s_bus}** from **{s_village}** and is on their way to school!")
                
                confirm_voice = f"Hooray! Student {clean_name} is successfully on board {s_bus} heading to school."
                audio_confirm = text_to_audio_bytes(confirm_voice, lang_code)
                if audio_confirm:
                    st.audio(audio_confirm, format="audio/mp3", autoplay=True)

    with feed_col:
        st.markdown("#### 🎫 Recently Dispatched Tickets")
        if st.session_state.custom_students:
            for stu in st.session_state.custom_students[:4]:
                st.markdown(f"""
                <div class="protocol-box" style="border-left-color: #10B981; background: #ECFDF5;">
                    <div class="protocol-title">🎫 Ticket for {stu['Student_Name']}</div>
                    <div class="protocol-desc">
                        • <b>Bus Assigned:</b> {stu['Manual_Bus_Override']}<br>
                        • <b>Route:</b> {stu['Origin_Village']} ➔ School Hub<br>
                        • <b>Status:</b> 🌟 {stu['Journey_Status']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="protocol-box" style="border-left-color: #3B82F6; background: #EFF6FF;">
                <div class="protocol-title">Ready for Your First Dispatch!</div>
                <div class="protocol-desc">Use the form on the left to send students to school and collect their special boarding tickets!</div>
            </div>
            """, unsafe_allow_html=True)

with tab_people:
    st.markdown("#### 📊 Real-Time People & Crowd Watch")
    arrived_cnt = int((df["Journey_Status"] == "Arrived at School").sum())
    transit_cnt = int((df["Journey_Status"].isin(["Riding on Bus", "Traveling to School"])).sum())
    waiting_cnt = int((df["Journey_Status"] == "Waiting at Bus Stop").sum())

    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown(f'<div class="kpi-card kpi-emerald"><div class="kpi-label">🏫 Safely at School</div><div class="kpi-value">{arrived_cnt}</div><div class="kpi-trend">Ready to learn</div></div>', unsafe_allow_html=True)
    with p2:
        st.markdown(f'<div class="kpi-card kpi-sky"><div class="kpi-label">🚌 On the Bus</div><div class="kpi-value">{transit_cnt}</div><div class="kpi-trend">Rriding happily</div></div>', unsafe_allow_html=True)
    with p3:
        st.markdown(f'<div class="kpi-card kpi-amber"><div class="kpi-label">🚏 Waiting at Stop</div><div class="kpi-value">{waiting_cnt}</div><div class="kpi-trend">Bus arriving soon</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    g1, g2 = st.columns(2)
    with g1:
        village_summary = df.groupby(["Origin_Village", "Exam_Candidate"]).size().reset_index(name="People")
        village_summary["Category"] = np.where(village_summary["Exam_Candidate"], "Test Students (Priority)", "Regular Students")
        fig1 = px.bar(
            village_summary, x="Origin_Village", y="People", color="Category",
            title="Students Waiting in Each Village",
            color_discrete_map={"Test Students (Priority)": "#6366F1", "Regular Students": "#06B6D4"},
            barmode="group"
        )
        fig1.update_traces(marker_line_color="#0F172A", marker_line_width=2)
        fig1.update_layout(
            paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAFC",
            font=dict(color="#0F172A", family="Plus Jakarta Sans"),
            margin=dict(l=20, r=20, t=45, b=20),
            xaxis=dict(linecolor="#0F172A", linewidth=2, mirror=True, title=""),
            yaxis=dict(linecolor="#0F172A", linewidth=2, mirror=True, gridcolor="#CBD5E1", title="Number of Students")
        )
        st.plotly_chart(fig1, use_container_width=True)

    with g2:
        mode_counts = df["Assigned_Unit"].apply(
            lambda x: "Gov Bus" if "BUS" in x else ("Auto Rickshaw" if "AUTO" in x else "Wave 2")
        ).value_counts()
        fig2 = px.pie(
            names=mode_counts.index, values=mode_counts.values, hole=0.52,
            title="How Students are Traveling",
            color_discrete_sequence=["#10B981", "#3B82F6", "#F59E0B"]
        )
        fig2.update_traces(marker=dict(line=dict(color="#0F172A", width=2.5)), textinfo="percent+label")
        fig2.update_layout(
            paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
            font=dict(color="#0F172A", family="Plus Jakarta Sans"),
            margin=dict(l=20, r=20, t=45, b=20)
        )
        st.plotly_chart(fig2, use_container_width=True)

with tab_ai:
    st.markdown("#### 🤖 Friendly AI Voice Helper")
    st.markdown("Ask anything! Click a quick question or type below:")

    q1, q2, q3 = st.columns(3)
    quick_prompt = None
    with q1:
        if st.button("🎓 Are all test students seated?", use_container_width=True):
            quick_prompt = "Are all test students seated?"
    with q2:
        if st.button("🌊 Are roads safe today?", use_container_width=True):
            quick_prompt = "Are roads safe today?"
    with q3:
        if st.button("🔍 Check Friend #1", use_container_width=True):
            quick_prompt = "Check Friend #1"

    user_query = st.chat_input("Type your question here...")
    active_query = quick_prompt or user_query

    def generate_ai_response(query: str, language: str):
        q_lower = query.lower()
        matched_student = None
        for _, row in df.iterrows():
            if row["Student_ID"].lower() in q_lower or row["Student_Name"].lower() in q_lower:
                matched_student = row
                break

        if matched_student is not None:
            sid = matched_student["Student_ID"]
            sname = matched_student["Student_Name"]
            village = matched_student["Origin_Village"]
            unit = matched_student["Assigned_Unit"]
            return f"**{sname} ({sid})** from **{village}** is riding safely on **{unit}**! 🎉"

        if any(w in q_lower for w in ["flood", "road", "safe", "weather"]):
            if affected_village:
                return f"⚠️ **Weather Alert:** The direct road from **{affected_village}** has water, so our friendly buses are taking the safe **Bypass Route**!"
            else:
                return "☀️ **Great News:** All roads are completely clear and safe for travel today!"

        return (
            f"🌟 **Status Update:** **{rescued_exam_students} out of {total_exam_students}** test students (**{exam_rescue_rate:.0f}%**) have secured comfortable seats. "
            f"We have **{active_buses} buses** and auto-rickshaws running smoothly!"
        )

    if active_query:
        st.session_state.chat_history.append({"role": "user", "content": active_query})
        reply = generate_ai_response(active_query, lang_code)
        audio_reply = text_to_audio_bytes(reply.replace("**", "").replace("🌟", "").replace("🎉", ""), lang_code)
        st.session_state.chat_history.append({"role": "assistant", "content": reply, "audio": audio_reply})

    for msg in st.session_state.chat_history[-6:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("audio"):
                st.audio(msg["audio"], format="audio/mp3")

with tab_sim:
    st.markdown("#### 🎮 Interactive Bus Game Map")
    sim_col1, sim_col2 = st.columns([1, 2.4])
    with sim_col1:
        sim_step = st.slider("Trip Progress (Minutes)", 0, 60, 30, step=5)
        run_anim = st.button("▶️ Play Bus Journey Animation", use_container_width=True)
        st.markdown(f"""
        <div class="protocol-box" style="border-left-color: #3B82F6; background: #EFF6FF;">
            <div class="protocol-title">⏱️ Minute {sim_step} Update</div>
            <div class="protocol-desc">
            • <b>Buses Rolling:</b> {active_buses} Units<br>
            • <b>Auto Shuttles:</b> {feeder_units} Active<br>
            • <b>Route Status:</b> {'Safe Detour Active' if affected_village else 'Direct Path'}<br>
            • <b>Trip Progress:</b> {min(100, int((sim_step / 55) * 100))}%
            </div>
        </div>
        """, unsafe_allow_html=True)

    with sim_col2:
        sim_placeholder = st.empty()

        def render_sim_frame(minute_mark):
            progress = min(1.0, minute_mark / 55.0)
            hub = NODES["Kanakapura Edu Hub (Exam Center)"]
            fig_sim = go.Figure()

            for v_name, coords in NODES.items():
                if coords["type"] == "HUB":
                    continue
                is_flooded = (v_name == affected_village)
                if is_flooded:
                    fig_sim.add_trace(go.Scatter(
                        x=[coords["lon"], hub["lon"]], y=[coords["lat"], hub["lat"]],
                        mode="lines", line=dict(color="#EF4444", width=3, dash="dash"),
                        name="Closed Road"
                    ))
                    wp = NODES["Kodihalli Creek"]
                    fig_sim.add_trace(go.Scatter(
                        x=[coords["lon"], wp["lon"], hub["lon"]],
                        y=[coords["lat"], wp["lat"], hub["lat"]],
                        mode="lines", line=dict(color="#F59E0B", width=4.5),
                        name="Safe Detour"
                    ))
                    if progress < 0.5:
                        p2 = progress * 2
                        vx = coords["lon"] + (wp["lon"] - coords["lon"]) * p2
                        vy = coords["lat"] + (wp["lat"] - coords["lat"]) * p2
                    else:
                        p2 = (progress - 0.5) * 2
                        vx = wp["lon"] + (hub["lon"] - wp["lon"]) * p2
                        vy = wp["lat"] + (hub["lat"] - wp["lat"]) * p2
                else:
                    fig_sim.add_trace(go.Scatter(
                        x=[coords["lon"], hub["lon"]], y=[coords["lat"], hub["lat"]],
                        mode="lines", line=dict(color="#4F46E5", width=3.5),
                        name="Bus Route"
                    ))
                    vx = coords["lon"] + (hub["lon"] - coords["lon"]) * progress
                    vy = coords["lat"] + (hub["lat"] - coords["lat"]) * progress

                fig_sim.add_trace(go.Scatter(
                    x=[vx], y=[vy], mode="markers+text",
                    text=["🚌"], textfont=dict(size=22),
                    marker=dict(size=16, color="#10B981", line=dict(width=2.5, color="#0F172A")),
                    showlegend=False
                ))

            node_df = pd.DataFrame([{"Name": k, "Lon": v["lon"], "Lat": v["lat"]} for k, v in NODES.items()])
            fig_sim.add_trace(go.Scatter(
                x=node_df["Lon"], y=node_df["Lat"], mode="markers+text",
                text=node_df["Name"], textposition="top center",
                textfont=dict(family="Fredoka", size=13, color="#0F172A"),
                marker=dict(size=18, color="#0F172A", line=dict(width=2, color="#FFFFFF")),
                name="Villages & School"
            ))

            fig_sim.update_layout(
                title=f"Bus Simulation at Minute {minute_mark}",
                paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAFC",
                font=dict(color="#0F172A", family="Plus Jakarta Sans"),
                height=420, margin=dict(l=15, r=15, t=40, b=15),
                showlegend=False,
                xaxis=dict(showgrid=True, gridcolor="#CBD5E1", linecolor="#0F172A", linewidth=2.5, mirror=True),
                yaxis=dict(showgrid=True, gridcolor="#CBD5E1", linecolor="#0F172A", linewidth=2.5, mirror=True)
            )
            sim_placeholder.plotly_chart(fig_sim, use_container_width=True)

        if run_anim:
            for step in range(0, 60, 10):
                render_sim_frame(step)
                time.sleep(0.35)
        else:
            render_sim_frame(sim_step)

with tab_manifest:
    f1, f2, f3 = st.columns([1.5, 1.5, 2])
    with f1: filter_exam = st.selectbox("Show Students", ["All Students", "Test Candidates", "Regular Students"])
    with f2: filter_village = st.selectbox("Village", ["All Villages"] + list(df["Origin_Village"].unique()))
    with f3: search_id = st.text_input("Search Name", placeholder="e.g., Rohan")

    filtered_df = df.copy()
    if filter_exam == "Test Candidates": filtered_df = filtered_df[filtered_df["Exam_Candidate"]]
    elif filter_exam == "Regular Students": filtered_df = filtered_df[~filtered_df["Exam_Candidate"]]
    if filter_village != "All Villages": filtered_df = filtered_df[filtered_df["Origin_Village"] == filter_village]
    if search_id:
        filtered_df = filtered_df[
            filtered_df["Student_ID"].str.contains(search_id, case=False) |
            filtered_df["Student_Name"].str.contains(search_id, case=False)
        ]

    st.dataframe(
        filtered_df[["Student_ID", "Student_Name", "Origin_Village", "Exam_Candidate", "Journey_Status", "Criticality_Index", "Assigned_Unit"]],
        use_container_width=True, height=430,
        column_config={
            "Criticality_Index": st.column_config.ProgressColumn("Priority", format="%.1f", min_value=0, max_value=100),
            "Exam_Candidate": st.column_config.CheckboxColumn("Test Today")
        }
    )
