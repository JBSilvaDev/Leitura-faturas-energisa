import pdfplumber

def extract_text_from_pdf(pdf_path):
    """
    Extrai o texto de um arquivo PDF.

    Args:
        pdf_path (Path): O caminho para o arquivo PDF.

    Returns:
        str: O texto extraído do PDF.
    """
    text = ''
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + '\n'
    except Exception as e:
        print(f"Erro ao extrair texto do PDF {pdf_path}: {e}")
        return ""
    return text
