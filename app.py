import streamlit as st
import os
import subprocess

st.set_page_config(page_title="DDR Report Generator", page_icon="🏠")

st.title("🏠 DDR Report Generator")
st.subheader("UrbanRoof — AI-Powered Property Diagnostic Reports")

st.markdown("""
This system converts raw site inspection data into a structured  
**Detailed Diagnostic Report (DDR)** PDF using AI analysis.

### Pipeline
```
Sample Report.pdf + Thermal Images.pdf
        ↓
   PDF Extraction (pdfplumber)
        ↓
   Claude AI Analysis (reasoning + structuring)
        ↓
   PDF Generation (reportlab)
        ↓
   Final DDR.pdf
```
""")

st.divider()

st.markdown("### Sample Output")
st.markdown("The system generated this DDR from the provided inspection documents:")

with open("Sample_output_DDR_Report_Flat103.pdf", "rb") as f:
    st.download_button(
        label="📄 Download Sample DDR Report",
        data=f,
        file_name="DDR_Report_Flat103.pdf",
        mime="application/pdf"
    )

st.divider()

st.markdown("### How It Works")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**Step 1: Extract**")
    st.markdown("Text and images pulled from both PDFs using pdfplumber and pdfimages")
with col2:
    st.markdown("**Step 2: Analyse**")
    st.markdown("Claude AI merges observations, identifies root causes, assesses severity")
with col3:
    st.markdown("**Step 3: Generate**")
    st.markdown("reportlab assembles a professional branded PDF with images in correct sections")

st.divider()
st.markdown("**Output includes:** Property Issue Summary · Area-wise Observations · Root Cause · Severity Assessment · Recommended Actions · Missing Information")
st.caption("Built by [Your Name] | UrbanRoof AI Generalist Assignment")
