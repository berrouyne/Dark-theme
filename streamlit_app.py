import streamlit as st
import fitz  # PyMuPDF
import io
import os
from datetime import datetime

st.set_page_config(page_title="PDF Dark Mode Converter 🌗", page_icon="🌗")


def convert_to_dark(input_pdf_bytes):
    input_stream = io.BytesIO(input_pdf_bytes)
    doc = fitz.open(stream=input_stream, filetype="pdf")

    output_stream = io.BytesIO()

    for page in doc:
        # Set dark background
        rect = page.rect
        page.draw_rect(rect, color=(0, 0, 0), fill=(0, 0, 0))

        # Add white text
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        bbox = fitz.Rect(span["bbox"])
                        text = span["text"]
                        fontsize = span["size"]
                        fontname = span.get("font", "helv")  # fallback

                        page.insert_textbox(
                            bbox,
                            text,
                            fontsize=fontsize,
                            fontname=fontname,
                            color=(1, 1, 1),  # white
                            align=0  # left aligned
                        )

    doc.save(output_stream)
    output_stream.seek(0)
    return output_stream


# UI
st.title("🌓 PDF Light ➜ Dark Mode Converter")
st.markdown("Upload your light-mode PDF and get a dark-mode version for easier night reading 🌙")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    st.info(f"Processing file: `{uploaded_file.name}`...")

    # Read the PDF file and convert it
    with st.spinner("Converting to dark mode..."):
        dark_pdf = convert_to_dark(uploaded_file.read())

    # Download button
    dark_filename = uploaded_file.name.replace(".pdf", "") + "_darkmode.pdf"
    st.success("✅ Conversion complete!")
    st.download_button(
        label="📥 Download Dark Mode PDF",
        data=dark_pdf,
        file_name=dark_filename,
        mime="application/pdf"
    )
