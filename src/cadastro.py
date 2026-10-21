"""Cadastro de novas URLs (comando #add)."""
from src.urls import normalizar, validar_formato


def _precisa_quebra_de_linha(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
    except FileNotFoundError:
        return False
    return conteudo != "" and not conteudo.endswith("\n")


def adicionar_url(banco, url, caminho_arquivo):
    url = normalizar(url)

    if url == "":
        raise ValueError("Informe a URL depois do comando. Exemplo: #add www.exemplo.com.br")
    if not validar_formato(url):
        raise ValueError(f"Formato de URL inválido: '{url}'.")
    if url in banco:
        raise ValueError(f"A URL '{url}' já está cadastrada.")

    quebra = "\n" if _precisa_quebra_de_linha(caminho_arquivo) else ""

    # Grava primeiro no arquivo: se der erro, o banco em memória fica intacto.
    with open(caminho_arquivo, "a", encoding="utf-8") as arquivo:
        arquivo.write(quebra + url + "\n")

    banco.add(url)
    return url