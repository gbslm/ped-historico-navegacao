"""Arquivos de conteúdo das páginas (Checkpoint 2).

Cada URL válida tem um arquivo .txt na pasta de páginas. O nome do
arquivo é a URL com '/' trocado por '_':

    www.ifpb.edu.br/tsi  ->  www.ifpb.edu.br_tsi.txt
"""

import os


def caminho_arquivo(pasta, url):
    """Caminho do .txt associado à URL."""
    return os.path.join(pasta, url.replace("/", "_") + ".txt")


def ler(pasta, url):
    """Devolve o texto da página.

    Levanta FileNotFoundError (ou outro OSError) se não for possível ler.
    """
    with open(caminho_arquivo(pasta, url), "r", encoding="utf-8") as arquivo:
        return arquivo.read().rstrip()


def criar_padrao(pasta, url):
    """Cria o .txt com um texto padrão, se ele ainda não existir.

    Retorna True se criou, False se já existia.
    """
    caminho = caminho_arquivo(pasta, url)
    if os.path.exists(caminho):
        return False
    os.makedirs(pasta, exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(f"Conteúdo de exemplo da página {url}.\n"
                      "Edite este arquivo para mudar o texto exibido.\n")
    return True
