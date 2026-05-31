from ortools.linear_solver import pywraplp


def resolver_ortools(vertices, retangulos):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return None

    x = {}
    for v in vertices:
        x[v] = solver.IntVar(0, 1, f'x_{v[0]}_{v[1]}')

    for r in retangulos:
        solver.Add(solver.Sum([x[v] for v in r]) >= 1)

    solver.Minimize(solver.Sum([x[v] for v in vertices]))

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('OR-Tools: Solução ótima encontrada!')
        print(f'Mínimo de guardas: {solver.Objective().Value()}')
        return [v for v in vertices if x[v].solution_value() > 0.5]

    print('OR-Tools: Não foi encontrada solução ótima.')
    return None