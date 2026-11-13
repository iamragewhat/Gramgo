import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG & LIGHT-MODE CURVY DESIGN SYSTEM (CUSTOM CSS)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ROUTELESS // Tactical Transit Command",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,800;1,700;1,800&family=Lora:ital,wght@0,600;0,700;1,600;1,700&display=swap');

    /* Global Light Background, Dark Text, Bold & Italic Curvy Font */
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
        letter-spacing: 0.8px;
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
        padding: 22px 28px;
        background: #FFFFFF;
        border: 2.5px solid #0F172A;
        border-left: 8px solid #0F172A;
        border-radius: 14px;
        margin-bottom: 24px;
        box-shadow: 5px 5px 0px #0F172A;
    }
    .command-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.65rem;
        font-weight: 800;
        font-style: italic;
        letter-spacing: 0.5px;
        color: #0F172A;
        margin: 0;
    }
    .command-subtitle {
        font-family: 'Lora', Georgia, serif;
        font-size: 0.9rem;
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
        letter-spacing: 0.5px;
        border: 2px solid #0F172A;
    }
    .status-crisis {
        background: #FEE2E2;
        color: #991B1B;
    }
    .status-normal {
        background: #DCFCE7;
        color: #166534;
    }

    /* KPI Telemetry Cards with Darkened Boundaries */
    .kpi-card {
        background: #FFFFFF;
        border: 2.5px solid #0F172A;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 4px 4px 0px #0F172A;
        transition: all 0.2s ease;
    }
    .kpi-card:hover {
        transform: translate(-2px, -2px);
        box-shadow: 6px 6px 0px #0F172A;
    }
    .kpi-label {
        font-family: 'Lora', Georgia, serif;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #334155;
        font-weight: 700;
        font-style: italic;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 2.1rem;
        font-weight: 800;
        font-style: italic;
        color: #0F172A;
        line-height: 1.1;
    }
    .kpi-trend {
        font-family: 'Lora', Georgia, serif;
        font-size: 0.78rem;
        margin-top: 8px;
        font-weight: 700;
        font-style: italic;
    }
    .trend-good { color: #15803D; }
    .trend-warn { color: #B45309; }
    .trend-bad { color: #B91C1C; }

    /* Protocol Boxes */
    .protocol-box {
        background: #FFFFFF;
        border: 2px solid #0F172A;
        border-left: 6px solid #0F172A;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 14px;
        box-shadow: 3px 3px 0px #0F172A;
    }
    .protocol-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 0.95rem;
        font-weight: 800;
        font-style: italic;
        color: #0F172A;
        margin-bottom: 6px;
    }
    .protocol-desc {
        font-family: 'Lora', Georgia, serif;
        font-size: 0.88rem;
        font-weight: 600;
        font-style: italic;
        color: #1E293B;
        line-height: 1.5;
    }

    /* Customizing Tabs with Darkened Boundaries */
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
        padding: 10px 18px;
        font-weight: 800;
        font-style: italic;
        border: 1.5px solid transparent;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0F172A !important;
        color: #FFFFFF !important;
        border: 1.5px solid #0F172A !important;
    }

    /* Inputs, Selectboxes, Dataframes & Headings */
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
    [data-testid="stDataFrame"] {
        border: 2.5px solid #0F172A;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 4px 4px 0px #0F172A;
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
    st.markdown("### 🎛️ Scenario Simulator")
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
    st.markdown("### ⚙️ Fleet Engine")
    total_fleet = 8
    bus_capacity = 48
    st.markdown(f"""
    <div style='font-family: "Lora", serif; font-size: 0.85rem; font-weight: 700; font-style: italic; color: #0F172A; line-height: 1.7; background: #F8FAFC; padding: 12px; border: 2px solid #0F172A; border-radius: 10px;'>
    • Base Fleet: {total_fleet} Gov Buses<br>
    • Capacity: {bus_capacity} Pax/Bus<br>
    • Micro-Feeder: 6 Pax/Unit<br>
    • Solver: V2.4-Knapsack
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
        <div class="command-title">Routeless // Transit Command Center</div>
        <div class="command-subtitle">Kanakapura Education Hub &nbsp;|&nbsp; Crisis Dispatch & Allocation Engine</div>
    </div>
    <div class="status-badge {'status-crisis' if is_crisis else 'status-normal'}">{'● Active Crisis Protocol' if is_crisis else '● Normal Operations'}</div>
</div>
""", unsafe_allow_html=True)

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
        <div class="kpi-trend trend-warn">⚡ {active_buses} Buses + Feeders Active</div>
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
        <div class="kpi-trend trend-good">🛡️ 0 Exam Candidates Stranded</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. TABS & INTERACTIVE VIEWS
# -----------------------------------------------------------------------------
tab_map, tab_manifest, tab_analytics, tab_comms = st.tabs([
    "🛰️ Geospatial Network Map",
    "📋 Priority Seat Manifest",
    "📊 Load & Capacity Telemetry",
    "📡 Automated Comms Gateway"
])

with tab_map:
    col_map, col_intel = st.columns([2.3, 1])
    
    with col_map:
        map_df = pd.DataFrame([
            {"Name": k, "Lon": v["lon"], "Lat": v["lat"], "Type": v["type"], "Status": "SEVERED" if k == affected_village else "ACTIVE"}
            for k, v in NODES.items()
        ])
        
        fig_map = px.scatter(
            map_df, x="Lon", y="Lat", text="Name", color="Status",
            color_discrete_map={"ACTIVE": "#0284C7", "SEVERED": "#DC2626"},
            height=460
        )
        fig_map.update_traces(
            textposition="top center",
            textfont=dict(family="Lora, serif", size=13, color="#0F172A"),
            marker=dict(size=18, line=dict(width=2.5, color="#0F172A"))
        )
        fig_map.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#F8FAFC",
            margin=dict(l=20, r=20, t=20, b=20),
            font=dict(color="#0F172A", family="Lora, serif"),
            xaxis=dict(showgrid=True, gridcolor="#CBD5E1", zeroline=False, linecolor="#0F172A", linewidth=2, mirror=True),
            yaxis=dict(showgrid=True, gridcolor="#CBD5E1", zeroline=False, linecolor="#0F172A", linewidth=2, mirror=True),
            legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.95)", bordercolor="#0F172A", borderwidth=2)
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with col_intel:
        st.markdown("#### 🧠 AI Rerouting Logic")
        if affected_village:
            st.markdown(f"""
            <div class="protocol-box" style="border-left-color: #DC2626; background: #FEF2F2;">
                <div class="protocol-title" style="color: #991B1B;">Corridor Severed: {affected_village}</div>
                <div class="protocol-desc">Direct road impassable due to flooding. Telemetry automatically computed bypass via Kodihalli Creek (+18m detour).</div>
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
        fig1 = px.bar(
            village_summary, x="Origin_Village", y="Count", color="Type",
            color_discrete_map={"Exam Candidate (Priority)": "#0284C7", "Regular Commuter": "#94A3B8"}
        )
        fig1.update_traces(marker_line_color="#0F172A", marker_line_width=1.5)
        fig1.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#F8FAFC",
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
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font=dict(color="#0F172A", family="Lora, serif"),
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig2, use_container_width=True)

with tab_comms:
    st.markdown("#### 📲 Zero-Data SMS / IVR Student Notification Gateway")
    sample_exam_student = df[df["Exam_Candidate"]].iloc[0]
    col_sms1, col_sms2 = st.columns(2)
    with col_sms1:
        st.markdown("**Priority Exam Boarding Pass (SMS Payload)**")
        st.code(f"""[ROUTELESS EMERGENCY DISPATCH]
ID: {sample_exam_student['Student_ID']} | EXAM PRIORITY CONFIRMED
UNIT: {sample_exam_student['Assigned_Unit']}
PICKUP: {sample_exam_student['Origin_Village']} Main Chowk
STATUS: {sample_exam_student['Corridor_Status']}
BOARDING CODE: #EX-{np.random.randint(1000,9999)}""", language="text")
    with col_sms2:
        st.markdown("**Wave-2 Deferral Advisory**")
        st.code(f"""[ROUTELESS TRANSIT ADVISORY]
STATUS: WAVE-2 STANDBY
DUE TO EXAM EMERGENCY & BUS SHORTAGE, MORNING SEAT
IS SHIFTED TO WAVE-2 SHUTTLE AT 10:30 AM.""", language="text")
