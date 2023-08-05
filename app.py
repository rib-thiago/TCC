from flask import Flask, render_template, request, send_file, redirect, url_for
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
from translate import Translator
import os

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pdf_file = request.files['file']
        page_input = request.form['page_numbers']

        pdf_reader = PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)

        pdf_writer = PdfWriter()  # Single PdfWriter for the final output

        if ',' in page_input:  # Extract individual pages
            page_nums = map(int, page_input.split(','))
            for page_num in page_nums:
                if 1 <= page_num <= num_pages:
                    pdf_writer.add_page(pdf_reader.pages[page_num - 1])
        elif '-' in page_input:  # Extract page range
            start, end = map(int, page_input.split('-'))
            start = max(start, 1)
            end = min(end, num_pages)
            for i in range(start - 1, end):
                pdf_writer.add_page(pdf_reader.pages[i])

        output_filename = 'split.pdf'
        with open(output_filename, 'wb') as output_file:
            pdf_writer.write(output_file)

        return send_file(output_filename, as_attachment=True)

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
