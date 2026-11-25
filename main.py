"""Navegador web simulado - Checkpoints 1 e 2.

Execute com:  python main.py
"""

from catalogo import Catalogo, normalizar, formato_valido
from historico import Historico

LINHA = "-" * 55

TEXTO_AJUDA = """
=== Ajuda ===
  <url>          Acessa uma página cadastrada.      Ex.: www.ifpb.edu.br/tsi
  /<pasta>       Acessa uma página interna da página atual (home).
                 Ex.: estando em www.ifpb.edu.br, digite /tsi
  #back          Volta para a última página visitada.
  #showhist      Mostra a página atual e o histórico de visitas.
  #add <url>     Cadastra uma URL (e as páginas do caminho).
                 Ex.: #add www.site.com/loja/ofertas
                 Também aceita caminho interno: #add /ofertas (usa a home)
  #help          Mostra esta ajuda.
  #sair          Encerra o programa.
Obs.: cada página pode ter no máximo 2 links internos.
"""


def mostrar_estado(historico):
    """Mostra o painel com histórico e home."""
    visitadas = historico.paginas_visitadas()
    texto_hist = "".join(f"[{u}]" for u in visitadas) if visitadas else "[ ]"
    texto_home = f"[{historico.home}]" if historico.home else "[ ]"
    print(LINHA)
    print("Histórico de Visitas:", texto_hist)
    print("Home:", texto_home)
    print("Digite a url, #back, #showhist, #add <url>, #help ou #sair.")


def mostrar_pagina(catalogo, url):
    """Exibe o conteúdo do arquivo da página e seus links internos."""
    print("\nPágina encontrada!")
    print(f"url: {url}")
    try:
        print(catalogo.conteudo(url))
    except OSError:
        print("(Conteúdo indisponível: arquivo .txt da página não encontrado.)")
    links = catalogo.links(url)
    if links:
        print("\nLinks disponíveis:")
        for link in links:
            print(link)
    else:
        print("\nEsta página não tem links internos.")


def resolver_destino(entrada, home):
    """Transforma o que foi digitado em uma URL completa.

    Entrada iniciada por '/' é um caminho interno da home atual.
    Retorna (url, None) se deu certo, ou (None, mensagem_de_erro).
    """
    if entrada.startswith("/"):
        if home is None:
            return None, ("Você ainda não está em nenhuma página. "
                          "Digite uma URL completa primeiro.")
        caminho = entrada.lower().rstrip("/")
        if caminho == "":
            return None, "Caminho interno inválido. Exemplo: /tsi"
        url = home + caminho
    else:
        url = normalizar(entrada)
    if not formato_valido(url):
        return None, "URL com formato inválido. Exemplo: www.ifpb.edu.br"
    return url, None


def acessar_url(catalogo, historico, entrada):
    url, erro = resolver_destino(entrada, historico.home)
    if erro:
        print(erro)
    elif not catalogo.existe(url):
        print("Página não encontrada!")
    else:
        historico.visitar(url)
        mostrar_pagina(catalogo, url)


def comando_showhist(historico):
    print("\n=== Situação do histórico ===")
    if historico.home is None:
        print("Nenhuma página visitada ainda.")
        return
    print(f"Página atual (home): {historico.home}")
    visitadas = historico.paginas_visitadas()
    if not visitadas:
        print("Histórico vazio (não há página anterior).")
        return
    print("Páginas anteriores (da mais recente para a mais antiga):")
    for posicao, url in enumerate(reversed(visitadas), start=1):
        print(f"  {posicao}. {url}")


def comando_back(catalogo, historico):
    if historico.voltar():
        print(f"Voltando para: {historico.home}")
        mostrar_pagina(catalogo, historico.home)
    else:
        print("Não há página anterior no histórico para voltar.")


def comando_add(catalogo, historico, argumento):
    if argumento == "":
        print("Uso: #add <url>   Exemplo: #add www.exemplo.com.br/loja")
        return
    url, erro = resolver_destino(argumento, historico.home)
    if erro:
        print(erro)
        return
    _, mensagem = catalogo.adicionar(url)
    print(mensagem)


def processar(entrada, catalogo, historico):
    """Trata uma linha digitada. Retorna False quando deve encerrar."""
    entrada = entrada.strip()
    if entrada == "":
        return True

    if entrada.startswith("#"):
        partes = entrada.split(maxsplit=1)
        comando = partes[0].lower()
        argumento = partes[1] if len(partes) > 1 else ""

        if comando == "#sair":
            print("Encerrando o navegador. Até logo!")
            return False
        elif comando == "#back":
            comando_back(catalogo, historico)
        elif comando == "#showhist":
            comando_showhist(historico)
        elif comando == "#add":
            comando_add(catalogo, historico, argumento)
        elif comando == "#help":
            print(TEXTO_AJUDA)
        else:
            print(f"Comando '{comando}' desconhecido. Digite #help para ver os comandos.")
    else:
        acessar_url(catalogo, historico, entrada)
    return True


def main():
    catalogo = Catalogo()
    historico = Historico()

    try:
        qtd, ignoradas = catalogo.carregar()
        print(f"{qtd} páginas carregadas do arquivo.")
        for linha in ignoradas:
            print(f"Aviso: linha ignorada (formato inválido ou limite de links): {linha}")
    except FileNotFoundError:
        print("Aviso: arquivo data/urls.txt não encontrado. Começando sem URLs.")
    except OSError as erro:
        print(f"Erro ao ler o arquivo de URLs: {erro}")

    print("Digite #help para ver os comandos.")
    continuar = True
    while continuar:
        mostrar_estado(historico)
        try:
            entrada = input("url: ")
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando o navegador.")
            break
        continuar = processar(entrada, catalogo, historico)


if __name__ == "__main__":
    main()
