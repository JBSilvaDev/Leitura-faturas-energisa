import pdfplumber
from pathlib import Path
import os
import re
import shutil
import pandas as pd


CAMINHO_RAIZ = r"C:\Users\julianobs\OneDrive - Suzano S A\Area Dev\GitHub\Leitura-faturas-energisa"

pasta_pendentes = Path(fr"{CAMINHO_RAIZ}\faturas_pendentes")
itens = os.listdir(pasta_pendentes)
listaItens = []

regex = {
  "uc": [
    r"CÓDIGO:\s*(\d+)\d",
    r"UC:\s*(\d+)"
  ],
  "venc":[
    r'Protocolo de Autorização:.*?(\d{2}/\d{2}/\d{4})\s*R\$',
    r"\d{4}-\d{2}-\d\s+(\d{2}/\d{2}/\d{4})"
  ],
  "emis":[
    r"EMISS[ÃA]O\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})",
    r"DATA EMISSÂO/APRESENTAÇÂO:(\d{2}/\d{2}/\d{4})"
  ],
  "nf":[
    r"NOTA FISCAL Nº[:\-]?\s*(\d{3}\.\d{3}\.\d{3})",
    r"NOTA FISCAL N°[:\-]?\s*(\d{3}\.\d{3}\.\d{3})"
  ],
  "cb":[
    r"(\d{11}-\d\s\d{11}-\d\s\d{11,13}-\d\s\d{11}-\d)",
    r"(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})"
  ],
  "val":[
    r"R\$ (\d{1,3},\d{2})"
  ]
}

def moverArquivo(arquivo, status):
    # Movendo arquivos
    origem = Path(fr"{CAMINHO_RAIZ}\faturas_pendentes\{arquivo}")
    if status:
        destino = Path(fr"{CAMINHO_RAIZ}\faturas_sucesso")
    else:
        destino = Path(fr"{CAMINHO_RAIZ}\faturas_erro")
    # Movendo o arquivo
    shutil.move(origem, destino)

def rgx_none(chave, texto):
  num_tentativas = 5
  for i, rgx in enumerate(regex[chave]):
    if i >= num_tentativas:
      break
    match = re.search(rgx, texto)
    try:
      if match != None:
        return match.group(1)
    except:
      if match != None:
        return match.group()
  return "Não encontrado"


def extract_text_from_pdf(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    return text

for pdf in itens:
    # Caminho para o PDF
    pdf_item = Path(rf"{pasta_pendentes}\{pdf}")

    # Extrair texto do PDF
    extracted_text = extract_text_from_pdf(pdf_item)

    # Converter o texto extraído em uma lista
    list_data = extracted_text.split('\n')
    texto = ' '.join(list_data)
    dicionario = {
        "Item": pdf,
        "uc": rgx_none("uc", texto),
        "venc": rgx_none("venc", texto),
        "emissao": rgx_none("emis", texto),
        "valor_total": rgx_none("val", texto),
        "nota_fiscal": rgx_none("nf", texto),
        "cod_barras": rgx_none("cb", texto)
        }
    listaItens.append(dicionario)

    if "Não encontrado" in dicionario.values():
        print("Houve erro em um dos valores")
        moverArquivo(pdf, False)
    else:
        print("Tudo certo, nenhum campo com erro")
        moverArquivo(pdf, True)

df = pd.DataFrame(listaItens)
df.to_excel("./faturas.xlsx",index=False)
        
 