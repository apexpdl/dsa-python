"""Sorting — the warm-up gym for algorithmic thinking."""

LESSON = {
    "id": "sorting",
    "title": "Sorting — Comparisons, Swaps, and Divide-and-Conquer",
    "tags": ["sorting", "fundamentals"],
    "summary": (
        "Why sorting is the gateway to algorithmic thinking, how each "
        "of the classic sorts tells a different story, and the rules "
        "for choosing one over another."
    ),
    "body": r'''
## Why sort?

A sorted list is dramatically easier to reason about than an
unsorted one. Searching becomes fast. Duplicates land next to each
other. Frequencies become runs. Medians sit in the middle. Many hard
problems collapse into easy ones the moment you sort, because the
sorted order **encodes** information that the input did not have.

So even though sorting itself is rarely the final goal, "sort first,
then walk" is one of the most reliable problem-solving moves in your
toolkit.

## The big four

For beginners, four sorts cover 95% of the intuition you will ever
need.

### Selection sort — the bored cashier

Imagine you are stacking books on a shelf. You look at every unsorted
book, find the smallest, and slot it into position 1. Then you do it
again for position 2, ignoring position 1. Repeat.

```python
def selection_sort(arr: list[int]) -> None:
    n = len(arr)
    for i in range(n):
        # Assume arr[i] is the smallest unsorted element...
        min_idx = i
        # ...then look at every later element to verify or replace.
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        # Swap the found minimum into position i.
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
```

Two nested loops mean *O(n²)* time, regardless of input. It is the
simplest sort to write but among the slowest to run. Useful as a
teaching tool, not for production.

### Bubble sort — the swap parade

Walk left to right. Every time two adjacent elements are out of
order, swap them. One pass guarantees the biggest element bubbles to
the end. Repeat until you do a full pass with zero swaps.

```python
def bubble_sort(arr: list[int]) -> None:
    n = len(arr)
    for end in range(n - 1, 0, -1):
        swapped = False
        for j in range(end):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # Early exit: a clean pass means the array is already sorted.
        if not swapped:
            return
```

The early exit makes bubble sort actually decent on nearly-sorted
input — *O(n)* in the best case. Worst case is still *O(n²)*.

### Insertion sort — the card player

You hold cards in your left hand, sorted. You draw one from the
deck. You slide it leftward through your hand until it sits between a
smaller card on the left and a larger card on the right.

```python
def insertion_sort(arr: list[int]) -> None:
    for i in range(1, len(arr)):
        # The value we want to insert into the sorted prefix.
        current = arr[i]
        j = i - 1
        # Slide larger neighbors one step right to make room.
        while j >= 0 and arr[j] > current:
            arr[j + 1] = arr[j]
            j -= 1
        # Drop current into the gap.
        arr[j + 1] = current
```

Beautifully simple. Surprisingly effective on small or nearly-sorted
inputs — often the fastest of the *O(n²)* sorts in practice. Most
real-world libraries fall back to insertion sort for small subarrays
even inside fancy sorts like Timsort.

### Merge sort — divide and conquer

Cut the array in half. Sort each half (by recursion, naturally).
Merge the two sorted halves by walking two indices and always taking
the smaller front element.

```python
def merge_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(a: list[int], b: list[int]) -> list[int]:
    result = []
    i = j = 0
    # Walk both lists in lockstep, picking the smaller front item.
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i]); i += 1
        else:
            result.append(b[j]); j += 1
    # Whichever list has leftovers, drain it.
    result.extend(a[i:])
    result.extend(b[j:])
    return result
```

The recursion tree has *log n* layers, each does *O(n)* work merging,
so total time is *O(n log n)*. Merge sort is **stable** (equal
elements keep their original order) and *O(n)* extra space.

### Quick sort — the gambler

Pick any element as a pivot. Partition the rest into "smaller than
pivot" and "larger than pivot". Recursively sort each side. The
pivot ends up between them, in its final position.

```python
def quick_sort(arr: list[int], lo: int = 0, hi: int | None = None) -> None:
    if hi is None:
        hi = len(arr) - 1
    if lo >= hi:
        return
    # Partition step: place the pivot in its correct final spot.
    pivot = arr[hi]
    store = lo
    for i in range(lo, hi):
        if arr[i] <= pivot:
            arr[i], arr[store] = arr[store], arr[i]
            store += 1
    arr[store], arr[hi] = arr[hi], arr[store]
    # Recurse on the two sides.
    quick_sort(arr, lo, store - 1)
    quick_sort(arr, store + 1, hi)
```

Average *O(n log n)*. Worst case *O(n²)* if pivots are unlucky
(already-sorted input is the classic killer). In-place — no extra
array needed.

## A cheat sheet

| Sort | Average | Worst | Stable? | Notes |
|---|---|---|---|---|
| Selection | *O(n²)* | *O(n²)* | No | Easiest to write |
| Bubble | *O(n²)* | *O(n²)* | Yes | *O(n)* on sorted input |
| Insertion | *O(n²)* | *O(n²)* | Yes | Fastest *O(n²)* in practice |
| Merge | *O(n log n)* | *O(n log n)* | Yes | Needs extra space |
| Quick | *O(n log n)* | *O(n²)* | No | In-place, fast in practice |

## What does Python's `sorted` actually do?

Python's `sorted` (and `list.sort`) uses **Timsort**, a hybrid of
merge sort and insertion sort tuned for real-world input. It is
*O(n log n)*, stable, and dramatically fast on partially-sorted data.
For all practical purposes you should call `sorted` rather than
writing your own. But knowing how it works under the hood is exactly
what these classical sorts teach.

## When does sorting matter?

Sort first when:

1. Order itself is the answer (e.g., "return the k largest").
2. You need to put duplicates next to each other.
3. You want to binary search later.
4. Two pointers from opposite ends would unlock a solution.
5. You need to group by some key (sort by key, then walk).

If none of those apply, sorting is a free *O(n log n)* you do not
need to pay.

## Common beginner mistakes

**Mistake 1: thinking sorting is free.** It is not. *O(n log n)* is
fast, but inside an already-*O(n)* algorithm you have to ask whether
you are about to make it *O(n log n)* by sorting.

**Mistake 2: re-sorting inside a loop.** Sorting once before a loop
is *O(n log n)*. Sorting inside a loop is *O(n² log n)* and almost
always wrong.

**Mistake 3: forgetting stability.** When sorting tuples, equal first
elements stay in their original order in a stable sort. This matters
for problems like "sort by score, then by name (alphabetical) for
ties" — you can sort twice and rely on stability.

**Mistake 4: writing a custom comparator like in C++/Java.** In
Python, use `key=` for sort keys: `sorted(items, key=lambda x: x[1])`.
The `cmp_to_key` adapter exists but you rarely need it.

## The mental model

A sort is a one-time investment that pays off many times over.
*"Should I sort first?"* should be a question you ask reflexively
when you see an array problem. If sorting unlocks even one cheap
walk-through, it is usually worth the *O(n log n)* up-front cost.
''',
}
