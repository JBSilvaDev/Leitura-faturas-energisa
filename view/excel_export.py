import pandas as pd

class ExcelExporter:
    def __init__(self):
        pass
    
    def exportar_dados(dados, caminho_arquivo):
        df = pd.DataFrame(dados)
        df.to_excel(caminho_arquivo, index=False)