"""Step 11 — Heaps."""
from __future__ import annotations

PROBLEMS: list[dict] = [
    {
        "id": "kth-largest",
        "title": "K-th Largest Element in an Array",
        "step_id": 11,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["heap", "top-k", "selection"],
        "what_this_teaches": (
            "The **min-heap of size K** template — the canonical way "
            "to extract the K most/least/etc. of anything from a "
            "stream. The heap's smallest element is the 'threshold' "
            "for whether a new candidate makes it into the top K."
        ),
        "pattern": "Keep a min-heap of size K; pop the smallest when it overflows.",
        "prerequisite_lessons": ["queues"],
        "prerequisite_problems": ["second-largest-element", "merge-sort"],
        "next_problems": [
            "kth-smallest",
            "top-k-frequent",
            "median-from-stream",
            "merge-k-sorted-lists",
            "k-most-frequent",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 11 (Heaps)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 215 — Kth Largest Element in an Array",
                "url": "https://leetcode.com/problems/kth-largest-element-in-an-array/",
            },
            {
                "label": "Python docs — heapq module",
                "url": "https://docs.python.org/3/library/heapq.html",
            },
        ],
        "understanding": r'''
Given an unsorted array, return the **K-th largest** element. Not
the K-th distinct largest — just the K-th in sorted order if the
array were sorted descending.

Example: `[3, 2, 1, 5, 6, 4]`, `k = 2` → `5`.

The brute force is to sort and index. The optimized solution
maintains a **min-heap of size K** — one of the most reused tricks
in interview DSA.
''',
        "brute_force": {
            "explanation": r'''
Sort, then index. *O(n log n)*. Simple and often acceptable.
''',
            "code": r'''def kth_largest_sort(arr: list[int], k: int) -> int:
    return sorted(arr, reverse=True)[k - 1]
''',
            "complexity": "**Time**: *O(n log n)*. **Space**: *O(n)*.",
        },
        "thought_process": r'''
The **min-heap of size K** trick:

1. Walk through the array.
2. Push each element onto a min-heap.
3. If the heap grows larger than `K`, pop the smallest.

After processing every element, the heap contains the K largest
values, and the **top of the min-heap is the K-th largest**.

Why does this work? Because the heap maintains "the K largest so
far". The smallest in the heap is the threshold; any new element
smaller than the threshold gets ignored (it would be popped right
away). Any new element larger displaces the threshold.

Total work: *O(n log K)* — n insertions, each *O(log K)*. For
small `K` and large `n`, this is dramatically better than sorting.

There is also **Quickselect**: a partition-based selection
algorithm that runs in *O(n)* average time. It is what `numpy`
uses under the hood. We mention it for completeness but the
heap version is simpler and just as good for typical sizes.
''',
        "optimized": {
            "explanation": r'''
Maintain a min-heap of size K. Iterate the array, pushing each
element and popping when the heap exceeds K.
''',
            "code": r'''import heapq

def kth_largest(arr: list[int], k: int) -> int:
    # Python's heapq is a min-heap. The smallest item is at index 0.
    heap: list[int] = []
    for x in arr:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    # The heap now holds the k largest values. The smallest of them
    # (top of the min-heap) is the k-th largest.
    return heap[0]
''',
            "complexity": (
                "**Time**: *O(n log k)*. **Space**: *O(k)*."
            ),
        },
        "deep_concept": r'''
The "min-heap of size K" pattern handles a wide family of "top K"
problems:

- **Top K frequent elements** — heap of `(frequency, value)`.
- **K closest points to origin** — heap of `(distance, point)`.
- **Merge K sorted lists** — heap of `(value, list_id, index)`.
- **Find median from a data stream** — two heaps balancing each
  other.

The unifying idea: a heap gives you *O(log K)* access to the
"worst of the best K" — which is exactly the threshold that
decides whether a new candidate is good enough.

For the symmetric "smallest K" question, use a **max-heap of size
K** (in Python, negate values to simulate a max-heap with `heapq`).

The big-picture takeaway: heaps are the data structure for "give
me the next best thing, then the next best, then the next". Any
problem that fits that description is heap territory.
''',
        "confusion_notes": [
            {
                "question": "Why use a *min*-heap to find the K-th *largest*?",
                "answer": r'''
Because the **smallest** element of the K largest values is the
one we ultimately want to return. A min-heap keeps the smallest
at the top, where we can look at it in `O(1)`.

Imagine the K largest values lined up in sorted order. They look
like `[L_1, L_2, ..., L_K]` where `L_1 <= L_2 <= ... <= L_K` and
`L_K` is the maximum. The **K-th largest** in the conventional
ranking (1st largest = max, 2nd largest = next-to-max, etc.) is
**L_1** — the smallest of the K largest.

A min-heap of these K values has `L_1` at the top. So after
populating it with the K largest values from the array, `heap[0]`
*is* the answer.

If we tried to use a max-heap of size K, the top would be the
largest of the K — the *1st* largest of the whole array, not the
*K-th*. Wrong answer.

The other intuition: the heap acts as a **threshold filter**.
The element at the top of the min-heap is "the worst score that
still qualifies for the top K." Any new element better than the
threshold replaces it; any worse element is ignored.

So: min-heap for K-th largest. Max-heap for K-th smallest.
Always flip the heap direction relative to the question.
''',
            },
            {
                "question": "Why `O(n log K)` instead of `O(n log n)`?",
                "answer": r'''
Because the heap **never grows past size K**, so each heap
operation costs `O(log K)`, not `O(log n)`.

`heappush` on a heap of size `K` is `O(log K)` because the
sift-up walks the heap's tree of depth `log K`.
`heappop` is `O(log K)` for the same reason. We do at most `n`
pushes and `n - K` pops, all bounded by `O(log K)` each. Total:
`O(n log K)`.

When K is small (say, K = 10 in an array of a million elements),
this is dramatically faster than sorting the entire array, which
would be `O(n log n) = O(n log 1,000,000) = O(n × 20)`. The
heap-of-K approach is `O(n log 10) = O(n × 3.3)`, roughly 6×
faster.

When K approaches n (find the n-th largest, i.e., the minimum),
the heap grows to size n and the time becomes `O(n log n)`,
matching a full sort. In that regime, sorting is simpler. The
heap-of-K trick is for the asymmetric case where K << n.

A neat observation: the algorithm is essentially **doing partial
sorting**. It maintains the top K in a sorted-enough form (a
heap) without paying for full sortedness. This is the same idea
behind partial-sort algorithms in C++'s `<algorithm>` library.
''',
            },
            {
                "question": "Why use `heappush` followed by `heappop` instead of just `heappushpop`?",
                "answer": r'''
You can. `heapq.heappushpop(heap, x)` is a slight optimization
that combines push and pop into one operation, often faster than
calling them separately.

```python
import heapq

def kth_largest(arr, k):
    heap = []
    for x in arr:
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:
            heapq.heapreplace(heap, x)
    return heap[0]
```

Two improvements compared to the basic version:

1. **`heapreplace`** does a pop-then-push in one call, with
   guaranteed `O(log K)` and slightly fewer comparisons than
   doing them separately.
2. **The `if x > heap[0]` guard** skips heap mutation entirely
   when the new element is not big enough to displace the
   threshold. This is a noticeable speedup on inputs where most
   elements are small.

Functionally identical to the basic version, just faster in
practice. Use it once you have proven you understand the basic
flow.

There is also `heappushpop(heap, x)` which is push-then-pop in
one call. It is correct but slightly different semantics:
`pushpop` might return the pushed value itself (if it is the
smallest); `replace` always pops the current top first.

For "keep at most K elements" problems, `heapreplace` is
usually the right choice.
''',
            },
            {
                "question": "When should I use Quickselect instead?",
                "answer": r'''
**Quickselect** finds the K-th smallest (or largest) element in
*O(n)* average time and *O(1)* extra space. Compared to the
heap-of-K solution (`O(n log K)` time, `O(K)` space),
Quickselect is asymptotically faster for any K but has more
volatile runtime.

Quickselect uses Quicksort's partition step, recursing only on
the side that contains the K-th element. Average case `O(n)`,
worst case `O(n²)` (same bad-pivot scenario as Quicksort).

```python
def quickselect(arr, k):
    # Find the k-th largest (1-indexed).
    target = len(arr) - k       # convert to "find target-th smallest"
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        p = partition(arr, lo, hi)
        if p == target:
            return arr[p]
        elif p < target:
            lo = p + 1
        else:
            hi = p - 1
```

When to prefer Quickselect:

- When `K` is close to `n` (heap of K becomes a sort).
- When you can afford `O(n²)` worst-case (typically with random
  pivots, the worst case is astronomically unlikely).
- When you want to **modify the input array** to find the answer
  in place.

When to prefer the heap:

- When the input is a **stream** (you cannot reorder it).
- When you need a deterministic `O(n log K)` guarantee.
- When K is much smaller than n.

In interviews, mention both. The heap is easier to write
quickly. Quickselect demonstrates a deeper algorithmic move.
''',
            },
        ],
        "summary": r'''
**Pattern**: maintain a min-heap of size K.

**Lesson**: the top of a size-K min-heap is the threshold of "good
enough to be in the top K". When a new candidate arrives, compare
against the threshold and decide.

**Recognize next time**: any "top K largest / smallest / most
frequent / closest" problem. Almost always heaps.
''',
    },
]
