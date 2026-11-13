import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from gtts import gTTS
from io import BytesIO
import time

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG & ANIMATED HIGH-VISIBILITY DESIGN SYSTEM
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ROUTELESS // Dynamic Transit Command",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@600;700;800;900&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

    /* Global Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulseGlow {
        0% { box-shadow: 0 0 0 0 rgba(79, 70, 229, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(79, 70, 229, 0); }
        100% { box-shadow: 0 0 0 0 rgba(79, 70, 229, 0); }
    }

    @keyframes floatBadge {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-3px); }
        100% { transform: translateY(0px); }
    }

    .stApp {
        background: linear-gradient(135deg, #EEF2FF 0%, #F8FAFC 50%, #F1F5F9 100%);
        color: #0F172A;
        font-family: 'Plus Jakarta Sans', sans-serif;
        animation: fadeIn 0.5s ease-out;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 3px solid #0F172A;
        box-shadow: 4px 0px 20px rgba(15, 23, 42, 0.05);
    }
    [data-testid="stSidebar"] h3 {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        color: #312E81 !important;
        background: #EEF2FF;
        padding: 10px 14px;
        border-radius: 10px;
        border: 2px solid #0F172A;
        box-shadow: 3px 3px 0px #0F172A;
    }

    /* Vibrant Top Command Banner with Float Effect */
    .command-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 24px 32px;
        background: linear-gradient(135deg, #4338CA 0%, #0284C7 50%, #0D9488 100%);
        border: 3px solid #0F172A;
        border-radius: 18px;
        margin-bottom: 24px;
        box-shadow: 6px 6px 0px #0F172A;
        animation: floatBadge 4s ease-in-out infinite;
    }
    .command-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.85rem;
        font-weight: 900;
        color: #FFFFFF !important;
        margin: 0;
        letter-spacing: 0.5px;
        text-shadow: 2px 2px 0px rgba(15, 23, 42, 0.3);
    }
    .command-subtitle {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1rem;
        font-weight: 700;
        color: #E0F2FE !important;
        margin-top: 6px;
    }
    .status-badge {
        font-family: 'Outfit', sans-serif;
        font-size: 0.92rem;
        padding: 10px 20px;
        border-radius: 999px;
        font-weight: 800;
        border: 3px solid #0F172A;
        box-shadow: 4px 4px 0px #0F172A;
        animation: pulseGlow 2s infinite;
    }
    .status-crisis { background: #FEE2E2; color: #DC2626 !important; }
    .status-normal { background: #ECFDF5; color: #059669 !important; }

    /* Animated KPI Cards */
    .kpi-card {
        border: 3px solid #0F172A;
        border-radius: 16px;
        padding: 20px 22px;
        box-shadow: 5px 5px 0px #0F172A;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        animation: fadeIn 0.6s ease-out;
    }
    .kpi-card:hover {
        transform: translateY(-4px) translateX(-2px);
        box-shadow: 8px 8px 0px #0F172A;
    }
    .kpi-emerald { background: linear-gradient(135deg, #ECFDF5 0%, #A7F3D0 100%); }
    .kpi-sky     { background: linear-gradient(135deg, #F0F9FF 0%, #BAE6FD 100%); }
    .kpi-amber   { background: linear-gradient(135deg, #FFFBEB 0%, #FDE68A 100%); }
    .kpi-indigo  { background: linear-gradient(135deg, #EEF2FF 0%, #C7D2FE 100%); }

    .kpi-label {
        font-family: 'Outfit', sans-serif;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #1E293B !important;
        font-weight: 800;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-family: 'Outfit', sans-serif;
        font-size: 2.3rem;
        font-weight: 900;
        color: #0F172A !important;
        line-height: 1.1;
    }
    .kpi-trend {
        font-size: 0.88rem;
        margin-top: 10px;
        font-weight: 800;
        color: #0F172A !important;
    }

    /* Protocol & Action Cards */
    .protocol-box {
        background: #FFFFFF;
        border: 3px solid #0F172A;
        border-left: 8px solid #4F46E5;
        padding: 18px 20px;
        border-radius: 14px;
        margin-bottom: 16px;
        box-shadow: 5px 5px 0px #0F172A;
        transition: transform 0.2s ease;
    }
    .protocol-box:hover {
        transform: translateX(3px);
    }
    .protocol-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.08rem;
        font-weight: 900;
        color: #0F172A !important;
        margin-bottom: 6px;
    }
    .protocol-desc {
        font-size: 0.95rem;
        font-weight: 600;
        color: #1E293B !important;
        line-height: 1.6;
    }

    /* High-Visibility Animated Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4F46E5 0%, #2563EB 100%) !important;
        color: #FFFFFF !important;
        border: 3px solid #0F172A !important;
        border-radius: 12px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
        padding: 0.65rem 1.2rem !important;
        box-shadow: 4px 4px 0px #0F172A !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #4338CA 0%, #1D4ED8 100%) !important;
        transform: translateY(-2px) translateX(-2px);
        box-shadow: 6px 6px 0px #0F172A !important;
    }

    /* Animated Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #FFFFFF;
        padding: 10px;
        border-radius: 16px;
        border: 3px solid #0F172A;
        box-shadow: 5px 5px 0px #0F172A;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Outfit', sans-serif;
        font-size: 0.95rem;
        color: #1E293B !important;
        border-radius: 10px;
        padding: 12px 18px;
        font-weight: 800;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4F46E5 0%, #0284C7 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 3px 3px 0px #0F172A;
    }

    /* Headers & Inputs */
    h1, h2, h3, h4 {
        font-family: 'Outfit', sans-serif !important;
        color: #0F172A !important;
        font-weight: 900 !important;
    }
    p, label, .stMarkdown {
        color: #0F172A !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.98rem;
        font-weight: 700;
    }
    [data-baseweb="select"] > div, [data-baseweb="input"] > div {
        background-color: #FFFFFF !important;
        border: 2.5px solid #0F172A !important;
        border-radius: 10px !important;
        color: #0F172A !important;
        font-weight: 700 !important;
    }
    [data-testid="stDataFrame"], [data-testid="stExpander"], [data-testid="stForm"] {
        background-color: #FFFFFF !important;
        border: 3px solid #0F172A !important;
        border-radius: 16px !important;
        box-shadow: 5px 5px 0px #0F172A !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. MULTILINGUAL VOICE & UI STRINGS
# -----------------------------------------------------------------------------
LANG_CONFIG = {
    "English": {"code": "en"},
    "हिन्दी (Hindi)": {"code": "hi"},
    "ಕನ್ನಡ (Kannada)": {"code": "kn"},
}

UI_STRINGS = {
    "English": {
        "title": "ROUTELESS // Smart Rural Student Transit",
        "subtitle": "Live Student Dispatch, Real-Time Crowd Analytics & Multilingual Voice AI",
        "guide_title": "👋 Quick Start Guide (Easy 3-Step Overview)",
        "guide_body": """
        * **Step 1 — Add & Dispatch Students:** Open the **➕ Add & Dispatch Student** tab to register a student, assign a bus, and send them directly to the Exam Center.
        * **Step 2 — Test Crisis Scenarios:** Use the **1-Click Scenario Presets** on the left sidebar to see how the AI handles bus breakdowns, +40% exam crowds, and flooded roads.
        * **Step 3 — Voice & AI Assistant:** Click **Listen to Live Voice Briefing** or ask the AI Assistant in **English, Hindi, or Kannada**!
        """,
        "speak_btn": "🔊 Listen to Live Voice Briefing (English)",
    },
    "हिन्दी (Hindi)": {
        "title": "रूटलेस (ROUTELESS) // स्मार्ट ग्रामीण छात्र परिवहन",
        "subtitle": "लाइव छात्र डिस्पैच, रीयल-टाइम भीड़ विश्लेषण और बहुभाषी वॉयस एआई",
        "guide_title": "👋 त्वरित मार्गदर्शिका (आसान 3-चरणीय परिचय)",
        "guide_body": """
        * **चरण 1 — छात्र जोड़ें और भेजें:** किसी भी छात्र को बस में जोड़ने और सीधे परीक्षा केंद्र भेजने के लिए **➕ Add & Dispatch Student** टैब खोलें।
        * **चरण 2 — आपात स्थिति जांचें:** बाईं ओर दिए गए बटन दबाकर देखें कि बस खराब होने या बाढ़ आने पर एआई कैसे तुरंत समाधान करता है।
        * **चरण 3 — आवाज़ और एआई सहायक:** लाइव हिंदी घोषणा सुनें या एआई से अपना प्रश्न पूछें!
        """,
        "speak_btn": "🔊 लाइव आवाज़ घोषणा सुनें (हिन्दी)",
    },
    "ಕನ್ನಡ (Kannada)": {
        "title": "ರೂಟ್‌ಲೆಸ್ (ROUTELESS) // ಸ್ಮಾರ್ಟ್ ಗ್ರಾಮೀಣ ವಿದ್ಯಾರ್ಥಿ ಸಾರಿಗೆ",
        "subtitle": "ನೇರ ವಿದ್ಯಾರ್ಥಿ ರವಾನೆ, ಜನಸಂದಣಿ ವಿಶ್ಲೇಷಣೆ ಮತ್ತು ಬಹುಭಾಷಾ ಧ್ವನಿ AI",
        "guide_title": "👋 ತ್ವರಿತ ಮಾರ್ಗದರ್ಶಿ (ಸರಳ 3-ಹಂತಗಳ ಮಾಹಿತಿ)",
        "guide_body": """
        * **ಹಂತ 1 — ವಿದ್ಯಾರ್ಥಿಯನ್ನು ಬಸ್‌ಗೆ ಸೇರಿಸಿ:** ವಿದ್ಯಾರ್ಥಿಯನ್ನು ನೋಂದಾಯಿಸಲು ಮತ್ತು ಪರೀಕ್ಷಾ ಕೇಂದ್ರಕ್ಕೆ ಕಳುಹಿಸಲು **➕ Add & Dispatch Student** ಟ್ಯಾಬ್ ತೆರೆಯಿರಿ.
        * **ಹಂತ 2 — ತುರ್ತು ಪರಿಸ್ಥಿತಿ ಪರೀಕ್ಷಿಸಿ:** ಬಸ್ ಕೆಟ್ಟುಹೋದಾಗ ಅಥವಾ ಪ್ರವಾಹ ಬಂದಾಗ AI ಹೇಗೆ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತದೆ ಎಂಬುದನ್ನು ಎಡಭಾಗದ ಬಟನ್‌ಗಳಿಂದ ನೋಡಿ.
        * **ಹಂತ 3 — ಧ್ವನಿ ಮತ್ತು AI ಸಹಾಯಕ:** ಕನ್ನಡದಲ್ಲಿ ನೇರ ಧ್ವನಿ ಪ್ರಕಟಣೆ ಕೇಳಿ ಅಥವಾ AI ಸಹಾಯಕರನ್ನು ಪ್ರಶ್ನಿಸಿ!
        """,
        "speak_btn": "🔊 ನೇರ ಧ್ವನಿ ಪ್ರಕಟಣೆ ಕೇಳಿ (ಕನ್ನಡ)",
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
# 3. NODES & BASE MANIFEST DATA
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
        journey_stage = np.random.choice(["Arrived at Exam Hub", "In Transit on Bus", "Waiting at Pickup"], p=[0.35, 0.45, 0.20])
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
# 4. SESSION STATE INITIALIZATION
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
# 5. SIDEBAR: LANGUAGE, PRESETS & CONTROLS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🌐 Language / भाषा / ಭಾಷೆ")
    selected_lang = st.selectbox(
        "Select Preferred Language",
        list(LANG_CONFIG.keys()),
        index=0
    )
    lang_code = LANG_CONFIG[selected_lang]["code"]
    strings = UI_STRINGS[selected_lang]

    st.markdown("### ⚡ 1-Click Scenario Presets")
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        if st.button("🚨 Exam Crisis", use_container_width=True):
            st.session_state.broken_buses = 2
            st.session_state.demand_surge = 40
            st.session_state.flood_idx = 1
            st.session_state.micro_feeders = True
    with p_col2:
        if st.button("✅ Normal Day", use_container_width=True):
            st.session_state.broken_buses = 0
            st.session_state.demand_surge = 0
            st.session_state.flood_idx = 0
            st.session_state.micro_feeders = False

    if st.button("🌊 Extreme Flood + 4 Down", use_container_width=True):
        st.session_state.broken_buses = 4
        st.session_state.demand_surge = 60
        st.session_state.flood_idx = 2
        st.session_state.micro_feeders = True

    st.markdown("---")
    st.markdown("### 🎛️ Live Network Controls")
    broken_buses = st.slider("Disabled Government Buses", 0, 4, key="broken_buses")
    demand_surge_pct = st.slider("Exam Day Demand Surge (%)", 0, 80, step=5, key="demand_surge")
    flood_options = [
        "None (All Clear)",
        "Maralawadi ↔ Edu Hub (Bridge Submerged)",
        "Harohalli ↔ Edu Hub (Landslide)"
    ]
    flood_corridor = st.selectbox(
        "Flooded / Blocked Corridor",
        flood_options,
        index=st.session_state.flood_idx
    )
    deploy_micro_feeders = st.toggle("Deploy Local Auto/Van Feeders", key="micro_feeders")

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
    surge_sample["Student_Name"] = [f"Surge Student #{i}" for i in range(1, n_extra + 1)]
    surge_sample["Exam_Candidate"] = np.random.choice([True, False], size=n_extra, p=[0.65, 0.35])
    surge_sample["Minutes_To_Gate_Close"] = np.where(surge_sample["Exam_Candidate"], np.random.choice([50, 85, 115], size=n_extra), 360)
    df = pd.concat([base_df, surge_sample], ignore_index=True)
else:
    df = base_df.copy()

if st.session_state.custom_students:
    custom_df = pd.DataFrame(st.session_state.custom_students)
    df = pd.concat([custom_df, df], ignore_index=True)

affected_village = "Maralawadi Cluster" if "Maralawadi" in flood_corridor else ("Harohalli Sector" if "Harohalli" in flood_corridor else None)
df["Corridor_Status"] = np.where(df["Origin_Village"] == affected_village, "REROUTED (+18m Bypass)", "NOMINAL")

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
        return f"GOV-BUS-0{(idx // bus_capacity) + 1}"
    elif idx < (primary_seat_pool + feeder_seat_pool):
        return f"FEEDER-AUTO-{(idx - primary_seat_pool) // 6 + 1:02d}"
    else:
        return "DEFERRED / WAVE-2 STANDBY"

df["Assigned_Unit"] = [assign_transport(i, r) for i, r in df.iterrows()]

total_students = len(df)
exam_students = df[df["Exam_Candidate"]]
total_exam_students = len(exam_students)
rescued_exam_students = len(exam_students[~exam_students["Assigned_Unit"].str.contains("DEFERRED")])
exam_rescue_rate = (rescued_exam_students / total_exam_students * 100) if total_exam_students > 0 else 100.0
total_seated = len(df[~df["Assigned_Unit"].str.contains("DEFERRED")])
unseated_count = total_students - total_seated

# -----------------------------------------------------------------------------
# 7. HEADER, GUIDE & VOICE BRIEFING
# -----------------------------------------------------------------------------
is_crisis = (broken_buses > 0) or (demand_surge_pct >= 25) or (affected_village is not None)
st.markdown(f"""
<div class="command-header">
    <div>
        <div class="command-title">{strings['title']}</div>
        <div class="command-subtitle">{strings['subtitle']}</div>
    </div>
    <div class="status-badge {'status-crisis' if is_crisis else 'status-normal'}">{'🚨 Active Crisis Response' if is_crisis else '✅ Smooth Operations'}</div>
</div>
""", unsafe_allow_html=True)

col_guide, col_voice = st.columns([1.85, 1.15])
with col_guide:
    with st.expander(strings["guide_title"], expanded=True):
        st.markdown(strings["guide_body"])

with col_voice:
    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
    if st.button(strings["speak_btn"], use_container_width=True):
        if lang_code == "hi":
            briefing = f"रूटलेस लाइव अपडेट। कुल {total_students} छात्रों में से {rescued_exam_students} परीक्षा छात्रों को बस सीट मिल गई है। {active_buses} सरकारी बसें और {feeder_units} ऑटो रिक्शा छात्रों को परीक्षा केंद्र ले जा रहे हैं।"
        elif lang_code == "kn":
            briefing = f"ರೂಟ್‌ಲೆಸ್ ನೇರ ಮಾಹಿತಿ. ಒಟ್ಟು {total_students} ವಿದ್ಯಾರ್ಥಿಗಳಲ್ಲಿ {rescued_exam_students} ಪರೀಕ್ಷಾ ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ ಸೀಟು ಖಚಿತವಾಗಿದೆ. {active_buses} ಸರ್ಕಾರಿ ಬಸ್‌ಗಳು ಮತ್ತು {feeder_units} ಆಟೋ ರಿಕ್ಷಾಗಳು ವಿದ್ಯಾರ್ಥಿಗಳನ್ನು ಪರೀಕ್ಷಾ ಕೇಂದ್ರಕ್ಕೆ ಕರೆದೊಯ್ಯುತ್ತಿವೆ."
        else:
            briefing = f"Routeless Live Dispatch Briefing. {rescued_exam_students} out of {total_exam_students} exam students have confirmed seats, achieving {exam_rescue_rate:.0f} percent exam coverage. {active_buses} Express Buses and {feeder_units} Feeder Autos are actively transporting students."
        audio_data = text_to_audio_bytes(briefing, lang_code)
        if audio_data:
            st.audio(audio_data, format="audio/mp3", autoplay=True)
        else:
            st.info(briefing)

# -----------------------------------------------------------------------------
# 8. ANIMATED KPI CARDS
# -----------------------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'''
    <div class="kpi-card kpi-emerald">
        <div class="kpi-label">🎓 Exam Coverage</div>
        <div class="kpi-value">{exam_rescue_rate:.1f}%</div>
        <div class="kpi-trend">✅ {rescued_exam_students} / {total_exam_students} Secured</div>
    </div>
    ''', unsafe_allow_html=True)
with c2:
    st.markdown(f'''
    <div class="kpi-card kpi-sky">
        <div class="kpi-label">🚌 Active Fleet</div>
        <div class="kpi-value">{total_seated} <span style="font-size:1.2rem;color:#334155;">/ {total_students}</span></div>
        <div class="kpi-trend">⚡ {active_buses} Buses + {feeder_units} Autos</div>
    </div>
    ''', unsafe_allow_html=True)
with c3:
    st.markdown(f'''
    <div class="kpi-card kpi-amber">
        <div class="kpi-label">📈 Crowd Surge</div>
        <div class="kpi-value">+{demand_surge_pct}%</div>
        <div class="kpi-trend">⚠️ {broken_buses} Buses Under Repair</div>
    </div>
    ''', unsafe_allow_html=True)
with c4:
    st.markdown(f'''
    <div class="kpi-card kpi-indigo">
        <div class="kpi-label">🛡️ Exam Stranded</div>
        <div class="kpi-value">{max(0, total_exam_students - rescued_exam_students)}</div>
        <div class="kpi-trend">🕒 {unseated_count} in Wave-2</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 9. ANIMATED TABS & WORKSPACES
# -----------------------------------------------------------------------------
tab_add, tab_people, tab_ai, tab_sim, tab_manifest = st.tabs([
    "➕ Add & Dispatch Student",
    "📊 Real-Time People Analytics",
    "🤖 Multilingual AI Assistant",
    "🎮 Live Route Simulator",
    "📋 Full Student Manifest"
])

with tab_add:
    st.markdown("#### 🚌 Register Student & Direct Dispatch to Kanakapura Exam Center")
    st.markdown("Assign any student directly onto an active vehicle and generate their priority boarding pass instantly.")

    form_col, feed_col = st.columns([1.3, 1.2])

    with form_col:
        with st.form("dispatch_student_form", clear_on_submit=True):
            s_name = st.text_input("Student Full Name", placeholder="e.g., Priya Sharma")
            c_sub1, c_sub2 = st.columns(2)
            with c_sub1:
                s_village = st.selectbox("Pickup Village", [k for k, v in NODES.items() if v["type"] == "VILLAGE"])
            with c_sub2:
                available_bus_list = [f"GOV-BUS-0{i}" for i in range(1, active_buses + 1)] + [f"FEEDER-AUTO-0{i}" for i in range(1, 6)]
                s_bus = st.selectbox("Assign Vehicle", available_bus_list)

            c_sub3, c_sub4 = st.columns(2)
            with c_sub3:
                s_exam = st.checkbox("Appearing for Exam Today", value=True)
            with c_sub4:
                s_mins = st.number_input("Minutes to Gate Close", min_value=15, max_value=240, value=60, step=15)

            submitted = st.form_submit_button("🚀 Dispatch to Exam Center", use_container_width=True)

            if submitted:
                clean_name = s_name.strip() if s_name.strip() else f"Walk-In Student #{len(st.session_state.custom_students) + 1}"
                new_id = f"RTL-VIP-{101 + len(st.session_state.custom_students)}"
                dist_map = {"Harohalli Sector": 16.4, "Maralawadi Cluster": 14.8, "Sathanur South": 12.2, "Kodihalli Creek": 9.5, "Uyyamballi Outpost": 15.1}
                
                new_record = {
                    "Student_ID": new_id,
                    "Student_Name": clean_name,
                    "Origin_Village": s_village,
                    "Exam_Candidate": s_exam,
                    "Minutes_To_Gate_Close": int(s_mins),
                    "Distance_KM": dist_map.get(s_village, 12.0),
                    "Journey_Status": "Dispatched to Exam Hub",
                    "Manual_Bus_Override": s_bus
                }
                st.session_state.custom_students.insert(0, new_record)
                st.success(f"✅ **{clean_name} ({new_id})** assigned to **{s_bus}** from **{s_village}** and dispatched!")
                
                confirm_voice = f"Confirmed! Student {clean_name} has been assigned to {s_bus} and dispatched."
                audio_confirm = text_to_audio_bytes(confirm_voice, lang_code)
                if audio_confirm:
                    st.audio(audio_confirm, format="audio/mp3", autoplay=True)

    with feed_col:
        st.markdown("#### 🎫 Live Priority Boarding Passes")
        if st.session_state.custom_students:
            for stu in st.session_state.custom_students[:4]:
                st.markdown(f"""
                <div class="protocol-box" style="border-left-color: #059669; background: #ECFDF5;">
                    <div class="protocol-title">🎫 {stu['Student_Name']} ({stu['Student_ID']})</div>
                    <div class="protocol-desc">
                        • <b>Vehicle:</b> {stu['Manual_Bus_Override']}<br>
                        • <b>Route:</b> {stu['Origin_Village']} ➔ Exam Hub<br>
                        • <b>Status:</b> 🟢 {stu['Journey_Status']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="protocol-box" style="border-left-color: #0284C7; background: #F0F9FF;">
                <div class="protocol-title">No Dispatches Yet</div>
                <div class="protocol-desc">Use the form on the left to board students onto buses and generate priority boarding passes.</div>
            </div>
            """, unsafe_allow_html=True)

with tab_people:
    st.markdown("#### 📊 Real-Time Passenger Flow & Crowd Telemetry")
    arrived_cnt = int((df["Journey_Status"] == "Arrived at Exam Hub").sum())
    transit_cnt = int((df["Journey_Status"].isin(["In Transit on Bus", "Dispatched to Exam Hub"])).sum())
    waiting_cnt = int((df["Journey_Status"] == "Waiting at Pickup").sum())

    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown(f'<div class="kpi-card kpi-emerald"><div class="kpi-label">🏫 Arrived at Exam Hub</div><div class="kpi-value">{arrived_cnt} People</div><div class="kpi-trend">Checked in at gates</div></div>', unsafe_allow_html=True)
    with p2:
        st.markdown(f'<div class="kpi-card kpi-sky"><div class="kpi-label">🚌 In-Transit</div><div class="kpi-value">{transit_cnt} People</div><div class="kpi-trend">En route on buses & autos</div></div>', unsafe_allow_html=True)
    with p3:
        st.markdown(f'<div class="kpi-card kpi-amber"><div class="kpi-label">🚏 Waiting at Stops</div><div class="kpi-value">{waiting_cnt} People</div><div class="kpi-trend">Next pickup soon</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    g1, g2 = st.columns(2)
    with g1:
        village_summary = df.groupby(["Origin_Village", "Exam_Candidate"]).size().reset_index(name="People")
        village_summary["Category"] = np.where(village_summary["Exam_Candidate"], "Exam Candidates (Priority 1)", "Regular Students (Priority 2)")
        fig1 = px.bar(
            village_summary, x="Origin_Village", y="People", color="Category",
            title="Real-Time Student Crowd by Village",
            color_discrete_map={"Exam Candidates (Priority 1)": "#4F46E5", "Regular Students (Priority 2)": "#38BDF8"},
            barmode="group"
        )
        fig1.update_traces(marker_line_color="#0F172A", marker_line_width=1.5)
        fig1.update_layout(
            paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAFC",
            font=dict(color="#0F172A", family="Plus Jakarta Sans"),
            margin=dict(l=20, r=20, t=45, b=20),
            xaxis=dict(linecolor="#0F172A", linewidth=2, mirror=True, title=""),
            yaxis=dict(linecolor="#0F172A", linewidth=2, mirror=True, gridcolor="#E2E8F0", title="Number of People")
        )
        st.plotly_chart(fig1, use_container_width=True)

    with g2:
        mode_counts = df["Assigned_Unit"].apply(
            lambda x: "Gov Express Bus" if "GOV-BUS" in x else ("Micro-Feeder Auto" if "FEEDER" in x else "Wave-2 Standby")
        ).value_counts()
        fig2 = px.pie(
            names=mode_counts.index, values=mode_counts.values, hole=0.52,
            title="Live Transport Mode Allocation",
            color_discrete_sequence=["#059669", "#0284C7", "#F59E0B"]
        )
        fig2.update_traces(marker=dict(line=dict(color="#0F172A", width=2)), textinfo="percent+label")
        fig2.update_layout(
            paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
            font=dict(color="#0F172A", family="Plus Jakarta Sans"),
            margin=dict(l=20, r=20, t=45, b=20)
        )
        st.plotly_chart(fig2, use_container_width=True)

with tab_ai:
    st.markdown("#### 💬 Routeless Multilingual AI Assistant")
    st.markdown("Ask questions or check individual student IDs.")

    q1, q2, q3 = st.columns(3)
    quick_prompt = None
    with q1:
        if st.button("🎓 Exam seat coverage status?", use_container_width=True):
            quick_prompt = "Exam seat coverage status?"
    with q2:
        if st.button("🌊 Road flood & detour status?", use_container_width=True):
            quick_prompt = "Road flood & detour status?"
    with q3:
        if st.button("🔍 Check Student RTL-2026005", use_container_width=True):
            quick_prompt = "Check Student RTL-2026005"

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
            route = matched_student["Corridor_Status"]
            return f"Student **{sname} ({sid})** from **{village}** is confirmed on **{unit}**. Corridor Status: **{route}**."

        if any(w in q_lower for w in ["flood", "road", "blocked", "detour"]):
            if affected_village:
                return f"**Flood Detour Active:** The main road from **{affected_village}** is blocked by flooding. Buses are rerouted via **Kodihalli Creek Bypass (+18 mins)**."
            else:
                return "**All Roads Clear:** No flooding or road blockages are active right now."

        return (
            f"**Live Fleet Report:** **{rescued_exam_students} out of {total_exam_students}** exam candidates (**{exam_rescue_rate:.1f}%**) have confirmed transport. "
            f"Active fleet: **{active_buses} Express Buses** and **{feeder_units} Feeder Autos**."
        )

    if active_query:
        st.session_state.chat_history.append({"role": "user", "content": active_query})
        reply = generate_ai_response(active_query, lang_code)
        audio_reply = text_to_audio_bytes(reply.replace("**", ""), lang_code)
        st.session_state.chat_history.append({"role": "assistant", "content": reply, "audio": audio_reply})

    for msg in st.session_state.chat_history[-6:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("audio"):
                st.audio(msg["audio"], format="audio/mp3")

with tab_sim:
    st.markdown("#### 🎮 Interactive Real-Time Fleet Movement Simulator")
    sim_col1, sim_col2 = st.columns([1, 2.4])
    with sim_col1:
        sim_step = st.slider("Journey Progress (Minutes)", 0, 60, 30, step=5)
        run_anim = st.button("▶️ Play Live Bus Animation", use_container_width=True)
        st.markdown(f"""
        <div class="protocol-box" style="border-left-color: #0284C7; background: #F0F9FF;">
            <div class="protocol-title">⏱️ T + {sim_step} Mins Status</div>
            <div class="protocol-desc">
            • <b>Buses Active:</b> {active_buses} Express Units<br>
            • <b>Feeders Active:</b> {feeder_units} Auto-Rickshaws<br>
            • <b>Route Mode:</b> {'Detour Active (' + affected_village + ')' if affected_village else 'Direct Corridors'}<br>
            • <b>Trip Completion:</b> {min(100, int((sim_step / 55) * 100))}%
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
                        mode="lines", line=dict(color="#E11D48", width=3, dash="dash"),
                        name="Blocked Road"
                    ))
                    wp = NODES["Kodihalli Creek"]
                    fig_sim.add_trace(go.Scatter(
                        x=[coords["lon"], wp["lon"], hub["lon"]],
                        y=[coords["lat"], wp["lat"], hub["lat"]],
                        mode="lines", line=dict(color="#D97706", width=4),
                        name="Safe Bypass"
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
                        name="Active Corridor"
                    ))
                    vx = coords["lon"] + (hub["lon"] - coords["lon"]) * progress
                    vy = coords["lat"] + (hub["lat"] - coords["lat"]) * progress

                fig_sim.add_trace(go.Scatter(
                    x=[vx], y=[vy], mode="markers+text",
                    text=["🚌"], textfont=dict(size=20),
                    marker=dict(size=14, color="#10B981", line=dict(width=2, color="#0F172A")),
                    showlegend=False
                ))

            node_df = pd.DataFrame([{"Name": k, "Lon": v["lon"], "Lat": v["lat"]} for k, v in NODES.items()])
            fig_sim.add_trace(go.Scatter(
                x=node_df["Lon"], y=node_df["Lat"], mode="markers+text",
                text=node_df["Name"], textposition="top center",
                textfont=dict(family="Plus Jakarta Sans", size=12, color="#0F172A"),
                marker=dict(size=16, color="#0F172A"),
                name="Hubs & Villages"
            ))

            fig_sim.update_layout(
                title=f"Live Fleet Map at T + {minute_mark} Minutes",
                paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAFC",
                font=dict(color="#0F172A", family="Plus Jakarta Sans"),
                height=420, margin=dict(l=15, r=15, t=40, b=15),
                showlegend=False,
                xaxis=dict(showgrid=True, gridcolor="#CBD5E1", linecolor="#0F172A", linewidth=2, mirror=True),
                yaxis=dict(showgrid=True, gridcolor="#CBD5E1", linecolor="#0F172A", linewidth=2, mirror=True)
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
    with f1: filter_exam = st.selectbox("Filter Student Group", ["All Students", "Exam Candidates Only", "Regular Commuters"])
    with f2: filter_village = st.selectbox("Origin Village", ["All Villages"] + list(df["Origin_Village"].unique()))
    with f3: search_id = st.text_input("Search Name or ID", placeholder="e.g., Priya or RTL-2026004")

    filtered_df = df.copy()
    if filter_exam == "Exam Candidates Only": filtered_df = filtered_df[filtered_df["Exam_Candidate"]]
    elif filter_exam == "Regular Commuters": filtered_df = filtered_df[~filtered_df["Exam_Candidate"]]
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
            "Criticality_Index": st.column_config.ProgressColumn("Priority Score", format="%.1f", min_value=0, max_value=100),
            "Exam_Candidate": st.column_config.CheckboxColumn("Exam Today")
        }
    )
