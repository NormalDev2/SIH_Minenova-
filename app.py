import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Mining Doc Intelligence", layout="wide", page_icon="📁")

# ==========================================
# SIMULATED DATABASE (Real Internet Data)
# ==========================================
# This simulates the end-state of your OCR/Extraction pipeline from public internet PDFs.
def load_database():
    if 'docs_db' not in st.session_state:
        st.session_state.docs_db = pd.DataFrame([
            {"Filename": "BHP_Annual_Report_2023.pdf", "Pages": 352, "Date": "2023-09-15", "Status": "Processed", "Type": "Annual Report"},
            {"Filename": "BHP_Operational_Review_Q4_2023.pdf", "Pages": 48, "Date": "2024-01-20", "Status": "Processed", "Type": "Quarterly"},
            {"Filename": "Rio_Tinto_Annual_Report_2023.pdf", "Pages": 298, "Date": "2024-02-21", "Status": "Processed", "Type": "Annual Report"}
        ])
    
    if 'facts_db' not in st.session_state:
        st.session_state.facts_db = pd.DataFrame([
            {"Fact_ID": "F-001", "Metric": "Iron Ore Production", "Value": 257.0, "Unit": "Mt", "Entity": "BHP", "Year": "2023", "Document": "BHP_Annual_Report_2023.pdf", "Page": 42, "Location": "Table 3, Cell B4", "Confidence": "98%", "Status": "Verified"},
            {"Fact_ID": "F-002", "Metric": "Iron Ore Production", "Value": 253.0, "Unit": "Mt", "Entity": "BHP", "Year": "2022", "Document": "BHP_Annual_Report_2023.pdf", "Page": 42, "Location": "Table 3, Cell B3", "Confidence": "99%", "Status": "Verified"},
            {"Fact_ID": "F-003", "Metric": "Revenue", "Value": 53.8, "Unit": "Billion USD", "Entity": "BHP", "Year": "2023", "Document": "BHP_Annual_Report_2023.pdf", "Page": 12, "Location": "Financials, Row 1", "Confidence": "95%", "Status": "Verified"},
            {"Fact_ID": "F-004", "Metric": "Iron Ore Production", "Value": 331.5, "Unit": "Mt", "Entity": "Rio Tinto", "Year": "2023", "Document": "Rio_Tinto_Annual_Report_2023.pdf", "Page": 24, "Location": "Operations, Cell C2", "Confidence": "97%", "Status": "Verified"},
            # CONFLICTING DATA POINT INJECTED FOR DEMO
            {"Fact_ID": "F-005", "Metric": "Iron Ore Production", "Value": 259.5, "Unit": "Mt", "Entity": "BHP", "Year": "2023", "Document": "BHP_Operational_Review_Q4_2023.pdf", "Page": 8, "Location": "Q4 Summary", "Confidence": "85%", "Status": "Conflict"}
        ])

load_database()

# ==========================================
# SIDEBAR: THE FILE EXPLORER UI
# ==========================================
with st.sidebar:
    st.title("🏛️ DocuMine Intel")
    st.caption("Verifiable Document Intelligence")
    st.divider()
    
    view = st.radio("Navigation", [
        "📁 Documents", 
        "📊 Extracted Data", 
        "📈 Tracked Metrics", 
        "⚠ Conflicts", 
        "📑 Reports"
    ])
    
    st.divider()
    st.info("System Philosophy:\n\n*The AI writes the explanation, but does not decide the facts.*")

# ==========================================
# MAIN AREA ROUTING
# ==========================================

# --- 1. DOCUMENTS VIEW ---
if view == "📁 Documents":
    st.header("Document Repository")
    st.write("Files scraped from public internet sources and internal uploads.")
    st.dataframe(st.session_state.docs_db, use_container_width=True, hide_index=True)
    st.button("➕ Fetch New Documents (Web Scraping Engine)")

# --- 2. EXTRACTED DATA VIEW ---
elif view == "📊 Extracted Data":
    st.header("Structured Fact Database")
    st.write("Every extracted value linked to its exact source. No LLM hallucinations.")
    
    df = st.session_state.facts_db
    
    # Styled dataframe to show confidence and status
    def color_status(val):
        color = 'green' if val == 'Verified' else 'red' if val == 'Conflict' else 'orange'
        return f'color: {color}'
        
    # NOTE: Changed applymap to map for newer Pandas versions!
    st.dataframe(df.style.map(color_status, subset=['Status']), use_container_width=True, hide_index=True)

# --- 3. TRACKED METRICS (VISUALIZATIONS) ---
elif view == "📈 Tracked Metrics":
    st.header("Tracked Metrics & Change Detection")
    
    df = st.session_state.facts_db
    # Filter out conflicts for clean charts
    clean_df = df[df['Status'] == 'Verified']
    
    metric = st.selectbox("Select Metric to Track:", ["Iron Ore Production", "Revenue"])
    metric_df = clean_df[clean_df["Metric"] == metric].sort_values(by="Year")
    
    if not metric_df.empty:
        # Comparison & Change Detection Logic
        st.subheader("Automated Change Detection")
        if metric == "Iron Ore Production" and len(metric_df[metric_df["Entity"] == "BHP"]) > 1:
            val_2022 = metric_df[(metric_df["Entity"] == "BHP") & (metric_df["Year"] == "2022")]["Value"].values[0]
            val_2023 = metric_df[(metric_df["Entity"] == "BHP") & (metric_df["Year"] == "2023")]["Value"].values[0]
            change = val_2023 - val_2022
            pct_change = (change / val_2022) * 100
            
            st.success(f"**BHP {metric}:** 2022 ({val_2022} Mt) ➔ 2023 ({val_2023} Mt) | **Change: +{change} Mt (+{pct_change:.2f}%)**")
            st.caption("Evidence: Both values sourced from `BHP_Annual_Report_2023.pdf`, Page 42.")

        st.divider()
        st.subheader("Geological Visualization Rules Applied")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Rule: Compare entities ➔ Bar Chart**")
            # Grouped bar chart comparing BHP and Rio Tinto for 2023
            bar_df = metric_df[metric_df["Year"] == "2023"]
            fig_bar = px.bar(bar_df, x="Entity", y="Value", color="Entity", text_auto=True, title=f"{metric} Comparison (2023)")
            fig_bar.update_layout(yaxis_title=metric_df["Unit"].iloc[0])
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with col2:
            st.write("**Rule: Show change over time ➔ Line Chart**")
            # Line chart for BHP over time
            line_df = metric_df[metric_df["Entity"] == "BHP"]
            fig_line = px.line(line_df, x="Year", y="Value", markers=True, title=f"BHP {metric} Trend")
            fig_line.update_traces(marker=dict(size=12))
            st.plotly_chart(fig_line, use_container_width=True)

# --- 4. CONFLICTS VIEW ---
elif view == "⚠ Conflicts":
    st.header("Conflict Detection")
    st.error("⚠ CONFLICT DETECTED: Iron Ore Production (BHP, 2023)")
    st.write("Two different documents claim conflicting values for the same metric.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Source 1 (Authoritative)**")
        st.metric("Value", "257.0 Mt")
        st.caption("📄 `BHP_Annual_Report_2023.pdf`")
        st.caption("📍 Page 42, Table 3, Cell B4")
        if st.button("Mark Source 1 as Correct"):
            st.success("Conflict Resolved. Database updated.")
            
    with col2:
        st.warning("**Source 2 (Conflicting)**")
        st.metric("Value", "259.5 Mt")
        st.caption("📄 `BHP_Operational_Review_Q4_2023.pdf`")
        st.caption("📍 Page 8, Q4 Summary")
        if st.button("Mark Source 2 as Correct"):
            st.success("Conflict Resolved. Database updated.")

# --- 5. REPORTS VIEW ---
elif view == "📑 Reports":
    st.header("Interactive Evidence-Linked Reporting")
    st.write("Reports are generated dynamically from the Fact Database. Click any value to view provenance.")
    
    st.button("🔄 Regenerate Report with Latest Data")
    st.markdown("---")
    
    # Simulating the Jinja template rendering
    st.markdown("""
    ### 1. Executive Summary - Global Mining (FY 2023)
    
    In the fiscal year 2023, major operators reported strong yield despite market volatility. 
    **BHP** recorded a verified Iron Ore Production of <a href='#' title='Fact-001: BHP Annual Report 2023, Pg 42'>**257.0 Mt**</a>, representing an increase of <a href='#' title='Calculated from Fact-001 and Fact-002'>**1.58%**</a> compared to their 2022 output of <a href='#' title='Fact-002: BHP Annual Report 2023, Pg 42'>**253.0 Mt**</a>.
    
    Meanwhile, **Rio Tinto** led the comparison group with an extracted output of <a href='#' title='Fact-004: Rio Tinto Annual Report 2023, Pg 24'>**331.5 Mt**</a>.
    
    ### 2. Significant Changes & Exceptions
    *   **Revenue:** BHP reported total revenue of <a href='#' title='Fact-003: BHP Annual Report, Pg 12'>**53.8 Billion USD**</a>.
    *   **Data Conflicts:** A minor discrepancy of **2.5 Mt** was detected between BHP's Q4 Operational Review and the finalized Annual Report. The system has currently deferred to the Annual Report pending user resolution.
    
    ### 3. Methodology & Sources
    *Numbers in this report are automatically synchronized with the Structured Fact Database. Hover over any metric to view its exact document, page, and cell location.*
    """, unsafe_allow_html=True)