"""Queues — FIFO and the BFS engine."""

LESSON = {
    "id": "queues",
    "title": "Queues — First In, First Out",
    "tags": ["queue", "deque", "patterns"],
    "summary": (
        "A queue is a checkout line. New arrivals join the back; people "
        "are served from the front. It's the engine inside BFS, level "
        "order traversal, and many sliding-window tricks."
    ),
    "body": r'''
## The line analogy

Think of a queue at a coffee shop. The first person in line is served
first. New customers join the back. Nobody jumps the line. That is
exactly the data structure: **first in, first out**, or FIFO.

In Python we use `collections.deque` (double-ended queue) as our
go-to. A plain list also works, but `list.pop(0)` is *O(n)* — it
shuffles every other element forward. `deque.popleft()` is *O(1)*,
so for any non-trivial queue you should reach for `deque`.

```python
from collections import deque

q: deque[int] = deque()
q.append(7)      # enqueue
q.append(3)
q.append(9)
front = q[0]     # peek front: 7
v = q.popleft()  # dequeue: returns 7, queue becomes deque([3, 9])
```

`deque` supports `append`, `appendleft`, `pop`, `popleft`, all in
*O(1)*. That makes it not just a queue, but also a stack, and a
double-ended container.

## Where does a queue actually help?

The **headline** use case is **breadth-first search (BFS)**. A BFS
explores a graph or grid in layers: first all the nodes at distance
0 (the start), then distance 1, then distance 2, and so on. A queue
is the natural data structure for "explore in the order you
discovered things".

```python
def bfs(start, neighbors):
    """Return distances from start to all reachable nodes."""
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

The pattern: start with the source in the queue with distance 0.
Repeatedly take the front, look at its neighbours, record any
unvisited ones with distance + 1, push them to the back. Because we
serve front-first, we always exhaust the current layer before
touching the next.

This same engine powers level-order tree traversal, shortest-path
problems in unweighted graphs, "rotten oranges" style spread
simulations, and "flood fill" tasks.

## Pattern: level-order traversal

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

The trick is the `level_size = len(q)` snapshot. We freeze how many
nodes belong to the current level, drain exactly that many, and what
remains in the queue is the next level. Beautiful and tiny.

## Pattern: monotonic deque (sliding window maximum)

This is the queue's most beautiful party trick. Given an array and a
window of size `k`, return the maximum of every window.

The brute force is *O(n × k)*. With a monotonic deque, we get *O(n)*.

```python
def max_window(nums: list[int], k: int) -> list[int]:
    dq: deque[int] = deque()           # stores INDICES; values in dq are decreasing
    out: list[int] = []
    for i, x in enumerate(nums):
        # Drop indices that have fallen out of the window.
        while dq and dq[0] <= i - k:
            dq.popleft()
        # Maintain decreasing-values invariant: pop weaker tails.
        while dq and nums[dq[-1]] < x:
            dq.pop()
        dq.append(i)
        # The front of the deque is always the index of the current max.
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out
```

The deque always holds the indices of the "still relevant" elements
in the window, in decreasing value order. The front is always the
current maximum. Each index is appended once and popped once across
the whole run — so the total work is linear.

If you have not seen this before, do not panic. It is a beautiful but
slippery idea. The bookkeeping for "remove stale entries from the
front, maintain monotonicity at the back" pays off once you write it
a few times.

## When does a queue feel wrong?

If the problem cares about **most recent first**, you want a stack
(LIFO), not a queue. If it cares about **priority** (smallest first,
or largest first), you want a heap (priority queue). A plain FIFO
queue is right when "first discovered, first explored" matches the
problem's flow.

## Common beginner mistakes

**Mistake 1: using `list.pop(0)`.** It is *O(n)*. Use
`deque.popleft()` if you actually need a queue. Many beginner BFS
implementations are accidentally *O(n²)* because of this.

**Mistake 2: forgetting to mark a node visited when you enqueue it,
not when you dequeue it.** If you mark on dequeue, a node may be
enqueued multiple times before its first visit, blowing up memory
and time. Mark on enqueue.

**Mistake 3: confusing BFS with DFS in a graph.** BFS uses a queue
and explores layer by layer. DFS uses a stack (or recursion) and
goes deep before going wide. They are different shapes; do not mix
them.

**Mistake 4: thinking BFS finds shortest paths in weighted graphs.**
It does not. BFS finds shortest paths only when every edge has
weight 1. For weighted graphs, you need Dijkstra (a heap-based
algorithm) instead.

## The mental model

Queue is a checkout line: front out, back in. It is the data
structure for "process in the order discovered". BFS, level-order,
spread/flood simulations — all queues underneath. When you see "level
by level" or "shortest steps in an unweighted setting", reach for a
deque first.
''',
}
