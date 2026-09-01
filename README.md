# PRITHVI AI

Prithvi AI is an enterprise-grade, verifiable document processing and data extraction engine built for complex corporate, financial, and industrial PDF documents (e.g., Annual Reports, Quarterly Summaries, SEC filings). 

The platform extracts structured metrics while preserving full spatial and textual provenance (document name, page number, and table cell coordinate). It features automated YoY variance calculations, visual analytics, cross-document conflict detection, and an interactive human-in-the-loop resolution workflow.

---

## Key Features

* **Verifiable Data Ingestion & Indexing:** Maps extracted metrics directly to source file metadata, page numbers, and table cell locations (`Table 3, Cell B4`).
* **Interactive Fact Inspector:** Browse, search, filter, and export the structured fact database to CSV with live status tracking (`Verified`, `Conflict`, `Pending`).
* **Deterministic Analytics & YoY Variance:** Automatically computes year-over-year production and financial variances without LLM hallucination risks.
* **Human-in-the-Loop Conflict Resolution:** Flags discrepancies between conflicting sources (e.g., preliminary Q4 reviews vs. final audited annual reports) and provides side-by-side approval controls.
* **Auditable Dynamic Reporting:** Generates dynamic executive summaries where numbers feature interactive badges displaying exact source document evidence on hover.
* **Clean Enterprise UI:** Modern, lightweight interface styled without visual bloat for professional auditing environments.

---

## Architecture Overview

```text
 ┌────────────────────────┐
 │   PDF Source Documents │ (Annual Reports, Quarterly Summaries)
 └───────────┬────────────┘
             │
             ▼
 ┌────────────────────────┐
 │ Ingestion & Parsing    │ (Structure & Bounding Box Extraction)
 └───────────┬────────────┘
             │
             ▼
 ┌────────────────────────┐
 │ Fact Schema Mapping    │ (Metric, Value, Unit, Page, Cell Coordinates)
 └───────────┬────────────┘
             │
             ▼
 ┌────────────────────────┐
 │ Multi-Doc Validation   │ ──► Conflict Detected? ──► [ Conflict Resolution View ]
 └───────────┬────────────┘                                        │
             │ Approved                                            │ Resolved
             ▼                                                     ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │               In-Memory State / Fact Database (facts_db)                │
 └───────┬───────────────────────────────┬────────────────────────┬───────┘
         │                               │                        │
         ▼                               ▼                        ▼
 ┌───────────────┐               ┌───────────────┐        ┌───────────────┐
 │ Fact Inspector│               │Analytics Engine│       │ Dynamic Report│
 └───────────────┘               └───────────────┘        └───────────────┘


### Module Breakdown

#### 1. Control Dashboard
Displays macro-level system indicators: total ingested documents, total facts, overall verification percentage, active conflicts count, and system architecture stage breakdown.

#### 2. Document Repository
Allows operators to drag-and-drop new PDF documents into the pipeline or trigger external web scraping runs across public financial repositories (SEC EDGAR, ASX).

#### 3. Fact Inspector
Provides a grid view of all extracted metrics with multi-select dropdown filters by Entity, Verification Status, and text search across Metric names. Includes a single-click CSV exporter.

#### 4. Analytics & Variance
Calculates year-over-year production variances deterministically between fiscal periods and renders cross-entity bar charts and multi-year trend lines using Plotly.

#### 5. Conflict Resolution
Flags overlapping facts with conflicting values (e.g., preliminary vs. audited values). Displays side-by-side comparative cards with extraction confidence scores and source locations for one-click operator resolution.

#### 6. Dynamic Reports
Generates executive text summaries where every figure is enclosed in custom CSS badges. Hovering over a badge displays a native browser tooltip containing the original document filename and page number.
