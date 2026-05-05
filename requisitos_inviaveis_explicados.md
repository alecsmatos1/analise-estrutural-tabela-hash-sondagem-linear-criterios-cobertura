# Requisitos inviaveis explicados

Este documento explica os requisitos marcados como inviaveis na medicao final
do `cfgcoverage`.

A decisao adotada foi manter apenas execucao real nos testes e excluir da
medicao os requisitos que a propria modelagem do CFG torna impossiveis de
executar em Python. Nenhum requisito abaixo foi coberto por chamada artificial
a `__cov_node__`.

Resultado final apos aplicar os inviaveis:

```text
Total: Block: 100 Edge: 100 Essential edge: 100 Edge-pair: 100 Prime Path: 100
```

## Padrao 1: ultima iteracao de `for`

Nos lacos `for`, o CFG do `cfgcoverage` cria tres tipos de nos:

- `FOR_ITER`: no que representa a tentativa de obter o proximo item.
- `FOR_BODY`: no do corpo do laco.
- `FOR_AFTER`: no executado depois que o laco termina.

O requisito inviavel tem sempre a forma:

```text
corpo ou condicao do for -> FOR_ITER -> FOR_AFTER
```

Na execucao instrumentada observada, quando o item atual e o ultimo item do
iteravel, o trace vai direto do corpo/condicao para `FOR_AFTER`. Quando ainda
existe proximo item, o trace passa pelo `FOR_ITER`, mas segue para o corpo da
proxima iteracao, nao para `FOR_AFTER`.

Portanto, estes caminhos exigem uma transicao intermediaria que o
instrumentador nao registra como trace executavel.

### `funcao_hash` -- 2

#### `(13, 12, 14)`

- Tipo: edge-pair.
- Trecho: ramo `str`, no laco `for caractere in chave`.
- Significado esperado pelo CFG: `soma += ord(caractere)` volta ao
  `FOR_ITER` e sai imediatamente para o `return`.
- Por que e inviavel: na ultima iteracao real, o trace registrado faz
  `13 -> 14`. Em iteracoes intermediarias, o trace faz `13 -> 12 -> 13`.
  O trace `13 -> 12 -> 14` nao aparece.

#### `(18, 17, 19)`

- Tipo: edge-pair.
- Trecho: ramo generico, no laco `for caractere in str(chave)`.
- Significado esperado pelo CFG: `soma += ord(caractere)` volta ao
  `FOR_ITER` e sai imediatamente para o `return`.
- Por que e inviavel: na ultima iteracao real, o trace registrado faz
  `18 -> 19`. Em iteracoes intermediarias, o trace faz `18 -> 17 -> 18`.
  O trace `18 -> 17 -> 19` nao aparece.

### `chaves` -- 8

#### `(5, 2, 4)`

- Tipo: edge-pair.
- Trecho: ultimo item valido executa `resultado.append(entrada[0])`.
- Por que e inviavel: quando o item valido e o ultimo, o trace registrado faz
  `5 -> 4`. Quando nao e o ultimo, faz `5 -> 2 -> 3`. O caminho
  `5 -> 2 -> 4` nao ocorre.

#### `(8, 2, 4)`

- Tipo: edge-pair.
- Trecho: ultimo item `REMOVIDO` avalia `entrada is not REMOVIDO`.
- Por que e inviavel: quando `REMOVIDO` e o ultimo item, o trace registrado
  faz `8 -> 4`. Quando ha proximo item, faz `8 -> 2 -> 3`. O caminho
  `8 -> 2 -> 4` nao ocorre.

#### `(9, 2, 4)`

- Tipo: edge-pair.
- Trecho: ultimo item `None` avalia `entrada is not None`.
- Por que e inviavel: quando `None` e o ultimo item, o trace registrado faz
  `9 -> 4`. Quando ha proximo item, faz `9 -> 2 -> 3`. O caminho
  `9 -> 2 -> 4` nao ocorre.

Prime paths tambem justificados pelo mesmo motivo:

```text
(9, 2, 4)
(9, 8, 2, 4)
(9, 8, 5, 2, 4)
```

Todos exigem a saida `2 -> 4` imediatamente depois de uma volta pelo iterador
na ultima iteracao do `for`.

### `valores` -- 9

#### `(5, 2, 4)`

- Tipo: edge-pair.
- Trecho: ultimo item valido executa `resultado.append(entrada[1])`.
- Por que e inviavel: quando o item valido e o ultimo, o trace registrado faz
  `5 -> 4`. Quando nao e o ultimo, faz `5 -> 2 -> 3`. O caminho
  `5 -> 2 -> 4` nao ocorre.

#### `(8, 2, 4)`

- Tipo: edge-pair.
- Trecho: ultimo item `REMOVIDO` avalia `entrada is not REMOVIDO`.
- Por que e inviavel: quando `REMOVIDO` e o ultimo item, o trace registrado
  faz `8 -> 4`. Quando ha proximo item, faz `8 -> 2 -> 3`. O caminho
  `8 -> 2 -> 4` nao ocorre.

#### `(9, 2, 4)`

- Tipo: edge-pair.
- Trecho: ultimo item `None` avalia `entrada is not None`.
- Por que e inviavel: quando `None` e o ultimo item, o trace registrado faz
  `9 -> 4`. Quando ha proximo item, faz `9 -> 2 -> 3`. O caminho
  `9 -> 2 -> 4` nao ocorre.

Prime paths tambem justificados pelo mesmo motivo:

```text
(9, 2, 4)
(9, 8, 2, 4)
(9, 8, 5, 2, 4)
```

### `itens` -- 10

#### `(5, 2, 4)`

- Tipo: edge-pair.
- Trecho: ultimo item valido executa `resultado.append(entrada)`.
- Por que e inviavel: quando o item valido e o ultimo, o trace registrado faz
  `5 -> 4`. Quando nao e o ultimo, faz `5 -> 2 -> 3`. O caminho
  `5 -> 2 -> 4` nao ocorre.

#### `(8, 2, 4)`

- Tipo: edge-pair.
- Trecho: ultimo item `REMOVIDO` avalia `entrada is not REMOVIDO`.
- Por que e inviavel: quando `REMOVIDO` e o ultimo item, o trace registrado
  faz `8 -> 4`. Quando ha proximo item, faz `8 -> 2 -> 3`. O caminho
  `8 -> 2 -> 4` nao ocorre.

#### `(9, 2, 4)`

- Tipo: edge-pair.
- Trecho: ultimo item `None` avalia `entrada is not None`.
- Por que e inviavel: quando `None` e o ultimo item, o trace registrado faz
  `9 -> 4`. Quando ha proximo item, faz `9 -> 2 -> 3`. O caminho
  `9 -> 2 -> 4` nao ocorre.

Prime paths tambem justificados pelo mesmo motivo:

```text
(9, 2, 4)
(9, 8, 2, 4)
(9, 8, 5, 2, 4)
```

### `__str__` -- 12

#### `(5, 2, 4)`

- Tipo: edge-pair.
- Trecho: ultimo item `None` adiciona a linha `VAZIO`.
- Por que e inviavel: quando `None` e o ultimo item, o trace registrado faz
  `5 -> 4`. Quando ha proximo item, faz `5 -> 2 -> 3`. O caminho
  `5 -> 2 -> 4` nao ocorre.

#### `(9, 2, 4)`

- Tipo: edge-pair.
- Trecho: ultimo item `REMOVIDO` adiciona a linha `REMOVIDO`.
- Por que e inviavel: quando `REMOVIDO` e o ultimo item, o trace registrado
  faz `9 -> 4`. Quando ha proximo item, faz `9 -> 2 -> 3`. O caminho
  `9 -> 2 -> 4` nao ocorre.

#### `(10, 2, 4)`

- Tipo: edge-pair.
- Trecho: ultimo item par `(chave, valor)` adiciona a linha `chave -> valor`.
- Por que e inviavel: quando o par e o ultimo item, o trace registrado faz
  `10 -> 4`. Quando ha proximo item, faz `10 -> 2 -> 3`. O caminho
  `10 -> 2 -> 4` nao ocorre.

Prime paths tambem justificados pelo mesmo motivo:

```text
(8, 5, 2, 4)
(8, 6, 12, 10, 2, 4)
(8, 6, 12, 9, 2, 4)
```

Todos terminam exigindo uma volta ao `FOR_ITER` seguida de saida imediata para
`FOR_AFTER`, padrao que nao aparece como trace executavel.

## Padrao 2: estado impossivel de `primeira_removida`

No metodo `_procurar_posicao`, a variavel `primeira_removida` segue uma regra
simples:

```text
primeira_removida = None
```

Depois disso, ela pode receber uma posicao removida, mas nunca volta para
`None`. Portanto, qualquer caminho que exija `primeira_removida` preenchida
antes da primeira iteracao, ou que exija reset para `None`, contradiz o codigo.

### `_procurar_posicao` -- 3

#### `(0, 1, 5, 2, 6, 10, 7, 14, 11, 18, 15)`

- Tipo: prime path.
- Por que e inviavel: na primeira iteracao, o caminho entra no ramo
  `entrada is None`, `para_insercao=True` e tenta retornar
  `primeira_removida`. Isso exigiria `primeira_removida is not None` logo na
  primeira iteracao, mas ela acabou de ser inicializada como `None`.

#### `(0, 1, 5, 2, 6, 10, 8, 25, 22, 30, 29, 9)`

- Tipo: prime path.
- Por que e inviavel: na primeira iteracao, o caminho trata uma entrada
  `REMOVIDO` como se `primeira_removida is None` fosse falso e segue sem
  registrar a primeira removida. Como `primeira_removida` inicia em `None`,
  esse estado nao existe na primeira remocao observada.

#### `(26, 9, 1, 5, 2, 6, 10, 8, 25, 22, 30, 29, 26)`

- Tipo: prime path.
- Por que e inviavel: o caminho passa por `26`, onde `primeira_removida`
  recebe uma posicao. Depois exige novamente o ramo `29 -> 26`, isto e,
  `primeira_removida is None`. Como a variavel nunca volta a `None`, esse
  ciclo nao pode ocorrer.

## Padrao 3: saida do `while` sem iterar

O laco principal de `_procurar_posicao` e:

```text
while passos < self.capacidade:
```

O metodo inicializa `passos = 0`. Assim, o `while` so nao executa se
`self.capacidade <= 0`. Pelo construtor publico, capacidade nao positiva e
rejeitada com `ValueError`.

### `_procurar_posicao` -- 3

#### `(0, 1, 5, 4, 41, 39)`

- Tipo: prime path.
- Por que e inviavel: exige sair do `while` antes de qualquer iteracao e
  retornar `None`. Isso so acontece se `capacidade <= 0`, estado rejeitado
  pelo construtor.

#### `(0, 1, 5, 4, 41, 40, 37)`

- Tipo: prime path.
- Por que e inviavel: exige sair do `while` sem iterar e ainda retornar
  `primeira_removida`. Alem de depender de `capacidade <= 0`, exigiria uma
  `primeira_removida` preenchida sem nenhuma iteracao capaz de atribui-la.

#### `(0, 1, 5, 4, 41, 40, 39)`

- Tipo: prime path.
- Por que e inviavel: exige sair do `while` sem iterar e avaliar
  `primeira_removida is not None` como falso. A saida sem iteracao depende de
  `capacidade <= 0`, estado invalido para a classe construida publicamente.

## Padrao 4: combinacoes longas dos mesmos estados impossiveis

Os caminhos abaixo combinam os mesmos problemas ja descritos: saida do `while`
em um estado contraditorio, retorno antecipado apos um estado impossivel de
`primeira_removida`, ou sequencias que dependem do reset impossivel de
`primeira_removida`.

### `_procurar_posicao` -- 3

#### `(6, 10, 8, 25, 22, 30, 29, 26, 9, 1, 5, 4, 41, 39)`

- Tipo: prime path.
- Por que e inviavel: registra `primeira_removida` em `26`, sai do laco e
  depois segue para retorno `None` em `39`, ignorando uma removida ja
  registrada. Esse estado contradiz a condicao final de insercao.

#### `(6, 10, 8, 25, 22, 30, 29, 26, 9, 1, 5, 4, 41, 40, 39)`

- Tipo: prime path.
- Por que e inviavel: registra `primeira_removida`, sai do laco, avalia
  `primeira_removida is not None` e ainda assim retorna `None`. Isso contradiz
  o fluxo final, que retorna a posicao removida quando ela existe.

#### `(6, 10, 8, 25, 22, 30, 29, 9, 1, 5, 4, 41, 39)`

- Tipo: prime path.
- Por que e inviavel: passa por uma entrada `REMOVIDO` sem registrar a primeira
  removida e depois sai retornando `None`. Para isso, `primeira_removida`
  precisaria ja estar preenchida antes dessa remocao, mas o caminho nao contem
  atribuicao anterior compatavel.

#### `(6, 10, 8, 25, 22, 30, 29, 9, 1, 5, 4, 41, 40, 39)`

- Tipo: prime path.
- Por que e inviavel: combina uma passagem por `REMOVIDO` sem nova atribuicao
  com saida final que avalia e descarta `primeira_removida`. O estado exigido
  nao e produzido pelo metodo.

#### `(6, 10, 8, 25, 22, 30, 9, 1, 5, 4, 41, 40, 37)`

- Tipo: prime path.
- Por que e inviavel: tenta sair do laco e retornar `primeira_removida` sem
  passar pelo no `26`, que e o unico ponto que atribui essa variavel.

#### `(6, 10, 8, 25, 22, 30, 9, 1, 5, 4, 41, 40, 39)`

- Tipo: prime path.
- Por que e inviavel: sai do laco apos uma entrada `REMOVIDO` sem registrar
  `primeira_removida`, e depois retorna `None`. E uma combinacao de saida de
  ciclo com estado que nao corresponde ao fluxo real.

#### `(8, 25, 22, 30, 29, 26, 9, 1, 5, 2, 6, 10, 7, 14, 11, 18, 17)`

- Tipo: prime path.
- Por que e inviavel: registra `primeira_removida` em uma iteracao anterior e
  depois encontra `None` em modo de insercao, mas segue para retorno de
  `posicao` (`17`) em vez de retornar a primeira removida (`15`).

#### `(8, 25, 22, 30, 29, 26, 9, 1, 5, 2, 6, 10, 7, 14, 12)`

- Tipo: prime path.
- Por que e inviavel: registra `primeira_removida` e depois encontra `None`,
  mas segue para o ramo de busca (`para_insercao=False`). Esse caminho mistura
  estado criado em insercao com decisao final de busca.

#### `(8, 25, 22, 30, 29, 9, 1, 5, 2, 6, 10, 7, 14, 11, 18, 17)`

- Tipo: prime path.
- Por que e inviavel: exige que uma entrada `REMOVIDO` anterior nao registre
  `primeira_removida` e, ao encontrar `None`, retorne `posicao`. O fluxo real
  sem primeira removida nao produz esse historico.

#### `(8, 25, 22, 30, 29, 9, 1, 5, 2, 6, 10, 7, 14, 12)`

- Tipo: prime path.
- Por que e inviavel: combina passagem por `REMOVIDO` sem atribuicao
  compatavel com encontro posterior de `None` em busca comum. O estado
  intermediario exigido nao e alcancavel a partir da inicializacao do metodo.

#### `(8, 25, 22, 30, 9, 1, 5, 2, 6, 10, 7, 14, 11, 18, 15)`

- Tipo: prime path.
- Por que e inviavel: encontra `None` e tenta retornar `primeira_removida`,
  mas o caminho nao contem atribuicao anterior em `26`. Isso exigiria
  `primeira_removida` preenchida sem ter sido registrada.

#### `(8, 25, 22, 30, 9, 1, 5, 2, 6, 10, 7, 14, 11, 18, 17)`

- Tipo: prime path.
- Por que e inviavel: encontra `None` em modo de insercao e retorna `posicao`
  depois de uma passagem por `REMOVIDO` que nao produziu estado consistente.

## Padrao 5: no `EXIT` artificial

### `inserir` -- 4

#### `(10,)`

- Tipo: prime path.
- Trecho: no triangular `EXIT` do CFG.
- Por que e inviavel: o no `10` nao corresponde a uma instrucao Python
  executada diretamente. Ele recebe apenas arestas `FAKE` vindas dos blocos de
  fim de `inserir`. Como nao ha chamada instrumentada real para esse no, o
  prime path unitario `(10,)` nao pode aparecer no trace de execucao.
