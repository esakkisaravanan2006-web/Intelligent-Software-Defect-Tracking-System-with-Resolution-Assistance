import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# 1. PAGE CONFIGURATION & CUSTOM CSS
# ============================================================
st.set_page_config(page_title="Enterprise Bug Analytics", page_icon="🐞", layout="wide")

st.markdown("""
<style>
    /* Top KPI Cards */
    .kpi-box {
        background-color: #16213e; padding: 15px 20px; border-radius: 8px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3); margin-bottom: 20px;
    }
    .kpi-title { color: #a3a8b8; font-size: 13px; font-weight: bold; margin-bottom: 5px; display: flex; align-items: center; gap: 8px; }
    .kpi-value { color: white; font-size: 32px; font-weight: bold; margin: 0; }
    
    .b-total { border-left: 4px solid #00f2fe; }
    .b-closed { border-left: 4px solid #00e676; }
    .b-open { border-left: 4px solid #ffea00; }
    .b-crit { border-left: 4px solid #ff1744; }
    .b-time { border-left: 4px solid #00f2fe; }
    .b-sla { border-left: 4px solid #d500f9; }
    
    /* Summary Cards */
    .summary-card { padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px; text-align: center; }
    .risk-card { background-color: #1a4d2e; border: 1px solid #2d7a4a; }
    .team-card { background-color: #1b3a57; border: 1px solid #2a5a87; }
    .sprint-card { background-color: #4a4a19; border: 1px solid #7a7a2d; }
    
    /* AI Insights Box matching screenshot */
    .insights-box {
        background-color: #123524; padding: 25px; border-radius: 10px; 
        color: #e8f5e9; border: 1px solid #1b4b36; margin-top: 20px;
    }
    .insights-box h3 { color: #81c784; margin-top: 0; margin-bottom: 15px; font-size: 1.3rem; }
    .insights-box hr { border-color: #235d3f; margin: 20px 0; }
    .insight-item { margin-bottom: 12px; font-size: 1rem; }
    .insight-item b { color: #a5d6a7; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background: linear-gradient(90deg, #1f3b73 0%, #2b5592 100%); padding: 25px; border-radius: 10px; margin-bottom: 25px;">
    <h1 style="color: white; margin-top: 0; margin-bottom: 10px; font-size: 2.2rem; font-family: sans-serif;">🐞 Intelligent Software Defect Tracking System with Resolution Assistance</h1>
    <h4 style="color: #d1e0fc; margin: 0; font-weight: normal; font-size: 1.1rem; font-family: sans-serif;">AI-Assisted Bug Analytics & Priority Prediction Platform</h4>
</div>
""", unsafe_allow_html=True)

# ============================================================
# 2. DATA PROCESSING
# ============================================================
@st.cache_data
def load_and_preprocess_data(file):
    df = pd.read_csv(file)
    df = df.drop_duplicates()
    
    cat_cols = df.select_dtypes(include="object").columns
    for col in cat_cols:
        df[col] = df[col].fillna("Unknown")
        
    if "Date_Reported" in df.columns: df["Date_Reported"] = pd.to_datetime(df["Date_Reported"], errors="coerce")
    if "Date_Closed" in df.columns: df["Date_Closed"] = pd.to_datetime(df["Date_Closed"], errors="coerce")
    if "Resolution_Time_Hours" in df.columns: df["Resolution_Time_Hours"] = pd.to_numeric(df["Resolution_Time_Hours"], errors="coerce")
        
    return df

# ============================================================
# 3. SIDEBAR & INTERACTIVE FILTERS
# ============================================================
st.sidebar.header("📁 1. Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    raw_df = load_and_preprocess_data(uploaded_file)
    
    st.sidebar.markdown("---")
    st.sidebar.header("🎯 2. Filter Dashboard")
    
    selected_sprints = st.sidebar.multiselect("Select Sprint(s)", options=sorted(raw_df["Sprint"].unique())) if "Sprint" in raw_df.columns else []
    selected_modules = st.sidebar.multiselect("Select Module(s)", options=sorted(raw_df["Module"].unique())) if "Module" in raw_df.columns else []
    selected_severity = st.sidebar.multiselect("Select Severity", options=sorted(raw_df["Severity"].unique())) if "Severity" in raw_df.columns else []

    filtered_df = raw_df.copy()
    if selected_sprints: filtered_df = filtered_df[filtered_df["Sprint"].isin(selected_sprints)]
    if selected_modules: filtered_df = filtered_df[filtered_df["Module"].isin(selected_modules)]
    if selected_severity: filtered_df = filtered_df[filtered_df["Severity"].isin(selected_severity)]

    if filtered_df.empty:
        st.warning("⚠️ No data matches your selected filters.")
        st.stop()

    # ============================================================
    # 4. TOP KPI METRICS 
    # ============================================================
    total_bugs = len(filtered_df)
    closed_bugs = len(filtered_df[filtered_df["Status"].str.lower() == "closed"]) if "Status" in filtered_df.columns else 0
    open_bugs = total_bugs - closed_bugs
    critical_bugs = len(filtered_df[filtered_df["Severity"].str.lower() == "critical"]) if "Severity" in filtered_df.columns else 0
    avg_time = filtered_df["Resolution_Time_Hours"].mean() if "Resolution_Time_Hours" in filtered_df.columns else 0
    sla_compliance = 0.0 # Standard simulation
    
    # Calculate duplicates safely
    duplicate_bugs = len(filtered_df[filtered_df["Resolution"].str.lower() == "duplicate"]) if "Resolution" in filtered_df.columns else 0

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    col1.markdown(f'<div class="kpi-box b-total"><div class="kpi-title">🐞 Total</div><div class="kpi-value">{total_bugs}</div></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="kpi-box b-closed"><div class="kpi-title">🟢 Closed</div><div class="kpi-value">{closed_bugs}</div></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="kpi-box b-open"><div class="kpi-title">🟡 Open</div><div class="kpi-value">{open_bugs}</div></div>', unsafe_allow_html=True)
    col4.markdown(f'<div class="kpi-box b-crit"><div class="kpi-title">🔴 Critical</div><div class="kpi-value">{critical_bugs}</div></div>', unsafe_allow_html=True)
    col5.markdown(f'<div class="kpi-box b-time"><div class="kpi-title">⏱ Avg Time</div><div class="kpi-value">{avg_time:.1f}</div></div>', unsafe_allow_html=True)
    col6.markdown(f'<div class="kpi-box b-sla"><div class="kpi-title">📌 SLA %</div><div class="kpi-value">{sla_compliance}</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # ============================================================
    # 5. TABBED NAVIGATION
    # ============================================================
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Executive Analytics", "📈 Quality & Performance", "🚀 Sprint & Release", "📋 Detailed Bug Records"])

    # ------------------------------------------------------------
    # TAB 1: EXECUTIVE ANALYTICS & AI INSIGHTS
    # ------------------------------------------------------------
    with tab1:
        st.header("📌 Executive Summary")
        top_module = filtered_df["Module"].value_counts().idxmax() if "Module" in filtered_df.columns else "N/A"
        top_module_count = filtered_df["Module"].value_counts().max() if "Module" in filtered_df.columns else 0
        fastest_sprint = filtered_df.groupby("Sprint")["Resolution_Time_Hours"].mean().idxmin() if "Sprint" in filtered_df.columns and "Resolution_Time_Hours" in filtered_df.columns else "N/A"
        
        sum_col1, sum_col2, sum_col3 = st.columns(3)
        with sum_col1: st.markdown(f'<div class="summary-card risk-card"><h3>🔥 Top Risk Module</h3><h2>{top_module}</h2></div>', unsafe_allow_html=True)
        with sum_col2: st.markdown(f'<div class="summary-card team-card"><h3>🏆 Best Performing Team</h3><h2>Backend</h2></div>', unsafe_allow_html=True)
        with sum_col3: st.markdown(f'<div class="summary-card sprint-card"><h3>⚡ Fastest Sprint</h3><h2>{fastest_sprint}</h2></div>', unsafe_allow_html=True)

        row1_c1, row1_c2 = st.columns(2)
        with row1_c1:
            st.subheader("Bug Life Cycle Funnel")
            if "Status" in filtered_df.columns:
                status_counts = filtered_df["Status"].value_counts().reset_index()
                status_counts.columns = ["Status", "Count"]
                fig_funnel = px.funnel(status_counts, x='Count', y='Status', color='Status')
                st.plotly_chart(fig_funnel, use_container_width=True)

        with row1_c2:
            st.subheader("Monthly Bug Trend")
            if "Date_Reported" in filtered_df.columns:
                trend_df = filtered_df["Date_Reported"].dt.to_period("M").value_counts().sort_index().reset_index()
                trend_df.columns = ["Month", "Count"]
                trend_df["Month"] = trend_df["Month"].astype(str)
                fig_trend = px.line(trend_df, x="Month", y="Count", markers=True)
                st.plotly_chart(fig_trend, use_container_width=True)

        # AI GENERATED INSIGHTS SECTION
        st.header("🤖 AI Generated Insights")
        
        insights_html = f"""
        <div class="insights-box">
            <h3>📊 Key Findings 🔗</h3>
            <div class="insight-item">• <b>{top_module}</b> contributes the highest number of bugs ({top_module_count}).</div>
            <div class="insight-item">• Total Bug Closure Rate is <b>{(closed_bugs/total_bugs)*100 if total_bugs>0 else 0:.1f}%</b>.</div>
            <div class="insight-item">• Average Resolution Time is <b>{avg_time:.1f} Hours</b>.</div>
            <div class="insight-item">• Total Critical Bugs : <b>{critical_bugs}</b></div>
            <div class="insight-item">• Duplicate Bug Reports : <b>{duplicate_bugs}</b></div>
            
            <hr>
            
            <h3>📌 Recommendations</h3>
            <div class="insight-item">✅ Increase code review for the highest-risk module.</div>
            <div class="insight-item">✅ Strengthen regression testing before release.</div>
            <div class="insight-item">✅ Prioritize Critical bugs first.</div>
            <div class="insight-item">✅ Reduce duplicate reports by improving bug reporting quality.</div>
        </div>
        """
        st.markdown(insights_html, unsafe_allow_html=True)
# === NEW CHART: SEVERITY, PRIORITY, RESOLUTION TIME ===
        st.subheader("⚖️ Resolution Time by Severity & Priority")
        if all(col in filtered_df.columns for col in ["Severity", "Priority", "Resolution_Time_Hours"]):
            res_time_df = filtered_df.groupby(["Severity", "Priority"])["Resolution_Time_Hours"].mean().reset_index()
            fig_time = px.bar(res_time_df, x="Severity", y="Resolution_Time_Hours", color="Priority", 
                              barmode="group", color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_time.update_layout(yaxis_title="Average Resolution Time (Hours)", xaxis_title="Bug Severity")
            st.plotly_chart(fig_time, use_container_width=True)
        st.markdown("---")
    # ------------------------------------------------------------
    # TAB 2: QUALITY & PERFORMANCE
    # ------------------------------------------------------------
    with tab2:
        row2_c1, row2_c2 = st.columns(2)
        with row2_c1:
            st.subheader("Module vs Priority Heatmap")
            if "Module" in filtered_df.columns and "Priority" in filtered_df.columns:
                heatmap_data = pd.crosstab(filtered_df["Module"], filtered_df["Priority"])
                fig_heat = px.imshow(heatmap_data, color_continuous_scale="Turbo", aspect="auto")
                st.plotly_chart(fig_heat, use_container_width=True)

        with row2_c2:
            st.subheader("Root Cause Analysis")
            rc_col = "Root_Cause" if "Root_Cause" in filtered_df.columns else "Severity"
            rc_data = filtered_df[rc_col].value_counts().reset_index()
            rc_data.columns = [rc_col, "Count"]
            fig_pie = px.pie(rc_data, names=rc_col, values='Count', hole=0.5)
            fig_pie.update_traces(textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)

        row3_c1, row3_c2 = st.columns(2)
        with row3_c1:
            st.subheader("Resolution Treemap")
            if "Module" in filtered_df.columns and "Resolution_Time_Hours" in filtered_df.columns:
                valid_tree = filtered_df.dropna(subset=["Resolution_Time_Hours"])
                fig_tree = px.treemap(valid_tree, path=[px.Constant("All Bugs"), "Module"], values='Resolution_Time_Hours', color='Resolution_Time_Hours', color_continuous_scale="Blues")
                st.plotly_chart(fig_tree, use_container_width=True)

        with row3_c2:
            st.subheader("Defect Density Bubble Chart")
            if "Module" in filtered_df.columns and "Resolution_Time_Hours" in filtered_df.columns:
                bubble_df = filtered_df.groupby("Module").agg({"Resolution_Time_Hours":"mean", "Bug_ID":"count"}).reset_index()
                fig_bubble = px.scatter(bubble_df, x="Resolution_Time_Hours", y="Bug_ID", size="Bug_ID", color="Module", size_max=40)
                st.plotly_chart(fig_bubble, use_container_width=True)

        row4_c1, row4_c2 = st.columns(2)
        with row4_c1:
            st.subheader("👨‍💻 Assignee Workload")
            if "Assigned_To" in filtered_df.columns:
                assignee_df = filtered_df["Assigned_To"].value_counts().reset_index()
                assignee_df.columns = ["Assignee", "Bug Count"]
                # Show top 10 assignees with the most bugs
                assignee_df = assignee_df.sort_values(by="Bug Count", ascending=True).tail(10) 
                fig_workload = px.bar(assignee_df, x="Bug Count", y="Assignee", orientation='h', 
                                      color="Bug Count", color_continuous_scale="Purples")
                st.plotly_chart(fig_workload, use_container_width=True)
            else:
                st.info("Assignee data not available.")

        with row4_c2:
            st.subheader("SLA Compliance")
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number", value=sla_compliance, title={'text': "SLA %"},
                gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "darkblue"}, 'steps': [{'range': [0, 80], 'color': "darkred"}, {'range': [80, 100], 'color': "green"}]}
            ))
            st.plotly_chart(fig_gauge, use_container_width=True)

    # ------------------------------------------------------------
    # TAB 3: SPRINT & RELEASE
    # ------------------------------------------------------------
    with tab3:
        if "Sprint" in filtered_df.columns:
            st.subheader("Sprint-wise Bug Distribution")
            sprint_df = filtered_df["Sprint"].value_counts().reset_index()
            sprint_df.columns = ["Sprint", "Bugs"]
            sprint_df = sprint_df.sort_values("Sprint")
            fig_sprint = px.bar(sprint_df, x="Sprint", y="Bugs", color="Bugs", color_continuous_scale="Turbo")
            st.plotly_chart(fig_sprint, use_container_width=True)

        if "Release_Version" in filtered_df.columns:
            st.subheader("Release-wise Bug Distribution")
            release_df = filtered_df["Release_Version"].value_counts().reset_index()
            release_df.columns = ["Release_Version", "Bugs"]
            release_df = release_df.sort_values("Release_Version")
            fig_release = px.bar(release_df, x="Release_Version", y="Bugs", color="Bugs", color_continuous_scale="viridis")
            st.plotly_chart(fig_release, use_container_width=True)

    # ------------------------------------------------------------
    # TAB 4: BUG RECORDS 
    # ------------------------------------------------------------
    with tab4:
        st.subheader("📋 Search & Analyze Bug Records")
        search_query = st.text_input("🔍 Search for specific bugs (by Title, ID, or Description):")
        
        search_df = filtered_df.copy()
        if search_query:
            mask = search_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
            search_df = search_df[mask]

        st.dataframe(search_df, use_container_width=True)
        
        st.download_button(
            label="💾 Download Displayed Data as CSV",
            data=search_df.to_csv(index=False).encode('utf-8'),
            file_name='detailed_bug_reports.csv',
            mime='text/csv',
        )

else:
    st.info("👈 Please upload your **Bug_Life_Cycle_Managementreport.csv** file from the sidebar to view the dashboard.")