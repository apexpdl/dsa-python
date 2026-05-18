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
