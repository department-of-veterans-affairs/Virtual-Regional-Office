from lib.main import main  # pragma: no cover (main is tested elsewhere)
import pdfkit


def lambda_handler(event, context):  # pragma: no cover
    # testing out pdfkit
    config = pdfkit.configuration(wkhtmltopdf='/opt/bin/wkhtmltopdf')
    pdf = pdfkit.from_url(event.get('url'), None, configuration=config)

    print(pdf)

    return main()
