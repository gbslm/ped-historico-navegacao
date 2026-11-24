import unittest

from src.arvore import ArvoreWeb, LimiteLinksError


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

    def test_in_e_len(self):
        a = ArvoreWeb()
        a.inserir("site.com/x")
        self.assertIn("site.com/x", a)
        self.assertNotIn("site.com/y", a)
        self.assertEqual(len(a), 2)

    def test_todas_urls(self):
        a = ArvoreWeb()
        a.inserir("site.com/x/y")
        a.inserir("site.com/z")
        a.inserir("outro.com")
        self.assertEqual(a.todas_urls(),
                         ["site.com", "site.com/x", "site.com/x/y",
                          "site.com/z", "outro.com"])


if __name__ == "__main__":
    unittest.main()