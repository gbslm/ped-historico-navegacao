"""Catálogo de URLs válidas (a nossa "Wide World Web" simulada).

Guarda as URLs numa ArvoreWeb (arvore.py). O arquivo urls.txt carrega as
URLs na inicialização e registra as novas cadastradas; os textos das
páginas ficam em arquivos .txt (conteudo.py), na pasta 'paginas' ao lado
do urls.txt.
"""

import os

import conteudo
from arvore import ArvoreWeb, LimiteLinksError

CAMINHO_PADRAO = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "data", "urls.txt")


def normalizar(url):
    """Padroniza a URL: minúsculas, sem http(s):// e sem '/' no final."""
    url = url.strip().lower()
    for prefixo in ("http://", "https://"):
        if url.startswith(prefixo):
            url = url[len(prefixo):]
    return url.rstrip("/")


def formato_valido(url):
    """Verifica o formato: domínio com ponto, sem espaços, sem '//' ou '/' inicial."""
    if url == "" or " " in url:
        return False
    partes = url.split("/")
    if "" in partes:            # pega "a//b" e "/a"
        return False
    dominio = partes[0]
    if "." not in dominio or dominio.startswith(".") or dominio.endswith("."):
        return False
    return True


class Catalogo:
    def __init__(self, caminho=CAMINHO_PADRAO, pasta_paginas=None):
        self._caminho = caminho
        if pasta_paginas is None:
            pasta_paginas = os.path.join(os.path.dirname(caminho), "paginas")
        self._pasta = pasta_paginas
        self._arvore = ArvoreWeb()

    def carregar(self):
        """Lê o arquivo e popula a árvore.

        Retorna (qtd_de_paginas, lista_de_linhas_ignoradas).
        Levanta FileNotFoundError se o arquivo não existir.
        """
        ignoradas = []
        with open(self._caminho, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if linha == "" or linha.startswith("#"):
                    continue
                url = normalizar(linha)
                if not formato_valido(url):
                    ignoradas.append(linha)
                    continue
                try:
                    self._arvore.inserir(url)
                except LimiteLinksError:
                    ignoradas.append(linha)
        return self._arvore.quantidade(), ignoradas

    def existe(self, url):
        return self._arvore.buscar(url) is not None

    def links(self, url):
        """Links internos disponíveis a partir da URL."""
        return self._arvore.links(url)

    def conteudo(self, url):
        """Texto do arquivo da página (levanta OSError se não puder ler)."""
        return conteudo.ler(self._pasta, url)

    def adicionar(self, url):
        """Cadastra uma URL (e as páginas do caminho). Retorna (sucesso, mensagem)."""
        url = normalizar(url)
        if not formato_valido(url):
            return False, "Formato de URL inválido. Exemplo: www.site.com.br/pasta"
        if self.existe(url):
            return False, "Essa URL já está cadastrada."
        try:
            criadas = self._arvore.inserir(url)
        except LimiteLinksError as erro:
            return False, str(erro)

        mensagem = f"URL '{url}' cadastrada com sucesso!"
        if len(criadas) > 1:
            mensagem += " Páginas criadas: " + ", ".join(criadas)
        try:
            with open(self._caminho, "a", encoding="utf-8") as arquivo:
                arquivo.write(url + "\n")
            for nova in criadas:
                conteudo.criar_padrao(self._pasta, nova)
        except OSError as erro:
            mensagem += f" (Aviso: não foi possível gravar em disco: {erro})"
        return True, mensagem

    def quantidade(self):
        return self._arvore.quantidade()
