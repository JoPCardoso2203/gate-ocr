import cv2
import os
import glob
import re
from PIL import Image as ImagePil
import pytesseract

def get_latest_file_path(path):
    """return the more recent file in a path"""

    file_paths = glob.glob(f'{path}/*') # obtem o path de cada arquivo na pasta
    all_files_modification_time = [ os.path.getmtime(path) for path in file_paths ] # Obtem o modification time de cada arquivo
    latest_file_index = all_files_modification_time.index(max(all_files_modification_time)) # obtem o index do maior deles, o arquivo mais recente
    return file_paths[latest_file_index], max(all_files_modification_time)

def tratar_imagens(pasta_origem, pasta_destino='ajeitado'):
    arquivo, tempo = get_latest_file_path(pasta_origem)
    imagem = cv2.imread(arquivo)

    # transformar a imagem em escala de cinza
    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)

    _, imagem_tratada = cv2.threshold(imagem_cinza, 127, 255, cv2.THRESH_TRUNC or cv2.THRESH_OTSU)
    nome_arquivo = os.path.basename(arquivo)
    cv2.imwrite(f'{pasta_destino}/{nome_arquivo}', imagem_tratada)

    arquivo, tempo = get_latest_file_path(pasta_destino)
    imagem = ImagePil.open(arquivo)
    imagem = imagem.convert("P")
    imagem2 = ImagePil.new("P", imagem.size, 255)

    for x in range(imagem.size[1]):
        for y in range(imagem.size[0]):
            cor_pixel = imagem.getpixel((y, x))
            if cor_pixel < 115:
                imagem2.putpixel((y, x), 0)
    nome_arquivo = os.path.basename(arquivo)
    imagem2 = imagem2.convert('RGB')
    imagem2.save(f'final/{nome_arquivo}')

def MostrarTexto(pasta_origem):
    pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\Tesseract.exe"
    config = r'--oem 3 --psm 11'
    arquivo, tempo = get_latest_file_path(pasta_origem)
    imagem = cv2.imread(arquivo)
    texto = pytesseract.image_to_string(imagem, config=config)
    texto = texto.replace(" ", "")
    print(re.match(re.compile("[A-Z]{3}[0-9][0-9A-Z][0-9]{2}"), texto).string.strip())

def filtrar():
    arquivo, tempo = get_latest_file_path("final")
    imagem = cv2.imread(arquivo)
    imagem = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)
    # em preto e branco
    _, nova_imagem = cv2.threshold(imagem, 0, 255, cv2.THRESH_BINARY_INV)

    # encontrar os contornos de cada letra
    contornos, _ = cv2.findContours(nova_imagem, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    regiao_letras = []

    # filtrar os contornos que são realmente de letras
    for contorno in contornos:
        (x, y, largura, altura) = cv2.boundingRect(contorno)
        area = cv2.contourArea(contorno)
        if area > 100:
            regiao_letras.append((x, y, largura, altura))
    # desenhar os contornos e separar as letras em arquivos individuais

    imagem_final = cv2.merge([imagem] * 3)

    i = 0
    for retangulo in regiao_letras:
        x, y, largura, altura = retangulo
        imagem_letra = imagem[y-2:y+altura+2, x-2:x+largura+2]
        i += 1
        nome_arquivo = os.path.basename(arquivo).replace(".jpg", f"letra{i}.jpg")
        cv2.rectangle(imagem_final, (x-2, y-2), (x+largura+2, y+altura+2), (0, 255, 0), 1)
    nome_arquivo = os.path.basename(arquivo)
    cv2.imwrite(f"identificado/{nome_arquivo}", imagem_final)



if __name__ == "__main__":
    tratar_imagens("Imagens", pasta_destino='ajeitado')
    filtrar()
    MostrarTexto("final")

