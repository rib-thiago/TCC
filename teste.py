from flask import Flask, render_template, request
import os
import pytesseract
import cv2
from textblob import TextBlob


def extract_text(filename, language, dest_language):
    # Mapeia os códigos de idiomas entre o Tesseract e o TextBlob
    lang_map = {
        "por": "pt",
        "eng": "en",
        "rus": "ru",
        "spa": "es",
        "deu": "de",
        "chi_sim": "zh-CN",
        "jpn": "ja",
        "fra": "fr",
        "ara": "ar"
    }

    # passo 1: ler a imagem
    imagem = cv2.imread(filename)

    # passo 2: pedir pro tessaract extrair o texto da imagem
    texto = pytesseract.image_to_string(imagem, language)

    tb = TextBlob(texto)
    translated = tb.translate(from_lang=lang_map[language], to=lang_map[dest_language])

    return texto, translated


app = Flask(__name__)

@app.route('/ocr', methods=['GET', 'POST'])
def index():
    extracted_text = None
    translated_text = None

    if request.method == 'POST':
        pdf_file = request.files['file']
        filename = os.path.basename(pdf_file.filename)
        pdf_file.save(os.path.join('./uploads', filename))

        language = request.form['language']
        dest_language = request.form['dest_language']

        texto, translated = extract_text(f'./uploads/{filename}', language, dest_language)

        # Passar as variáveis para o template
        return render_template('ocr.html', extracted_text=texto, translated_text=translated)

    # Retorna uma resposta vazia ou redireciona para a página principal
    return render_template('ocr.html', extracted_text=extracted_text, translated_text=translated_text)


if __name__ == '__main__':
    os.environ["TESSDATA_PREFIX"] = "/home/thiago/tessdata"
    app.run(debug=True)
