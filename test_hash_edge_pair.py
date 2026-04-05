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


class TestHashEdgePair(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
