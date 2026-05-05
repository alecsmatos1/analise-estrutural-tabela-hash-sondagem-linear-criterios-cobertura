import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))

from tabelaHash import REMOVIDO, TabelaHashSondagemLinear


class ObjetoStrVazio:
    def __str__(self):
        return ""


class ObjetoStrUmCaractere:
    def __str__(self):
        return "x"


def montar_tabela(entradas, capacidade=None):
    tabela = TabelaHashSondagemLinear.__new__(TabelaHashSondagemLinear)
    tabela.capacidade = capacidade if capacidade is not None else len(entradas)
    tabela.tabela = list(entradas)
    tabela.quantidade = sum(
        1 for entrada in entradas if entrada is not None and entrada is not REMOVIDO
    )
    return tabela


class TestHashEdgePair(unittest.TestCase):
    def test_construtor_rejeita_capacidade_invalida(self):
        with self.assertRaises(ValueError):
            TabelaHashSondagemLinear(0)

    def test_funcao_hash_cobre_pares_dos_lacos(self):
        tabela = TabelaHashSondagemLinear(5)

        self.assertEqual(tabela.funcao_hash(7), 2)
        self.assertEqual(tabela.funcao_hash(""), 0)
        self.assertEqual(tabela.funcao_hash("a"), ord("a") % 5)
        self.assertEqual(tabela.funcao_hash("ab"), (ord("a") + ord("b")) % 5)
        self.assertEqual(tabela.funcao_hash(ObjetoStrVazio()), 0)
        self.assertEqual(tabela.funcao_hash(ObjetoStrUmCaractere()), ord("x") % 5)
        self.assertEqual(
            tabela.funcao_hash((1, 2)),
            sum(ord(caractere) for caractere in str((1, 2))) % 5,
        )

    def test_busca_para_ao_encontrar_none(self):
        tabela = TabelaHashSondagemLinear(3)

        self.assertIsNone(tabela._procurar_posicao(0, para_insercao=False))

    def test_insercao_em_none_sem_removido_previo(self):
        tabela = TabelaHashSondagemLinear(3)

        self.assertEqual(tabela._procurar_posicao(0, para_insercao=True), 0)

    def test_removido_seguido_de_none_retorna_primeiro_removido(self):
        tabela = montar_tabela([REMOVIDO, None, None])

        self.assertEqual(tabela._procurar_posicao(0, para_insercao=True), 0)

    def test_segundo_removido_nao_substitui_o_primeiro(self):
        tabela = montar_tabela([REMOVIDO, REMOVIDO, None])

        self.assertEqual(tabela._procurar_posicao(0, para_insercao=True), 0)

    def test_colisao_avanca_ate_encontrar_a_chave(self):
        tabela = montar_tabela([(3, "tres"), (0, "zero"), None])

        self.assertEqual(tabela._procurar_posicao(0, para_insercao=False), 1)

    def test_varredura_completa_distingue_insercao_e_busca_sem_none(self):
        tabela = montar_tabela([REMOVIDO, (1, "um"), (2, "dois")])

        self.assertEqual(tabela._procurar_posicao(3, para_insercao=True), 0)
        self.assertIsNone(tabela._procurar_posicao(3, para_insercao=False))

    def test_operacoes_publicas_cobrem_pares_de_inserir_buscar_remover(self):
        tabela = TabelaHashSondagemLinear(2)
        tabela.inserir(0, "zero")
        tabela.inserir(0, "ZERO")
        self.assertEqual(tabela.buscar(0), "ZERO")

        tabela.remover(0)
        self.assertFalse(tabela.contem(0))
        tabela.inserir(2, "dois")

        tabela.inserir(1, "um")
        with self.assertRaises(OverflowError):
            tabela.inserir(3, "tres")
        with self.assertRaises(KeyError):
            tabela.buscar(3)
        with self.assertRaises(KeyError):
            tabela.remover(3)

    def test_coletores_cobrem_pares_de_estados(self):
        cenarios = [
            [],
            [None, None],
            [None, REMOVIDO],
            [None, (1, "um")],
            [REMOVIDO, None],
            [REMOVIDO, (1, "um")],
            [(1, "um"), None],
            [(1, "um"), REMOVIDO],
            [(1, "um"), (2, "dois")],
        ]

        for entradas in cenarios:
            with self.subTest(entradas=entradas):
                tabela = montar_tabela(entradas)
                esperados = [entrada for entrada in entradas if entrada is not None and entrada is not REMOVIDO]

                self.assertEqual(tabela.chaves(), [entrada[0] for entrada in esperados])
                self.assertEqual(tabela.valores(), [entrada[1] for entrada in esperados])
                self.assertEqual(tabela.itens(), esperados)
                self.assertIsInstance(str(tabela), str)


if __name__ == "__main__":
    unittest.main()
