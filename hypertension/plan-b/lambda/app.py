import pdfkit
def lambda_handler(event, context):
    pdf = pdfkit.from_file(event.file, 'test-html.pdf')
    print(pdf, file='test-pdf-output.pdf')
