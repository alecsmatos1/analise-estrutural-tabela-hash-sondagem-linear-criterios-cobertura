class MarcadorRemovido:
    """
    Objeto especial usado para marcar posições removidas logicamente.
    Não usamos None, porque None significa "posição que nunca foi ocupada".
    """
    pass


REMOVIDO = MarcadorRemovido()


class TabelaHashSondagemLinear:
    def __init__(self, capacidade=11):
        """
        Cria uma tabela hash vazia com a capacidade indicada.
        """
        if capacidade <= 0:
            raise ValueError("A capacidade deve ser maior que zero.")

        self.capacidade = capacidade
        self.tabela = [None] * capacidade
        self.quantidade = 0

    def funcao_hash(self, chave):
        """
        Função de hash manual e previsível.

        Ideia:
        - se a chave for string, somamos os códigos ASCII dos caracteres;
        - se a chave for inteiro, usamos o próprio valor;
        - caso contrário, convertemos para string e somamos os caracteres.

        Isso NÃO é ideal para uso real, mas é ótimo para ensino,
        porque permite prever facilmente onde cada chave será mapeada.
        """
        if isinstance(chave, int):
            return chave % self.capacidade

        if isinstance(chave, str):
            soma = 0
            for caractere in chave:
                soma += ord(caractere)
            return soma % self.capacidade

        soma = 0
        for caractere in str(chave):
            soma += ord(caractere)
        return soma % self.capacidade

    def _procurar_posicao(self, chave, para_insercao=False):
        """
        Procura a posição de uma chave na tabela.

        Se para_insercao=False:
            - retorna o índice da chave, se ela existir;
            - retorna None, se ela não existir.

        Se para_insercao=True:
            - retorna o índice da própria chave, se ela já existir;
            - retorna a melhor posição livre para inserir;
            - retorna None, se não houver posição disponível.

        A sondagem é linear:
            pos, pos+1, pos+2, ... (com retorno ao início da tabela)
        """
        posicao_inicial = self.funcao_hash(chave)
        posicao = posicao_inicial
        primeira_removida = None
        passos = 0

        # Percorremos no máximo "capacidade" posições,
        # para não entrar em laço infinito.
        while passos < self.capacidade:
            entrada = self.tabela[posicao]

            # Caso 1: posição nunca usada
            if entrada is None:
                if para_insercao:
                    # Se já encontramos uma posição REMOVIDA antes,
                    # é melhor reutilizá-la.
                    if primeira_removida is not None:
                        return primeira_removida
                    return posicao
                else:
                    # Em busca comum, encontrar None significa
                    # que a chave não está na tabela.
                    return None

            # Caso 2: posição removida logicamente
            elif entrada is REMOVIDO:
                if para_insercao and primeira_removida is None:
                    primeira_removida = posicao

            # Caso 3: posição ocupada por um par (chave, valor)
            else:
                chave_guardada, _ = entrada
                if chave_guardada == chave:
                    return posicao

            # Próxima posição (sondagem linear com aritmética modular)
            posicao = (posicao + 1) % self.capacidade
            passos += 1

        # Se percorremos a tabela toda:
        # para inserção, ainda podemos reutilizar uma posição removida.
        if para_insercao and primeira_removida is not None:
            return primeira_removida

        return None

    def inserir(self, chave, valor):
        """
        Insere um novo par (chave, valor) na tabela.

        Se a chave já existir, apenas atualiza o valor.
        """
        posicao = self._procurar_posicao(chave, para_insercao=True)

        if posicao is None:
            raise OverflowError("Tabela hash cheia.")

        entrada_atual = self.tabela[posicao]

        # Decisão composta interessante para aula:
        # ou a posição é vazia, ou ela está marcada como removida.
        if entrada_atual is None or entrada_atual is REMOVIDO:
            self.tabela[posicao] = (chave, valor)
            self.quantidade += 1
        else:
            # A chave já existe: atualiza somente o valor
            self.tabela[posicao] = (chave, valor)

    def buscar(self, chave):
        """
        Retorna o valor associado à chave.

        Lança KeyError se a chave não existir.
        """
        posicao = self._procurar_posicao(chave, para_insercao=False)

        if posicao is None:
            raise KeyError(f"Chave não encontrada: {chave}")

        return self.tabela[posicao][1]

    def remover(self, chave):
        """
        Remove logicamente uma chave da tabela.

        A remoção é "lógica" porque colocamos um marcador especial
        em vez de simplesmente usar None.
        """
        posicao = self._procurar_posicao(chave, para_insercao=False)

        if posicao is None:
            raise KeyError(f"Chave não encontrada: {chave}")

        self.tabela[posicao] = REMOVIDO
        self.quantidade -= 1

    def contem(self, chave):
        """
        Devolve True se a chave estiver na tabela e False caso contrário.
        """
        return self._procurar_posicao(chave, para_insercao=False) is not None

    def chaves(self):
        """
        Devolve uma lista com todas as chaves presentes na tabela.
        """
        resultado = []

        for entrada in self.tabela:
            if entrada is not None and entrada is not REMOVIDO:
                resultado.append(entrada[0])

        return resultado

    def valores(self):
        """
        Devolve uma lista com todos os valores presentes na tabela.
        """
        resultado = []

        for entrada in self.tabela:
            if entrada is not None and entrada is not REMOVIDO:
                resultado.append(entrada[1])

        return resultado

    def itens(self):
        """
        Devolve uma lista de pares (chave, valor) presentes na tabela.
        """
        resultado = []

        for entrada in self.tabela:
            if entrada is not None and entrada is not REMOVIDO:
                resultado.append(entrada)

        return resultado

    def __len__(self):
        return self.quantidade

    def __str__(self):
        """
        Gera uma representação textual da tabela,
        útil para depuração e demonstração em aula.
        """
        linhas = []

        for i, entrada in enumerate(self.tabela):
            if entrada is None:
                linhas.append(f"{i}: VAZIO")
            elif entrada is REMOVIDO:
                linhas.append(f"{i}: REMOVIDO")
            else:
                chave, valor = entrada
                linhas.append(f"{i}: {chave} -> {valor}")

        return "\n".join(linhas)


if __name__ == "__main__":
    tabela = TabelaHashSondagemLinear(7)

    print("Tabela inicialmente vazia:")
    print(tabela)
    print("-" * 40)

    # Inserções
    tabela.inserir("ana", 10)
    tabela.inserir("bia", 20)
    tabela.inserir("carlos", 30)

    print("Após inserir ana, bia e carlos:")
    print(tabela)
    print("-" * 40)

    # Busca
    print("Valor associado à chave 'bia':", tabela.buscar("bia"))
    print("A tabela contém 'ana'?", tabela.contem("ana"))
    print("A tabela contém 'joao'?", tabela.contem("joao"))
    print("-" * 40)

    # Atualização de chave existente
    tabela.inserir("bia", 99)
    print("Após atualizar o valor da chave 'bia':")
    print(tabela)
    print("-" * 40)

    # Remoção lógica
    tabela.remover("ana")
    print("Após remover 'ana':")
    print(tabela)
    print("-" * 40)

    # Reutilização de posição removida
    tabela.inserir("davi", 40)
    print("Após inserir 'davi':")
    print(tabela)
    print("-" * 40)

    print("Chaves:", tabela.chaves())
    print("Valores:", tabela.valores())
    print("Itens:", tabela.itens())
    print("Quantidade de elementos:", len(tabela))
