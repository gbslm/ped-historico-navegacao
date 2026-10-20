"""Histórico de navegação.

Estrutura de dados: PILHA implementada com nós encadeados.

Cada nó guarda uma url e "aponta" (referência) para o nó que está abaixo
dele na pilha. A variável _topo aponta para o nó de cima.

    _topo -> [www.apple.com] -> [www.google.com.br] -> [www.ifpb.edu.br] -> None

Empilhar e voltar mexem apenas no topo, por isso as duas operações são O(1).
"""


class NoHistorico:
    """Um elemento da pilha: guarda uma url e aponta para o próximo nó."""

    def __init__(self, url, proximo=None):
        self.url = url
        self.proximo = proximo


class Historico:
    """Pilha de URLs visitadas anteriormente (não inclui o home atual)."""

    def __init__(self):
        self._topo = None      # pilha vazia: ninguém no topo
        self._tamanho = 0

    def empilhar(self, url):
        """Coloca uma url no topo da pilha."""
        # O novo nó passa a apontar para o antigo topo...
        novo = NoHistorico(url, self._topo)
        # ...e o topo passa a ser o novo nó.
        self._topo = novo
        self._tamanho += 1

    def voltar(self):
        """Remove a url do topo e a devolve. Devolve None se a pilha estiver vazia."""
        if self._topo is None:
            return None
        url = self._topo.url
        self._topo = self._topo.proximo   # o nó de baixo vira o topo
        self._tamanho -= 1
        return url

    def esta_vazio(self):
        """True se não há nenhuma url na pilha."""
        return self._topo is None

    def tamanho(self):
        """Quantidade de urls na pilha."""
        return self._tamanho

    def como_lista(self):
        """Devolve uma lista com as urls, da mais antiga para a mais recente."""
        urls = []
        atual = self._topo
        while atual is not None:       # percorre do topo até o fundo
            urls.append(atual.url)
            atual = atual.proximo
        urls.reverse()                 # o topo é a mais recente, então inverte
        return urls