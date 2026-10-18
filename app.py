"""Streamlit entry point. Run with: streamlit run app.py."""
import json
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from resume_parser import ParserError, Resume, extract_pdf, parse_resume

load_dotenv()
st.set_page_config(page_title="LLM Resume Parser", page_icon=str(Path(__file__).parent / "assets" / "icon.png"), layout="centered")
st.caption("DOCUMENT WORKFLOWS / STRUCTURED EXTRACTION")
st.title("From resume to structured data")
st.write("Extract contact details, skills, experience and education from a text-based PDF, then inspect and download the result.")
st.caption("The default model endpoint runs locally. Your document is sent to the endpoint you configure; review it before using personal data.")

with st.container(border=True):
    uploaded = st.file_uploader("Resume PDF", type=["pdf"], help="Up to 10 MB and 50 pages. Scanned PDFs require OCR first.")
    extract, example = st.columns(2)
    run = extract.button("Extract resume", type="primary", use_container_width=True)
    sample = example.button("Load fictional example", use_container_width=True)

if sample:
    st.session_state["result"] = Resume.model_validate_json(
        (Path(__file__).parent / "examples" / "resume.json").read_text(encoding="utf-8")
    ).model_dump()
    st.session_state["is_example"] = True

if run:
    if uploaded is None:
        st.warning("Choose a PDF before extracting.")
    else:
        st.session_state.pop("result", None)
        try:
            with st.spinner("Extracting and validating..."):
                st.session_state["result"] = parse_resume(extract_pdf(uploaded.getvalue())).model_dump()
            st.session_state["is_example"] = False
        except ParserError as exc:
            st.error(str(exc))

if "result" in st.session_state:
    result = st.session_state["result"]
    st.subheader("Structured resume")
    if st.session_state.get("is_example"):
        st.info("Example only — fictional data, loaded without a model request.")
    else:
        st.caption("Schema checked. Review the extracted facts against the original resume; model output can contain errors.")
    st.json(result, expanded=True)
    st.download_button("Download JSON", json.dumps(result, indent=2, ensure_ascii=False), "resume.json", "application/json")

with st.expander("Model configuration"):
    st.write("Endpoint: " + os.getenv("RESUME_PARSER_BASE_URL", "http://localhost:1234/v1"))
    st.write("Model: " + os.getenv("RESUME_PARSER_MODEL", "local-model"))
    st.caption("Set configuration in your environment or a local .env file. API keys are never displayed here.")
