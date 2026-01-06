from controller.invoice_processor import process_invoices

def main():
    """
    Ponto de entrada principal para a aplicação de processamento de faturas.
    """
    print("Iniciando o processamento de faturas...")
    process_invoices()
    print("Processamento de faturas finalizado.")

if __name__ == "__main__":
    main()