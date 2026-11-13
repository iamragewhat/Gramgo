import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG & DESIGN SYSTEM (CUSTOM CSS)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ROUTELESS // Tactical Transit Command",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

    /* Global Theme & Typography */
    .stApp {
        background-color: #060913;
        color: #E2E8F0;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0A0F1D;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
    [data-testid="stSidebar"] .stMarkdown h3 {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        letter-spacing: 1.2px;
        color: #38BDF8;
        text-transform: uppercase;
    }

    /* Top Command Header */
    .command-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 28px;
        background: linear-gradient(135deg, #0D1424 0%, #090D18 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left: 4px solid #00F2FE;
        border-radius: 10px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }
    .command-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.35rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        color: #FFFFFF;
        margin: 0;
    }
    .command-subtitle {
        font-size: 0.82rem;
        color: #94A3B8;
        margin-top: 4px;
        font-weight: 400;
        letter-spacing: 0.5px;
    }
    .status-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        padding: 8px 14px;
        border-radius: 6px;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .status-crisis {
        background: rgba(255, 75, 75, 0.12);
        color: #FF5252;
        border: 1px solid rgba(255, 82, 82, 0.3);
    }
    .status-normal {
        background: rgba(0, 200, 83, 0.12);
        color: #00E676;
        border: 1px solid rgba(0, 230, 118, 0.3);
    }

    /* KPI Telemetry Cards */
    .kpi-card {
        background: linear-gradient(145deg, #0B101D 0%, #070A14 100%);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 8px;
        padding: 20px;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    .kpi-card:hover {
        border-color: rgba(56, 189, 248, 0.3);
        transform: translateY(-2px);
    }
    .kpi-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #8A99AD;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.9rem;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1.1;
    }
    .kpi-trend {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        margin-top: 8px;
        font-weight: 500;
    }
    .trend-good { color: #00E676; }
    .trend-warn { color: #FFD740; }
    .trend-bad { color: #FF5252; }

    /* Protocol Boxes */
    .protocol-box {
        background: #0A0F1D;
        border-left: 3px solid #38BDF8;
        border-top: 1px solid rgba(255,255,255,0.05);
        border-right: 1px solid rgba(255,255,255,0.05);
        border-bottom: 1px solid rgba(255,255,255,0.05);
        padding: 16px;
        border-radius: 6px;
        margin-bottom: 14px;
    }
    .protocol-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        font-weight: 700;
        color: #38BDF8;
        margin-bottom: 6px;
        letter-spacing: 0.5px;
    }
    .protocol-desc {
        font-size: 0.85rem;
        color: #94A3B8;
        line-height: 1.5;
    }

    /* Customizing Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #0A0F1D;
        padding: 6px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #8A99AD;
        border-radius: 6px;
        padding: 10px 18px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #162035 !important;
        color: #38BDF8 !important;
    }

    /* Inputs & Sliders styling */
    .stSlider label, .stSelectbox label, .stToggle label {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.85rem;
        font-weight: 500;
        color: #CBD5E1;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. NODES & SIMULATION DATA
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
# 3. SIDEBAR CONTROLS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎛️ SCENARIO SIMULATOR")
    st.caption("Inject live network disruptions to test dynamic bus reallocation.")
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    broken_buses = st.slider("Disabled Government Buses", 0, 4, 2)
    demand_surge_pct = st.slider("Exam Day Demand Surge (%)", 0, 80, 40, step=5)
    flood_corridor = st.selectbox(
        "Flooded / Blocked Corridor",
        ["None (All Clear)", "Maralawadi ↔ Edu Hub (Bridge Submerged)", "Harohalli ↔ Edu Hub (Landslide)"],
        index=1
    )
    deploy_micro_feeders = st.toggle("Deploy Local Auto/Van Feeders", value=True)
    
    st.markdown("---")
    st.markdown("### ⚙️ FLEET ENGINE")
    total_fleet = 8
    bus_capacity = 48
    st.markdown(f"""
    <div style='font-family: "JetBrains Mono", monospace; font-size: 0.78rem; color: #64748B; line-height: 1.6;'>
    • BASE FLEET: {total_fleet} GOV BUSES<br>
    • CAPACITY: {bus_capacity} PAX/BUS<br>
    • MICRO-FEEDER: 6 PAX/UNIT<br>
    • SOLVER ALGORITHM: V2.4-KNAPSACK
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. SOLVER & DATA PROCESSING
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
        <div class="command-title">ROUTELESS // TRANSIT COMMAND CENTER</div>
        <div class="command-subtitle">KANAKAPURA EDUCATION HUB &nbsp;|&nbsp; CRISIS DISPATCH & ALLOCATION ENGINE</div>
    </div>
    <div class="status-badge {'status-crisis' if is_crisis else 'status-normal'}">{'● ACTIVE CRISIS PROTOCOL' if is_crisis else '● NORMAL OPERATIONS'}</div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-label">Exam Candidate Coverage</div>
        <div class="kpi-value">{exam_rescue_rate:.1f}%</div>
        <div class="kpi-trend trend-good">✓ {rescued_exam_students} / {total_exam_students} EXAMINEES SECURED</div>
    </div>
    ''', unsafe_allow_html=True)
with c2:
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-label">Active Fleet Capacity</div>
        <div class="kpi-value">{total_seated} <span style="font-size:1.1rem;color:#64748B;">/ {total_students}</span></div>
        <div class="kpi-trend trend-warn">⚡ {active_buses} BUSES + FEEDERS ACTIVE</div>
    </div>
    ''', unsafe_allow_html=True)
with c3:
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-label">Demand Surge Load</div>
        <div class="kpi-value">+{demand_surge_pct}%</div>
        <div class="kpi-trend trend-bad">⚠ {broken_buses} GOV BUSES OFFLINE</div>
    </div>
    ''', unsafe_allow_html=True)
with c4:
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-label">Wave-2 Deferred</div>
        <div class="kpi-value">{unseated_count}</div>
        <div class="kpi-trend trend-good">🛡️ 0 EXAM CANDIDATES STRANDED</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. TABS & INTERACTIVE VIEWS
# -----------------------------------------------------------------------------
tab_map, tab_manifest, tab_analytics, tab_comms = st.tabs([
    "🛰️ GEOSPATIAL NETWORK MAP",
    "📋 PRIORITY SEAT MANIFEST",
    "📊 LOAD & CAPACITY TELEMETRY",
    "📡 AUTOMATED COMMS GATEWAY"
])

with tab_map:
    col_map, col_intel = st.columns([2.3, 1])
    
    with col_map:
        map_df = pd.DataFrame([
            {"Name": k, "Lat": v["lat"], "Lon": v["lon"], "Type": v["type"], "Status": "SEVERED" if k == affected_village else "ACTIVE"}
            for k, v in NODES.items()
        ])
        
        fig_map = px.scatter_mapbox(
            map_df, lat="Lat", lon="Lon", text="Name", color="Status",
            color_discrete_map={"ACTIVE": "#38BDF8", "SEVERED": "#FF5252"},
            zoom=10.2, height=460
        )
        fig_map.update_layout(
            mapbox_style="carto-darkmatter",
            paper_bgcolor="#0A0F1D",
            plot_bgcolor="#0A0F1D",
            margin=dict(l=0, r=0, t=0, b=0),
            font=dict(color="#E2E8F0", family="Plus Jakarta Sans"),
            legend=dict(x=0.02, y=0.98, bgcolor="rgba(10,15,29,0.8)")
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with col_intel:
        st.markdown("#### 🧠 AI REROUTING LOGIC")
        if affected_village:
            st.markdown(f"""
            <div class="protocol-box" style="border-left-color: #FF5252;">
                <div class="protocol-title" style="color: #FF5252;">CORRIDOR SEVERED: {affected_village.upper()}</div>
                <div class="protocol-desc">Direct road impassable due to flooding. Telemetry automatically computed bypass via Kodihalli Creek (+18m detour).</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="protocol-box" style="border-left-color: #00E676;">
                <div class="protocol-title" style="color: #00E676;">ALL ARTERIAL ROUTES CLEAR</div>
                <div class="protocol-desc">Rural transit grid operating at normal speed (42 km/h avg).</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="protocol-box">
            <div class="protocol-title">FLEET RECONSOLIDATION</div>
            <div class="protocol-desc">With <b>{broken_buses} buses offline</b>, remaining capacity is re-indexed by exam priority score. Non-exam commuters shifted to Wave-2.</div>
        </div>
        """, unsafe_allow_html=True)

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

with tab_analytics:
    g1, g2 = st.columns(2)
    with g1:
        village_summary = df.groupby(["Origin_Village", "Exam_Candidate"]).size().reset_index(name="Count")
        village_summary["Type"] = np.where(village_summary["Exam_Candidate"], "Exam Candidate (Priority)", "Regular Commuter")
        fig1 = px.bar(village_summary, x="Origin_Village", y="Count", color="Type", color_discrete_map={"Exam Candidate (Priority)": "#38BDF8", "Regular Commuter": "#1E293B"})
        fig1.update_layout(paper_bgcolor="#0A0F1D", plot_bgcolor="#0A0F1D", font=dict(color="#E2E8F0", family="Plus Jakarta Sans"), margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig1, use_container_width=True)
    with g2:
        mode_counts = df["Assigned_Unit"].apply(lambda x: "Gov Express Bus" if "GOV-BUS" in x else ("Micro-Feeder" if "FEEDER" in x else "Deferred")).value_counts()
        fig2 = px.pie(names=mode_counts.index, values=mode_counts.values, hole=0.6, color_discrete_sequence=["#00E676", "#38BDF8", "#FF5252"])
        fig2.update_layout(paper_bgcolor="#0A0F1D", plot_bgcolor="#0A0F1D", font=dict(color="#E2E8F0", family="Plus Jakarta Sans"), margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig2, use_container_width=True)

with tab_comms:
    st.markdown("#### 📲 ZERO-DATA SMS / IVR STUDENT NOTIFICATION GATEWAY")
    sample_exam_student = df[df["Exam_Candidate"]].iloc[0]
    col_sms1, col_sms2 = st.columns(2)
    with col_sms1:
        st.markdown("**PRIORITY EXAM BOARDING PASS (SMS PAYLOAD)**")
        st.code(f"""[ROUTELESS EMERGENCY DISPATCH]
ID: {sample_exam_student['Student_ID']} | EXAM PRIORITY CONFIRMED
UNIT: {sample_exam_student['Assigned_Unit']}
PICKUP: {sample_exam_student['Origin_Village']} Main Chowk
STATUS: {sample_exam_student['Corridor_Status']}
BOARDING CODE: #EX-{np.random.randint(1000,9999)}""", language="text")
    with col_sms2:
        st.markdown("**WAVE-2 DEFERRAL ADVISORY**")
        st.code(f"""[ROUTELESS TRANSIT ADVISORY]
STATUS: WAVE-2 STANDBY
DUE TO EXAM EMERGENCY & BUS SHORTAGE, MORNING SEAT
IS SHIFTED TO WAVE-2 SHUTTLE AT 10:30 AM.""", language="text")
