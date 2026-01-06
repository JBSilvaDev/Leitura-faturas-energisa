import pandas as pd
from pathlib import Path

import config.config as config
from utils.file_handler import listar_arquivos_pendentes, mover_arquivo
from utils.pdf_extractor import extract_text_from_pdf
from model.invoice_parser import parse_invoice

def process_invoices():
    """
    Processa todas as faturas pendentes, extrai os dados e as move
    para as pastas de sucesso ou erro. Salva os dados em um arquivo Excel.
    """
    arquivos_pendentes = listar_arquivos_pendentes()
    if not arquivos_pendentes:
        print("Nenhuma fatura pendente encontrada.")
        return

    lista_faturas = []
    for pdf_file in arquivos_pendentes:
        pdf_path = config.PASTA_PENDENTES / pdf_file
        
        print(f"Processando fatura: {pdf_file}")
        
        # Extrai o texto do PDF
        extracted_text = extract_text_from_pdf(pdf_path)
        
        if not extracted_text:
            mover_arquivo(pdf_file, False)
            print(f"Erro ao extrair texto de {pdf_file}. Movido para a pasta de erro.")
            continue

        # Analisa o texto e extrai os dados
        fatura_data = parse_invoice(extracted_text)
        fatura_data["Item"] = pdf_file
        
        lista_faturas.append(fatura_data)

        # Verifica se algum campo não foi encontrado
        if "Não encontrado" in fatura_data.values():
            print(f"Houve erro na leitura de um dos campos da fatura {pdf_file}.")
            mover_arquivo(pdf_file, False)
        else:
            print(f"Fatura {pdf_file} processada com sucesso.")
            mover_arquivo(pdf_file, True)

    # Salva os resultados em um arquivo Excel
    if lista_faturas:
        df = pd.DataFrame(lista_faturas)
        try:
            df.to_excel(config.CAMINHO_EXCEL, index=False)
            print(f"Dados salvos com sucesso em {config.CAMINHO_EXCEL}")
        except Exception as e:
            print(f"Erro ao salvar o arquivo Excel: {e}")

if __name__ == '__main__':
    process_invoices()
