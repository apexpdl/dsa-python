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
