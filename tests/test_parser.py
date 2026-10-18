from io import BytesIO
from types import SimpleNamespace
from unittest.mock import Mock
import json

import pytest
from pypdf import PdfWriter
from resume_parser import ParserError, Resume, extract_pdf, parse_resume, validate_output


def test_valid_response_preserves_fields():
    result = validate_output('{"full_name":"Alex","skills":["SQL"],"experience":[]}')
    assert result.full_name == "Alex"
    assert result.skills == ["SQL"]
    assert result.experience is None
    assert set(result.model_dump()) == {"full_name", "email", "phone", "skills", "experience", "education", "certifications"}


def test_fenced_json_and_null_lists():
    assert validate_output('```json\n{"skills":null}\n```').skills == []


@pytest.mark.parametrize("raw", [None, "", "not JSON", "[]", '{"skills":"SQL"}', '{"education":[42]}', '{} {}'])
def test_invalid_output_is_actionable(raw):
    with pytest.raises(ParserError):
        validate_output(raw)


def test_contact_normalization():
    data = Resume(email="invalid", phone="+966 (50) 123-4567")
    assert data.email is None
    assert data.phone == "966501234567"
    assert Resume(phone="not a phone").phone is None


@pytest.mark.parametrize("data", [b"", b"not a pdf"])
def test_invalid_pdf(data):
    with pytest.raises(ParserError):
        extract_pdf(data)


def test_blank_pdf_requires_ocr():
    writer, buffer = PdfWriter(), BytesIO()
    writer.add_blank_page(width=200, height=200)
    writer.write(buffer)
    with pytest.raises(ParserError, match="No readable text"):
        extract_pdf(buffer.getvalue())


def test_encrypted_pdf():
    writer, buffer = PdfWriter(), BytesIO()
    writer.add_blank_page(width=200, height=200)
    writer.encrypt("example-test-password")
    writer.write(buffer)
    with pytest.raises(ParserError, match="Password-protected"):
        extract_pdf(buffer.getvalue())


def test_size_limit():
    with pytest.raises(ParserError, match="10 MB"):
        extract_pdf(b"12345", max_bytes=4)


def test_mocked_model_completion():
    client = Mock()
    client.chat.completions.create.return_value = SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content='{"skills":["SQL"]}'))])
    assert parse_resume("Fictional resume", client).skills == ["SQL"]
    assert client.chat.completions.create.call_args.kwargs["messages"][1]["content"] == "Fictional resume"


def test_server_failure_is_actionable():
    client = Mock()
    client.chat.completions.create.side_effect = ConnectionError()
    with pytest.raises(ParserError, match="endpoint"):
        parse_resume("Example", client)


def test_empty_completion_is_actionable():
    client = Mock()
    client.chat.completions.create.return_value = SimpleNamespace(choices=[])
    with pytest.raises(ParserError, match="no completion"):
        parse_resume("Example", client)
