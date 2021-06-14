from lib.main import main
import pdfkit


def lambda_handler(event, context):
    # testing out pdfkit
    config = pdfkit.configuration(wkhtmltopdf='/opt/bin/wkhtmltopdf')
    pdf = pdfkit.from_url(event.get('url'), None, configuration=config)

    print(pdf)

    return main()
