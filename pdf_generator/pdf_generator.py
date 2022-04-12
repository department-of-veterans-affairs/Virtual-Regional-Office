import pdfkit, os
from jinja2 import Environment, PackageLoader, select_autoescape

script_dir = os.path.dirname(__file__)
env = Environment(
  loader=PackageLoader("pdf_generator"),
  autoescape=select_autoescape()
)

template = env.get_template("hypertension.html")

template_variables = {
  "name": "test",
  "ssn": "000-00-0000",
  "dob": "0/0/00",
  "claim_number": "000",
  "claim_date": "0/0/00",
  "systolic_pressure_summary_min": "0",
  "systolic_pressure_summary_max": "0",
  "systolic_pressure_summary_avg": "0",
  "systolic_pressure_summary_predominant_range": ["0", "0"],
  "diastolic_pressure_summary_min": "0",
  "diastolic_pressure_summary_max": "0",
  "diastolic_pressure_summary_avg": "0",
  "diastolic_pressure_summary_predominant_range": ["0", "0"],
  "medicine_name": "Placeholder",
  "systolic_bp_measurements": [
    {
      "facility": "Placeholder",
      "date": "0/0/00",
      "diastolic": "0",
      "systolic": "0"
    }
  ],
  "diastolic_bp_measurements_under_100": [
    {
      "facility": "Placeholder",
      "date": "0/0/00",
      "diastolic": "0",
      "systolic": "0"
    }
  ],
  "diastolic_bp_measurements_over_100": [
    {
      "facility": "Placeholder",
      "date": "0/0/00",
      "diastolic": "0",
      "systolic": "0"
    }
  ],
  "diastolic_bp_measurements_over_120": [
    {
      "facility": "Placeholder",
      "date": "0/0/00",
      "diastolic": "0",
      "systolic": "0"
    }
  ]
}



generated_html = template.render(**template_variables)

with open(os.path.join(script_dir, "generated_files/hypertension.html"), "w") as file:
  file.write(generated_html)

options = {
  "dpi": 300,
  "page-size": "Letter",
  "margin-top": "0.25in",
  "margin-right": "0.25in",
  "margin-bottom": "0.25in",
  "margin-left": "0.25in",
  "encoding": "UTF-8",
  "zoom": "0.8"
}

pdfkit.from_file(os.path.join(script_dir, "generated_files/hypertension.html"), os.path.join(script_dir, "output/hypertension.pdf"), options=options)
