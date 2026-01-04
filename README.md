# LLM Resume Parser

## Overview
This project is a local resume parsing tool built with Python and Streamlit. It leverages a local Large Language Model (LLM) via LM Studio to extract structured data from PDF resumes. The application parses unstructured text and converts it into a strict JSON format, identifying key fields such as contact information, skills, experience, education, and certifications.


## Features
- **Local Inference:** Runs entirely on your local machine using LM Studio, ensuring data privacy for sensitive resume information.
- **PDF Extraction:** Utilizes PyPDF2 to extract raw text from uploaded PDF documents.
- **Structured Output:** Forces the LLM to output data in a validated JSON schema.
- **Strict Parsing Rules:** Includes logic to handle missing data fields (set to null) and validate phone/email formats.


## Technical Stack

- **Frontend**: Streamlit
- **PDF Processing**: PyPDF2
- **LLM Integration**: OpenAI Python client (configured for local LM Studio)
- **LLM Model**: Meta-Llama-3.1-8B-Instruct (Q4_K_M quantization)
- **Language**: Python 3.8+



## Prerequisites

Before running this application, ensure you have the following installed:

1. **Python 3.8 or higher**
2. **LM Studio** with Meta-Llama-3.1-8B-Instruct model loaded
   - Download LM Studio from [https://lmstudio.ai](https://lmstudio.ai)
   - Load the Meta-Llama-3.1-8B-Instruct model
   - Start the local server (default: http://localhost:1234)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/MoayadAlshehry/llm-resume-parser.git
cd ats-resume-parser
```

### 2. Create a Virtual Environment

You can use either the built-in `venv` module or a Conda environment.

#### Option A: Using venv (standard Python)

```bash
python -m venv venv
source venv/bin/activate  # On Windows (CMD): venv\Scripts\activate
                          # On Windows (PowerShell): venv\Scripts\Activate.ps1
```
#### Option B: Using Conda                 
If you prefer Conda, you can create and activate an isolated environment as follows:
```bash
# Create a new Conda environment with Python 3.10 (recommended)
conda create -n ats-resume-parser python=3.10

# Activate the environment (Linux/macOS/Windows)
conda activate ats-resume-parser
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

The application expects the LM Studio server to be running at `http://localhost:1234`. 

If you need to modify these settings, edit the following in `app.py`:

```python
client = OpenAI(
    base_url="http://localhost:1234/v1", 
    api_key="lm-studio"
)
```

## Usage

### 1. Start LM Studio

Ensure the LM Studio application is running with the Meta-Llama-3.1-8B-Instruct model loaded and the local server is active.

### 2. Run the Application

```bash
streamlit run app.py
```

The application will launch in your default web browser at `http://localhost:8501`.

### 3. Upload a Resume

- Click `Browse files` and select a PDF resume file
- Click the "Extract Information" button
- The application will process the resume and display the extracted structured data in JSON format

## Output Structure

The system returns resume data in the following JSON structure:

```json
{
  "full_name": "String",
  "email": "String or null",
  "phone": "String or null",
  "skills": ["Array of strings"],
  "experience": [
    {
      "company": "String",
      "role": "String",
      "years": "String"
    }
  ],
  "education": [
    {
      "institution": "String",
      "degree": "String"
    }
  ],
  "certifications": [
    {
      "name": "String",
      "issuer": "String or null",
      "year": "String or null"
    }
  ]
}
```

## Validation Rules

The LLM enforces the following validation rules:

- **Missing Data**: Any field not found in the resume is set to `null`
- **Email**: Must follow valid email format; otherwise set to `null`
- **Phone**: Accepts numbers starting with '966' or '05'; invalid formats return `null`
- **Experience**: If no work experience is found, the field is set to `null` (not an empty list)
- **Certifications**: Extracted as a structured list with name, issuer, and year

## Troubleshooting

### Connection Error: Cannot Connect to LM Studio

- Verify LM Studio is running on your system
- Check that the local server is started (you should see output indicating the server is listening)
- Confirm the base URL is correct: `http://localhost:1234/v1`

### PDF Parsing Issues

- Ensure the PDF is text-based (not image-based or scanned)
- Verify the PDF file is not corrupted
- For scanned PDFs, consider using OCR preprocessing before uploading

### Memory Issues

If you encounter memory errors:
- Ensure sufficient system RAM (minimum 8GB recommended for Llama-3.1-8B)
- Consider using a smaller quantization if using Q4_K_M

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome. Please fork the repository, create a feature branch, and submit a pull request with your improvements.

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

## Acknowledgments

- Streamlit for the intuitive web framework
- Meta for the Llama-3.1 language model
- OpenAI for the Python client library
- LM Studio for enabling local LLM deployment
