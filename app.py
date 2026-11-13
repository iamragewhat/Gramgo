import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.graph_objects as go
from datetime import datetime, timedelta

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

    /* Global Dark Tactical Theme */
    .stApp {
        background-color: #080C14;
        color: #E2E8F0;
        font-family: 'Inter', sans-serif;
    }

    /* Hide default Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0D1320;
        border-right: 1px solid #1E293B;
    }

    /* Custom Top Command Header */
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

    /* KPI Telemetry Cards */
    .kpi-card {
        background-color: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 6px;
        padding: 16px 20px;
        transition: border-color 0.2s ease;
    }
    .kpi-card:hover {
        border-color: #38BDF8;
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
    .kpi-delta-good {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #34D399;
        margin-top: 4px;
    }
    .kpi-delta-warn {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #FBBF24;
        margin-top: 4px;
    }
    .kpi-delta-bad {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #F87171;
        margin-top: 4px;
    }

    /* Protocol Action Cards */
    .protocol-box {
        background-color: #0F172A;
        border-left: 3px solid #38BDF8;
        border-top: 1px solid #1E293B;
        border-right: 1px solid #1E293B;
        border-bottom: 1px solid #1E293B;
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

    /* Tabs Styling */
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
        border-bottom: none !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. GEOSPATIAL & SYNTHETIC NETWORK ENGINE
# -----------------------------------------------------------------------------
# Coordinates modeled around a rural cluster outside Bengaluru (Kanakapura sector)
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
        dist_km = {
            "Harohalli Sector": 16.4,
            "Maralawadi Cluster": 14.8,
            "Sathanur South": 12.2,
            "Kodihalli Creek": 9.5,
            "Uyyamballi Outpost": 15.1
        }[v]
        
        records.append({
            "Student_ID": f"RTL-{2026000 + i}",
            "Name": f"Student_{i:03d}",
            "Origin_Village": v,
            "Exam_Candidate": is_exam,
            "Minutes_To_Gate_Close": exam_mins,
            "Distance_KM": dist_km,
            "Special_Needs": np.random.choice([True, False], p=[0.05, 0.95])
        })
    return pd.DataFrame(records)

# -----------------------------------------------------------------------------
# 3. SIDEBAR: CRISIS INJECTION & DISPATCH PARAMETERS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎛️ SCENARIO INJECTION")
    st.caption("Simulate live network disruptions to test autonomous fleet reallocation.")
    
    st.markdown("---")
    broken_buses = st.slider("Disabled Government Buses", 0, 4, 2, help="Number of state buses offline due to mechanical failure.")
    demand_surge_pct = st.slider("Exam Day Demand Surge (%)", 0, 80, 40, step=5, help="Unexpected spike in student ridership.")
    flood_corridor = st.selectbox(
        "Flooded / Blocked Corridor",
        ["None (All Clear)", "Maralawadi ↔ Edu Hub (Bridge Submerged)", "Harohalli ↔ Edu Hub (Landslide)"],
        index=1
    )
    deploy_micro_feeders = st.toggle("Deploy Local Auto/Van Feeders", value=True, help="Authorize emergency contracts with local 6-seater micro-transit.")
    
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
# 4. CORE ALGORITHMIC SOLVER (OPTIMIZATION & REROUTING)
# -----------------------------------------------------------------------------
base_df = generate_base_manifest()

# 1. Apply Demand Surge
if demand_surge_pct > 0:
    n_extra = int(len(base_df) * (demand_surge_pct / 100.0))
    surge_sample = base_df.sample(n=n_extra, replace=True, random_state=99).copy()
    surge_sample["Student_ID"] = [f"RTL-SRG-{i:03d}" for i in range(1, n_extra + 1)]
    # Surge skews heavily toward exam candidates
    surge_sample["Exam_Candidate"] = np.random.choice([True, False], size=n_extra, p=[0.65, 0.35])
    surge_sample["Minutes_To_Gate_Close"] = np.where(surge_sample["Exam_Candidate"], np.random.choice([50, 85, 115], size=n_extra), 360)
    df = pd.concat([base_df, surge_sample], ignore_index=True)
else:
    df = base_df.copy()

# 2. Evaluate Corridor Disruption
affected_village = None
if "Maralawadi" in flood_corridor:
    affected_village = "Maralawadi Cluster"
elif "Harohalli" in flood_corridor:
    affected_village = "Harohalli Sector"

df["Corridor_Status"] = np.where(
    df["Origin_Village"] == affected_village,
    "REROUTED (+18m Bypass via Kodihalli)",
    "NOMINAL (Direct Corridor)"
)

# 3. Compute Multi-Factor Criticality Index (0 - 100)
# Urgency increases non-linearly as exam gate closure approaches
urgency_score = np.where(
    df["Exam_Candidate"],
    np.clip(100 - (df["Minutes_To_Gate_Close"] * 0.45), 45, 95),
    15
)
isolation_bonus = np.where(df["Origin_Village"] == affected_village, 12, 0)
access_bonus = np.where(df["Special_Needs"], 15, 0)
distance_weight = (df["Distance_KM"] / 20.0) * 10

df["Criticality_Index"] = np.round(np.clip(urgency_score + isolation_bonus + access_bonus + distance_weight, 0, 100), 1)
df = df.sort_values(by=["Criticality_Index", "Minutes_To_Gate_Close"], ascending=[False, True]).reset_index(drop=True)

# 4. Dynamic Fleet & Micro-Transit Allocation
active_buses = max(1, total_fleet - broken_buses)
primary_seat_pool = active_buses * bus_capacity
feeder_units = 14 if deploy_micro_feeders else 0
feeder_seat_pool = feeder_units * 6

def assign_transport(idx, row):
    if idx < primary_seat_pool:
        bus_num = (idx // bus_capacity) + 1
        if row["Origin_Village"] == affected_village:
            return f"GOV-BUS-0{bus_num} (Detour Alpha)"
        return f"GOV-BUS-0{bus_num} (Express)"
    elif idx < (primary_seat_pool + feeder_seat_pool):
        feeder_num = ((idx - primary_seat_pool) // 6) + 1
        return f"FEEDER-AUTO-{feeder_num:02d}"
    else:
        return "DEFERRED / WAVE-2 STANDBY"

df["Assigned_Unit"] = [assign_transport(i, r) for i, r in df.iterrows()]
df["ETA_Margin_Mins"] = np.where(
    df["Assigned_Unit"].str.contains("DEFERRED"),
    -45,
    np.where(df["Origin_Village"] == affected_village, 14, 28)
)

# Metrics Summary
total_students = len(df)
exam_students = df
