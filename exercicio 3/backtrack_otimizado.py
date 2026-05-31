def backtrack_otimizado(csp, melhor_atribuicao, limite_guardas):
    guardas_atuais = sum(1 for v in csp.atribuicoes.values() if v == 1)

    if guardas_atuais >= limite_guardas[0]:
        return

    if csp.is_completo():
        melhor_atribuicao.clear()
        melhor_atribuicao.update(csp.atribuicoes)
        limite_guardas[0] = guardas_atuais
        return

    v = csp.get_variavel_nao_atribuida()

    for valor in [0, 1]:
        if valor in csp.dominios[v]:
            backup = {var: set(dom) for var, dom in csp.dominios.items()}

            csp.atribuicoes[v] = valor
            csp.dominios[v] = {valor}

            if csp.ac3():
                backtrack_otimizado(csp, melhor_atribuicao, limite_guardas)

            del csp.atribuicoes[v]
            csp.dominios = backup