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

<img width="956" height="431" alt="Screenshot 2026-09-01 234724" src="https://github.com/user-attachments/assets/2d3dd923-dd86-463d-ba3e-ddc0379a4b81" />
<img width="938" height="392" alt="Screenshot 2026-09-01 234707" src="https://github.com/user-attachments/assets/740e29ad-d7fe-425a-bf8e-adada6510143" />
<img width="957" height="442" alt="Screenshot 2026-09-01 234657" src="https://github.com/user-attachments/assets/be2bc73b-309a-4a1c-bc38-fa0011c449c4" />
<img width="901" height="425" alt="Screenshot 2026-09-01 234645" src="https://github.com/user-attachments/assets/d181efbd-623a-46d5-8927-87148b7c8e94" />
<img width="952" height="430" alt="Screenshot 2026-09-01 234745" src="https://github.com/user-attachments/assets/d49384fa-0b76-430c-bcc8-52ea0935176b" />
<img width="932" height="426" alt="Screenshot 2026-09-01 234737" src="https://github.com/user-attachments/assets/7dda1c25-abb3-415e-9384-c00b44e84daf" />

