import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from gtts import gTTS
from io import BytesIO
import time

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG & LIGHT-MODE CURVY DESIGN SYSTEM (CUSTOM CSS)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ROUTELESS // Multilingual Smart Transit",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,800;1,700;1,800&family=Lora:ital,wght@0,600;0,700;1,600;1,700&display=swap');

    .stApp {
        background-color: #F4F6F9;
        color: #0F172A;
        font-family: 'Lora', Georgia, serif;
        font-weight: 700;
        font-style: italic;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}

    /* Sidebar Styling with Darkened Boundary */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 2.5px solid #0F172A;
    }
    [data-testid="stSidebar"] .stMarkdown h3 {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.05rem;
        font-weight: 800;
        font-style: italic;
        color: #0F172A;
        text-transform: uppercase;
        border-bottom: 2px solid #0F172A;
        padding-bottom: 6px;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
        color: #0F172A !important;
        font-family: 'Lora', Georgia, serif !important;
        font-weight: 700 !important;
        font-style: italic !important;
    }

    /* Top Command Header */
    .command-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 26px;
        background: #FFFFFF;
        border: 2.5px solid #0F172A;
        border-left: 8px solid #0F172A;
        border-radius: 14px;
        margin-bottom: 18px;
        box-shadow: 5px 5px 0px #0F172A;
    }
    .command-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.6rem;
        font-weight: 800;
        font-style: italic;
        color: #0F172A;
        margin: 0;
    }
    .command-subtitle {
        font-family: 'Lora', Georgia, serif;
        font-size: 0.88rem;
        font-weight: 700;
        font-style: italic;
        color: #334155;
        margin-top: 4px;
    }
    .status-badge {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 0.85rem;
        padding: 8px 16px;
        border-radius: 999px;
        font-weight: 800;
        font-style: italic;
        border: 2px solid #0F172A;
    }
    .status-crisis { background: #FEE2E2; color: #991B1B; }
    .status-normal { background: #DCFCE7; color: #166534; }

    /* KPI Telemetry Cards */
    .kpi-card {
        background: #FFFFFF;
        border: 2.5px solid #0F172A;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 4px 4px 0px #0F172A;
        transition: all 0.2s ease;
    }
    .kpi-card:hover {
        transform: translate(-2px, -2px);
        box-shadow: 6px 6px 0px #0F172A;
    }
    .kpi-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        color: #334155;
        font-weight: 700;
        font-style: italic;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 2rem;
        font-weight: 800;
        font-style: italic;
        color: #0F172A;
        line-height: 1.1;
    }
    .kpi-trend {
        font-size: 0.78rem;
        margin-top: 8px;
        font-weight: 700;
        font-style: italic;
    }
    .trend-good { color: #15803D; }
    .trend-warn { color: #B45309; }
    .trend-bad { color: #B91C1C; }

    /* Protocol & Guide Boxes */
    .protocol-box {
        background: #FFFFFF;
        border: 2px solid #0F172A;
        border-left: 6px solid #0F172A;
        padding: 14px 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        box-shadow: 3px 3px 0px #0F172A;
    }
    .protocol-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 0.95rem;
        font-weight: 800;
        font-style: italic;
        color: #0F172A;
        margin-bottom: 4px;
    }
    .protocol-desc {
        font-size: 0.86rem;
        color: #1E293B;
        line-height: 1.45;
    }

    /* Buttons with Darkened Borders */
    .stButton > button {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 2px solid #0F172A !important;
        border-radius: 10px !important;
        font-family: 'Playfair Display', Georgia, serif !important;
        font-weight: 800 !important;
        font-style: italic !important;
        box-shadow: 3px 3px 0px #0F172A !important;
        transition: all 0.15s ease !important;
    }
    .stButton > button:hover {
        background-color: #0F172A !important;
        color: #FFFFFF !important;
        transform: translate(-1px, -1px);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #FFFFFF;
        padding: 8px;
        border-radius: 12px;
        border: 2.5px solid #0F172A;
        box-shadow: 3px 3px 0px #0F172A;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 0.88rem;
        color: #334155;
        border-radius: 8px;
        padding: 10px 16px;
        font-weight: 800;
        font-style: italic;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0F172A !important;
        color: #FFFFFF !important;
    }

    h1, h2, h3, h4, p, label, .stMarkdown {
        color: #0F172A !important;
        font-family: 'Lora', Georgia, serif !important;
        font-weight: 700 !important;
        font-style: italic !important;
    }
    [data-baseweb="select"] > div, [data-baseweb="input"] > div {
        background-color: #FFFFFF !important;
        border: 2px solid #0F172A !important;
        border-radius: 8px !important;
        color: #0F172A !important;
    }
    [data-testid="stDataFrame"], [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 2.5px solid #0F172A !important;
        border-radius: 12px !important;
        box-shadow: 4px 4px 0px #0F172A !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. MULTILINGUAL TRANSLATIONS & VOICE SYNTHESIS HELPER
# -----------------------------------------------------------------------------
LANG_CONFIG = {
    "English": {"code": "en", "flag": "🇬🇧"},
    "हिन्दी (Hindi)": {"code": "hi", "flag": "🇮🇳"},
    "ಕನ್ನಡ (Kannada)": {"code": "kn", "flag": "🇮🇳"},
}

UI_STRINGS = {
    "English": {
        "title": "Routeless // Smart Rural Student Transit",
        "subtitle": "Interactive Crisis Dispatch, Multilingual Voice & AI Assistant",
        "guide_title": "👋 New Here? Click for a 30-Second Beginner Guide",
        "guide_body": """
        1. **Pick a Preset Scenario** on the left sidebar (or adjust sliders) to simulate bus breakdowns, +40% exam day crowds, or flooded roads.
        2. **Watch Instant Reallocation:** The AI automatically reserves seats for students with exams first and deploys local auto-rickshaws for overflow.
        3. **Use Voice & AI Assistant:** Click **Speak Live Briefing** or ask the AI Assistant in **English, Hindi, or Kannada** to check routes or student seat numbers!
        """,
        "speak_btn": "🔊 Listen to Live Voice Briefing (English)",
    },
    "हिन्दी (Hindi)": {
        "title": "रूटलेस (ROUTELESS) // ग्रामीण छात्र परिवहन प्रणाली",
        "subtitle": "आपातकालीन बस प्रबंधन, बहुभाषी आवाज़ और एआई सहायक",
        "guide_title": "👋 पहली बार आए हैं? 30-सेकंड की आसान गाइड देखें",
        "guide_body": """
        1. **आपात स्थिति चुनें:** बाईं ओर दिए गए बटन दबाएं (जैसे बस खराब होना, 40% भीड़ बढ़ना, या सड़क पर बाढ़ आना)।
        2. **तुरंत सीट आवंटन देखें:** एआई पहले परीक्षा देने वाले छात्रों को बस में सीट देता है और अतिरिक्त छात्रों के लिए ऑटो-रिक्शा भेजता है।
        3. **आवाज़ और एआई सहायक:** नीचे दिए गए बटन से हिंदी में लाइव घोषणा सुनें या एआई से अपना बस नंबर पूछें!
        """,
        "speak_btn": "🔊 लाइव आवाज़ घोषणा सुनें (हिन्दी)",
    },
    "ಕನ್ನಡ (Kannada)": {
        "title": "ರೂಟ್‌ಲೆಸ್ (ROUTELESS) // ಗ್ರಾಮೀಣ ವಿದ್ಯಾರ್ಥಿ ಸಾರಿಗೆ ವ್ಯವಸ್ಥೆ",
        "subtitle": "ತುರ್ತು ಬಸ್ ನಿರ್ವಹಣೆ, ಬಹುಭಾಷಾ ಧ್ವನಿ ಮತ್ತು AI ಸಹಾಯಕ",
        "guide_title": "👋 ಹೊಸಬರೇ? 30-ಸೆಕೆಂಡುಗಳ ಸರಳ ಮಾರ್ಗದರ್ಶಿ ನೋಡಿ",
        "guide_body": """
        1. **ಪರಿಸ್ಥಿತಿಯನ್ನು ಆಯ್ಕೆಮಾಡಿ:** ಎಡಭಾಗದ ಬಟನ್‌ಗಳನ್ನು ಒತ್ತಿ (ಬಸ್ ಕೆಟ್ಟುಹೋಗುವುದು, 40% ಜನಸಂದಣಿ, ಅಥವಾ ರಸ್ತೆ ಪ್ರವಾಹ).
        2. **ತಕ್ಷಣದ ಸೀಟು ಹಂಚಿಕೆ:** ಪರೀಕ್ಷೆ ಬರೆಯುವ ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ AI ಮೊದಲ ಆದ್ಯತೆ ನೀಡುತ್ತದೆ ಮತ್ತು ಹೆಚ್ಚುವರಿ ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ ಆಟೋ-ರಿಕ್ಷಾ ವ್ಯವಸ್ಥೆ ಮಾಡುತ್ತದೆ.
        3. **ಧ್ವನಿ ಮತ್ತು AI ಸಹಾಯಕ:** ಕನ್ನಡದಲ್ಲಿ ನೇರ ಧ್ವನಿ ಪ್ರಕಟಣೆ ಕೇಳಿ ಅಥವಾ AI ಸಹಾಯಕರನ್ನು ನಿಮ್ಮ ಬಸ್ ವಿವರ ಕೇಳಿ!
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
# 3. NODES & SIMULATION DATA
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
    records = []
    for i in range(1, n_students + 1):
        v = np.random.choice(villages, p=[0.25, 0.22, 0.20, 0.18, 0.15])
        is_exam = np.random.choice([True, False], p=[0.42, 0.58])
        exam_mins = np.random.choice([45, 75, 110, 180]) if is_exam else 360
        dist_km = {"Harohalli Sector": 16.4, "Maralawadi Cluster": 14.8, "Sathanur South": 12.2, "Kodihalli Creek": 9.5, "Uyyamballi Outpost": 15.1}[v]
        records.append({
            "Student_ID": f"RTL-{2026000 + i}",
            "Origin_Village": v,
            "Exam_Candidate": is_exam,
            "Minutes_To_Gate_Close": exam_mins,
            "Distance_KM": dist_km,
            "Special_Needs": np.random.choice([True, False], p=[0.05, 0.95])
        })
    return pd.DataFrame(records)

# -----------------------------------------------------------------------------
# 4. SESSION STATE FOR PRESETS & CHAT
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

# -----------------------------------------------------------------------------
# 5. SIDEBAR: LANGUAGE, ONE-CLICK PRESETS & CONTROLS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🌐 Language / भाषा / ಭಾಷೆ")
    selected_lang = st.selectbox(
        "Choose Voice & Interface Language",
        list(LANG_CONFIG.keys()),
        index=0
    )
    lang_code = LANG_CONFIG[selected_lang]["code"]
    strings = UI_STRINGS[selected_lang]

    st.markdown("### ⚡ 1-Click Scenario Presets")
    st.caption("Tap any button below to test how the AI responds:")
    
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

    if st.button("🌊 Extreme Flood + 4 Buses Down", use_container_width=True):
        st.session_state.broken_buses = 4
        st.session_state.demand_surge = 60
        st.session_state.flood_idx = 2
        st.session_state.micro_feeders = True

    st.markdown("---")
    st.markdown("### 🎛️ Custom Controls")
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
    surge_sample["Exam_Candidate"] = np.random.choice([True, False], size=n_extra, p=[0.65, 0.35])
    surge_sample["Minutes_To_Gate_Close"] = np.where(surge_sample["Exam_Candidate"], np.random.choice([50, 85, 115], size=n_extra), 360)
    df = pd.concat([base_df, surge_sample], ignore_index=True)
else:
    df = base_df.copy()

affected_village = "Maralawadi Cluster" if "Maralawadi" in flood_corridor else ("Harohalli Sector" if "Harohalli" in flood_corridor else None)
df["Corridor_Status"] = np.where(df["Origin_Village"] == affected_village, "REROUTED (+18m Bypass)", "NOMINAL")

urgency_score = np.where(df["Exam_Candidate"], np.clip(100 - (df["Minutes_To_Gate_Close"] * 0.45), 45, 95), 15)
df["Criticality_Index"] = np.round(np.clip(urgency_score + np.where(df["Origin_Village"] == affected_village, 12, 0) + np.where(df["Special_Needs"], 15, 0) + (df["Distance_KM"]/20)*10, 0, 100), 1)
df = df.sort_values(by=["Criticality_Index", "Minutes_To_Gate_Close"], ascending=[False, True]).reset_index(drop=True)

active_buses = max(1, total_fleet - broken_buses)
primary_seat_pool = active_buses * bus_capacity
feeder_units = 14 if deploy_micro_feeders else 0
feeder_seat_pool = feeder_units * 6

def assign_transport(idx):
    if idx < primary_seat_pool:
        return f"GOV-BUS-0{(idx // bus_capacity) + 1}"
    elif idx < (primary_seat_pool + feeder_seat_pool):
        return f"FEEDER-AUTO-{(idx - primary_seat_pool) // 6 + 1:0
