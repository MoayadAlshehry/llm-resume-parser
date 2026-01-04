import streamlit as st
import PyPDF2 as pdf
from openai import OpenAI
import json
import re


client = OpenAI(
    base_url="http://localhost:1234/v1", 
    api_key="lm-studio"
)

def clean_json_output(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        text = match.group(0) 
    return text

def parse_cv(cv_text):
    system_instruction = """
    You are an advanced AI specialized in parsing resumes (CVs) for recruitment systems.
    Your task is to extract information and format it as strict JSON.

    Follow these specific validation rules:
    1. **Missing Data**: If any field is not found, strictly set its value to null.
    2. **Email**: Must be a valid email format. If invalid or not found, set to null.
    3. **Phone**: Look for numbers starting with '966' or '05'. If the format is correct, extract it. If not found, set to null. (Number only, no spaces or +)
    4. **Experience**: If the candidate has no work experience, set "experience" to null (do not return an empty list).
    5. **Certifications**: Extract certificates in a specific list.

    Required JSON Structure:
    {
        "full_name": "String",
        "email": "String or null",
        "phone": "String or null",
        "skills": ["Array of strings"],
        "experience": [
            {"company": "String", "role": "String", "years": "String"}
        ], 
        "education": [
            {"institution": "String", "degree": "String"}
        ],
        "certifications": [
            {"name": "String", "issuer": "String or null", "year": "String or null"}
        ]
    }

    Return ONLY the JSON object. Do not add any conversational text.
    """

    completion = client.chat.completions.create(
        model="local-model",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Here is the resume text:\n{cv_text}"}
        ],
        temperature=0.0,
        
    )

    return completion.choices[0].message.content

def input_pdf_text(file):
    reader = pdf.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += str(page.extract_text())
    return text

st.title("LLM Resume Parser")
st.text("Upload a CV in PDF format to extract structured information using a local LLM.")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", help="Upload a resume/CV in PDF format.")
submit_button = st.button("Extract Information")

if submit_button:
    if submit_button and uploaded_file is not None:
        with st.spinner("Processing..."):
            cv_text = input_pdf_text(uploaded_file)
            structured_data = parse_cv(cv_text)
            st.subheader("Extracted Information:")
            cleaned_data = clean_json_output(structured_data)
            st.json(json.loads(cleaned_data))