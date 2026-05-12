import os
import sys
import unittest
from itertools import product

sys.path.insert(0, os.path.dirname(__file__))

import tabelaHash as modulo_tabela_hash
from tabelaHash import REMOVIDO, TabelaHashSondagemLinear
from test_hash_prime_paths import TestHashPrimePaths as BasePrimePaths


def montar_tabela(entradas, capacidade=None):
    tabela = TabelaHashSondagemLinear.__new__(TabelaHashSondagemLinear)
    tabela.capacidade = capacidade if capacidade is not None else len(entradas)
    tabela.tabela = list(entradas)
    tabela.quantidade = sum(
        1 for entrada in entradas if entrada is not None and entrada is not REMOVIDO
    )
    return tabela


def hash_esperado(chave, capacidade):
    if isinstance(chave, int):
        return chave % capacidade

    if isinstance(chave, str):
        return sum(ord(caractere) for caractere in chave) % capacidade

    return sum(ord(caractere) for caractere in str(chave)) % capacidade


def procurar_esperado(entradas, capacidade, chave, para_insercao=False):
    posicao = hash_esperado(chave, capacidade)
    primeira_removida = None
    passos = 0

    while passos < capacidade:
        entrada = entradas[posicao]

        if entrada is None:
            if para_insercao:
                if primeira_removida is not None:
                    return primeira_removida
                return posicao
            return None

        if entrada is REMOVIDO:
            if para_insercao and primeira_removida is None:
                primeira_removida = posicao
        else:
            chave_guardada, _ = entrada
            if chave_guardada == chave:
                return posicao

        posicao = (posicao + 1) % capacidade
        passos += 1

    if para_insercao and primeira_removida is not None:
        return primeira_removida

    return None


def entradas_por_padrao(padrao):
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
            chave = indice + capacidade
            entradas.append((chave, f"valor-{chave}"))
        else:
            raise ValueError(f"Simbolo desconhecido: {simbolo}")

    return entradas


class ObjetoComStr:
    def __init__(self, texto):
        self.texto = texto

    def __str__(self):
        return self.texto


class TestHashMutacao(BasePrimePaths):
    def test_construtor_estado_inicial_e_mensagem_de_erro(self):
        tabela_padrao = TabelaHashSondagemLinear()
        self.assertEqual(tabela_padrao.capacidade, 11)
        self.assertEqual(tabela_padrao.tabela, [None] * 11)
        self.assertEqual(tabela_padrao.quantidade, 0)

        tabela = TabelaHashSondagemLinear(4)

        self.assertEqual(tabela.capacidade, 4)
        self.assertEqual(tabela.tabela, [None, None, None, None])
        self.assertEqual(tabela.quantidade, 0)

        for capacidade in (0, -1):
            with self.subTest(capacidade=capacidade):
                with self.assertRaisesRegex(
                    ValueError,
                    "^A capacidade deve ser maior que zero\\.$",
                ):
                    TabelaHashSondagemLinear(capacidade)

    def test_funcao_hash_caracterizacao_exata(self):
        chaves = [
            -8,
            -1,
            0,
            1,
            8,
            "",
            "a",
            "ab",
            "ana",
            ObjetoComStr(""),
            ObjetoComStr("xy"),
            (1, 2),
        ]

        for capacidade in (1, 2, 5, 7):
            tabela = TabelaHashSondagemLinear(capacidade)
            for chave in chaves:
                with self.subTest(capacidade=capacidade, chave=repr(chave)):
                    self.assertEqual(
                        tabela.funcao_hash(chave),
                        hash_esperado(chave, capacidade),
                    )

    def test_procurar_posicao_bate_com_oraculo_independente(self):
        tabela_vazia = TabelaHashSondagemLinear(3)
        self.assertIsNone(tabela_vazia._procurar_posicao(0))

        tabela_invalida = montar_tabela([None, (2, "dois")], capacidade=2)
        self.assertIsNone(tabela_invalida._procurar_posicao(2, False))

        for padrao in product("NRAB", repeat=4):
            entradas = entradas_por_padrao(padrao)
            tabela = montar_tabela(entradas, capacidade=4)

            for chave in range(8):
                for para_insercao in (False, True):
                    with self.subTest(
                        padrao="".join(padrao),
                        chave=chave,
                        para_insercao=para_insercao,
                    ):
                        self.assertEqual(
                            tabela._procurar_posicao(chave, para_insercao),
                            procurar_esperado(
                                entradas,
                                4,
                                chave,
                                para_insercao,
                            ),
                        )

    def test_operacoes_publicas_preservam_estado_exato(self):
        tabela = TabelaHashSondagemLinear(5)

        tabela.inserir(0, "zero")
        tabela.inserir(5, "cinco")
        tabela.inserir(10, "dez")
        self.assertEqual(
            tabela.tabela,
            [(0, "zero"), (5, "cinco"), (10, "dez"), None, None],
        )
        self.assertEqual(len(tabela), 3)

        tabela.inserir(5, "CINCO")
        self.assertEqual(
            tabela.tabela,
            [(0, "zero"), (5, "CINCO"), (10, "dez"), None, None],
        )
        self.assertEqual(len(tabela), 3)
        self.assertEqual(tabela.buscar(5), "CINCO")

        tabela.remover(5)
        self.assertIs(tabela.tabela[1], REMOVIDO)
        self.assertEqual(len(tabela), 2)
        self.assertFalse(tabela.contem(5))

        tabela.inserir(15, "quinze")
        self.assertEqual(
            tabela.tabela,
            [(0, "zero"), (15, "quinze"), (10, "dez"), None, None],
        )
        self.assertEqual(len(tabela), 3)
        self.assertEqual(tabela.chaves(), [0, 15, 10])
        self.assertEqual(tabela.valores(), ["zero", "quinze", "dez"])
        self.assertEqual(
            tabela.itens(),
            [(0, "zero"), (15, "quinze"), (10, "dez")],
        )

    def test_mensagens_de_busca_remocao_e_overflow_sao_observaveis(self):
        tabela = TabelaHashSondagemLinear(1)
        tabela.inserir("a", 10)

        with self.assertRaisesRegex(OverflowError, "^Tabela hash cheia\\.$"):
            tabela.inserir("b", 20)

        for operacao in (tabela.buscar, tabela.remover):
            with self.subTest(operacao=operacao.__name__):
                with self.assertRaisesRegex(
                    KeyError,
                    "^'Chave n\u00e3o encontrada: b'$",
                ):
                    operacao("b")

    def test_coletores_e_str_sao_exatos_para_estados_compostos(self):
        cenarios = [
            [],
            [None],
            [REMOVIDO],
            [(1, "um")],
            [None, REMOVIDO, (2, "dois"), (3, "tres")],
            [(0, "zero"), REMOVIDO, None, (3, "tres")],
        ]

        for entradas in cenarios:
            with self.subTest(entradas=entradas):
                tabela = montar_tabela(entradas)
                validas = [
                    entrada
                    for entrada in entradas
                    if entrada is not None and entrada is not REMOVIDO
                ]

                self.assertEqual(tabela.chaves(), [entrada[0] for entrada in validas])
                self.assertEqual(tabela.valores(), [entrada[1] for entrada in validas])
                self.assertEqual(tabela.itens(), validas)

                linhas = []
                for indice, entrada in enumerate(entradas):
                    if entrada is None:
                        linhas.append(f"{indice}: VAZIO")
                    elif entrada is REMOVIDO:
                        linhas.append(f"{indice}: REMOVIDO")
                    else:
                        chave, valor = entrada
                        linhas.append(f"{indice}: {chave} -> {valor}")
                self.assertEqual(str(tabela), "\n".join(linhas))

    def test_importacao_nao_executa_bloco_de_demonstracao(self):
        self.assertFalse(hasattr(modulo_tabela_hash, "tabela"))


    def test_inserir_aceita_valor_zero(self):
        tabela = TabelaHashSondagemLinear(3)
        tabela.inserir("zero", 0)
        self.assertEqual(tabela.buscar("zero"), 0)
        
    
del BasePrimePaths


if __name__ == "__main__":
    unittest.main()
