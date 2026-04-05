import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))

from tabelaHash import REMOVIDO, TabelaHashSondagemLinear


def montar_tabela(entradas):
    tabela = TabelaHashSondagemLinear(len(entradas))
    tabela.tabela = list(entradas)
    tabela.quantidade = sum(
        1 for entrada in entradas if entrada is not None and entrada is not REMOVIDO
    )
    return tabela


class TestHashDesvios(unittest.TestCase):
    def test_rejeita_capacidade_nao_positiva(self):
        with self.assertRaises(ValueError):
            TabelaHashSondagemLinear(0)

    def test_funcao_hash_cobre_int_str_e_outro_tipo(self):
        tabela = TabelaHashSondagemLinear(5)

        self.assertEqual(tabela.funcao_hash(7), 2)
        self.assertEqual(tabela.funcao_hash("ab"), (ord("a") + ord("b")) % 5)
        self.assertEqual(
            tabela.funcao_hash((1, 2)),
            sum(ord(caractere) for caractere in str((1, 2))) % 5,
        )

    def test_inserir_buscar_atualizar_remover_e_reutilizar_posicao_removida(self):
        tabela = TabelaHashSondagemLinear(3)

        tabela.inserir(0, "zero")
        self.assertEqual(tabela.buscar(0), "zero")
        self.assertEqual(len(tabela), 1)

        tabela.inserir(0, "ZERO")
        self.assertEqual(tabela.buscar(0), "ZERO")
        self.assertEqual(len(tabela), 1)

        tabela.remover(0)
        self.assertIs(tabela.tabela[0], REMOVIDO)
        self.assertEqual(len(tabela), 0)

        tabela.inserir(3, "tres")
        self.assertEqual(tabela.buscar(3), "tres")
        self.assertEqual(tabela.tabela[0], (3, "tres"))
        self.assertTrue(tabela.contem(3))
        self.assertFalse(tabela.contem(0))

    def test_busca_e_remocao_de_chave_inexistente_lancam_keyerror(self):
        tabela = TabelaHashSondagemLinear(3)
        tabela.inserir(0, "zero")

        with self.assertRaises(KeyError):
            tabela.buscar(3)

        with self.assertRaises(KeyError):
            tabela.remover(3)

    def test_inserir_lanca_overflow_quando_tabela_esta_cheia(self):
        tabela = TabelaHashSondagemLinear(2)
        tabela.inserir(0, "zero")
        tabela.inserir(1, "um")

        with self.assertRaises(OverflowError):
            tabela.inserir(2, "dois")

    def test_procurar_posicao_diferencia_busca_e_insercao_em_tabela_sem_vazios(self):
        tabela = montar_tabela([REMOVIDO, (1, "um"), (2, "dois")])

        self.assertEqual(tabela._procurar_posicao(3, para_insercao=True), 0)
        self.assertIsNone(tabela._procurar_posicao(3, para_insercao=False))

    def test_chaves_valores_itens_e_str_ignoram_vazios_e_removidos(self):
        tabela = montar_tabela([None, REMOVIDO, (2, "dois")])

        self.assertEqual(tabela.chaves(), [2])
        self.assertEqual(tabela.valores(), ["dois"])
        self.assertEqual(tabela.itens(), [(2, "dois")])

        representacao = str(tabela)
        self.assertIn("0: VAZIO", representacao)
        self.assertIn("1: REMOVIDO", representacao)
        self.assertIn("2: 2 -> dois", representacao)


if __name__ == "__main__":
    unittest.main()
