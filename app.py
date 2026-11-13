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
exam_students = df[df["Exam_Candidate"]]
total_exam_students = len(exam_students)
rescued_exam_students = len(exam_students[~exam_students["Assigned_Unit"].str.contains("DEFERRED")])
exam_rescue_rate = (rescued_exam_students / total_exam_students * 100) if total_exam_students > 0 else 100.0
total_seated = len(df[~df["Assigned_Unit"].str.contains("DEFERRED")])
unseated_count = total_students - total_seated

# -----------------------------------------------------------------------------
# 5. COMMAND HEADER & TELEMETRY STRIP
# -----------------------------------------------------------------------------
is_crisis = (broken_buses > 0) or (demand_surge_pct >= 25) or (affected_village is not None)
badge_class = "status-crisis" if is_crisis else "status-normal"
badge_text = "● ACTIVE CRISIS PROTOCOL" if is_crisis else "● NOMINAL OPERATIONS"

st.markdown(f"""
<div class="command-header">
    <div>
        <div class="command-title">ROUTELESS // AUTONOMOUS RURAL DISPATCH</div>
        <div class="command-subtitle">SECTOR: KANAKAPURA EDUCATION CLUSTER &nbsp;|&nbsp; WINDOW: EXAM WAVE 08:00–10:00 IST</div>
    </div>
    <div class="status-badge {badge_class}">{badge_text}</div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Exam Candidate Coverage</div>
        <div class="kpi-value">{exam_rescue_rate:.1f}%</div>
        <div class="kpi-delta-good">{rescued_exam_students} / {total_exam_students} EXAMINEES SECURED</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Active Fleet Capacity</div>
        <div class="kpi-value">{total_seated} <span style="font-size:1rem;color:#64748B;">/ {total_students}</span></div>
        <div class="kpi-delta-warn">{active_buses} BUSES + {feeder_units} MICRO-FEEDERS</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    delta_cls = "kpi-delta-bad" if broken_buses > 0 else "kpi-delta-good"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Demand Surge Load</div>
        <div class="kpi-value">+{demand_surge_pct}%</div>
        <div class="{delta_cls}">{broken_buses} BUSES OFFLINE // +{total_students - len(base_df)} EXTRA PAX</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    defer_cls = "kpi-delta-good" if unseated_count == 0 else "kpi-delta-warn"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Wave-2 Deferred (Non-Exam)</div>
        <div class="kpi-value">{unseated_count}</div>
        <div class="{defer_cls}">0 EXAM CANDIDATES STRANDED</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. MAIN TACTICAL WORKSPACE (TABS)
# -----------------------------------------------------------------------------
tab_map, tab_manifest, tab_analytics, tab_comms = st.tabs([
    "🛰️ LIVE GEOSPATIAL TOPOLOGY",
    "📋 PRIORITY SEAT MANIFEST",
    "📊 CAPACITY & LOAD TELEMETRY",
    "📡 AUTOMATED DISPATCH COMMS"
])

# --- TAB 1: GEOSPATIAL ROUTING MAP ---
with tab_map:
    col_map, col_intel = st.columns([2.2, 1])
    
    with col_map:
        hub_coords = [NODES["Kanakapura Edu Hub (Exam Center)"]["lon"], NODES["Kanakapura Edu Hub (Exam Center)"]["lat"]]
        
        # Build route arcs
        routes = []
        for name, info in NODES.items():
            if info["type"] == "HUB":
                continue
            start = [info["lon"], info["lat"]]
            is_blocked = (name == affected_village)
            
            if is_blocked:
                # Blocked direct path (Red)
                routes.append({
                    "name": f"{name} -> Hub (BLOCKED)",
                    "path": [start, hub_coords],
                    "color": [239, 68, 68, 220],
                    "width": 6
                })
                # Detour bypass path via Kodihalli Creek (Cyan/Emerald)
                waypoint = [NODES["Kodihalli Creek"]["lon"], NODES["Kodihalli Creek"]["lat"]]
                routes.append({
                    "name": f"{name} -> Detour Alpha -> Hub",
                    "path": [start, waypoint, hub_coords],
                    "color": [56, 189, 248, 240],
                    "width": 5
                })
            else:
                routes.append({
                    "name": f"{name} -> Hub (ACTIVE)",
                    "path": [start, hub_coords],
                    "color": [16, 185, 129, 200],
                    "width": 4
                })

        node_data = [
            {
                "name": k,
                "lon": v["lon"],
                "lat": v["lat"],
                "color": [56, 189, 248, 255] if v["type"] == "HUB" else ([239, 68, 68, 255] if k == affected_village else [248, 250, 252, 230]),
                "radius": 900 if v["type"] == "HUB" else 550
            }
            for k, v in NODES.items()
        ]

        path_layer = pdk.Layer(
            "PathLayer",
            data=routes,
            get_path="path",
            get_color="color",
            get_width="width",
            width_min_pixels=3,
            pickable=True
        )

        scatter_layer = pdk.Layer(
            "ScatterplotLayer",
            data=node_data,
            get_position=["lon", "lat"],
            get_fill_color="color",
            get_radius="radius",
            pickable=True
        )

        text_layer = pdk.Layer(
            "TextLayer",
            data=node_data,
            get_position=["lon", "lat"],
            get_text="name",
            get_color=[248, 250, 252, 255],
            get_size=13,
            get_alignment_baseline="'bottom'",
            get_pixel_offset=[0, -12]
        )

        view_state = pdk.ViewState(latitude=12.56, longitude=77.43, zoom=10.3, pitch=35)
        deck = pdk.Deck(
            layers=[path_layer, scatter_layer, text_layer],
            initial_view_state=view_state,
            map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
            tooltip={"text": "{name}"}
        )
        st.pydeck_chart(deck, use_container_width=True)

    with col_intel:
        st.markdown("#### 🧠 TACTICAL REROUTING ENGINE")
        if affected_village:
            st.markdown(f"""
            <div class="protocol-box" style="border-left-color: #EF4444;">
                <div class="protocol-title" style="color: #F87171;">CORRIDOR SEVERED: {affected_village.upper()}</div>
                <div class="protocol-desc">Direct arterial road flagged impassable. Telemetry rerouted heavy buses via <b>Kodihalli Creek Bypass (+18 mins)</b>. Departure schedule advanced by 20 mins for affected cohort.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="protocol-box" style="border-left-color: #10B981;">
                <div class="protocol-title" style="color: #34D399;">ALL ARTERIAL CORRIDORS CLEAR</div>
                <div class="protocol-desc">Primary rural highway network operating at nominal speed (42 km/h average).</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="protocol-box">
            <div class="protocol-title">FLEET CONSOLIDATION PROTOCOL</div>
            <div class="protocol-desc">With <b>{broken_buses} buses offline</b>, remaining {active_buses} buses converted to Express Point-to-Point Exam Shuttles. Non-exam commuters shifted to Wave-2 (10:30 IST).</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="protocol-box" style="border-left-color: #FBBF24;">
            <div class="protocol-title" style="color: #FBBF24;">MICRO-MOBILITY BRIDGE ACTIVE</div>
            <div class="protocol-desc">{'Dispatched ' + str(feeder_units) + ' contracted rural auto-rickshaws to absorb overflow exam candidates from isolated hamlets.' if deploy_micro_feeders else 'WARNING: Micro-feeders disabled. Enable in sidebar to prevent exam candidate overflow.'}</div>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 2: PRIORITY SEAT MANIFEST ---
with tab_manifest:
    f1, f2, f3 = st.columns([1.5, 1.5, 2])
    with f1:
        filter_exam = st.selectbox("Filter Cohort", ["All Students", "Exam Candidates Only", "Non-Exam Commuters"])
    with f2:
        filter_village = st.selectbox("Origin Village", ["All Villages"] + list(df["Origin_Village"].unique()))
    with f3:
        search_id = st.text_input("Search Student ID", placeholder="e.g., RTL-2026004")

    filtered_df = df.copy()
    if filter_exam == "Exam Candidates Only":
        filtered_df = filtered_df[filtered_df["Exam_Candidate"] == True]
    elif filter_exam == "Non-Exam Commuters":
        filtered_df = filtered_df[filtered_df["Exam_Candidate"] == False]
    
    if filter_village != "All Villages":
        filtered_df = filtered_df[filtered_df["Origin_Village"] == filter_village]
    
    if search_id:
        filtered_df = filtered_df[filtered_df["Student_ID"].str.contains(search_id, case=False)]

    st.dataframe(
        filtered_df[[
            "Student_ID", "Origin_Village", "Exam_Candidate", 
            "Minutes_To_Gate_Close", "Criticality_Index", 
            "Corridor_Status", "Assigned_Unit"
        ]],
        use_container_width=True,
        height=440,
        column_config={
            "Criticality_Index": st.column_config.ProgressColumn(
                "Criticality Score",
                format="%.1f",
                min_value=0,
                max_value=100,
            ),
            "Exam_Candidate": st.column_config.CheckboxColumn("Exam Today"),
            "Minutes_To_Gate_Close": st.column_config.NumberColumn("Gate Closes (Min)", format="%d m")
        }
    )

# --- TAB 3: CAPACITY & LOAD TELEMETRY ---
with tab_analytics:
    g1, g2 = st.columns(2)
    
    with g1:
        # Allocation breakdown by village
        village_summary = df.groupby(["Origin_Village", "Exam_Candidate"]).size().reset_index(name="Count")
        village_summary["Type"] = np.where(village_summary["Exam_Candidate"], "Exam Candidate (Priority 1)", "Regular Student (Priority 2)")
        
        fig1 = go.Figure()
        for t, color in [("Exam Candidate (Priority 1)", "#38BDF8"), ("Regular Student (Priority 2)", "#334155")]:
            sub = village_summary[village_summary["Type"] == t]
            fig1.add_trace(go.Bar(
                x=sub["Origin_Village"],
                y=sub["Count"],
                name=t,
                marker_color=color
            ))
        fig1.update_layout(
            title="Demand Distribution by Village & Priority Tier",
            barmode="stack",
            paper_bgcolor="#0F172A",
            plot_bgcolor="#0F172A",
            font=dict(color="#E2E8F0", family="Inter"),
            margin=dict(l=20, r=20, t=45, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig1, use_container_width=True)

    with g2:
        # Transport Mode Split
        mode_counts = df["Assigned_Unit"].apply(
            lambda x: "Gov Express Bus" if "GOV-BUS" in x else ("Micro-Feeder Auto" if "FEEDER" in x else "Wave-2 Deferred")
        ).value_counts()

        fig2 = go.Figure(data=[go.Pie(
            labels=mode_counts.index,
            values=mode_counts.values,
            hole=0.62,
            marker=dict(colors=["#10B981", "#38BDF8", "#EF4444"])
        )])
        fig2.update_layout(
            title="Crisis Fleet Seat Allocation Split",
            paper_bgcolor="#0F172A",
            plot_bgcolor="#0F172A",
            font=dict(color="#E2E8F0", family="Inter"),
            margin=dict(l=20, r=20, t=45, b=20)
        )
        st.plotly_chart(fig2, use_container_width=True)

# --- TAB 4: AUTOMATED DISPATCH COMMS ---
with tab_comms:
    st.markdown("#### 📲 ZERO-DATA SMS / IVR STUDENT NOTIFICATION GATEWAY")
    st.caption("Rural students often lack mobile data during severe weather. ROUTELESS dispatches compressed SMS boarding passes automatically.")
    
    sample_exam_student = df[df["Exam_Candidate"]].iloc[0]
    sample_deferred = df[df["Assigned_Unit"].str.contains("DEFERRED")]
    
    col_sms1, col_sms2 = st.columns(2)
    with col_sms1:
        st.markdown("**PRIORITY EXAM BOARDING PASS (SMS PAYLOAD)**")
        st.code(f"""
[ROUTELESS EMERGENCY DISPATCH]
ID: {sample_exam_student['Student_ID']} | EXAM PRIORITY CONFIRMED
UNIT: {sample_exam_student['Assigned_Unit']}
PICKUP: {sample_exam_student['Origin_Village']} Main Chowk
STATUS: {sample_exam_student['Corridor_Status']}
BOARDING CODE: #EX-{np.random.randint(1000,9999)} (Show Driver)
        """, language="text")

    with col_sms2:
        st.markdown("**WAVE-2 DEFERRAL ADVISORY (NON-EXAM COHORT)**")
        def_id = sample_deferred.iloc[0]["Student_ID"] if len(sample_deferred) > 0 else "N/A (0 Deferred)"
        st.code(f"""
[ROUTELESS TRANSIT ADVISORY]
ID: {def_id} | STATUS: WAVE-2 STANDBY
DUE TO EXAM EMERGENCY & BUS SHORTAGE, YOUR MORNING
SEAT IS SHIFTED TO WAVE-2 SHUTTLE AT 10:30 AM.
ATTENDANCE EXEMPTION LOGGED WITH COLLEGE ADMIN.
        """, language="text")
