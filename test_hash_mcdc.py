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


class TestHashMCDC(unittest.TestCase):
    def test_d1_para_insercao_controla_reuso_quando_primeira_removida_ainda_nao_existe(self):
        tabela = montar_tabela([REMOVIDO, None, None])

        self.assertEqual(tabela._procurar_posicao(0, para_insercao=True), 0)
        self.assertIsNone(tabela._procurar_posicao(0, para_insercao=False))

    def test_d1_primeira_removida_nao_eh_sobrescrita_no_segundo_removido(self):
        tabela = montar_tabela([REMOVIDO, REMOVIDO, None])

        self.assertEqual(tabela._procurar_posicao(0, para_insercao=True), 0)

    def test_d2_saida_do_laco_retorna_primeira_removida_quando_ha_reuso_possivel(self):
        tabela = montar_tabela([REMOVIDO, (1, "um"), (2, "dois")])

        self.assertEqual(tabela._procurar_posicao(3, para_insercao=True), 0)

    def test_d2_saida_do_laco_retorna_none_quando_nao_ha_posicao_disponivel(self):
        tabela_insercao = montar_tabela([(0, "zero"), (1, "um"), (2, "dois")])
        tabela_busca = montar_tabela([(0, "zero"), (1, "um"), (2, "dois")])

        self.assertIsNone(tabela_insercao._procurar_posicao(3, para_insercao=True))
        self.assertIsNone(tabela_busca._procurar_posicao(3, para_insercao=False))

    def test_d3_inserir_distingue_none_removido_e_chave_existente(self):
        tabela_vazia = TabelaHashSondagemLinear(3)
        tabela_vazia.inserir(0, "zero")
        self.assertEqual(tabela_vazia.tabela[0], (0, "zero"))
        self.assertEqual(len(tabela_vazia), 1)

        tabela_existente = TabelaHashSondagemLinear(3)
        tabela_existente.inserir(0, "zero")
        tabela_existente.inserir(0, "ZERO")
        self.assertEqual(tabela_existente.tabela[0], (0, "ZERO"))
        self.assertEqual(len(tabela_existente), 1)

        tabela_removida = montar_tabela([REMOVIDO, None, None])
        tabela_removida.inserir(0, "zero")
        self.assertEqual(tabela_removida.tabela[0], (0, "zero"))
        self.assertEqual(len(tabela_removida), 1)

    def test_d4_d5_d6_iteradores_ignoram_none_e_removido(self):
        tabela = montar_tabela([None, REMOVIDO, (2, "dois")])

        self.assertEqual(tabela.chaves(), [2])
        self.assertEqual(tabela.valores(), ["dois"])
        self.assertEqual(tabela.itens(), [(2, "dois")])


if __name__ == "__main__":
    unittest.main()
