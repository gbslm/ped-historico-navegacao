import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arvore import ArvoreWeb, LimiteLinksError


class TestArvore(unittest.TestCase):
    def test_inserir_cria_ancestrais(self):
        a = ArvoreWeb()
        criadas = a.inserir("site.com/x/y")
        self.assertEqual(criadas, ["site.com", "site.com/x", "site.com/x/y"])
        self.assertIsNotNone(a.buscar("site.com/x"))
        self.assertEqual(a.quantidade(), 3)

    def test_buscar_inexistente(self):
        a = ArvoreWeb()
        a.inserir("site.com/x")
        self.assertIsNone(a.buscar("site.com/z"))
        self.assertIsNone(a.buscar("outro.com"))

    def test_dominio_nao_duplica(self):
        a = ArvoreWeb()
        a.inserir("site.com/x")
        a.inserir("site.com/y")
        self.assertEqual(a.quantidade(), 3)  # site.com, /x, /y

    def test_links_em_ordem_de_cadastro(self):
        a = ArvoreWeb()
        a.inserir("site.com/tsi")
        a.inserir("site.com/rc")
        self.assertEqual(a.links("site.com"), ["/tsi", "/rc"])
        self.assertEqual(a.links("site.com/tsi"), [])

    def test_limite_de_dois_links(self):
        a = ArvoreWeb()
        a.inserir("site.com/a")
        a.inserir("site.com/b")
        with self.assertRaises(LimiteLinksError):
            a.inserir("site.com/c/d")
        self.assertIsNone(a.buscar("site.com/c"))   # nada foi criado
        self.assertEqual(a.quantidade(), 3)


if __name__ == "__main__":
    unittest.main()