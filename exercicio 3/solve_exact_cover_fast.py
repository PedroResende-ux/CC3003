import time
from functools import lru_cache
from pathlib import Path
import sys


repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from parser import parser


def solve_exact_cover_fast(instance):
    vertices = instance['vertices']
    rects = instance['retangulos']
    rect_count = len(rects)
    all_mask = (1 << rect_count) - 1

    vertex_masks = []
    for vertex in vertices:
        mask = 0
        for rect_index, rect in enumerate(rects):
            if vertex in rect:
                mask |= 1 << rect_index
        if mask:
            vertex_masks.append((vertex, mask))

    if not vertex_masks:
        return []

    rect_to_vertices = [[] for _ in range(rect_count)]
    for vertex_index, (_, mask) in enumerate(vertex_masks):
        for rect_index in range(rect_count):
            if (mask >> rect_index) & 1:
                rect_to_vertices[rect_index].append(vertex_index)

    uncovered = all_mask
    greedy_solution = []
    while uncovered:
        best_index = max(
            range(len(vertex_masks)),
            key=lambda i: (vertex_masks[i][1] & uncovered).bit_count()
        )
        greedy_solution.append(best_index)
        uncovered &= ~vertex_masks[best_index][1]

    best = {
        'count': len(greedy_solution),
        'solution': greedy_solution[:],
        'seen': {}
    }

    @lru_cache(maxsize=None)
    def lower_bound(mask):
        if mask == 0:
            return 0

        remaining = mask.bit_count()
        max_cover = max((vm & mask).bit_count() for _, vm in vertex_masks)
        if max_cover == 0:
            return 10**9
        return (remaining + max_cover - 1) // max_cover

    def search(mask, chosen):
        if not mask:
            if len(chosen) < best['count']:
                best['count'] = len(chosen)
                best['solution'] = chosen[:]
            return

        if len(chosen) + lower_bound(mask) >= best['count']:
            return

        previous = best['seen'].get(mask)
        if previous is not None and previous <= len(chosen):
            return
        best['seen'][mask] = len(chosen)

        hardest_rect = min(
            (rect_index for rect_index in range(rect_count) if (mask >> rect_index) & 1),
            key=lambda rect_index: len(rect_to_vertices[rect_index])
        )

        candidates = sorted(
            rect_to_vertices[hardest_rect],
            key=lambda vertex_index: (vertex_masks[vertex_index][1] & mask).bit_count(),
            reverse=True
        )

        for vertex_index in candidates:
            cover_mask = vertex_masks[vertex_index][1] & mask
            if cover_mask == 0:
                continue
            chosen.append(vertex_index)
            search(mask & ~cover_mask, chosen)
            chosen.pop()

    search(all_mask, [])
    return [vertex_masks[index][0] for index in best['solution']]


base_candidates = [
    Path(__file__).resolve().parent.parent / 'PartsRectangulares' / 'Exemplos',
    Path.cwd() / 'PartsRectangulares' / 'Exemplos',
]
base_dir = next((candidate for candidate in base_candidates if candidate.exists()), None)

if base_dir is None:
    raise FileNotFoundError('Nao foi possivel localizar a pasta PartsRectangulares/Exemplos')

ficheiros_teste = [
    str(base_dir / 'parts40'),
    str(base_dir / 'step50')
]

print('==================================================')
print('   AVALIAÇÃO EXPERIMENTAL DOS MÉTODOS EXATOS      ')
print('==================================================\n')

for ficheiro in ficheiros_teste:
    nome_instancia = ficheiro.split('/')[-1]

    try:
        instancias = parser(ficheiro)
        instancia = instancias[0]

        print(f'--- Instância: {nome_instancia} ---')
        print(f"Dimensão: {len(instancia['vertices'])} vértices | {len(instancia['retangulos'])} retângulos")

        start_mip = time.time()
        solucao_mip = resolver_ortools(instancia['vertices'], instancia['retangulos'])
        tempo_mip = time.time() - start_mip

        melhor_valor_mip = len(solucao_mip) if solucao_mip else float('inf')

        if solucao_mip:
            print(f'  > OR-Tools (MIP): {melhor_valor_mip} guardas | Tempo: {tempo_mip:.4f}s')
        else:
            print('  > OR-Tools (MIP): Nenhuma solução encontrada.')

        start_mac = time.time()
        solucao_mac = solve_exact_cover_fast(instancia)
        tempo_mac = time.time() - start_mac

        if solucao_mac:
            print(f'  > MAC (AC-3+B&B): {len(solucao_mac)} guardas | Tempo: {tempo_mac:.4f}s\n')
        else:
            print('  > MAC (AC-3+B&B): Nenhuma solução encontrada.\n')

    except Exception as e:
        print(f'Erro ao processar a instância {nome_instancia}: {e}\n')