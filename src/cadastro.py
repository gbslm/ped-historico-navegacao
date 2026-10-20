"""Cadastro de novas URLs (comando #add)."""
from src.urls import normalizar, validar_formato


def _precisa_quebra_de_linha(caminho):
    """True se o arquivo existe, tem conteúdo e não termina com quebra de linha."""
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
    except FileNotFoundError:
        return False
    return conteudo != "" and not conteudo.endswith("\n")


def adicionar_url(banco, url, caminho_arquivo):
    """Cadastra uma url no banco (memória) e no arquivo (disco).

    Devolve a url normalizada que foi cadastrada.
    Levanta ValueError, com mensagem para o usuário, se a url estiver vazia,
    com formato inválido ou já cadastrada.
    Levanta OSError se não conseguir gravar no arquivo; nesse caso o banco
    em memória não é alterado.
    """
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