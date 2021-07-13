from pathlib import Path
import os
import pdfkit

WKHTMLTOPDF_PATH = Path(os.environ["WKHTMLTOPDF_PATH"]).resolve()


def generate_pdf_from_string(html: str) -> bytes:
    assert WKHTMLTOPDF_PATH.exists()
    config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

    return pdfkit.from_string(html, False, configuration=config)
