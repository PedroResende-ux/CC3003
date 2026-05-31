from pathlib import Path


def encontrar_ficheiro_dados(nome_ficheiro):
    base_candidates = [
        Path(__file__).resolve().parent.parent / 'PartsRectangulares' / 'Exemplos',
        Path.cwd() / 'PartsRectangulares' / 'Exemplos',
    ]

    for base_dir in base_candidates:
        candidate = base_dir / nome_ficheiro
        if candidate.exists():
            return str(candidate)

    raise FileNotFoundError(f'Nao foi possivel localizar o ficheiro de dados: {nome_ficheiro}')


ficheiro_dados = encontrar_ficheiro_dados('parts40')
todas_instancias = parser(ficheiro_dados)

instancia_teste = todas_instancias[0]

motor_csp = CSPVigilancia(
    vertices=instancia_teste['vertices'],
    retangulos_alvo=instancia_teste['retangulos']
)

print(f" -> Total de vértices: {len(motor_csp.vertices)}")
print(f" -> Total de retângulos a cobrir: {len(motor_csp.retangulos)}")