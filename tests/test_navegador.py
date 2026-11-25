import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import resolver_destino


class TestResolverDestino(unittest.TestCase):
    def test_url_completa(self):
        self.assertEqual(resolver_destino("HTTPS://WWW.A.com/x/", None),
                         ("www.a.com/x", None))

    def test_caminho_interno_usa_home(self):
        self.assertEqual(resolver_destino("/tsi", "www.a.com"),
                         ("www.a.com/tsi", None))
        self.assertEqual(resolver_destino("/tsi/alunos", "www.a.com"),
                         ("www.a.com/tsi/alunos", None))

    def test_caminho_interno_sem_home(self):
        url, erro = resolver_destino("/tsi", None)
        self.assertIsNone(url)
        self.assertIsNotNone(erro)

    def test_entradas_invalidas(self):
        for entrada in ["semponto", "/", "/a b", "//x", "a.com//b"]:
            url, erro = resolver_destino(entrada, "www.a.com")
            self.assertIsNone(url, entrada)
            self.assertIsNotNone(erro, entrada)


if __name__ == "__main__":
    unittest.main()
