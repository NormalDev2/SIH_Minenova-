import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- PAGE CONFIGURATION & THEME ---

st.set_page_config(
    page_title="DocuMine | Document Extraction Engine", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Enterprise Dashboard Styling
st.markdown("""
    <style>
    /* Global Container Styles */
    .main { background-color: #FAFAFA; }
    
    /* Subtle Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        padding: 16px;
        border-radius: 4px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    
    /* Clean Text Badges for Evidence */
    .badge-verified {
        background-color: #EDF7ED;
        color: #1E4620;
        padding: 2px 6px;
        border-radius: 3px;
        border: 1px solid #C3E6CB;
        font-family: monospace;
        font-size: 0.9em;
    }
    
    /* Clean Sidebar Override */
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)


# --- STATE INITIALIZATION & DATABASE ---
def init_session_state():
    if 'docs_db' not in st.session_state:
        st.session_state.docs_db = pd.DataFrame([
            {"Doc_ID": "DOC-01", "Filename": "BHP_Annual_Report_2023.pdf", "Pages": 352, "Date_Uploaded": "2023-09-15", "Status": "Processed", "Type": "Annual Report"},
            {"Doc_ID": "DOC-02", "Filename": "BHP_Operational_Review_Q4_2023.pdf", "Pages": 48, "Date_Uploaded": "2024-01-20", "Status": "Processed", "Type": "Quarterly Report"},
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

def resolve_conflict(chosen_id, rejected_id):
    st.session_state.facts_db.loc[st.session_state.facts_db['Fact_ID'] == chosen_id, 'Status'] = 'Verified'
    st.session_state.facts_db.loc[st.session_state.facts_db['Fact_ID'] == rejected_id, 'Status'] = 'Resolved (Rejected)'
    st.rerun()


#--- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("DocuMine Engine")
    st.caption("Structured Document Processing Platform")
    st.divider()
    
    view = st.radio(
        "Navigation", 
        [
            "Overview", 
            "Document Management", 
            "Fact Database", 
            "Analytics & Variance", 
            "Data Conflicts", 
            "Automated Reports"
        ],
        index=0
    )
    
    st.divider()
    
    total_facts = len(st.session_state.facts_db)
    conflicts_cnt = len(st.session_state.facts_db[st.session_state.facts_db['Status'] == 'Conflict'])
    
    st.metric("Indexed Facts", total_facts)
    if conflicts_cnt > 0:
        st.warning(f"Pending Conflicts: {conflicts_cnt}")
    else:
        st.success("All Conflicts Resolved")

    st.divider()
    st.caption("System Status: Online | Core v2.4")

# VIEW ROUTING & MAIN CONTENT

# --- OVERVIEW ---
if view == "Overview":
    st.header("System Overview")
    st.write("Summary of document ingestion status and structured extraction outputs.")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Documents", len(st.session_state.docs_db))
    m2.metric("Extracted Datapoints", len(st.session_state.facts_db))
    
    verified_pct = (len(st.session_state.facts_db[st.session_state.facts_db['Status'] == 'Verified']) / len(st.session_state.facts_db)) * 100
    m3.metric("Verification Rate", f"{verified_pct:.1f}%")
    m4.metric("Unresolved Conflicts", len(st.session_state.facts_db[st.session_state.facts_db['Status'] == 'Conflict']))
    
    st.divider()
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("Ingested Files")
        st.dataframe(st.session_state.docs_db, use_container_width=True, hide_index=True)
        
    with c2:
        st.subheader("Processing Architecture")
        st.markdown("""
        1. **Ingestion Layer:** Multi-format PDF ingestion.
        2. **Parsing Layer:** Table detection and bounding box extraction.
        3. **Mapping Layer:** Key-value pair extraction to schema.
        4. **Validation Layer:** Cross-document reconciliation.
        5. **Review Layer:** Operator approval interface.
        """)

# --- DOCUMENT MANAGEMENT ---
elif view == "Document Management":
    st.header("Document Ingestion")
    st.write("Upload source files or monitor automated ingestion feeds.")
    
    col_up1, col_up2 = st.columns([3, 1])
    with col_up1:
        uploaded_file = st.file_uploader("Upload PDF Document", type=["pdf"])
        if uploaded_file is not None:
            if st.button("Run Processing Pipeline"):
                new_doc = {
                    "Doc_ID": f"DOC-0{len(st.session_state.docs_db)+1}",
                    "Filename": uploaded_file.name,
                    "Pages": 120,
                    "Date_Uploaded": datetime.now().strftime("%Y-%m-%d"),
                    "Status": "Processed",
                    "Type": "User Upload"
                }
                st.session_state.docs_db = pd.concat([st.session_state.docs_db, pd.DataFrame([new_doc])], ignore_index=True)
                st.success(f"Ingested and indexed `{uploaded_file.name}`.")
                st.rerun()
                
    with col_up2:
        st.write("### Actions")
        if st.button("Run External Crawler", use_container_width=True):
            st.info("Scanning configured file repositories...")

    st.divider()
    st.dataframe(st.session_state.docs_db, use_container_width=True, hide_index=True)

# --- FACT DATABASE ---
elif view == "Fact Database":
    st.header("Fact Index")
    st.write("Extracted data points mapped directly to original page coordinates and tables.")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        entity_filter = st.multiselect("Entity", options=st.session_state.facts_db["Entity"].unique(), default=st.session_state.facts_db["Entity"].unique())
    with col_f2:
        status_filter = st.multiselect("Status", options=st.session_state.facts_db["Status"].unique(), default=st.session_state.facts_db["Status"].unique())
    with col_f3:
        search_term = st.text_input("Filter Metric Name", "")

    df_filtered = st.session_state.facts_db[
        (st.session_state.facts_db["Entity"].isin(entity_filter)) &
        (st.session_state.facts_db["Status"].isin(status_filter)) &
        (st.session_state.facts_db["Metric"].str.contains(search_term, case=False))
    ]

    def style_status(val):
        if val == 'Verified':
            return 'background-color: #EDF7ED; color: #1E4620; font-weight: 500;'
        elif val == 'Conflict':
            return 'background-color: #FDF2F2; color: #9B1C1C; font-weight: 500;'
        return 'background-color: #FEF3C7; color: #92400E;'

    st.dataframe(
        df_filtered.style.map(style_status, subset=['Status']), 
        use_container_width=True, 
        hide_index=True
    )
    
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button("Export Dataset (CSV)", data=csv, file_name="extracted_facts.csv", mime="text/csv")

# --- ANALYTICS & VARIANCE ---
elif view == "Analytics & Variance":
    st.header("Metric Analysis")
    
    clean_df = st.session_state.facts_db[st.session_state.facts_db['Status'] == 'Verified']
    
    selected_metric = st.selectbox("Target Metric:", clean_df["Metric"].unique())
    metric_subset = clean_df[clean_df["Metric"] == selected_metric].sort_values(by="Year")
    
    if not metric_subset.empty:
        st.subheader("Variance Calculation")
        bhp_data = metric_subset[metric_subset["Entity"] == "BHP"]
        
        if len(bhp_data) >= 2:
            val_22 = bhp_data[bhp_data["Year"] == "2022"]["Value"].values[0]
            val_23 = bhp_data[bhp_data["Year"] == "2023"]["Value"].values[0]
            diff = val_23 - val_22
            pct = (diff / val_22) * 100
            
            unit = bhp_data["Unit"].iloc[0]
            
            c_m1, c_m2 = st.columns(2)
            c_m1.info(f"**BHP {selected_metric} Change (2022 to 2023):** +{diff:.2f} {unit} (+{pct:.2f}%)")
            c_m2.caption(f"**Source Document:** `{bhp_data['Document'].iloc[0]}` (Page {bhp_data['Page'].iloc[0]})")

        st.divider()
        st.subheader("Visualizations")
        
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
                    color_discrete_sequence=["#1E3A8A", "#0D9488"],
                    title=f"2023 {selected_metric}"
                )
                fig_bar.update_layout(yaxis_title=data_2023["Unit"].iloc[0], showlegend=False, template="plotly_white")
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("No 2023 data points available.")
                
        with col_v2:
            st.markdown("**Historical Trajectory**")
            data_trend = metric_subset[metric_subset["Entity"] == "BHP"]
            if not data_trend.empty:
                fig_line = px.line(
                    data_trend, 
                    x="Year", 
                    y="Value", 
                    markers=True,
                    title=f"BHP {selected_metric} Trend"
                )
                fig_line.update_traces(line_color="#1E3A8A", line_width=2, marker=dict(size=8))
                fig_line.update_layout(yaxis_title=data_trend["Unit"].iloc[0], template="plotly_white")
                st.plotly_chart(fig_line, use_container_width=True)
            else:
                st.info("Insufficient data points for trend visual.")

# --- DATA CONFLICTS ---
elif view == "Data Conflicts":
    st.header("Conflict Review Interface")
    st.write("Review discrepancies detected between different document sources for identical metrics.")
    
    conflicts = st.session_state.facts_db[st.session_state.facts_db["Status"] == "Conflict"]
    
    if not conflicts.empty:
        for idx, conflict_row in conflicts.iterrows():
            st.error(f"Data Mismatch: {conflict_row['Metric']} ({conflict_row['Entity']}, {conflict_row['Year']})")
            
            opposing_fact = st.session_state.facts_db[
                (st.session_state.facts_db["Metric"] == conflict_row["Metric"]) &
                (st.session_state.facts_db["Entity"] == conflict_row["Entity"]) &
                (st.session_state.facts_db["Year"] == conflict_row["Year"]) &
                (st.session_state.facts_db["Fact_ID"] != conflict_row["Fact_ID"])
            ].iloc[0]
            
            col_c1, col_c2 = st.columns(2)
            
            with col_c1:
                st.markdown("**Candidate Record A**")
                st.metric(label="Extracted Value", value=f"{opposing_fact['Value']} {opposing_fact['Unit']}")
                st.write(f"**File:** `{opposing_fact['Document']}`")
                st.write(f"**Location:** Page {opposing_fact['Page']}, {opposing_fact['Location']}")
                st.write(f"**Extraction Score:** {opposing_fact['Confidence']*100:.0f}%")
                
                if st.button(f"Approve Record A ({opposing_fact['Value']} {opposing_fact['Unit']})", key=f"btn_{opposing_fact['Fact_ID']}"):
                    resolve_conflict(opposing_fact['Fact_ID'], conflict_row['Fact_ID'])
                    
            with col_c2:
                st.markdown("**Candidate Record B**")
                st.metric(label="Extracted Value", value=f"{conflict_row['Value']} {conflict_row['Unit']}")
                st.write(f"**File:** `{conflict_row['Document']}`")
                st.write(f"**Location:** Page {conflict_row['Page']}, {conflict_row['Location']}")
                st.write(f"**Extraction Score:** {conflict_row['Confidence']*100:.0f}%")
                
                if st.button(f"Approve Record B ({conflict_row['Value']} {conflict_row['Unit']})", key=f"btn_{conflict_row['Fact_ID']}"):
                    resolve_conflict(conflict_row['Fact_ID'], opposing_fact['Fact_ID'])
    else:
        st.success("No active data conflicts in database.")
        if st.button("Simulate Test Conflict"):
            st.session_state.facts_db.loc[st.session_state.facts_db['Fact_ID'] == 'F-001', 'Status'] = 'Verified'
            st.session_state.facts_db.loc[st.session_state.facts_db['Fact_ID'] == 'F-005', 'Status'] = 'Conflict'
            st.rerun()

# --- AUTOMATED REPORTS ---
elif view == "Automated Reports":
    st.header("Report Output & Source Auditing")
    st.write("Dynamic text output mapped directly to verified data records.")
    
    col_rep1, col_rep2 = st.columns([3, 1])
    with col_rep2:
        st.button("Refresh Content", use_container_width=True)
        st.button("Export Summary (PDF)", use_container_width=True)
        
    with col_rep1:
        bhp_23_fact = st.session_state.facts_db[st.session_state.facts_db['Fact_ID'] == 'F-001'].iloc[0]
        bhp_22_fact = st.session_state.facts_db[st.session_state.facts_db['Fact_ID'] == 'F-002'].iloc[0]
        rio_23_fact = st.session_state.facts_db[st.session_state.facts_db['Fact_ID'] == 'F-004'].iloc[0]
        rev_fact = st.session_state.facts_db[st.session_state.facts_db['Fact_ID'] == 'F-003'].iloc[0]
        
        calc_change = ((bhp_23_fact['Value'] - bhp_22_fact['Value']) / bhp_22_fact['Value']) * 100
        
        st.markdown("---")
        st.markdown(f"""
        ### Operational Performance Summary (FY 2023)
        
        **1. Production Volumes**
        For the 2023 fiscal year, **BHP** reported an Iron Ore Production figure of 
        <span class='badge-verified' title='Source: {bhp_23_fact["Document"]} | Page {bhp_23_fact["Page"]}'>
        {bhp_23_fact["Value"]} {bhp_23_fact["Unit"]}
        </span>. This represents a YoY variance of 
        <span class='badge-verified' title='Calculated from records F-001 and F-002'>
        +{calc_change:.2f}%
        </span> 
        compared to the FY 2022 total of 
        <span class='badge-verified' title='Source: {bhp_22_fact["Document"]} | Page {bhp_22_fact["Page"]}'>
        {bhp_22_fact["Value"]} {bhp_22_fact["Unit"]}
        </span>.
        
        Over the same reporting timeframe, **Rio Tinto** registered production of 
        <span class='badge-verified' title='Source: {rio_23_fact["Document"]} | Page {rio_23_fact["Page"]}'>
        {rio_23_fact["Value"]} {rio_23_fact["Unit"]}
        </span>.
        
        **2. Financial Figures**
        * **Consolidated Revenue:** BHP reported total revenue of 
          <span class='badge-verified' title='Source: {rev_fact["Document"]} | Page {rev_fact["Page"]}'>
          {rev_fact["Value"]} {rev_fact["Unit"]}
          </span>.
        * **Audit Status:** All extracted values have passed validation rules. Discrepancies between interim quarterly operational reviews and full-year financial statements have been cataloged for operator review.
        
        ---
        *Hover over highlighted values to inspect primary document references.*
        """, unsafe_allow_html=True)
