from flask import Flask, render_template, request
import os
from PyPDF2 import PdfReader

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = None

    if request.method == 'POST':
        pdf_file = request.files['file']
        pdf_reader = PdfReader(pdf_file)

        extracted_text = ""
        for page in pdf_reader.pages:
            extracted_text += page.extract_text()

    return render_template("index.html", extracted_text=extracted_text)

if __name__ == '__main__':
    app.run(debug=True)
