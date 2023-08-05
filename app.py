from flask import Flask, render_template, request, send_file, redirect
from io import BytesIO
from PyPDF2 import PdfMerger

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/merge", methods=["POST"])
def merge():
    pdf_files = request.files.getlist("PDF_files")
    merger = PdfMerger()
    for pdf_file in pdf_files:
        merger.append(pdf_file)
    with open("merged.pdf", "wb") as output_file:
        merger.write(output_file)
    return send_file("merged.pdf", as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
