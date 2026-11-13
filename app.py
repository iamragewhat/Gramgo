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
        return f"FEEDER-AUTO-{(idx - primary_seat_pool) // 6 + 1:02d}"
    else:
        return "DEFERRED / WAVE-2 STANDBY"

df["Assigned_Unit"] = [assign_transport(i) for i in range(len(df))]

total_students = len(df)
exam_students = df[df["Exam_Candidate"]]
total_exam_students = len(exam_students)
rescued_exam_students = len(exam_students[~exam_students["Assigned_Unit"].str.contains("DEFERRED")])
exam_rescue_rate = (rescued_exam_students / total_exam_students * 100) if total_exam_students > 0 else 100.0
total_seated = len(df[~df["Assigned_Unit"].str.contains("DEFERRED")])
unseated_count = total_students - total_seated

# -----------------------------------------------------------------------------
# 7. HEADER, BEGINNER GUIDE & MULTILINGUAL VOICE BRIEFING
# -----------------------------------------------------------------------------
is_crisis = (broken_buses > 0) or (demand_surge_pct >= 25) or (affected_village is not None)
st.markdown(f"""
<div class="command-header">
    <div>
        <div class="command-title">{strings['title']}</div>
        <div class="command-subtitle">{strings['subtitle']}</div>
    </div>
    <div class="status-badge {'status-crisis' if is_crisis else 'status-normal'}">{'● Active Crisis Protocol' if is_crisis else '● Normal Operations'}</div>
</div>
""", unsafe_allow_html=True)

col_guide, col_voice = st.columns([1.8, 1.2])
with col_guide:
    with st.expander(strings["guide_title"], expanded=False):
        st.markdown(strings["guide_body"])

with col_voice:
    if st.button(strings["speak_btn"], use_container_width=True):
        if lang_code == "hi":
            briefing = (
                f"रूटलेस आपातकालीन सूचना। कुल {total_students} छात्रों में से {rescued_exam_students} परीक्षा छात्रों को सीट मिल गई है। "
                f"{broken_buses} सरकारी बसें खराब हैं, इसलिए {active_buses} बसें और {feeder_units} ऑटो रिक्शा चलाए जा रहे हैं। "
                f"{'सावधान: ' + affected_village + ' मार्ग पर बाढ़ के कारण बसों को कोडिहल्ली वैकल्पिक मार्ग से भेजा गया है।' if affected_village else 'सभी मुख्य सड़कें सुरक्षित हैं।'}"
            )
        elif lang_code == "kn":
            briefing = (
                f"ರೂಟ್‌ಲೆಸ್ ತುರ್ತು ಪ್ರಕಟಣೆ. ಒಟ್ಟು {total_students} ವಿದ್ಯಾರ್ಥಿಗಳಲ್ಲಿ {rescued_exam_students} ಪರೀಕ್ಷಾ ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ ಸೀಟು ಖಚಿತವಾಗಿದೆ. "
                f"{broken_buses} ಸರ್ಕಾರಿ ಬಸ್‌ಗಳು ಕೆಟ್ಟುಹೋಗಿರುವುದರಿಂದ, {active_buses} ಬಸ್‌ಗಳು ಮತ್ತು {feeder_units} ಆಟೋ ರಿಕ್ಷಾಗಳನ್ನು ನಿಯೋಜಿಸಲಾಗಿದೆ. "
                f"{'ಎಚ್ಚರಿಕೆ: ' + affected_village + ' ರಸ್ತೆಯಲ್ಲಿ ಪ್ರವಾಹವಿರುವುದರಿಂದ ಬಸ್‌ಗಳನ್ನು ಕೋಡಿಹಳ್ಳಿ ಪರ್ಯಾಯ ಮಾರ್ಗದಲ್ಲಿ ಕಳುಹಿಸಲಾಗಿದೆ.' if affected_village else 'ಎಲ್ಲಾ ಮುಖ್ಯ ರಸ್ತೆಗಳು ಸುರಕ್ಷಿತವಾಗಿವೆ.'}"
            )
        else:
            briefing = (
                f"Routeless Live Dispatch Briefing. Out of {total_students} total students, {rescued_exam_students} out of {total_exam_students} exam candidates have secured seats, achieving {exam_rescue_rate:.0f} percent exam coverage. "
                f"With {broken_buses} government buses offline, {active_buses} express buses and {feeder_units} local feeder autos are active. "
                f"{'Alert: ' + affected_village + ' road is flooded; buses are rerouted via Kodihalli bypass.' if affected_village else 'All arterial roads are clear.'}"
            )
        audio_data = text_to_audio_bytes(briefing, lang_code)
        if audio_data:
            st.audio(audio_data, format="audio/mp3", autoplay=True)
        else:
            st.info(briefing)

# -----------------------------------------------------------------------------
# 8. KPI CARDS
# -----------------------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-label">Exam Candidate Coverage</div>
        <div class="kpi-value">{exam_rescue_rate:.1f}%</div>
        <div class="kpi-trend trend-good">✓ {rescued_exam_students} / {total_exam_students} Examinees Secured</div>
    </div>
    ''', unsafe_allow_html=True)
with c2:
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-label">Active Fleet Capacity</div>
        <div class="kpi-value">{total_seated} <span style="font-size:1.15rem;color:#475569;">/ {total_students}</span></div>
        <div class="kpi-trend trend-warn">⚡ {active_buses} Buses + {feeder_units} Feeders</div>
    </div>
    ''', unsafe_allow_html=True)
with c3:
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-label">Demand Surge Load</div>
        <div class="kpi-value">+{demand_surge_pct}%</div>
        <div class="kpi-trend trend-bad">⚠ {broken_buses} Gov Buses Offline</div>
    </div>
    ''', unsafe_allow_html=True)
with c4:
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-label">Wave-2 Deferred</div>
        <div class="kpi-value">{unseated_count}</div>
        <div class="kpi-trend trend-good">🛡️ {max(0, total_exam_students - rescued_exam_students)} Exam Candidates Stranded</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 9. INTERACTIVE WORKSPACE TABS
# -----------------------------------------------------------------------------
tab_ai, tab_sim, tab_map, tab_manifest, tab_analytics = st.tabs([
    "🤖 Multilingual AI Assistant",
    "🎮 Live Route Simulator",
    "🛰️ Network Topology Map",
    "📋 Student Seat Manifest",
    "📊 Load Analytics"
])

# --- TAB 1: MULTILINGUAL AI ASSISTANT WITH VOICE ---
with tab_ai:
    st.markdown("#### 💬 Ask the Routeless AI Assistant (English / हिन्दी / ಕನ್ನಡ)")
    st.caption("Ask about exam bus seats, flooded road detours, or type a Student ID (e.g., RTL-2026005) to check boarding status.")

    # Quick-tap beginner prompt pills
    q1, q2, q3 = st.columns(3)
    quick_prompt = None
    with q1:
        if st.button("❓ Will all exam students reach on time?", use_container_width=True):
            quick_prompt = "Will all exam students reach on time?"
    with q2:
        if st.button("🌊 How are flooded roads handled?", use_container_width=True):
            quick_prompt = "How are flooded roads handled?"
    with q3:
        if st.button("🔍 Check status for Student RTL-2026005", use_container_width=True):
            quick_prompt = "Check status for Student RTL-2026005"

    user_query = st.chat_input("Type your question here in English, Hindi, or Kannada...")
    active_query = quick_prompt or user_query

    def generate_ai_response(query: str, language: str):
        q_lower = query.lower()
        # Check if user asked for a specific student ID
        matched_student = None
        for _, row in df.iterrows():
            if row["Student_ID"].lower() in q_lower:
                matched_student = row
                break

        if matched_student is not None:
            sid = matched_student["Student_ID"]
            village = matched_student["Origin_Village"]
            unit = matched_student["Assigned_Unit"]
            route = matched_student["Corridor_Status"]
            if language == "hi":
                return f"छात्र {sid} ({village}) को {unit} आवंटित किया गया है। मार्ग की स्थिति: {route}।"
            elif language == "kn":
                return f"ವಿದ್ಯಾರ್ಥಿ {sid} ({village}) ಅವರಿಗೆ {unit} ನಿಗದಿಪಡಿಸಲಾಗಿದೆ. ಮಾರ್ಗದ ಸ್ಥಿತಿ: {route}."
            return f"Student **{sid}** from **{village}** is assigned to **{unit}**. Route Status: **{route}**."

        if any(w in q_lower for w in ["flood", "road", "blocked", "detour", "बाढ़", "सड़क", "ಪ್ರವಾಹ", "ರಸ್ತೆ"]):
            if affected_village:
                if language == "hi":
                    return f"चेतावनी: {affected_village} मुख्य सड़क बाढ़ के कारण बंद है। एआई ने सभी बसों को कोडिहल्ली क्रीक बाईपास (+18 मिनट) पर मोड़ दिया है और छात्रों को 20 मिनट पहले बुलाया है।"
                elif language == "kn":
                    return f"ಎಚ್ಚರಿಕೆ: {affected_village} ಮುಖ್ಯ ರಸ್ತೆ ಪ್ರವಾಹದಿಂದ ಮುಚ್ಚಲ್ಪಟ್ಟಿದೆ. AI ಎಲ್ಲಾ ಬಸ್‌ಗಳನ್ನು ಕೋಡಿಹಳ್ಳಿ ಬೈಪಾಸ್ (+18 ನಿಮಿಷ) ಮೂಲಕ ತಿರುಗಿಸಿದೆ."
                return f"**Flood Rerouting Active:** The direct road from **{affected_village}** is submerged. Our routing solver automatically diverted buses via the **Kodihalli Creek Bypass (+18 mins)** and advanced pickup alerts by 20 minutes."
            else:
                if language == "hi":
                    return "अभी सभी सड़कें साफ हैं और बसें सामान्य समय पर चल रही हैं।"
                elif language == "kn":
                    return "ಪ್ರಸ್ತುತ ಎಲ್ಲಾ ರಸ್ತೆಗಳು ಸುರಕ್ಷಿತವಾಗಿವೆ ಮತ್ತು ಬಸ್‌ಗಳು ಸಾಮಾನ್ಯ ಸಮಯಕ್ಕೆ ಚಲಿಸುತ್ತಿವೆ."
                return "**All Corridors Clear:** No roads are currently flooded. All buses are operating on their direct routes."

        # Default comprehensive status answer
        if language == "hi":
            return (
                f"वर्तमान स्थिति: {total_exam_students} परीक्षा छात्रों में से {rescued_exam_students} ({exam_rescue_rate:.1f}%) को सीट मिल चुकी है। "
                f"{broken_buses} बसें खराब होने के बावजूद, {active_buses} एक्सप्रेस बसें और {feeder_units} स्थानीय ऑटो-रिक्शा छात्रों को समय पर परीक्षा केंद्र पहुंचा रहे हैं।"
            )
        elif language == "kn":
            return (
                f"ಪ್ರಸ್ತುತ ಸ್ಥಿತಿ: {total_exam_students} ಪರೀಕ್ಷಾ ವಿದ್ಯಾರ್ಥಿಗಳಲ್ಲಿ {rescued_exam_students} ({exam_rescue_rate:.1f}%) ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ ಸೀಟು ಖಚಿತವಾಗಿದೆ. "
                f"{broken_buses} ಬಸ್‌ಗಳು ಕೆಟ್ಟುಹೋಗಿದ್ದರೂ, {active_buses} ಎಕ್ಸ್‌ಪ್ರೆಸ್ ಬಸ್‌ಗಳು ಮತ್ತು {feeder_units} ಸ್ಥಳೀಯ ಆಟೋ-ರಿಕ್ಷಾಗಳು ವಿದ್ಯಾರ್ಥಿಗಳನ್ನು ಸಮಯಕ್ಕೆ ಸರಿಯಾಗಿ ಪರೀಕ್ಷಾ ಕೇಂದ್ರಕ್ಕೆ ತಲುಪಿಸುತ್ತಿವೆ."
            )
        return (
            f"**Live Dispatch Summary:** **{rescued_exam_students} of {total_exam_students}** exam candidates (**{exam_rescue_rate:.1f}%**) have confirmed transport. "
            f"Even with **{broken_buses} buses offline** and a **+{demand_surge_pct}% demand surge**, our priority algorithm allocated **{active_buses} Express Gov Buses** and **{feeder_units} Micro-Feeder Autos** to ensure exam students arrive before gate closure."
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

# --- TAB 2: INTERACTIVE STEP-BY-STEP ROUTE SIMULATOR ---
with tab_sim:
    st.markdown("#### 🎮 Interactive Real-Time Fleet Movement & Crisis Simulation")
    st.caption("Drag the timeline slider or click 'Run Live Simulation' to watch buses and micro-feeders navigate around flooded roads to the Exam Hub.")

    sim_col1, sim_col2 = st.columns([1, 2.5])
    with sim_col1:
        sim_step = st.slider("Simulation Timeline (Minutes from Dispatch)", 0, 60, 30, step=5)
        run_anim = st.button("▶️ Play Live Dispatch Animation", use_container_width=True)
        
        st.markdown(f"""
        <div class="protocol-box">
            <div class="protocol-title">⏱️ T + {sim_step} Mins Telemetry</div>
            <div class="protocol-desc">
            • <b>Active Express Buses:</b> {active_buses} en route<br>
            • <b>Feeder Autos:</b> {feeder_units} bridging villages<br>
            • <b>Detour Status:</b> {'Bypassing ' + affected_village if affected_village else 'Direct Paths'}<br>
            • <b>Est. Arrival Completion:</b> {min(100, int((sim_step / 55) * 100))}%
            </div>
        </div>
        """, unsafe_allow_html=True)

    with sim_col2:
        sim_placeholder = st.empty()

        def render_sim_frame(minute_mark):
            progress = min(1.0, minute_mark / 55.0)
            hub = NODES["Kanakapura Edu Hub (Exam Center)"]
            fig_sim = go.Figure()

            # Draw corridors & moving vehicles
            for v_name, coords in NODES.items():
                if coords["type"] == "HUB":
                    continue
                is_flooded = (v_name == affected_village)
                if is_flooded:
                    # Blocked direct line (dashed red)
                    fig_sim.add_trace(go.Scatter(
                        x=[coords["lon"], hub["lon"]], y=[coords["lat"], hub["lat"]],
                        mode="lines", line=dict(color="#DC2626", width=3, dash="dash"),
                        name=f"{v_name} (Flooded)"
                    ))
                    # Detour via Kodihalli Creek
                    wp = NODES["Kodihalli Creek"]
                    fig_sim.add_trace(go.Scatter(
                        x=[coords["lon"], wp["lon"], hub["lon"]],
                        y=[coords["lat"], wp["lat"], hub["lat"]],
                        mode="lines", line=dict(color="#D97706", width=3.5),
                        name="Emergency Detour Bypass"
                    ))
                    # Vehicle position along 2-segment detour
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
                        mode="lines", line=dict(color="#0284C7", width=3),
                        name=f"{v_name} Corridor"
                    ))
                    vx = coords["lon"] + (hub["lon"] - coords["lon"]) * progress
                    vy = coords["lat"] + (hub["lat"] - coords["lat"]) * progress

                # Moving Bus Marker
                fig_sim.add_trace(go.Scatter(
                    x=[vx], y=[vy], mode="markers+text",
                    text=["🚌"], textfont=dict(size=18),
                    marker=dict(size=12, color="#16A34A", line=dict(width=2, color="#0F172A")),
                    showlegend=False
                ))

            # Plot Nodes
            node_df = pd.DataFrame([{"Name": k, "Lon": v["lon"], "Lat": v["lat"]} for k, v in NODES.items()])
            fig_sim.add_trace(go.Scatter(
                x=node_df["Lon"], y=node_df["Lat"], mode="markers+text",
                text=node_df["Name"], textposition="top center",
                textfont=dict(family="Lora, serif", size=12, color="#0F172A"),
                marker=dict(size=16, color="#0F172A"),
                name="Stations"
            ))

            fig_sim.update_layout(
                title=f"Live Fleet Position at T + {minute_mark} Minutes",
                paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAFC",
                font=dict(color="#0F172A", family="Lora, serif"),
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

# --- TAB 3: NETWORK TOPOLOGY MAP ---
with tab_map:
    col_map, col_intel = st.columns([2.3, 1])
    with col_map:
        map_df = pd.DataFrame([
            {"Name": k, "Lon": v["lon"], "Lat": v["lat"], "Status": "SEVERED" if k == affected_village else "ACTIVE"}
            for k, v in NODES.items()
        ])
        fig_map = px.scatter(
            map_df, x="Lon", y="Lat", text="Name", color="Status",
            color_discrete_map={"ACTIVE": "#0284C7", "SEVERED": "#DC2626"},
            height=440
        )
        fig_map.update_traces(
            textposition="top center",
            textfont=dict(family="Lora, serif", size=13, color="#0F172A"),
            marker=dict(size=18, line=dict(width=2.5, color="#0F172A"))
        )
        fig_map.update_layout(
            paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAFC",
            margin=dict(l=20, r=20, t=20, b=20),
            font=dict(color="#0F172A", family="Lora, serif"),
            xaxis=dict(showgrid=True, gridcolor="#CBD5E1", linecolor="#0F172A", linewidth=2, mirror=True),
            yaxis=dict(showgrid=True, gridcolor="#CBD5E1", linecolor="#0F172A", linewidth=2, mirror=True),
            legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.95)", bordercolor="#0F172A", borderwidth=2)
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with col_intel:
        st.markdown("#### 🧠 AI Rerouting Decisions")
        if affected_village:
            st.markdown(f"""
            <div class="protocol-box" style="border-left-color: #DC2626; background: #FEF2F2;">
                <div class="protocol-title" style="color: #991B1B;">Corridor Severed: {affected_village}</div>
                <div class="protocol-desc">Direct road impassable due to flooding. Telemetry computed bypass via Kodihalli Creek (+18m detour).</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="protocol-box" style="border-left-color: #16A34A; background: #F0FDF4;">
                <div class="protocol-title" style="color: #166534;">All Arterial Routes Clear</div>
                <div class="protocol-desc">Rural transit grid operating at normal speed (42 km/h avg).</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="protocol-box">
            <div class="protocol-title">Fleet Reconsolidation</div>
            <div class="protocol-desc">With <b>{broken_buses} buses offline</b>, remaining capacity is prioritized for exam students first.</div>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 4: PRIORITY SEAT MANIFEST ---
with tab_manifest:
    f1, f2, f3 = st.columns([1.5, 1.5, 2])
    with f1: filter_exam = st.selectbox("Filter Cohort", ["All Students", "Exam Candidates Only", "Non-Exam Commuters"])
    with f2: filter_village = st.selectbox("Origin Village", ["All Villages"] + list(df["Origin_Village"].unique()))
    with f3: search_id = st.text_input("Search Student ID", placeholder="e.g., RTL-2026004")

    filtered_df = df.copy()
    if filter_exam == "Exam Candidates Only": filtered_df = filtered_df[filtered_df["Exam_Candidate"]]
    elif filter_exam == "Non-Exam Commuters": filtered_df = filtered_df[~filtered_df["Exam_Candidate"]]
    if filter_village != "All Villages": filtered_df = filtered_df[filtered_df["Origin_Village"] == filter_village]
    if search_id: filtered_df = filtered_df[filtered_df["Student_ID"].str.contains(search_id, case=False)]

    st.dataframe(
        filtered_df[["Student_ID", "Origin_Village", "Exam_Candidate", "Minutes_To_Gate_Close", "Criticality_Index", "Corridor_Status", "Assigned_Unit"]],
        use_container_width=True, height=420,
        column_config={
            "Criticality_Index": st.column_config.ProgressColumn("Criticality Score", format="%.1f", min_value=0, max_value=100),
            "Exam_Candidate": st.column_config.CheckboxColumn("Exam Today"),
            "Minutes_To_Gate_Close": st.column_config.NumberColumn("Gate Closes (Min)", format="%d m")
        }
    )

# --- TAB 5: LOAD ANALYTICS ---
with tab_analytics:
    g1, g2 = st.columns(2)
    with g1:
        village_summary = df.groupby(["Origin_Village", "Exam_Candidate"]).size().reset_index(name="Count")
        village_summary["Type"] = np.where(village_summary["Exam_Candidate"], "Exam Candidate (Priority)", "Regular Commuter")
        fig1 = px.bar(
            village_summary, x="Origin_Village", y="Count", color="Type",
            color_discrete_map={"Exam Candidate (Priority)": "#0284C7", "Regular Commuter": "#94A3B8"}
        )
        fig1.update_traces(marker_line_color="#0F172A", marker_line_width=1.5)
        fig1.update_layout(
            paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAFC",
            font=dict(color="#0F172A", family="Lora, serif"),
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis=dict(linecolor="#0F172A", linewidth=2, mirror=True),
            yaxis=dict(linecolor="#0F172A", linewidth=2, mirror=True, gridcolor="#E2E8F0")
        )
        st.plotly_chart(fig1, use_container_width=True)
    with g2:
        mode_counts = df["Assigned_Unit"].apply(lambda x: "Gov Express Bus" if "GOV-BUS" in x else ("Micro-Feeder" if "FEEDER" in x else "Deferred")).value_counts()
        fig2 = px.pie(
            names=mode_counts.index, values=mode_counts.values, hole=0.55,
            color_discrete_sequence=["#16A34A", "#0284C7", "#DC2626"]
        )
        fig2.update_traces(marker=dict(line=dict(color="#0F172A", width=2)))
        fig2.update_layout(
            paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
            font=dict(color="#0F172A", family="Lora, serif"),
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig2, use_container_width=True)
