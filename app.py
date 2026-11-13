import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG & ENTERPRISE DESIGN SYSTEM (CUSTOM CSS)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ROUTELESS // Rural Transit Command",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap');

    .stApp {
        background-color: #080C14;
        color: #E2E8F0;
        font-family: 'Inter', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}

    [data-testid="stSidebar"] {
        background-color: #0D1320;
        border-right: 1px solid #1E293B;
    }

    .command-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 24px;
        background: linear-gradient(90deg, #0F172A 0%, #1E293B 100%);
        border: 1px solid #334155;
        border-left: 4px solid #38BDF8;
        border-radius: 6px;
        margin-bottom: 20px;
    }
    .command-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.4rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        color: #F8FAFC;
        margin: 0;
    }
    .command-subtitle {
        font-size: 0.85rem;
        color: #94A3B8;
        margin: 2px 0 0 0;
    }
    .status-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        padding: 6px 12px;
        border-radius: 4px;
        font-weight: 600;
        letter-spacing: 1px;
    }
    .status-crisis {
        background-color: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid #EF4444;
    }
    .status-normal {
        background-color: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid #10B981;
    }

    .kpi-card {
        background-color: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 6px;
        padding: 16px 20px;
    }
    .kpi-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #94A3B8;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.8rem;
        font-weight: 700;
        color: #F8FAFC;
    }
    .kpi-delta-good { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #34D399; margin-top: 4px; }
    .kpi-delta-warn { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #FBBF24; margin-top: 4px; }
    .kpi-delta-bad { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #F87171; margin-top: 4px; }

    .protocol-box {
        background-color: #0F172A;
        border-left: 3px solid #38BDF8;
        border: 1px solid #1E293B;
        padding: 14px 18px;
        border-radius: 4px;
        margin-bottom: 12px;
    }
    .protocol-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        font-weight: 700;
        color: #38BDF8;
        margin-bottom: 4px;
    }
    .protocol-desc {
        font-size: 0.88rem;
        color: #CBD5E1;
        line-height: 1.45;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #0D1320;
        padding: 6px;
        border-radius: 6px;
        border: 1px solid #1E293B;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #94A3B8;
        border-radius: 4px;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E293B !important;
        color: #38BDF8 !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. NODES & MANIFEST DATA
# -----------------------------------------------------------------------------
NODES = {
    "Kanakapura Edu Hub (Exam Center)": {"lat": 12.5460, "lon": 77.4190, "type": "HUB", "status": "NOMINAL"},
    "Harohalli Sector": {"lat": 12.6780, "lon": 77.4410, "type": "VILLAGE", "status": "NOMINAL"},
    "Maralawadi Cluster": {"lat": 12.6150, "lon": 77.5120, "type": "VILLAGE", "status": "FLOODED"},
    "Sathanur South": {"lat": 12.4480, "lon": 77.3850, "type": "VILLAGE", "status": "NOMINAL"},
    "Kodihalli Creek": {"lat": 12.5120, "lon": 77.4890, "type": "VILLAGE", "status": "NOMINAL"},
    "Uyyamballi Outpost": {"lat": 12.4850, "lon": 77.3320, "type": "VILLAGE", "status": "NOMINAL"},
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
# 3. SIDEBAR CONTROLS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎛️ SCENARIO INJECTION")
    st.caption("Simulate live network disruptions to test autonomous fleet reallocation.")
    st.markdown("---")
    broken_buses = st.slider("Disabled Government Buses", 0, 4, 2)
    demand_surge_pct = st.slider("Exam Day Demand Surge (%)", 0, 80, 40, step=5)
    flood_corridor = st.selectbox(
        "Flooded / Blocked Corridor",
        ["None (All Clear)", "Maralawadi ↔ Edu Hub (Bridge Submerged)", "Harohalli ↔ Edu Hub (Landslide)"],
        index=1
    )
    deploy_micro_feeders = st.toggle("Deploy Local Auto/Van Feeders", value=True)
    
    st.markdown("---")
    st.markdown("### ⚙️ FLEET PARAMETERS")
    total_fleet = 8
    bus_capacity = 48
    st.markdown(f"""
    <div style='font-family: "JetBrains Mono", monospace; font-size: 0.8rem; color: #94A3B8;'>
    • BASE FLEET: {total_fleet} GOV BUSES<br>
    • SEAT CAP/BUS: {bus_capacity} PAX<br>
    • MICRO-FEEDER CAP: 6 PAX/UNIT<br>
    • SOLVER: GREEDY-KNAPSACK V2.4
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. SOLVER & LOGIC
# -----------------------------------------------------------------------------
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
feeder_seat_pool = (14 if deploy_micro_feeders else 0) * 6

def assign_transport(idx, row):
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
# 5. HEADER & KPIS
# -----------------------------------------------------------------------------
is_crisis = (broken_buses > 0) or (demand_surge_pct >= 25) or (affected_village is not None)
st.markdown(f"""
<div class="command-header">
    <div>
        <div class="command-title">ROUTELESS // AUTONOMOUS RURAL DISPATCH</div>
        <div class="command-subtitle">SECTOR: KANAKAPURA EDUCATION CLUSTER &nbsp;|&nbsp; WINDOW: EXAM WAVE 08:00–10:00 IST</div>
    </div>
    <div class="status-badge {'status-crisis' if is_crisis else 'status-normal'}">{'● ACTIVE CRISIS PROTOCOL' if is_crisis else '● NOMINAL OPERATIONS'}</div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Exam Candidate Coverage</div><div class="kpi-value">{exam_rescue_rate:.1f}%</div><div class="kpi-delta-good">{rescued_exam_students} / {total_exam_students} EXAMINEES SECURED</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Active Fleet Capacity</div><div class="kpi-value">{total_seated} <span style="font-size:1rem;color:#64748B;">/ {total_students}</span></div><div class="kpi-delta-warn">{active_buses} BUSES + FEEDERS</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Demand Surge Load</div><div class="kpi-value">+{demand_surge_pct}%</div><div class="kpi-delta-bad">{broken_buses} BUSES OFFLINE</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Wave-2 Deferred</div><div class="kpi-value">{unseated_count}</div><div class="kpi-delta-good">0 EXAM CANDIDATES STRANDED</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. TABS
# -----------------------------------------------------------------------------
tab_map, tab_manifest, tab_analytics, tab_comms = st.tabs([
    "🛰️ LIVE GEOSPATIAL TOPOLOGY",
    "📋 PRIORITY SEAT MANIFEST",
    "📊 CAPACITY & LOAD TELEMETRY",
    "📡 AUTOMATED DISPATCH COMMS"
])

with tab_map:
    col_map, col_intel = st.columns([2.2, 1])
    
    with col_map:
        map_df = pd.DataFrame([
            {"Name": k, "Lat": v["lat"], "Lon": v["lon"], "Type": v["type"], "Status": "SE
