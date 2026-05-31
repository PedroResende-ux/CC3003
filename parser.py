def parser(nome_ficheiro):
    with open(nome_ficheiro, 'r') as f:
        linhas = f.read().strip().split('\n')

    num_instancias = int(linhas[0].strip())
    instancias = []

    idx_linha = 1
    for i in range(num_instancias):
        if idx_linha >= len(linhas):
            break

        num_retangulos = int(linhas[idx_linha].strip())
        idx_linha += 1

        retangulos = []
        vertices_unicos = set()

        for _ in range(num_retangulos):
            partes = list(map(int, linhas[idx_linha].strip().split()))
            idx_linha += 1

            num_pontos = partes[1]
            pontos_deste_retangulo = []
            idx_coord = 2

            for _ in range(num_pontos):
                x = partes[idx_coord]
                y = partes[idx_coord + 1]
                ponto = (x, y)

                pontos_deste_retangulo.append(ponto)
                vertices_unicos.add(ponto)

                idx_coord += 2

            retangulos.append(pontos_deste_retangulo)

        instancias.append({
            'vertices': list(vertices_unicos),
            'retangulos': retangulos,
        })

    return instancias