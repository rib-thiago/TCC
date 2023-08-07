###-------------------------------------------------------------------------#
#                                   vostok-1                                   #
#----------------------------------------------------------------------------#
# Script:
# img2str.py
#
# Descrição:
# Este é um script em Python que extrai texto de uma imagem usando o OCR
# Tesseract e o traduz para um idioma específico usando a biblioteca TextBlob.
#
# Autor: Thiago Ribeiro
# Data: 10/03/2023
# Versão: 1.0
#
# Uso:
# Para utilizar o script, execute-o com os seguintes argumentos:
# python3 img2str.py [imagem] --idioma [origem] --idioma-destino [destino]
#
# Exemplo:
# python3 img2str.py exemplo_imagem.jpg -l por -d eng
#
# Dependências:
# - pytesseract
# - opencv-python
# - textblob
#
# Observações:
# Nenhuma.
#
# --------------- #
# Registro de Alterações    #
# --------------- #
#
# Versão    Data          Autor                  Descrição
# -------   ----          ------                 -----------
# [Versão]  [Data]        [Seu Nome/Empresa]     [Descrição da alteração]
#
# FIXME:
#   Traceback (most recent call last):
#  File "/home/thiago/ocr-translate-pdf/jpg2txt/img2str.py", line 105,
#  in <module>
#    extract_text(args.filename, args.language, args.dest_language)
#  File "/home/thiago/ocr-translate-pdf/jpg2txt/img2str.py", line 84,
#  in extract_text
#    translated = tb.translate(from_lang=lang_map[language],
#                 to=lang_map[dest_language])
#  KeyError: 'en'
#
# Cangelog do TextBlob:
#
# 0.16.0 (2020-04-26)
# Deprecations:
#
# TextBlob.translate() and TextBlob.detect_language are deprecated.
# Use the official Google Translate API instead (215).
#
# XXX:
# Nenhum.
#
################################################################################

import argparse
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

    # passo 3: imprimir a resposta na tela
    print("ORIGINAL")
    print("=" * 20)
    print(texto)
    print()

    print(f"TRANSLATED ({dest_language.upper()})")
    print("=" * 20)
    print(translated)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract text from an image")
    parser.add_argument("filename", help="path to the image file")
    parser.add_argument("--language", "-l", default="eng", help="language code for OCR")
    parser.add_argument("--dest-language", "-d", default="eng", help="destination language code for translation")

    args = parser.parse_args()

    extract_text(args.filename, args.language, args.dest_language)


