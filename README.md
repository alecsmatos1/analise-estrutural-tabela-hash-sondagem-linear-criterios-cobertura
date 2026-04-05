# Analise Estrutural de Tabela Hash com Sondagem Linear

Este repositorio contem a implementacao `tabelaHash.py` e uma suite de testes estruturais para uma tabela hash com sondagem linear, desenvolvida no contexto da disciplina `SSC5877 - Verificacao, Validacao e Teste de Software`.

O recorte deste repositorio foi reduzido ao que e necessario para executar o codigo e os testes. Dependencias instalaveis, artefatos gerados e relatorios auxiliares ficaram de fora do versionamento.

## Conteudo versionado

- `tabelaHash.py`: implementacao principal
- `test_hash_desvios.py`: testes para cobertura de arestas
- `test_hash_mcdc.py`: testes para o criterio MC/DC
- `test_hash_edge_pair.py`: testes para o criterio edge-pair
- `test_hash_prime_paths.py`: testes para o criterio prime paths

## Requisitos

- Python 3.10 ou superior

Nao ha dependencias obrigatorias de terceiros para executar os testes principais, porque a suite usa `unittest`, que faz parte da biblioteca padrao do Python.

## Como executar os testes

Executar todos os testes:

```bash
python -m unittest discover
```

Executar um arquivo especifico:

```bash
python -m unittest test_hash_desvios.py
python -m unittest test_hash_mcdc.py
python -m unittest test_hash_edge_pair.py
python -m unittest test_hash_prime_paths.py
```

## Ferramentas opcionais

Se voce quiser usar ferramentas externas para medicao, geracao de relatorios ou uma experiencia diferente de execucao, instale-as localmente em vez de subi-las ao repositório.

Exemplo com ambiente virtual:

```bash
python -m venv .venv
```

Ativacao no Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Instalacao de ferramentas opcionais:

```bash
python -m pip install pytest cfgcoverage pymcdc python-docx
```

Com `pytest`, por exemplo:

```bash
python -m pytest
```

## Observacoes

- A funcao hash foi mantida simples e previsivel para fins didaticos.
- Arquivos como PDFs, DOCX, HTML gerado, dependencias vendorizadas e scripts auxiliares de medicao nao fazem parte do commit principal.
