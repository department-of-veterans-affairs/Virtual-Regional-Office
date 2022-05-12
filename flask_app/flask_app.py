from flask import Flask, make_response, request, render_template_string, jsonify

from pdf_generator import generate_pdf_from_string, generate_template_file

app = Flask(__name__)

@app.route("/", methods=["POST"])
def pdf_generator():
    request_json = request.get_json()
    pdf_type = request_json["pdf_type"]
    return_pdf = request_json["return_pdf"]

    template = generate_template_file(f"{pdf_type}", request_json)
    if return_pdf:
      pdf = generate_pdf_from_string(template)
      response = make_response(pdf)
      response.headers.set("Content-Disposition", "attachment", filename=f"{pdf_type}.pdf")
      response.headers.set("Content-Type", "application/pdf")
      return response
    else:
      return render_template_string(template)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)