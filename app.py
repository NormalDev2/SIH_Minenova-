import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# 1. PAGE CONFIGURATION & THEME
# ==========================================
st.set_page_config(
    page_title="DocuMine Intel | Enterprise Doc AI", 
    layout="wide", 
    page_icon="⛏️",
    initial_sidebar_state="expanded"
)

# Custom Styling for Enterprise Look & Feel
st.markdown("""
    <style>
    .main { background-color: #FAFAFA; }
    .stMetric { background-color: #FFFFFF; padding: 15px; border-radius: 8px; border: 1px solid #E0E0E0; }
    .badge-verified { background-color: #D4EDDA; color: #155724; padding: 3px 8px; border-radius: 4px; border: 1px solid #C3E6CB; font-weight: 600; }
    .badge-conflict { background-color: #F8D7DA; color: #721C24; padding: 3px 8px; border-radius: 4px; border: 1px solid #F5C6CB; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. STATE INITIALIZATION (PERSISTENT DB)
# ==========================================
def init_session_state():
    if 'docs_db' not in st.session_state:
        st.session_state.docs_db = pd.DataFrame([
            {"Doc_ID": "DOC-01", "Filename": "BHP_Annual_Report_2023.pdf", "Pages": 352, "Date_Uploaded": "2023-09-15", "Status": "Processed", "Type": "Annual Report"},
            {"Doc_ID": "DOC-02", "Filename": "BHP_Operational_Review_Q4_2023.pdf", "Pages": 48, "Date_Uploaded": "2024-01-20", "Status": "Processed", "Type": "Quarterly"},
            {"Doc_ID": "DOC-03", "Filename": "Rio_Tinto_Annual_Report_2023.pdf", "Pages": 298, "Date_Uploaded": "2024-02-21", "Status": "Processed", "Type": "Annual Report"}
        ])
    
    if 'facts_db' not in st.session_state:
        st.session_state.facts_db = pd.DataFrame([
            {"Fact_ID": "F-001", "Metric": "Iron Ore Production", "Value": 257.0, "Unit": "Mt", "Entity": "BHP", "Year": "2023", "Document": "BHP_Annual_Report_2023.pdf", "Page": 42, "Location": "Table 3, Cell B4", "Confidence": 0.98, "Status": "Verified"},
            {"Fact_ID": "F-002", "Metric": "Iron Ore Production", "Value": 253.0, "Unit": "Mt", "Entity": "BHP", "Year": "2022", "Document": "BHP_Annual_Report_2023.pdf", "Page": 42, "Location": "Table 3, Cell B3", "Confidence": 0.99, "Status": "Verified"},
            {"Fact_ID": "F-003", "Metric": "Revenue", "Value": 53.8, "Unit": "Billion USD", "Entity": "BHP", "Year": "2023", "Document": "BHP_Annual_Report_2023.pdf", "Page": 12, "Location": "Financials, Row 1", "Confidence": 0.95, "Status": "Verified"},
            {"Fact_ID": "F-004", "Metric": "Iron Ore Production", "Value": 331.5, "Unit": "Mt", "Entity": "Rio Tinto", "Year": "2023", "Document": "Rio_Tinto_Annual_Report_2023.pdf", "Page": 24, "Location": "Operations, Cell C2", "Confidence": 0.97, "Status": "Verified"},
            {"Fact_ID": "F-005", "Metric": "Iron Ore Production", "Value": 259.5, "Unit": "Mt", "Entity": "BHP", "Year": "2023", "Document": "BHP_Operational_Review_Q4_2023.pdf", "Page": 8, "Location": "Q4 Summary", "Confidence": 0.85, "Status": "Conflict"}
        ])

init_session_state()

# Helper function to refresh facts state
def resolve_conflict(chosen_id, rejected_id):
    st.session_state.facts_db.loc[st.session_state.facts_db['Fact_ID'] == chosen_id, 'Status'] = 'Verified'
    st.session_state.facts_db.loc[st.session_state.facts_db['Fact_ID'] == rejected_id, 'Status'] = 'Resolved (Rejected)'
    st.rerun()

# ==========================================
# 3. SIDEBAR CONTROLS & NAVIGATION
# ==========================================
with st.sidebar:
    st.title("⛏️ DocuMine Intel")
    st.caption("Verifiable Mining Document Extraction Engine")
    st.divider()
    
    # Navigation Radio
    view = st.radio(
        "Navigation", 
        ["📊 Control Dashboard", "📁 Document Repository", "🔍 Fact Inspector", "📈 Analytics & Change", "⚠ Conflict Resolution", "📑 Dynamic Reports"],
        index=0
    )
    
    st.divider()
    
    # Sidebar Metrics Summary
    total_facts = len(st.session_state.facts_db)
    conflicts_cnt = len(st.session_state.facts_db[st.session_state.facts_db['Status'] == 'Conflict'])
    
    st.metric("Total Extracted Facts", total_facts)
    if conflicts_cnt > 0:
        st.sidebar.error(f"Unresolved Conflicts: {conflicts_cnt}")
    else:
        st.sidebar.success("All Conflicts Resolved")

    st.divider()
    st.caption("SIH Prototype v2.4 | Engine Status: **Active**")

# ==========================================
# 4. VIEW ROUTING & MAIN MODULES
# ==========================================

# --- VIEW 1: CONTROL DASHBOARD ---
if view == "📊 Control Dashboard":
    st.header("Executive Control Dashboard")
    st.write("Real-time operational summary of document ingestion and data verification pipelines.")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Ingested Documents", len(st.session_state.docs_db))
    m2.metric("Extracted Datapoints", len(st.session_state.facts_db))
    
    verified_pct = (len(st.session_state.facts_db[st.session_state.facts_db['Status'] == 'Verified']) / len(st.session_state.facts_db)) * 100
    m3.metric("Verification Rate", f"{verified_pct:.1f}%")
    m4.metric("Active Data Conflicts", len(st.session_state.facts_db[st.session_state.facts_db['Status'] == 'Conflict']))
    
    st.divider()
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("Recent Ingestion Activity")
        st.dataframe(st.session_state.docs_db, use_container_width=True, hide_index=True)
        
    with c2:
        st.subheader("System Architecture")
        st.info("""
        **Processing Steps:**
        1. **Ingestion:** Native & Scanned PDF OCR
        2. **Layout Parsing:** Structure & Bounding Box Extraction
        3. **Fact Extraction:** Deterministic Schema Mapping
        4. **Cross-Validation:** Multi-document entity matching
        5. **Human Audit:** Interactive UI confirmation
        """)

# --- VIEW 2: DOCUMENT REPOSITORY ---
elif view == "📁 Document Repository":
    st.header("Document Ingestion & Storage")
    st.write("Manage parsed documents and trigger automated scraping pipelines.")
    
    col_up1, col_up2 = st.columns([3, 1])
    with col_up1:
        uploaded_file = st.file_uploader("Upload PDF Documents for Processing", type=["pdf"])
        if uploaded_file is not None:
            if st.button("Process Uploaded File"):
                new_doc = {
                    "Doc_ID": f"DOC-0{len(st.session_state.docs_db)+1}",
                    "Filename": uploaded_file.name,
                    "Pages": 120,
                    "Date_Uploaded": datetime.now().strftime("%Y-%m-%d"),
                    "Status": "Processed",
                    "Type": "Custom Upload"
                }
                st.session_state.docs_db = pd.concat([st.session_state.docs_db, pd.DataFrame([new_doc])], ignore_index=True)
                st.success(f"Successfully processed `{uploaded_file.name}`!")
                st.rerun()
                
    with col_up2:
        st.write("### Quick Actions")
        if st.button("🔄 Trigger Web Crawler", use_container_width=True):
            st.toast("Crawling SEC EDGAR & ASX repositories...", icon="🔍")

    st.divider()
    st.dataframe(st.session_state.docs_db, use_container_width=True, hide_index=True)

# --- VIEW 3: FACT INSPECTOR ---
elif view == "🔍 Fact Inspector":
    st.header("Structured Fact Database")
    st.write("Every extracted value is mapped to its exact spatial location within the source PDF.")
    
    # Filter Controls
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        entity_filter = st.multiselect("Filter Entity", options=st.session_state.facts_db["Entity"].unique(), default=st.session_state.facts_db["Entity"].unique())
    with col_f2:
        status_filter = st.multiselect("Filter Status", options=st.session_state.facts_db["Status"].unique(), default=st.session_state.facts_db["Status"].unique())
    with col_f3:
        search_term = st.text_input("Search Metric", "")

    # Apply Filters
    df_filtered = st.session_state.facts_db[
        (st.session_state.facts_db["Entity"].isin(entity_filter)) &
        (st.session_state.facts_db["Status"].isin(status_filter)) &
        (st.session_state.facts_db["Metric"].str.contains(search_term, case=False))
    ]

    # Styling Status Column
    def style_status(val):
        if val == 'Verified':
            return 'background-color: #D4EDDA; color: #155724; font-weight: bold;'
        elif val == 'Conflict':
            return 'background-color: #F8D7DA; color: #721C24; font-weight: bold;'
        return 'background-color: #FFF3CD; color: #856404;'

    st.dataframe(
        df_filtered.style.map(style_status, subset=['Status']), 
        use_container_width=True, 
        hide_index=True
    )
    
    # Data Export Capability
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export Fact Database (CSV)", data=csv, file_name="extracted_facts.csv", mime="text/csv")

# --- VIEW 4: ANALYTICS & CHANGE ---
elif view == "📈 Analytics & Change":
    st.header("Analytics Engine & Deterministic Rules")
    
    clean_df = st.session_state.facts_db[st.session_state.facts_db['Status'] == 'Verified']
    
    selected_metric = st.selectbox("Select Metric for Trend Analysis:", clean_df["Metric"].unique())
    metric_subset = clean_df[clean_df["Metric"] == selected_metric].sort_values(by="Year")
    
    if not metric_subset.empty:
        # Automated Variance Calculation
        st.subheader("Automated Year-over-Year (YoY) Variance")
        bhp_data = metric_subset[metric_subset["Entity"] == "BHP"]
        
        if len(bhp_data) >= 2:
            val_22 = bhp_data[bhp_data["Year"] == "2022"]["Value"].values[0]
            val_23 = bhp_data[bhp_data["Year"] == "2023"]["Value"].values[0]
            diff = val_23 - val_22
            pct = (diff / val_22) * 100
            
            unit = bhp_data["Unit"].iloc[0]
            
            c_m1, c_m2 = st.columns(2)
            c_m1.success(f"**BHP {selected_metric} Variance (2022 ➔ 2023):** +{diff:.2f} {unit} (+{pct:.2f}%)")
            c_m2.caption(f"**Audit Trail:** Sourced from `{bhp_data['Document'].iloc[0]}`, Page {bhp_data['Page'].iloc[0]}. Verified deterministically.")

        st.divider()
        st.subheader("Structured Visualizations")
        
        col_v1, col_v2 = st.columns(2)
        
        with col_v1:
            st.markdown("**Cross-Entity Comparison (2023)**")
            data_2023 = metric_subset[metric_subset["Year"] == "2023"]
            if not data_2023.empty:
                fig_bar = px.bar(
                    data_2023, 
                    x="Entity", 
                    y="Value", 
                    color="Entity", 
                    text_auto=True,
                    color_discrete_sequence=px.colors.qualitative.Bold,
                    title=f"2023 {selected_metric} by Entity"
                )
                fig_bar.update_layout(yaxis_title=data_2023["Unit"].iloc[0], showlegend=False)
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("No data available for 2023 comparison.")
                
        with col_v2:
            st.markdown("**Historical Trajectory Trend**")
            data_trend = metric_subset[metric_subset["Entity"] == "BHP"]
            if not data_trend.empty:
                fig_line = px.line(
                    data_trend, 
                    x="Year", 
                    y="Value", 
                    markers=True,
                    title=f"BHP {selected_metric} Historical Trend"
                )
                fig_line.update_traces(line_color="#1F77B4", line_width=3, marker=dict(size=10))
                fig_line.update_layout(yaxis_title=data_trend["Unit"].iloc[0])
                st.plotly_chart(fig_line, use_container_width=True)
            else:
                st.info("Insufficient historical data points for line trend.")

# --- VIEW 5: CONFLICT RESOLUTION ---
elif view == "⚠ Conflict Resolution":
    st.header("Human-in-the-Loop Conflict Resolution")
    st.write("Identified data discrepancies requiring manual verification.")
    
    conflicts = st.session_state.facts_db[st.session_state.facts_db["Status"] == "Conflict"]
    
    if not conflicts.empty:
        for idx, conflict_row in conflicts.iterrows():
            st.error(f"⚠ CONFLICT DETECTED: {conflict_row['Metric']} ({conflict_row['Entity']}, {conflict_row['Year']})")
            
            # Find the opposing verified fact for comparison
            opposing_fact = st.session_state.facts_db[
                (st.session_state.facts_db["Metric"] == conflict_row["Metric"]) &
                (st.session_state.facts_db["Entity"] == conflict_row["Entity"]) &
                (st.session_state.facts_db["Year"] == conflict_row["Year"]) &
                (st.session_state.facts_db["Fact_ID"] != conflict_row["Fact_ID"])
            ].iloc[0]
            
            col_c1, col_c2 = st.columns(2)
            
            with col_c1:
                st.info("**Primary Candidate (Authoritative Source)**")
                st.metric(label="Extracted Value", value=f"{opposing_fact['Value']} {opposing_fact['Unit']}")
                st.write(f"**Document:** `{opposing_fact['Document']}`")
                st.write(f"**Location:** Page {opposing_fact['Page']}, {opposing_fact['Location']}")
                st.write(f"**Model Confidence:** {opposing_fact['Confidence']*100:.0f}%")
                
                if st.button(f"Confirm Value: {opposing_fact['Value']} {opposing_fact['Unit']}", key=f"btn_{opposing_fact['Fact_ID']}"):
                    resolve_conflict(opposing_fact['Fact_ID'], conflict_row['Fact_ID'])
                    
            with col_c2:
                st.warning("**Secondary Candidate (Discrepant Source)**")
                st.metric(label="Extracted Value", value=f"{conflict_row['Value']} {conflict_row['Unit']}")
                st.write(f"**Document:** `{conflict_row['Document']}`")
                st.write(f"**Location:** Page {conflict_row['Page']}, {conflict_row['Location']}")
                st.write(f"**Model Confidence:** {conflict_row['Confidence']*100:.0f}%")
                
                if st.button(f"Confirm Value: {conflict_row['Value']} {conflict_row['Unit']}", key=f"btn_{conflict_row['Fact_ID']}"):
                    resolve_conflict(conflict_row['Fact_ID'], opposing_fact['Fact_ID'])
    else:
        st.success("🎉 Zero Conflicts Detected. Database integrity fully verified!")
        if st.button("Simulate New Data Conflict"):
            # Inject a mock conflict for demonstration purposes
            st.session_state.facts_db.loc[st.session_state.facts_db['Fact_ID'] == 'F-001', 'Status'] = 'Verified'
            st.session_state.facts_db.loc[st.session_state.facts_db['Fact_ID'] == 'F-005', 'Status'] = 'Conflict'
            st.rerun()

# --- VIEW 6: DYNAMIC REPORTS ---
elif view == "📑 Dynamic Reports":
    st.header("Dynamic Report Generation & Provenance Audit")
    st.write("Generates automated summary documents where every figure links to verified database facts.")
    
    col_rep1, col_rep2 = st.columns([3, 1])
    with col_rep2:
        st.button("🔄 Sync with Latest Facts", use_container_width=True)
        st.button("📥 Export Report (PDF)", use_container_width=True)
        
    with col_rep1:
        # Fetch actual data values dynamically from session state
        bhp_23_fact = st.session_state.facts_db[st.session_state.facts_db['Fact_ID'] == 'F-001'].iloc[0]
        bhp_22_fact = st.session_state.facts_db[st.session_state.facts_db['Fact_ID'] == 'F-002'].iloc[0]
        rio_23_fact = st.session_state.facts_db[st.session_state.facts_db['Fact_ID'] == 'F-004'].iloc[0]
        rev_fact = st.session_state.facts_db[st.session_state.facts_db['Fact_ID'] == 'F-003'].iloc[0]
        
        # Calculate dynamic variance
        calc_change = ((bhp_23_fact['Value'] - bhp_22_fact['Value']) / bhp_22_fact['Value']) * 100
        
        st.markdown("---")
        st.markdown(f"""
        ### Executive Mining Review (FY 2023)
        
        **1. Operational Output Summary**
        During FY 2023, **BHP** registered a verified Iron Ore Production total of 
        <span class='badge-verified' title='Source: {bhp_23_fact["Document"]} | Pg {bhp_23_fact["Page"]}'>
        {bhp_23_fact["Value"]} {bhp_23_fact["Unit"]}
        </span>, reflecting a YoY output variance of 
        <span class='badge-verified' title='Calculated deterministically from F-001 and F-002'>
        +{calc_change:.2f}%
        </span> 
        relative to FY 2022 output of 
        <span class='badge-verified' title='Source: {bhp_22_fact["Document"]} | Pg {bhp_22_fact["Page"]}'>
        {bhp_22_fact["Value"]} {bhp_22_fact["Unit"]}
        </span>.
        
        Peer comparison shows **Rio Tinto** reaching an annual output volume of 
        <span class='badge-verified' title='Source: {rio_23_fact["Document"]} | Pg {rio_23_fact["Page"]}'>
        {rio_23_fact["Value"]} {rio_23_fact["Unit"]}
        </span> over the identical tracking window.
        
        **2. Financial Performance & Revenue Tracking**
        * **Total Consolidated Revenue:** BHP generated 
          <span class='badge-verified' title='Source: {rev_fact["Document"]} | Pg {rev_fact["Page"]}'>
          {rev_fact["Value"]} {rev_fact["Unit"]}
          </span>.
        * **Conflict Metrics:** Highlighting system data integrity checks, discrepancies between initial quarterly operational reports and final annual filings are highlighted above for review.
        
        ---
        *Hover over highlighted metrics to inspect linked evidence source paths.*
        """, unsafe_allow_html=True)
