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


class TestHashPrimePaths(unittest.TestCase):
    def test_p1_busca_interrompida_por_none(self):
        tabela = TabelaHashSondagemLinear(3)

        self.assertIsNone(tabela._procurar_posicao(0, para_insercao=False))

    def test_p2_insercao_retorna_posicao_livre_sem_removido_previo(self):
        tabela = TabelaHashSondagemLinear(3)

        self.assertEqual(tabela._procurar_posicao(0, para_insercao=True), 0)

    def test_p3_insercao_retorna_primeira_removida_quando_ha_none_mais_adiante(self):
        tabela = montar_tabela([REMOVIDO, None, None])

        self.assertEqual(tabela._procurar_posicao(0, para_insercao=True), 0)

    def test_p6_encontra_chave_apos_colisao(self):
        tabela = montar_tabela([(3, "tres"), (0, "zero"), None])

        self.assertEqual(tabela._procurar_posicao(0, para_insercao=False), 1)

    def test_p7_colisao_segue_ate_none_quando_chave_nao_existe(self):
        tabela = montar_tabela([(3, "tres"), None, None])

        self.assertIsNone(tabela._procurar_posicao(0, para_insercao=False))

    def test_p8_ciclo_registra_primeira_remocao_e_varre_o_restante(self):
        tabela = montar_tabela([REMOVIDO, (3, "tres"), (6, "seis")])

        self.assertEqual(tabela._procurar_posicao(0, para_insercao=True), 0)

    def test_p9_ciclo_com_remocao_ja_registrada(self):
        tabela = montar_tabela([REMOVIDO, REMOVIDO, (6, "seis")])

        self.assertEqual(tabela._procurar_posicao(0, para_insercao=True), 0)

    def test_p11_saida_do_laco_reutiliza_removido_sem_posicao_none(self):
        tabela = montar_tabela([REMOVIDO, (1, "um"), (2, "dois")])

        self.assertEqual(tabela._procurar_posicao(3, para_insercao=True), 0)

    def test_p12_saida_do_laco_retorna_none_sem_posicao_disponivel(self):
        tabela = montar_tabela([(0, "zero"), (1, "um"), (2, "dois")])

        self.assertIsNone(tabela._procurar_posicao(3, para_insercao=True))


if __name__ == "__main__":
    unittest.main()



