import streamlit as st
import fitz  # PyMuPDF
from PIL import Image, ImageOps
import io
import time
import numpy as np
import cv2
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from streamlit_pdf_viewer import pdf_viewer

# --- Page Config ---
st.set_page_config(
    page_title="🌓 PDF Dark Mode Converter",
    page_icon="🌗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Disable Streamlit Menu (includes 'Deploy') ---
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- Custom Styling (to mimic your HTML) ---
st.markdown("""
    <style>
        body {
            background: #1e1e1e;
            color: #ffffff;
        }
        * {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        }
        h1 {
            font-size: 2.5em;
            text-align: center;
            margin-bottom: 0.2em;
            color: #ffffff;
        }
        .description {
            text-align: center;
            color: #cccccc;
            margin-bottom: 2em;
        }
        .block-container {
            padding-top: 60px;
        }
        .stButton>button {
            padding: 12px 24px;
            background: linear-gradient(135deg, #3f3f3f, #1f1f1f);
            color: #fff;
            font-size: 1em;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #555, #2a2a2a);
        }
    </style>
""", unsafe_allow_html=True)

# --- Title & Description ---
st.markdown("<h1>🌓 Welcome to the PDF Dark Mode Converter</h1>", unsafe_allow_html=True)
st.markdown("<p class='description'>Night reader? We’ve got you. Upload your light-mode PDF and get it back in a smooth dark theme — all local, all private.</p>", unsafe_allow_html=True)

# --- Core PDF Conversion Logic ---
def process_pdf(input_pdf_bytes, filter_level=100, dpi=150):
    pdf_document = fitz.open(stream=input_pdf_bytes, filetype="pdf")
    output_buffer = io.BytesIO()
    c = canvas.Canvas(output_buffer)

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        page_width, page_height = page.rect.width, page.rect.height

        pix = page.get_pixmap(dpi=dpi)
        arr = np.frombuffer(pix.samples, dtype=np.uint8)
        channels = 4 if pix.alpha else 3
        arr = arr.reshape((pix.height, pix.width, channels))
        arr = cv2.cvtColor(arr, cv2.COLOR_BGRA2RGB if channels == 4 else cv2.COLOR_BGR2RGB)

        image = Image.fromarray(arr)
        inverted_image = ImageOps.invert(image)
        blend_factor = filter_level / 100
        final_image = Image.blend(image, inverted_image, blend_factor)

        image_bytes = io.BytesIO()
        final_image.save(image_bytes, format="PNG", quality=100)
        image_bytes.seek(0)

        c.setPageSize((page_width, page_height))
        img_reader = ImageReader(image_bytes)
        c.drawImage(img_reader, 0, 0, width=page_width, height=page_height)
        c.showPage()

    c.save()
    output_buffer.seek(0)
    return output_buffer

# --- Upload + Convert ---
if "processed_files" not in st.session_state:
    st.session_state.processed_files = []

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    if st.button("Convert to Dark Mode"):
        st.session_state.processed_files.clear()
        with st.spinner("Processing your file..."):
            binary = uploaded_file.read()
            dark_pdf = process_pdf(binary, filter_level=100, dpi=150)
            st.session_state.processed_files.append((
                uploaded_file.name,
                dark_pdf.getvalue(),
                f"download_{time.time()}"
            ))
        st.success("✅ Done! Scroll down to preview or download.")

# --- Preview & Download ---
for file_name, file_data, key in st.session_state.processed_files:
    st.download_button(
        label="📥 Download Dark Mode PDF",
        data=file_data,
        file_name=file_name.replace(".pdf", "_darkmode.pdf"),
        mime="application/pdf",
        key=key
    )
    st.markdown("---")
    pdf_viewer(file_data, width=1200, height=600)
