"""Step 15 — Graphs."""
from __future__ import annotations

PROBLEMS: list[dict] = [
    {
        "id": "graph-bfs",
        "title": "Breadth-First Search (BFS)",
        "step_id": 15,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["graph", "bfs", "queue"],
        "understanding": r'''
BFS visits every node of a graph in **layers**: first the source,
then everything at distance 1 from the source, then distance 2, and
so on. It uses a queue (FIFO) and is the natural choice when the
problem cares about **shortest path in an unweighted graph** or
"closest first".

We will treat the graph as an adjacency list: a dict from node to
list of neighbours.
''',
        "brute_force": {
            "explanation": r'''
There is no "brute force" alternative — BFS is the right algorithm
for layer-by-layer traversal. The only choice is the data
structure: queue (BFS) versus stack/recursion (DFS).

The two important things to get right:

1. **Mark nodes visited when you enqueue them, not when you
   dequeue them.** Otherwise you may enqueue the same node multiple
   times before its first dequeue, ballooning memory and time.
2. **Use `collections.deque` for the queue.** A plain `list` with
   `pop(0)` is *O(n)* per dequeue and silently destroys BFS's
   *O(V + E)* runtime.
''',
            "code": r'''# Naive: using list as queue (don't do this).
def bfs_list(start, graph):
    visited = {start}
    q = [start]
    order = []
    while q:
        node = q.pop(0)         # O(n)! BAD.
        order.append(node)
        for n in graph.get(node, ()):
            if n not in visited:
                visited.add(n)
                q.append(n)
    return order
''',
            "complexity": (
                "**Time**: *O(V × (V + E))* with `pop(0)`. **Space**: *O(V)*."
            ),
        },
        "thought_process": r'''
Imagine you are infecting a town starting from one person. On day 1
only you are infected. On day 2 everyone you touched yesterday is
infected. On day 3 everyone they touched is infected. And so on.

That is exactly BFS. The queue holds "everyone newly infected
today, waiting for their turn to infect tomorrow". Marking on
enqueue is the equivalent of "patient zero plans visits to all
their contacts the moment they themselves get sick".

The algorithm produces the **shortest path in terms of edge count**
because each layer is exactly one step further from the source.

A pattern: when you want to find the shortest distance from a
single source in an unweighted graph, BFS is the right tool. When
edges have weights, Dijkstra is needed (a heap-based variant).
''',
        "optimized": {
            "explanation": r'''
BFS using `collections.deque` for *O(1)* dequeue.
''',
            "code": r'''from collections import deque

def bfs(start, graph: dict) -> dict:
    """Return distances from start to every reachable node."""
    distance = {start: 0}
    q = deque([start])
    while q:
        node = q.popleft()
        for nb in graph.get(node, ()):
            # Mark on enqueue. The check ensures each node is
            # enqueued at most once.
            if nb not in distance:
                distance[nb] = distance[node] + 1
                q.append(nb)
    return distance
''',
            "complexity": (
                "**Time**: *O(V + E)*. **Space**: *O(V)* for the "
                "distance map and the queue."
            ),
        },
        "deep_concept": r'''
BFS is the engine inside many "shortest" or "fewest steps"
problems:

- **Rotten oranges** — multi-source BFS spreading from every rotten
  cell.
- **Word ladder** — BFS over word graph where edges are one-letter
  changes.
- **Knight on a chessboard** — BFS over board positions.
- **0/1 BFS** — variant where edges have weight 0 or 1; uses a
  deque to maintain shortest distances in a single pass.

The two patterns to remember:

1. **Single-source BFS**: start from one node; compute distances to
   all others.
2. **Multi-source BFS**: start from a set of nodes; compute the
   distance to the **nearest** of them, for each cell.

Multi-source BFS is one of the most beautiful tricks in graph
algorithms. It is exactly BFS with multiple starting nodes in the
queue, all at distance 0. The "nearest source" comes out naturally
because BFS visits in layers.
''',
        "summary": r'''
**Pattern**: queue-based traversal, mark on enqueue.

**Lesson**: BFS produces shortest paths in unweighted graphs. Use
`deque`. Mark on enqueue.

**Recognize next time**: any "shortest steps", "fewest moves",
"closest such cell" problem in an unweighted graph or grid.
''',
    },
]
