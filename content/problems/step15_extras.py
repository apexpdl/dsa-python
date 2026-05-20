"""Step 15 extras — Graphs (47 problems).

Comprehensive coverage of the Striver A-Z Step 15: graph fundamentals,
BFS/DFS applications, topological sort, shortest paths (BFS/Dijkstra/
Bellman-Ford/Floyd-Warshall), MST (Prim, Kruskal), DSU, and advanced
algorithms (Kosaraju SCC, Tarjan bridges, articulation points).
"""
from __future__ import annotations


_SHEET = {
    "label": "Striver's A2Z DSA Course Sheet",
    "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
}


def _lc(num: int, slug: str) -> dict:
    return {
        "label": f"LeetCode {num} — {slug.replace('-', ' ').title()}",
        "url": f"https://leetcode.com/problems/{slug}/",
    }


PROBLEMS: list[dict] = [
    # ==================================================================
    # LEARNING
    # ==================================================================
    {
        "id": "graph-introduction",
        "title": "Introduction to Graphs",
        "step_id": 15,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["graph", "concept"],
        "what_this_teaches": "Vocabulary: vertex, edge, directed/undirected, weighted, cycle, path, connected, dense vs sparse.",
        "pattern": "Conceptual.",
        "prerequisite_lessons": [],
        "prerequisite_problems": [],
        "next_problems": ["graph-representation"],
        "resources": [
            {"label": "Wikipedia — Graph", "url": "https://en.wikipedia.org/wiki/Graph_(abstract_data_type)"},
            _SHEET,
        ],
        "understanding": r'''
A **graph** is a set of *vertices* (or *nodes*) connected by *edges*.
Unlike trees, graphs may have cycles, multiple components, and edges
can point both ways or just one.

**Key distinctions:**
- **Directed vs undirected**: in a directed graph an edge `u → v` does
  not imply `v → u`.
- **Weighted vs unweighted**: each edge may carry a weight (cost,
  distance, capacity).
- **Connected vs disconnected**: a graph is connected if every pair of
  vertices has a path; otherwise it has multiple *components*.
- **Cyclic vs acyclic**: contains a closed loop or not. A directed
  acyclic graph (DAG) supports topological ordering.
- **Sparse vs dense**: O(V) edges (sparse) vs O(V²) edges (dense).
  Choice of representation depends on this.

Real-world examples: road networks, social networks, dependency graphs,
state-transition systems, web link graphs, neural networks. Graphs are
the most general data structure for representing relationships.
''',
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Master the vocabulary first; it determines which algorithm to reach for.",
        "optimized": {"explanation": "—", "code": "", "complexity": "—"},
        "deep_concept": "Trees are a special case of graphs (connected, acyclic, undirected, with a designated root). Linked lists are a special case of trees. Almost everything in DSA is some form of graph problem.",
        "confusion_notes": [
            {
                "question": "When is a problem secretly a graph problem?",
                "answer": "Whenever you have *entities* and *relations between them*. Word ladder (words → graph), course schedule (courses → graph), social networks (people → graph), 2D grid problems (cells → graph), even DP problems can sometimes be reframed as shortest-path on a DAG.",
            },
        ],
        "summary": "Graph = vertices + edges. Master directed/undirected, weighted/unweighted, cyclic/acyclic distinctions.",
    },
    {
        "id": "graph-representation",
        "title": "Graph Representations: Adjacency List vs Matrix",
        "step_id": 15,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["graph", "representation"],
        "what_this_teaches": "Memory and time trade-offs between adjacency list and adjacency matrix.",
        "pattern": "Choosing a representation.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["graph-introduction"],
        "next_problems": ["graph-bfs", "graph-dfs"],
        "resources": [
            {"label": "GFG — Graph representations", "url": "https://www.geeksforgeeks.org/graph-and-its-representations/"},
            _SHEET,
        ],
        "understanding": r'''
**Adjacency list**: for each vertex, store a list of neighbors. Memory
O(V + E). Iterating over neighbors of v takes O(deg(v)). This is the
default representation for sparse graphs (most real-world graphs).

**Adjacency matrix**: a V × V matrix where `m[u][v]` indicates if an
edge exists (and possibly its weight). Memory O(V²). Edge lookup is
O(1). Useful for dense graphs, Floyd-Warshall, or when you frequently
query 'is u connected to v?'.

**Edge list**: just a list of (u, v, w) triples. Useful for Kruskal's
MST algorithm (sort edges).
''',
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Default to adjacency list. Use matrix only when V is small (≤ 500) and you need O(1) edge queries.",
        "optimized": {
            "explanation": "Three representations of the same graph.",
            "code": r'''
from collections import defaultdict

# Adjacency list (undirected)
adj = defaultdict(list)
def add_edge(u, v):
    adj[u].append(v); adj[v].append(u)

# Adjacency matrix (undirected, V=4)
V = 4
mat = [[0]*V for _ in range(V)]
def add_edge_mat(u, v):
    mat[u][v] = 1; mat[v][u] = 1

# Edge list (weighted)
edges = []
def add_edge_list(u, v, w):
    edges.append((u, v, w))
''',
            "complexity": "List O(V + E), matrix O(V²), edge list O(E).",
        },
        "deep_concept": "—",
        "confusion_notes": [
            {
                "question": "Why is adjacency list the default in practice?",
                "answer": "Because most graphs are sparse — E is usually much smaller than V². On a Facebook-like graph with billions of users, the matrix would be a quintillion entries, mostly zeros. Adjacency list scales with actual relationships.",
            },
        ],
        "summary": "List for sparse + iteration. Matrix for dense + O(1) edge queries. Edge list for sorting algorithms.",
    },
    {
        "id": "connected-components",
        "title": "Connected Components",
        "step_id": 15,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["graph", "dfs", "bfs"],
        "what_this_teaches": "Multiple BFS/DFS launches to handle disconnected graphs.",
        "pattern": "Loop over vertices, launch search per unvisited.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["graph-representation"],
        "next_problems": ["graph-bfs", "graph-dfs"],
        "resources": [
            {"label": "GFG — Connected components", "url": "https://www.geeksforgeeks.org/connected-components-in-an-undirected-graph/"},
            _SHEET,
        ],
        "understanding": "Find all maximal sets of mutually-reachable vertices in an undirected graph.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Iterate over all vertices; if unvisited, launch BFS/DFS from it (a new component); mark everything reachable.",
        "optimized": {
            "explanation": "Loop + DFS per unvisited vertex.",
            "code": r'''
def count_components(V, adj):
    visited = [False] * V
    count = 0
    def dfs(u):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs(v)
    for u in range(V):
        if not visited[u]:
            count += 1
            dfs(u)
    return count
''',
            "complexity": "Time O(V + E), space O(V).",
        },
        "deep_concept": "Each DFS/BFS marks one component; the outer loop ensures we don't miss isolated parts.",
        "confusion_notes": [],
        "summary": "For each unvisited vertex, do a DFS/BFS — that's one component.",
    },
    {
        "id": "graph-dfs",
        "title": "Depth-First Search on a Graph",
        "step_id": 15,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["graph", "dfs"],
        "what_this_teaches": "Recursive DFS with a visited set; how it differs from tree DFS (cycles).",
        "pattern": "DFS with visited.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["graph-bfs"],
        "next_problems": ["number-of-provinces"],
        "resources": [
            {"label": "GFG — Graph DFS", "url": "https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/"},
            _SHEET,
        ],
        "understanding": "Walk a graph by always going deeper from the current vertex before backtracking. Use a visited set to avoid infinite loops in cyclic graphs.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "—",
        "optimized": {
            "explanation": "Recursive DFS.",
            "code": r'''
def dfs(start, adj, visited=None):
    if visited is None: visited = set()
    visited.add(start)
    out = [start]
    for v in adj[start]:
        if v not in visited:
            out.extend(dfs(v, adj, visited))
    return out
''',
            "complexity": "Time O(V + E), space O(V).",
        },
        "deep_concept": "DFS uses an *implicit* stack (the call stack). For very deep graphs, prefer an explicit stack to avoid Python's recursion limit.",
        "confusion_notes": [
            {
                "question": "Tree DFS doesn't use 'visited' — why does graph DFS need it?",
                "answer": "Because trees have no cycles. Graphs do, so without `visited` we'd revisit vertices forever (in cycles) or duplicate work (in DAGs that aren't trees).",
            },
        ],
        "summary": "DFS with visited set. O(V + E) for the standard variant.",
    },

    # ==================================================================
    # BFS / DFS PROBLEMS
    # ==================================================================
    {
        "id": "number-of-provinces",
        "title": "Number of Provinces",
        "step_id": 15,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["graph", "dfs", "dsu"],
        "what_this_teaches": "Counting connected components from an adjacency matrix.",
        "pattern": "Connected components.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["connected-components"],
        "next_problems": ["connected-components-undirected"],
        "resources": [
            _lc(547, "number-of-provinces"),
            _SHEET,
        ],
        "understanding": "Cities are connected via `isConnected[i][j]`. Find the number of provinces (connected components).",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Standard connected-components counting, but neighbors are looked up via the matrix.",
        "optimized": {
            "explanation": "DFS over an adjacency matrix.",
            "code": r'''
def find_circle_num(is_connected):
    n = len(is_connected)
    visited = [False] * n
    def dfs(u):
        visited[u] = True
        for v in range(n):
            if is_connected[u][v] and not visited[v]:
                dfs(v)
    count = 0
    for i in range(n):
        if not visited[i]:
            count += 1
            dfs(i)
    return count
''',
            "complexity": "Time O(n²), space O(n).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "DFS over matrix; count launches.",
    },
    {
        "id": "connected-components-undirected",
        "title": "Connected Components in an Undirected Graph",
        "step_id": 15,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["graph", "dfs", "bfs"],
        "what_this_teaches": "Same as connected-components but on an edge-list input.",
        "pattern": "Build adj + count components.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["connected-components"],
        "next_problems": ["rotten-oranges"],
        "resources": [_SHEET],
        "understanding": "Given N vertices and a list of edges, count connected components.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Build adjacency list from edges, then standard connected components.",
        "optimized": {
            "explanation": "—",
            "code": r'''
from collections import defaultdict
def count_components_from_edges(n, edges):
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    visited = [False] * n
    count = 0
    def dfs(u):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]: dfs(v)
    for u in range(n):
        if not visited[u]:
            count += 1; dfs(u)
    return count
''',
            "complexity": "Time O(V + E).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Build adjacency, then connected-components.",
    },
    {
        "id": "rotten-oranges",
        "title": "Rotting Oranges",
        "step_id": 15,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["graph", "bfs", "multi-source"],
        "what_this_teaches": "Multi-source BFS on a grid: seed the queue with *all* sources at distance 0, then expand layer by layer.",
        "pattern": "Multi-source BFS.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["graph-bfs"],
        "next_problems": ["flood-fill", "distance-of-nearest-1"],
        "resources": [
            _lc(994, "rotting-oranges"),
            _SHEET,
        ],
        "understanding": r'''
A 2-D grid contains empty cells (0), fresh oranges (1), and rotten
oranges (2). Each minute, every fresh orange adjacent to a rotten one
turns rotten. Return the minimum minutes until no fresh oranges remain
— or -1 if impossible.
''',
        "brute_force": {"explanation": "Simulate minute by minute, scanning the whole grid each step → O(m·n · steps).", "code": "", "complexity": "—"},
        "thought_process": r'''
**Multi-source BFS.** Initialize a queue with *all* rotten orange
positions at distance 0. BFS outward — each layer increments time by 1.
After BFS, check if any fresh orange remains.
''',
        "optimized": {
            "explanation": "Multi-source BFS.",
            "code": r'''
from collections import deque

def oranges_rotting(grid):
    m, n = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 2: q.append((i, j, 0))
            elif grid[i][j] == 1: fresh += 1
    minutes = 0
    while q:
        i, j, t = q.popleft()
        minutes = max(minutes, t)
        for di, dj in ((1,0),(-1,0),(0,1),(0,-1)):
            ni, nj = i+di, j+dj
            if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 1:
                grid[ni][nj] = 2
                fresh -= 1
                q.append((ni, nj, t+1))
    return -1 if fresh > 0 else minutes
''',
            "complexity": "Time O(m·n), space O(m·n).",
        },
        "deep_concept": "Multi-source BFS is the trick whenever you have multiple starting points and want the minimum distance from *any* source.",
        "confusion_notes": [
            {
                "question": "Why not run BFS from each rotten orange separately?",
                "answer": "Because then each orange might take O(m·n) and we'd do it K times. Multi-source BFS does the union in one pass with the same complexity as a single BFS.",
            },
        ],
        "summary": "Seed BFS with all sources at distance 0; expand layer by layer; track max time.",
    },
    {
        "id": "flood-fill",
        "title": "Flood Fill",
        "step_id": 15,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["graph", "dfs", "grid"],
        "what_this_teaches": "Grid-based DFS to spread a value through a 4-connected region.",
        "pattern": "Grid DFS.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["graph-dfs"],
        "next_problems": ["number-of-distinct-islands"],
        "resources": [
            _lc(733, "flood-fill"),
            _SHEET,
        ],
        "understanding": "Given an image (2-D grid), starting pixel, and a new color, recolor the connected region of same-colored pixels.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "DFS from the start, recoloring as you go. Stop when neighbor's color differs.",
        "optimized": {
            "explanation": "DFS with in-place recoloring.",
            "code": r'''
def flood_fill(image, sr, sc, color):
    orig = image[sr][sc]
    if orig == color: return image
    m, n = len(image), len(image[0])
    def dfs(i, j):
        if not (0 <= i < m and 0 <= j < n) or image[i][j] != orig:
            return
        image[i][j] = color
        for di, dj in ((1,0),(-1,0),(0,1),(0,-1)):
            dfs(i+di, j+dj)
    dfs(sr, sc)
    return image
''',
            "complexity": "Time O(m·n), space O(m·n).",
        },
        "deep_concept": "In-place recoloring serves as the visited marker — once a pixel is recolored, the original-color check fails for subsequent visits.",
        "confusion_notes": [],
        "summary": "DFS, recolor in place. The recolor is the visited mark.",
    },
    {
        "id": "cycle-undirected-bfs",
        "title": "Cycle Detection in Undirected Graph — BFS",
        "step_id": 15,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["graph", "bfs"],
        "what_this_teaches": "Track the parent during BFS; if we encounter a visited neighbor that's not the parent, there's a cycle.",
        "pattern": "BFS with parent tracking.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["graph-bfs"],
        "next_problems": ["cycle-undirected-dfs"],
        "resources": [
            {"label": "GFG — Detect cycle undirected (BFS)", "url": "https://www.geeksforgeeks.org/detect-cycle-in-an-undirected-graph-using-bfs/"},
            _SHEET,
        ],
        "understanding": "Detect whether an undirected graph contains a cycle.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "BFS from each unvisited vertex; in the queue store (node, parent); if you see a visited neighbor that's not the parent, return True.",
        "optimized": {
            "explanation": "BFS with parent.",
            "code": r'''
from collections import deque
def has_cycle_undirected_bfs(V, adj):
    visited = [False] * V
    def bfs(src):
        q = deque([(src, -1)])
        visited[src] = True
        while q:
            u, parent = q.popleft()
            for v in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    q.append((v, u))
                elif v != parent:
                    return True
        return False
    for s in range(V):
        if not visited[s] and bfs(s):
            return True
    return False
''',
            "complexity": "Time O(V + E), space O(V).",
        },
        "deep_concept": "In an undirected DFS/BFS tree, a *back edge* (to a non-parent already-visited vertex) signals a cycle.",
        "confusion_notes": [
            {
                "question": "Why check `v != parent`?",
                "answer": "Because the undirected edge from u to its parent is stored as both (u, parent) and (parent, u) in the adjacency list. Without the check, we'd flag every edge as a cycle.",
            },
        ],
        "summary": "BFS storing parent; a visited non-parent neighbor = cycle.",
    },
    {
        "id": "cycle-undirected-dfs",
        "title": "Cycle Detection in Undirected Graph — DFS",
        "step_id": 15,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["graph", "dfs"],
        "what_this_teaches": "Same idea as BFS variant — back edge = cycle — implemented recursively.",
        "pattern": "DFS with parent tracking.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["cycle-undirected-bfs"],
        "next_problems": ["bipartite-bfs"],
        "resources": [
            {"label": "GFG — Detect cycle undirected (DFS)", "url": "https://www.geeksforgeeks.org/detect-cycle-undirected-graph/"},
            _SHEET,
        ],
        "understanding": "Same as the BFS version — detect a cycle in an undirected graph.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Recursive DFS carrying the parent index.",
        "optimized": {
            "explanation": "Recursive DFS with parent.",
            "code": r'''
def has_cycle_undirected_dfs(V, adj):
    visited = [False] * V
    def dfs(u, parent):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                if dfs(v, u): return True
            elif v != parent:
                return True
        return False
    for u in range(V):
        if not visited[u] and dfs(u, -1):
            return True
    return False
''',
            "complexity": "Time O(V + E), space O(V).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "DFS with parent; back edge to non-parent = cycle.",
    },
    {
        "id": "distance-of-nearest-1",
        "title": "Distance of Nearest 1 (or 0)",
        "step_id": 15,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["graph", "bfs", "multi-source"],
        "what_this_teaches": "Multi-source BFS to compute distance from *any* source.",
        "pattern": "Multi-source BFS.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["rotten-oranges"],
        "next_problems": ["surrounded-regions"],
        "resources": [
            _lc(542, "01-matrix"),
            _SHEET,
        ],
        "understanding": "Given a 0/1 matrix, return the distance from each cell to the nearest 0.",
        "brute_force": {"explanation": "BFS from each cell → O((mn)²). Too slow.", "code": "", "complexity": "—"},
        "thought_process": "Multi-source BFS from *all* the zeros at once.",
        "optimized": {
            "explanation": "Multi-source BFS.",
            "code": r'''
from collections import deque
def update_matrix(mat):
    m, n = len(mat), len(mat[0])
    INF = float('inf')
    dist = [[INF]*n for _ in range(m)]
    q = deque()
    for i in range(m):
        for j in range(n):
            if mat[i][j] == 0:
                dist[i][j] = 0
                q.append((i, j))
    while q:
        i, j = q.popleft()
        for di, dj in ((1,0),(-1,0),(0,1),(0,-1)):
            ni, nj = i+di, j+dj
            if 0 <= ni < m and 0 <= nj < n and dist[ni][nj] > dist[i][j] + 1:
                dist[ni][nj] = dist[i][j] + 1
                q.append((ni, nj))
    return dist
''',
            "complexity": "Time O(m·n), space O(m·n).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Multi-source BFS seeded by zeros; each cell's first-visit distance = its answer.",
    },
    {
        "id": "surrounded-regions",
        "title": "Surrounded Regions",
        "step_id": 15,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["graph", "dfs", "grid"],
        "what_this_teaches": "Mark all 'safe' regions (touching the boundary) first, then flip the rest.",
        "pattern": "Boundary-rooted DFS.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["flood-fill"],
        "next_problems": ["number-of-enclaves"],
        "resources": [
            _lc(130, "surrounded-regions"),
            _SHEET,
        ],
        "understanding": "Flip every 'O' that is fully surrounded by 'X' to 'X'. An 'O' connected to the boundary is *not* flipped.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Walk the boundary; from every boundary 'O', DFS marking those reachable as 'safe' (with a temporary marker '#'). Then flip remaining 'O' to 'X' and '#' back to 'O'.",
        "optimized": {
            "explanation": "Boundary-rooted DFS.",
            "code": r'''
def solve(board):
    if not board: return
    m, n = len(board), len(board[0])
    def dfs(i, j):
        if not (0 <= i < m and 0 <= j < n) or board[i][j] != 'O':
            return
        board[i][j] = '#'
        for di, dj in ((1,0),(-1,0),(0,1),(0,-1)):
            dfs(i+di, j+dj)
    for i in range(m):
        dfs(i, 0); dfs(i, n-1)
    for j in range(n):
        dfs(0, j); dfs(m-1, j)
    for i in range(m):
        for j in range(n):
            if board[i][j] == 'O':
                board[i][j] = 'X'
            elif board[i][j] == '#':
                board[i][j] = 'O'
''',
            "complexity": "Time O(m·n).",
        },
        "deep_concept": "Inverted DFS: instead of finding what's *enclosed*, find what's *connected to the boundary* (safe). Flip the complement.",
        "confusion_notes": [],
        "summary": "DFS from every boundary 'O' marking safe regions; then flip non-safe to 'X'.",
    },
    {
        "id": "number-of-enclaves",
        "title": "Number of Enclaves",
        "step_id": 15,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["graph", "dfs", "grid"],
        "what_this_teaches": "Same boundary-rooted DFS technique applied to counting.",
        "pattern": "Boundary-rooted DFS.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["surrounded-regions"],
        "next_problems": ["number-of-distinct-islands"],
        "resources": [
            _lc(1020, "number-of-enclaves"),
            _SHEET,
        ],
        "understanding": "Count land cells (1) that cannot reach the boundary.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "DFS from all boundary 1s and mark them as visited; count remaining unvisited 1s.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def num_enclaves(grid):
    m, n = len(grid), len(grid[0])
    def dfs(i, j):
        if not (0 <= i < m and 0 <= j < n) or grid[i][j] != 1:
            return
        grid[i][j] = 0
        for di, dj in ((1,0),(-1,0),(0,1),(0,-1)):
            dfs(i+di, j+dj)
    for i in range(m):
        dfs(i, 0); dfs(i, n-1)
    for j in range(n):
        dfs(0, j); dfs(m-1, j)
    return sum(row.count(1) for row in grid)
''',
            "complexity": "Time O(m·n).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "DFS from boundary 1s, zero them out; remaining 1s = enclave cells.",
    },
    {
        "id": "number-of-distinct-islands",
        "title": "Number of Distinct Islands",
        "step_id": 15,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["graph", "dfs", "hashing"],
        "what_this_teaches": "Canonicalize island shape (normalize to a tuple) and hash.",
        "pattern": "Shape hashing.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["flood-fill"],
        "next_problems": ["bipartite-bfs"],
        "resources": [
            {"label": "LeetCode 694 — Number of Distinct Islands", "url": "https://leetcode.com/problems/number-of-distinct-islands/"},
            _SHEET,
        ],
        "understanding": "Count distinct *shapes* of islands (two islands are the same shape iff one can be translated to match the other).",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "For each island, DFS and record visit positions *relative to the start*. The set of relative offsets uniquely identifies the shape.",
        "optimized": {
            "explanation": "DFS + frozenset of relative positions.",
            "code": r'''
def num_distinct_islands(grid):
    m, n = len(grid), len(grid[0])
    shapes = set()
    def dfs(i, j, oi, oj, shape):
        if not (0 <= i < m and 0 <= j < n) or grid[i][j] != 1:
            return
        grid[i][j] = 0
        shape.append((i - oi, j - oj))
        for di, dj in ((1,0),(-1,0),(0,1),(0,-1)):
            dfs(i+di, j+dj, oi, oj, shape)
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                shape = []
                dfs(i, j, i, j, shape)
                shapes.add(frozenset(shape))
    return len(shapes)
''',
            "complexity": "Time O(m·n).",
        },
        "deep_concept": "Translation-invariant shape comparison via canonical-form hashing is a recurring trick.",
        "confusion_notes": [
            {
                "question": "Why frozenset and not tuple?",
                "answer": "If we want to allow translation only, a *sorted tuple* or frozenset of positions works. Tuples in DFS-visit order would differ if DFS visits cells differently. To allow rotation/reflection, additional canonicalization is needed.",
            },
        ],
        "summary": "DFS recording relative positions; frozenset of offsets = shape signature.",
    },
    {
        "id": "bipartite-bfs",
        "title": "Bipartite Check — BFS",
        "step_id": 15,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["graph", "bfs", "coloring"],
        "what_this_teaches": "Two-color the graph BFS-style; conflict = not bipartite.",
        "pattern": "BFS 2-coloring.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["graph-bfs"],
        "next_problems": ["bipartite-dfs"],
        "resources": [
            _lc(785, "is-graph-bipartite"),
            _SHEET,
        ],
        "understanding": "Return True iff vertices can be split into two groups such that every edge crosses groups.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "BFS from each unvisited vertex, assigning alternating colors; conflict = not bipartite.",
        "optimized": {
            "explanation": "BFS 2-coloring.",
            "code": r'''
from collections import deque
def is_bipartite(graph):
    n = len(graph)
    color = [-1] * n
    for s in range(n):
        if color[s] != -1: continue
        color[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]:
                    return False
    return True
''',
            "complexity": "Time O(V + E), space O(V).",
        },
        "deep_concept": "Bipartiteness = no odd cycle. BFS detects odd cycles because two BFS layers an odd distance apart would receive the same color.",
        "confusion_notes": [],
        "summary": "BFS alternating colors; same-color edge = not bipartite.",
    },
    {
        "id": "bipartite-dfs",
        "title": "Bipartite Check — DFS",
        "step_id": 15,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["graph", "dfs", "coloring"],
        "what_this_teaches": "Same problem via recursive DFS.",
        "pattern": "DFS 2-coloring.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["bipartite-bfs"],
        "next_problems": ["cycle-directed-dfs"],
        "resources": [_SHEET],
        "understanding": "—",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Recursive DFS, passing the expected color.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def is_bipartite_dfs(graph):
    n = len(graph)
    color = [-1] * n
    def dfs(u, c):
        color[u] = c
        for v in graph[u]:
            if color[v] == -1:
                if not dfs(v, 1 - c): return False
            elif color[v] == c:
                return False
        return True
    for s in range(n):
        if color[s] == -1 and not dfs(s, 0):
            return False
    return True
''',
            "complexity": "Time O(V + E).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "DFS assigning alternating colors; same-color edge = fail.",
    },
    {
        "id": "cycle-directed-dfs",
        "title": "Cycle Detection in Directed Graph — DFS",
        "step_id": 15,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["graph", "dfs", "cycle"],
        "what_this_teaches": "Maintain a *recursion stack* in addition to visited. Back edge = vertex in recursion stack.",
        "pattern": "DFS with recursion-stack marker.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["graph-dfs"],
        "next_problems": ["topo-sort-dfs"],
        "resources": [
            {"label": "GFG — Detect cycle in directed graph", "url": "https://www.geeksforgeeks.org/detect-cycle-in-a-graph/"},
            _SHEET,
        ],
        "understanding": "Detect whether a directed graph contains a cycle.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": r'''
In an undirected graph, a back edge to any non-parent visited vertex
indicates a cycle. In a *directed* graph, that doesn't work — we need
to distinguish between vertices in the *current DFS path* (back edges
= cycle) and vertices in *finished* branches (cross/forward edges, no
cycle).

Use two flags: `visited` (ever-touched) and `on_stack` (currently in
DFS path). A neighbor `v` with `on_stack[v] == True` means a back edge
→ cycle.
''',
        "optimized": {
            "explanation": "DFS with recursion-stack flag.",
            "code": r'''
def is_cyclic_directed(V, adj):
    visited = [False] * V
    on_stack = [False] * V
    def dfs(u):
        visited[u] = True
        on_stack[u] = True
        for v in adj[u]:
            if not visited[v]:
                if dfs(v): return True
            elif on_stack[v]:
                return True
        on_stack[u] = False
        return False
    for u in range(V):
        if not visited[u] and dfs(u):
            return True
    return False
''',
            "complexity": "Time O(V + E), space O(V).",
        },
        "deep_concept": "The 'three-color' DFS (white/gray/black) is essentially the same — `gray` ≈ on_stack, `black` ≈ done.",
        "confusion_notes": [
            {
                "question": "Why does undirected cycle detection not need `on_stack`?",
                "answer": "Because in an undirected graph, every back edge to a visited (non-parent) vertex is a cycle. In a directed graph, edges going to *already finished* vertices don't form a cycle — only edges to vertices still on the current DFS path do.",
            },
        ],
        "summary": "DFS with both visited and on_stack flags. Edge to on_stack vertex = cycle.",
    },

    # ==================================================================
    # TOPO SORT
    # ==================================================================
    {
        "id": "topo-sort-dfs",
        "title": "Topological Sort — DFS (Postorder)",
        "step_id": 15,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["graph", "topo", "dfs"],
        "what_this_teaches": "Topological order = reverse postorder of DFS on a DAG.",
        "pattern": "Postorder DFS + reverse.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["cycle-directed-dfs"],
        "next_problems": ["kahns-algorithm", "course-schedule-i"],
        "resources": [
            {"label": "GFG — Topological Sort", "url": "https://www.geeksforgeeks.org/topological-sorting/"},
            _SHEET,
        ],
        "understanding": r'''
For a DAG, return a linear ordering of vertices such that for every
directed edge `u → v`, u comes before v.
''',
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "DFS, recording each vertex in postorder. Reverse the postorder list. The reversed list is a valid topological order.",
        "optimized": {
            "explanation": "DFS-based topo sort.",
            "code": r'''
def topo_sort_dfs(V, adj):
    visited = [False] * V
    order = []
    def dfs(u):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]: dfs(v)
        order.append(u)        # postorder
    for u in range(V):
        if not visited[u]: dfs(u)
    return order[::-1]         # reverse
''',
            "complexity": "Time O(V + E).",
        },
        "deep_concept": "Postorder of DFS visits children before parents. Reversing makes parents come before children — exactly the topological invariant.",
        "confusion_notes": [
            {
                "question": "What if the graph isn't a DAG?",
                "answer": "DFS-based topo sort still produces *some* ordering, but it won't satisfy the topological property (because cycles can't be linearized). For safety, detect cycles first.",
            },
        ],
        "summary": "DFS postorder; reverse the list. Only valid on DAGs.",
    },
    {
        "id": "kahns-algorithm",
        "title": "Kahn's Algorithm (Topological Sort via BFS)",
        "step_id": 15,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["graph", "topo", "bfs"],
        "what_this_teaches": "Process vertices with in-degree 0 first; decrement neighbors' in-degrees; queue them when they hit 0.",
        "pattern": "BFS over in-degree zero.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["topo-sort-dfs"],
        "next_problems": ["course-schedule-ii"],
        "resources": [
            {"label": "Wikipedia — Topological sorting", "url": "https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm"},
            _SHEET,
        ],
        "understanding": "Compute in-degrees; queue all with in-degree 0; pop one, append to result, decrement its neighbors, queue any that hit 0.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "—",
        "optimized": {
            "explanation": "Kahn's BFS.",
            "code": r'''
from collections import deque
def kahn(V, adj):
    indeg = [0] * V
    for u in range(V):
        for v in adj[u]: indeg[v] += 1
    q = deque(u for u in range(V) if indeg[u] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == V else []   # empty = cycle exists
''',
            "walkthrough": r'''
**Kahn's Algorithm** for **topological sort**. *O(V + E)*.
The BFS-based topo sort, named after A. B. Kahn (1962).

The problem: given a **DAG (directed acyclic graph)**, output
the vertices in an order such that every directed edge
`u → v` appears with `u` before `v`. This is a **topological
ordering**.

**The Kahn's algorithm idea**: a vertex with **in-degree 0**
has no prerequisites — it can come first in the topo order.
Output it, then "remove" it from the graph (decrement
in-degrees of its neighbors). Repeat.

**`from collections import deque`** — Queue for BFS.

**`def kahn(V, adj):`** — Takes the vertex count and
adjacency list. Returns a topo ordering, or an empty list if
the graph has a cycle.

**`indeg = [0] * V`** — Initialize an in-degree array.

**`for u in range(V): for v in adj[u]: indeg[v] += 1`** —
Compute in-degrees by walking every edge.

**`q = deque(u for u in range(V) if indeg[u] == 0)`** —
**Seed the queue with all in-degree-0 vertices.** These are
the "sources" — vertices with no prerequisites.

**`order = []`** — Accumulator for the topo order.

**`while q:`** — Process while the queue is non-empty.

**`u = q.popleft()`** — Take the next ready vertex.

**`order.append(u)`** — Output it.

**`for v in adj[u]:`** — For each successor `v` of `u`...

**`indeg[v] -= 1`** — Removing `u` reduces `v`'s in-degree
by 1. (Symbolically. We don't actually modify the graph.)

**`if indeg[v] == 0: q.append(v)`** — If `v` now has no
remaining prerequisites, it's ready to be output. Enqueue it.

**`return order if len(order) == V else []`** — **Cycle
detection.** If we managed to output every vertex, we have a
valid topo order. If `len(order) < V`, some vertices were
never enqueued — they have a non-zero in-degree even after
processing everyone else. That means they're in a **cycle**,
where each node waits for the next.

**Why does this work?**

Topological order means: for every directed edge `u → v`, `u`
must come **before** `v`. Equivalently, every node must come
**after** all of its prerequisites.

Kahn's algorithm enforces this directly: a node is only
output when all its prerequisites have been output (in-degree
reaches 0).

**Trace on:**
```
edges: 5→0, 5→2, 4→0, 4→1, 2→3, 3→1
```
```
indeg = [2, 2, 1, 1, 0, 0].
q = [4, 5]. order = [].

Pop 4: order=[4]. Neighbors 0,1. indeg[0]=1, indeg[1]=1.
Pop 5: order=[4,5]. Neighbors 0,2. indeg[0]=0 → enqueue 0. indeg[2]=0 → enqueue 2.
q = [0, 2].
Pop 0: order=[4,5,0]. No neighbors.
Pop 2: order=[4,5,0,2]. Neighbor 3. indeg[3]=0 → enqueue 3.
q = [3].
Pop 3: order=[4,5,0,2,3]. Neighbor 1. indeg[1]=0 → enqueue 1.
q = [1].
Pop 1: order=[4,5,0,2,3,1]. No neighbors.
q empty.

len(order) = 6 = V. Return [4, 5, 0, 2, 3, 1].
```

Valid topo order (one of several possible).

**Why is this O(V + E)?**

Each vertex is enqueued and processed once: *O(V)*. Each
edge is examined once when its source is processed: *O(E)*.
Total *O(V + E)*.

**Properties:**
- **Time**: *O(V + E)*.
- **Space**: *O(V)* for the queue and indegree array.

**Cycle detection via Kahn:**

If the graph has a cycle, the vertices in the cycle never
have in-degree 0 (each is the prerequisite of another in the
cycle). They're never enqueued, never output. `len(order)`
ends up less than V.

This is one of the **cleanest cycle detection algorithms**
for directed graphs.

**Applications:**
- **Course scheduling**: find an order to take courses
  satisfying prerequisites.
- **Build systems** (make, cargo, bazel): compile files in
  dependency order.
- **Task scheduling** with dependencies.
- **Linker symbol resolution**.
- **Spreadsheet recalculation**: evaluate cells in dependency
  order.

Kahn's algorithm is **simpler to understand** than DFS-based
topo sort and is the recommended teaching version.

**Alternative**: DFS-based topo sort. Do post-order DFS;
reverse the post-order. Also *O(V + E)*. Use DFS when:
- The graph is sparse and DFS is natural.
- You're already doing DFS for other reasons.

Both versions appear in interviews.
''',
            "complexity": "Time O(V + E).",
        },
        "deep_concept": "Kahn's also detects cycles: if final `len(order) != V`, the graph has a cycle (some vertex never reached in-degree 0).",
        "confusion_notes": [],
        "summary": "BFS over in-degree zero vertices; pop, output, decrement neighbors.",
    },
    {
        "id": "cycle-directed-bfs",
        "title": "Cycle Detection in Directed Graph — Kahn's BFS",
        "step_id": 15,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["graph", "topo", "cycle"],
        "what_this_teaches": "Kahn's algorithm doubles as a cycle detector.",
        "pattern": "Kahn's algorithm.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["kahns-algorithm"],
        "next_problems": ["course-schedule-i"],
        "resources": [_SHEET],
        "understanding": "Detect a cycle in a directed graph via Kahn's algorithm.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Run Kahn's; if not all vertices appear in the topo order, there's a cycle.",
        "optimized": {
            "explanation": "—",
            "code": r'''
from collections import deque
def has_cycle_kahn(V, adj):
    indeg = [0] * V
    for u in range(V):
        for v in adj[u]: indeg[v] += 1
    q = deque(u for u in range(V) if indeg[u] == 0)
    count = 0
    while q:
        u = q.popleft(); count += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return count != V
''',
            "complexity": "Time O(V + E).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Run Kahn's; if processed < V, there's a cycle.",
    },
    {
        "id": "course-schedule-i",
        "title": "Course Schedule",
        "step_id": 15,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["graph", "topo", "cycle"],
        "what_this_teaches": "Course prerequisites form a directed graph; can we finish? = is it a DAG?",
        "pattern": "Cycle detection on directed graph.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["cycle-directed-bfs"],
        "next_problems": ["course-schedule-ii"],
        "resources": [
            _lc(207, "course-schedule"),
            _SHEET,
        ],
        "understanding": "n courses, prerequisites given as (a, b) meaning b must be taken before a. Can you finish all courses?",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Detect a cycle in the prereq graph. If acyclic → True.",
        "optimized": {
            "explanation": "—",
            "code": r'''
from collections import defaultdict, deque
def can_finish(num_courses, prerequisites):
    adj = defaultdict(list)
    indeg = [0] * num_courses
    for a, b in prerequisites:
        adj[b].append(a); indeg[a] += 1
    q = deque(u for u in range(num_courses) if indeg[u] == 0)
    done = 0
    while q:
        u = q.popleft(); done += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0: q.append(v)
    return done == num_courses
''',
            "complexity": "Time O(V + E).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Cycle check via Kahn's. Return done == n.",
    },
    {
        "id": "course-schedule-ii",
        "title": "Course Schedule II",
        "step_id": 15,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["graph", "topo"],
        "what_this_teaches": "Return the topological order (one valid completion sequence).",
        "pattern": "Kahn's outputs the order.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["course-schedule-i"],
        "next_problems": ["eventual-safe-states"],
        "resources": [
            _lc(210, "course-schedule-ii"),
            _SHEET,
        ],
        "understanding": "Same setup, but return a valid order (or empty if impossible).",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Same as Course Schedule, return the order.",
        "optimized": {
            "explanation": "—",
            "code": r'''
from collections import defaultdict, deque
def find_order(num_courses, prerequisites):
    adj = defaultdict(list)
    indeg = [0] * num_courses
    for a, b in prerequisites:
        adj[b].append(a); indeg[a] += 1
    q = deque(u for u in range(num_courses) if indeg[u] == 0)
    order = []
    while q:
        u = q.popleft(); order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0: q.append(v)
    return order if len(order) == num_courses else []
''',
            "complexity": "Time O(V + E).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Kahn's; return the topo order or empty list on cycle.",
    },
    {
        "id": "eventual-safe-states",
        "title": "Find Eventual Safe States",
        "step_id": 15,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["graph", "topo", "cycle"],
        "what_this_teaches": "A vertex is *safe* iff every path from it reaches a terminal vertex. Reverse the graph, then Kahn's.",
        "pattern": "Reverse + Kahn's.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["course-schedule-ii"],
        "next_problems": ["alien-dictionary"],
        "resources": [
            _lc(802, "find-eventual-safe-states"),
            _SHEET,
        ],
        "understanding": "A node is safe iff all paths from it terminate (i.e., not stuck in a cycle).",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Reverse all edges. A vertex with no outgoing edges in the original = no incoming in the reverse = a 'source' in the reverse graph. Kahn's on the reverse gives all vertices not part of (and not reaching) a cycle. Sort the result.",
        "optimized": {
            "explanation": "Reverse + Kahn's.",
            "code": r'''
from collections import defaultdict, deque
def eventual_safe_nodes(graph):
    n = len(graph)
    rev = defaultdict(list)
    indeg = [0] * n
    for u in range(n):
        for v in graph[u]:
            rev[v].append(u)
            indeg[u] += 1
    q = deque(u for u in range(n) if indeg[u] == 0)
    safe = []
    while q:
        u = q.popleft(); safe.append(u)
        for v in rev[u]:
            indeg[v] -= 1
            if indeg[v] == 0: q.append(v)
    return sorted(safe)
''',
            "complexity": "Time O(V + E).",
        },
        "deep_concept": "Reversing converts 'reaches a terminal' into 'is reached by a source' which is exactly what Kahn's processes.",
        "confusion_notes": [],
        "summary": "Reverse edges; run Kahn's; return sorted result.",
    },
    {
        "id": "alien-dictionary",
        "title": "Alien Dictionary",
        "step_id": 15,
        "lecture_id": 3,
        "difficulty": "hard",
        "tags": ["graph", "topo"],
        "what_this_teaches": "Build a precedence graph from adjacent word pairs; topo-sort it.",
        "pattern": "Pairwise comparison → topo sort.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["course-schedule-ii"],
        "next_problems": ["shortest-path-undirected-unit"],
        "resources": [
            {"label": "LeetCode 269 — Alien Dictionary", "url": "https://leetcode.com/problems/alien-dictionary/"},
            _SHEET,
        ],
        "understanding": "Given a list of words sorted in alien lexicographic order, derive the order of letters.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "For each adjacent word pair (w1, w2), find the first differing char; w1's char precedes w2's. Build a graph and topo sort it.",
        "optimized": {
            "explanation": "Build edges + Kahn's.",
            "code": r'''
from collections import defaultdict, deque
def alien_order(words):
    adj = defaultdict(set)
    indeg = {c: 0 for w in words for c in w}
    for w1, w2 in zip(words, words[1:]):
        for a, b in zip(w1, w2):
            if a != b:
                if b not in adj[a]:
                    adj[a].add(b); indeg[b] += 1
                break
        else:
            if len(w1) > len(w2):
                return ""           # invalid: "abc" before "ab"
    q = deque(c for c, d in indeg.items() if d == 0)
    out = []
    while q:
        c = q.popleft(); out.append(c)
        for d in adj[c]:
            indeg[d] -= 1
            if indeg[d] == 0: q.append(d)
    return ''.join(out) if len(out) == len(indeg) else ""
''',
            "complexity": "Time O(total chars + edges).",
        },
        "deep_concept": "Many ordering problems reduce to topo sort once you identify the pairwise constraints.",
        "confusion_notes": [],
        "summary": "Pairwise compare → edges → Kahn's. Watch out for invalid prefix cases.",
    },

    # ==================================================================
    # SHORTEST PATH
    # ==================================================================
    {
        "id": "shortest-path-undirected-unit",
        "title": "Shortest Path in Undirected Graph (Unit Weights)",
        "step_id": 15,
        "lecture_id": 4,
        "difficulty": "easy",
        "tags": ["graph", "bfs"],
        "what_this_teaches": "BFS gives shortest path on unweighted graphs.",
        "pattern": "BFS.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["graph-bfs"],
        "next_problems": ["shortest-path-dag", "dijkstra"],
        "resources": [_SHEET],
        "understanding": "Compute shortest distance from a source to every other vertex in an undirected, unweighted graph.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "—",
        "optimized": {
            "explanation": "BFS layered distances.",
            "code": r'''
from collections import deque
def shortest_path_unit(V, adj, src):
    dist = [-1] * V
    dist[src] = 0
    q = deque([src])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist
''',
            "complexity": "Time O(V + E).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "BFS; first time we visit v gives shortest distance.",
    },
    {
        "id": "shortest-path-dag",
        "title": "Shortest Path in DAG",
        "step_id": 15,
        "lecture_id": 4,
        "difficulty": "medium",
        "tags": ["graph", "topo", "shortest-path"],
        "what_this_teaches": "Topological order + relaxation = shortest path on a DAG even with negative weights.",
        "pattern": "Topo sort + relax in order.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["topo-sort-dfs"],
        "next_problems": ["dijkstra"],
        "resources": [
            {"label": "GFG — Shortest path in DAG", "url": "https://www.geeksforgeeks.org/shortest-path-for-directed-acyclic-graphs/"},
            _SHEET,
        ],
        "understanding": "Compute shortest distances from a source in a DAG with weighted edges.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Topo sort; process vertices in that order; for each vertex u, relax all outgoing edges. Since u comes before its descendants, by the time we relax u's edges, u's distance is finalized.",
        "optimized": {
            "explanation": "Topo + relax.",
            "code": r'''
def shortest_path_dag(V, adj_with_weights, src):
    # adj_with_weights[u] = list of (v, w)
    visited = [False] * V
    order = []
    def dfs(u):
        visited[u] = True
        for v, _ in adj_with_weights[u]:
            if not visited[v]: dfs(v)
        order.append(u)
    for u in range(V):
        if not visited[u]: dfs(u)
    order.reverse()
    INF = float('inf')
    dist = [INF] * V
    dist[src] = 0
    for u in order:
        if dist[u] == INF: continue
        for v, w in adj_with_weights[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist
''',
            "complexity": "Time O(V + E).",
        },
        "deep_concept": "Topo-order relaxation works because all predecessors are processed before their successors.",
        "confusion_notes": [],
        "summary": "Topo sort + relax edges in that order. O(V+E), works with negative weights.",
    },
    {
        "id": "dijkstra",
        "title": "Dijkstra's Shortest Path Algorithm",
        "step_id": 15,
        "lecture_id": 4,
        "difficulty": "medium",
        "tags": ["graph", "shortest-path", "heap"],
        "what_this_teaches": "Greedy: repeatedly extract the unvisited vertex with the smallest tentative distance, relax its neighbors.",
        "pattern": "Min-heap of (dist, vertex) tuples.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["heap-introduction"],
        "next_problems": ["shortest-path-weighted-undirected", "path-min-effort"],
        "resources": [
            {"label": "Wikipedia — Dijkstra's algorithm", "url": "https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm"},
            _SHEET,
        ],
        "understanding": r'''
Compute single-source shortest paths in a graph with **non-negative**
edge weights.

**Algorithm:** maintain a min-heap of (tentative_distance, vertex).
Repeatedly pop the smallest; if it's the first pop for that vertex,
relax all outgoing edges, pushing updated distances.
''',
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": r'''
**Why does greedy work?** Because once we pop vertex u from the
priority queue, no shorter path to u can exist — every other path would
have to go through some unvisited vertex with a current distance
strictly larger than dist[u] (heap ordering), and edge weights are
non-negative, so the path can only grow.
''',
        "optimized": {
            "explanation": "Min-heap Dijkstra.",
            "code": r'''
import heapq
def dijkstra(V, adj, src):
    INF = float('inf')
    dist = [INF] * V
    dist[src] = 0
    h = [(0, src)]
    while h:
        d, u = heapq.heappop(h)
        if d > dist[u]: continue       # stale entry
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(h, (nd, v))
    return dist
''',
            "walkthrough": r'''
**Dijkstra's algorithm** — one of the most famous algorithms
in computer science. Computes shortest paths from a single
source to all vertices in a graph with **non-negative edge
weights**. *O((V + E) log V)* with a min-heap.

**`import heapq`** — Python's min-heap. We'll use it to
always extract the next "closest unfinalized" vertex.

**`def dijkstra(V, adj, src):`** — Takes the number of
vertices, an adjacency list `adj[u] = [(v, w), ...]` of
(neighbor, edge weight) pairs, and the source vertex.
Returns an array of shortest distances from `src`.

**`INF = float('inf')`** — A "haven't reached yet" sentinel.

**`dist = [INF] * V`** — Distance array, all infinity
initially. By the end, `dist[u]` will hold the shortest
distance from `src` to `u`.

**`dist[src] = 0`** — Source is at distance 0 from itself.

**`h = [(0, src)]`** — Min-heap initialized with `(0, src)`.
We store tuples `(distance, vertex)` so the heap orders by
distance ascending. The smallest entry is always the next
vertex to finalize.

**`while h:`** — Continue while there's something to process.

**`d, u = heapq.heappop(h)`** — Extract the vertex with the
**smallest tentative distance**. This is the **greedy step**:
Dijkstra claims that this vertex's distance is now **final**
— no shorter path can exist (assuming non-negative weights).

**`if d > dist[u]: continue`** — **Stale entry skip.** The
heap might contain multiple entries for the same vertex (we
push every time we improve a distance). The first time we pop
`u`, the distance is correct. Later pops for `u` have stale,
larger distances — skip them.

The reason we don't bother removing old entries when we add
new ones: removing from a heap is *O(n)*. It's cheaper to
just push duplicates and skip when popping. This is called
**lazy deletion**.

**`for v, w in adj[u]:`** — For each neighbor `v` of `u`, with
edge weight `w`...

**`nd = d + w`** — Compute the candidate new distance to `v`:
distance to `u` plus the edge weight.

**`if nd < dist[v]:`** — **Relaxation step.** If this path is
shorter than any path we've found to `v` so far...

**`dist[v] = nd`** — Update the distance.

**`heapq.heappush(h, (nd, v))`** — Push the new (distance,
vertex) onto the heap for later processing.

**`return dist`** — All distances computed.

**Why does Dijkstra work?**

The greedy correctness: when we pop the vertex with the
**smallest tentative distance**, no shorter path to it can
exist via any other vertex. Reason: every alternative path
goes through some unpopped vertex with tentative distance
**larger** than ours (we picked the smallest). Adding more
non-negative edges only makes the path longer. So our
tentative distance is the true shortest distance.

This argument **fails** with negative edges: a later negative
edge could shorten a path through some "finalized" vertex.
For negative edges, use Bellman-Ford or SPFA.

**Why O((V + E) log V)?**

- Each vertex is "finalized" once, contributing *O(log V)*
  for its pop.
- Each edge is examined once across all relaxations,
  contributing *O(log V)* for the potential push.
- Total: *O((V + E) log V)*.

**Trace on a small graph:**
```
        2
   A -------> B
   |           \
  1|            \3
   v             v
   C -------> D
        4
```
Sources: A. adj = {A: [(B,2), (C,1)], B: [(D,3)], C: [(D,4)], D: []}

```
Init: dist = [0, INF, INF, INF], h = [(0, A)]
Pop (0, A). d=0=dist[A]. Relax neighbors:
  B: nd=2 < INF. dist[B]=2. Push (2, B).
  C: nd=1 < INF. dist[C]=1. Push (1, C).
h = [(1, C), (2, B)].

Pop (1, C). d=1=dist[C]. Relax neighbors:
  D: nd=5 < INF. dist[D]=5. Push (5, D).
h = [(2, B), (5, D)].

Pop (2, B). d=2=dist[B]. Relax neighbors:
  D: nd=5 not < 5. Skip.
h = [(5, D)].

Pop (5, D). d=5=dist[D]. No neighbors.

Done: dist = [0, 2, 1, 5].
```

**Properties:**
- **Non-negative weights only.** Otherwise correctness breaks.
- **Single source.** For all-pairs use Floyd-Warshall or
  multiple Dijkstra runs.
- **Sparse graphs**: this min-heap version is ideal.
- **Dense graphs**: a different implementation (array-based,
  no heap) gives *O(V²)* which can beat the heap version
  when `E ≈ V²`.

**Applications:**
- Network routing (OSPF protocol).
- GPS shortest path.
- Game AI pathfinding (Dijkstra is the predecessor of A*).
- Network flow algorithms (subroutine).
- Dependency resolution.

Dijkstra is one of the "must-know" algorithms in DSA.
Combined with Floyd-Warshall, Bellman-Ford, and BFS for
unweighted graphs, it covers the shortest-path universe.
''',
            "complexity": "Time O((V + E) log V), space O(V + E).",
        },
        "deep_concept": "Dijkstra is a *greedy* algorithm. Each pop finalizes one vertex's distance. The non-negative weight assumption is essential — otherwise a later edge could 'unfinalize' a vertex.",
        "confusion_notes": [
            {
                "question": "Why the `if d > dist[u]: continue` check?",
                "answer": "Because we may push the same vertex multiple times with different distances. The first pop is the smallest (and correct) one; later pops are stale and should be skipped.",
            },
            {
                "question": "Why does Dijkstra fail with negative edges?",
                "answer": "Because a vertex 'finalized' (popped) might later become reachable via a negative edge that creates a shorter path. The greedy argument breaks. Use Bellman-Ford instead.",
            },
        ],
        "summary": "Min-heap of (dist, vertex); pop, relax, push. O((V+E) log V). Non-negative weights only.",
    },
    {
        "id": "shortest-path-weighted-undirected",
        "title": "Shortest Path in Weighted Undirected Graph",
        "step_id": 15,
        "lecture_id": 4,
        "difficulty": "medium",
        "tags": ["graph", "dijkstra"],
        "what_this_teaches": "Dijkstra works on weighted *undirected* graphs too — just store each edge in both directions.",
        "pattern": "Dijkstra.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["dijkstra"],
        "next_problems": ["path-min-effort"],
        "resources": [_SHEET],
        "understanding": "Same as Dijkstra on directed weighted, but the input is undirected.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "When reading edges, store (v, w) in both adj[u] and adj[v].",
        "optimized": {
            "explanation": "Same Dijkstra code.",
            "code": "# Same as the dijkstra function above. Build adj symmetrically.",
            "complexity": "Time O((V + E) log V).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Just Dijkstra on a symmetric adjacency list.",
    },
    {
        "id": "path-min-effort",
        "title": "Path With Minimum Effort",
        "step_id": 15,
        "lecture_id": 4,
        "difficulty": "medium",
        "tags": ["graph", "dijkstra", "grid"],
        "what_this_teaches": "Dijkstra with a custom cost: 'effort' = max edge weight along the path, not sum.",
        "pattern": "Dijkstra variant with min-of-max.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["dijkstra"],
        "next_problems": ["cheapest-flights-k-stops"],
        "resources": [
            _lc(1631, "path-with-minimum-effort"),
            _SHEET,
        ],
        "understanding": "Find the path from top-left to bottom-right of a grid such that the maximum absolute difference between consecutive cells is minimized.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Dijkstra where the 'distance' to a cell is `max(distance_so_far, abs(height_diff))`.",
        "optimized": {
            "explanation": "Dijkstra with min-of-max.",
            "code": r'''
import heapq
def minimum_effort_path(heights):
    m, n = len(heights), len(heights[0])
    INF = float('inf')
    eff = [[INF]*n for _ in range(m)]
    eff[0][0] = 0
    h = [(0, 0, 0)]
    while h:
        e, i, j = heapq.heappop(h)
        if i == m-1 and j == n-1: return e
        if e > eff[i][j]: continue
        for di, dj in ((1,0),(-1,0),(0,1),(0,-1)):
            ni, nj = i+di, j+dj
            if 0 <= ni < m and 0 <= nj < n:
                ne = max(e, abs(heights[ni][nj] - heights[i][j]))
                if ne < eff[ni][nj]:
                    eff[ni][nj] = ne
                    heapq.heappush(h, (ne, ni, nj))
    return 0
''',
            "complexity": "Time O(m·n · log(m·n)).",
        },
        "deep_concept": "Dijkstra generalizes to any 'min-of-something' shortest path where 'something' is monotone non-decreasing as you extend a path.",
        "confusion_notes": [],
        "summary": "Dijkstra with effort = max(running_effort, abs(diff)).",
    },
    {
        "id": "cheapest-flights-k-stops",
        "title": "Cheapest Flights Within K Stops",
        "step_id": 15,
        "lecture_id": 4,
        "difficulty": "medium",
        "tags": ["graph", "bfs", "bellman-ford"],
        "what_this_teaches": "Dijkstra with a 'stops used' dimension, or relaxed Bellman-Ford with K iterations.",
        "pattern": "Multi-dimensional Dijkstra / Bellman-Ford with K rounds.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["dijkstra"],
        "next_problems": ["network-delay-time"],
        "resources": [
            _lc(787, "cheapest-flights-within-k-stops"),
            _SHEET,
        ],
        "understanding": "Find the cheapest route from src to dst using at most K stops.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Run Bellman-Ford for exactly K+1 rounds (each round corresponds to one more edge in the path).",
        "optimized": {
            "explanation": "Bounded Bellman-Ford.",
            "code": r'''
def find_cheapest_price(n, flights, src, dst, k):
    INF = float('inf')
    dist = [INF] * n
    dist[src] = 0
    for _ in range(k + 1):
        new_dist = dist[:]
        for u, v, w in flights:
            if dist[u] + w < new_dist[v]:
                new_dist[v] = dist[u] + w
        dist = new_dist
    return -1 if dist[dst] == INF else dist[dst]
''',
            "complexity": "Time O(K · E), space O(V).",
        },
        "deep_concept": "Bellman-Ford with K iterations naturally enforces an edge budget — each round relaxes paths of length ≤ k+1.",
        "confusion_notes": [
            {
                "question": "Why `new_dist = dist[:]` and not relax in place?",
                "answer": "Because we want each round to consider only edges added by the *previous* round, not chains within the same round. In-place relaxation would let a single round take a long path.",
            },
        ],
        "summary": "Bellman-Ford with K+1 iterations; copy dist between rounds to enforce the edge budget.",
    },
    {
        "id": "network-delay-time",
        "title": "Network Delay Time",
        "step_id": 15,
        "lecture_id": 4,
        "difficulty": "medium",
        "tags": ["graph", "dijkstra"],
        "what_this_teaches": "Standard Dijkstra; answer is the max of all distances.",
        "pattern": "Dijkstra.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["dijkstra"],
        "next_problems": ["number-of-ways-shortest"],
        "resources": [
            _lc(743, "network-delay-time"),
            _SHEET,
        ],
        "understanding": "From source K, return the time it takes for a signal to reach all nodes (= max shortest distance). Return -1 if some node is unreachable.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Dijkstra; answer = max(dist).",
        "optimized": {
            "explanation": "Dijkstra.",
            "code": r'''
import heapq
from collections import defaultdict
def network_delay_time(times, n, k):
    adj = defaultdict(list)
    for u, v, w in times: adj[u].append((v, w))
    INF = float('inf')
    dist = [INF] * (n + 1)
    dist[k] = 0
    h = [(0, k)]
    while h:
        d, u = heapq.heappop(h)
        if d > dist[u]: continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(h, (dist[v], v))
    ans = max(dist[1:])
    return -1 if ans == INF else ans
''',
            "complexity": "Time O((V+E) log V).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Standard Dijkstra; output max distance.",
    },
    {
        "id": "number-of-ways-shortest",
        "title": "Number of Ways to Arrive at Destination",
        "step_id": 15,
        "lecture_id": 4,
        "difficulty": "medium",
        "tags": ["graph", "dijkstra", "counting"],
        "what_this_teaches": "Dijkstra augmented with a 'ways' counter at each vertex.",
        "pattern": "Dijkstra + DP on shortest paths.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["dijkstra"],
        "next_problems": ["city-with-smallest-neighbors"],
        "resources": [
            _lc(1976, "number-of-ways-to-arrive-at-destination"),
            _SHEET,
        ],
        "understanding": "Count distinct shortest paths from 0 to n-1.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "During Dijkstra, maintain `ways[v]`. When relaxing v to a strictly smaller distance, set ways[v] = ways[u]. When the same distance, ways[v] += ways[u].",
        "optimized": {
            "explanation": "—",
            "code": r'''
import heapq
from collections import defaultdict
def count_paths(n, roads):
    MOD = 10**9 + 7
    adj = defaultdict(list)
    for u, v, w in roads:
        adj[u].append((v, w)); adj[v].append((u, w))
    dist = [float('inf')] * n
    ways = [0] * n
    dist[0] = 0; ways[0] = 1
    h = [(0, 0)]
    while h:
        d, u = heapq.heappop(h)
        if d > dist[u]: continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                ways[v] = ways[u]
                heapq.heappush(h, (nd, v))
            elif nd == dist[v]:
                ways[v] = (ways[v] + ways[u]) % MOD
    return ways[n-1] % MOD
''',
            "complexity": "Time O((V+E) log V).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Dijkstra carrying a `ways` count; reset on strict improvement, accumulate on tie.",
    },
    {
        "id": "city-with-smallest-neighbors",
        "title": "Find the City With the Smallest Number of Neighbors at a Threshold Distance",
        "step_id": 15,
        "lecture_id": 4,
        "difficulty": "medium",
        "tags": ["graph", "floyd-warshall"],
        "what_this_teaches": "All-pairs shortest paths via Floyd-Warshall, then count neighbors within threshold.",
        "pattern": "Floyd-Warshall.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["dijkstra"],
        "next_problems": ["floyd-warshall", "bellman-ford"],
        "resources": [
            _lc(1334, "find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance"),
            _SHEET,
        ],
        "understanding": "For each city, count reachable cities within threshold; return the city with the smallest such count (break ties by highest index).",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Run Floyd-Warshall (all pairs shortest paths). For each city, count cities at distance ≤ threshold.",
        "optimized": {
            "explanation": "Floyd-Warshall + count.",
            "code": r'''
def find_the_city(n, edges, threshold):
    INF = float('inf')
    d = [[INF]*n for _ in range(n)]
    for i in range(n): d[i][i] = 0
    for u, v, w in edges:
        d[u][v] = d[v][u] = w
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    best = (float('inf'), -1)
    for i in range(n):
        count = sum(1 for j in range(n) if i != j and d[i][j] <= threshold)
        if count <= best[0]:
            best = (count, i)
    return best[1]
''',
            "complexity": "Time O(V³).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Floyd-Warshall, then count cities within threshold per node.",
    },
    {
        "id": "bellman-ford",
        "title": "Bellman-Ford Algorithm",
        "step_id": 15,
        "lecture_id": 4,
        "difficulty": "medium",
        "tags": ["graph", "shortest-path", "negative-weights"],
        "what_this_teaches": "Single-source shortest path with negative weights, plus negative-cycle detection.",
        "pattern": "Edge relaxation V-1 times + one extra check.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["dijkstra"],
        "next_problems": ["floyd-warshall"],
        "resources": [
            {"label": "Wikipedia — Bellman-Ford", "url": "https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm"},
            _SHEET,
        ],
        "understanding": "Compute shortest paths from a source even with negative weights, and detect negative cycles.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Relax every edge V-1 times. If any edge can still be relaxed on the Vth iteration, there's a negative cycle.",
        "optimized": {
            "explanation": "Bellman-Ford.",
            "code": r'''
def bellman_ford(V, edges, src):
    INF = float('inf')
    dist = [INF] * V
    dist[src] = 0
    for _ in range(V - 1):
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    # detect negative cycle
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return None      # negative cycle exists
    return dist
''',
            "complexity": "Time O(V · E).",
        },
        "deep_concept": "Each round of relaxation finalizes paths of length one more edge. After V-1 rounds, all simple paths are settled. If V-th round still relaxes, a cycle is involved.",
        "confusion_notes": [],
        "summary": "Relax V-1 times; one more round detects negative cycles. O(V·E).",
    },
    {
        "id": "floyd-warshall",
        "title": "Floyd-Warshall Algorithm",
        "step_id": 15,
        "lecture_id": 4,
        "difficulty": "medium",
        "tags": ["graph", "all-pairs"],
        "what_this_teaches": "Compute all-pairs shortest paths via dynamic programming over intermediate vertices.",
        "pattern": "Triple-loop DP.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["bellman-ford"],
        "next_problems": ["prims-algorithm"],
        "resources": [
            {"label": "Wikipedia — Floyd-Warshall", "url": "https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm"},
            _SHEET,
        ],
        "understanding": "All-pairs shortest paths in O(V³). Works with negative weights (no negative cycles).",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "DP: `d[i][j]` via intermediate vertex k = `min(d[i][j], d[i][k] + d[k][j])`.",
        "optimized": {
            "explanation": "Triple loop.",
            "code": r'''
def floyd_warshall(V, edges):
    INF = float('inf')
    d = [[INF]*V for _ in range(V)]
    for i in range(V): d[i][i] = 0
    for u, v, w in edges: d[u][v] = w
    for k in range(V):
        for i in range(V):
            for j in range(V):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d
''',
            "complexity": "Time O(V³).",
        },
        "deep_concept": "The k loop must be *outermost*. After iteration k, `d[i][j]` is the shortest path using only intermediate vertices {0, ..., k}.",
        "confusion_notes": [
            {
                "question": "Why must k be the outermost loop?",
                "answer": "Because the DP order is on the *set of allowed intermediates*. After loop k, every entry represents shortest distance through {0..k}. Reordering breaks the DP correctness.",
            },
        ],
        "summary": "Triple loop with k outermost; O(V³); all-pairs.",
    },

    # ==================================================================
    # MST / DSU
    # ==================================================================
    {
        "id": "prims-algorithm",
        "title": "Prim's Minimum Spanning Tree",
        "step_id": 15,
        "lecture_id": 5,
        "difficulty": "medium",
        "tags": ["graph", "mst", "heap"],
        "what_this_teaches": "Grow the MST one vertex at a time, always adding the cheapest edge to a new vertex.",
        "pattern": "Min-heap + grow tree.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["dijkstra"],
        "next_problems": ["kruskals-algorithm"],
        "resources": [
            {"label": "Wikipedia — Prim's algorithm", "url": "https://en.wikipedia.org/wiki/Prim%27s_algorithm"},
            _SHEET,
        ],
        "understanding": "Minimum Spanning Tree (MST) = subset of V-1 edges connecting all vertices with minimum total weight.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Start with one vertex; repeatedly add the cheapest edge connecting the current tree to a new vertex. Use a min-heap.",
        "optimized": {
            "explanation": "Min-heap Prim.",
            "code": r'''
import heapq
def prims_mst(V, adj):
    visited = [False] * V
    h = [(0, 0)]
    total = 0
    while h:
        w, u = heapq.heappop(h)
        if visited[u]: continue
        visited[u] = True
        total += w
        for v, ew in adj[u]:
            if not visited[v]:
                heapq.heappush(h, (ew, v))
    return total
''',
            "complexity": "Time O(E log V).",
        },
        "deep_concept": "Cut property: for any cut of the graph, the minimum-weight edge crossing the cut is in some MST. Prim's exploits this by always growing across the cut between visited and unvisited.",
        "confusion_notes": [],
        "summary": "Min-heap of edges leaving the current tree; pop, add new vertex, push its outgoing edges.",
    },
    {
        "id": "kruskals-algorithm",
        "title": "Kruskal's Minimum Spanning Tree",
        "step_id": 15,
        "lecture_id": 5,
        "difficulty": "medium",
        "tags": ["graph", "mst", "dsu"],
        "what_this_teaches": "Sort edges by weight; add the next cheapest if it doesn't form a cycle (use DSU to test).",
        "pattern": "Sort + DSU union-find.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["prims-algorithm"],
        "next_problems": ["dsu-rank-size"],
        "resources": [
            {"label": "Wikipedia — Kruskal's algorithm", "url": "https://en.wikipedia.org/wiki/Kruskal%27s_algorithm"},
            _SHEET,
        ],
        "understanding": "Same MST problem, edge-centric algorithm: sort edges and pick cheapest non-cycle-forming ones.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Sort edges ascending; iterate; for each edge, if its endpoints are in different DSU components, union them and add the edge to MST. Stop after V-1 edges.",
        "optimized": {
            "explanation": "Sort + DSU.",
            "code": r'''
def kruskal(V, edges):
    parent = list(range(V))
    rank = [0] * V
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb: return False
        if rank[ra] < rank[rb]: ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]: rank[ra] += 1
        return True
    edges_sorted = sorted(edges, key=lambda x: x[2])
    total = 0
    used = 0
    for u, v, w in edges_sorted:
        if union(u, v):
            total += w
            used += 1
            if used == V - 1: break
    return total
''',
            "complexity": "Time O(E log E + E α(V)) ≈ O(E log E).",
        },
        "deep_concept": "Cycle property: the heaviest edge of any cycle is *not* in any MST. Kruskal greedily picks the lightest edge that doesn't close a cycle.",
        "confusion_notes": [],
        "summary": "Sort edges; greedy add with DSU cycle check; stop at V-1 edges.",
    },
    {
        "id": "dsu-rank-size",
        "title": "Disjoint Set Union (Rank and Size Variants)",
        "step_id": 15,
        "lecture_id": 5,
        "difficulty": "medium",
        "tags": ["dsu", "union-find"],
        "what_this_teaches": "Union-find with path compression and union by rank/size — nearly O(1) per op.",
        "pattern": "DSU.",
        "prerequisite_lessons": [],
        "prerequisite_problems": [],
        "next_problems": ["provinces-dsu", "kruskals-algorithm"],
        "resources": [
            {"label": "Wikipedia — Disjoint-set data structure", "url": "https://en.wikipedia.org/wiki/Disjoint-set_data_structure"},
            _SHEET,
        ],
        "understanding": r'''
**Union-Find / Disjoint Set Union (DSU)** is a data structure
supporting:
- `find(x)` — return the representative of x's set.
- `union(x, y)` — merge the sets of x and y.

With path compression and union by rank/size, both ops are nearly O(1)
amortized (specifically, O(α(n)) where α is the inverse Ackermann
function).
''',
        "brute_force": {"explanation": "Naive implementations are O(n) per op.", "code": "", "complexity": "—"},
        "thought_process": "—",
        "optimized": {
            "explanation": "DSU with path compression and union by rank.",
            "code": r'''
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n
    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # path compression
            x = self.parent[x]
        return x
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb: return False
        if self.rank[ra] < self.rank[rb]: ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True
''',
            "complexity": "Amortized O(α(n)) per op.",
        },
        "deep_concept": "Path compression + union by rank gives near-linear total time for any sequence of n union/find operations. Used in Kruskal, connected components, percolation, dynamic connectivity, etc.",
        "confusion_notes": [
            {
                "question": "What is α(n) and why does it matter?",
                "answer": "α is the inverse Ackermann function — for all practical purposes (n ≤ 2^65536), α(n) ≤ 5. So DSU operations are essentially constant time.",
            },
        ],
        "summary": "find with path compression + union by rank/size = near-O(1) per op.",
    },
    {
        "id": "provinces-dsu",
        "title": "Number of Provinces — DSU",
        "step_id": 15,
        "lecture_id": 5,
        "difficulty": "easy",
        "tags": ["graph", "dsu"],
        "what_this_teaches": "Count connected components using DSU instead of DFS.",
        "pattern": "DSU merge + count distinct roots.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["dsu-rank-size", "number-of-provinces"],
        "next_problems": ["ops-to-make-connected"],
        "resources": [_lc(547, "number-of-provinces"), _SHEET],
        "understanding": "Same as Number of Provinces, but solved with union-find.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Walk the adjacency matrix; union i and j whenever connected. Count distinct roots.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def find_circle_num_dsu(is_connected):
    n = len(is_connected)
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[ra] = rb
    for i in range(n):
        for j in range(i+1, n):
            if is_connected[i][j]: union(i, j)
    return len({find(i) for i in range(n)})
''',
            "complexity": "Time O(n² α(n)).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "DSU union edges; count distinct roots.",
    },
    {
        "id": "ops-to-make-connected",
        "title": "Number of Operations to Make Network Connected",
        "step_id": 15,
        "lecture_id": 5,
        "difficulty": "medium",
        "tags": ["graph", "dsu"],
        "what_this_teaches": "Components - 1 operations are needed (and feasible iff redundant edges ≥ components - 1).",
        "pattern": "DSU + count extra edges.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["provinces-dsu"],
        "next_problems": ["account-merge"],
        "resources": [
            _lc(1319, "number-of-operations-to-make-network-connected"),
            _SHEET,
        ],
        "understanding": "Given n computers and cable connections, find min operations to connect all (or -1 if impossible).",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Each redundant edge (closing a cycle) can be 'rewired'. If we have at least (components - 1) extras, the answer is components - 1.",
        "optimized": {
            "explanation": "DSU + count.",
            "code": r'''
def make_connected(n, connections):
    if len(connections) < n - 1: return -1
    parent = list(range(n))
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for u, v in connections:
        ru, rv = find(u), find(v)
        if ru != rv: parent[ru] = rv
    components = len({find(i) for i in range(n)})
    return components - 1
''',
            "complexity": "Time O((n + E) α(n)).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "DSU; answer = components - 1 if edges ≥ n-1, else -1.",
    },
    {
        "id": "account-merge",
        "title": "Accounts Merge",
        "step_id": 15,
        "lecture_id": 5,
        "difficulty": "medium",
        "tags": ["graph", "dsu", "hashing"],
        "what_this_teaches": "DSU keyed by email; merge accounts sharing an email; emit final groups.",
        "pattern": "DSU with string keys.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["dsu-rank-size"],
        "next_problems": ["number-of-islands-ii"],
        "resources": [
            _lc(721, "accounts-merge"),
            _SHEET,
        ],
        "understanding": "Each account has a name and a list of emails. Accounts sharing any email belong to the same person. Merge them.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Treat each account index as a DSU node. For each email, record the first account that owns it; subsequent accounts owning the same email union with that one. Then bucket emails by root account.",
        "optimized": {
            "explanation": "DSU + email map.",
            "code": r'''
def accounts_merge(accounts):
    n = len(accounts)
    parent = list(range(n))
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    email_to_acc = {}
    for i, acc in enumerate(accounts):
        for email in acc[1:]:
            if email in email_to_acc:
                ru, rv = find(i), find(email_to_acc[email])
                if ru != rv: parent[ru] = rv
            else:
                email_to_acc[email] = i
    groups = {}
    for email, idx in email_to_acc.items():
        root = find(idx)
        groups.setdefault(root, []).append(email)
    return [[accounts[root][0]] + sorted(emails) for root, emails in groups.items()]
''',
            "complexity": "Time O(N · K log K) for sorting emails per group.",
        },
        "deep_concept": "DSU shines whenever you need 'group by transitive connection'.",
        "confusion_notes": [],
        "summary": "DSU on account indices; map each email to the first owning account; merge.",
    },
    {
        "id": "number-of-islands-ii",
        "title": "Number of Islands II",
        "step_id": 15,
        "lecture_id": 5,
        "difficulty": "hard",
        "tags": ["graph", "dsu", "grid", "online"],
        "what_this_teaches": "Online connectivity via DSU as land cells are added one by one.",
        "pattern": "DSU on grid with dynamic insertion.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["dsu-rank-size"],
        "next_problems": ["making-large-island"],
        "resources": [
            {"label": "LeetCode 305 — Number of Islands II", "url": "https://leetcode.com/problems/number-of-islands-ii/"},
            _SHEET,
        ],
        "understanding": "Process a stream of positions converting water to land; after each operation return the number of islands.",
        "brute_force": {"explanation": "Re-run BFS after each add → O(K·M·N).", "code": "", "complexity": "—"},
        "thought_process": "Maintain a DSU of grid cells. On each add, create a new component; union with each of the 4 land neighbors. Update island count: +1 for new land, -1 per successful union.",
        "optimized": {
            "explanation": "DSU + online updates.",
            "code": r'''
def num_islands2(m, n, positions):
    parent = {}
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    out = []
    count = 0
    for r, c in positions:
        if (r, c) in parent:
            out.append(count); continue
        parent[(r, c)] = (r, c)
        count += 1
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr, nc = r+dr, c+dc
            if (nr, nc) in parent:
                ru, rv = find((r, c)), find((nr, nc))
                if ru != rv:
                    parent[ru] = rv
                    count -= 1
        out.append(count)
    return out
''',
            "complexity": "Time O(K · α).",
        },
        "deep_concept": "Online union is one of DSU's most valuable properties — supports dynamic connectivity without recomputing from scratch.",
        "confusion_notes": [],
        "summary": "DSU keyed by (row, col); each add maybe creates +1 component, each successful union subtracts 1.",
    },
    {
        "id": "making-large-island",
        "title": "Making A Large Island",
        "step_id": 15,
        "lecture_id": 5,
        "difficulty": "hard",
        "tags": ["graph", "dsu", "grid"],
        "what_this_teaches": "Precompute island sizes via DSU; then for each 0 cell, sum the unique neighboring island sizes + 1.",
        "pattern": "DSU sizing + per-cell aggregation.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["number-of-islands-ii"],
        "next_problems": ["swim-in-water"],
        "resources": [
            _lc(827, "making-a-large-island"),
            _SHEET,
        ],
        "understanding": "Given a 0/1 grid, you may flip at most one 0 to 1. Return the size of the largest possible island.",
        "brute_force": {"explanation": "Try each 0, run BFS to size the joined island → O((mn)²).", "code": "", "complexity": "—"},
        "thought_process": "Use DSU to label each island and record its size. For every 0 cell, compute the sum of *distinct* neighboring island sizes + 1.",
        "optimized": {
            "explanation": "DSU + per-cell summation.",
            "code": r'''
def largest_island(grid):
    n = len(grid)
    parent = list(range(n*n))
    size = [1]*(n*n)
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            if size[ra] < size[rb]: ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
    def idx(i, j): return i*n + j
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1:
                for di, dj in ((1,0),(0,1)):
                    ni, nj = i+di, j+dj
                    if ni < n and nj < n and grid[ni][nj] == 1:
                        union(idx(i, j), idx(ni, nj))
    best = max((size[find(idx(i, j))] for i in range(n) for j in range(n) if grid[i][j] == 1), default=0)
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                roots = set()
                for di, dj in ((1,0),(-1,0),(0,1),(0,-1)):
                    ni, nj = i+di, j+dj
                    if 0 <= ni < n and 0 <= nj < n and grid[ni][nj] == 1:
                        roots.add(find(idx(ni, nj)))
                s = 1 + sum(size[r] for r in roots)
                best = max(best, s)
    return best
''',
            "complexity": "Time O(n² α).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "DSU label islands by size; for each 0 sum sizes of unique neighbor roots + 1; take max.",
    },
    {
        "id": "swim-in-water",
        "title": "Swim in Rising Water",
        "step_id": 15,
        "lecture_id": 5,
        "difficulty": "hard",
        "tags": ["graph", "dijkstra", "dsu", "binary-search"],
        "what_this_teaches": "Min-of-max path; solvable by Dijkstra (min-of-max), DSU (Kruskal-style), or binary search + BFS.",
        "pattern": "Min-of-max path.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["path-min-effort"],
        "next_problems": [],
        "resources": [
            _lc(778, "swim-in-rising-water"),
            _SHEET,
        ],
        "understanding": "Find the minimum time t such that the path from (0,0) to (n-1,n-1) stays in cells with elevation ≤ t.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Dijkstra with effort = max along path. Same template as Path with Min Effort.",
        "optimized": {
            "explanation": "—",
            "code": r'''
import heapq
def swim_in_water(grid):
    n = len(grid)
    h = [(grid[0][0], 0, 0)]
    visited = {(0, 0)}
    while h:
        t, i, j = heapq.heappop(h)
        if i == n-1 and j == n-1: return t
        for di, dj in ((1,0),(-1,0),(0,1),(0,-1)):
            ni, nj = i+di, j+dj
            if 0 <= ni < n and 0 <= nj < n and (ni, nj) not in visited:
                visited.add((ni, nj))
                heapq.heappush(h, (max(t, grid[ni][nj]), ni, nj))
    return -1
''',
            "complexity": "Time O(n² log n).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Dijkstra with effort = max(running, cell_height).",
    },

    # ==================================================================
    # OTHER ALGORITHMS
    # ==================================================================
    {
        "id": "kosaraju",
        "title": "Kosaraju's Algorithm — Strongly Connected Components",
        "step_id": 15,
        "lecture_id": 6,
        "difficulty": "hard",
        "tags": ["graph", "scc", "dfs"],
        "what_this_teaches": "Two-pass DFS: first on the original graph (collect finish times), then on the transposed graph (pop in reverse finish order).",
        "pattern": "Two DFS passes + transpose.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["topo-sort-dfs"],
        "next_problems": ["tarjan-bridges"],
        "resources": [
            {"label": "Wikipedia — Kosaraju's algorithm", "url": "https://en.wikipedia.org/wiki/Kosaraju%27s_algorithm"},
            _SHEET,
        ],
        "understanding": r'''
A **Strongly Connected Component (SCC)** is a maximal set of vertices
such that every vertex can reach every other.

Kosaraju's algorithm computes SCCs in O(V + E):
1. DFS the original graph, recording vertices in reverse postorder
   (finishing time order).
2. Transpose the graph (reverse all edges).
3. DFS the transposed graph in step-1 order. Each DFS tree is one SCC.
''',
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Why does this work? In the transposed graph, an SCC remains an SCC. The reverse-finish-order ensures we start each new DFS from the 'topmost' vertex of a remaining SCC, so the DFS from there can only reach within that SCC.",
        "optimized": {
            "explanation": "Kosaraju.",
            "code": r'''
from collections import defaultdict
def kosaraju(V, adj):
    visited = [False] * V
    order = []
    def dfs1(u):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]: dfs1(v)
        order.append(u)
    for u in range(V):
        if not visited[u]: dfs1(u)
    radj = defaultdict(list)
    for u in range(V):
        for v in adj[u]: radj[v].append(u)
    visited = [False] * V
    sccs = []
    def dfs2(u, comp):
        visited[u] = True
        comp.append(u)
        for v in radj[u]:
            if not visited[v]: dfs2(v, comp)
    for u in reversed(order):
        if not visited[u]:
            comp = []
            dfs2(u, comp)
            sccs.append(comp)
    return sccs
''',
            "complexity": "Time O(V + E).",
        },
        "deep_concept": "Tarjan's algorithm computes SCCs in *one* DFS using low-link values — more complex but a single pass.",
        "confusion_notes": [],
        "summary": "DFS finish-time order on original; DFS on transpose in reverse order; each tree = 1 SCC.",
    },
    {
        "id": "tarjan-bridges",
        "title": "Tarjan's Algorithm — Bridges in a Graph",
        "step_id": 15,
        "lecture_id": 6,
        "difficulty": "hard",
        "tags": ["graph", "dfs", "low-link"],
        "what_this_teaches": "DFS with discovery and low-link times. An edge (u, v) is a bridge iff `low[v] > disc[u]`.",
        "pattern": "DFS low-link computation.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["graph-dfs"],
        "next_problems": ["articulation-points"],
        "resources": [
            {"label": "GFG — Bridges in a graph", "url": "https://www.geeksforgeeks.org/bridge-in-a-graph/"},
            _SHEET,
        ],
        "understanding": "A **bridge** is an edge whose removal disconnects the graph. Find all bridges.",
        "brute_force": {"explanation": "Remove each edge and check connectivity → O(E · (V + E)).", "code": "", "complexity": "—"},
        "thought_process": r'''
DFS computing two arrays: `disc[u]` (DFS discovery time) and `low[u]`
(smallest disc value reachable from u's subtree by going down 0+ tree
edges and at most one back-edge).

Edge (u, v) is a bridge iff `low[v] > disc[u]` — meaning v's subtree
cannot reach u or anything earlier without going through edge (u, v).
''',
        "optimized": {
            "explanation": "Tarjan's bridge DFS.",
            "code": r'''
def critical_connections(n, connections):
    from collections import defaultdict
    adj = defaultdict(list)
    for u, v in connections:
        adj[u].append(v); adj[v].append(u)
    disc = [-1] * n
    low = [0] * n
    timer = [0]
    bridges = []
    def dfs(u, parent):
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        for v in adj[u]:
            if v == parent: continue
            if disc[v] == -1:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    bridges.append([u, v])
            else:
                low[u] = min(low[u], disc[v])
    dfs(0, -1)
    return bridges
''',
            "complexity": "Time O(V + E).",
        },
        "deep_concept": "Low-link DFS is one of the most powerful graph-theoretic techniques — it also computes articulation points and SCCs (Tarjan).",
        "confusion_notes": [],
        "summary": "DFS with disc[] and low[]. Bridge iff low[v] > disc[u].",
    },
    {
        "id": "articulation-points",
        "title": "Articulation Points (Cut Vertices)",
        "step_id": 15,
        "lecture_id": 6,
        "difficulty": "hard",
        "tags": ["graph", "dfs", "low-link"],
        "what_this_teaches": "DFS with low-link; u is an articulation point iff it's the root and has ≥ 2 children, or it has a child v with `low[v] >= disc[u]`.",
        "pattern": "DFS low-link variant.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["tarjan-bridges"],
        "next_problems": [],
        "resources": [
            {"label": "GFG — Articulation Points", "url": "https://www.geeksforgeeks.org/articulation-points-or-cut-vertices-in-a-graph/"},
            _SHEET,
        ],
        "understanding": "An **articulation point** is a vertex whose removal disconnects the graph.",
        "brute_force": {"explanation": "Remove each vertex, check connectivity → O(V · (V + E)).", "code": "", "complexity": "—"},
        "thought_process": "Same low-link DFS as bridges, but the *vertex* condition differs.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def articulation_points(V, adj):
    disc = [-1] * V; low = [0] * V
    timer = [0]; ap = set()
    def dfs(u, parent):
        children = 0
        disc[u] = low[u] = timer[0]; timer[0] += 1
        for v in adj[u]:
            if v == parent: continue
            if disc[v] == -1:
                children += 1
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if parent == -1 and children > 1:
                    ap.add(u)
                if parent != -1 and low[v] >= disc[u]:
                    ap.add(u)
            else:
                low[u] = min(low[u], disc[v])
    for s in range(V):
        if disc[s] == -1: dfs(s, -1)
    return sorted(ap)
''',
            "complexity": "Time O(V + E).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "DFS low-link; root with ≥ 2 children or non-root with low[v] ≥ disc[u] is an articulation point.",
    },
]
