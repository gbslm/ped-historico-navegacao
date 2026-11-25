import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from catalogo import Catalogo
import conteudo


class TestCatalogoCP2(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.caminho = os.path.join(self.tmp.name, "urls.txt")
        with open(self.caminho, "w", encoding="utf-8") as f:
            f.write("www.a.com/x/y\nwww.a.com/z\nwww.a.com/w\n")
        self.cat = Catalogo(self.caminho)

    def tearDown(self):
        self.tmp.cleanup()

    def test_carregar_ignora_estouro_de_limite(self):
        qtd, ignoradas = self.cat.carregar()
        self.assertEqual(ignoradas, ["www.a.com/w"])
        self.assertEqual(qtd, 4)  # a.com, x, y, z
        self.assertEqual(self.cat.links("www.a.com"), ["/x", "/z"])

    def test_ancestrais_sao_validos(self):
        self.cat.carregar()
        self.assertTrue(self.cat.existe("www.a.com/x"))

    def test_adicionar_pagina_interna_cria_arquivos(self):
        self.cat.carregar()
        ok, _ = self.cat.adicionar("www.b.com/loja/ofertas")
        self.assertTrue(ok)
        pasta = os.path.join(self.tmp.name, "paginas")
        for url in ["www.b.com", "www.b.com/loja", "www.b.com/loja/ofertas"]:
            self.assertIn(url, conteudo.ler(pasta, url))
        self.assertIn("www.b.com/loja", self.cat.conteudo("www.b.com/loja"))

    def test_adicionar_estourando_limite(self):
        self.cat.carregar()
        ok, _ = self.cat.adicionar("www.a.com/novo")
        self.assertFalse(ok)
        self.assertFalse(self.cat.existe("www.a.com/novo"))

    def test_adicionar_persiste_para_proxima_execucao(self):
        self.cat.carregar()
        self.cat.adicionar("www.b.com/loja")
        novo = Catalogo(self.caminho)
        novo.carregar()
        self.assertTrue(novo.existe("www.b.com/loja"))


if __name__ == "__main__":
    unittest.main()
