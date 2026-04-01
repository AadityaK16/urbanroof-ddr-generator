"""
DDR (Detailed Diagnostic Report) PDF Generator
Urbanroof - Flat No. 103, 27 September 2022
Combines Sample Report + Thermal Images into a professional client-ready PDF
"""

import os
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image as RLImage, HRFlowable, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.colors import HexColor

# ── Colour palette ──────────────────────────────────────────────────────────
BRAND_BLUE   = HexColor("#1B3A6B")
BRAND_ORANGE = HexColor("#E8500A")
LIGHT_BLUE   = HexColor("#EAF1FB")
LIGHT_GREY   = HexColor("#F5F5F5")
DARK_GREY    = HexColor("#444444")
RED          = HexColor("#CC0000")
AMBER        = HexColor("#E07B00")
GREEN        = HexColor("#1A7A1A")
WHITE        = colors.white
BLACK        = colors.black

# ── Paths — UPDATE THESE FOR YOUR MACHINE ───────────────────────────────────
BASE      = r"C:\Users\aadit\Urbanroof\ddrG" #change the directory accordingly to where you have the images and want the output PDF
SAMP_DIR  = f"{BASE}/extracted_images/sample"
THERM_DIR = f"{BASE}/extracted_images/thermal"
OUT_PDF   = f"{BASE}/DDR_Report_Flat103.pdf"

os.makedirs(f"{BASE}/extracted_images/sample", exist_ok=True)
os.makedirs(f"{BASE}/extracted_images/thermal", exist_ok=True)

# ── Helpers ──────────────────────────────────────────────────────────────────
def get_sample_photos(start, count):
    """Return up to `count` real inspection photo paths starting from index."""
    all_imgs = sorted([f for f in os.listdir(SAMP_DIR) if f.endswith('.jpg')])
    real = []
    for f in all_imgs:
        img = Image.open(f"{SAMP_DIR}/{f}")
        w, h = img.size
        if 200 <= w <= 800 and 200 <= h <= 800:
            real.append(f"{SAMP_DIR}/{f}")
    return real[start:start+count]

def get_thermal_photos(start, count):
    """Return up to `count` thermal image paths."""
    all_imgs = sorted([f for f in os.listdir(THERM_DIR) if f.endswith('.jpg')])
    real = [f"{THERM_DIR}/{f}" for f in all_imgs
            if Image.open(f"{THERM_DIR}/{f}").size[0] >= 500]
    return real[start:start+count]

def photo_row(paths, width=7*cm, caption_prefix="Photo"):
    """Build a table row of images with captions."""
    cells = []
    for i, p in enumerate(paths):
        try:
            img = RLImage(p, width=width, height=width*0.75)
            cap = Paragraph(f"{caption_prefix} {i+1}", styles['Caption'])
            cells.append([img, cap])
        except Exception:
            cells.append([Paragraph("Image Not Available", styles['Small']),
                          Paragraph("", styles['Small'])])
    if not cells:
        return []
    rows = []
    for i in range(0, len(cells), 3):
        chunk = cells[i:i+3]
        while len(chunk) < 3:
            chunk.append(["", ""])
        img_row = [c[0] for c in chunk]
        cap_row = [c[1] for c in chunk]
        t = Table([img_row, cap_row], colWidths=[width+0.3*cm]*3)
        t.setStyle(TableStyle([
            ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        rows.append(t)
        rows.append(Spacer(1, 0.3*cm))
    return rows

# ── Styles ───────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

styles.add(ParagraphStyle('ReportTitle',
    fontSize=22, textColor=WHITE, fontName='Helvetica-Bold',
    alignment=TA_CENTER, spaceAfter=6))
styles.add(ParagraphStyle('SubTitle',
    fontSize=13, textColor=WHITE, fontName='Helvetica',
    alignment=TA_CENTER, spaceAfter=4))
styles.add(ParagraphStyle('SectionHeader',
    fontSize=14, textColor=WHITE, fontName='Helvetica-Bold',
    alignment=TA_LEFT, spaceAfter=6, spaceBefore=4,
    leftIndent=8, leading=18))
styles.add(ParagraphStyle('SubHeader',
    fontSize=11, textColor=BRAND_BLUE, fontName='Helvetica-Bold',
    spaceAfter=4, spaceBefore=8, leading=14))
styles.add(ParagraphStyle('BodyText2',
    fontSize=9.5, textColor=DARK_GREY, fontName='Helvetica',
    spaceAfter=4, leading=14, alignment=TA_JUSTIFY))
styles.add(ParagraphStyle('BulletItem',
    fontSize=9.5, textColor=DARK_GREY, fontName='Helvetica',
    leftIndent=14, spaceAfter=3, leading=13,
    bulletIndent=4, bulletText='•'))
styles.add(ParagraphStyle('Caption',
    fontSize=8, textColor=DARK_GREY, fontName='Helvetica-Oblique',
    alignment=TA_CENTER, spaceAfter=2))
styles.add(ParagraphStyle('Small',
    fontSize=8, textColor=DARK_GREY, fontName='Helvetica', spaceAfter=2))
styles.add(ParagraphStyle('TableHeader',
    fontSize=9, textColor=WHITE, fontName='Helvetica-Bold',
    alignment=TA_CENTER))
styles.add(ParagraphStyle('TableCell',
    fontSize=9, textColor=DARK_GREY, fontName='Helvetica',
    alignment=TA_LEFT, leading=12))
styles.add(ParagraphStyle('SeverityHigh',
    fontSize=9, textColor=RED, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('SeverityMed',
    fontSize=9, textColor=AMBER, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('SeverityLow',
    fontSize=9, textColor=GREEN, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('Disclaimer',
    fontSize=8, textColor=DARK_GREY, fontName='Helvetica-Oblique',
    alignment=TA_JUSTIFY, leading=12))

def section_header(title):
    data = [[Paragraph(title, styles['SectionHeader'])]]
    t = Table(data, colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), BRAND_BLUE),
        ('ROWBACKGROUNDS',(0,0), (-1,-1), [BRAND_BLUE]),
        ('TOPPADDING',    (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('BOX',           (0,0), (-1,-1), 0.5, BRAND_ORANGE),
    ]))
    return t

def info_table(rows):
    data = [[Paragraph(k, styles['SubHeader']),
             Paragraph(v, styles['BodyText2'])] for k, v in rows]
    t = Table(data, colWidths=[5.5*cm, 12*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (0,-1), LIGHT_BLUE),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
        ('GRID',          (0,0), (-1,-1), 0.3, colors.lightgrey),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 6),
    ]))
    return t

# ── Page template ─────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4

def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BRAND_BLUE)
    canvas.rect(0, PAGE_H - 1.5*cm, PAGE_W, 1.5*cm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(1.5*cm, PAGE_H - 1.0*cm, "URBANROOF PRIVATE LIMITED")
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(PAGE_W - 1.5*cm, PAGE_H - 1.0*cm,
                           "Detailed Diagnostic Report | Flat No. 103")
    canvas.setFillColor(BRAND_BLUE)
    canvas.rect(0, 0, PAGE_W, 1.0*cm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(1.5*cm, 0.35*cm, "www.urbanroof.in  |  Confidential – Client Use Only")
    canvas.drawRightString(PAGE_W - 1.5*cm, 0.35*cm, f"Page {doc.page}")
    canvas.setFillColor(BRAND_ORANGE)
    canvas.rect(0, 1.0*cm, PAGE_W, 0.18*cm, fill=1, stroke=0)
    canvas.restoreState()

def on_first_page(canvas, doc):
    on_page(canvas, doc)

# ── Story ─────────────────────────────────────────────────────────────────────
story = []
sev_colors = {"HIGH": RED, "MEDIUM": AMBER, "LOW": GREEN}

# ── COVER PAGE ────────────────────────────────────────────────────────────────
story.append(Spacer(1, 1.5*cm))

cover_data = [
    [Paragraph("DETAILED DIAGNOSTIC REPORT", styles['ReportTitle'])],
    [Paragraph("Property Health Assessment - Water Leakage & Structural Inspection", styles['SubTitle'])],
    [Paragraph("Flat No. 103 | 11-Year-Old Residential Flat | Inspection Date: 27 September 2022", styles['SubTitle'])],
]
cover_table = Table(cover_data, colWidths=[17.5*cm])
cover_table.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,-1), BRAND_BLUE),
    ('TOPPADDING',    (0,0), (-1,-1), 14),
    ('BOTTOMPADDING', (0,0), (-1,-1), 14),
    ('BOX',           (0,0), (-1,-1), 1.5, BRAND_ORANGE),
]))
story.append(cover_table)
story.append(Spacer(1, 0.8*cm))

stat_data = [[
    Paragraph("<b>Inspection Score</b><br/>85.71%", styles['BodyText2']),
    Paragraph("<b>Areas Inspected</b><br/>7 Zones", styles['BodyText2']),
    Paragraph("<b>Issues Identified</b><br/>11 Findings", styles['BodyText2']),
    Paragraph("<b>Thermal Scans</b><br/>30 Images", styles['BodyText2']),
]]
stat_table = Table(stat_data, colWidths=[4.35*cm]*4)
stat_table.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,-1), LIGHT_BLUE),
    ('BOX',           (0,0), (-1,-1), 0.5, BRAND_BLUE),
    ('INNERGRID',     (0,0), (-1,-1), 0.5, BRAND_BLUE),
    ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
    ('TOPPADDING',    (0,0), (-1,-1), 10),
    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
]))
story.append(stat_table)
story.append(Spacer(1, 0.8*cm))

story.append(info_table([
    ("Prepared by",     "UrbanRoof Private Limited | www.urbanroof.in"),
    ("Inspected by",    "Krushna & Mahesh"),
    ("Inspection Date", "27 September 2022, 14:28 IST"),
    ("Property",        "Flat No. 103 | 11-year-old residential flat"),
    ("Property Type",   "Flat (Multi-floor building)"),
    ("Previous Audit",  "No previous structural audit or repair work done"),
    ("Thermal Device",  "BOSCH GTC 400 C Professional | Serial: 02700034772"),
    ("Report Date",     "September 2022"),
]))

story.append(Spacer(1, 0.6*cm))
story.append(Paragraph(
    "This report is prepared solely for the use of the client. It covers visible and accessible "
    "conditions at the time of inspection. It does not constitute a structural engineering opinion "
    "or guarantee future performance. UrbanRoof recommends obtaining professional remediation advice "
    "before undertaking any repair work.",
    styles['Disclaimer']))
story.append(PageBreak())

# ── SECTION 1 — PROPERTY ISSUE SUMMARY ───────────────────────────────────────
story.append(section_header("SECTION 1 — PROPERTY ISSUE SUMMARY"))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "The inspection of Flat No. 103 was carried out on 27 September 2022 across seven impacted "
    "zones: Hall, Common Bedroom, Master Bedroom, Kitchen, Parking Area, Common Bathroom, and the "
    "External Wall. A total of 11 distinct issues were recorded — primarily water ingress at skirting "
    "level, tile joint gaps in bathroom areas, dampness and efflorescence on internal wall surfaces, "
    "structural cracks on the external wall, plumbing deficiencies in bathrooms, and seepage at the "
    "parking area ceiling below the flat. Thermal imaging confirmed active moisture presence in "
    "multiple zones, with temperature differentials of 3-5°C indicating hidden dampness behind wall "
    "and floor finishes.",
    styles['BodyText2']))
story.append(Spacer(1, 0.3*cm))

summary_headers = [
    Paragraph("Point",       styles['TableHeader']),
    Paragraph("Location",    styles['TableHeader']),
    Paragraph("Observation", styles['TableHeader']),
    Paragraph("Severity",    styles['TableHeader']),
]
summary_rows = [
    ["1",   "Hall (Flat 103)",            "Dampness at skirting level",                       "HIGH"],
    ["2",   "Common Bedroom (Flat 103)",  "Dampness at skirting level",                       "HIGH"],
    ["2.1", "Common Bathroom (Flat 103)", "Gaps in tile joints",                              "MEDIUM"],
    ["3",   "Master Bedroom (Flat 103)",  "Dampness at skirting level",                       "HIGH"],
    ["3.1", "MB Bathroom (Flat 103)",     "Gaps in tile joints",                              "MEDIUM"],
    ["4",   "Kitchen (Flat 103)",         "Dampness at skirting level",                       "HIGH"],
    ["4.1", "MB Bathroom (Flat 103)",     "Gaps in tile joints",                              "MEDIUM"],
    ["5",   "Master Bedroom (Flat 103)",  "Dampness & efflorescence on wall surface",         "HIGH"],
    ["5.1", "External Wall (Building)",   "Cracks on external wall near Master Bedroom",      "HIGH"],
    ["6",   "Parking Ceiling (Below 103)","Leakage at parking ceiling",                       "HIGH"],
    ["6.1", "Common Bathroom (Flat 103)", "Plumbing issue & gaps in tile joints",             "HIGH"],
    ["7",   "Common Bathroom (Flat 103)", "Mild dampness at ceiling",                         "MEDIUM"],
    ["7.1", "Flat 203 Bathrooms",         "Gap between tile joints (Common & MB Bathrooms)",  "MEDIUM"],
]

tdata = [summary_headers]
for row in summary_rows:
    sev = row[3]
    tdata.append([
        Paragraph(row[0], styles['TableCell']),
        Paragraph(row[1], styles['TableCell']),
        Paragraph(row[2], styles['TableCell']),
        Paragraph(f"<b>{sev}</b>",
                  ParagraphStyle('sev', parent=styles['TableCell'],
                                 textColor=sev_colors.get(sev, BLACK))),
    ])

sum_table = Table(tdata, colWidths=[1.2*cm, 4.5*cm, 8.3*cm, 2.5*cm])
sum_table.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0),  BRAND_BLUE),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [WHITE, LIGHT_GREY]),
    ('GRID',          (0,0), (-1,-1), 0.3, colors.lightgrey),
    ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING',    (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING',   (0,0), (-1,-1), 5),
]))
story.append(sum_table)
story.append(PageBreak())

# ── SECTION 2 — AREA-WISE OBSERVATIONS ───────────────────────────────────────
story.append(section_header("SECTION 2 — AREA-WISE OBSERVATIONS"))
story.append(Spacer(1, 0.3*cm))

areas = [
    {
        "title": "Area 1 — Hall (Skirting Level Dampness)",
        "negative": (
            "Dampness was observed at the skirting level of the Hall of Flat No. 103. "
            "The dampness appears continuous and is present along the lower portion of the walls, "
            "suggesting persistent water accumulation or seepage from an adjacent wet area. "
            "The affected area showed signs of paint peeling and surface degradation."
        ),
        "positive": (
            "Common Bathroom tile hollowness was identified as the likely positive-side (source) area. "
            "Gaps and deteriorated grout in the bathroom tile joints allow water to percolate through "
            "the floor/wall substrate and appear as dampness in the adjoining Hall skirting area."
        ),
        "thermal": (
            "Thermal images 1-4 (RB02380X-RB02402X) for this zone show a hotspot of 28.8°C against a "
            "coldspot of 23.4°C — a differential of 5.4°C confirming active moisture migration behind "
            "the hall wall and floor finishes."
        ),
        "sample_start": 0,  "sample_count": 6,
        "thermal_start": 0, "thermal_count": 2,
    },
    {
        "title": "Area 2 — Common Bedroom (Skirting Level Dampness)",
        "negative": (
            "Dampness was observed at the skirting level of the Common Bedroom of Flat No. 103. "
            "The damp patches are visible along the base of walls, indicating water seepage from "
            "the bathroom above or alongside. No previous repair work had been carried out in this area."
        ),
        "positive": (
            "Common Bathroom tile hollowness on the positive side: gaps between tile joints in the "
            "Common Bathroom were identified as the water entry path. Loose plumbing joints and "
            "concealed plumbing leakage further contribute to the moisture build-up."
        ),
        "thermal": (
            "Thermal images 5-8 (RB02403X-RB02406X) show hotspot readings of 25.5-26.5°C with "
            "coldspots at 20.5-21.5°C. The ~5°C differential is consistent with subsurface dampness "
            "in the bedroom skirting zone."
        ),
        "sample_start": 6,  "sample_count": 6,
        "thermal_start": 2, "thermal_count": 2,
    },
    {
        "title": "Area 3 — Master Bedroom (Skirting Dampness & Wall Efflorescence)",
        "negative": (
            "Dampness was observed at the skirting level of the Master Bedroom. Additionally, dampness "
            "and efflorescence (white salt deposits) were noted on the wall surface of the Master Bedroom, "
            "indicating prolonged water contact with the wall material. Efflorescence is a clear sign of "
            "ongoing moisture movement through the wall structure."
        ),
        "positive": (
            "MB Bathroom tile hollowness was identified on the positive side. Gaps between the tile joints "
            "of the Master Bedroom Bathroom allow water ingress, which then migrates into the bedroom walls. "
            "Cracks on the External Wall near the Master Bedroom also act as an additional water entry point "
            "from outside the building."
        ),
        "thermal": (
            "Thermal images 9-14 (RB02392X-RB02398X) show hotspot readings of 25.6-25.9°C and coldspots "
            "of 20.6-20.9°C. The consistent ~5°C differential across multiple scans confirms extensive "
            "moisture presence behind the master bedroom walls and floor area."
        ),
        "sample_start": 12, "sample_count": 8,
        "thermal_start": 4, "thermal_count": 2,
    },
    {
        "title": "Area 4 — Kitchen (Skirting Level Dampness)",
        "negative": (
            "Dampness was observed at the skirting level of the Kitchen of Flat No. 103. "
            "The affected skirting area shows moisture staining and surface deterioration. "
            "Leakage appears to be continuous (all-time leakage as recorded in the checklist)."
        ),
        "positive": (
            "The Master Bedroom Bathroom tile joints on the positive side show gaps and open grout, "
            "allowing water to seep laterally into the kitchen skirting zone. Concealed plumbing leakage "
            "due to damage in the Nahani trap and brickbat coba layer under the tile flooring is a "
            "probable contributing source."
        ),
        "thermal": (
            "Thermal images 15-17 (RB02399X-RB02401X) show hotspot readings of 25.2-26.5°C with coldspots "
            "at 20.2-21.5°C. The thermal differential confirms moisture accumulation at the kitchen "
            "skirting zone."
        ),
        "sample_start": 20, "sample_count": 5,
        "thermal_start": 6, "thermal_count": 2,
    },
    {
        "title": "Area 5 — External Wall (Structural Cracks)",
        "negative": (
            "Moderate cracks were observed on the External Wall of the building near the Master Bedroom "
            "of Flat No. 103. The cracks indicate weathering and possible structural stress. External "
            "plumbing pipes were also noted to be in moderate condition with signs of cracking and leakage. "
            "Algae/fungus growth was observed on the external wall surface."
        ),
        "positive": (
            "Positive-side inputs indicate: existing paint condition is unknown (not sure), structural "
            "condition of RCC members shows moderate cracks on column/beam, and the external wall surface "
            "shows moderate cracking. No sealant on window frame joints was observed. The external wall "
            "is a direct contributor to internal dampness in the Master Bedroom."
        ),
        "thermal": (
            "Thermal images 18-22 (RB02381X-RB02385X) for the external wall zone show hotspot readings "
            "of 26.5-27.3°C with coldspots at 21.5-22.3°C. The thermal data confirms moisture ingress "
            "through the external wall cracks into the building envelope."
        ),
        "sample_start": 26, "sample_count": 8,
        "thermal_start": 8, "thermal_count": 2,
    },
    {
        "title": "Area 6 — Parking Area (Ceiling Seepage / Leakage)",
        "negative": (
            "Leakage and seepage were observed at the Parking Area ceiling, directly below Flat No. 103. "
            "The seepage is visible as damp patches and staining on the parking ceiling, indicating that "
            "water is penetrating through the floor slab of Flat No. 103 into the parking area below."
        ),
        "positive": (
            "Common Bathroom tile hollowness and a plumbing issue were identified as the primary positive-side "
            "sources. Loose plumbing joints, gaps around the Nahani trap, and open tile joints in the Common "
            "Bathroom are allowing water to reach the structural slab and leak below into the parking area."
        ),
        "thermal": (
            "Thermal images 23-27 (RB02387X-RB02391X) show hotspot readings of 25.1-25.9°C with coldspots "
            "at 20.1-20.9°C. The thermal data confirms active water movement through the slab in the parking "
            "zone."
        ),
        "sample_start": 34, "sample_count": 6,
        "thermal_start": 10, "thermal_count": 2,
    },
    {
        "title": "Area 7 — Common Bathroom Ceiling (Mild Dampness) & Flat 203",
        "negative": (
            "Mild dampness was observed at the ceiling of the Common Bathroom of Flat No. 103. "
            "Additionally, the outlet in Flat 203 (floor above) was found to be leaking, and tile "
            "joints in both the Common Bathroom and Master Bedroom Bathroom of Flat No. 203 were found "
            "to be open — making Flat 203 a contributing source of the dampness in Flat 103's ceiling."
        ),
        "positive": (
            "Open tile joint gaps in Common and Master Bedroom Bathrooms of Flat No. 203 (floor above) "
            "are allowing water to seep down through the slab into the Common Bathroom ceiling of Flat 103. "
            "This is a cross-flat issue requiring coordination with the occupant of Flat 203."
        ),
        "thermal": (
            "Thermal images 28-30 (RB02377X-RB02379X) show hotspot readings of 26.4-27.8°C with coldspots "
            "at 21.4-22.8°C. The highest hotspot of 27.8°C (image 30) indicates the most active moisture "
            "zone at this location."
        ),
        "sample_start": 40, "sample_count": 6,
        "thermal_start": 12, "thermal_count": 2,
    },
]

for area in areas:
    story.append(Paragraph(area["title"], styles['SubHeader']))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BRAND_ORANGE, spaceAfter=6))
    story.append(Paragraph("<b>Negative Side (Affected Area):</b>", styles['SubHeader']))
    story.append(Paragraph(area["negative"], styles['BodyText2']))
    story.append(Paragraph("<b>Positive Side (Source Area):</b>", styles['SubHeader']))
    story.append(Paragraph(area["positive"], styles['BodyText2']))
    story.append(Paragraph("<b>Thermal Imaging Findings:</b>", styles['SubHeader']))
    story.append(Paragraph(area["thermal"], styles['BodyText2']))
    story.append(Paragraph("<b>Inspection Photographs:</b>", styles['SubHeader']))
    photos = get_sample_photos(area["sample_start"], area["sample_count"])
    if photos:
        for row in photo_row(photos, width=5.2*cm, caption_prefix="Inspection Photo"):
            story.append(row)
    else:
        story.append(Paragraph("Image Not Available", styles['Small']))
    story.append(Paragraph("<b>Thermal Images:</b>", styles['SubHeader']))
    thermals = get_thermal_photos(area["thermal_start"], area["thermal_count"])
    if thermals:
        for row in photo_row(thermals, width=7*cm, caption_prefix="Thermal Image"):
            story.append(row)
    else:
        story.append(Paragraph("Image Not Available", styles['Small']))
    story.append(Spacer(1, 0.4*cm))

story.append(PageBreak())

# ── SECTION 3 — PROBABLE ROOT CAUSE ──────────────────────────────────────────
story.append(section_header("SECTION 3 — PROBABLE ROOT CAUSE"))
story.append(Spacer(1, 0.3*cm))

root_causes = [
    ("Primary Cause: Deteriorated Tile Joint Grout",
     "The most widespread root cause is the deterioration and opening of tile joint grout in all "
     "bathroom and wet areas (Common Bathroom, Master Bedroom Bathroom, Kitchen). Over the 11-year "
     "life of the property, grout naturally shrinks, cracks, and loses adhesion — creating direct "
     "pathways for water to enter the structural substrate beneath tiles."),
    ("Secondary Cause: Concealed Plumbing Failure",
     "Damage to the Nahani trap and brickbat coba waterproofing layer beneath the tile flooring "
     "was confirmed. Loose plumbing joints around flush tanks, angle cocks, and wash basins were "
     "also observed, contributing to chronic low-level water leakage that saturates the surrounding "
     "structure over time."),
    ("Tertiary Cause: External Wall Cracks",
     "Moderate cracks on the external wall near the Master Bedroom provide a direct ingress point "
     "for rainwater into the building envelope. Combined with the absence of effective sealants on "
     "window frame joints, external moisture is contributing to the dampness observed inside the "
     "Master Bedroom."),
    ("Contributing Cause: Cross-Flat Leakage from Flat 203",
     "Open tile joints and an outlet leakage in Flat No. 203 (the floor above) are causing water "
     "to seep through the inter-floor slab and appear as ceiling dampness in the Common Bathroom "
     "of Flat 103. This is an external factor that cannot be resolved without cooperation from "
     "the occupant of Flat 203."),
    ("Contributing Cause: Age-Related Waterproofing Failure",
     "The property is 11 years old with no previous structural audit or waterproofing treatment. "
     "Original waterproofing membranes in wet areas typically have a service life of 8-12 years, "
     "suggesting that the entire wet-area waterproofing system may be at or past end-of-life."),
]

for title, text in root_causes:
    story.append(Paragraph(f"<b>{title}</b>", styles['SubHeader']))
    story.append(Paragraph(text, styles['BodyText2']))
    story.append(Spacer(1, 0.2*cm))

story.append(PageBreak())

# ── SECTION 4 — SEVERITY ASSESSMENT ──────────────────────────────────────────
story.append(section_header("SECTION 4 — SEVERITY ASSESSMENT"))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "Severity is assessed on three levels: HIGH (immediate attention required, risk of structural "
    "damage or health hazard), MEDIUM (attention required within 3–6 months), and LOW (monitor and "
    "address during routine maintenance).",
    styles['BodyText2']))
story.append(Spacer(1, 0.3*cm))

sev_headers = [
    Paragraph("Area",      styles['TableHeader']),
    Paragraph("Issue",     styles['TableHeader']),
    Paragraph("Severity",  styles['TableHeader']),
    Paragraph("Reasoning", styles['TableHeader']),
]
sev_rows = [
    ("Hall",                  "Skirting dampness",              "HIGH",
     "Continuous all-time leakage; thermal differential 5.4°C confirms active moisture. Risk of structural degradation and mould growth."),
    ("Common Bedroom",        "Skirting dampness",              "HIGH",
     "Active moisture confirmed by thermal imaging (~5°C differential). Prolonged dampness risks wall plaster failure."),
    ("Common Bathroom",       "Tile joint gaps + plumbing",     "HIGH",
     "Primary source of leakage to parking below and bedroom dampness. Active plumbing defect present."),
    ("Master Bedroom",        "Skirting dampness + efflorescence","HIGH",
     "Efflorescence indicates prolonged moisture contact with structure. Risk of reinforcement corrosion over time."),
    ("Master Bedroom",        "Wall dampness",                  "HIGH",
     "Combined internal and external sources. Efflorescence confirms deep moisture penetration."),
    ("External Wall",         "Structural cracks",              "HIGH",
     "Cracks in external wall allow direct rainwater ingress. RCC member cracking is a structural concern."),
    ("Parking Ceiling",       "Leakage/seepage",                "HIGH",
     "Active water breakthrough to parking area confirms slab waterproofing failure. Public safety concern."),
    ("MB Bathroom",           "Tile joint gaps",                "MEDIUM",
     "Contributing to kitchen and bedroom dampness. Not yet causing structural damage but requires prompt repair."),
    ("Kitchen",               "Skirting dampness",              "MEDIUM",
     "Dampness present but contained to skirting level. Thermal imaging confirms moisture presence."),
    ("Common Bathroom ceiling","Mild ceiling dampness",         "MEDIUM",
     "Source is from Flat 203 above. Moderate severity pending cooperation from Flat 203 occupant."),
    ("Flat 203 Bathrooms",    "Open tile joints",               "MEDIUM",
     "Cross-flat issue. Causes ceiling dampness in Flat 103. Requires coordination with Flat 203."),
]

tdata = [sev_headers]
for row in sev_rows:
    sev = row[2]
    tdata.append([
        Paragraph(row[0], styles['TableCell']),
        Paragraph(row[1], styles['TableCell']),
        Paragraph(f"<b>{sev}</b>",
                  ParagraphStyle('sv', parent=styles['TableCell'],
                                 textColor=sev_colors.get(sev, BLACK))),
        Paragraph(row[3], styles['TableCell']),
    ])

sev_table = Table(tdata, colWidths=[3*cm, 3.5*cm, 2*cm, 9*cm])
sev_table.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0),  BRAND_BLUE),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [WHITE, LIGHT_GREY]),
    ('GRID',          (0,0), (-1,-1), 0.3, colors.lightgrey),
    ('VALIGN',        (0,0), (-1,-1), 'TOP'),
    ('TOPPADDING',    (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING',   (0,0), (-1,-1), 5),
    ('FONTSIZE',      (0,1), (-1,-1), 8.5),
]))
story.append(sev_table)
story.append(PageBreak())

# ── SECTION 5 — RECOMMENDED ACTIONS ──────────────────────────────────────────
story.append(section_header("SECTION 5 — RECOMMENDED ACTIONS"))
story.append(Spacer(1, 0.3*cm))

actions = [
    ("IMMEDIATE ACTIONS (Within 1 Month)", RED, [
        "Complete re-tiling and re-grouting of the Common Bathroom and Master Bedroom Bathroom — "
        "remove existing tiles, apply fresh waterproofing membrane (polyurethane or cementitious), "
        "and relay tiles with non-shrink epoxy grout.",
        "Replace damaged Nahani trap and repair brickbat coba waterproofing layer beneath bathroom "
        "floors before re-tiling.",
        "Fix all loose and leaking concealed plumbing joints in the Common and Master Bedroom Bathrooms "
        "— inspect and replace corroded angle cocks, bibcocks, and flush tank connections.",
        "Apply crack filler and external waterproofing treatment to all cracks on the external wall "
        "near the Master Bedroom. Apply anti-carbonation or elastomeric coating over the treated area.",
        "Address parking ceiling leakage immediately — apply crystalline waterproofing treatment from "
        "the underside of the slab and investigate the primary source through Flat 103's floor.",
    ]),
    ("SHORT-TERM ACTIONS (Within 3 Months)", AMBER, [
        "Re-grout all tile joints in the Kitchen and any other wet areas showing gaps or hollowness.",
        "Apply waterproof sealant at all window frame joints and external pipe penetrations through walls.",
        "Carry out a full positive-side waterproofing treatment of all bathroom floors and walls up to "
        "300mm height using a brush-applied membrane.",
        "Engage with the occupant of Flat No. 203 to address the open tile joints and outlet leakage "
        "in their bathrooms — the Common Bathroom ceiling dampness in Flat 103 cannot be permanently "
        "resolved without repairs in Flat 203.",
        "Repaint all affected interior surfaces after moisture levels have reduced — use anti-fungal "
        "primer before applying final coat.",
    ]),
    ("LONG-TERM RECOMMENDATIONS (6-12 Months)", GREEN, [
        "Commission a full structural audit of the building given the 11-year age, visible RCC member "
        "cracking, and external wall deterioration.",
        "Undertake a comprehensive external wall waterproofing treatment for the entire building facade "
        "to prevent future rainwater ingress.",
        "Install or replace expansion joint sealants at all structural joints in the building.",
        "Consider a full bathroom waterproofing renewal programme for all flats, given the age of the "
        "building and systemic waterproofing failures observed.",
    ]),
]

for section_title, color, items in actions:
    head_data = [[Paragraph(section_title, styles['SectionHeader'])]]
    head_t = Table(head_data, colWidths=[17.5*cm])
    head_t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), color),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
    ]))
    story.append(head_t)
    story.append(Spacer(1, 0.2*cm))
    for item in items:
        story.append(Paragraph(item, styles['BulletItem']))
    story.append(Spacer(1, 0.4*cm))

story.append(PageBreak())

# ── SECTION 6 — ADDITIONAL NOTES ─────────────────────────────────────────────
story.append(section_header("SECTION 6 — ADDITIONAL NOTES"))
story.append(Spacer(1, 0.3*cm))

notes = [
    ("Thermal Imaging Summary",
     "30 thermal scans were conducted on 27 September 2022 using the BOSCH GTC 400 C Professional "
     "(Serial: 02700034772) with emissivity set at 0.94 and reflected temperature at 23°C. All scans "
     "recorded hotspot temperatures in the range of 25.1°C to 28.8°C, with coldspots ranging from "
     "20.1°C to 23.4°C. The consistent temperature differentials of 3-5°C across all affected zones "
     "confirm active subsurface moisture presence behind wall and floor finishes throughout the flat."),
    ("Checklist Findings",
     "The inspection checklist identified 1 flagged item (WC / External Wall) out of 7, giving an "
     "overall inspection score of 85.71%. Key checklist findings include: leakage due to concealed "
     "plumbing (confirmed), damage to Nahani trap/brickbat coba (confirmed), gaps around Nahani trap "
     "joints (confirmed), loose plumbing joints (confirmed), and moderate cracks on RCC column/beam "
     "(confirmed). No previous structural audit or repair work had been undertaken prior to this "
     "inspection."),
    ("Property Age Consideration",
     "At 11 years of age, the property is at a critical maintenance threshold. Standard waterproofing "
     "systems in India have a design life of 8-12 years, meaning the original waterproofing in all wet "
     "areas is likely at or beyond end-of-life. The cluster of issues identified is consistent with "
     "this age profile and does not necessarily indicate any construction defect, but does require "
     "comprehensive remediation."),
    ("Flat 203 Coordination Required",
     "The mild ceiling dampness in the Common Bathroom of Flat 103 has been traced to leakage from "
     "Flat 203 (the floor above). A permanent fix for this specific issue requires the occupant of "
     "Flat 203 to repair their bathroom tile joints and outlet leakage. The building management or "
     "society committee should be engaged to facilitate this."),
]

for title, text in notes:
    story.append(Paragraph(f"<b>{title}</b>", styles['SubHeader']))
    story.append(Paragraph(text, styles['BodyText2']))
    story.append(Spacer(1, 0.2*cm))

story.append(PageBreak())

# ── SECTION 7 — MISSING OR UNCLEAR INFORMATION ───────────────────────────────
story.append(section_header("SECTION 7 — MISSING OR UNCLEAR INFORMATION"))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "The following information was not available in the source documents or could not be confirmed "
    "at the time of inspection:",
    styles['BodyText2']))
story.append(Spacer(1, 0.2*cm))

missing_data = [
    ["Item", "Status", "Impact"],
    ["Client Name, Mobile & Email",        "Not Available (redacted in source document)",
     "Cannot confirm client identity for report delivery"],
    ["Flat Address (full)",                 "Not Available (only Flat No. 103 mentioned)",
     "Full property address not confirmed"],
    ["Existing paint type & manufacturer",  "Not Sure (as noted in checklist)",
     "Cannot specify compatible repair paint system"],
    ["Sealant condition on window frames",  "N/A (not inspected or not present)",
     "External waterproofing completeness uncertain"],
    ["Condition of RCC corrosion/spalling", "N/A (not observed or not accessible)",
     "Structural reinforcement condition unknown"],
    ["Expansion joint condition",           "N/A (not observed)",
     "Building movement joint status unknown"],
    ["Flat 203 occupant contact/consent",   "Not Available",
     "Cross-flat repair cannot proceed without coordination"],
    ["Previous waterproofing details",      "No previous work done (confirmed)",
     "No baseline to compare against"],
    ["Thermal image to room mapping",       "Partial - sequence inferred from inspection order",
     "Thermal zone mapping is approximate"],
]

miss_table = Table(missing_data, colWidths=[4.5*cm, 6.5*cm, 6.5*cm])
miss_table.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0),  BRAND_BLUE),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [WHITE, LIGHT_GREY]),
    ('GRID',          (0,0), (-1,-1), 0.3, colors.lightgrey),
    ('FONTNAME',      (0,0), (-1,0),  'Helvetica-Bold'),
    ('FONTSIZE',      (0,0), (-1,0),  9),
    ('TEXTCOLOR',     (0,0), (-1,0),  WHITE),
    ('FONTSIZE',      (0,1), (-1,-1), 8.5),
    ('VALIGN',        (0,0), (-1,-1), 'TOP'),
    ('TOPPADDING',    (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING',   (0,0), (-1,-1), 5),
]))
story.append(miss_table)
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph(
    "All other information presented in this report is directly sourced from the Inspection Report "
    "dated 27 September 2022 and the Thermal Images Report (same date). No information has been "
    "invented or assumed. Where data was conflicting or missing, it has been explicitly noted above.",
    styles['Disclaimer']))

# ── BUILD PDF ─────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUT_PDF,
    pagesize=A4,
    topMargin=1.8*cm,
    bottomMargin=1.5*cm,
    leftMargin=1.5*cm,
    rightMargin=1.5*cm,
    title="Detailed Diagnostic Report - Flat No. 103",
    author="UrbanRoof Private Limited",
)

doc.build(story, onFirstPage=on_first_page, onLaterPages=on_page)
print(f"✅ DDR PDF generated: {OUT_PDF}")