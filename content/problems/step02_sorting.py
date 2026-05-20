"""Step 2 — Sorting algorithms.

Sorting is the warm-up gym. Each algorithm teaches a different
fundamental move: selection (finding the min), bubble (adjacent
swaps), insertion (slide and insert), merge (divide and conquer),
quick (partition).
"""
from __future__ import annotations

PROBLEMS: list[dict] = [
    {
        "id": "selection-sort",
        "title": "Selection Sort",
        "step_id": 2,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["sorting", "fundamentals"],
        "what_this_teaches": (
            "The simplest possible sorting recipe — find the minimum, "
            "place it, repeat — and the *loop-invariant* mental tool "
            "that proves it correct. Both ideas reappear constantly."
        ),
        "pattern": "Pick the minimum of the unsorted suffix, swap it to the front, repeat.",
        "prerequisite_lessons": ["arrays", "sorting"],
        "prerequisite_problems": ["largest-element"],
        "next_problems": [
            "bubble-sort",
            "insertion-sort",
            "second-largest-element",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 2 (Sorting I)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "Wikipedia — Selection sort",
                "url": "https://en.wikipedia.org/wiki/Selection_sort",
            },
        ],
        "understanding": r'''
We have an array of numbers and we want to sort it in ascending
order. *Selection sort* is one of the simplest possible recipes:

> *Find the minimum in the unsorted portion. Swap it into the next
> sorted position. Repeat.*

That is it. Imagine sorting a pile of books by height. You scan the
whole pile for the shortest book, place it at the left edge, then
ignore it. From the rest, you find the shortest, place it next,
ignore it. Continue until nothing remains unsorted.

Every iteration **selects** the next smallest element — hence the
name.
''',
        "brute_force": {
            "explanation": r'''
We maintain a moving frontier `i` between sorted (everything to the
left) and unsorted (everything from `i` onwards). For each `i` from
0 to `n - 1`, we scan the unsorted suffix to find the index of the
minimum, then swap it into position `i`.

We do not have a separate "optimized" version of selection sort —
this *is* the algorithm.
''',
            "code": r'''def selection_sort(arr: list[int]) -> None:
    n = len(arr)
    # Outer loop: i is the position we're about to fill.
    # After iteration i, arr[0..i] is final-sorted.
    for i in range(n):
        # Assume the current element is the minimum of the rest.
        # We will challenge this assumption with the inner loop.
        min_idx = i
        # Inner loop: scan everything after i to find any element
        # smaller than the current "best so far".
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                # Found a new candidate for the minimum; remember it.
                min_idx = j
        # Place the found minimum at position i. If it was already
        # there (min_idx == i), the swap is a harmless no-op.
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
''',
            "walkthrough": r'''
Selection sort. The simplest sort to *understand* — find the
smallest, put it first, repeat with the rest. Slow but
educational.

**`def selection_sort(arr: list[int]) -> None:`** — Takes
the array, returns nothing. We modify in place (notice the
return type is `None`).

**`n = len(arr)`** — Cache length.

**`for i in range(n):`** — Outer loop. After iteration `i`,
the first `i + 1` slots of the array (`arr[0..i]`) are
final-sorted — they hold the smallest `i + 1` values in their
correct positions.

The "selection" idea: at each step, we **select** the smallest
remaining value and put it where it belongs.

**`min_idx = i`** — Initial guess: the smallest in the
remaining portion is at position `i` itself. We'll update if
we find something smaller.

**`for j in range(i + 1, n):`** — Inner loop scans the
remaining unsorted portion (positions `i + 1` onward) looking
for the actual minimum.

**`if arr[j] < arr[min_idx]:`** — Challenger comparison. If
`arr[j]` is smaller than our current best, dethrone it.

**`min_idx = j`** — Remember the new champion's index.

**`arr[i], arr[min_idx] = arr[min_idx], arr[i]`** — After the
inner loop completes, `min_idx` is the position of the
smallest remaining value. Swap it into position `i`.

If `min_idx == i`, the swap is a no-op (swapping with self).
Some implementations check for this to skip the wasted swap;
the version above doesn't bother because the cost is trivial.

**Why is it O(n²)?**

The inner loop runs `n - 1`, `n - 2`, ..., `1`, `0` times for
successive outer iterations. That's `n × (n - 1) / 2` total
comparisons — *O(n²)*.

Crucially, **selection sort doesn't benefit from being given
sorted input.** It scans the entire remaining portion every
time, regardless of whether the data is sorted. Even on
already-sorted input, the cost is *O(n²)*. This is in
contrast to insertion sort (which is *O(n)* on sorted input)
and Timsort.

**Trace on `[64, 25, 12, 22, 11]`:**
```
Iter 0: scan [64,25,12,22,11], min at index 4 (val 11). Swap.
        arr = [11, 25, 12, 22, 64]
Iter 1: scan [25,12,22,64], min at index 2 (val 12). Swap.
        arr = [11, 12, 25, 22, 64]
Iter 2: scan [25,22,64], min at index 3 (val 22). Swap.
        arr = [11, 12, 22, 25, 64]
Iter 3: scan [25,64], min at index 3 (val 25, already there). Swap (no-op).
Iter 4: scan [], no work. Swap (no-op).
Result: [11, 12, 22, 25, 64].
```

**Properties:**
- **Time**: *O(n²)* always (best, average, worst).
- **Space**: *O(1)*.
- **Stable**: No. The swap can rearrange equal elements.
- **Adaptive**: No. Already-sorted input doesn't speed it up.

Selection sort is **rarely** used in practice — insertion
sort is faster on small inputs, Timsort on larger ones. But
it's pedagogically valuable: the algorithm is so simple you
can write it from scratch with no notes.
''',
            "complexity": (
                "**Time**: *O(n²)*. Two nested loops; the work does "
                "not depend on the input being sorted or not.\n\n"
                "**Space**: *O(1)*. We sort in place."
            ),
        },
        "thought_process": r'''
What makes selection sort beginner-friendly is that the algorithm
maps exactly onto the way humans sort things by hand: "find the
smallest, put it next, repeat". There is no extra cleverness.

What makes it slow is that it does not learn from the work it did
last round. After placing the minimum at position 0, it forgets
everything and starts over from position 1. There is no propagation
of information. Compare this with merge sort, where the work of
sorting each half is reused when we merge.

The number of comparisons is roughly `(n - 1) + (n - 2) + ... + 1`,
which equals `n(n - 1)/2`, which is *O(n²)*. That is the same
whether the input is already sorted, reverse sorted, or random.
That predictability is a kind of fairness, but it is also a flaw:
selection sort cannot exploit "almost sorted" inputs.

A second observation: selection sort makes at most `n - 1` swaps,
because each iteration swaps once. That is unusually low. If your
problem cares about minimizing swaps (say, swaps are expensive in
hardware), selection sort suddenly looks attractive even though its
comparisons are quadratic. Real algorithm choices depend on what
you are optimizing.
''',
        "deep_concept": r'''
Selection sort is a particular instance of a general algorithmic
move: **maintain an invariant, extend it one step at a time**. The
invariant here is "arr[0..i] is the smallest `i + 1` elements,
sorted". Every iteration grows the invariant by one position.

This way of thinking — "what is true after each iteration?" — is the
core of **loop invariants**. Loop invariants are how serious people
prove that their loops are correct. Get comfortable stating the
invariant of every loop you write; it pays off enormously in harder
problems.

A final note on **stability**. A sorting algorithm is *stable* if it
preserves the relative order of elements that compare equal. The
naive selection sort above is **not stable** because the swap can
jump an equal element past another one. This rarely matters for
plain integer sorting, but it does matter when you are sorting
records by one field and want the other fields' order preserved.
''',
        "confusion_notes": [
            {
                "question": "Why does the outer loop run from `0` to `n - 1` and not all the way to `n`?",
                "answer": r'''
Because after we have placed the first `n - 1` elements
correctly, the last element is *automatically* in the right
spot — there is nothing else to compare it against.

Think of it physically. We start with `n` unsorted slots.
Iteration 0 places the smallest into slot 0. Iteration 1 places
the next smallest into slot 1. After iteration `n - 2`, we have
placed `n - 1` elements correctly in slots 0 through `n - 2`.
What remains in slot `n - 1`? The only element we have not yet
placed — which must be the largest. By process of elimination,
it is already where it belongs. Running iteration `n - 1` would
be a no-op.

In code, `for i in range(n):` actually runs `n` iterations, not
`n - 1`. The last iteration is harmless but redundant. You can
write `for i in range(n - 1):` to save one iteration; it does
not change correctness. Most beginners just write `range(n)`
because the off-by-one is easier to keep straight.

The deeper lesson: **the last element in any sort-by-elimination
algorithm sorts itself**. The same observation makes bubble
sort's outer loop one shorter, and it is the reason quicksort's
recursion has the base case `lo >= hi` rather than `lo > hi`.
''',
            },
            {
                "question": "What is a *loop invariant* and why should I care?",
                "answer": r'''
A loop invariant is a statement that is **true at the start of
every iteration** of a loop. It captures what the loop has
accomplished so far and lets you reason about correctness
without tracing every step.

For selection sort, the invariant is: *"Before iteration `i`,
`arr[0..i-1]` contains the smallest `i` elements of the array,
sorted in non-decreasing order."*

Read that carefully. At the start of iteration `i = 0`, the
statement says "arr[0..-1]" — that is, an empty prefix —
"contains the smallest 0 elements, sorted." Trivially true.

At the start of iteration `i = 1`, after one pass, the
invariant says `arr[0..0]` contains the smallest 1 element,
sorted. That is the minimum of the whole array, which is exactly
what we placed there. True.

Each iteration **extends the invariant by one**: it grows the
sorted prefix by one element while preserving the property. When
the loop exits at `i = n`, the invariant says `arr[0..n-1]`
contains all `n` elements, sorted. That is the goal. Done.

Why care? Because loop invariants are how you **prove your loops
correct** without running them. They convert "I am pretty sure
this works" into "I can explain why this works." For hard
problems with subtle off-by-ones (binary search, sliding window,
two pointers), explicitly stating the invariant catches bugs
before you write a single line of code.

When you sit down to write any loop, ask yourself: *"what is true
before iteration `i`, and how does iteration `i` extend it?"*.
That single discipline elevates your code quality enormously.
''',
            },
            {
                "question": "Why is selection sort so slow even though the algorithm is simple?",
                "answer": r'''
Because **the work each pass does is the same regardless of
what we found in earlier passes**. Selection sort has no way to
exploit information from one pass to speed up the next.

Concretely, every outer iteration triggers an inner scan over
the entire remaining unsorted suffix. The first pass scans `n -
1` elements. The second pass scans `n - 2`. Then `n - 3`, and so
on. The total work is `(n - 1) + (n - 2) + ... + 1 = n(n - 1)/2`,
which is *O(n²)*.

Critically, this total is the **same** for every input. An
already-sorted array? *O(n²)* scans, even though no swaps are
needed. A nearly-sorted array? *O(n²)* scans. A reverse-sorted
array? *O(n²)* scans. The algorithm cannot tell the difference;
it always does the worst-case amount of comparison work.

Contrast this with insertion sort, which exits its inner loop as
soon as the next element falls into place. On already-sorted
input, insertion sort does only `O(n)` comparisons — a thousand
times faster than selection sort on the same input.

The general principle: a good algorithm **exploits structure in
the input**. Selection sort exploits nothing. It is the
algorithmic equivalent of brute force — correct, simple, slow.
Useful as a baseline for understanding, but rarely the right
choice in real code.
''',
            },
            {
                "question": "Why is selection sort *unstable*? What does that even mean?",
                "answer": r'''
A sorting algorithm is **stable** if elements with equal keys
keep their *original* relative order after sorting. **Unstable**
means equal elements can swap positions.

Consider `arr = [(2, 'a'), (1, 'x'), (2, 'b')]`, sorted by the
first field. A stable sort returns
`[(1, 'x'), (2, 'a'), (2, 'b')]` — the two `(2, ...)` elements
keep `'a'` before `'b'` because `'a'` was originally first.

Selection sort, on the other hand, can produce
`[(1, 'x'), (2, 'b'), (2, 'a')]`. Here is why. On iteration 0,
we scan for the minimum (which is the `(1, 'x')` at index 1).
We swap it with the element at index 0, which was `(2, 'a')`.
After the swap, `(2, 'a')` is at index 1 and `(2, 'b')` is at
index 2. The first `(2, ...)` element's original position
relative to the second has flipped — `'b'` now comes before
`'a'`.

When does stability matter? When you sort *records by one
field* and care about the order of other fields. For example,
sorting a list of employees by department: you want employees
within the same department to keep their alphabetical-by-name
order from a previous sort. Stable sorts preserve that; unstable
ones scramble it.

Python's built-in `sorted` (Timsort) is **stable**. C++'s
`std::sort` is **unstable** by default; if you need stability,
use `std::stable_sort`. Java's `Arrays.sort` is stable for
objects (mergesort variant), unstable for primitives (Dual-Pivot
QuickSort).

For curriculum problems involving plain numbers, stability
rarely matters. For interview problems involving records or
tuples, always ask yourself "do I need stability?" before
choosing a sort.
''',
            },
        ],
        "summary": r'''
**Pattern**: pick the minimum, swap it forward, repeat.

**Lesson**: selection sort is the simplest sort to understand and
the slowest to run. Useful as a teaching tool and as a real choice
when swaps are expensive.

**Recognize next time**: probably never — but it cements the *loop
invariant* mental tool, which you will reuse forever.
''',
    },
    {
        "id": "bubble-sort",
        "title": "Bubble Sort",
        "step_id": 2,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["sorting", "fundamentals"],
        "what_this_teaches": (
            "How **adjacent swaps** turn into a sorting algorithm, "
            "and the hidden connection between sort runtime and the "
            "**inversion count** of the input — a deep idea you will "
            "reuse in merge-sort-based inversion counting later."
        ),
        "pattern": "Adjacent comparison-and-swap, repeated until a pass does nothing.",
        "prerequisite_lessons": ["sorting"],
        "prerequisite_problems": ["selection-sort"],
        "next_problems": [
            "insertion-sort",
            "recursive-bubble-sort",
            "count-inversions",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 2 (Sorting I)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "Wikipedia — Bubble sort",
                "url": "https://en.wikipedia.org/wiki/Bubble_sort",
            },
        ],
        "understanding": r'''
Bubble sort gets its name from the visual image: large elements
"bubble" toward the right end on each pass, the way a bubble rises
to the top of a glass of soda. The recipe:

> *Walk through the array; whenever adjacent elements are out of
> order, swap them. Repeat passes until a clean pass happens.*

Each full pass guarantees that the largest unsorted element ends up
in its final position at the right end. So after `k` passes, the
last `k` positions are correct.
''',
        "brute_force": {
            "explanation": r'''
The textbook implementation has two nested loops: an outer "how many
passes have we done?" loop and an inner "compare adjacent pairs"
loop. We shrink the inner range each pass because the right end is
already sorted.

A small but worthwhile optimization: if a pass completes with **no
swaps**, the array is already sorted and we can stop early.
''',
            "code": r'''def bubble_sort(arr: list[int]) -> None:
    n = len(arr)
    # Outer loop: each iteration "settles" one more element at the end.
    for end in range(n - 1, 0, -1):
        # Track whether we swapped at all this pass.
        swapped = False
        # Inner loop: walk from the start to the current end boundary.
        # Note: we go up to `end`, not `end + 1`, because we compare
        # j with j + 1, and we must not read past the array.
        for j in range(end):
            if arr[j] > arr[j + 1]:
                # Out of order — swap them.
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # If a full pass did nothing, the array is sorted.
        if not swapped:
            return
''',
            "walkthrough": r'''
Bubble sort. Compare neighbors, swap if out of order, repeat
until no swaps happen. Famous for being slow but simple.

**`def bubble_sort(arr: list[int]) -> None:`** — In-place sort,
returns nothing.

**`n = len(arr)`** — Cache length.

**`for end in range(n - 1, 0, -1):`** — Outer loop. `end`
counts **down** from `n - 1` to `1`. Why? Because after each
pass, the **largest unsorted element bubbles up to position
`end`** and stays there. So next pass only needs to handle
elements before that position.

`range(n - 1, 0, -1)` gives the sequence `n-1, n-2, ..., 1`.
The third argument `-1` makes it decrement; the second
argument `0` is the exclusive stop, so `0` itself is not
included (good — we never need to do a "pass" with `end = 0`
because the array would have only one unsorted element left,
which is trivially in place).

**`swapped = False`** — Track whether we did any swap this
pass. If we didn't, the array is already sorted — early exit.

**`for j in range(end):`** — Inner loop: scan from position
`0` up to position `end - 1`. We compare `arr[j]` with
`arr[j + 1]`, so the last `j` we want to use is `end - 1`
(so `j + 1 = end`). `range(end)` is `0, 1, ..., end - 1` —
exactly what we want.

**`if arr[j] > arr[j + 1]:`** — Out of order: the smaller
element should come first.

**`arr[j], arr[j + 1] = arr[j + 1], arr[j]`** — Swap them.

**`swapped = True`** — Record that we did work.

**`if not swapped: return`** — **Early exit optimization.**
If no swap occurred during the whole inner loop, the array is
already sorted; no point in further passes. This makes bubble
sort *O(n)* on already-sorted input.

**Why "bubble"?**

Watch the largest element. On any pass, when we compare it to
its right neighbor, it's strictly larger; so we swap, and the
big element moves one step right. Next comparison: it's
again the larger, so it swaps right again. The big element
"bubbles" to the right end of the unsorted region in a single
pass.

Smaller elements bubble too, but more slowly — they only
move one position per pass (each pass, they may or may not
get swapped depending on their neighbor). A small element at
the far right of the array can take up to `n` passes to drift
to the front. **That's why bubble sort is slow.**

**Trace on `[5, 1, 4, 2, 8]`:**
```
Pass 1 (end=4): compare (5,1)→swap, (5,4)→swap, (5,2)→swap, (5,8)→no.
                arr = [1, 4, 2, 5, 8]. swapped=True. (8 bubbled to end.)
Pass 2 (end=3): (1,4)→no, (4,2)→swap, (4,5)→no.
                arr = [1, 2, 4, 5, 8]. swapped=True. (4 bubbled.)
Pass 3 (end=2): (1,2)→no, (2,4)→no.
                arr unchanged. swapped=False. → Early exit.
```

Three passes instead of four. Already-sorted input would exit
after one pass.

**Properties:**
- **Time**: *O(n²)* worst; *O(n)* best with the early-exit.
- **Space**: *O(1)*.
- **Stable**: Yes (we use `>` not `>=`, so equal elements
  don't swap).
- **Adaptive**: Yes — already-sorted input runs in *O(n)*.

Bubble sort is the **canonical bad sort**. It's covered for
pedagogical reasons; you'd never ship it. But its "if no
work, stop" pattern reappears in algorithms like the
Bellman-Ford shortest path.
''',
            "complexity": (
                "**Time**: *O(n²)* worst case, *O(n)* best case if "
                "input is already sorted (the early-exit triggers).\n\n"
                "**Space**: *O(1)*."
            ),
        },
        "thought_process": r'''
Bubble sort and selection sort sit at the same complexity, but they
think differently. Selection sort does a global search per pass to
find the minimum, then puts it in place. Bubble sort does local
fixes — it only ever swaps neighbours.

That locality is bubble sort's defining feature. **Every swap moves
an element by at most one position**. So if an element starts far
from its destination, it takes many passes to drift across. That is
why bubble sort is famous for being slow on real inputs.

But the locality also gives bubble sort its one redeeming feature.
If the input is already sorted, the very first pass does zero swaps,
and the algorithm exits after *O(n)* comparisons. No other quadratic
sort handles "already sorted" so cheaply.

There is a famous bit of trivia: bubble sort is one of the worst
sorts in terms of swap count, *and* in terms of cache behavior, *and*
in terms of branch prediction. People sometimes joke that bubble
sort exists only to be a counterexample. But it teaches you
something important: **adjacent-swap algorithms behave like
inversion counters**. Every swap removes exactly one inversion
(pair out of order). So bubble sort is secretly counting
inversions. If you ever need to count them, you can do it in
*O(n log n)* with a clever merge-sort variant — which we cover later
in Step 3.
''',
        "deep_concept": r'''
The connection to inversions is the soul of bubble sort. Define an
**inversion** as a pair of indices `i < j` where `arr[i] > arr[j]`.
A sorted array has zero inversions. Bubble sort terminates exactly
when the number of inversions is zero, and each swap removes exactly
one inversion. So the number of swaps equals the number of
inversions. That is a beautiful invariant and shows why "almost
sorted" inputs (few inversions) finish quickly.

This connection between an algorithm's runtime and a combinatorial
property of the input (inversion count) is the kind of insight that
distinguishes a serious programmer from a code-writer. Try to spot
these structural relationships in every algorithm you study.
''',
        "confusion_notes": [
            {
                "question": "Why does the outer loop go *down* (`for end in range(n - 1, 0, -1):`)?",
                "answer": r'''
Because after each pass, the **last `end + 1` positions are
already final**, so the next pass does not need to look at them.
Walking the outer variable downward is one way to encode that
"everything past `end` is done" boundary.

The first pass bubbles the maximum element to position `n - 1`.
The second pass bubbles the second-maximum to position `n - 2`.
And so on. After `k` passes, the rightmost `k` positions are
sorted and frozen. The inner loop never needs to touch them
again.

`range(n - 1, 0, -1)` produces the sequence `n - 1, n - 2, ...,
1`. On iteration with `end = k`, the inner loop walks
`j = 0, 1, ..., end - 1` and compares `arr[j]` with `arr[j +
1]`. The largest valid `j + 1` is `end`, which is the rightmost
position that still needs work. Anything beyond `end` is already
sorted.

You could also write the outer loop counting up:

```python
for i in range(n - 1):
    for j in range(0, n - 1 - i):
        ...
```

Both forms are correct; the down-counting version is just a
common idiom you should be able to read at a glance.

The shared idea: in any sort that "settles" elements at one end
pass by pass, the active region shrinks. Encoding the shrinking
boundary in the outer loop is one of the small disciplines that
keeps inner loops fast.
''',
            },
            {
                "question": "What does the `swapped` flag actually buy us?",
                "answer": r'''
It buys us **early termination on sorted (or nearly-sorted)
input**, dropping the best-case complexity from *O(n²)* to
*O(n)*.

Without the flag, the outer loop runs `n - 1` times no matter
what. With the flag, we set it to `False` at the start of each
pass and to `True` whenever a swap happens. If a full pass
completes with `swapped` still `False`, we know the array is
already sorted, and we can `return` immediately.

For an already-sorted input, the very first pass does zero
swaps. The flag stays `False`. We exit after exactly `n - 1`
comparisons. *O(n)*.

For a nearly-sorted input (only a few inversions), the algorithm
exits after a few passes instead of `n - 1`. Still much better
than worst case.

This early-exit pattern shows up in many adaptive algorithms.
The general lesson: **let the algorithm sense when it is done
and stop**. A boolean flag that costs one bit of memory and one
comparison per pass can save quadratic time on real-world
inputs, which are often "almost sorted" because they came from
some prior process.
''',
            },
            {
                "question": "Why does \"swap equals one inversion removed\" matter? Is that just trivia?",
                "answer": r'''
It is not trivia — it is a clean **proof** that bubble sort is
optimal among adjacent-swap algorithms, and it points the way to
an *O(n log n)* algorithm for counting inversions.

The proof. An adjacent swap takes two neighbours `arr[j]` and
`arr[j+1]` and reorders them. If they were out of order before
the swap (i.e., `arr[j] > arr[j+1]`), the swap removes exactly
one inversion — the pair `(j, j+1)`. The swap cannot remove any
other inversion, because no other pair changed positions.

So the total number of adjacent swaps any sorting algorithm
performs is **at least equal to the inversion count**. Bubble
sort performs exactly that many. Therefore bubble sort uses the
**minimum possible number of adjacent swaps**.

The deeper application: counting inversions is itself a classic
problem (in this curriculum's Step 3 hard section). The brute
force is *O(n²)* — for each pair, check whether it is an
inversion. But by modifying merge sort to count inversions
during the merge step, we get *O(n log n)*. That algorithm
exists because we understand the connection between sorting and
inversions, which bubble sort makes explicit.

The thing-worth-stealing from this problem: **algorithms have
hidden invariants that connect their runtime to combinatorial
properties of the input**. Find that invariant and you understand
the algorithm at a much deeper level.
''',
            },
            {
                "question": "Why do real systems never use bubble sort?",
                "answer": r'''
Because almost every other sort beats it on every realistic
metric: comparisons, swaps, cache behavior, and branch
prediction.

Selection sort: same big-O but fewer swaps (one per outer
iteration). Insertion sort: same big-O but exits early on
nearly-sorted input (so does bubble, but insertion's inner
arithmetic is faster). Merge sort and quick sort: *O(n log n)*,
massively faster on any non-trivial input. Timsort (Python's
built-in): hybrid of merge and insertion that destroys bubble
on real workloads.

Bubble sort also has terrible **memory access patterns** —
adjacent swaps thrash the CPU cache because each pass touches
every element. Quick sort and merge sort cluster their work and
benefit from caching.

In production code, you should reach for the standard library's
`sorted` (or `arr.sort()` in place). It is *O(n log n)*, stable,
and highly optimized. Roll your own only when you have a
specific reason — interview practice, a specialized constraint
like "minimum swaps," or a teaching context.

So why teach bubble sort at all? Because the **mental model** of
adjacent swaps removing inversions is useful far beyond bubble
sort itself, and writing bubble sort once or twice is a great
way to internalize loop invariants.

In short: learn bubble sort, then never use it.
''',
            },
        ],
        "summary": r'''
**Pattern**: adjacent comparisons and swaps, repeated until clean.

**Lesson**: bubble sort is quadratic in general but linear on
sorted/nearly-sorted input. The "swap = remove one inversion"
invariant is the deep takeaway.

**Recognize next time**: rarely worth using in practice; remember
the inversion connection because it powers merge-sort-based
inversion counting in Step 3.
''',
    },
    {
        "id": "insertion-sort",
        "title": "Insertion Sort",
        "step_id": 2,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["sorting", "fundamentals"],
        "what_this_teaches": (
            "How a sort can **exploit existing order** — insertion "
            "sort's `O(n²)` worst case becomes nearly `O(n)` on "
            "almost-sorted input. That sensitivity to structure is "
            "why production sorts (Timsort) wrap insertion sort "
            "inside themselves as the small-array base case."
        ),
        "pattern": "Maintain a sorted prefix; slide the next element leftward into place.",
        "prerequisite_lessons": ["sorting"],
        "prerequisite_problems": ["bubble-sort"],
        "next_problems": [
            "merge-sort",
            "quick-sort",
            "recursive-insertion-sort",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 2 (Sorting I)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "Wikipedia — Insertion sort",
                "url": "https://en.wikipedia.org/wiki/Insertion_sort",
            },
        ],
        "understanding": r'''
Insertion sort imitates how most people sort a hand of playing cards.
You hold the cards face-up in your left hand, sorted. You pick a
fresh card from the deck. You slide it leftward through your hand
until it sits between a smaller card on the left and a larger card
on the right. Then you pick the next card. Repeat.

Translating to an array: we treat `arr[0..i - 1]` as the sorted hand,
and `arr[i]` as the new card to insert. We slide `arr[i]` leftward by
swapping with the previous element until it lands in the right spot.
''',
        "brute_force": {
            "explanation": r'''
Outer loop: `i` ranges from 1 to `n - 1`. Inner loop: walk `j` from
`i` back toward 0, swapping whenever `arr[j - 1] > arr[j]`. Stop the
moment a swap is not needed.

A common slight variant uses *shifts* instead of swaps for a small
speedup: pull `current = arr[i]`, shift everything bigger one step
right, then drop `current` into the gap. The code below uses this
shift form.
''',
            "code": r'''def insertion_sort(arr: list[int]) -> None:
    n = len(arr)
    # Outer loop: we are about to insert arr[i] into the sorted
    # prefix arr[0..i - 1].
    for i in range(1, n):
        # Save the value we want to insert. Once we start shifting,
        # arr[i] gets overwritten, so we need this copy.
        current = arr[i]
        j = i - 1
        # Slide larger elements one position to the right to make
        # room. We stop when we either hit the left edge or find an
        # element <= current.
        while j >= 0 and arr[j] > current:
            arr[j + 1] = arr[j]
            j -= 1
        # Drop current into the empty slot we just opened.
        arr[j + 1] = current
''',
            "walkthrough": r'''
Insertion sort. The way humans naturally sort playing cards
in their hand: pick up each new card and slide it into its
proper position among the already-sorted ones.

**`def insertion_sort(arr: list[int]) -> None:`** — In-place
sort.

**`n = len(arr)`** — Cache length.

**`for i in range(1, n):`** — Outer loop. Start at `i = 1`
because `arr[0..0]` (single element) is trivially sorted.
After each iteration, `arr[0..i]` is sorted.

The invariant: at the start of each iteration, `arr[0..i-1]`
is sorted. We extend this by inserting `arr[i]` into its
correct position.

**`current = arr[i]`** — **Save the value to be inserted.**
This is critical. We're about to shift elements rightward,
which will overwrite `arr[i]`. We need a separate copy.

**`j = i - 1`** — Start scanning leftward from just before
the current insertion point.

**`while j >= 0 and arr[j] > current:`** — Continue while:
1. We haven't fallen off the left edge (`j >= 0`).
2. The element at position `j` is larger than what we want to
   insert. Larger elements must move right to make room.

Note Python's short-circuit evaluation: `j >= 0` is checked
first. If `j` is `-1`, we don't try to read `arr[-1]` (which
in Python would wrap around to the last element — wrong!).

**`arr[j + 1] = arr[j]`** — Slide the larger element one
position to the right. Now position `j + 1` holds what used
to be at `j`; position `j` is still occupied by the same
value (we just copied it forward, not moved it).

**`j -= 1`** — Move the scanner one step left, looking at
the next-leftward element.

**`arr[j + 1] = current`** — After the loop exits, either
`j < 0` (we hit the left edge — `current` is the smallest so
far and goes at position 0) or `arr[j] <= current` (we found
the right spot — `current` goes just to the right of `arr[j]`).
Either way, `arr[j + 1]` is the empty slot.

**Why is this O(n²) worst case?**

For each `i`, the inner while loop can shift up to `i`
elements. Summing: `1 + 2 + ... + (n-1) = O(n²)`.

But notice the early-exit: if `arr[j] <= current`, we stop.
On **already-sorted** input, this triggers immediately on
every iteration — the inner loop does **zero** work. Total
time: *O(n)*. This is the best of all *O(n²)* sorts.

**Trace on `[5, 2, 4, 6, 1]`:**
```
i=1, current=2, j=0: arr[0]=5 > 2 → shift, j=-1. Stop.
                     Place at arr[0]. arr = [2, 5, 4, 6, 1].
i=2, current=4, j=1: arr[1]=5 > 4 → shift, j=0. arr[0]=2 ≤ 4 → stop.
                     Place at arr[1]. arr = [2, 4, 5, 6, 1].
i=3, current=6, j=2: arr[2]=5 ≤ 6 → don't enter loop.
                     Place at arr[3] (no change). arr = [2, 4, 5, 6, 1].
i=4, current=1, j=3: arr[3]=6 > 1 → shift. j=2. arr[2]=5 > 1 → shift.
                     j=1. arr[1]=4 > 1 → shift. j=0. arr[0]=2 > 1 → shift.
                     j=-1. Stop. Place at arr[0]. arr = [1, 2, 4, 5, 6].
```

**Properties:**
- **Time**: *O(n²)* worst, *O(n)* best (sorted input).
- **Space**: *O(1)*.
- **Stable**: Yes (we use `>` not `>=`, so equal elements
  preserve order).
- **Adaptive**: Yes — partially-sorted input runs much faster.

**When is insertion sort actually used?**
- For **small arrays** (n ≤ 10-30), insertion sort is faster
  than any *O(n log n)* sort due to lower constants.
- Python's `Timsort` uses insertion sort on small runs and
  merge sort to combine them.
- For **nearly-sorted** data (the common real-world case),
  insertion sort approaches *O(n)*.

Insertion sort is genuinely useful, not just pedagogical.
''',
            "complexity": (
                "**Time**: *O(n²)* worst and average, *O(n)* on "
                "already-sorted input (the inner while loop never "
                "runs).\n\n"
                "**Space**: *O(1)*."
            ),
        },
        "thought_process": r'''
Insertion sort is the fastest of the three *O(n²)* sorts in
practice, by a wide margin. The reason is twofold:

1. **It moves through memory linearly**, which is friendly to the
   CPU cache and to branch prediction.
2. **It exploits sortedness**. On nearly-sorted input, the inner
   while loop barely runs, so the algorithm is *almost* linear.

This is why real-world sorts often use insertion sort for small
subarrays. CPython's Timsort, Java's Arrays.sort, and most
high-performance sorting code switch to insertion sort once the
subarray is below about 32 elements. The constant factors win.

The conceptual move worth stealing is **"maintain a sorted prefix"**.
That invariant — "elements before index `i` are sorted" — is exactly
the same shape as selection sort's invariant. But the way we grow
it differs: selection sort pulls the next item into position by
*finding* the smallest; insertion sort *inserts* the next item into
the sorted prefix by sliding it leftward.

The same trade keeps showing up in algorithms: do you search for
what comes next, or insert what arrives where it belongs? Selection
vs insertion is the prototype.
''',
        "deep_concept": r'''
There is a wonderful connection: **insertion sort is essentially the
in-place version of binary insertion sort.** If the prefix is
sorted, we could find the insertion point with binary search in
*O(log i)* — but then we still have to shift everything, which is
*O(i)*. Net result is still quadratic. So we usually use the linear
scan, which is faster in constants. This shows that asymptotic
analysis is not the only story.

There is also a clean connection to **sorted insertions in a linked
list**. The same algorithm, written for a singly linked list, is
*O(n²)* time but uses zero shifts — every insertion is pointer
splicing. Linked-list insertion sort is the natural way to sort a
linked list when memory is tight.

The "do not redo work" principle suggests that on truly random
input, *O(n²)* sorts cannot be beaten without divide-and-conquer.
That's what merge sort delivers next.
''',
        "confusion_notes": [
            {
                "question": "Why does insertion sort use shifts instead of swaps?",
                "answer": r'''
Because a **shift** is half the work of a **swap**.

A swap moves two values: each ends up in the other's slot. That
is two writes. An insertion sort shift moves one value rightward
to make room: one write. When you have to slide many elements
to insert a new one, doing it with shifts saves half the
operations compared to a sequence of swaps.

Concretely, the shift version of insertion sort looks like this:

```python
current = arr[i]            # save the value we want to insert
j = i - 1
while j >= 0 and arr[j] > current:
    arr[j + 1] = arr[j]     # slide a larger neighbour rightward
    j -= 1
arr[j + 1] = current        # drop current into the open slot
```

Notice that the inner loop only ever does one write per
iteration (`arr[j + 1] = arr[j]`). At the very end, one extra
write (`arr[j + 1] = current`) places the saved value. Total
writes for inserting one element into a sorted prefix of length
`k` is at most `k + 1`.

A swap-based version would write `2k` times in the worst case,
because each swap is two writes. So shifts are roughly 2× faster
in terms of memory writes. On modern hardware where writes are
the slowest part of memory access, this matters.

The general lesson: **when you can save a value and shift many
others by one, do not swap pairwise — shift and place**. The same
trick speeds up many in-place array compaction routines.
''',
            },
            {
                "question": "Why is insertion sort *O(n)* on already-sorted input?",
                "answer": r'''
Because the inner `while` loop **exits immediately** when the
new element is already in place.

Look at the loop:

```python
while j >= 0 and arr[j] > current:
    arr[j + 1] = arr[j]
    j -= 1
```

If `arr[j]` is already `<= current`, the condition
`arr[j] > current` is `False` and the loop body never runs. We
skip directly to the final assignment, which (because `current`
already equals `arr[i]`) is a no-op.

For an already-sorted array, every iteration of the outer loop
encounters `arr[i]` already in the right place, and the inner
loop does zero work. The outer loop runs `n - 1` times, each
with constant work. Total: *O(n)*.

This **adaptivity** to existing order is what makes insertion
sort so valuable in practice. Real-world data is often "mostly
sorted" — sensor readings drift gradually, logs are nearly
chronological, sorted data has only a few recent insertions.
Insertion sort handles all of these in near-linear time.

The next sort up, merge sort, does *O(n log n)* work on every
input regardless of structure. It is asymptotically faster on
random data but **slower** than insertion sort on highly-sorted
data. This is why production hybrid sorts (Timsort, introsort)
detect sorted runs and switch to insertion sort for them.
''',
            },
            {
                "question": "Why save `current` before sliding? Couldn't I just compare in place?",
                "answer": r'''
Because the first slide *overwrites* `arr[i]`, the value we are
trying to insert.

Walk through it carefully. Suppose `arr = [3, 5, 7, 4, 8]` and
we are inserting `arr[3] = 4` into the sorted prefix
`[3, 5, 7]`. The inner loop will execute `arr[j + 1] = arr[j]`
with `j = 2`, which assigns `arr[3] = arr[2] = 7`. Now the
array is `[3, 5, 7, 7, 8]` — the `4` is gone, overwritten by
`7`.

If we had not saved `current = 4` at the top, the value would
be lost forever. We would have nothing to insert at the end.

So `current = arr[i]` at the very top of the iteration is
**mandatory**. It is the same "save a copy before mutating"
discipline you saw in `count-digits` (saving `original` before
the loop destroys `n`).

The general pattern: whenever a loop's first action would
destroy information the loop needs later, stash that information
in a local variable. This pattern reappears in linked-list
operations (save `next_node` before flipping `curr.next`), in
swaps inside arrays, and in many in-place algorithms.
''',
            },
            {
                "question": "Why is insertion sort the fastest of the `O(n²)` sorts in practice?",
                "answer": r'''
Three reasons combine to make it the fastest.

First, **adaptivity**. On already-sorted or nearly-sorted input,
insertion sort runs in *O(n)*. Selection sort always does
*O(n²)* comparisons regardless of input. Bubble sort can also
adapt with the `swapped` flag, but its inner loop does more work
per comparison.

Second, **cache friendliness**. Insertion sort accesses memory
in a tight contiguous pattern — it reads `arr[i]`, then
neighbours just to the left. Modern CPUs cache memory in chunks,
so consecutive accesses to nearby addresses are essentially
free. Selection sort and merge sort touch memory more
scattered-ly and suffer more cache misses on small inputs.

Third, **simple inner loop**. The body of the inner `while` is
two lines (a comparison and a shift). No conditional branches
beyond the loop condition, no function calls. Modern branch
predictors love this kind of code and run it at close to peak
hardware speed.

The combined effect: for arrays of, say, 32 elements or fewer,
insertion sort often **beats** *O(n log n)* sorts like merge
sort and quick sort, even though it is asymptotically worse.
This is why every serious production sort routine (CPython's
Timsort, Java's `Arrays.sort`, GCC's `std::sort`) switches to
insertion sort once the recursive subarray drops below ~16-32
elements.

The lesson: **asymptotic analysis is a guide, not a law**.
Constants matter, and on small inputs the constants can flip
the comparison.
''',
            },
        ],
        "summary": r'''
**Pattern**: maintain a sorted prefix; insert the next element by
sliding it leftward.

**Lesson**: insertion sort is quadratic in the worst case but
near-linear on nearly-sorted input — and it has terrific constants.
That is why it lives inside most production sort routines as the
base-case sub-sort.

**Recognize next time**: small `n`, nearly-sorted input, or as the
"small-array fallback" inside a divide-and-conquer sort.
''',
    },
    {
        "id": "merge-sort",
        "title": "Merge Sort",
        "step_id": 2,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["sorting", "divide-and-conquer", "recursion"],
        "what_this_teaches": (
            "Divide-and-conquer in its purest form — split a problem "
            "into two halves, solve each recursively, combine the "
            "results. The two-pointer **merge** routine is the only "
            "real work; it shows up again in merging K sorted lists, "
            "counting inversions, and external sorting."
        ),
        "pattern": "Divide in half, recursively sort each side, merge two sorted halves.",
        "prerequisite_lessons": ["recursion", "sorting"],
        "prerequisite_problems": ["insertion-sort"],
        "next_problems": [
            "quick-sort",
            "count-inversions",
            "reverse-pairs",
            "merge-k-sorted-lists",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 2 (Sorting II)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "Wikipedia — Merge sort",
                "url": "https://en.wikipedia.org/wiki/Merge_sort",
            },
        ],
        "understanding": r'''
Merge sort is the first **divide-and-conquer** algorithm we meet,
and it is the cleanest possible introduction to the idea. The
recipe in one breath:

> *Split the array in half. Sort each half. Merge the two sorted
> halves into one.*

Each of the three steps is easy:
- "Split in half" is `mid = len(arr) // 2`.
- "Sort each half" is a recursive call — we trust ourselves.
- "Merge two sorted halves" is the only piece of real work: walk
  two pointers, always pick the smaller front element.

The whole algorithm is built out of one truly new operation: the
two-pointer merge.
''',
        "brute_force": {
            "explanation": r'''
We will write merge sort recursively, returning a new sorted list
each call. There is also an in-place version using indices, which is
trickier to read but uses less memory. The recursive copy version is
what beginners should learn first.
''',
            "code": r'''def merge_sort(arr: list[int]) -> list[int]:
    # Base case: a 0- or 1-element list is trivially sorted.
    if len(arr) <= 1:
        # Return a copy so callers can never accidentally mutate
        # their input through ours.
        return arr[:]
    # Divide: split into two halves around the midpoint.
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    # Conquer: merge the two sorted halves into one sorted list.
    return _merge(left, right)


def _merge(a: list[int], b: list[int]) -> list[int]:
    # Two pointers walk through a and b in parallel. At each step
    # we pick the smaller front element and append it to the result.
    merged: list[int] = []
    i = j = 0
    while i < len(a) and j < len(b):
        # Use <= rather than < to keep the merge STABLE — equal
        # elements keep their original relative order.
        if a[i] <= b[j]:
            merged.append(a[i])
            i += 1
        else:
            merged.append(b[j])
            j += 1
    # Whichever list still has leftovers, append them. At most one
    # of these `extend` calls actually does any work.
    merged.extend(a[i:])
    merged.extend(b[j:])
    return merged
''',
            "walkthrough": r'''
Merge sort. The cleanest example of **divide and conquer** in
all of DSA. Split, recurse, merge. *O(n log n)* guaranteed.

**The main function: `merge_sort`**

**`def merge_sort(arr: list[int]) -> list[int]:`** — Takes a
list, returns a new sorted list. (Not in-place. We could
write an in-place version, but the out-of-place version is
clearer and easier to reason about.)

**`if len(arr) <= 1: return arr[:]`** — **Base case.** A list
of 0 or 1 elements is already sorted. Return a copy (with
`arr[:]`) so the caller's data isn't shared with our output.

**`mid = len(arr) // 2`** — Pick the midpoint. For length 7,
this is 3. The left half will be `arr[0..2]` (length 3) and
the right half `arr[3..6]` (length 4). Slightly unbalanced is
fine — divide-and-conquer handles unbalanced splits.

**`left = merge_sort(arr[:mid])`** — **Recurse on the left
half.** Trust the recursive call to return a sorted version.

**`right = merge_sort(arr[mid:])`** — **Recurse on the right
half.** Same trust.

**`return _merge(left, right)`** — **Conquer step.** Merge
the two sorted halves into one sorted list using the helper.

**The merge helper: `_merge`**

This is where the real work happens.

**`def _merge(a: list[int], b: list[int]) -> list[int]:`** —
Takes two **already-sorted** lists, returns their merged
sorted union.

**`merged: list[int] = []`** — Output accumulator.

**`i = j = 0`** — Two pointers, one for each input.

**`while i < len(a) and j < len(b):`** — Continue while both
lists have elements left to compare.

**`if a[i] <= b[j]:`** — Compare the **fronts** of both lists.

The `<=` (not `<`) is the **stability** trick. When equal
elements appear in both lists, we prefer the one from `a`
(the left half). This preserves the original relative order
of equal elements — making the sort stable.

**`merged.append(a[i]); i += 1`** — Take from `a`, advance.

**`merged.append(b[j]); j += 1`** — Take from `b`, advance.

**`merged.extend(a[i:]); merged.extend(b[j:])`** — When one
list runs out, the other might have remaining elements. They
are already sorted, so just append them to the end.

`extend` adds all elements from an iterable. Either `a[i:]`
or `b[j:]` (or both) is empty by this point — at most one of
these calls does real work.

**`return merged`** — Hand back the merged result.

**Why is this O(n log n)?**

Draw the recursion tree:
- Level 0: 1 list of size `n`.
- Level 1: 2 lists of size `n/2`.
- Level 2: 4 lists of size `n/4`.
- ...
- Level `log n`: `n` lists of size 1.

At each level, the **total work to merge all lists at that
level** is *O(n)* (because every element of the original
array is touched exactly once in some merge). There are
`log n` levels. Total: *O(n log n)*.

**Trace on `[5, 2, 8, 1, 4, 3]`:**
```
merge_sort([5, 2, 8, 1, 4, 3])
├── merge_sort([5, 2, 8])
│   ├── merge_sort([5]) → [5]
│   ├── merge_sort([2, 8])
│   │   ├── merge_sort([2]) → [2]
│   │   ├── merge_sort([8]) → [8]
│   │   └── _merge([2], [8]) → [2, 8]
│   └── _merge([5], [2, 8]) → [2, 5, 8]
├── merge_sort([1, 4, 3])
│   ├── merge_sort([1]) → [1]
│   ├── merge_sort([4, 3])
│   │   ├── merge_sort([4]) → [4]
│   │   ├── merge_sort([3]) → [3]
│   │   └── _merge([4], [3]) → [3, 4]
│   └── _merge([1], [3, 4]) → [1, 3, 4]
└── _merge([2, 5, 8], [1, 3, 4]) → [1, 2, 3, 4, 5, 8]
```

**Properties:**
- **Time**: *O(n log n)* always — best, average, worst.
- **Space**: *O(n)* for the merge buffers, plus *O(log n)*
  recursion stack.
- **Stable**: Yes (with `<=` in the merge).
- **Adaptive**: No — runs the same way on any input.

**When is merge sort used?**
- When you need a **guaranteed** *O(n log n)* worst case.
- When **stability** matters (e.g., sorting by multiple keys).
- For sorting **linked lists** (where merge sort is more
  natural than quick sort).
- For **external sorting** of huge files that don't fit in
  RAM — merge sort generalizes elegantly to disk-based merges.
- As the foundation of **Timsort** (Python's built-in sort),
  which is a hybrid of merge sort and insertion sort.

Merge sort is the workhorse you can always trust.
''',
            "complexity": (
                "**Time**: *O(n log n)*. There are `log n` levels of "
                "recursion, and each level does *O(n)* merging work. "
                "This holds for the best, average, and worst case.\n\n"
                "**Space**: *O(n)*. Each merge allocates a list of "
                "size equal to its inputs. Recursion adds *O(log n)* "
                "stack depth."
            ),
        },
        "thought_process": r'''
The pivotal move in merge sort is realizing that **merging two
sorted lists is much easier than sorting from scratch**. The merge
step is one linear walk. It is so easy that we can afford to do it
*log n* times — once per level of recursion — and the total work is
*O(n log n)*.

For a beginner the leap of faith is: "I trust that the recursive
call returns a sorted list, so I just need to merge them". You
should refuse to think about what is happening inside the recursive
call. Just trust that it does what its name says.

A second insight: merge sort is **stable** if the merge uses `<=`
(not `<`) when comparing fronts. With `<=` we always prefer the
left list on ties, preserving original order. Stability matters when
you sort by one field and want to keep another field's order
unchanged.

A third insight: merge sort uses *O(n)* auxiliary memory. That is
the price for *O(n log n)* guaranteed worst case. Quick sort uses
less memory but has a quadratic worst case. Choose accordingly.

When does merge sort shine in practice?

- When data is on disk and you cannot fit it in RAM (external
  merge sort).
- When you need a stable sort.
- When you cannot afford the quadratic worst case of quick sort.
- When the data is a linked list (linked-list merge sort is
  surprisingly elegant and uses *O(log n)* stack only).
''',
        "deep_concept": r'''
Merge sort is the canonical example of the **master theorem** for
recurrences: `T(n) = 2 T(n / 2) + O(n)`, which solves to
`O(n log n)`. Once you grok this recurrence, you have a tool to
analyze a wide range of divide-and-conquer algorithms.

A beautiful adaptation: by tweaking the merge step to *count* how
many times an element from the right list "overtakes" elements from
the left, we get an *O(n log n)* algorithm for **counting
inversions** — far better than the naive *O(n²)* version. This is
Step 3 territory but it shows that small twists to merge sort yield
surprisingly powerful algorithms.

Another adaptation: merging more than two sorted lists at once
(say, K) with a min-heap is *O(N log K)* and the algorithm of
choice for merging K sorted streams. That is Step 11, the heaps
lecture.

The thread tying these together is that **the merge step is the
real magic**. Once you have two sorted things, glueing them is
nearly free. Whenever you face a problem on a single unsorted
array, ask: "what if I split into pieces I can sort cheaply, then
combine?". Many algorithmic insights begin here.
''',
        "confusion_notes": [
            {
                "question": "Why is merge sort `O(n log n)`? Where do the two factors come from?",
                "answer": r'''
The two factors come from two separate observations.

**Where the `log n` comes from**: each recursive call splits the
array in half. Starting with size `n`, the children are size
`n/2`, then `n/4`, then `n/8`, and so on. The recursion tree has
`log₂(n)` levels before the subarrays shrink to size 1.

**Where the `n` comes from**: at every level of the recursion
tree, **the total work across all subarrays is exactly `O(n)`**.
At the top level, one merge of two halves takes *O(n)* time. At
the second level, two merges of pairs of quarters take *O(n/2 +
n/2) = O(n)*. At the third level, four merges of eighth-sized
pieces take *O(n)*. Every level does *O(n)* total merging work.

Multiply: `log n` levels × `O(n)` work per level = `O(n log n)`
total.

This argument generalizes to many divide-and-conquer
algorithms. Whenever the recurrence is `T(n) = 2 T(n/2) + O(n)`
or `T(n) = a T(n/b) + f(n)` with `f(n) = O(n^(log_b(a)))`, the
**Master Theorem** gives you the answer immediately. Merge sort
is the canonical example.

A useful visual: draw the recursion tree as a triangle. Its
height is `log n`, its width (work per level) is `n`. The total
area is `n log n`. Some divide-and-conquer algorithms have
different shapes (binary search is `n = 1` work per level for
`log n` levels, giving `O(log n)`); merge sort's rectangle is
the prototype.
''',
            },
            {
                "question": "Why does the merge step use `<=` instead of `<`? Does it matter?",
                "answer": r'''
It matters when you care about **stability**.

Stability means: if two elements compare equal, the one that
came first in the original array stays first in the sorted
output. Some algorithms preserve stability automatically; others
do not. Merge sort can be either, depending on this one
comparison.

In the merge step, when the front element of the left list ties
with the front element of the right list, we have to decide
which to take first. The convention `if a[i] <= b[j]: take a` —
i.e., prefer the **left** list on ties — produces a **stable**
merge sort. The convention `if a[i] < b[j]: take a` (strict
less-than) would still produce a correct sort but it would prefer
the **right** list on ties, which can scramble the relative
order of equal elements that originated in different halves.

Why does the left-preference preserve stability? Because the
left list contains the elements that were earlier in the
*original* array (we split with `arr[:mid]` and `arr[mid:]`, so
left = earlier indices). Taking from the left first on ties
means earlier-original-position wins. Repeat this recursively
all the way up the tree, and the algorithm globally preserves
"earlier originated first."

In practice, stability matters when you sort records by one
field and want a previous secondary sort to be preserved.
Python's `sorted` is stable. Use `<=` in your merge if you want
to match that contract.
''',
            },
            {
                "question": "Why does merge sort need `O(n)` extra memory? Can't we do it in place?",
                "answer": r'''
The merge step needs an auxiliary buffer to hold the combined
result while it reads from both input halves. You cannot
correctly merge two sorted halves of the *same* array in place
without a complex algorithm — the writes would overwrite reads.

To see why, imagine merging `[2, 5]` and `[1, 3]` in place
inside `[2, 5, 1, 3]`. We compare `2` and `1`, decide `1` is
smaller, and want to write `1` to position 0. But position 0
holds `2`, which we have not consumed yet. Writing `1` there
loses `2`. We need somewhere to stash `2` first.

The simplest fix is the one we use: allocate a new list of size
`n`, walk both halves with two pointers, write the merged result
into the new list, and (optionally) copy it back. This uses
*O(n)* extra memory.

There are *in-place merge sort* algorithms, but they are either
much slower (the "block merge" variants can hit *O(n log² n)*)
or much more complex (Trabb Pardo's algorithm uses *O(1)* extra
memory but is rarely worth the code complexity).

In practice, the *O(n)* memory cost is usually fine. The
exceptions: sorting truly enormous datasets that do not fit in
RAM (where you use **external merge sort**, which streams data
from disk in chunks), and sorting linked lists (where merging
two sorted lists genuinely is *O(1)* extra memory because
pointers can be rewired without copying values).

So the rule of thumb: merge sort on arrays uses *O(n)* extra
memory; merge sort on linked lists uses *O(1)* extra memory and
*O(log n)* stack.
''',
            },
            {
                "question": "Why does the merge `extend` the leftovers at the end?",
                "answer": r'''
Because one of the two halves usually finishes first, and the
other half still has sorted elements waiting.

Picture merging `[1, 4, 6]` and `[2, 3]`. The pointers walk like
this: we take `1` from left, `2` from right, `3` from right, and
then the right list is empty. The left list still has `[4, 6]`
waiting. Those are already sorted (because each half was
recursively sorted), and they are all bigger than everything we
have placed (because anything smaller would have already moved).
So we can dump them all into the output as-is.

`merged.extend(a[i:])` does exactly that: append the rest of
`a` starting from where `i` left off. If `a` is the list that
finished first, `a[i:]` is empty and the extend is a no-op. So
both `extend` calls are safe to run unconditionally.

This is a small but important detail. Forgetting the leftover
extends produces a half-merged result that loses the tail of
whichever list ran longer. It is a classic merge bug — make
sure your merge function always drains both inputs.

In some merge implementations, you write the loop as `while i <
len(a) or j < len(b):` and check inside which pointer is still
valid before reading. That works too, but it has more branches
in the hot loop. The "main loop while both alive, then drain
the survivor" structure is usually faster and easier to read.
''',
            },
        ],
        "summary": r'''
**Pattern**: divide and conquer — split, recurse, merge.

**Lesson**: *O(n log n)* worst-case sorting via a beautifully
simple merge step. The merge two-pointer routine is the only piece
of work; the rest is recursion.

**Recognize next time**: every time you see "I can do two sorted
things easily, what if I split the unsorted input into two?", you
are reaching for the merge-sort pattern. It is the gateway drug to
the rest of divide-and-conquer.
''',
    },
    {
        "id": "quick-sort",
        "title": "Quick Sort",
        "step_id": 2,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["sorting", "divide-and-conquer", "recursion", "partition"],
        "what_this_teaches": (
            "**Partitioning** as a fundamental primitive — pick a "
            "pivot, place everything smaller on one side and "
            "everything larger on the other. The same partition step "
            "powers Quickselect (k-th smallest in *O(n)* average) and "
            "the Dutch National Flag algorithm."
        ),
        "pattern": "Partition around a pivot, recursively sort each side.",
        "prerequisite_lessons": ["sorting", "recursion"],
        "prerequisite_problems": ["merge-sort"],
        "next_problems": [
            "sort-0s-1s-2s",
            "kth-largest",
            "kth-smallest",
            "kth-element-two-sorted",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 2 (Sorting II)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "Wikipedia — Quicksort",
                "url": "https://en.wikipedia.org/wiki/Quicksort",
            },
        ],
        "understanding": r'''
Quick sort is the second divide-and-conquer sort, and it is the
default choice of most production sort libraries on dense numeric
data. The recipe:

> *Pick a "pivot" element. Rearrange the array so that everything
> smaller than the pivot sits to its left and everything larger sits
> to its right. The pivot is now in its final position. Recursively
> sort the two sides.*

Unlike merge sort, quick sort does the heavy lifting *before* the
recursive calls (the partitioning step), and the "merge" step is
trivial because the two halves are already separated.
''',
        "brute_force": {
            "explanation": r'''
There is no real "brute force" version of quick sort — it is already
*O(n log n)* on average. The interesting variation is how we choose
the pivot and how we partition. Two classic schemes are
*Lomuto partition* (simple, slower) and *Hoare partition* (more
efficient, trickier). For learning purposes we use Lomuto: always
take the last element as the pivot.
''',
            "code": r'''def quick_sort(arr: list[int]) -> None:
    _qs(arr, 0, len(arr) - 1)


def _qs(arr: list[int], lo: int, hi: int) -> None:
    # Base case: a range of 0 or 1 elements is already sorted.
    if lo >= hi:
        return
    # Partition: put the pivot in its final sorted position and
    # return that position.
    p = _partition(arr, lo, hi)
    # Recurse on the two sides. The pivot at index p is already in
    # its final spot, so we exclude it.
    _qs(arr, lo, p - 1)
    _qs(arr, p + 1, hi)


def _partition(arr: list[int], lo: int, hi: int) -> int:
    # Lomuto partition with pivot = last element of the range.
    pivot = arr[hi]
    # `store` is the next index that will receive a "small" element.
    # Everything at indices [lo .. store - 1] is < pivot.
    store = lo
    # Walk through [lo .. hi - 1] (we skip the pivot itself).
    for i in range(lo, hi):
        if arr[i] < pivot:
            # The element at i belongs on the "small" side.
            arr[i], arr[store] = arr[store], arr[i]
            store += 1
    # Place the pivot in its final spot: between the small and large
    # sides. After the swap, everything before `store` is < pivot,
    # arr[store] is the pivot, and everything after is >= pivot.
    arr[store], arr[hi] = arr[hi], arr[store]
    return store
''',
            "walkthrough": r'''
Quick sort. Different philosophy than merge sort. Instead of
splitting *then* sorting, we **partition** around a pivot
(putting smaller things on the left, larger on the right)
*then* recurse. The partition is the clever part.

**The driver: `quick_sort`**

**`def quick_sort(arr: list[int]) -> None:`** — In-place sort.

**`_qs(arr, 0, len(arr) - 1)`** — Kick off the recursion on
the full range `[0, n - 1]` (inclusive).

**The recursive worker: `_qs`**

**`def _qs(arr: list[int], lo: int, hi: int) -> None:`** —
Sorts `arr[lo..hi]` (inclusive on both ends).

**`if lo >= hi: return`** — **Base case.** A range of 0 or 1
elements is trivially sorted.

**`p = _partition(arr, lo, hi)`** — Partition the range
around a pivot. After this call:
- The pivot is at index `p`.
- Everything in `arr[lo..p-1]` is **strictly less** than the
  pivot.
- Everything in `arr[p+1..hi]` is **>= pivot**.

The pivot is now in its **final sorted position** — it never
moves again. That's the key insight.

**`_qs(arr, lo, p - 1)`** — Recursively sort the left side.

**`_qs(arr, p + 1, hi)`** — Recursively sort the right side.

Notice we **exclude `p`** from both recursive calls. The
pivot is already in place.

**The partition: `_partition`**

This is the heart of quick sort. The **Lomuto** partition
scheme uses the last element as the pivot.

**`pivot = arr[hi]`** — Pick the last element as the pivot.

**`store = lo`** — `store` will track "where the next 'small'
element should go." Invariant: everything in `arr[lo..store-1]`
is `< pivot`.

**`for i in range(lo, hi):`** — Walk through every element
**except** the pivot itself (the loop stops at `hi - 1`).

**`if arr[i] < pivot:`** — Found a "small" element (smaller
than the pivot).

**`arr[i], arr[store] = arr[store], arr[i]`** — Swap it into
the "small zone" at position `store`. The element that was at
`store` (which we know is `>= pivot` because of how `store`
advances) moves to position `i` — also fine, since it's
"large" and we're past `store`.

**`store += 1`** — Advance the boundary; the small zone is
now one element larger.

**`arr[store], arr[hi] = arr[hi], arr[store]`** — After the
loop, `arr[lo..store-1]` is `< pivot` and `arr[store..hi-1]`
is `>= pivot`. The pivot is still at `hi`. We swap it into
position `store`, the **boundary**, which is its correct
final position.

**`return store`** — Return the pivot's final position so the
recursive calls know where to split.

**Trace partition on `arr = [3, 7, 4, 1, 9, 2, 6], lo=0, hi=6`:**

```
pivot = arr[6] = 6. store = 0.
i=0, arr[0]=3 < 6: swap arr[0] with arr[0] (no-op). store=1.
i=1, arr[1]=7 not < 6: skip.
i=2, arr[2]=4 < 6: swap arr[2] with arr[1]. arr=[3,4,7,1,9,2,6]. store=2.
i=3, arr[3]=1 < 6: swap arr[3] with arr[2]. arr=[3,4,1,7,9,2,6]. store=3.
i=4, arr[4]=9 not < 6: skip.
i=5, arr[5]=2 < 6: swap arr[5] with arr[3]. arr=[3,4,1,2,9,7,6]. store=4.
Loop ends. Swap pivot (arr[6]=6) with arr[4]=9: arr=[3,4,1,2,6,7,9].
Return store = 4.
```

Now arr[0..3] = [3,4,1,2] all < 6, arr[5..6] = [7,9] all >= 6,
arr[4] = 6 in final position. Recurse on [0..3] and [5..6].

**Why is quick sort O(n log n) on average?**

If the pivot reliably splits the array near the middle, the
recursion tree has depth `log n`, and each level does *O(n)*
partition work. Total *O(n log n)*.

But the pivot choice matters. With a **bad pivot** (e.g.,
always the smallest), one side is empty and the other has
`n - 1` elements. The recursion tree degenerates to a linked
list of depth `n`, giving *O(n²)* total work.

**The classic killer**: an already-sorted array with last-
element-as-pivot. Every partition picks the largest, and the
left side gets everything. *O(n²)* on sorted input!

**Mitigation**: pick the pivot randomly, or use the
**median-of-three** rule (median of first, last, middle).
This makes the worst case astronomically unlikely.

**Properties:**
- **Time**: *O(n log n)* average, *O(n²)* worst.
- **Space**: *O(log n)* recursion stack on average.
- **Stable**: No (the swaps can reorder equal elements).
- **In-place**: Yes (no auxiliary arrays).

**When is quick sort used?**
- The most common sort in many languages' libraries (C's
  `qsort`, C++'s `std::sort` is a quicksort/introsort hybrid).
- When **in-place** sorting is required and memory is tight.
- When average-case performance and constant factors matter
  more than worst-case guarantees.

Python doesn't use quick sort by default (uses Timsort, a
merge sort variant), but most other languages do.
''',
            "complexity": (
                "**Time**: *O(n log n)* average. *O(n²)* worst case "
                "(already-sorted input with a naive last-element "
                "pivot is the classic killer).\n\n"
                "**Space**: *O(log n)* recursion depth on average, "
                "*O(n)* worst case."
            ),
        },
        "thought_process": r'''
The clever insight in quick sort is that *one* swap can do the work
of many comparisons. After the partition step, the pivot is **in
its final position** — it will never move again. That is more
information than any pass of bubble or insertion sort gives us.

The price is that the algorithm's performance depends on **the
quality of the pivot**. A perfectly balanced pivot splits the
remaining elements into two equal halves; the recursion tree is
`log n` deep. A terrible pivot (the smallest or largest element)
puts all `n - 1` remaining elements on one side; the recursion tree
is `n` deep, and we are back to *O(n²)*.

To avoid the worst case in practice, real implementations use one
of:

- **Random pivot**: pick a random index. Expected runtime
  *O(n log n)*. Adversarial inputs cannot trigger the worst case.
- **Median-of-three**: take the median of `arr[lo]`, `arr[mid]`,
  `arr[hi]`. Cheap and very effective on real data.
- **Introsort**: start with quick sort but fall back to heap sort
  if recursion depth exceeds a threshold. Guarantees *O(n log n)*
  worst case.

C++ std::sort is introsort under the hood. Python's `sorted` is
Timsort, which is merge-sort-based. Both are excellent and you
should rarely write your own.
''',
        "deep_concept": r'''
The deep idea is **partition as a primitive**. Once you can
partition an array around a pivot in *O(n)*, you can do much more
than sort:

- **Quickselect**: find the k-th smallest element in *O(n)* average
  time. Same partition routine; recurse on only one side.
- **Dutch national flag**: 3-way partition. You walk three pointers
  (low, mid, high) and rearrange around two pivot values. This is
  the algorithm behind "sort 0s, 1s, and 2s" in Step 3.
- **In-place selection algorithms** for many statistical questions.

The partition operation is so versatile that it is worth
implementing it carefully once and reusing it everywhere.

Another deep observation: quick sort is **not stable** as usually
implemented. The swaps inside `_partition` can leap an element past
an equal one. If stability matters, prefer merge sort.

Finally: quick sort is a tale about averages versus worst cases. In
real-world data, *O(n²)* almost never happens, and the much smaller
memory footprint of quick sort makes it the winner. In adversarial
contexts (a malicious user choosing inputs), random pivots or
introsort restore the worst-case guarantee.
''',
        "confusion_notes": [
            {
                "question": "Why does quick sort have a worst case of `O(n²)` if it's `O(n log n)` on average?",
                "answer": r'''
The worst case happens when the **pivot is the smallest or
largest element of the subarray every single time**. When that
happens, the partition step splits the subarray into a zero-sized
half and an `n - 1` sized half, and the recursion tree degenerates
into a chain of length `n` instead of a balanced tree of depth
`log n`.

Concretely: suppose your pivot is always the last element, and
your input is already sorted ascending. The pivot is the largest
element of every subarray, so partition puts all `n - 1` other
elements on the "smaller" side. Then you recurse on a subarray of
size `n - 1`, which again has the largest element at the end. And
so on. The total work is `n + (n - 1) + (n - 2) + ... + 1 =
O(n²)`.

That same bad case applies to reverse-sorted input with a
first-element pivot, or any "adversarial" input that the pivot
choice cannot escape from.

The fix is to **randomize the pivot** or use **median-of-three**.
With a random pivot, the expected depth is `O(log n)` even on
adversarial input, because no input can consistently fool a
random choice. Most production quick sorts (introsort, in
particular) use median-of-three and also fall back to heap sort
if recursion gets too deep, guaranteeing `O(n log n)` worst case.

The bottom line: textbook quick sort with a last-element pivot is
*O(n²)* on sorted input. Real quick sort uses randomization or
median-of-three, which makes the *O(n²)* case essentially never
happen.
''',
            },
            {
                "question": "What exactly does the partition function do, step by step?",
                "answer": r'''
The partition function rearranges the subarray `arr[lo..hi]` so
that the pivot (taken here as `arr[hi]`) ends up in its **final
sorted position**, with all smaller elements to its left and all
larger elements to its right.

Walk through it on `arr = [5, 3, 8, 4, 7, 6]` with `lo = 0`, `hi
= 5`, so the pivot is `arr[5] = 6`.

Initialize `store = lo = 0`. The variable `store` is "where the
next element less than the pivot should land."

Now scan `i` from `lo` to `hi - 1`:

- `i = 0`: `arr[i] = 5 < 6 = pivot`. Swap `arr[0]` with
  `arr[store=0]` (a no-op), then bump store to 1. Array
  unchanged.
- `i = 1`: `arr[i] = 3 < 6`. Swap `arr[1]` with `arr[store=1]`
  (no-op), bump store to 2.
- `i = 2`: `arr[i] = 8 >= 6`. Skip; do not bump store.
- `i = 3`: `arr[i] = 4 < 6`. Swap `arr[3]` with `arr[store=2]`.
  Array becomes `[5, 3, 4, 8, 7, 6]`. Bump store to 3.
- `i = 4`: `arr[i] = 7 >= 6`. Skip.

End of scan. Now swap `arr[store=3]` with the pivot `arr[hi=5]`.
Array becomes `[5, 3, 4, 6, 7, 8]`. Return `store = 3`.

After partition, `arr[3] = 6` is in its final sorted position.
Everything to the left (`[5, 3, 4]`) is less than 6 (but not yet
sorted internally), and everything to the right (`[7, 8]`) is
greater (also not yet sorted). We recurse on the two sides.

The invariant being maintained inside the loop is:
`arr[lo..store - 1]` contains elements less than pivot,
`arr[store..i - 1]` contains elements greater or equal, and
`arr[i..hi - 1]` is the unscanned region. When the loop ends,
the entire pre-pivot region is partitioned. The final swap drops
the pivot into the boundary slot.
''',
            },
            {
                "question": "Why is quick sort not stable?",
                "answer": r'''
The partition step performs swaps that can jump an equal element
**past another equal element**, breaking the "preserve original
order on ties" property.

Consider `arr = [(2, 'a'), (1, 'x'), (2, 'b'), (3, 'y')]` sorted
by the first field, with pivot `(3, 'y')`. The partition scan
swaps `(2, 'b')` and `(1, 'x')` to bring elements `< 3` to the
front. After partition the array is something like
`[(2, 'a'), (1, 'x'), (2, 'b'), (3, 'y')]` — but in general the
relative order of the two `(2, ...)` elements can flip,
depending on which pivot choice and partition scheme you use.

Compare with merge sort: the merge step preserves stability
because when two elements tie, the convention `<=` keeps the
left-list element first, and "left" always means "earlier in the
original array."

When does stability matter? When sorting records by one field
and you want a prior order on another field preserved. For
example, sorting employees by department while keeping
alphabetical order within each department.

If you need a fast in-place sort that is also stable, you have
to pick one: merge sort (stable, `O(n)` extra memory) or
Timsort (Python's built-in `sorted`, which is stable). C++'s
`std::stable_sort` is the stable variant for C++.

For curriculum problems on plain numbers, stability rarely
matters. But always ask "does this problem need stable order?"
before reaching for `quick sort`.
''',
            },
            {
                "question": "How is Quickselect related to Quick Sort?",
                "answer": r'''
**Quickselect** uses the same partition primitive as Quick Sort,
but it solves a different problem in `O(n)` average time
instead of `O(n log n)`.

The problem Quickselect solves: *"find the k-th smallest
element of an array."* The trick: after one partition, you know
exactly where the pivot lands — say, at index `p`. If `p == k`,
the pivot IS the k-th smallest. If `p > k`, the answer is in
the left subarray, so recurse there. If `p < k`, the answer is
in the right subarray, recurse there.

```python
def quickselect(arr, lo, hi, k):
    if lo >= hi:
        return arr[lo]
    p = partition(arr, lo, hi)
    if p == k:
        return arr[p]
    elif p > k:
        return quickselect(arr, lo, p - 1, k)
    else:
        return quickselect(arr, p + 1, hi, k)
```

The key insight: unlike quick sort, Quickselect only recurses
**into one side**. So instead of doubling work at each level,
we cut it roughly in half. The expected total work is
`n + n/2 + n/4 + ... = 2n = O(n)`.

The worst case is still `O(n²)` (same bad-pivot scenario as
quick sort), but with random pivots the expected time is `O(n)`.
This is how libraries find the median, the top K, or any order
statistic without sorting the whole array.

The same partition primitive thus does double duty: drive a
full sort (Quick Sort), or pluck out a single order statistic
(Quickselect). It is one of the most reused subroutines in
practical algorithm design.
''',
            },
        ],
        "summary": r'''
**Pattern**: partition around a pivot, then recurse on the two
sides.

**Lesson**: a single well-chosen swap can "freeze" an element in
its final position. Quick sort is *O(n log n)* on average with a
worst case of *O(n²)*; pick your pivot wisely.

**Recognize next time**: any time you want to put an element in its
final position and split the rest into two groups. Quickselect
(find the k-th smallest) and the Dutch national flag are direct
descendants.
''',
    },
]
