import os
import shutil
from pathlib import Path
import config.config as config

def mover_arquivo(arquivo, status):
    """
    Move um arquivo para a pasta de sucesso ou erro.

    Args:
        arquivo (str): O nome do arquivo a ser movido.
        status (bool): True para sucesso, False para erro.
    """
    origem = config.PASTA_PENDENTES / arquivo
    if status:
        destino = config.PASTA_SUCESSO
    else:
        destino = config.PASTA_ERRO
    
    # Garante que a pasta de destino exista
    destino.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(origem, destino)
    except Exception as e:
        print(f"Erro ao mover o arquivo {arquivo}: {e}")

def listar_arquivos_pendentes():
    """
    Lista os arquivos na pasta de faturas pendentes.

    Returns:
        list: Uma lista de nomes de arquivos.
    """
    try:
        return os.listdir(config.PASTA_PENDENTES)
    except FileNotFoundError:
        print(f"A pasta {config.PASTA_PENDENTES} não foi encontrada.")
        return []
