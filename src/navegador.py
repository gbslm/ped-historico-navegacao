
from src.cadastro import adicionar_url
from src.historico import Historico
from src.urls import carregar_urls, normalizar, validar_formato

CAMINHO_URLS = "dados/urls.txt"

COMANDOS_DISPONIVEIS = "#back, #sair, #showhist, #add <url>"


def formatar_lista(urls):
    """Formata como [url1][url2]..., ou [ ] quando a lista está vazia."""
    if len(urls) == 0:
        return "[ ]"
    texto = ""
    for url in urls:
        texto += f"[{url}]"
    return texto


class Navegador:
    """Guarda o estado da navegação (home, histórico e urls cadastradas)."""

    def __init__(self, banco, caminho_urls):
        self._banco = banco                  
        self._caminho_urls = caminho_urls
        self._historico = Historico()
        self._home = None         

    def obter_home(self):
        return self._home

    def obter_historico(self):
        return self._historico.como_lista()


    def visitar(self, url):
   
        url = normalizar(url)

        if not validar_formato(url):
            print(f"Formato de URL inválido: '{url}'.")
            print("Exemplos válidos: www.ifpb.edu.br ou http://example.com/register")
            return False

        if url not in self._banco:
            print(f"Página não encontrada (404): '{url}'.")
            print("Use #add <url> para cadastrá-la.")
            return False

        if url == self._home:
            print("Você já está nesta página.")
            return False

  
        if self._home is not None:
            self._historico.empilhar(self._home)
        self._home = url
        print("Página encontrada!")
        return True

    def voltar(self):
        anterior = self._historico.voltar()
        if anterior is None:
            print("Não há página anterior no histórico.")
            return False
        self._home = anterior
        print(f"Voltando para: {anterior}")
        return True

    def mostrar_historico(self):
        
        if self._home is None:
            print("Nenhuma página visitada ainda.")
            return
        print("Situação atual do histórico:")
        print(f"  Home (atual): {self._home}")
        urls = self._historico.como_lista()
        urls.reverse()   
        posicao = 1
        for url in urls:
            print(f"  {posicao}. {url}")
            posicao += 1

    def cadastrar(self, url):
        
        try:
            cadastrada = adicionar_url(self._banco, url, self._caminho_urls)
        except ValueError as erro:
            print(f"Erro: {erro}")
        except OSError as erro:
            print(f"Não foi possível gravar no arquivo de URLs: {erro}")
        else:
            print(f"URL cadastrada com sucesso: {cadastrada}")

    def executar(self, entrada):
        
        entrada = entrada.strip()

        if entrada == "":
            print(f"Digite uma url ou um comando ({COMANDOS_DISPONIVEIS}).")
            return True

        if entrada.startswith("#"):
            return self._executar_comando(entrada)

        if entrada.startswith("/"):
            print("A navegação por páginas internas (/pagina) será feita no Checkpoint 2.")
            print("Por enquanto, digite a URL completa.")
            return True

        self.visitar(entrada)
        return True

    def _executar_comando(self, entrada):
        partes = entrada.split(maxsplit=1)    
        comando = partes[0].lower()
        argumento = ""
        if len(partes) > 1:
            argumento = partes[1]

        if comando == "#sair":
            print("Encerrando o navegador. Até logo!")
            return False
        if comando == "#back":
            self.voltar()
        elif comando == "#showhist":
            self.mostrar_historico()
        elif comando == "#add":
            self.cadastrar(argumento)
        else:
            print(f"Comando desconhecido: {comando}")
            print(f"Comandos disponíveis: {COMANDOS_DISPONIVEIS}")
        return True

    def _mostrar_cabecalho(self):
        if self._home is None:
            home = "[ ]"
        else:
            home = f"[{self._home}]"
        print()
        print("-" * 60)
        print(f"Histórico de Visitas: {formatar_lista(self._historico.como_lista())}")
        print(f"Home: {home}")
        print("Digite a url ou #back para retornar à última página visitada.")

    def rodar(self):
        continuar = True
        while continuar:
            self._mostrar_cabecalho()
            try:
                entrada = input("url: ")
            except (EOFError, KeyboardInterrupt):
                print("\nEncerrando o navegador. Até logo!")
                break
            continuar = self.executar(entrada)


def iniciar(caminho_urls=CAMINHO_URLS):
    """Carrega o arquivo de URLs e inicia a interface."""
    print("=" * 60)
    print("Navegador simulado - Histórico de Navegação")
    print("=" * 60)

    try:
        banco = carregar_urls(caminho_urls)
    except FileNotFoundError:
        print(f"Aviso: arquivo '{caminho_urls}' não encontrado.")
        print("Execute o programa a partir da pasta do projeto.")
        print("Começando sem URLs; use #add <url> para cadastrar.")
        banco = set()
    except (OSError, UnicodeDecodeError) as erro:
        print(f"Erro ao ler o arquivo de URLs: {erro}")
        return

    print(f"{len(banco)} URL(s) carregada(s).")
    print(f"Comandos: {COMANDOS_DISPONIVEIS}")

    navegador = Navegador(banco, caminho_urls)
    navegador.rodar()