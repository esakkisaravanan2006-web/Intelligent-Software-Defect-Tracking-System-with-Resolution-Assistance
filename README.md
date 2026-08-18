# 🐞 Intelligent Software Defect Tracking System with Resolution Assistance

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B?logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly)

## 📌 Executive Overview
The **Intelligent Software Defect Tracking System** is a robust, interactive analytics dashboard designed to transform raw bug tracking data into actionable insights. Built entirely in Python using Streamlit, this platform bridges the gap between software quality assurance and data science. It enables project managers, developers, and QA leads to dynamically monitor defect lifecycles, identify critical system vulnerabilities, and optimize resource allocation across sprint cycles.

## 🎯 Business Context & Problem Statement
In modern software development, unchecked defects and unprioritized bug backlogs lead to severe operational bottlenecks, missed sprint deadlines, and degraded product quality. Traditional tracking systems often provide static data without highlighting *where* the delays are happening. 

**The Solution:** This system addresses these challenges by introducing data-driven visibility. By analyzing historical bug life cycle data, the dashboard visualizes Service Level Agreement (SLA) compliance, highlights workload imbalances, and isolates the specific application modules generating the highest volume of critical defects.

## 📊 Core Dashboard Modules & Features

### 1. Executive Summary & KPIs
*   **Dynamic KPI Metrics:** Real-time calculation of total defects, open critical issues, and average resolution times.
*   **Defect Life Cycle Funnel:** A visual representation of bug attrition from 'Reported' to 'Closed', helping teams identify where bugs get stuck in the pipeline.
*   **Trend Analytics:** Time-series analysis of defects mapped across different months and sprint cycles.

### 2. Quality & Performance Analytics
*   **Severity vs. Priority Matrix:** Heatmap representations that expose misaligned priorities (e.g., high-severity bugs marked as low-priority).
*   **Resolution Time Deep-Dives:** Treemap visualizations breaking down the exact time taken to resolve issues across different application modules.

### 3. Resource Workload Management
*   **Assignee Distribution:** Bar charting that tracks how many open, in-progress, and resolved tickets are assigned to individual developers.
*   **Bottleneck Identification:** Instantly flags if a single developer or QA tester is overloaded, allowing for proactive task redistribution.

### 4. Interactive Data Slicing
*   **Multi-Parameter Filtering:** The sidebar allows users to slice the entire dataset dynamically by specific Sprints, Modules, and Severity levels. 
*   **Stateful UI:** Charts and metrics instantly recalculate and re-render based on the selected filters.

## 🛠️ Technical Architecture & Methodology

*   **Frontend / UI:** `Streamlit` was selected for its rapid prototyping capabilities and seamless integration with Python-based data pipelines.
*   **Data Processing:** `Pandas` handles the ingestion of the `.csv` report, executing complex data cleaning, aggregation, and grouping operations (e.g., calculating average resolution times by module).
*   **Visualization Engine:** `Plotly Graph_Objects` and `Plotly Express` generate fluid, interactive, browser-native charts that allow users to hover, zoom, and export data dynamically.

## 💻 Local Installation & Setup

To run this project locally on your machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR-USERNAME/Intelligent-Software-Defect-Tracking-System.git](https://github.com/YOUR-USERNAME/Intelligent-Software-Defect-Tracking-System.git)
   cd Intelligent-Software-Defect-Tracking-System
