from flask import Flask, render_template, request
import os
from PyPDF2 import PdfReader
from translate import Translator

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pdf_file = request.files['file']
        if pdf_file and pdf_file.filename.endswith('.pdf'):
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
            pdf_file.save(pdf_path)

            translated_text = extract_and_translate(pdf_path)
            return render_template('translation_result.html', translated_text=translated_text)

    return render_template('index.html')

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
