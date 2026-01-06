from pathlib import Path
import os

# Obtém o caminho absoluto para o diretório do projeto
CAMINHO_RAIZ = Path(__file__).parent.resolve()

# Define os caminhos para as pastas
PASTA_PENDENTES = CAMINHO_RAIZ / "faturas_pendentes"
PASTA_SUCESSO = CAMINHO_RAIZ / "faturas_sucesso"
PASTA_ERRO = CAMINHO_RAIZ / "faturas_erro"
CAMINHO_EXCEL = CAMINHO_RAIZ / "faturas.xlsx"

# Verifica e cria as pastas, se necessário
for pasta in [PASTA_PENDENTES, PASTA_SUCESSO, PASTA_ERRO]:
    if not pasta.exists():
        pasta.mkdir(parents=True, exist_ok=True)

# Regex para extração de dados
REGEX = {
    "uc": [r"CÓDIGO:\s*(\d+)\d", r"UC:\s*(\d+)"],
    "venc": [
        r"Protocolo de Autorização:.*?(\d{2}/\d{2}/\d{4})\s*R\$",
        r"\d{4}-\d{2}-\d\s+(\d{2}/\d{2}/\d{4})",
    ],
    "emis": [
        r"EMISS[ÃA]O\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})",
        r"DATA EMISSÂO/APRESENTAÇÂO:(\d{2}/\d{2}/\d{4})",
    ],
    "nf": [
        r"NOTA FISCAL Nº[:\-]?\s*(\d{3}\.\d{3}\.\d{3})",
        r"NOTA FISCAL N°[:\-]?\s*(\d{3}\.\d{3}\.\d{3})",
    ],
    "cb": [
        r"(\d{11}-\d\s\d{11}-\d\s\d{11,13}-\d\s\d{11}-\d)",
        r"(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})",
    ],
    "val": [r"R\$ (\d{1,3},\d{2})"],
}
