"""Representação das URLs e de suas páginas internas (Checkpoint 2).

Cada URL é um caminho dentro de uma ÁRVORE:

    www.ifpb.edu.br              <- raiz (domínio)
        /tsi
            /professores
            /alunos
        /rc

Regras do professor aplicadas aqui:
  * só existe um nó por domínio (não há dois domínios iguais);
  * cada página tem no máximo 2 links internos (MAX_LINKS);
  * toda página do caminho é válida (se existe /rc/coordenacao, então
    www.ifpb.edu.br/rc também existe).

Cada nível guarda seus filhos num dicionário (nome -> Pagina), então
descer um nível é O(1) e buscar uma URL custa O(profundidade).
"""

MAX_LINKS = 2


class LimiteLinksError(Exception):
    """Levantada quando uma página já tem MAX_LINKS links internos."""


class Pagina:
    """Um nó da árvore: o nome do trecho da URL e seus links internos."""

    def __init__(self, nome):
        self.nome = nome
        self.filhos = {}  # nome -> Pagina (em ordem de cadastro)


class ArvoreWeb:
    def __init__(self):
        self._dominios = {}   # único "root server": domínio -> Pagina
        self._total = 0       # quantidade de páginas cadastradas

    def inserir(self, url):
        """Cadastra a URL e todas as páginas do caminho que ainda não existem.

        Retorna a lista de URLs criadas agora (da mais curta para a mais longa).
        Levanta LimiteLinksError, sem alterar a árvore, se estourar o limite.
        """
        partes = url.split("/")

        # 1ª passada: só confere o limite (não altera nada)
        nivel = self._dominios
        for i, parte in enumerate(partes):
            if parte in nivel:
                nivel = nivel[parte].filhos
            else:
                if nivel is not self._dominios and len(nivel) >= MAX_LINKS:
                    pai = "/".join(partes[:i])
                    raise LimiteLinksError(
                        f"A página '{pai}' já tem {MAX_LINKS} links internos.")
                break

        # 2ª passada: cria os nós que faltam
        criadas = []
        nivel = self._dominios
        for i, parte in enumerate(partes):
            if parte not in nivel:
                nivel[parte] = Pagina(parte)
                self._total += 1
                criadas.append("/".join(partes[:i + 1]))
            nivel = nivel[parte].filhos
        return criadas

    def buscar(self, url):
        """Retorna a Pagina da URL ou None se ela não existir."""
        nivel = self._dominios
        pagina = None
        for parte in url.split("/"):
            if parte not in nivel:
                return None
            pagina = nivel[parte]
            nivel = pagina.filhos
        return pagina

    def links(self, url):
        """Links internos da URL, no formato ['/tsi', '/rc'] ([] se não houver)."""
        pagina = self.buscar(url)
        if pagina is None:
            return []
        return ["/" + nome for nome in pagina.filhos]

    def quantidade(self):
        return self._total