"""
Laboratorijska vjezba 1 - Pretrazivanje prostora stanja
Implementacija BFS, UCS i A* algoritama te provjera heuristika
"""

import sys
import heapq
from collections import deque


# =============================================================================
# POMOCNE FUNKCIJE
# =============================================================================

def reconstruct_path(parent, start_state, goal_state):
    """
    Rekonstruira putanju od pocetnog do ciljnog stanja.

    Args:
        parent: dict - rjecnik roditelja {stanje: prethodno_stanje}
        start_state: str - pocetno stanje
        goal_state: str - ciljno stanje

    Returns:
        list - lista stanja od pocetnog do ciljnog
    """
    path = []
    current = goal_state
    # Kreci se unazad od cilja prema pocetku
    while current is not None:
        path.append(current)
        current = parent.get(current)
    # Obrni putanju da ide od pocetka prema cilju
    path.reverse()
    return path


def shortest_path_cost(start, goals, graph):
    """
    Izracunava stvarnu cijenu najkraceg puta (h*) od pocetnog stanja do najblizeg cilja.
    Koristi UCS/Dijkstra algoritam za pronalazenje optimalnog puta.

    Args:
        start: str - pocetno stanje
        goals: list - lista ciljnih stanja
        graph: dict - graf prijelaza {stanje: {susjed: cijena}}

    Returns:
        float - najjeftinija cijena do cilja ili inf ako cilj nije dostizan
    """
    # Rjecnik najboljih poznatih cijena za svako stanje
    g_cost = {start: 0.0}
    # Priority queue: (cijena, stanje)
    pq = [(0.0, start)]
    # Skup vec obradenih stanja
    closed = set()
    # Konvertiraj goals u set za O(1) provjeru clanstva
    goals_set = set(goals) if not isinstance(goals, set) else goals

    while pq:
        cost, state = heapq.heappop(pq)

        # Preskoci zastarjeli unos iz priority queue-a
        # (ako smo u meduvremenu nasli jeftiniji put do ovog stanja)
        if cost > g_cost.get(state, float('inf')):
            continue

        # Preskoci ako je stanje vec obradeno
        if state in closed:
            continue
        closed.add(state)

        # Provjeri jesmo li stigli do nekog od ciljnih stanja
        if state in goals_set:
            return cost  # Vraca h*(start) - stvarnu cijenu do cilja

        # Ekspandiraj susjede abecednim redom (za deterministicko ponasanje)
        for neighbor, edge_cost in sorted(graph.get(state, {}).items()):
            tentative = cost + edge_cost

            # Azuriraj ako smo nasli jeftiniji put do susjeda
            if tentative < g_cost.get(neighbor, float('inf')):
                g_cost[neighbor] = tentative
                heapq.heappush(pq, (tentative, neighbor))

    # Cilj nije dostizan iz pocetnog stanja
    return float('inf')


# -------------------------------------------------
# 1. UCITAVANJE PODATAKA
# -------------------------------------------------

def load_state_space(file_path):
    """
    Ucitava prostor stanja iz datoteke.

    Format datoteke:
    - 1. red: pocetno stanje
    - 2. red: ciljna stanja (odvojena razmakom)
    - ostali redovi: prijelazi u formatu "stanje: susjed1,cijena1 susjed2,cijena2 ..."
    - redovi koji pocinju s # su komentari i ignoriraju se

    Args:
        file_path: str - putanja do datoteke

    Returns:
        tuple: (start_state, goal_states, graph)
        - start_state: str - pocetno stanje
        - goal_states: list - lista ciljnih stanja
        - graph: dict - graf prijelaza {stanje: {susjed: cijena}}
    """
    graph = {}
    start_state = None
    goal_states = []

    # Ucitaj datoteku i filtriraj prazne redove i komentare
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print(f"Greska: Datoteka {file_path} nije pronadena.")
        sys.exit(1)

    if not lines:
        return None, [], {}

    # Parsiranje pocetnog stanja (1. redak)
    start_state = lines[0]

    # Parsiranje ciljnih stanja (2. redak)
    goal_states = lines[1].split()

    # Parsiranje prijelaza (ostali redovi)
    transitions = lines[2:]

    for line in transitions:
        try:
            # Format: "stanje: susjed1,cijena1 susjed2,cijena2"
            state, neighbors_str = line.split(':', 1)
            state = state.strip()
            neighbors = {}

            # Parsiraj sve susjede
            for part in neighbors_str.strip().split():
                next_state, cost_str = part.split(',')
                neighbors[next_state.strip()] = float(cost_str)

            graph[state] = neighbors
        except ValueError as e:
            # Preskaci neispravan format
            continue

    return start_state, goal_states, graph


def load_heuristic(file_path):
    """
    Ucitava heuristicke vrijednosti iz datoteke.

    Format datoteke:
    - svaki red: "stanje: vrijednost"
    - redovi koji pocinju s # su komentari i ignoriraju se

    Args:
        file_path: str - putanja do datoteke

    Returns:
        dict: {stanje: heuristicka_vrijednost}
    """
    heuristics = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            for line in lines:
                # Format: "stanje: vrijednost"
                state, value_str = line.split(':', 1)
                heuristics[state.strip()] = float(value_str.strip())
    except FileNotFoundError:
        # Vrati prazan rjecnik ako datoteka ne postoji
        return {}
    except ValueError:
        # Vrati prazan rjecnik ako je format neispravan
        return {}

    return heuristics


# -------------------------------------------------
# 2. ALGORITMI PRETRAZIVANJA
# -------------------------------------------------

def bfs(start, goals, graph):
    """
    Breadth-First Search (BFS) - Pretrazivanje u sirinu.

    BFS istrazuje prostor stanja sloj po sloj, pocevsi od pocetnog stanja.
    Prvo istrazuje sva stanja na dubini 1, zatim na dubini 2, itd.
    Garantira najkraci put po broju cvorova (ne po cijeni).

    Koristi FIFO (First In First Out) red za obradu stanja.
    Susjedi se dodaju abecednim redom radi determinizma.

    Vremenska slozenost: O(|V| + |E|) gdje je V broj stanja, E broj bridova
    Prostorna slozenost: O(|V|) za cuvanje reda i skupa posjecenih stanja

    Args:
        start: str - pocetno stanje
        goals: list - lista ciljnih stanja
        graph: dict - graf prijelaza {stanje: {susjed: cijena}}

    Returns:
        dict - rezultat pretrazivanja s kljucevima:
               found, visited, path_length, total_cost, path
    """
    # Skup vec posjecenih stanja (sprjecava ponavljanje)
    visited = {start}
    # FIFO red: (trenutno_stanje, putanja_do_stanja)
    queue = deque([(start, [start])])
    # Konvertiraj goals u set za O(1) provjeru clanstva
    goals_set = set(goals) if not isinstance(goals, set) else goals

    while queue:
        # Uzmi prvo stanje iz reda (FIFO princip)
        # Ovo osigurava da stanja budu obradena po redoslijedu dubine
        state, path = queue.popleft()

        # Provjera cilja: jesmo li stigli do nekog od ciljnih stanja?
        # Provjeravamo nakon sto izvucemo stanje iz reda (goal test on expansion)
        if state in goals_set:
            # Izracunaj ukupnu cijenu puta (suma svih cijena bridova)
            # Napomena: BFS ne garantira najjeftiniji put, samo najkraci po broju cvorova
            total_cost = 0.0
            for i in range(len(path) - 1):
                s1 = path[i]
                s2 = path[i + 1]
                total_cost += graph[s1].get(s2, 0.0)

            return {
                "found": True,
                "visited": len(visited),
                "path_length": len(path),
                "total_cost": total_cost,
                "path": path
            }

        # Ekspanzija: dodaj sve neposjecene susjede u red
        # Abecedno sortiranje susjeda (vazno za BFS determinizam)
        if state not in graph:
            continue  # Nema susjeda, preskoci ekspanziju

        successors = sorted(graph[state].keys())

        for neighbor in successors:
            if neighbor not in visited:
                visited.add(neighbor)
                # Dodaj susjeda u red s produzenom putanjom
                queue.append((neighbor, path + [neighbor]))

    # Nismo pronasli rjesenje
    return {"found": False, "visited": len(visited)}


def ucs_stable(start, goals, graph):
    """
    Uniform Cost Search (UCS) - Pretrazivanje jednolicne cijene.

    UCS istrazuje prostor stanja tako da uvijek prvo ekspandira stanje s
    najmanjom ukupnom cijenom puta od pocetka. Garantira optimalan put
    (najjeftiniji po cijeni).

    Koristi priority queue (min-heap) gdje je prioritet ukupna cijena g(n).
    Abecedno sortiranje susjeda osigurava determinizam kod jednakih cijena.

    Vremenska slozenost: O(|E| log |V|) zbog operacija s priority queue-om
    Prostorna slozenost: O(|V|) za cuvanje priority queue-a i closed skupa

    Args:
        start: str - pocetno stanje
        goals: list - lista ciljnih stanja
        graph: dict - graf prijelaza {stanje: {susjed: cijena}}

    Returns:
        dict - rezultat pretrazivanja s kljucevima:
               found, visited, path_length, total_cost, path
    """
    # Skup vec obradenih stanja
    closed = set()
    # Najbolje poznate cijene za svako stanje
    g_cost = {start: 0.0}
    # Rjecnik roditelja za rekonstrukciju puta
    parent = {start: None}
    # Konvertiraj goals u set za O(1) provjeru clanstva
    goals_set = set(goals) if not isinstance(goals, set) else goals

    # Priority queue: (g_cost, state)
    # state sluzi kao abecedni tie-breaker kada su g_cost vrijednosti jednake
    # Python automatski usporeduje elemente tuple-a slijeva nadesno
    pq = [(0.0, start)]

    while pq:
        # Uzmi stanje s najmanjom cijenom
        cost, state = heapq.heappop(pq)

        # Preskoci zastarjeli unos iz priority queue-a
        # (ako smo u meduvremenu nasli jeftiniji put)
        if cost > g_cost.get(state, float('inf')):
            continue

        # Preskoci vec obradena stanja
        if state in closed:
            continue
        closed.add(state)

        # Provjera cilja: jesmo li pronasli rjesenje?
        if state in goals_set:
            # Rekonstruiraj putanju od pocetka do cilja
            path = reconstruct_path(parent, start, state)
            return {
                "found": True,
                "visited": len(closed),
                "path_length": len(path),
                "total_cost": cost,
                "path": path
            }

        # Ekspanzija: razmotrimo sve susjede trenutnog stanja
        # Abecedno sortiranje za deterministicko ponasanje
        if state not in graph:
            continue  # Nema susjeda, preskoci ekspanziju

        for neighbor, edge_cost in sorted(graph[state].items()):
            tentative = cost + edge_cost

            # Azuriraj ako smo nasli jeftiniji put do susjeda
            if tentative < g_cost.get(neighbor, float('inf')):
                g_cost[neighbor] = tentative
                parent[neighbor] = state
                # Dodaj u priority queue: (g_cost, state)
                heapq.heappush(pq, (tentative, neighbor))

    # Nismo pronasli rjesenje
    return {"found": False, "visited": len(closed)}


def astar_stable(start, goals, graph, heuristics):
    """
    A* Search - Heuristicki algoritam pretrazivanja.

    A* kombinira stvarnu cijenu puta g(n) s heuristickom procjenom h(n)
    do cilja. Ekspandira stanje s najmanjom vrijednosti f(n) = g(n) + h(n).

    Ako je heuristika admisibilna (optimisticna), A* garantira optimalan put.
    Ako je heuristika konzistentna, A* je jos ucinkovitiji.

    Koristi priority queue gdje je prioritet f(n) = g(n) + h(n).
    Abecedno sortiranje susjeda osigurava determinizam kod jednakih f(n).

    Vremenska slozenost: O(|E| log |V|), ali cesto brze od UCS zbog heuristike
    Prostorna slozenost: O(|V|) za cuvanje priority queue-a i closed skupa

    Args:
        start: str - pocetno stanje
        goals: list - lista ciljnih stanja
        graph: dict - graf prijelaza {stanje: {susjed: cijena}}
        heuristics: dict - heuristicke vrijednosti {stanje: h(stanje)}

    Returns:
        dict - rezultat pretrazivanja s kljucevima:
               found, visited, path_length, total_cost, path
    """
    # Skup vec obradenih stanja
    closed = set()
    # Najbolje poznate cijene puta (g vrijednosti)
    g_cost = {start: 0.0}
    # Rjecnik roditelja za rekonstrukciju puta
    parent = {start: None}
    # Heuristicka vrijednost pocetnog stanja
    h0 = heuristics.get(start, 0.0)
    # Konvertiraj goals u set za O(1) provjeru clanstva
    goals_set = set(goals) if not isinstance(goals, set) else goals

    # Priority queue: (f=g+h, state, g)
    # f: prioritet za sortiranje (g + h)
    # state: abecedni tie-breaker kada su f vrijednosti jednake
    # g: stvarna cijena (potrebno za provjeru zastarjelih unosa)
    pq = [(h0, start, 0.0)]

    while pq:
        # Uzmi stanje s najmanjom f(n) vrijednosti
        f, state, g = heapq.heappop(pq)

        # Preskoci zastarjeli unos iz priority queue-a
        # (ako smo u meduvremenu nasli jeftiniji put)
        if g > g_cost.get(state, float('inf')):
            continue

        # Preskoci vec obradena stanja
        if state in closed:
            continue
        closed.add(state)

        # Provjera cilja: jesmo li pronasli rjesenje?
        if state in goals_set:
            # Rekonstruiraj putanju od pocetka do cilja
            path = reconstruct_path(parent, start, state)
            return {
                "found": True,
                "visited": len(closed),
                "path_length": len(path),
                "total_cost": g,  # Vracamo g (stvarnu cijenu), ne f
                "path": path
            }

        # Ekspanzija: razmotrimo sve susjede trenutnog stanja
        # Abecedno sortiranje za deterministicko ponasanje
        if state not in graph:
            continue  # Nema susjeda, preskoci ekspanziju

        for neighbor, edge_cost in sorted(graph[state].items()):
            # Izracunaj novu g(neighbor) vrijednost
            tentative_g = g + edge_cost

            # Azuriraj ako smo nasli jeftiniji put do susjeda
            if tentative_g < g_cost.get(neighbor, float('inf')):
                g_cost[neighbor] = tentative_g
                parent[neighbor] = state
                # Dohvati heuristicku procjenu za susjeda
                h = heuristics.get(neighbor, 0.0)
                # Izracunaj f(neighbor) = g(neighbor) + h(neighbor)
                # Dodaj u priority queue: (f_cost, state, g_cost)
                heapq.heappush(pq, (tentative_g + h, neighbor, tentative_g))

    # Nismo pronasli rjesenje
    return {"found": False, "visited": len(closed)}


# -------------------------------------------------
# 3. PROVJERA HEURISTIKE
# -------------------------------------------------

def check_optimistic(graph, heuristics, goals, heuristic_file):
    """
    Provjerava je li heuristika optimisticna (admisibilna).

    Heuristika h je optimisticna ako za svako stanje s vrijedi:
    h(s) <= h*(s)

    gdje je h*(s) stvarna najjeftinija cijena od s do najblizeg cilja.

    Optimisticna heuristika nikad ne precjenjuje stvarnu cijenu do cilja,
    sto je nuzan uvjet da A* garantira optimalan put.

    Args:
        graph: dict - graf prijelaza
        heuristics: dict - heuristicke vrijednosti
        goals: list - ciljna stanja
        heuristic_file: str - ime datoteke s heuristikom (za ispis)
    """
    print(f"# HEURISTIC-OPTIMISTIC {heuristic_file}")
    is_optimistic = True

    # Prikupi sva stanja iz grafa i heuristike
    all_states = set(graph.keys())
    all_states.update(heuristics.keys())

    # Provjeri svako stanje abecednim redom
    for state in sorted(all_states):
        # Dohvati heuristicku procjenu h(s)
        h_s = heuristics.get(state, 0.0)
        # Izracunaj stvarnu najjeftiniju cijenu h*(s)
        h_s_star = shortest_path_cost(state, goals, graph)

        result = ""
        # Provjera uvjeta: h(s) <= h*(s)
        # Ako je cilj nedostizan (h* = inf), ignoriramo/OK
        if h_s_star == float('inf') or h_s <= h_s_star:
            result = "[OK]"
        else:
            # Heuristika precjenjuje - nije optimisticna
            result = "[ERR]"
            is_optimistic = False

        # Ispis s jednom decimalom
        print(f"[CONDITION]: {result} h({state}) <= h*: {h_s:.1f} <= {h_s_star:.1f}")

    # Ispis zakljucka
    conclusion = "Heuristic is optimistic." if is_optimistic else "Heuristic is not optimistic."
    print(f"[CONCLUSION]: {conclusion}")


def check_consistent(graph, heuristics, heuristic_file):
    """
    Provjerava je li heuristika konzistentna (monotona).

    Heuristika h je konzistentna ako za svaki prijelaz s -> t vrijedi:
    h(s) <= c(s, t) + h(t)

    gdje je c(s, t) cijena prijelaza iz stanja s u stanje t.

    Konzistentnost je jaci uvjet od optimisticnosti. Ako je heuristika
    konzistentna, ona je i optimisticna. Konzistentna heuristika garantira
    da A* nece morati ponovo otvarati zatvorena stanja.

    Args:
        graph: dict - graf prijelaza
        heuristics: dict - heuristicke vrijednosti
        heuristic_file: str - ime datoteke s heuristikom (za ispis)
    """
    print(f"# HEURISTIC-CONSISTENT {heuristic_file}")
    is_consistent = True

    # Prikupi sva stanja
    all_states = set(graph.keys())
    all_states.update(heuristics.keys())

    # Provjeri svaki prijelaz abecednim redom
    for state_s in sorted(all_states):
        # Dohvati heuristicku vrijednost h(s)
        h_s = heuristics.get(state_s, 0.0)

        # Iteracija preko svih prijelaza (s -> t) abecedno
        successors = sorted(graph.get(state_s, {}).items())

        for neighbor_t, cost_c in successors:
            # Dohvati heuristicku vrijednost h(t)
            h_t = heuristics.get(neighbor_t, 0.0)

            # Provjera uvjeta: h(s) <= c(s, t) + h(t)
            if h_s <= cost_c + h_t:
                result = "[OK]"
            else:
                # Uvjet konzistentnosti nije zadovoljen
                result = "[ERR]"
                is_consistent = False

            # Ispis s jednom decimalom
            print(f"[CONDITION]: {result} h({state_s}) <= h({neighbor_t}) + c: {h_s:.1f} <= {h_t:.1f} + {cost_c:.1f}")

    # Ispis zakljucka
    conclusion = "Heuristic is consistent." if is_consistent else "Heuristic is not consistent."
    print(f"[CONCLUSION]: {conclusion}")


# -------------------------------------------------
# 4. ISPIS REZULTATA
# -------------------------------------------------

def print_result(alg_name, result, heuristic_file=None):
    """
    Ispisuje rezultat pretrazivanja u standardnom formatu.

    Args:
        alg_name: str - ime algoritma (BFS, UCS, A-STAR)
        result: dict - rezultat pretrazivanja
        heuristic_file: str - ime datoteke s heuristikom (samo za A*)
    """
    # Zaglavlje s imenom algoritma
    header = f"# {alg_name.upper()}"
    if heuristic_file:
        header += f" {heuristic_file}"

    print(header)

    # Ako rjesenje nije pronadeno
    if not result["found"]:
        print("[FOUND_SOLUTION]: no")
        return

    # Ako je rjesenje pronadeno, ispisi sve detalje
    print("[FOUND_SOLUTION]: yes")
    print(f"[STATES_VISITED]: {result['visited']}")
    # Duzina puta je broj cvorova
    print(f"[PATH_LENGTH]: {result['path_length']}")
    # Ukupna cijena s jednom decimalom
    print(f"[TOTAL_COST]: {result['total_cost']:.1f}")
    print(f"[PATH]: {' => '.join(result['path'])}")


# =============================================================================
# 5. GLAVNI PROGRAM
# =============================================================================

if __name__ == "__main__":

    # 1. Parsiranje argumenata komandne linije
    # Ocekivani formati:
    # --alg [bfs|ucs|astar] --ss <datoteka> [--h <datoteka>]
    # --ss <datoteka> --h <datoteka> --check-optimistic
    # --ss <datoteka> --h <datoteka> --check-consistent
    args = sys.argv[1:]
    args_dict = {}
    flags = set()

    # Parsiraj argumente u rjecnik i skup zastavica
    for i in range(len(args)):
        if args[i].startswith("--"):
            if i + 1 < len(args) and not args[i + 1].startswith("--"):
                # Argument s vrijednoscu (npr. --ss istra.txt)
                args_dict[args[i]] = args[i + 1]
            else:
                # Zastavica bez vrijednosti (npr. --check-optimistic)
                flags.add(args[i])

    # Dohvati argumente
    ss_path = args_dict.get('--ss')
    h_path = args_dict.get('--h')
    alg = args_dict.get('--alg')

    # Provjeri je li naveden opisnik prostora stanja
    if not ss_path:
        sys.exit(1)

    # 2. Ucitavanje stanja (potrebno za sve modove)
    start_state, goal_states, graph = load_state_space(ss_path)

    # 3. Ucitavanje heuristike (potrebno za A* i provjere)
    heuristics = {}
    if h_path:
        heuristics = load_heuristic(h_path)

    # 4. Provjere heuristike (imaju najvisi prioritet)
    if '--check-optimistic' in flags:
        if not h_path:
            sys.exit(1)
        check_optimistic(graph, heuristics, goal_states, h_path)
        sys.exit(0)

    if '--check-consistent' in flags:
        if not h_path:
            sys.exit(1)
        check_consistent(graph, heuristics, h_path)
        sys.exit(0)

    # 5. Pokretanje algoritama pretrazivanja
    if not alg:
        sys.exit(1)

    # Inicijalizacija rezultata (default vrijednost ako nijedan algoritam ne uspije)
    res = {"found": False, "visited": 0}

    # Pokreni odabrani algoritam
    if alg == 'bfs':
        res = bfs(start_state, goal_states, graph)
        print_result('BFS', res)
    elif alg == 'ucs':
        res = ucs_stable(start_state, goal_states, graph)
        print_result('UCS', res)
    elif alg == 'astar':
        if not h_path:
            sys.exit(1)
        res = astar_stable(start_state, goal_states, graph, heuristics)
        print_result('A-STAR', res, h_path)
    else:
        sys.exit(1)
