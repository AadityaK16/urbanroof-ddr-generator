# DDR Report Generator — AI-Powered Property Diagnostic Report System

> **AI Generalist Assignment | UrbanRoof Private Limited**
> Converts raw site inspection data + thermal imaging data into a structured, client-ready Detailed Diagnostic Report (DDR) PDF.

---

## What This Does

This system reads two raw input documents:
- **Sample Report** (site inspection observations, area-wise findings, checklists)
- **Thermal Images Report** (thermal camera readings, hotspot/coldspot temperatures)

And generates a single **professional DDR PDF** containing:
1. Property Issue Summary
2. Area-wise Observations (with inspection photos + thermal images embedded)
3. Probable Root Cause Analysis
4. Severity Assessment (HIGH / MEDIUM / LOW with reasoning)
5. Recommended Actions (Immediate / Short-term / Long-term)
6. Additional Notes
7. Missing or Unclear Information (explicitly marked "Not Available")

---

## How It Works

```
Sample Report.pdf      ──┐
                         ├──► [PDF Extractor] ──► [AI Analysis] ──► [PDF Builder] ──► Final DDR.pdf
Thermal Images.pdf     ──┘         ↓                    ↓                 ↓
                               pdfplumber           Claude AI          reportlab
                               pdfimages           (reasoning +       (structured
                             (text + images)        structuring)        PDF output)
```

**Step 1 — Extraction:** `pdfplumber` and `pdfimages` extract all text and images from both input PDFs.

**Step 2 — AI Analysis:** Claude AI (via claude.ai) reads and reasons over both documents — merging observations, identifying root causes, assessing severity, and generating recommendations. The AI output is structured into the 7 DDR sections.

**Step 3 — PDF Generation:** `reportlab` assembles the final DDR PDF with branded formatting, colour-coded severity tables, and images placed in the correct sections.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10+ | Core language |
| pdfplumber | Extract text and images from input PDFs |
| pdfimages (poppler-utils) | Extract embedded images from PDFs |
| Pillow (PIL) | Image processing and format conversion |
| reportlab | Generate the final professional PDF output |
| Claude AI | Document reasoning, structuring, and report generation |

---

## Project Structure

```
urbanroof-ddr/
├── build_ddr.py              # Main script — runs the full pipeline
├── Sample Report.pdf         # Input: site inspection report
├── Thermal Images.pdf        # Input: thermal imaging report
├── extracted_images/
│   ├── sample/               # Auto-generated: inspection photos
│   └── thermal/              # Auto-generated: thermal camera images
├── DDR_Report_Flat103.pdf    # Output: final client-ready DDR
└── README.md
```

---

## Setup & Usage

### 1. Install dependencies

```bash
pip install pdfplumber pypdf pillow reportlab
```

On Ubuntu/Debian, also install poppler for image extraction:
```bash
sudo apt install poppler-utils
```

On Windows, download poppler from: https://github.com/oschwartz10612/poppler-windows/releases

### 2. Place your input files

Put your inspection PDF and thermal PDF in the same folder as `build_ddr.py`.
Update the paths at the top of `build_ddr.py` if needed:

```python
BASE      = "/path/to/your/folder"
SAMP_PDF  = f"{BASE}/Sample Report.pdf"
THERM_PDF = f"{BASE}/Thermal Images.pdf"
OUT_PDF   = f"{BASE}/DDR_Report_Output.pdf"
```

### 3. Extract images from PDFs

```bash
mkdir -p extracted_images/sample extracted_images/thermal
pdfimages -j "Sample Report.pdf" extracted_images/sample/img
pdfimages -j "Thermal Images.pdf" extracted_images/thermal/img
```

### 4. Run the report generator

```bash
python3 build_ddr.py
```

Output: `DDR_Report_Flat103.pdf` — a fully formatted, client-ready report.

---

## Sample Output

The generated DDR includes:

- **Cover page** with property details, inspection stats, and disclaimer
- **Colour-coded severity table** (RED = HIGH, AMBER = MEDIUM, GREEN = LOW)
- **7 area-wise observation sections** each with inspection photos and thermal images
- **Root cause analysis** in plain, client-friendly language
- **Prioritised action plan** (Immediate → Short-term → Long-term)
- **Missing information** clearly flagged as "Not Available"

---

## Design Decisions

**Why no live API calls in the script?**
The AI reasoning step (document analysis, structuring, root cause identification) was performed using Claude AI. The script handles extraction and PDF generation deterministically — making it fast, reliable, and free to run without API credits.

For a production version, the AI step can be integrated as an API call:
```python
import anthropic
client = anthropic.Anthropic(api_key="your-key")
# Send extracted text → receive structured DDR sections → pass to PDF builder
```

**Why reportlab over other PDF libraries?**
reportlab gives precise control over layout, fonts, colours, and image placement — essential for a professional client-deliverable report with branded formatting.

**Why pdfimages over pdfplumber for image extraction?**
pdfimages (poppler) extracts images at original resolution and quality. pdfplumber is used for text extraction where its layout-awareness is superior.

---

## Limitations

- Client name and contact details were not present in the source documents (redacted) — marked as "Not Available" in the report
- Thermal image-to-room mapping is approximate (inferred from inspection sequence order)
- The system currently handles one flat per run — batch processing across multiple flats would require a loop over input file pairs
- Cross-flat issues (e.g. Flat 203 leakage) are flagged but cannot be resolved programmatically

## How I Would Improve It

- Add an API call layer so the AI analysis step runs automatically on any new input PDFs
- Build a simple web UI (Streamlit or Flask) where inspectors upload PDFs and download the DDR
- Add OCR support for scanned/image-based PDFs using pytesseract
- Auto-match thermal images to rooms using image filename timestamps vs inspection timestamps
- Add a database layer to store historical DDRs and track issue resolution over time

---

## Author

Built as part of the AI Generalist / Applied AI Builder assignment for UrbanRoof Private Limited.
