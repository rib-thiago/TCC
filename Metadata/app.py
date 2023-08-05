from flask import Flask, render_template, request, send_file, redirect, url_for
import os
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import create_string_object


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    pdf_file = request.files['file']
    if pdf_file:
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
        pdf_file.save(pdf_path)
        return redirect(url_for('edit_metadata', pdf_path=pdf_path))
    return redirect('/')

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

if __name__ == '__main__':
    app.run(debug=True)
