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
        "what_this_teaches": (
            "BFS — the layer-by-layer traversal engine that powers "
            "every 'shortest path in an unweighted graph' problem. "
            "Once you grok the 'mark on enqueue + deque' pattern, "
            "rotten oranges, word ladder, knight on chessboard, and "
            "0/1 matrix all start to look like the same problem in "
            "different costumes."
        ),
        "pattern": "Queue-based traversal; enqueue starts at distance 0; mark on enqueue.",
        "prerequisite_lessons": ["queues", "trees"],
        "prerequisite_problems": [],
        "next_problems": [
            "graph-dfs",
            "rotten-oranges",
            "flood-fill",
            "shortest-path-undirected-unit",
            "number-of-provinces",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 15 (Graphs)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "Python docs — collections.deque",
                "url": "https://docs.python.org/3/library/collections.html#collections.deque",
            },
        ],
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
            "walkthrough": r'''
This is the WRONG way to implement BFS in Python. It produces
the correct answer but with a hidden *O(V)* hit per dequeue —
turning the algorithm into *O(V²)* total. Let me explain.

**`def bfs_list(start, graph):`** — Takes a start node and an
adjacency graph (dict from node → iterable of neighbors).

**`visited = {start}`** — Set of nodes we've already enqueued.
Using a **set** means *O(1)* lookups. Initialize with `start`
because we're about to enqueue it.

**`q = [start]`** — Queue of nodes to process. **Implemented
as a Python list.** This is where the trouble lies.

**`order = []`** — Accumulator for the BFS visit order.

**`while q:`** — Continue while the queue is non-empty.

**`node = q.pop(0)`** — **This is the bug.** `list.pop(0)`
removes the first element and shifts every remaining element
left by one position. That shift is *O(n)* where n is the
current queue length. In a BFS over V nodes, we do V such
pops; total work is *O(V²)* just from the dequeues.

For small graphs (V ≤ 1000) this is invisible. For V = 10⁶,
it's catastrophic — a trillion operations.

**`order.append(node)`** — Record the visit.

**`for n in graph.get(node, ()):`** — Walk every neighbor.
The `.get(node, ())` returns an empty tuple if `node` isn't in
the graph dict, avoiding a KeyError.

**`if n not in visited:`** — Skip nodes we've already
enqueued. The set lookup is *O(1)*.

**`visited.add(n); q.append(n)`** — Mark visited and enqueue.

**`return order`** — Hand back the visit order.

**The fix**: use `collections.deque` instead of a list.
`deque.popleft()` is *O(1)*. Everything else stays the same.
That's the optimized version below.

The lesson: **don't use `list.pop(0)` for queues**. It's one
of the most common performance bugs in Python DSA code. The
algorithm is correct; the data structure choice is wrong.
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
            "walkthrough": r'''
The canonical BFS. The same algorithm as before but with a
proper queue. *O(V + E)* time — linear in graph size.

**`from collections import deque`** — Import the deque
("double-ended queue") class. It supports *O(1)* append and
popleft, unlike a regular Python list.

**`def bfs(start, graph: dict) -> dict:`** — Takes the start
node and an adjacency-map graph. Returns a dict mapping each
reachable node to its distance from `start`.

**`distance = {start: 0}`** — Map from node to its distance.
We seed it with `start: 0` (the start node is at distance 0
from itself). This map doubles as our "visited" set — a key
being present means "we've enqueued this node."

**`q = deque([start])`** — Initialize the queue with `start`.
The deque constructor accepts any iterable.

**`while q:`** — Process until queue is empty.

**`node = q.popleft()`** — **The crucial O(1) operation.**
Dequeue the front of the queue. Unlike `list.pop(0)`, this is
constant time regardless of queue size.

**`for nb in graph.get(node, ()):`** — Walk every neighbor.
Using `.get(node, ())` returns an empty tuple if `node` has
no entry in the graph (a sink with no outgoing edges).

**`if nb not in distance:`** — Is `nb` unvisited? `distance`
serves as both the "visited" set and the answer accumulator.

**`distance[nb] = distance[node] + 1`** — Set the neighbor's
distance to one more than the current node's. This is the
**BFS distance update**: each step away from start adds 1.

**`q.append(nb)`** — Enqueue the neighbor for later
processing. *O(1)* with deque.

**`return distance`** — Hand back the distance map.

**Why does this give shortest paths?**

BFS processes nodes in **distance order**. Layer 0 is just
`start`. Layer 1 is all nodes one step from `start`. Layer 2
is all nodes two steps from `start`. Etc.

The reason: a node enters the queue when discovered via its
first encountered predecessor. Because BFS expands by layers,
that first predecessor is on the layer immediately below the
discovered node. So the recorded distance is always the
**minimum** number of edges.

**Trace on a simple graph:**
```
graph = {1: [2, 3], 2: [4], 3: [4, 5], 4: [], 5: []}

Init: distance = {1: 0}, q = deque([1])

Pop 1: neighbors 2 and 3.
       distance = {1:0, 2:1, 3:1}, q = deque([2, 3])

Pop 2: neighbor 4. (4 not in distance.)
       distance = {1:0, 2:1, 3:1, 4:2}, q = deque([3, 4])

Pop 3: neighbors 4 (already in distance, skip) and 5.
       distance = {1:0, 2:1, 3:1, 4:2, 5:2}, q = deque([4, 5])

Pop 4: no neighbors. q = deque([5])
Pop 5: no neighbors. q = deque([])
Done.

Final: distance = {1:0, 2:1, 3:1, 4:2, 5:2}.
```

Each edge is examined a constant number of times (once from
each end). Each node is enqueued exactly once. Total work
*O(V + E)*. Memory *O(V)* for the distance map and the queue.

BFS is the foundation of:
- **Shortest path in unweighted graphs** (this very problem).
- **Topological sort via Kahn's algorithm**.
- **Level-order traversal of trees**.
- **Bipartite checking** (2-color BFS).
- **Multi-source BFS** (start from all sources at distance 0).
- **0/1 BFS** (deque with appendleft for free edges).

Master the deque pattern; it's the workhorse of every BFS
variant.
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
        "confusion_notes": [
            {
                "question": "Why mark a node visited *when we enqueue it*, not when we dequeue it?",
                "answer": r'''
Because the same node might appear in many neighbour-lists. If
we wait until dequeue to mark it visited, every enqueue between
"first time we see it" and "we finally dequeue it" will
re-enqueue the same node. The queue balloons, the algorithm
slows down, and in pathological cases the runtime degrades from
*O(V + E)* to something much worse.

Walk through a tiny example. Suppose nodes `A, B, C` all
neighbour `D`. We start BFS from `A`. We enqueue `A`. We dequeue
`A` and look at its neighbours: enqueue `B, C, D`. We dequeue
`B` and look at its neighbours: among them is `D`. If `D` is
not marked visited yet, we enqueue it again. Same for `C`. Now
the queue has `D` three times, and we will do three identical
explorations of `D`'s neighbours.

Marking on enqueue closes this hole. The first time `D` is
spotted (as a neighbour of `A`), we add it to `visited` and to
the queue. From then on, anyone else who tries to enqueue `D`
checks `if D not in visited` first and skips. Each node is
enqueued at most once.

This makes the algorithm `O(V + E)` exactly: each vertex is
processed once (each contributes one queue insertion and one
removal), and each edge is examined twice (once from each
endpoint).

The same discipline applies in DFS, in Dijkstra (with a slight
twist because Dijkstra is "lazy delete"), and in any traversal
where a node has multiple incoming edges. Mark when you commit
to visiting, not when you actually visit.
''',
            },
            {
                "question": "Why is `list.pop(0)` so disastrous compared to `deque.popleft()`?",
                "answer": r'''
Because `list.pop(0)` is `O(n)`. Every other element of the
list has to slide one slot to the left to fill the gap left
by the removed front element. Doing that inside a loop that
runs `n` times gives `O(n²)` total work — silently turning your
linear-time BFS into a quadratic-time disaster.

`collections.deque` is a doubly-linked list of fixed-size
blocks. Both `popleft()` and `append()` are `O(1)`. So `deque`-
based BFS stays at the promised `O(V + E)`.

The frustrating part: the `list.pop(0)` version still works.
The correctness is identical to the `deque` version. It just
runs many times slower on large inputs — sometimes 100x slower
or worse, depending on the graph size. You will not notice on a
20-node toy example; you will notice when your real graph has
100,000 nodes.

So **always reach for `deque` when you need FIFO behavior**.
The performance gap is silent and severe, and there is no
reason to ever choose `list.pop(0)` for queue-like work.

Reminder of the import:

```python
from collections import deque
q = deque([start])
node = q.popleft()
q.append(neighbour)
```

Three lines of habit. Burn them in.
''',
            },
            {
                "question": "What if I want to know the actual shortest *path*, not just the distance?",
                "answer": r'''
Track a **parent map** alongside the distance map. Whenever you
enqueue a neighbour, record which node was its predecessor.
After BFS finishes, reconstruct the path by walking the parent
pointers backwards from the target.

```python
from collections import deque

def shortest_path(start, target, graph):
    if start == target:
        return [start]
    parent = {start: None}
    q = deque([start])
    while q:
        node = q.popleft()
        for nb in graph.get(node, ()):
            if nb in parent:
                continue
            parent[nb] = node
            if nb == target:
                # Reconstruct: walk parents back to the source.
                path = []
                cur = nb
                while cur is not None:
                    path.append(cur)
                    cur = parent[cur]
                return path[::-1]
            q.append(nb)
    return None       # no path
```

Two small additions to the basic BFS:

1. A `parent` dict mapping each visited node to the node that
   first discovered it.
2. After finding `target`, walk the parents backwards to
   reconstruct the path, then reverse.

This is a foundational pattern for path-reconstruction
problems: word ladder, shortest knight's path, etc. Memorize
the shape.

There is no extra time cost — the BFS still runs in `O(V + E)`.
The reconstruction is `O(path length)`, which is bounded by `V`.
''',
            },
            {
                "question": "When does BFS *not* give the shortest path?",
                "answer": r'''
When the edges have **different weights**. BFS treats every
edge as a single "step," so the shortest *number-of-edges* path
matches the shortest *total-weight* path only when all weights
are equal (typically 1).

For weighted graphs with non-negative weights, use **Dijkstra's
algorithm**, which uses a priority queue (min-heap) instead of
a plain FIFO queue. The heap always pops the node with the
smallest cumulative distance, ensuring optimal expansion order.

For weighted graphs with weights of only 0 and 1, use **0/1
BFS** — a deque-based variant where 0-weight edges push to the
front of the deque and 1-weight edges push to the back. This
keeps the deque sorted enough that BFS-like behavior still
gives shortest paths.

For graphs with negative weights, neither BFS nor Dijkstra
works. You need **Bellman-Ford** (slower but handles
negatives) or **SPFA**.

The summary:

| Edges have... | Algorithm |
|---|---|
| Unit weights | BFS — `O(V + E)` |
| Weights 0 and 1 | 0/1 BFS — `O(V + E)` |
| Non-negative weights | Dijkstra — `O((V + E) log V)` |
| Any weights, no negative cycles | Bellman-Ford — `O(V × E)` |
| Any weights, all-pairs | Floyd-Warshall — `O(V³)` |

For interview problems, recognize the graph type first, then
pick the matching algorithm. BFS is the right answer for
"shortest path in unweighted graph" — and only there.
''',
            },
        ],
        "summary": r'''
**Pattern**: queue-based traversal, mark on enqueue.

**Lesson**: BFS produces shortest paths in unweighted graphs. Use
`deque`. Mark on enqueue.

**Recognize next time**: any "shortest steps", "fewest moves",
"closest such cell" problem in an unweighted graph or grid.
''',
    },
]
