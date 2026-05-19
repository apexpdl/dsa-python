"""Step 11 extras — Heaps / Priority Queue (14 problems).

Teaches heap fundamentals first (introduction, push/pop, heapify, is-heap),
then heavy applications (top-K, merge K sorted lists, median from stream,
task scheduler, twitter design, hand of straights).
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
    # ------------------------------------------------------------------
    # 1) Heap Introduction
    # ------------------------------------------------------------------
    {
        "id": "heap-introduction",
        "title": "Introduction to Heap / Priority Queue",
        "step_id": 11,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["heap", "priority-queue", "concept"],
        "what_this_teaches": "What a heap is, why it exists, how it differs from a sorted array or BST, and the two main flavors (min-heap vs max-heap).",
        "pattern": "Conceptual overview.",
        "prerequisite_lessons": ["arrays", "binary-tree-basics"],
        "prerequisite_problems": [],
        "next_problems": ["min-max-heap-impl", "heap-array-impl", "is-max-heap"],
        "resources": [
            {"label": "Wikipedia — Binary heap", "url": "https://en.wikipedia.org/wiki/Binary_heap"},
            _SHEET,
        ],
        "understanding": r'''
A **heap** is a complete binary tree with a single rule: the root holds
the extreme element (smallest in a min-heap, largest in a max-heap) and
the same property holds *recursively* for every subtree. There is no
left-vs-right order — only parent-vs-child.

**Why does this exist?** Suppose you constantly need the *current
smallest* (or largest) item among many, and the set keeps changing:
- A sorted array gives O(1) read but O(n) insert.
- A BST gives O(log n) insert and O(log n) read, but rebalancing is
  fiddly to implement correctly.
- A heap gives O(log n) insert, O(1) read of the extreme, O(log n)
  pop, and is implementable in a flat array with simple index arithmetic.

For 90% of "I need the next-extreme element" problems, a heap is the
right answer.

**Min-heap vs max-heap.** A min-heap has the smallest at the root
(parent ≤ children); a max-heap has the largest (parent ≥ children).
Python's `heapq` is a *min-heap*. To simulate a max-heap, push the
negative of each value.

**Array layout.** A heap of size n lives in an array `a[0..n−1]`:
- node `i`'s children are at `2i + 1` and `2i + 2`.
- node `i`'s parent is at `(i − 1) // 2`.

No pointers, no nodes, no allocation per insert. This is one of the
reasons heaps are blisteringly fast in practice.
''',
        "brute_force": {
            "explanation": r'''
For "keep getting the smallest of a changing set", a sorted list works:
push = `bisect.insort` O(n), pop = `pop(0)` O(n). On small inputs this
is fine. We replace it with a heap when n is large or operations are
frequent.
''',
            "code": r'''
import bisect
sorted_list = []
def push(x):       bisect.insort(sorted_list, x)        # O(n)
def pop_min():     return sorted_list.pop(0)            # O(n)
def peek_min():    return sorted_list[0]                # O(1)
''',
            "complexity": "O(n) per insert, O(n) per pop.",
        },
        "thought_process": r'''
We want O(log n) per insert and pop, with O(1) peek. The trick: keep the
extreme at index 0 and only fix the *path* from a changed node to the
root (or to a leaf). The path length is ⌈log₂ n⌉. That is the
heap's promise.
''',
        "optimized": {
            "explanation": r'''
Using Python's built-in `heapq` module. We illustrate the three core
operations: push, pop, peek. Behind the scenes, both push and pop
re-establish the heap property via a "sift up" or "sift down" along
exactly one root-to-leaf path.
''',
            "code": r'''
import heapq

heap = []                  # represents a min-heap as a flat list

heapq.heappush(heap, 5)    # O(log n): append then sift up to keep parent ≤ child
heapq.heappush(heap, 1)
heapq.heappush(heap, 3)

print(heap[0])             # peek smallest, O(1)
print(heapq.heappop(heap)) # remove smallest, O(log n)

# Max-heap via negation
maxh = []
for v in [5, 1, 3]:
    heapq.heappush(maxh, -v)
print(-maxh[0])            # largest
''',
            "complexity": "Push O(log n), pop O(log n), peek O(1).",
        },
        "deep_concept": r'''
A heap is not a sorted structure — it's *partially* sorted. The exact
order of siblings is unspecified; only the parent-child relation is
fixed. This is why iterating a heap does *not* give sorted output: you
must repeatedly pop to extract in order.

Heaps support O(n) bulk construction (Floyd's heapify) — see
`heap-array-impl`.
''',
        "confusion_notes": [
            {
                "question": "Why does Python only give us a min-heap? How do I get a max-heap?",
                "answer": "The standard library chose min-heap for simplicity. Two common tricks: (1) push negated values for numeric data: `heappush(h, -x)` and read with `-h[0]`; (2) for non-numeric or composite keys, push tuples like `(-priority, item)`.",
            },
            {
                "question": "If a heap isn't sorted, why is `heap[0]` the min?",
                "answer": "Because the *root* is the unique node with no parent. Every other node has a parent ≤ itself, so every node ≥ root. Hence root = min. Siblings, however, can be in any order — that's why a heap is 'partially' sorted.",
            },
            {
                "question": "Heap vs BST — when do I choose which?",
                "answer": "Heap: when you only need the extreme repeatedly. BST: when you need ordered traversal, lookup of arbitrary keys, range queries, or floor/ceil. Heaps are simpler to implement and have better constants for their narrow use case.",
            },
        ],
        "summary": "A heap is a partially-sorted complete binary tree stored in an array. O(log n) push/pop, O(1) peek. Min-heap default in Python; negate for max-heap.",
    },

    # ------------------------------------------------------------------
    # 2) Min/Max Heap Implementation
    # ------------------------------------------------------------------
    {
        "id": "min-max-heap-impl",
        "title": "Implement Min-Heap and Max-Heap from Scratch",
        "step_id": 11,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["heap", "implementation"],
        "what_this_teaches": "How sift-up and sift-down work mechanically. Reading and writing the array indices for parent/child.",
        "pattern": "Hand-written heap operations.",
        "prerequisite_lessons": ["arrays"],
        "prerequisite_problems": ["heap-introduction"],
        "next_problems": ["heap-array-impl", "is-max-heap"],
        "resources": [
            {"label": "Striver — Heap implementation", "url": "https://takeuforward.org/data-structure/min-heap-max-heap-priority-queue/"},
            _SHEET,
        ],
        "understanding": r'''
Implement a min-heap (and a max-heap) supporting `push(x)`, `pop()`,
`peek()`, `size()`, all using an underlying array.

This is the canonical interview-flavored exercise on heaps. After
writing it once, the library `heapq` stops feeling magical.
''',
        "brute_force": {
            "explanation": r'''
Use a Python list and on each pop call `min(list)` + remove. O(n) per
op. Acceptable only at the smallest scales.
''',
            "code": r'''
class SlowMinHeap:
    def __init__(self):
        self.data = []
    def push(self, x):
        self.data.append(x)
    def peek(self):
        return min(self.data)
    def pop(self):
        m = min(self.data)
        self.data.remove(m)
        return m
''',
            "complexity": "Push O(1), peek O(n), pop O(n).",
        },
        "thought_process": r'''
Switch to the standard array layout: parent of i is `(i − 1) // 2`,
children are `2i + 1`, `2i + 2`.

**Push** = append to the end (preserves completeness), then *sift up*:
while the new node violates the heap property with its parent, swap up.
At most ⌈log₂ n⌉ swaps.

**Pop** = swap root with the last element (preserves completeness),
truncate the last, then *sift down*: while the root violates the heap
property with its smaller child, swap down. At most ⌈log₂ n⌉ swaps.
''',
        "optimized": {
            "explanation": r'''
Class with O(log n) push and pop. Showing the min-heap; max-heap is
identical with the comparator flipped.
''',
            "code": r'''
class MinHeap:
    def __init__(self):
        self.a = []

    def size(self):
        return len(self.a)

    def peek(self):
        return self.a[0]                # O(1)

    def push(self, x):
        self.a.append(x)                # add at the next leaf slot
        self._sift_up(len(self.a) - 1)

    def pop(self):
        top = self.a[0]
        last = self.a.pop()             # remove last leaf
        if self.a:                      # if there are still items
            self.a[0] = last
            self._sift_down(0)
        return top

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self.a[i] < self.a[parent]:
                self.a[i], self.a[parent] = self.a[parent], self.a[i]
                i = parent
            else:
                return

    def _sift_down(self, i):
        n = len(self.a)
        while True:
            left  = 2 * i + 1
            right = 2 * i + 2
            smallest = i
            if left  < n and self.a[left]  < self.a[smallest]: smallest = left
            if right < n and self.a[right] < self.a[smallest]: smallest = right
            if smallest == i:
                return
            self.a[i], self.a[smallest] = self.a[smallest], self.a[i]
            i = smallest


class MaxHeap(MinHeap):
    # Flip comparisons. Cleaner: store -x; but here we keep it explicit.
    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self.a[i] > self.a[parent]:
                self.a[i], self.a[parent] = self.a[parent], self.a[i]
                i = parent
            else:
                return

    def _sift_down(self, i):
        n = len(self.a)
        while True:
            left  = 2 * i + 1
            right = 2 * i + 2
            largest = i
            if left  < n and self.a[left]  > self.a[largest]: largest = left
            if right < n and self.a[right] > self.a[largest]: largest = right
            if largest == i:
                return
            self.a[i], self.a[largest] = self.a[largest], self.a[i]
            i = largest
''',
            "complexity": "Push O(log n), pop O(log n), peek O(1).",
        },
        "deep_concept": r'''
The reason heap operations are O(log n): each fix-up traverses at most
one root-to-leaf path, and a complete tree of n nodes has height
⌊log₂ n⌋.

In production-quality code you would also handle: equal elements,
key updates (decrease-key for Dijkstra), and an `_heapify` bulk-build.
''',
        "confusion_notes": [
            {
                "question": "Why pop the last element first, then place it at the root?",
                "answer": "Removing the root would break completeness (we'd have a hole at the top). Trick: take the *last* leaf (which we can remove without breaking completeness), put it at the root, and sift it down. The original root value was already saved to return.",
            },
            {
                "question": "Why use `(i - 1) // 2` for parent?",
                "answer": "Because children are at `2i + 1` and `2i + 2`. Inverting that mapping: if i is odd it came from `2p + 1` so `p = (i - 1) / 2`; if i is even (and > 0) it came from `2p + 2` so `p = (i - 2) / 2`. Both cases simplify to `(i - 1) // 2` with integer floor division.",
            },
        ],
        "summary": "Heap = array with parent/child index arithmetic. Push appends and sifts up; pop swaps root with last, truncates, and sifts down. Both O(log n).",
    },

    # ------------------------------------------------------------------
    # 3) Heap as Array — Floyd's Heapify
    # ------------------------------------------------------------------
    {
        "id": "heap-array-impl",
        "title": "Build a Heap in O(n) — Floyd's heapify",
        "step_id": 11,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["heap", "heapify", "implementation"],
        "what_this_teaches": "Building a heap from an unsorted array in O(n), not O(n log n). Why bottom-up sift-downs are linear.",
        "pattern": "Bulk heap construction.",
        "prerequisite_lessons": ["amortized-analysis"],
        "prerequisite_problems": ["min-max-heap-impl"],
        "next_problems": ["is-max-heap"],
        "resources": [
            {"label": "CLRS — Building a heap", "url": "https://en.wikipedia.org/wiki/Binary_heap#Building_a_heap"},
            _SHEET,
        ],
        "understanding": r'''
Given an unsorted array, turn it into a valid heap in-place.

The naïve approach: call `push` n times → O(n log n). But there is a
strictly faster way: walk indices from `n // 2 - 1` down to `0` and call
`sift_down` on each. The total work is O(n) because nodes near the
bottom (where most of them live) sift down very little, while the few
near the top sift down deep.
''',
        "brute_force": {
            "explanation": r'''
Repeatedly push: O(n log n).
''',
            "code": r'''
import heapq
def build_brute(arr):
    h = []
    for x in arr:
        heapq.heappush(h, x)
    return h
''',
            "complexity": "Time O(n log n).",
        },
        "thought_process": r'''
Most of the n nodes are leaves and trivially satisfy the heap property —
half of them in fact (indices `n // 2 .. n − 1`). We only need to fix
the internal nodes, working *bottom-up* so that when we sift down node
i, both of its subtrees are already valid heaps.

**Why total O(n)?** A node at height h takes O(h) work to sift down.
The number of nodes at height h is ≤ ⌈n / 2^(h+1)⌉. Summing
`Σ h · n / 2^(h+1)` converges to 2n. Hence O(n).
''',
        "optimized": {
            "explanation": r'''
Floyd's algorithm: sift-down each internal node from the last to the
first. The Python standard library's `heapq.heapify` does exactly this.
''',
            "code": r'''
def sift_down(a, i, n):
    while True:
        left  = 2 * i + 1
        right = 2 * i + 2
        smallest = i
        if left  < n and a[left]  < a[smallest]: smallest = left
        if right < n and a[right] < a[smallest]: smallest = right
        if smallest == i:
            return
        a[i], a[smallest] = a[smallest], a[i]
        i = smallest

def build_heap(a):
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(a, i, n)
    return a

# verify against heapq
import heapq
arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
mine = build_heap(arr.copy())
ref = arr.copy(); heapq.heapify(ref)
print(mine == ref)              # may differ — both are valid heaps
print(mine[0], ref[0])          # but min at root is the same
''',
            "complexity": "Time O(n), space O(1) extra.",
        },
        "deep_concept": r'''
This is a classic example of an algorithm where the *intuitive* upper
bound (each call is O(log n), so n calls = O(n log n)) is loose. A
tighter amortized analysis exploits the *distribution* of node heights
— half the nodes have height 0, a quarter height 1, an eighth height 2,
and so on. The sum is geometric and bounded by 2n.
''',
        "confusion_notes": [
            {
                "question": "Why start at `n // 2 - 1` and not at `n - 1`?",
                "answer": "Because indices `[n // 2, n - 1]` are leaves (they have no children in the array). They already satisfy the heap property vacuously. Starting earlier is wasted work.",
            },
            {
                "question": "Two different heapified arrays both 'work' — is that OK?",
                "answer": "Yes. A heap is a partial order, not a sort. Many array layouts satisfy the heap property for the same multiset of values. As long as `a[i] ≤ a[2i + 1]` and `a[i] ≤ a[2i + 2]` for every valid i, it is a valid min-heap.",
            },
        ],
        "summary": "Floyd's heapify: sift-down from index `n // 2 - 1` down to 0 → O(n) total.",
    },

    # ------------------------------------------------------------------
    # 4) Is Max Heap
    # ------------------------------------------------------------------
    {
        "id": "is-max-heap",
        "title": "Check if an Array is a Max-Heap",
        "step_id": 11,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["heap", "validation"],
        "what_this_teaches": "Verifying the heap invariant — a one-pass check using the parent-child index formulas.",
        "pattern": "Invariant check by index arithmetic.",
        "prerequisite_lessons": ["arrays"],
        "prerequisite_problems": ["heap-array-impl"],
        "next_problems": ["kth-largest"],
        "resources": [
            {"label": "GFG — Check if a given array is a Heap", "url": "https://www.geeksforgeeks.org/how-to-check-if-a-given-array-represents-a-binary-heap/"},
            _SHEET,
        ],
        "understanding": r'''
Given an array, determine whether it represents a max-heap. That is,
for every node i with a child c, check `a[i] >= a[c]`.

For a min-heap, flip the inequality.
''',
        "brute_force": {
            "explanation": r'''
For every node, list its children explicitly using `2i + 1`, `2i + 2`,
and check both. There is no asymptotically faster method since we must
read every parent-child pair at least once.
''',
            "code": r'''
def is_max_heap_brute(a):
    n = len(a)
    for i in range(n):
        left, right = 2 * i + 1, 2 * i + 2
        if left < n and a[i] < a[left]:
            return False
        if right < n and a[i] < a[right]:
            return False
    return True
''',
            "complexity": "Time O(n), space O(1).",
        },
        "thought_process": r'''
Already optimal. The slight refinement is to loop only up to the last
internal node `n // 2 - 1` — leaves cannot violate the heap property
because they have no children.
''',
        "optimized": {
            "explanation": r'''
Loop only over internal nodes.
''',
            "code": r'''
def is_max_heap(a):
    n = len(a)
    for i in range((n // 2) - 1 + 1):   # 0..(n//2 - 1)
        left, right = 2 * i + 1, 2 * i + 2
        if left < n and a[i] < a[left]:
            return False
        if right < n and a[i] < a[right]:
            return False
    return True
''',
            "complexity": "Time O(n), space O(1).",
        },
        "deep_concept": r'''
The function is essentially a structural assertion. In production
code, you might call this in test cases after `heapify` or
`heappush/heappop` sequences to verify your implementation.
''',
        "confusion_notes": [
            {
                "question": "Do I need to verify the *complete tree* property?",
                "answer": "No — if the heap is stored in an array `a[0..n-1]` with no gaps, completeness is automatic. The completeness check matters only for *pointer-based* heaps; for array-backed ones, we only verify the heap *property* (parent ≥/≤ children).",
            },
        ],
        "summary": "Loop internal nodes, compare each to its children, return False on first violation.",
    },

    # ------------------------------------------------------------------
    # 5) Kth Smallest Element
    # ------------------------------------------------------------------
    {
        "id": "kth-smallest",
        "title": "Kth Smallest Element in an Array",
        "step_id": 11,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["heap", "selection"],
        "what_this_teaches": "How a *max-heap of size k* finds the Kth smallest in O(n log k).",
        "pattern": "Bounded-size heap.",
        "prerequisite_lessons": ["heap"],
        "prerequisite_problems": ["heap-introduction", "kth-largest"],
        "next_problems": ["k-most-frequent"],
        "resources": [
            {"label": "LeetCode 215 — Kth Largest Element (use min-heap of k for smallest)", "url": "https://leetcode.com/problems/kth-largest-element-in-an-array/"},
            _SHEET,
        ],
        "understanding": r'''
Given an array `nums` and integer `k`, return the Kth smallest element.

Symmetry with Kth Largest: use a *max-heap* of size k to keep the
"smallest k so far". The root of that max-heap is the largest among the
k smallest — and once we have processed everything, that root is
exactly the Kth smallest in the array.
''',
        "brute_force": {
            "explanation": r'''
Sort the array, return `nums[k - 1]`. O(n log n).
''',
            "code": r'''
def kth_smallest_brute(nums, k):
    return sorted(nums)[k - 1]
''',
            "complexity": "Time O(n log n), space O(n) if sort is out-of-place.",
        },
        "thought_process": r'''
Two strategies dominate:
1. **Heap of size k.** Maintain a max-heap of the smallest k items
   seen. When a new item arrives, if heap size < k, push; else if new
   item < heap top, replace. After n items, heap top = Kth smallest.
   O(n log k) time, O(k) memory.
2. **Quickselect.** Partition-based selection in expected O(n).
   Worst-case O(n²), but with randomized pivoting, average is O(n).
''',
        "optimized": {
            "explanation": r'''
Max-heap of size k, using Python's heapq with negated values.
''',
            "code": r'''
import heapq

def kth_smallest(nums, k):
    heap = []                              # we'll store negatives → max-heap
    for x in nums:
        if len(heap) < k:
            heapq.heappush(heap, -x)
        elif x < -heap[0]:                 # x smaller than current biggest of top-k
            heapq.heapreplace(heap, -x)
    return -heap[0]
''',
            "complexity": "Time O(n log k), space O(k).",
        },
        "deep_concept": r'''
The 'heap of size K' template generalizes to: top-K largest (min-heap of
k), top-K smallest (max-heap of k), top-K most-frequent (min-heap of k
ordered by frequency), top-K closest points (max-heap of k ordered by
distance), etc.

When n is huge and k is small, this is dramatically faster than
sorting: instead of n log n, we get n log k.
''',
        "confusion_notes": [
            {
                "question": "Why max-heap for the Kth *smallest*?",
                "answer": "Because we want to keep the *smallest* k elements seen, and the worst (largest) among them sits at the root. New items only matter if they are smaller than that worst.",
            },
            {
                "question": "Why `heapreplace` instead of pop + push?",
                "answer": "Performance: `heapreplace` does a single sift-down (one O(log k) pass) instead of two separate ones. Same outcome, half the work.",
            },
        ],
        "summary": "Max-heap of size k tracks 'best k so far'. Top of heap after one pass is the Kth smallest.",
    },

    # ------------------------------------------------------------------
    # 6) Sort Characters By Frequency / Replace Each Element By Its Rank
    # ------------------------------------------------------------------
    {
        "id": "replace-by-rank",
        "title": "Replace Each Element by Its Rank",
        "step_id": 11,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["heap", "ranking", "hash-map"],
        "what_this_teaches": "Using a heap (or sort) to assign positional ranks to elements, then mapping them back.",
        "pattern": "Rank assignment via sorted pairs.",
        "prerequisite_lessons": ["sorting", "hashing"],
        "prerequisite_problems": ["heap-introduction"],
        "next_problems": ["task-scheduler"],
        "resources": [
            {"label": "GFG — Replace elements with their respective rank", "url": "https://www.geeksforgeeks.org/replace-elements-with-their-rank-in-the-array/"},
            _SHEET,
        ],
        "understanding": r'''
Given an array, replace each element with its **rank** (its 1-based
position in the sorted order). Equal elements share the same rank.

**Example:** `[40, 10, 20, 30]` → ranks `[4, 1, 2, 3]`.
''',
        "brute_force": {
            "explanation": r'''
For each element x, count how many distinct elements are ≤ x. O(n²).
''',
            "code": r'''
def replace_by_rank_brute(arr):
    distinct = sorted(set(arr))
    rank_of = {v: i + 1 for i, v in enumerate(distinct)}
    return [rank_of[x] for x in arr]
''',
            "complexity": "Time O(n log n) — actually already efficient via the dict map.",
        },
        "thought_process": r'''
The "heap" approach: push pairs `(value, original_index)` into a
min-heap, pop them in order, and assign ranks as you pop. But honestly
the cleanest method is `sorted(set(arr))` + dict lookup — same
asymptotics as a heap, simpler code.
''',
        "optimized": {
            "explanation": r'''
Sort distinct values, build a value→rank map, then translate the array.
''',
            "code": r'''
def replace_by_rank(arr):
    distinct = sorted(set(arr))
    rank = {v: i + 1 for i, v in enumerate(distinct)}
    return [rank[x] for x in arr]
''',
            "complexity": "Time O(n log n), space O(n).",
        },
        "deep_concept": r'''
**Rank** comes up constantly in coordinate-compression problems: when
the actual values may be huge but you only care about relative
positions, replace each value by its rank to fit a fixed-size structure
(e.g., a Fenwick tree of size n).
''',
        "confusion_notes": [
            {
                "question": "Why dedupe before ranking?",
                "answer": "Because equal values must receive equal ranks, and we want consecutive ranks for distinct values. `set()` + sort gives us each distinct value exactly once in sorted order.",
            },
        ],
        "summary": "Sort distinct values, build `value → rank` dict, look each element up.",
    },

    # ------------------------------------------------------------------
    # 7) Task Scheduler
    # ------------------------------------------------------------------
    {
        "id": "task-scheduler",
        "title": "Task Scheduler",
        "step_id": 11,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["heap", "greedy", "scheduling"],
        "what_this_teaches": "Greedy scheduling using a max-heap and a cooldown queue. Also a clean closed-form via counting.",
        "pattern": "Max-heap + temporary holding queue, OR formula via most-frequent task.",
        "prerequisite_lessons": ["heap", "greedy"],
        "prerequisite_problems": ["heap-introduction"],
        "next_problems": ["hand-of-straights", "k-most-frequent"],
        "resources": [
            _lc(621, "task-scheduler"),
            _SHEET,
        ],
        "understanding": r'''
You have a list of CPU tasks, each labeled with a single letter. The
CPU processes one task per unit of time. After running a task X, you
must wait `n` time units before running X again. (Other tasks or idle
time can fill the gap.) Find the minimum total time to finish all
tasks.

**Example:** `tasks = ["A","A","A","B","B","B"], n = 2` → 8.
Schedule: `A B idle A B idle A B`.

**Two solutions:**
1. Simulate with a max-heap of task counts + a cooldown queue (works
   when tasks have priorities or in real scheduling).
2. Closed-form: count the most frequent task, fmax. The answer is
   `max(len(tasks), (fmax - 1) * (n + 1) + (# tasks with count == fmax))`.
   This is the *real* trick interviewers want.
''',
        "brute_force": {
            "explanation": r'''
Simulate one tick at a time using a max-heap of counts and a queue of
"cooling" tasks. Each iteration: pop the largest count, decrement it,
push to the cooling queue with a release-tick. Whenever cooled tasks
become ready, push them back into the heap. Otherwise the CPU is idle.
''',
            "code": r'''
import heapq
from collections import Counter, deque

def least_interval_sim(tasks, n):
    counts = Counter(tasks)
    heap = [-c for c in counts.values()]   # max-heap of remaining counts
    heapq.heapify(heap)
    cool = deque()                          # (release_time, neg_count)
    t = 0
    while heap or cool:
        t += 1
        if heap:
            c = heapq.heappop(heap) + 1     # decrement count (c was negative)
            if c < 0:
                cool.append((t + n, c))
        if cool and cool[0][0] == t:
            heapq.heappush(heap, cool.popleft()[1])
    return t
''',
            "complexity": "Time O(total_tasks · log 26) — effectively O(total_tasks). Space O(26).",
        },
        "thought_process": r'''
The greedy intuition: every cycle of `n + 1` slots, the most-frequent
task X must run at most once. So we lay out `fmax − 1` full cycles
followed by one final slot for the last X. Total slots from this
skeleton: `(fmax − 1) · (n + 1) + 1`. If multiple tasks share that
maximum frequency, each one adds `+1` to the final slot. So:

`answer = (fmax − 1) · (n + 1) + (#tasks with count == fmax)`.

But if we have so many tasks that they fill every slot anyway, the
answer is simply `len(tasks)`. Take the max of the two.
''',
        "optimized": {
            "explanation": r'''
Closed-form computation in O(N) (or O(N + 26) depending on view).
''',
            "code": r'''
from collections import Counter

def least_interval(tasks, n):
    cnt = Counter(tasks)
    fmax = max(cnt.values())
    num_max = sum(1 for c in cnt.values() if c == fmax)
    return max(len(tasks), (fmax - 1) * (n + 1) + num_max)
''',
            "complexity": "Time O(N), space O(26).",
        },
        "deep_concept": r'''
Why does the formula work? Think of the schedule as a 2-D grid of `fmax`
rows × `(n + 1)` columns. Place one copy of the most-frequent task per
row in column 0. The rest of the row holds either other tasks or idle.
The last row needs only as many slots as there are tasks with the
maximum frequency. The grid's filled-area equals
`(fmax − 1) · (n + 1) + num_max`. If you have so many other tasks that
they spill outside the grid, the cooldown is never the binding
constraint and the answer is just the task count.
''',
        "confusion_notes": [
            {
                "question": "Why `max(len(tasks), ...)`? Doesn't the formula always dominate?",
                "answer": "No. If you have many low-frequency tasks, every slot of the schedule is filled and there is no idle time. The cooldown never causes a wait. In that case `len(tasks)` is the true answer and the formula would underestimate.",
            },
            {
                "question": "Does the order of execution we choose matter?",
                "answer": "For *total time* — no. The formula proves it: regardless of order, as long as we are 'greedy' about running the most-frequent next, we hit the optimal duration.",
            },
        ],
        "summary": "Either simulate with max-heap + cooldown queue, or use the formula `(fmax-1)*(n+1) + num_max`, capped below by `len(tasks)`.",
    },

    # ------------------------------------------------------------------
    # 8) Hand of Straights
    # ------------------------------------------------------------------
    {
        "id": "hand-of-straights",
        "title": "Hand of Straights",
        "step_id": 11,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["heap", "greedy", "hash-map"],
        "what_this_teaches": "Greedy with the smallest available card. A min-heap (or sorted multiset) gives O(n log n).",
        "pattern": "Repeatedly extract minimum and consume k consecutive values.",
        "prerequisite_lessons": ["heap", "greedy"],
        "prerequisite_problems": ["heap-introduction"],
        "next_problems": ["task-scheduler"],
        "resources": [
            _lc(846, "hand-of-straights"),
            _SHEET,
        ],
        "understanding": r'''
Alice has cards in `hand` and wants to rearrange them into groups of
exactly `groupSize` consecutive numbers each. Return `True` iff this is
possible.

**Example:** `hand = [1,2,3,6,2,3,4,7,8], groupSize = 3` → True. Groups:
`[1,2,3], [2,3,4], [6,7,8]`.
''',
        "brute_force": {
            "explanation": r'''
Sort the hand. Repeatedly try to peel off `groupSize` consecutive cards
starting from the smallest available. Use a frequency map to track
remaining counts.
''',
            "code": r'''
from collections import Counter

def is_n_straight_hand_brute(hand, groupSize):
    if len(hand) % groupSize != 0:
        return False
    cnt = Counter(hand)
    for card in sorted(cnt):
        if cnt[card] == 0:
            continue
        need = cnt[card]                # we must form `need` groups starting at this card
        for offset in range(groupSize):
            if cnt[card + offset] < need:
                return False
            cnt[card + offset] -= need
    return True
''',
            "complexity": "Time O(n log n), space O(n).",
        },
        "thought_process": r'''
The greedy is: the smallest remaining card *must* be the start of some
group (no smaller card can pair with it). So peel off
`groupSize` consecutive starting at that smallest. Repeat.

Implementation choices: a sorted Counter is the cleanest; a min-heap
also works (pop, consume k consecutive by re-checking counts).
''',
        "optimized": {
            "explanation": r'''
The same greedy, but using a min-heap for the available cards. Each
group requires one heap-pop and k-1 lookups. This shines when groupSize
is small.
''',
            "code": r'''
import heapq
from collections import Counter

def is_n_straight_hand(hand, groupSize):
    if len(hand) % groupSize != 0:
        return False
    cnt = Counter(hand)
    heap = list(cnt.keys())
    heapq.heapify(heap)
    while heap:
        smallest = heap[0]
        if cnt[smallest] == 0:
            heapq.heappop(heap)
            continue
        need = cnt[smallest]
        for offset in range(groupSize):
            v = smallest + offset
            if cnt[v] < need:
                return False
            cnt[v] -= need
    return True
''',
            "complexity": "Time O(n log n), space O(n).",
        },
        "deep_concept": r'''
The 'smallest must start a group' argument is a textbook **exchange
argument**: if it didn't start a group, the group containing it would
have a smaller card too, contradicting smallest-ness.
''',
        "confusion_notes": [
            {
                "question": "Why does the smallest card *have* to start a group?",
                "answer": "Because every group has a minimum, and groups are runs of consecutive integers. If the smallest available card weren't the start, the group containing it would need an even smaller card — but none exists. So the smallest is always the start of some group.",
            },
        ],
        "summary": "Greedy: peel off groups starting from the smallest available card; use a min-heap or sorted Counter.",
    },

    # ------------------------------------------------------------------
    # 9) Design Twitter (LeetCode 355)
    # ------------------------------------------------------------------
    {
        "id": "design-twitter",
        "title": "Design Twitter",
        "step_id": 11,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["heap", "design", "hash-map"],
        "what_this_teaches": "Combining heaps with hash-maps to build a real-time feed. Heap merging across multiple sources.",
        "pattern": "K-way merge using a max-heap.",
        "prerequisite_lessons": ["heap"],
        "prerequisite_problems": ["merge-k-sorted-lists"],
        "next_problems": ["median-from-stream"],
        "resources": [
            _lc(355, "design-twitter"),
            _SHEET,
        ],
        "understanding": r'''
Design a Twitter-like system supporting:
- `postTweet(userId, tweetId)`
- `getNewsFeed(userId)` — 10 most recent tweets by the user and the people they follow
- `follow(followerId, followeeId)`
- `unfollow(followerId, followeeId)`

The interesting operation is `getNewsFeed`. We must merge the most
recent tweets of `userId` and all of `userId`'s followees. This is a
small k-way merge.
''',
        "brute_force": {
            "explanation": r'''
On each `getNewsFeed`, gather all tweets from the user and all followees
into a list, sort by time descending, take the first 10. Slow if a user
follows many active accounts.
''',
            "code": r'''
class TwitterBrute:
    def __init__(self):
        self.tweets = {}      # user -> list of (time, tweetId)
        self.follow_map = {}  # user -> set of followees
        self.t = 0
    def postTweet(self, u, tid):
        self.tweets.setdefault(u, []).append((self.t, tid))
        self.t += 1
    def getNewsFeed(self, u):
        users = self.follow_map.get(u, set()) | {u}
        all_tweets = []
        for v in users:
            all_tweets.extend(self.tweets.get(v, []))
        all_tweets.sort(key=lambda x: -x[0])
        return [tid for _, tid in all_tweets[:10]]
    def follow(self, a, b):
        self.follow_map.setdefault(a, set()).add(b)
    def unfollow(self, a, b):
        self.follow_map.get(a, set()).discard(b)
''',
            "complexity": "getNewsFeed in O(M log M) where M is total tweets across followees.",
        },
        "thought_process": r'''
Each user's tweets are stored in chronological order. For
`getNewsFeed`, run a k-way merge where each followee contributes a
pointer to their latest unread tweet. A max-heap keyed by tweet time
extracts the top 10 in O(10 · log k) per call, where k = number of
followees.
''',
        "optimized": {
            "explanation": r'''
Max-heap based k-way merge. Each user's tweet list is iterated from the
back (most recent). Heap entries are `(-time, tweetId, user_idx, next_idx)`.
''',
            "code": r'''
import heapq
from collections import defaultdict

class Twitter:
    def __init__(self):
        self.t = 0
        self.tweets = defaultdict(list)        # user -> [(time, tweetId), ...]
        self.followees = defaultdict(set)      # user -> {followees}

    def postTweet(self, u, tid):
        self.tweets[u].append((self.t, tid))
        self.t += 1

    def follow(self, a, b):
        self.followees[a].add(b)

    def unfollow(self, a, b):
        self.followees[a].discard(b)

    def getNewsFeed(self, u):
        users = self.followees[u] | {u}
        heap = []
        # seed heap with each user's most-recent tweet
        for v in users:
            if self.tweets[v]:
                last = len(self.tweets[v]) - 1
                time, tid = self.tweets[v][last]
                heapq.heappush(heap, (-time, tid, v, last - 1))
        feed = []
        while heap and len(feed) < 10:
            neg_time, tid, v, prev = heapq.heappop(heap)
            feed.append(tid)
            if prev >= 0:
                time, tid2 = self.tweets[v][prev]
                heapq.heappush(heap, (-time, tid2, v, prev - 1))
        return feed
''',
            "complexity": "postTweet O(1); getNewsFeed O((f + 10) log f) where f is followee count.",
        },
        "deep_concept": r'''
This is a hidden 'merge K sorted lists' problem. Each user's tweet
sequence is sorted by time; we are merging the top 10 of K sorted
sequences. The same heap pattern shows up in log aggregation, search
result fan-in, and database joins.
''',
        "confusion_notes": [
            {
                "question": "Why store tweets in a list and not in a heap?",
                "answer": "Tweets are *posted* in time order, so the list is already sorted. A heap would be overkill on a per-user basis. We use a heap only at merge time, across users.",
            },
            {
                "question": "Should `follow_map` include the user themselves?",
                "answer": "Some designs do; this one keeps them separate and adds `{u}` explicitly inside getNewsFeed. Both styles are fine — just be consistent.",
            },
        ],
        "summary": "Per-user chronological lists + a max-heap for k-way merge on getNewsFeed.",
    },

    # ------------------------------------------------------------------
    # 10) Merge K Sorted Lists
    # ------------------------------------------------------------------
    {
        "id": "merge-k-sorted-lists",
        "title": "Merge K Sorted Lists",
        "step_id": 11,
        "lecture_id": 2,
        "difficulty": "hard",
        "tags": ["heap", "linked-list", "k-way-merge"],
        "what_this_teaches": "The canonical k-way merge with a min-heap.",
        "pattern": "Min-heap of (value, list-pointer).",
        "prerequisite_lessons": ["heap", "linked-list"],
        "prerequisite_problems": ["heap-introduction"],
        "next_problems": ["median-from-stream", "design-twitter"],
        "resources": [
            _lc(23, "merge-k-sorted-lists"),
            _SHEET,
        ],
        "understanding": r'''
Given an array of k linked lists, each sorted in ascending order, merge
them into one sorted linked list.

**Example:** `[[1,4,5], [1,3,4], [2,6]]` → `1 → 1 → 2 → 3 → 4 → 4 → 5 → 6`.
''',
        "brute_force": {
            "explanation": r'''
Concatenate everything into a list, sort, rebuild as a linked list.
O(N log N) where N is total elements.
''',
            "code": r'''
def merge_brute(lists):
    vals = []
    for head in lists:
        while head:
            vals.append(head.val)
            head = head.next
    vals.sort()
    dummy = ListNode(0); cur = dummy
    for v in vals:
        cur.next = ListNode(v); cur = cur.next
    return dummy.next
''',
            "complexity": "Time O(N log N), space O(N).",
        },
        "thought_process": r'''
We can do better: each pop only takes O(log k) instead of O(log N)
because the heap holds at most k items at any time. Total: O(N log k).
''',
        "optimized": {
            "explanation": r'''
Push the head of each list into a min-heap. Pop the smallest, append to
the result, push the next node of that list. Tie-break by list index
(so ListNode comparison doesn't error).
''',
            "code": r'''
import heapq

class ListNode:
    def __init__(self, val=0, nxt=None):
        self.val = val; self.next = nxt

def merge_k_lists(lists):
    heap = []
    for i, head in enumerate(lists):
        if head:
            heapq.heappush(heap, (head.val, i, head))
    dummy = ListNode(0)
    cur = dummy
    while heap:
        val, i, node = heapq.heappop(heap)
        cur.next = node
        cur = node
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next
''',
            "complexity": "Time O(N log k), space O(k).",
        },
        "deep_concept": r'''
**K-way merge** is the bread-and-butter of external sorting and
distributed systems. Whenever you need a single sorted output from K
sorted sources, this is the template. The space O(k) is the secret
weapon — you never load all of N into memory.
''',
        "confusion_notes": [
            {
                "question": "Why add the list index `i` as the second tuple element?",
                "answer": "Because if two nodes have equal values, Python's tuple comparison falls through to the next field. ListNode objects don't support `<`, so we provide `i` to break the tie deterministically.",
            },
            {
                "question": "Is divide-and-conquer (pairwise merge) also O(N log k)?",
                "answer": "Yes — pairwise merging in a balanced binary fashion gives the same complexity. Both are standard. The heap version is arguably simpler.",
            },
        ],
        "summary": "Min-heap of (value, list_index, node). Pop, append, push next. O(N log k).",
    },

    # ------------------------------------------------------------------
    # 11) Find Median from Data Stream
    # ------------------------------------------------------------------
    {
        "id": "median-from-stream",
        "title": "Find Median from Data Stream",
        "step_id": 11,
        "lecture_id": 3,
        "difficulty": "hard",
        "tags": ["heap", "two-heaps", "streaming"],
        "what_this_teaches": "Classic two-heap trick: a max-heap for the lower half, a min-heap for the upper half, balanced.",
        "pattern": "Two-heap median.",
        "prerequisite_lessons": ["heap"],
        "prerequisite_problems": ["heap-introduction"],
        "next_problems": ["max-sum-combinations"],
        "resources": [
            _lc(295, "find-median-from-data-stream"),
            _SHEET,
        ],
        "understanding": r'''
Design a class that supports:
- `addNum(int x)` — accept the next number from a stream
- `findMedian()` — return the median of all numbers seen so far

**Example:** add 1, add 2 → median 1.5; add 3 → median 2.

**Challenge:** sorting after every insert is O(n log n) per query. We
want O(log n) per insert and O(1) per query.
''',
        "brute_force": {
            "explanation": r'''
Keep a sorted list (`bisect.insort`). Insert: O(n). Query: O(1).
''',
            "code": r'''
import bisect
class MedianFinderBrute:
    def __init__(self): self.a = []
    def addNum(self, x): bisect.insort(self.a, x)
    def findMedian(self):
        n = len(self.a)
        return self.a[n // 2] if n % 2 else (self.a[n // 2 - 1] + self.a[n // 2]) / 2
''',
            "complexity": "addNum O(n), findMedian O(1).",
        },
        "thought_process": r'''
Imagine splitting the stream into two halves at the median:
- `lo`: the smaller half — we care about its maximum.
- `hi`: the larger half — we care about its minimum.

If we use a **max-heap for lo** and a **min-heap for hi**, both
extremes are accessible in O(1). Median is either `lo.top` (odd total,
lo larger), or `(lo.top + hi.top) / 2` (even total).

Insertion: push into the appropriate heap, then rebalance so the sizes
differ by at most 1.
''',
        "optimized": {
            "explanation": r'''
Two heaps, sizes kept balanced.
''',
            "code": r'''
import heapq

class MedianFinder:
    def __init__(self):
        self.lo = []   # max-heap (store negatives)
        self.hi = []   # min-heap

    def addNum(self, x):
        # 1. push to lo (as negative for max-heap behavior)
        heapq.heappush(self.lo, -x)
        # 2. move the largest of lo into hi to keep lo ≤ hi
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        # 3. rebalance so that |lo| - |hi| in {0, 1}
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self):
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2
''',
            "complexity": "addNum O(log n), findMedian O(1).",
        },
        "deep_concept": r'''
The two-heap pattern works for any "running statistic that depends on
the median". Variants: kth-percentile from stream, running interquartile
range. The trick is always *split the data at the statistic of interest*.
''',
        "confusion_notes": [
            {
                "question": "Why always push to lo first, then move to hi?",
                "answer": "It's a uniform discipline that avoids special-casing. Pushing to lo and migrating the largest to hi enforces the invariant `max(lo) ≤ min(hi)` without us having to compare x to anything by hand.",
            },
            {
                "question": "What if we want the running median of just the last K elements (a sliding window)?",
                "answer": "That's harder — heaps don't support efficient deletion of arbitrary elements. Use a SortedList (Python's `sortedcontainers.SortedList`) or two heaps with lazy deletion.",
            },
        ],
        "summary": "max-heap on the lower half + min-heap on the upper half. Push to lo, migrate to hi, rebalance. Median in O(1).",
    },

    # ------------------------------------------------------------------
    # 12) Maximum Sum Combinations
    # ------------------------------------------------------------------
    {
        "id": "max-sum-combinations",
        "title": "Maximum Sum Combinations",
        "step_id": 11,
        "lecture_id": 3,
        "difficulty": "hard",
        "tags": ["heap", "combinations"],
        "what_this_teaches": "Top-K sums from two arrays via a max-heap with seen-set pruning.",
        "pattern": "K-best with branching exploration.",
        "prerequisite_lessons": ["heap"],
        "prerequisite_problems": ["heap-introduction", "kth-largest"],
        "next_problems": ["k-most-frequent"],
        "resources": [
            {"label": "InterviewBit — Maximum Sum Combinations", "url": "https://www.interviewbit.com/problems/maximum-sum-combinations/"},
            _SHEET,
        ],
        "understanding": r'''
Given two arrays `A` and `B` of size N each, and integer C, return the
top C maximum sums of the form `A[i] + B[j]`.

**Example:** `A = [1, 4, 2, 3], B = [2, 5, 1, 6], C = 3` →
top 3 sums = `[4 + 6, 3 + 6, 4 + 5]` = `[10, 9, 9]`.
''',
        "brute_force": {
            "explanation": r'''
Enumerate all N² pairs, sort the sums, take the top C.
''',
            "code": r'''
def max_combinations_brute(A, B, C):
    sums = sorted((a + b for a in A for b in B), reverse=True)
    return sums[:C]
''',
            "complexity": "Time O(N² log N²), space O(N²).",
        },
        "thought_process": r'''
Sort both arrays descending. The largest sum is `A[0] + B[0]`. The
**next** candidates are either `A[1] + B[0]` or `A[0] + B[1]`. After
extracting one, push the two children into a max-heap, avoiding
duplicates with a `seen` set.

This is the same approach as "Kth smallest number in M sorted lists"
or "Top-K closest points to origin" — a heap-driven traversal of a
2-D grid of candidate sums.
''',
        "optimized": {
            "explanation": r'''
Max-heap of (negative sum, (i, j)), seen-set to dedupe.
''',
            "code": r'''
import heapq

def max_combinations(A, B, C):
    A = sorted(A, reverse=True)
    B = sorted(B, reverse=True)
    n = len(A)
    heap = [(-(A[0] + B[0]), 0, 0)]
    seen = {(0, 0)}
    out = []
    while heap and len(out) < C:
        s, i, j = heapq.heappop(heap)
        out.append(-s)
        for di, dj in ((1, 0), (0, 1)):
            ni, nj = i + di, j + dj
            if ni < n and nj < n and (ni, nj) not in seen:
                seen.add((ni, nj))
                heapq.heappush(heap, (-(A[ni] + B[nj]), ni, nj))
    return out
''',
            "complexity": "Time O(C log C), space O(C).",
        },
        "deep_concept": r'''
We are doing a *best-first search* on the 2-D grid `(i, j)` where edges
go right or down. The heap is a frontier; the seen-set prevents
revisiting. This pattern recurs in many "K best of cross-product"
problems.
''',
        "confusion_notes": [
            {
                "question": "Why do we need a `seen` set?",
                "answer": "Because `(i+1, j)` and `(i, j+1)` can both generate `(i+1, j+1)`. Without dedupe, the same cell would enter the heap twice and we'd pop it twice (wasting a slot and giving a duplicate sum).",
            },
        ],
        "summary": "Sort both arrays descending; explore the 2-D grid of (i, j) with a max-heap and a seen-set; pop C times.",
    },

    # ------------------------------------------------------------------
    # 13) Top K Frequent Elements (numbers)
    # ------------------------------------------------------------------
    {
        "id": "k-most-frequent",
        "title": "Top K Frequent Elements",
        "step_id": 11,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["heap", "hash-map", "bucket-sort"],
        "what_this_teaches": "Top-K via min-heap of size K, or O(n) via bucket sort.",
        "pattern": "Frequency map + bounded heap.",
        "prerequisite_lessons": ["heap", "hashing"],
        "prerequisite_problems": ["heap-introduction"],
        "next_problems": ["top-k-frequent"],
        "resources": [
            _lc(347, "top-k-frequent-elements"),
            _SHEET,
        ],
        "understanding": r'''
Given an integer array `nums` and integer `k`, return the k most
frequent elements (in any order).

**Example:** `nums = [1,1,1,2,2,3], k = 2` → `[1, 2]`.
''',
        "brute_force": {
            "explanation": r'''
Count frequencies, sort by frequency descending, take the first k.
O(n log n).
''',
            "code": r'''
from collections import Counter

def top_k_brute(nums, k):
    cnt = Counter(nums)
    return [v for v, _ in cnt.most_common(k)]
''',
            "complexity": "Time O(n log n).",
        },
        "thought_process": r'''
Two faster strategies:
1. **Min-heap of size k** ordered by frequency. O(n log k).
2. **Bucket sort** indexed by frequency 0..n; walk from highest bucket
   down, collecting until we have k items. O(n).
''',
        "optimized": {
            "explanation": r'''
Bucket sort solution: each bucket `buckets[freq]` holds all elements
with that frequency. Walk from `len(nums)` down to 1 collecting.
''',
            "code": r'''
from collections import Counter

def top_k_frequent(nums, k):
    cnt = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for v, f in cnt.items():
        buckets[f].append(v)
    out = []
    for f in range(len(buckets) - 1, 0, -1):
        for v in buckets[f]:
            out.append(v)
            if len(out) == k:
                return out
    return out
''',
            "complexity": "Time O(n), space O(n).",
        },
        "deep_concept": r'''
Bucket sort works here because frequencies are bounded by n. Whenever
your sort key has a small finite range, prefer bucketing over comparison
sort.
''',
        "confusion_notes": [
            {
                "question": "When is the heap approach preferable to bucket sort?",
                "answer": "When n is enormous but k is tiny — the heap uses O(k) memory whereas the bucket approach uses O(n). Also when frequencies are unbounded (e.g., from a stream).",
            },
        ],
        "summary": "Frequency count + bucket sort by frequency. Walk from highest bucket downward, take k.",
    },

    # ------------------------------------------------------------------
    # 14) Top K Frequent Words
    # ------------------------------------------------------------------
    {
        "id": "top-k-frequent",
        "title": "Top K Frequent Words",
        "step_id": 11,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["heap", "hash-map", "sorting"],
        "what_this_teaches": "Top-K with a custom *compound* comparator — frequency descending, then lexicographic ascending.",
        "pattern": "Heap with tuple keys.",
        "prerequisite_lessons": ["heap", "hashing"],
        "prerequisite_problems": ["k-most-frequent"],
        "next_problems": [],
        "resources": [
            _lc(692, "top-k-frequent-words"),
            _SHEET,
        ],
        "understanding": r'''
Given a list of strings `words` and integer `k`, return the k most
frequent words. The answer must be sorted by frequency from highest to
lowest. Words with the same frequency are sorted by their *lexicographic*
order.

**Example:** `words = ["i","love","leetcode","i","love","coding"], k = 2`
→ `["i", "love"]`. Both have freq 2; "i" comes before "love"
lexicographically.
''',
        "brute_force": {
            "explanation": r'''
Sort the (word, freq) pairs by the tuple `(-freq, word)`. Take the first
k. O(W log W).
''',
            "code": r'''
from collections import Counter

def top_k_words_brute(words, k):
    cnt = Counter(words)
    items = sorted(cnt.items(), key=lambda x: (-x[1], x[0]))
    return [w for w, _ in items[:k]]
''',
            "complexity": "Time O(W log W), space O(W).",
        },
        "thought_process": r'''
Using a heap is tricky because the comparator is *mixed*: frequency
descending and word *ascending*. Python's tuple comparison gives us
ascending by default, so we need to negate freq for the first key.

A min-heap of size k with key `(freq, NegatedWord)` doesn't work
because strings don't negate. The standard trick: use a **max-heap of
all items** with key `(-freq, word)` so the min of the heap is the
greatest by our combined criterion. Then pop k times.

If k is much smaller than n, you can also keep a min-heap of size k
with a custom wrapper class to invert string comparison.
''',
        "optimized": {
            "explanation": r'''
heappush all distinct (`-freq`, `word`) pairs, then heappop k times.
''',
            "code": r'''
import heapq
from collections import Counter

def top_k_frequent_words(words, k):
    cnt = Counter(words)
    heap = [(-f, w) for w, f in cnt.items()]
    heapq.heapify(heap)
    return [heapq.heappop(heap)[1] for _ in range(k)]
''',
            "complexity": "Time O(W + k log W), space O(W).",
        },
        "deep_concept": r'''
Whenever the comparator is multi-keyed and the natural sort directions
conflict, the elegant approach is: enumerate all items with the
compound key, heapify once (O(W)), pop k times (O(k log W)). For very
small k this is great; for k close to W, just sort.
''',
        "confusion_notes": [
            {
                "question": "Why can't I just use a min-heap of size k like in 'Top K Frequent Elements'?",
                "answer": "Because the tiebreak goes *opposite* directions: we want highest freq but lowest word. A natural tuple `(freq, word)` for a min-heap of size k would evict the lexicographically smallest word on tie — exactly the wrong one. You'd need a wrapper class that inverts the string comparison.",
            },
            {
                "question": "Is `heapify` then k pops faster than `sorted(...)[:k]`?",
                "answer": "Asymptotically: heapify is O(W), k pops is O(k log W), total O(W + k log W). Full sort is O(W log W). So when k ≪ W, heap is better. When k is comparable to W, sort is just as good and simpler.",
            },
        ],
        "summary": "Counter → max-heap of (-freq, word) → pop k times.",
    },
]
