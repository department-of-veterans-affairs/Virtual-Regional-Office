import os
import requests
from pathlib import Path
from zipfile import ZipFile

wkhtmltopdf_url = 'https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-4/wkhtmltox-0.12.6-4.amazonlinux2_lambda.zip'
package_directory = Path('../../layers/vro--wkhtmltopdf/')


def download_wkhtmltopdf_main() -> None:
    binary_request = requests.get(wkhtmltopdf_url)
    filename = binary_request.headers['Content-Disposition'].split("filename=")[-1]
    with open(filename, 'wb') as f:
        f.write(binary_request.content)
        f.close()

    # unzip wkhtmltopdf package into layers directory
    with ZipFile(filename, 'r') as package:
        package.extractall(package_directory)

    # clean up download and temporary folder
    os.remove(filename)


if __name__ == "__main__":
    download_wkhtmltopdf_main()
