from lib.pdf_generator import PdfGenerator


def test_pdf_generator_instantiation():
    assert type(PdfGenerator().config.wkhtmltopdf) is bytes


def test_generate_from_string():
    assert (
        type(
            PdfGenerator().generate_from_string(
                "<html><body>Hello World!</body></html>"
            )
        )
        is bytes
    )
