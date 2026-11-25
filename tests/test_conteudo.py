import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(_file_))))

import conteudo


class TestConteudo(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.pasta = os.path.join(self.tmp.name, "paginas")

    def tearDown(self):
        self.tmp.cleanup()

    def test_nome_do_arquivo(self):
        caminho = conteudo.caminho_arquivo(self.pasta, "a.com/b/c")
        self.assertTrue(caminho.endswith("a.com_b_c.txt"))

    def test_criar_e_ler(self):
        self.assertTrue(conteudo.criar_padrao(self.pasta, "a.com/b"))
        self.assertIn("a.com/b", conteudo.ler(self.pasta, "a.com/b"))

    def test_nao_sobrescreve(self):
        conteudo.criar_padrao(self.pasta, "a.com")
        with open(conteudo.caminho_arquivo(self.pasta, "a.com"), "w", encoding="utf-8") as f:
            f.write("meu texto")
        self.assertFalse(conteudo.criar_padrao(self.pasta, "a.com"))
        self.assertEqual(conteudo.ler(self.pasta, "a.com"), "meu texto")

    def test_ler_inexistente(self):
        with self.assertRaises(FileNotFoundError):
            conteudo.ler(self.pasta, "nao.existe.com")


if _name_ == "_main_":
    unittest.main()
