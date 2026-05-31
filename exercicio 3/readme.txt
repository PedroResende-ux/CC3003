Exercício 3 - Vigilância de Partições Retangulares

Este diretório reúne as implementações usadas no Exercício 3:

- [csp_vigilancia.py](csp_vigilancia.py): estrutura de dados e propagação AC-3 para o modelo CSP.
- [backtrack_otimizado.py](backtrack_otimizado.py): pesquisa branch-and-bound com propagação.
- [resolver_ortools.py](resolver_ortools.py): formulação MIP com OR-Tools / SCIP.
- [solve_exact_cover_fast.py](solve_exact_cover_fast.py): benchmark comparativo dos métodos exatos em Python.
- [csp_vigilancia_setup.py](csp_vigilancia_setup.py): exemplo de utilização da classe e do parser.
- [swi_prolog_benchmark.pl](swi_prolog_benchmark.pl): benchmark equivalente em SWI-Prolog com CLPFD.
- [parser.py](../parser.py): parser partilhado na raiz do repositório.

Requisitos

- Python 3.10 ou superior.
- SWI-Prolog para executar o benchmark `.pl`.
- OR-Tools para o solver MIP em Python:

```bash
python3 -m pip install ortools
```

Como executar os programas

1. Abrir um terminal na raiz do repositório.
2. Entrar na pasta do exercício:

```bash
cd "exercicio 3"
```

3. Executar cada módulo conforme o objetivo:

```python
from csp_vigilancia import CSPVigilancia
from resolver_ortools import resolver_ortools
from backtrack_otimizado import backtrack_otimizado
```

Se quiseres testar o benchmark exato em Python:

```bash
python3 solve_exact_cover_fast.py
```

Se quiseres correr o benchmark em SWI-Prolog:

```bash
swipl -q -s "exercicio 3/swi_prolog_benchmark.pl" -g main -t halt
```

- `csp_vigilancia_setup.py` e `solve_exact_cover_fast.py` importam o parser partilhado a partir da raiz do repositório.


