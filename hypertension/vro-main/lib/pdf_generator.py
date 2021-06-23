import pdfkit


class PdfGenerator:
    def __init__(self, path="") -> None:
        self.config = pdfkit.configuration(wkhtmltopdf=path)

    def generate_from_string(self, html: str):
        return pdfkit.from_string(html, False, configuration=self.config)
