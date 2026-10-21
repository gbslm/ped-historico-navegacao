"""Histórico de navegação.

Estrutura de dados: PILHA implementada com nós encadeados.

Cada nó guarda uma url e "aponta" (referência) para o nó que está abaixo
dele na pilha. A variável _topo aponta para o nó de cima.

    _topo -> [www.apple.com] -> [www.google.com.br] -> [www.ifpb.edu.br] -> None

Empilhar e voltar mexem apenas no topo, por isso as duas operações são O(1).
"""


class NoHistorico:

    def __init__(self, url, proximo=None):
        self.url = url
        self.proximo = proximo


class Historico:

    def __init__(self):
        self._topo = None      # pilha vazia: ninguém no topo
        self._tamanho = 0

    def empilhar(self, url):
        novo = NoHistorico(url, self._topo)
        self._topo = novo
        self._tamanho += 1

    def voltar(self):
        if self._topo is None:
            return None
        url = self._topo.url
        self._topo = self._topo.proximo   # o nó de baixo vira o topo
        self._tamanho -= 1
        return url

    def esta_vazio(self):
        return self._topo is None

    def tamanho(self):
        return self._tamanho

    def como_lista(self):
        urls = []
        atual = self._topo
        while atual is not None:      
            urls.append(atual.url)
            atual = atual.proximo
        urls.reverse()               
        return urls