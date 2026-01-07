import re
import config.config as config

def extract_field(field_key, text):
    """
    Extrai um campo do texto usando uma lista de expressões regulares.

    Args:
        field_key (str): A chave para o dicionário de regex em config.
        text (str): O texto onde procurar o padrão.

    Returns:
        str: O valor encontrado ou "Não encontrado".
    """
    for rgx in config.REGEX[field_key]:
        match = re.search(rgx, text)
        if match:
            try:
                # Tenta retornar o primeiro grupo de captura, se existir
                return match.group(1)
            except IndexError:
                # Se não houver grupo de captura, retorna a correspondência inteira
                return match.group()
    return "Não encontrado"

def parse_invoice(text):
    """
    Analisa o texto de uma fatura e extrai os dados.

    Args:
        text (str): O texto da fatura.

    Returns:
        dict: Um dicionário com os dados extraídos.
    """
    # Junta as linhas do texto para facilitar a busca com regex
    full_text = ' '.join(text.split('\n'))
    
    invoice_data = {
        "uc": extract_field("uc", full_text),
        "venc": extract_field("venc", full_text),
        "emissao": extract_field("emis", full_text),
        "valor_total": extract_field("val", full_text),
        "nota_fiscal": extract_field("nf", full_text),
        "cod_barras": extract_field("cb", full_text),
        "endereco": extract_field("end", full_text)
    }
    return invoice_data
