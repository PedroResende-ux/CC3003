class CSPVigilancia:
    def __init__(self, vertices, retangulos_alvo):
        self.vertices = vertices
        self.retangulos = retangulos_alvo
        self.dominios = {v: {0, 1} for v in vertices}
        self.atribuicoes = {}
        self.vertice_para_retangulos = {v: [] for v in vertices}

        for indice_r, retangulo in enumerate(self.retangulos):
            for v in retangulo:
                if v in self.vertice_para_retangulos:
                    self.vertice_para_retangulos[v].append(indice_r)

    def is_completo(self):
        return len(self.atribuicoes) == len(self.vertices)

    def get_variavel_nao_atribuida(self):
        for v in self.vertices:
            if v not in self.atribuicoes:
                return v
        return None

    def revise(self, v, indice_r):
        retangulo = self.retangulos[indice_r]

        if any(self.atribuicoes.get(outro_v) == 1 for outro_v in retangulo):
            return False

        podem_cobrir = [outro_v for outro_v in retangulo if 1 in self.dominios[outro_v]]
        if len(podem_cobrir) == 1 and podem_cobrir[0] == v:
            if 0 in self.dominios[v]:
                self.dominios[v].remove(0)
                return True

        return False

    def ac3(self):
        fila = [(v, r) for v in self.vertices for r in self.vertice_para_retangulos[v]]

        while fila:
            v, r = fila.pop(0)
            if self.revise(v, r):
                if not self.dominios[v]:
                    return False

                for vizinho_r in self.vertice_para_retangulos[v]:
                    if vizinho_r != r:
                        for outro_v in self.retangulos[vizinho_r]:
                            if outro_v != v:
                                fila.append((outro_v, vizinho_r))

        return True