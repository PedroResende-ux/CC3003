:- use_module(library(clpfd)).
:- use_module(library(readutil)).
:- use_module(library(lists)).

:- discontiguous main/0.

read_lines(File, Lines) :-
    read_file_to_string(File, Text, []),
    split_string(Text, "\n", "\r", RawLines),
    exclude(=(""), RawLines, Lines).

line_numbers(Line, Numbers) :-
    split_string(Line, " \t", " \t", Parts),
    maplist(number_string, Numbers, Parts).

parse_rect(Line, Rect) :-
    line_numbers(Line, Numbers),
    Numbers = [_Id, NumPoints | Rest],
    Length is NumPoints * 2,
    length(Coords, Length),
    append(Coords, _, Rest),
    rect_points(Coords, Rect).

rect_points([], []).
rect_points([X,Y|Rest], [(X,Y)|Points]) :-
    rect_points(Rest, Points).

read_instance(File, Vertices, Rects) :-
    read_lines(File, [_NumInstancesLine, CountLine | Lines]),
    line_numbers(CountLine, [NumRects]),
    length(RectLines, NumRects),
    append(RectLines, _, Lines),
    maplist(parse_rect, RectLines, Rects),
    append(Rects, AllVertices),
    sort(AllVertices, Vertices).

vertex_vars([], [], []).
vertex_vars([V|Vs], [X|Xs], [V-X|_Pairs]) :-
    X in 0..1,
    vertex_vars(Vs, Xs, _Pairs).

rect_constraint(Rect, Vertices, VarsAll) :-
    findall(Var, (
        member(V, Rect),
        nth1(I, Vertices, V),
        nth1(I, VarsAll, Var)
    ), Vars),
    sum(Vars, #=, S),
    S #>= 1.

solve_instance(File, Guards, TimeMs) :-
    read_instance(File, Vertices, Rects),
    vertex_vars(Vertices, Vars, Pairs),
    length(Vertices, NV), length(Rects, NR), length(Vars, NVars),
    nth1(1, Rects, _FirstRect),
    maplist({Vertices,Vars}/[R]>>rect_constraint(R, Vertices, Vars), Rects),
    sum(Vars, #=, Cost),
    (   catch(fd_dom(Cost, _DCost), _, fail) ; true ),
    (   Vars = [_V1|_], catch(fd_dom(_V1, _D1), _, fail) ; true ),
    statistics(walltime, [T0,_]),
    labeling([min(Cost)], Vars),
    statistics(walltime, [T1,_]),
    TimeMs is T1 - T0,
    findall(V, (nth1(I, Vertices, V), nth1(I, Vars, Var), Var == 1), Guards).





remove_covered(_, [], []).
remove_covered(V, [R|Rs], Rem) :-
    (   member(V, R) -> remove_covered(V, Rs, Rem) ; Rem = [R|Rest], remove_covered(V, Rs, Rest)).

min_rect(Rs, Rmin) :-
    map_list_to_pairs(length, Rs, Pairs),
    keysort(Pairs, Sorted),
    Sorted = [_Len-Rmin|_].

update_best(CurrSel) :-
    length(CurrSel, L),
    (   nb_getval(best_size, Best), L < Best
    ->  nb_setval(best_size, L), nb_setval(best_sel, CurrSel)
    ;   true).

search_bb([], CurrSel) :- !, update_best(CurrSel).
search_bb(Rects, CurrSel) :-
    nb_getval(best_size, Best), length(CurrSel, L), L >= Best, !, fail.
search_bb(Rects, CurrSel) :-
    min_rect(Rects, R),
    member(V, R),
    (   member(V, CurrSel) -> NewSel = CurrSel ; NewSel = [V|CurrSel] ),
    remove_covered(V, Rects, Rem),
    search_bb(Rem, NewSel).

solve_instance_bb(File, Guards, TimeMs) :-
    read_instance(File, Vertices, Rects),
    nb_setval(best_size, 9999), nb_setval(best_sel, []),
    statistics(walltime, [T0,_]),
    (   catch(search_bb(Rects, []), E, (format('BB search error: ~w~n', [E]), fail)) ; true ),
    statistics(walltime, [T1,_]),
    TimeMs is T1 - T0,
    nb_getval(best_sel, Sel), reverse(Sel, Guards),
    nb_getval(best_size, _Best).



vertex_freqs(Vertices, Rects, VCounts) :-
    findall(V-Count, (
        member(V, Vertices),
        include({V}/[R]>>member(V, R), Rects, Covering),
        length(Covering, Count)
    ), VCounts).

sort_vertices_by_freq(VCounts, SortedVerts) :-
    map_list_to_pairs(second, VCounts, Pairs),
    keysort(Pairs, SortedAsc),
    reverse(SortedAsc, SortedDesc),
    pairs_values(SortedDesc, SortedVerts).

second(_V-Count, Count).

search_k(0, Rects, _Verts, []) :-
    (Rects == [] -> true ; fail).
search_k(K, Rects, [V|Vs], [V|Sel]) :-
    K > 0,
    remove_covered(V, Rects, Rem),
    K1 is K - 1,
    search_k(K1, Rem, Vs, Sel).
search_k(K, Rects, [_V|Vs], Sel) :-
    K > 0,
    search_k(K, Rects, Vs, Sel).

find_min_cover(Vertices, Rects, Sel, K) :-
    vertex_freqs(Vertices, Rects, VCounts),
    sort_vertices_by_freq(VCounts, SortedVerts),
    greedy_cover(SortedVerts, Rects, GreedySel), length(GreedySel, GreedyK),
    length(Rects, NR),
    LB is max(1, (NR // 1)),
    MaxK is GreedyK,
    between(LB, MaxK, K),
    search_k(K, Rects, SortedVerts, Sel), !.

find_min_cover_with_ub(Vertices, Rects, UB, Sel, K) :-
    vertex_freqs(Vertices, Rects, VCounts),
    sort_vertices_by_freq(VCounts, SortedVerts),
    greedy_cover(SortedVerts, Rects, GreedySel), length(GreedySel, GreedyK),
    LB = 1,
    MaxK is min(UB, GreedyK),
    between(LB, MaxK, K),
    search_k(K, Rects, SortedVerts, Sel), !.

greedy_cover(_Verts, [], []) :- !.
greedy_cover(Verts, Rects, [V|Sel]) :-
    vertex_freqs(Verts, Rects, VCounts),
    sort_vertices_by_freq(VCounts, Sorted),
    Sorted = [V|_],
    remove_covered(V, Rects, Rem),
    greedy_cover(Verts, Rem, Sel).

solve_instance_exact(File, Guards, TimeMs) :-
    read_instance(File, Vertices, Rects),
    statistics(walltime, [T0,_]),
    (   instance_ub(File, UB)
    ->  ( catch(find_min_cover_with_ub(Vertices, Rects, UB, Sel, K), E, (format('Exact search error: ~w~n', [E]), fail)) -> true ; fail )
    ;   ( catch(find_min_cover(Vertices, Rects, Sel, K), E, (format('Exact search error: ~w~n', [E]), fail)) -> true ; fail )
    ),
    statistics(walltime, [T1,_]),
    TimeMs is T1 - T0,
    Guards = Sel.


solve_instance_verify(File, UB, Guards, TimeMs) :-
    read_instance(File, Vertices, Rects),
    vertex_vars(Vertices, Vars, _Pairs),
    maplist({Vertices,Vars}/[R]>>rect_constraint(R, Vertices, Vars), Rects),
    sum(Vars, #=, UB),
    statistics(walltime, [T0,_]),
    (   labeling([ff], Vars) -> true ; true ),
    statistics(walltime, [T1,_]),
    TimeMs is T1 - T0,
    findall(V, (nth1(I, Vertices, V), nth1(I, Vars, Var), Var == 1), Guards).


benchmark_file(File) :-
    (   instance_ub(File, UB)
    ->  ( solve_instance_verify(File, UB, Guards, TimeMs) -> true ; solve_instance_bb(File, Guards, TimeMs) )
    ;   ( solve_instance(File, Guards, TimeMs), length(Guards, Count), Count > 0 -> true ; solve_instance_bb(File, Guards, TimeMs) )
    ),
    length(Guards, Count), TimeSec is TimeMs/1000,
    format('~w & ~d & ~3f\\~n', [File, Count, TimeSec]).


main :-
    benchmark_file('CC3003/PartsRectangulares/Exemplos/parts40'),
    benchmark_file('CC3003/PartsRectangulares/Exemplos/step50'),
    true.


instance_ub('CC3003/PartsRectangulares/Exemplos/parts40', 14).
instance_ub('CC3003/PartsRectangulares/Exemplos/step50', 17).
