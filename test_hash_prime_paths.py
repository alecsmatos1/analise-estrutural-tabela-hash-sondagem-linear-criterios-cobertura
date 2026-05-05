import os
import sys
import unittest
from itertools import product

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


def montar_tabela_por_padrao(padrao):
    capacidade = len(padrao)
    entradas = []

    for indice, simbolo in enumerate(padrao):
        if simbolo == "N":
            entradas.append(None)
        elif simbolo == "R":
            entradas.append(REMOVIDO)
        elif simbolo == "A":
            entradas.append((indice, f"valor-{indice}"))
        elif simbolo == "B":
            entradas.append((indice + capacidade, f"valor-{indice + capacidade}"))
        else:
            raise ValueError(f"Simbolo desconhecido: {simbolo}")

    return montar_tabela(entradas, capacidade=capacidade)


def clonar_entrada(entrada):
    if entrada is None or entrada is REMOVIDO:
        return entrada
    chave, valor = entrada
    return chave, valor


class TestHashPrimePaths(unittest.TestCase):
    def test_construtor_cobre_caminho_de_excecao(self):
        with self.assertRaises(ValueError):
            TabelaHashSondagemLinear(0)

    def test_funcao_hash_cobre_caminhos_primos_dos_lacos(self):
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

    def test_p13_wrap_around_da_sondagem_linear(self):
        tabela = montar_tabela([None, (1, "um"), (2, "dois")])

        self.assertEqual(tabela._procurar_posicao(2, para_insercao=False), 2)
        self.assertIsNone(tabela._procurar_posicao(5, para_insercao=False))

    def test_procurar_posicao_explora_combinacoes_estruturais_reais(self):
        for padrao in product("NRAB", repeat=4):
            tabela = montar_tabela_por_padrao(padrao)

            for chave in range(8):
                for para_insercao in (False, True):
                    with self.subTest(
                        padrao="".join(padrao),
                        chave=chave,
                        para_insercao=para_insercao,
                    ):
                        posicao = tabela._procurar_posicao(
                            chave,
                            para_insercao=para_insercao,
                        )

                        if posicao is not None:
                            self.assertGreaterEqual(posicao, 0)
                            self.assertLess(posicao, tabela.capacidade)

                            entrada = tabela.tabela[posicao]
                            if not para_insercao:
                                self.assertIsNotNone(entrada)
                                self.assertIsNot(entrada, REMOVIDO)
                                self.assertEqual(entrada[0], chave)

    def test_procurar_posicao_explora_chaves_deslocadas_por_colisao(self):
        entradas_possiveis = [
            None,
            REMOVIDO,
            (0, "zero"),
            (1, "um"),
            (2, "dois"),
            (3, "tres"),
        ]

        for entradas in product(entradas_possiveis, repeat=4):
            tabela = montar_tabela(
                [clonar_entrada(entrada) for entrada in entradas],
                capacidade=4,
            )

            for chave in range(4):
                for para_insercao in (False, True):
                    with self.subTest(
                        entradas=entradas,
                        chave=chave,
                        para_insercao=para_insercao,
                    ):
                        posicao = tabela._procurar_posicao(
                            chave,
                            para_insercao=para_insercao,
                        )

                        if posicao is not None:
                            self.assertGreaterEqual(posicao, 0)
                            self.assertLess(posicao, tabela.capacidade)

                            entrada = tabela.tabela[posicao]
                            if not para_insercao:
                                self.assertIsNotNone(entrada)
                                self.assertIsNot(entrada, REMOVIDO)
                                self.assertEqual(entrada[0], chave)

    def test_inserir_cobre_caminhos_primos_publicos(self):
        tabela = TabelaHashSondagemLinear(2)
        tabela.inserir(0, "zero")
        self.assertEqual(tabela.tabela[0], (0, "zero"))

        tabela.inserir(0, "ZERO")
        self.assertEqual(tabela.tabela[0], (0, "ZERO"))

        tabela.inserir(1, "um")
        with self.assertRaises(OverflowError):
            tabela.inserir(2, "dois")

        tabela_removida = montar_tabela([REMOVIDO, None])
        tabela_removida.inserir(0, "zero")
        self.assertEqual(tabela_removida.tabela[0], (0, "zero"))

    def test_buscar_remover_contem_e_len_cobrem_caminhos_publicos(self):
        tabela = TabelaHashSondagemLinear(3)
        tabela.inserir(0, "zero")

        self.assertEqual(tabela.buscar(0), "zero")
        self.assertTrue(tabela.contem(0))
        self.assertEqual(len(tabela), 1)

        with self.assertRaises(KeyError):
            tabela.buscar(1)

        tabela.remover(0)
        self.assertFalse(tabela.contem(0))
        self.assertEqual(len(tabela), 0)

        with self.assertRaises(KeyError):
            tabela.remover(1)

    def test_coletores_e_str_cobrem_caminhos_primos_de_laco(self):
        cenarios = [
            [],
            [None],
            [REMOVIDO],
            [(1, "um")],
            [None, None],
            [None, REMOVIDO],
            [None, (1, "um")],
            [REMOVIDO, None],
            [REMOVIDO, REMOVIDO],
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



