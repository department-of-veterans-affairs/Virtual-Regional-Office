from lib.pdf_generator import PdfGenerator


def test_pdf_generator_instantiation():
    assert isinstance(PdfGenerator().config.wkhtmltopdf, bytes) is True


def test_generate_from_string():
    assert (
        isinstance(
            PdfGenerator().generate_from_string(
                "<html><body>Hello World!</body></html>"
            ),
            bytes,
        )
        is True
    )
