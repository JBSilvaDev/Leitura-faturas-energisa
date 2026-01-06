import pdfplumber
from pathlib import Path
import os
import re
import shutil
import pandas as pd

CAMINHO_RAIZ = r"C:\Users\julianobs\OneDrive - Suzano S A\Area Dev\GitHub\Leitura-faturas-energisa"

class RegexExtractor:
    regex = {
        "uc": [r"CÓDIGO:\s*(\d+)\d", r"UC:\s*(\d+)"],
        "venc": [r'Protocolo de Autorização:.*?(\d{2}/\d{2}/\d{4})\s*R\$', r"\d{4}-\d{2}-\d\s+(\d{2}/\d{2}/\d{4})"],
        "emis": [r"EMISS[ÃA]O\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})", r"DATA EMISSÂO/APRESENTAÇÂO:(\d{2}/\d{2}/\d{4})"],
        "nf": [r"NOTA FISCAL Nº[:\-]?\s*(\d{3}\.\d{3}\.\d{3})", r"NOTA FISCAL N°[:\-]?\s*(\d{3}\.\d{3}\.\d{3})"],
        "cb": [r"(\d{11}-\d\s\d{11}-\d\s\d{11,13}-\d\s\d{11}-\d)", r"(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})"],
        "val": [r"R\$ (\d{1,3},\d{2})"]
    }

    @classmethod
    def extrair(cls, chave, texto):
        for rgx in cls.regex.get(chave, []):
            match = re.search(rgx, texto)
            if match:
                try:
                    return match.group(1)
                except:
                    return match.group()
        return "Não encontrado"

class PDFProcessor:
    def __init__(self, caminho_pdf):
        self.caminho_pdf = caminho_pdf
        self.texto = self._extrair_texto()

    def _extrair_texto(self):
        texto = ''
        with pdfplumber.open(self.caminho_pdf) as pdf:
            for page in pdf.pages:
                texto += page.extract_text() + '\n'
        return texto

    def extrair_dados(self):
        texto_unico = ' '.join(self.texto.split('\n'))
        return {
            "Item": self.caminho_pdf.name,
            "uc": RegexExtractor.extrair("uc", texto_unico),
            "venc": RegexExtractor.extrair("venc", texto_unico),
            "emissao": RegexExtractor.extrair("emis", texto_unico),
            "valor_total": RegexExtractor.extrair("val", texto_unico),
            "nota_fiscal": RegexExtractor.extrair("nf", texto_unico),
            "cod_barras": RegexExtractor.extrair("cb", texto_unico)
        }

class GerenciadorFaturas:
    def __init__(self, raiz):
        self.pasta_pendentes = Path(raiz) / "faturas_pendentes"
        self.pasta_sucesso = Path(raiz) / "faturas_sucesso"
        self.pasta_erro = Path(raiz) / "faturas_erro"
        self.lista_resultados = []

    def mover_arquivo(self, arquivo, sucesso):
        origem = self.pasta_pendentes / arquivo
        destino = self.pasta_sucesso if sucesso else self.pasta_erro
        shutil.move(origem, destino)

    def processar_faturas(self):
        for item in os.listdir(self.pasta_pendentes):
            caminho_pdf = self.pasta_pendentes / item
            processor = PDFProcessor(caminho_pdf)
            dados = processor.extrair_dados()
            self.lista_resultados.append(dados)

            if "Não encontrado" in dados.values():
                print(f"[ERRO] {item} - Campo não encontrado")
                self.mover_arquivo(item, False)
            else:
                print(f"[OK] {item} - Todos os campos extraídos")
                self.mover_arquivo(item, True)
        
        df = pd.DataFrame(self.lista_resultados)
        df.to_excel(Path(CAMINHO_RAIZ) / "faturas.xlsx", index=False)


# Execução
if __name__ == "__main__":
    gerenciador = GerenciadorFaturas(CAMINHO_RAIZ)
    gerenciador.processar_faturas()
