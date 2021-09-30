import io
from pdfminer.high_level import extract_text
from lib.pdf_generator import generate_pdf_from_string


def test_generate_pdf_from_string():
    generated = generate_pdf_from_string(
        "<html><body>Hello World!</body></html>"
    )
    assert isinstance(generated, bytes)

    extracted = extract_text(io.BytesIO(generated))
    assert "Hello" in extracted
    assert "World!" in extracted
