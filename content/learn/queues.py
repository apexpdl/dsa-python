"""Queues — FIFO and the BFS engine."""

LESSON = {
    "id": "queues",
    "title": "Queues — First In, First Out",
    "tags": ["queue", "deque", "patterns"],
    "summary": (
        "A full beginner chapter. A queue is a checkout line — new "
        "arrivals join the back, people are served from the front. "
        "It's the engine inside BFS, level-order traversal, and many "
        "sliding-window tricks."
    ),
    "body": r'''
## 0. What this chapter teaches

If stacks are piles, queues are lines. Same simplicity, different
behavior. The thing that makes queues important in DSA is not the
queue itself — it is the algorithms built on top of it,
especially **breadth-first search (BFS)**.

This chapter walks slowly through the basics, then through the
two big patterns (BFS and the monotonic deque), then through the
practical Python pitfalls. By the end you should be able to use a
queue without thinking and recognize "queue-shaped" problems
quickly.

## 1. The line analogy

Think of a queue at a coffee shop. The first person in line is
served first. New customers join the back. Nobody jumps the
line. That is the data structure: **first in, first out**, or
FIFO.

In Python you use `collections.deque` as your go-to queue. A
plain `list` also works, but `list.pop(0)` is *O(n)* — every
other element has to slide one slot to the left. `deque.
popleft()` is *O(1)*, so for any non-trivial queue you should
reach for `deque`.

```python
from collections import deque

q = deque()
q.append(7)         # enqueue (add to back)
q.append(3)
q.append(9)
front = q[0]        # peek front (returns 7, doesn't remove)
v = q.popleft()     # dequeue (returns 7, removes it)
# q is now deque([3, 9])
```

`deque` supports `append`, `appendleft`, `pop`, `popleft`, all in
*O(1)*. That makes it not just a queue but also a stack, and a
double-ended container.

## 2. The single biggest use case: BFS

**Breadth-first search** is the headline use of a queue. BFS
explores a graph or grid in **layers**: first the source, then
everything at distance 1, then distance 2, and so on. A queue
naturally supports this layer-by-layer flow because it serves
the **oldest discovered** node first.

```python
from collections import deque

def bfs(start, neighbors):
    distance = {start: 0}
    q = deque([start])
    while q:
        node = q.popleft()
        for n in neighbors(node):
            if n not in distance:
                distance[n] = distance[node] + 1
                q.append(n)
    return distance
```

The pattern: start with the source in the queue. Repeatedly take
the front, look at its neighbors, record any unvisited ones with
distance + 1, push them to the back. Because we serve
front-first, we always exhaust the current layer before touching
the next.

This same engine powers:

- Level-order tree traversal.
- Shortest path in unweighted graphs.
- "Rotten oranges" style spread simulations.
- Flood fill.
- Multi-source BFS (the "nearest source" generalization).

If a problem cares about "shortest distance in steps" or
"layer by layer" or "spread outward," BFS — and therefore a
queue — is almost certainly the right tool.

## 3. Pattern: level-order traversal

```python
def level_order(root):
    if root is None:
        return []
    levels = []
    q = deque([root])
    while q:
        level_size = len(q)
        current = []
        for _ in range(level_size):
            node = q.popleft()
            current.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        levels.append(current)
    return levels
```

The trick is the `level_size = len(q)` snapshot. We freeze how
many nodes belong to the current level, drain exactly that many,
and what remains in the queue is the next level. Beautiful and
tiny.

Almost every "process tree level by level" problem uses this
shape: right side view, average of each level, zigzag traversal,
level with maximum sum.

## 4. Pattern: monotonic deque (sliding window maximum)

The queue's most beautiful party trick. Given an array and a
window of size `k`, return the maximum of every window.

Brute force: *O(n × k)*. Monotonic deque: *O(n)*.

```python
from collections import deque

def max_window(nums, k):
    dq = deque()  # stores INDICES; the values at these indices are decreasing
    out = []
    for i, x in enumerate(nums):
        # Drop indices that fell out of the window.
        while dq and dq[0] <= i - k:
            dq.popleft()
        # Maintain decreasing-values invariant.
        while dq and nums[dq[-1]] < x:
            dq.pop()
        dq.append(i)
        # The front is the current maximum's index.
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out
```

The deque holds the indices of "still relevant" elements in the
window, in decreasing value order. The front is always the
current max. Each index is appended once and popped once across
the whole run, so the total work is linear.

If this is your first time seeing it, do not panic. It is a
beautiful but slippery idea. Write it out on paper for a tiny
example like `nums = [1, 3, -1, -3, 5, 3, 6, 7]`, `k = 3` and
watch the deque evolve. After two or three traces it clicks.

## 5. Multi-source BFS

A small but powerful generalization. Sometimes you have **many
starting points** rather than one — say, "for each empty cell,
find the distance to the nearest rotten orange." You want all
the rotten oranges to "spread" simultaneously and the algorithm
to record the nearest one for each cell.

The trick: start with **all sources in the queue at the same
time**, each marked at distance 0. Run normal BFS. Because BFS
explores layer by layer from the entire frontier, each cell's
recorded distance is automatically the distance to its **nearest**
source.

```python
def multi_source_bfs(grid, sources):
    distance = {s: 0 for s in sources}
    q = deque(sources)
    while q:
        node = q.popleft()
        for nb in neighbors(node, grid):
            if nb not in distance:
                distance[nb] = distance[node] + 1
                q.append(nb)
    return distance
```

This is exactly the same BFS as before, with a bigger initial
queue. It is one of the most underrated tricks in graph DSA.

Applications: rotten oranges (LeetCode 994), 0/1 matrix
(distance to nearest 0), shortest bridge.

## 6. Queue vs. stack vs. heap — when does each apply?

These three structures all "give you the next item to process"
but with different priorities:

| Structure | Next item served |
|---|---|
| Queue (FIFO) | Oldest enqueued |
| Stack (LIFO) | Most recently pushed |
| Heap (priority) | Smallest (or largest) by key |

- Use a **queue** for breadth-first / layer-by-layer / "first
  discovered first explored."
- Use a **stack** for depth-first / "explore one branch fully
  before backtracking" / explicit recursion simulation.
- Use a **heap** for "always process the smallest/largest /
  most/least urgent" / shortest-path in weighted graphs
  (Dijkstra).

Recognize the problem's shape; pick the right structure.

## 7. Common beginner mistakes

**Mistake 1: using `list.pop(0)`.** It is *O(n)*. Use
`deque.popleft()` for any non-trivial queue. Many beginner BFS
implementations are accidentally *O(V²)* because of this.

**Mistake 2: marking visited on dequeue instead of enqueue.** A
node may be enqueued multiple times before its first dequeue,
ballooning memory and time. Always mark on enqueue.

**Mistake 3: confusing BFS with DFS.** BFS uses a queue and
explores layer by layer. DFS uses a stack (or recursion) and
goes deep before going wide. They are different shapes; do not
mix them.

**Mistake 4: thinking BFS finds shortest paths in weighted
graphs.** It does not. BFS works only when every edge has the
same weight (typically 1). For weighted graphs, use Dijkstra
(heap-based) or Bellman-Ford.

**Mistake 5: forgetting the `level_size` snapshot in
level-order traversal.** Without it, you cannot tell where one
level ends and the next begins. The `for _ in range(level_size)`
is what separates levels cleanly.

## 8. End-of-chapter exercise

1. **Implement a queue using two stacks.** Classic structural
   exercise. LeetCode 232.
2. **Binary tree level order traversal.** Already covered.
   LeetCode 102.
3. **Rotten oranges.** Multi-source BFS in a grid. LeetCode 994.
4. **Sliding window maximum.** Monotonic deque. LeetCode 239.
5. **0/1 matrix.** Multi-source BFS where every 0 is a source.
   LeetCode 542.

Do all five. The last two are the payoff — once you can apply
the monotonic deque and multi-source BFS, you have unlocked a
huge family of problems.

## 9. Where to go next

- **Step 9** — the dedicated stacks/queues step with more queue
  problems.
- **Step 11** — heaps, the priority-based cousin.
- **Step 13** — tree level-order problems.
- **Step 15** — graph BFS problems and Dijkstra (which uses a
  heap-based priority queue).

Queues are tiny but they power some of the most useful
algorithms in the entire curriculum.
''',
}
