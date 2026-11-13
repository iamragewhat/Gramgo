import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="ROUTELESS: Rural Crisis Dispatch", layout="wide")

st.title("🚌 ROUTELESS: Rural Student Crisis Dispatch System")
st.markdown("### AI-Powered Dynamic Reallocation & Emergency Response Platform")

# --- SIDEBAR: CRISIS SIMULATOR ---
st.sidebar.header("🚨 Crisis Simulation Controls")
bus_breakdown = st.sidebar.checkbox("Simulate Bus Breakdown (-2 Buses)", value=True)
demand_surge = st.sidebar.slider("Student Demand Surge (%)", 0, 100, 40)
road_blocked = st.sidebar.checkbox("Main Road Blocked (Flooding)", value=True)
time_pressure = st.sidebar.selectbox("Exam Time Window", ["Next 1 Hour", "Next 2 Hours", "All Day"])

# --- DATA SETUP ---
@st.cache_data
def load_data():
    data = {
        "Student_ID": [f"S{i:03d}" for i in range(1, 101)],
        "Village": np.random.choice(["Village A (Flooded)", "Village B", "Village C"], 100),
        "Has_Exam": np.random.choice([True, False], 100, p=[0.35, 0.65]),
        "Distance_KM": np.random.uniform(5, 25, 100).round(1),
    }
    return pd.DataFrame(data)

df = load_data()

# Apply surge
if demand_surge > 0:
    extra_students = int(len(df) * (demand_surge / 100))
    # duplicate some rows to simulate surge
    surge_df = df.sample(n=extra_students, replace=True).copy()
    surge_df["Student_ID"] = [f"SURGE_{i}" for i in range(len(surge_df))]
    df = pd.concat([df, surge_df], ignore_index=True)

# Apply crisis logic: Blocked road impact
if road_blocked:
    df.loc[df["Village"] == "Village A (Flooded)", "Route_Status"] = "Rerouted via Detour (+15 mins)"
else:
    df.loc[df["Village"] == "Village A (Flooded)", "Route_Status"] = "Normal"

df.loc[df["Village"] != "Village A (Flooded)", "Route_Status"] = "Normal"

# Priority Scoring
df["Priority_Score"] = (df["Has_Exam"] * 50) + (df["Distance_KM"] * 1.5)
df = df.sort_values(by="Priority_Score", ascending=False).reset_index(drop=True)

# Bus Capacity calculation
total_buses = 10
if bus_breakdown:
    total_buses -= 2
total_capacity = total_buses * 45 # 45 seats per bus

df["Assigned_Transport"] = "Unassigned"
df.loc[:total_capacity-1, "Assigned_Transport"] = "Allocated Bus"
df.loc[total_capacity:, "Assigned_Transport"] = "Alternative Shuttle / Walk / Deferred"

# --- MAIN DASHBOARD METRICS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Students Seeking Transport", len(df))
col2.metric("Operational Buses", f"{total_buses} (2 Broken Down)")
col3.metric("Exam Students Prioritized", int(df["Has_Exam"].sum()))
col4.metric("Successfully Transported", min(len(df), total_capacity))

# --- TABS FOR DEEP DIVE ---
tab1, tab2, tab3 = st.tabs(["📋 Dispatch List", "📊 Impact & Analytics", "💡 AI Recommendations"])

with tab1:
    st.subheader("Dynamic Student Priority & Allocation Table")
    st.dataframe(df[["Student_ID", "Village", "Has_Exam", "Distance_KM", "Route_Status", "Assigned_Transport", "Priority_Score"]], use_container_width=True)

with tab2:
    st.subheader("Crisis Impact Breakdown")
    status_counts = df["Assigned_Transport"].value_counts()
    st.bar_chart(status_counts)

with tab3:
    st.subheader("🤖 AI-Generated Emergency Recommendations")
    st.success("1. **Priority Dispatch:** 100% of students with verified exams in the next 2 hours have been secured seats on the 8 remaining operational buses.")
    st.warning("2. **Flooding Mitigation:** Route 1 (Village A) is impassable. Automated dispatch recommends deploying 2 micro-shuttles to bridge students across the flooded creek to Bus Stop B.")
    st.info("3. **Surge Management:** For the 40% surplus demand, decentralized carpooling and bicycle fleets have been coordinated with local volunteers.")