from flask import Flask, render_template, request, send_file, redirect, url_for
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from io import BytesIO
from translate import Translator
import os


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

# Extract Text
@app.route('/extract', methods=['GET', 'POST'])
def extract():
    extracted_text = None

    if request.method == 'POST':
        pdf_file = request.files['file']
        pdf_reader = PdfReader(pdf_file)

        extracted_text = ""
        for page in pdf_reader.pages:
            extracted_text += page.extract_text()

    return render_template("extract.html", extracted_text=extracted_text)

# Merge PDFs
@app.route('/merge', methods=['GET', 'POST'])
def merge():
    if request.method == 'POST':
        pdf_files = request.files.getlist("PDF_files")
        merger = PdfMerger()
        for pdf_file in pdf_files:
            merger.append(pdf_file)
        merged_pdf = BytesIO()
        merger.write(merged_pdf)
        merged_pdf.seek(0)
        return send_file(merged_pdf, download_name='merged.pdf', as_attachment=True)

    return render_template("merge.html")

# Edit Metadata
@app.route('/metadata', methods=['GET', 'POST'])
def metadata():
    if request.method == 'POST':
        pdf_file = request.files['file']
        if pdf_file:
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
            pdf_file.save(pdf_path)
            return redirect(url_for('edit_metadata', pdf_path=pdf_path))
    return render_template("metadata.html")

@app.route('/edit_metadata', methods=['GET', 'POST'])
def edit_metadata():
    pdf_path = request.args.get('pdf_path')
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        pub_date = request.form['pub_date']

        reference = f"{author}. ({pub_date}). {title}."

        return redirect(url_for('generate_reference', reference=reference))

    return render_template("edit_metadata.html", pdf_path=pdf_path)

@app.route('/generate_reference')
def generate_reference():
    reference = request.args.get('reference')

    return render_template("generate_reference.html", reference=reference)

# Split PDF
@app.route('/split', methods=['GET', 'POST'])
def split():
    if request.method == 'POST':
        pdf_file = request.files['file']
        page_input = request.form['page_numbers']

        pdf_reader = PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)

        pdf_writer = PdfWriter()

        if ',' in page_input:
            page_nums = map(int, page_input.split(','))
            for page_num in page_nums:
                if 1 <= page_num <= num_pages:
                    pdf_writer.add_page(pdf_reader.pages[page_num - 1])
        elif '-' in page_input:
            start, end = map(int, page_input.split('-'))
            start = max(start, 1)
            end = min(end, num_pages)
            for i in range(start - 1, end):
                pdf_writer.add_page(pdf_reader.pages[i])

        output_pdf = BytesIO()
        pdf_writer.write(output_pdf)
        output_pdf.seek(0)
        return send_file(output_pdf, download_name='split.pdf', as_attachment=True)

    return render_template("split.html")

# Translate Text
@app.route('/translate', methods=['GET', 'POST'])
def translate():
    if request.method == 'POST':
        pdf_file = request.files['file']
        if pdf_file and pdf_file.filename.endswith('.pdf'):
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
            pdf_file.save(pdf_path)

            translated_text = extract_and_translate(pdf_path)
            return render_template('translate.html', translated_text=translated_text)

    return render_template('translate.html')

def extract_and_translate(pdf_path):
    translated_text = ""

    # Extract text from PDF
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        for page in pdf_reader.pages:
            translated_page_text = page.extract_text()

            # Translate each page's text
            translator = Translator(to_lang='pt')  # Change 'pt' to target language code

            # Split text into smaller chunks
            chunk_size = 500
            chunks = [translated_page_text[i:i + chunk_size] for i in range(0, len(translated_page_text), chunk_size)]

            for chunk in chunks:
                translated_chunk = translator.translate(chunk)
                translated_text += translated_chunk

    return translated_text

if __name__ == '__main__':
    app.run(debug=True)
