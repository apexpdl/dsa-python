"""Step 3 extras — the remaining array problems.

Easy: check-array-sorted, left-rotate-by-one, left-rotate-by-d,
move-zeros-to-end, linear-search, union-of-sorted-arrays,
intersection-of-sorted-arrays.

Medium: print-max-subarray, rearrange-alternating, next-permutation,
leaders-in-array, set-matrix-zeros, rotate-matrix-90,
spiral-traversal, subarrays-with-sum-k.

Hard: pascals-triangle, majority-element-n3, three-sum, four-sum,
longest-subarray-zero-sum, subarrays-with-xor-k,
merge-two-sorted-no-extra-space, repeating-and-missing,
count-inversions, reverse-pairs, max-product-subarray.
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
    # =================================================================
    # Lecture 1 — Easy (7 remaining problems)
    # =================================================================
    {
        "id": "check-array-sorted",
        "title": "Check if an Array is Sorted",
        "step_id": 3,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["arrays", "linear-scan"],
        "what_this_teaches": "Single-pass adjacent comparison — the most basic 'verify a property' pattern.",
        "pattern": "Walk once; if any adjacent pair is out of order, fail.",
        "prerequisite_lessons": ["arrays"],
        "prerequisite_problems": ["largest-element"],
        "next_problems": ["remove-duplicates-sorted", "binary-search"],
        "resources": [_SHEET, _lc(1752, "check-if-array-is-sorted-and-rotated")],
        "understanding": r'''
Given an array, return `True` if it is sorted in non-decreasing
order. Otherwise return `False`.

The check: walk once, compare each element with its successor.
If you ever see `arr[i] > arr[i + 1]`, the array is not sorted.

```python
def is_sorted(arr):
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True
```

*O(n)* time, *O(1)* space. Short-circuits on the first
violation.

A Pythonic alternative:

```python
def is_sorted(arr):
    return all(a <= b for a, b in zip(arr, arr[1:]))
```

`zip(arr, arr[1:])` pairs each element with its successor.
`all(...)` short-circuits on the first False.

**Variation**: strict-ascending (no duplicates). Use `<` instead
of `<=`.

**Variation**: rotated-sorted (sorted, then rotated some
amount). Count "drop" points; the array is rotated-sorted iff
there is exactly one drop (or zero for fully sorted) and
`arr[-1] <= arr[0]`. This is the basis of LeetCode 1752.
''',
        "summary": "**Pattern**: adjacent-pair check in one pass. The simplest property-verification scan.",
    },
    {
        "id": "left-rotate-by-one",
        "title": "Left Rotate an Array by One Place",
        "step_id": 3,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["arrays", "rotation"],
        "what_this_teaches": "In-place rotation by saving the first element, shifting, and dropping it at the end.",
        "pattern": "Save first, shift left, place at end.",
        "prerequisite_lessons": ["arrays"],
        "prerequisite_problems": ["remove-duplicates-sorted"],
        "next_problems": ["left-rotate-by-d", "move-zeros-to-end"],
        "resources": [_SHEET],
        "understanding": r'''
Rotate the array one position to the left. The first element
goes to the back; everyone else shifts left by one.

`[1, 2, 3, 4, 5]` → `[2, 3, 4, 5, 1]`.

```python
def rotate_left_by_one(arr):
    if not arr:
        return
    first = arr[0]
    for i in range(len(arr) - 1):
        arr[i] = arr[i + 1]
    arr[-1] = first
```

*O(n)* time, *O(1)* space.

The discipline: save the element you are about to overwrite. We
save `arr[0]` first because the shifting loop will overwrite it
on iteration 0. Without the save, `arr[0]` is gone forever.

A Pythonic shortcut:

```python
def rotate_left_by_one(arr):
    arr[:] = arr[1:] + arr[:1]
```

The `arr[:] = ...` replaces the contents in place; slicing
creates a new list. Same complexity but with extra allocation.
Use the explicit loop for in-place clarity.
''',
        "summary": "**Pattern**: save first, shift left, place at end.",
    },
    {
        "id": "left-rotate-by-d",
        "title": "Left Rotate an Array by D Places",
        "step_id": 3,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["arrays", "rotation", "reverse"],
        "what_this_teaches": "The 'three reversals' trick — rotation as a composition of three in-place reversals.",
        "pattern": "Reverse first d, reverse rest, reverse all (or reverse all first, then halves).",
        "prerequisite_lessons": ["arrays"],
        "prerequisite_problems": ["left-rotate-by-one", "reverse-an-array-recursion"],
        "next_problems": ["rotations-count"],
        "resources": [_SHEET, _lc(189, "rotate-array")],
        "understanding": r'''
Rotate the array `d` positions to the left.

`[1, 2, 3, 4, 5]`, `d = 2` → `[3, 4, 5, 1, 2]`.

## Brute force: rotate by one, d times

*O(n × d)*. Each call is *O(n)*; we do it `d` times. Slow for
large `d`.

## Extra-array

Make a new array of size `n`; copy elements to their rotated
positions. *O(n)* time, *O(n)* space.

```python
def rotate(arr, d):
    n = len(arr)
    d %= n                       # handle d > n
    result = [0] * n
    for i in range(n):
        result[i] = arr[(i + d) % n]
    arr[:] = result
```

## The three-reversal trick (*O(n)* time, *O(1)* space)

A beautiful in-place algorithm:

1. Reverse `arr[0 : d]`.
2. Reverse `arr[d : n]`.
3. Reverse the whole array.

Or equivalently:

1. Reverse the whole array.
2. Reverse `arr[0 : n - d]`.
3. Reverse `arr[n - d : n]`.

Walk through with `arr = [1, 2, 3, 4, 5]`, `d = 2`:

- Reverse `arr[0:2]`: `[2, 1, 3, 4, 5]`.
- Reverse `arr[2:5]`: `[2, 1, 5, 4, 3]`.
- Reverse all: `[3, 4, 5, 1, 2]`. Done.

```python
def reverse_in_place(arr, lo, hi):
    while lo < hi:
        arr[lo], arr[hi] = arr[hi], arr[lo]
        lo += 1
        hi -= 1

def rotate(arr, d):
    n = len(arr)
    d %= n
    reverse_in_place(arr, 0, d - 1)
    reverse_in_place(arr, d, n - 1)
    reverse_in_place(arr, 0, n - 1)
```

*O(n)* time, *O(1)* extra space. This is the "production" answer
for array rotation.

The trick generalizes to "reverse words in a string," where you
reverse the whole string then each word. Same algebra.
''',
        "summary": "**Pattern**: three reversals for in-place rotation. The same identity behind reverse-words.",
    },
    {
        "id": "move-zeros-to-end",
        "title": "Move All Zeros to the End",
        "step_id": 3,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["arrays", "two-pointers", "in-place"],
        "what_this_teaches": "Two-pointer in-place compaction with the order of non-zeros preserved.",
        "pattern": "slow / fast pointers: slow writes non-zeros; fast scans.",
        "prerequisite_lessons": ["arrays", "two-pointers"],
        "prerequisite_problems": ["remove-duplicates-sorted"],
        "next_problems": ["rearrange-alternating"],
        "resources": [_SHEET, _lc(283, "move-zeroes")],
        "understanding": r'''
Move all zeros in the array to the end. Preserve the order of
the non-zero elements. Do it in place.

`[0, 1, 0, 3, 12]` → `[1, 3, 12, 0, 0]`.

## Two-pointer in-place compaction

A `write` pointer marks where the next non-zero should land.
A `read` pointer scans every position.

```python
def move_zeros(arr):
    write = 0
    for read in range(len(arr)):
        if arr[read] != 0:
            arr[write], arr[read] = arr[read], arr[write]
            write += 1
```

When `read` finds a non-zero, it swaps with `arr[write]` and
both advance. When `read` finds a zero, only `read` advances.

After the loop, all non-zeros are at the front in their original
order; all zeros are at the back.

*O(n)* time, *O(1)* extra space.

## Why swap and not just copy?

If you copy `arr[write] = arr[read]` without the swap, you lose
the zeros that were in front. Walk through `[0, 1]`: copy
`arr[0] = 1`, advance both. Now `arr = [1, 1]` — the zero is
gone. The swap version correctly produces `[1, 0]`.

The swap exchanges the non-zero forward with the zero (or
already-processed non-zero) that's currently at `write`. The
zeros pile up after the `write` pointer naturally.

## Pythonic two-line

```python
def move_zeros(arr):
    arr.sort(key=lambda x: x == 0)    # stable sort; zeros come last
```

Works because `bool` is `True`/`False` = `1`/`0`. Zeros get the
key `True` = 1; non-zeros get `False` = 0. Stable sort keeps
relative order within each group. *O(n log n)* time.

For DSA practice, write the two-pointer version. For prod code,
either works.
''',
        "summary": "**Pattern**: slow/fast pointer in-place compaction.",
    },
    {
        "id": "linear-search",
        "title": "Linear Search",
        "step_id": 3,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["arrays", "search"],
        "what_this_teaches": "The honest *O(n)* search — when the array is unsorted, this is the algorithm.",
        "pattern": "Walk until found.",
        "prerequisite_lessons": ["arrays"],
        "prerequisite_problems": [],
        "next_problems": ["binary-search", "two-sum"],
        "resources": [_SHEET],
        "understanding": r'''
Given an array and a target, return the index of the target if
present, else -1.

```python
def linear_search(arr, target):
    for i, x in enumerate(arr):
        if x == target:
            return i
    return -1
```

*O(n)* time, *O(1)* space.

That is the entire algorithm. For unsorted arrays, you cannot do
better than *O(n)* — you must examine every element in the worst
case.

Python ships this as `arr.index(target)`, which raises
`ValueError` on miss instead of returning -1. Both behaviors are
common; pick what the problem wants.

For sorted arrays, binary search gives *O(log n)*. If you find
yourself doing many linear searches on the same data, consider
either:

- **Sorting** + binary search: *O(n log n + q log n)* for q
  queries.
- **Hashing**: *O(n + q)* to build a set then check.

For one-off searches, plain linear search is correct and clean.
''',
        "summary": "**Pattern**: walk until found. *O(n)* baseline for unsorted data.",
    },
    {
        "id": "union-of-sorted-arrays",
        "title": "Union of Two Sorted Arrays",
        "step_id": 3,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["arrays", "two-pointers", "merge"],
        "what_this_teaches": "The merge step of merge sort, with deduplication. Two-pointer walk to combine sorted inputs.",
        "pattern": "Two pointers; take smaller; skip duplicates of the previously-taken value.",
        "prerequisite_lessons": ["arrays", "two-pointers"],
        "prerequisite_problems": ["merge-sort"],
        "next_problems": ["intersection-of-sorted-arrays", "merge-two-sorted-no-extra-space"],
        "resources": [_SHEET],
        "understanding": r'''
Given two sorted arrays, return their union as a sorted array
without duplicates.

`[1, 2, 3, 4]` ∪ `[2, 3, 5, 6]` → `[1, 2, 3, 4, 5, 6]`.

## Brute force

Concatenate, dedupe via set, sort. *O((n + m) log (n + m))*.

```python
def union_brute(a, b):
    return sorted(set(a) | set(b))
```

Correct, simple, throws away the sortedness of the inputs.

## Two-pointer merge

Walk both arrays simultaneously. At each step, take the smaller
front element — but skip if it equals the last value added to
the result (deduplication).

```python
def union(a, b):
    i = j = 0
    result = []
    while i < len(a) and j < len(b):
        x = a[i] if a[i] <= b[j] else b[j]
        if not result or result[-1] != x:
            result.append(x)
        if a[i] <= b[j]:
            i += 1
        else:
            j += 1
    # Drain whichever ran longer.
    for x in a[i:] + b[j:]:
        if not result or result[-1] != x:
            result.append(x)
    return result
```

*O(n + m)* time, *O(n + m)* output space.

## Why this matters

The merge step is the same one merge sort uses. Mastering it
here pays off for "merge K sorted lists" and "merge two sorted
arrays in place."

The deduplication is the new twist. Compare the candidate
against `result[-1]` — if equal, skip the append.
''',
        "summary": "**Pattern**: merge-style two-pointer walk + dedupe by checking against result's tail.",
    },
    {
        "id": "intersection-of-sorted-arrays",
        "title": "Intersection of Two Sorted Arrays",
        "step_id": 3,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["arrays", "two-pointers"],
        "what_this_teaches": "Two-pointer walk that advances both on match and only the smaller on mismatch.",
        "pattern": "Two pointers; match → take and advance both; mismatch → advance smaller.",
        "prerequisite_lessons": ["arrays", "two-pointers"],
        "prerequisite_problems": ["union-of-sorted-arrays"],
        "next_problems": ["three-sum"],
        "resources": [_SHEET, _lc(349, "intersection-of-two-arrays")],
        "understanding": r'''
Given two sorted arrays, return the intersection (elements
appearing in both). Return distinct values.

`[1, 2, 2, 3, 4]` ∩ `[2, 2, 4, 5]` → `[2, 4]`.

## Two-pointer walk

```python
def intersection(a, b):
    i = j = 0
    result = []
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            if not result or result[-1] != a[i]:
                result.append(a[i])
            i += 1
            j += 1
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1
    return result
```

Three cases per step:

- `a[i] == b[j]`: match. Add to result (if not duplicate),
  advance both.
- `a[i] < b[j]`: `a[i]` cannot match anything we have not seen
  in `b`. Skip it; advance `i`.
- `a[i] > b[j]`: symmetric. Advance `j`.

*O(n + m)* time. Each pointer advances at least once per
iteration, total iterations bounded by `n + m`.

## Alternative: hashing

```python
def intersection(a, b):
    return list(set(a) & set(b))
```

Works on unsorted input too. *O(n + m)* time, *O(n + m)* space.
Slightly cleaner but loses the order that the two-pointer
version preserves.

For sorted inputs, prefer two-pointer because it requires no
extra hash table.
''',
        "summary": "**Pattern**: two pointers; match advances both, mismatch advances the smaller.",
    },
    # =================================================================
    # Lecture 2 — Medium (8 remaining problems)
    # =================================================================
    {
        "id": "print-max-subarray",
        "title": "Print the Subarray with Maximum Sum",
        "step_id": 3,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["arrays", "kadane", "dp"],
        "what_this_teaches": "Kadane's algorithm extended to track the actual indices of the best subarray.",
        "pattern": "Track start/end indices alongside Kadane's running max.",
        "prerequisite_lessons": ["arrays", "dp"],
        "prerequisite_problems": ["kadane-algorithm"],
        "next_problems": ["max-product-subarray", "stock-buy-sell"],
        "resources": [_SHEET, _lc(53, "maximum-subarray")],
        "understanding": r'''
Same as Kadane's max-subarray-sum, but also return the actual
subarray (or its start/end indices).

Track three extra scalars: `start` (the current candidate's
start), `best_start` and `best_end` (the global best so far).

```python
def max_subarray_with_indices(arr):
    best_ending_here = arr[0]
    best_overall = arr[0]
    start = best_start = best_end = 0
    for i in range(1, len(arr)):
        if best_ending_here + arr[i] < arr[i]:
            # Start fresh: arr[i] alone is better than extending.
            start = i
            best_ending_here = arr[i]
        else:
            best_ending_here += arr[i]
        if best_ending_here > best_overall:
            best_overall = best_ending_here
            best_start = start
            best_end = i
    return best_overall, arr[best_start:best_end + 1]
```

When we "start fresh" at index `i` (because the running sum
would drop below `arr[i]`), we reset `start = i`. When the
global best improves, we snapshot `best_start = start` and
`best_end = i`.

*O(n)* time, *O(1)* extra space (the output slice doesn't
count).

This is the standard generalization: any "best running" problem
can be extended to also report the indices by adding 2-3 extra
scalars. Same algorithmic shape; just more bookkeeping.
''',
        "summary": "**Pattern**: Kadane + index tracking. Two more scalars.",
    },
    {
        "id": "rearrange-alternating",
        "title": "Rearrange Array Alternating Positive and Negative",
        "step_id": 3,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["arrays", "two-pointers"],
        "what_this_teaches": "Interleave-by-construction — separate into two groups, then merge them index-by-index.",
        "pattern": "Split into two arrays; interleave.",
        "prerequisite_lessons": ["arrays"],
        "prerequisite_problems": ["move-zeros-to-end"],
        "next_problems": ["next-permutation"],
        "resources": [_SHEET, _lc(2149, "rearrange-array-elements-by-sign")],
        "understanding": r'''
Given an array with equal numbers of positives and negatives,
rearrange so they alternate. The LeetCode version specifies "
positive first" — `[1, -2, 3, -4, 5, -6]` style.

## Two-array approach

Build two lists, then interleave:

```python
def rearrange(arr):
    pos = [x for x in arr if x > 0]
    neg = [x for x in arr if x < 0]
    result = []
    for p, n in zip(pos, neg):
        result.append(p)
        result.append(n)
    return result
```

*O(n)* time, *O(n)* space.

## Two-pointer in place (when sign-counts are equal)

Maintain a pointer for the next positive slot (0, 2, 4, ...) and
another for the next negative slot (1, 3, 5, ...). Walk the
array; for each element, place it in the next available slot of
its sign.

```python
def rearrange_inplace(arr):
    n = len(arr)
    result = [0] * n
    p, q = 0, 1
    for x in arr:
        if x > 0:
            result[p] = x
            p += 2
        else:
            result[q] = x
            q += 2
    return result
```

Still *O(n)* extra memory but with a different structure. True
*O(1)* in-place rearrangement is harder and rarely worth the
complexity.

## When counts differ

If positives and negatives have unequal counts, the problem
usually says "exhaust the equal pairs first, then append the
leftovers." Adjust the merge accordingly.
''',
        "summary": "**Pattern**: split-and-interleave for alternating arrays.",
    },
    {
        "id": "next-permutation",
        "title": "Next Permutation",
        "step_id": 3,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["arrays", "math", "permutations"],
        "what_this_teaches": "The lexicographic next-permutation algorithm — beautiful three-step procedure that finds the next 'word' in dictionary order.",
        "pattern": "Find pivot from the right; find swap partner; reverse the suffix.",
        "prerequisite_lessons": ["arrays"],
        "prerequisite_problems": ["left-rotate-by-d"],
        "next_problems": ["permutations"],
        "resources": [_SHEET, _lc(31, "next-permutation")],
        "understanding": r'''
Given an array of integers (interpreted as a sequence), produce
the **lexicographically next greater permutation**. If the array
is already the greatest (sorted descending), wrap around to the
smallest (sorted ascending).

For `[1, 2, 3]` → `[1, 3, 2]`. For `[1, 3, 2]` → `[2, 1, 3]`.
For `[3, 2, 1]` → `[1, 2, 3]`.

## The algorithm

1. **Find the pivot**: walk from the right; find the first index
   `i` where `arr[i] < arr[i + 1]`. (Everything right of `i` is
   non-increasing.)
2. **Find the swap partner**: walk from the right; find the
   first index `j` where `arr[j] > arr[i]`.
3. **Swap** `arr[i]` and `arr[j]`.
4. **Reverse** the suffix `arr[i + 1:]`.

If no pivot exists (step 1 fails), the array is sorted
descending; reverse the entire array to wrap to the smallest
permutation.

```python
def next_permutation(arr):
    n = len(arr)
    # Step 1: find the pivot
    i = n - 2
    while i >= 0 and arr[i] >= arr[i + 1]:
        i -= 1
    if i >= 0:
        # Step 2 & 3: find swap partner from the right, swap
        j = n - 1
        while arr[j] <= arr[i]:
            j -= 1
        arr[i], arr[j] = arr[j], arr[i]
    # Step 4: reverse the suffix
    arr[i + 1:] = arr[i + 1:][::-1]
```

*O(n)* time, *O(1)* space.

## Why does this work?

The intuition: a permutation's "next" version differs from the
current one only in the tail. We want to make the smallest
possible increase. The pivot is where we increase — find the
rightmost position where increasing is still possible (i.e.,
some element to its right is larger).

After the swap, the suffix is still sorted descending (because
we picked the smallest `arr[j] > arr[i]` from the right). To
minimize the result, we reverse the suffix to make it ascending.

This is one of the prettiest array algorithms in DSA. Trace it
on a few examples to feel the pattern.
''',
        "summary": "**Pattern**: pivot → swap → reverse suffix.",
    },
    {
        "id": "leaders-in-array",
        "title": "Leaders in an Array",
        "step_id": 3,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["arrays", "linear-scan"],
        "what_this_teaches": "Right-to-left scan with a running maximum — every element is a leader iff it beats everything to its right.",
        "pattern": "Scan right-to-left; track max-so-far; collect leaders.",
        "prerequisite_lessons": ["arrays"],
        "prerequisite_problems": ["largest-element"],
        "next_problems": ["next-greater-element-i"],
        "resources": [_SHEET],
        "understanding": r'''
An element is a **leader** if it is greater than every element
to its right. The rightmost element is always a leader (no
elements to its right).

`[16, 17, 4, 3, 5, 2]` → leaders are `[17, 5, 2]`.

## Right-to-left scan with running max

```python
def leaders(arr):
    result = []
    max_so_far = float("-inf")
    for x in reversed(arr):
        if x > max_so_far:
            result.append(x)
            max_so_far = x
    return result[::-1]      # restore original order
```

We scan from the right, tracking the maximum of "everything to
the right of the current element." If the current element beats
that max, it's a leader. Update the max.

We collect in reverse order, then flip at the end to match the
original left-to-right order.

*O(n)* time, *O(n)* space for the result (could be less if you
print or stream).

## Brute force

For each element, scan everything to its right. *O(n²)*.

The right-to-left running-max trick is a small but elegant
optimization. The same pattern handles "next greater element"
(with a stack), "Stock span" (also a stack), and similar
forward/backward lookups.
''',
        "summary": "**Pattern**: right-to-left scan, running max. Single-pass leader identification.",
    },
    {
        "id": "set-matrix-zeros",
        "title": "Set Matrix Zeroes",
        "step_id": 3,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["matrix", "in-place"],
        "what_this_teaches": "Using the matrix itself as auxiliary storage — encode 'this row/col should be zero' in the first row and column.",
        "pattern": "First row/col as marker flags; sweep and zero out.",
        "prerequisite_lessons": ["arrays"],
        "prerequisite_problems": ["sort-0s-1s-2s"],
        "next_problems": ["rotate-matrix-90", "spiral-traversal"],
        "resources": [_SHEET, _lc(73, "set-matrix-zeroes")],
        "understanding": r'''
Given an `m × n` matrix, if any cell is 0, set its entire row
and column to 0. Do it in place.

## Brute force with extra storage

Two arrays: `rows_to_zero` and `cols_to_zero`. Walk the matrix
once to flag; walk again to apply. *O(m × n)* time, *O(m + n)*
extra space.

## O(1) extra space

Use the matrix's **first row and first column** as the flag
arrays. We need two extra booleans to remember whether row 0 and
column 0 themselves originally contained a zero (because the
flagging process would overwrite that info).

```python
def set_zeroes(matrix):
    m, n = len(matrix), len(matrix[0])
    first_row_has_zero = any(matrix[0][j] == 0 for j in range(n))
    first_col_has_zero = any(matrix[i][0] == 0 for i in range(m))

    # Flag using first row/col as markers
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0

    # Apply: zero out rows and columns based on flags
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0

    # Finally, handle the first row and column
    if first_row_has_zero:
        for j in range(n):
            matrix[0][j] = 0
    if first_col_has_zero:
        for i in range(m):
            matrix[i][0] = 0
```

*O(m × n)* time, *O(1)* extra space.

The pattern: when extra memory is tight, **reuse the input as
auxiliary storage**. The first row/column trick is the canonical
example.
''',
        "summary": "**Pattern**: use first row/col as flag arrays for in-place zeroing.",
    },
    {
        "id": "rotate-matrix-90",
        "title": "Rotate Matrix by 90 Degrees",
        "step_id": 3,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["matrix", "in-place"],
        "what_this_teaches": "Transpose + reverse rows = 90° clockwise rotation. A beautiful two-step in-place algorithm.",
        "pattern": "Transpose along the diagonal, then reverse each row.",
        "prerequisite_lessons": ["arrays"],
        "prerequisite_problems": ["set-matrix-zeros"],
        "next_problems": ["spiral-traversal"],
        "resources": [_SHEET, _lc(48, "rotate-image")],
        "understanding": r'''
Rotate an `n × n` matrix 90° clockwise, in place.

```
1 2 3        7 4 1
4 5 6   →    8 5 2
7 8 9        9 6 3
```

## Two-step algorithm

**Step 1: Transpose** — flip along the main diagonal.

```
1 2 3        1 4 7
4 5 6   →    2 5 8
7 8 9        3 6 9
```

**Step 2: Reverse each row** — flip horizontally.

```
1 4 7        7 4 1
2 5 8   →    8 5 2
3 6 9        9 6 3
```

```python
def rotate(matrix):
    n = len(matrix)
    # Step 1: transpose
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # Step 2: reverse each row
    for row in matrix:
        row.reverse()
```

*O(n²)* time, *O(1)* extra space.

## Why does this work?

A 90° clockwise rotation maps `(i, j) → (j, n - 1 - i)`.
Transpose maps `(i, j) → (j, i)`. Row reverse maps `(j, i) →
(j, n - 1 - i)`. Compose: `(i, j) → (j, i) → (j, n - 1 - i)`.
Done.

For **counter-clockwise** 90°: transpose, then reverse each
**column** (or reverse columns, then transpose).

For **180°**: reverse the whole 2D structure — either reverse
rows then columns, or equivalently flip the matrix top-bottom
then left-right.

These compose-of-flips identities are the same ones used in
"reverse words in a string." Once you internalize transpose +
flip, you can derive any rotation.
''',
        "summary": "**Pattern**: transpose + reverse each row = 90° clockwise rotation in place.",
    },
    {
        "id": "spiral-traversal",
        "title": "Spiral Traversal of a Matrix",
        "step_id": 3,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["matrix", "simulation"],
        "what_this_teaches": "Four-walls simulation — maintain top/bottom/left/right boundaries and walk around them.",
        "pattern": "Top row →, right column ↓, bottom row ←, left column ↑; shrink the walls each loop.",
        "prerequisite_lessons": ["arrays"],
        "prerequisite_problems": ["rotate-matrix-90"],
        "next_problems": [],
        "resources": [_SHEET, _lc(54, "spiral-matrix")],
        "understanding": r'''
Given an `m × n` matrix, return all elements in spiral order
(outer ring, then inner, ...).

```
 1  2  3  4         1, 2, 3, 4,
 5  6  7  8    →    8, 12, 11, 10, 9,
 9 10 11 12         5, 6, 7
```

## Four-walls simulation

Maintain four boundary pointers: `top`, `bottom`, `left`,
`right`. Repeat: walk along the top row, then the right column,
then the bottom row, then the left column. Shrink the
appropriate boundary after each direction.

```python
def spiral_order(matrix):
    if not matrix:
        return []
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for j in range(left, right + 1):
            result.append(matrix[top][j])
        top += 1
        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1
        if top <= bottom:
            for j in range(right, left - 1, -1):
                result.append(matrix[bottom][j])
            bottom -= 1
        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1
    return result
```

The two `if` checks at the bottom are needed to handle the case
where the matrix has only one row or one column left — without
them we would double-traverse.

*O(m × n)* time, *O(1)* extra space (the result is the output).

## When to use

Beyond the problem itself, the four-walls simulation pattern
applies to anything that traverses a 2D region in concentric
layers: spiral fill, anti-clockwise spiral, "matrix layers"
problems.
''',
        "summary": "**Pattern**: four boundary pointers; shrink after each direction.",
    },
    {
        "id": "subarrays-with-sum-k",
        "title": "Number of Subarrays with Sum K",
        "step_id": 3,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["arrays", "prefix-sum", "hashing"],
        "what_this_teaches": "The prefix-sum + hash trick for *counting* subarrays (versus the *longest* variant).",
        "pattern": "Count occurrences of each prefix sum; for each new prefix, add count of (prefix - K) seen.",
        "prerequisite_lessons": ["arrays", "hashing"],
        "prerequisite_problems": ["longest-subarray-with-sum-k", "two-sum"],
        "next_problems": ["subarrays-with-xor-k", "binary-subarrays-with-sum"],
        "resources": [_SHEET, _lc(560, "subarray-sum-equals-k")],
        "understanding": r'''
Count the number of contiguous subarrays whose sum equals K.

`[1, 1, 1]`, K = 2 → 2 subarrays (`[1,1]` at indices 0-1 and
1-2).

## Brute force

Two loops; running sum. *O(n²)*.

## Prefix sum + hash

A subarray `arr[i..j]` sums to K iff `prefix[j+1] - prefix[i] =
K`, i.e., `prefix[i] = prefix[j+1] - K`.

For each new prefix sum `p`, we want to know **how many earlier
prefix sums equal `p - K`** — that's the count of subarrays
ending at the current position with sum K.

Maintain a `Counter` of prefix sums seen so far. Seed it with
`{0: 1}` to handle subarrays starting at index 0.

```python
from collections import Counter

def subarrays_with_sum_k(arr, k):
    prefix_count = Counter({0: 1})
    prefix = 0
    count = 0
    for x in arr:
        prefix += x
        count += prefix_count.get(prefix - k, 0)
        prefix_count[prefix] += 1
    return count
```

*O(n)* time, *O(n)* space.

The contrast with `longest-subarray-with-sum-k`:

- Longest: store the **first** index of each prefix sum; compute
  the longest matching length.
- Count: store the **count** of each prefix sum; sum up the
  matches.

Same prefix-sum trick, different bookkeeping. Both *O(n)*.

This pattern generalizes to many variants: count subarrays with
sum divisible by K, subarrays with XOR K, etc. The bookkeeping
adapts; the prefix-sum frame stays the same.
''',
        "summary": "**Pattern**: prefix sum + Counter. For each new prefix p, add count of (p - K) seen earlier.",
    },
    # =================================================================
    # Lecture 3 — Hard (11 problems)
    # =================================================================
    {
        "id": "pascals-triangle",
        "title": "Pascal's Triangle",
        "step_id": 3,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["arrays", "math", "combinatorics"],
        "what_this_teaches": "Three variants: print full triangle, print one row, find a single cell. Each highlights a different efficiency angle.",
        "pattern": "Row[i][j] = Row[i-1][j-1] + Row[i-1][j]; or use C(n, k).",
        "prerequisite_lessons": ["arrays"],
        "prerequisite_problems": ["factorial-of-n"],
        "next_problems": ["count-subsets-sum-k"],
        "resources": [_SHEET, _lc(118, "pascals-triangle"), _lc(119, "pascals-triangle-ii")],
        "understanding": r'''
Pascal's triangle:

```
       1
      1 1
     1 2 1
    1 3 3 1
   1 4 6 4 1
```

Three variants:

**1. Print the whole triangle up to N rows.**

```python
def pascals_full(n):
    triangle = [[1]]
    for i in range(1, n):
        prev = triangle[-1]
        row = [1]
        for j in range(1, i):
            row.append(prev[j - 1] + prev[j])
        row.append(1)
        triangle.append(row)
    return triangle
```

*O(n²)* time, *O(n²)* space.

**2. Print only the K-th row (0-indexed).**

The K-th row is `[C(k, 0), C(k, 1), ..., C(k, k)]` — binomial
coefficients. Use the identity `C(k, j+1) = C(k, j) × (k - j) /
(j + 1)`:

```python
def pascals_row(k):
    row = [1]
    for j in range(k):
        row.append(row[-1] * (k - j) // (j + 1))
    return row
```

*O(k)* time, *O(k)* space.

**3. Find the single value at (row R, column C).**

That's just `C(R, C)`. Compute directly:

```python
def pascals_cell(r, c):
    result = 1
    for j in range(c):
        result = result * (r - j) // (j + 1)
    return result
```

*O(c)* time, *O(1)* space.

The lesson: each variant has its own optimal complexity. Don't
build the whole triangle if you only need one row or one cell.

## Why does Pascal's triangle matter?

It appears in combinatorics (binomial coefficients), DP
recurrences ("count subsets of size K with sum S" mirrors the
triangle's recurrence), and probability (binomial distribution).

Memorize the C(n, k) closed form: `n! / (k! × (n-k)!)`. Many
counting problems reduce to it.
''',
        "summary": "**Pattern**: row[i][j] = row[i-1][j-1] + row[i-1][j]. Or use the C(n, k) formula directly.",
    },
    {
        "id": "majority-element-n3",
        "title": "Majority Element II (> N/3 times)",
        "step_id": 3,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["arrays", "boyer-moore", "voting"],
        "what_this_teaches": "Generalized Boyer-Moore — at most two elements can appear more than N/3 times. Track two candidates with two counters.",
        "pattern": "Two candidates, two counters; both decrement on a 'foreign' value.",
        "prerequisite_lessons": ["arrays", "hashing"],
        "prerequisite_problems": ["majority-element"],
        "next_problems": ["single-number-iii"],
        "resources": [_SHEET, _lc(229, "majority-element-ii")],
        "understanding": r'''
Find all elements appearing more than `n / 3` times. **At most
two** such elements can exist.

Why at most two? If three distinct values each appeared more
than `n / 3` times, their total appearances would exceed `n`
— impossible.

## Generalized Boyer-Moore vote (two candidates)

Maintain two candidates `c1, c2` and two counters `count1,
count2`. For each element:

- If it matches a current candidate, increment that counter.
- Else if a counter is zero, that slot adopts the new element.
- Else decrement both counters (the element "cancels" one vote
  against each candidate).

After one pass, the two candidates are the only possible >N/3
elements. Verify with a second pass.

```python
def majority_n3(arr):
    c1 = c2 = None
    count1 = count2 = 0
    for x in arr:
        if c1 == x:
            count1 += 1
        elif c2 == x:
            count2 += 1
        elif count1 == 0:
            c1, count1 = x, 1
        elif count2 == 0:
            c2, count2 = x, 1
        else:
            count1 -= 1
            count2 -= 1

    threshold = len(arr) // 3
    result = []
    if c1 is not None and arr.count(c1) > threshold:
        result.append(c1)
    if c2 is not None and c2 != c1 and arr.count(c2) > threshold:
        result.append(c2)
    return result
```

*O(n)* time, *O(1)* extra space.

The "match check before counter check" order is critical — if
we checked `count1 == 0` first, a value matching the existing
candidate might accidentally overwrite `c2`'s slot.

## Generalization to > N / (K + 1)

The same algorithm extends to "elements appearing more than
N/(K+1) times" — there can be at most K such elements. Maintain
K candidates and counters. The math is the same.
''',
        "summary": "**Pattern**: two candidates, two counters, mutual cancellation on foreign values.",
    },
    {
        "id": "three-sum",
        "title": "3-Sum",
        "step_id": 3,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["arrays", "two-pointers"],
        "what_this_teaches": "Sort + fix one + two-pointer. The template for all k-sum problems.",
        "pattern": "Sort; for each i, two-pointer search the rest for pair summing to -arr[i].",
        "prerequisite_lessons": ["arrays", "two-pointers"],
        "prerequisite_problems": ["two-sum"],
        "next_problems": ["four-sum"],
        "resources": [_SHEET, _lc(15, "3sum")],
        "understanding": r'''
Find all unique triples `(a, b, c)` in the array with `a + b +
c = 0`.

`[-1, 0, 1, 2, -1, -4]` → `[[-1, -1, 2], [-1, 0, 1]]`.

## Sort + fix-one + two-pointer

```python
def three_sum(arr):
    arr.sort()
    n = len(arr)
    result = []
    for i in range(n - 2):
        if i > 0 and arr[i] == arr[i - 1]:
            continue                     # skip duplicate first elements
        if arr[i] > 0:
            break                        # sorted: no more triples sum to 0
        left, right = i + 1, n - 1
        while left < right:
            s = arr[i] + arr[left] + arr[right]
            if s == 0:
                result.append([arr[i], arr[left], arr[right]])
                left += 1
                right -= 1
                while left < right and arr[left] == arr[left - 1]:
                    left += 1
                while left < right and arr[right] == arr[right + 1]:
                    right -= 1
            elif s < 0:
                left += 1
            else:
                right -= 1
    return result
```

*O(n²)* time after the *O(n log n)* sort.

The fiddly part is **duplicate skipping**:

- Outer `i`: skip if `arr[i] == arr[i - 1]` (already explored).
- Inner pointers: after recording a match, skip while
  `arr[left] == arr[left - 1]` and `arr[right] == arr[right +
  1]`.

Without the dedup, the result will contain duplicates.

## Why sort first?

Sorting enables the two-pointer search (which needs monotonicity).
It also makes duplicate skipping easy — duplicates land adjacent.

This template — **sort, fix some, two-pointer the rest** —
extends to 4-Sum (fix two, two-pointer the rest) and the general
K-Sum problem.
''',
        "summary": "**Pattern**: sort + fix one + two-pointer + skip duplicates.",
    },
    {
        "id": "four-sum",
        "title": "4-Sum",
        "step_id": 3,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["arrays", "two-pointers"],
        "what_this_teaches": "K-Sum recurrence: 4-Sum = fix one, then 3-Sum. Same template, one nesting deeper.",
        "pattern": "Sort; double fix + two-pointer for the remaining pair.",
        "prerequisite_lessons": ["arrays", "two-pointers"],
        "prerequisite_problems": ["three-sum"],
        "next_problems": [],
        "resources": [_SHEET, _lc(18, "4sum")],
        "understanding": r'''
Find all unique quadruples summing to a target value.

The pattern: nest another loop on top of the 3-Sum solution. For
each `i`, run 3-Sum on `arr[i + 1:]` with target `K - arr[i]`.

```python
def four_sum(arr, target):
    arr.sort()
    n = len(arr)
    result = []
    for i in range(n - 3):
        if i > 0 and arr[i] == arr[i - 1]:
            continue
        for j in range(i + 1, n - 2):
            if j > i + 1 and arr[j] == arr[j - 1]:
                continue
            left, right = j + 1, n - 1
            need = target - arr[i] - arr[j]
            while left < right:
                s = arr[left] + arr[right]
                if s == need:
                    result.append([arr[i], arr[j], arr[left], arr[right]])
                    left += 1
                    right -= 1
                    while left < right and arr[left] == arr[left - 1]:
                        left += 1
                    while left < right and arr[right] == arr[right + 1]:
                        right -= 1
                elif s < need:
                    left += 1
                else:
                    right -= 1
    return result
```

*O(n³)* time.

## Generalization: K-Sum

The recursive K-Sum:

- Base case K = 2: two-pointer search on a sorted subarray.
- Recursive case: fix one element; recurse on (K - 1)-Sum with
  target reduced.

```python
def k_sum(arr, target, k):
    arr.sort()
    def helper(start, k, target):
        if k == 2:
            return two_sum_sorted(arr, start, target)
        result = []
        for i in range(start, len(arr) - k + 1):
            if i > start and arr[i] == arr[i - 1]:
                continue
            for tail in helper(i + 1, k - 1, target - arr[i]):
                result.append([arr[i]] + tail)
        return result
    return helper(0, k, target)
```

Time: *O(n^(K - 1))*. K-Sum is essentially a recursion plus the
two-pointer base case.
''',
        "summary": "**Pattern**: K-Sum = recursive descent to 2-Sum two-pointer.",
    },
    {
        "id": "longest-subarray-zero-sum",
        "title": "Longest Subarray with Sum Zero",
        "step_id": 3,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["arrays", "prefix-sum", "hashing"],
        "what_this_teaches": "Specialization of 'longest subarray with sum K' to K = 0. Same prefix-sum + hash pattern.",
        "pattern": "First occurrence of each prefix sum; on revisit, length = current - first.",
        "prerequisite_lessons": ["arrays", "hashing"],
        "prerequisite_problems": ["longest-subarray-with-sum-k"],
        "next_problems": ["subarrays-with-xor-k"],
        "resources": [_SHEET],
        "understanding": r'''
Find the length of the longest contiguous subarray whose sum is
zero.

`[1, -1, 3, -3, 5]` → 4 (the subarray `[1, -1, 3, -3]`).

This is `longest-subarray-with-sum-K` with K = 0. The prefix-
sum + hash pattern works directly.

When does a subarray sum to zero? When two prefix sums are
**equal** — `prefix[j + 1] = prefix[i]`, meaning the elements
between contribute nothing.

So: maintain a dict of first-occurrence index for each prefix
sum. When a prefix repeats, the subarray between its first
occurrence and the current position sums to zero.

```python
def longest_zero_sum_subarray(arr):
    first_index = {0: -1}             # empty prefix at index -1
    prefix = 0
    best = 0
    for i, x in enumerate(arr):
        prefix += x
        if prefix in first_index:
            best = max(best, i - first_index[prefix])
        else:
            first_index[prefix] = i
    return best
```

*O(n)* time, *O(n)* space.

The `{0: -1}` seed handles subarrays starting at index 0
(prefix[0] = 0, which is "before" any element).

The `else` clause ensures we record only the **first** occurrence
of each prefix sum, so the resulting subarray is as long as
possible.
''',
        "summary": "**Pattern**: prefix sum repetition = zero-sum subarray. Track first occurrences.",
    },
    {
        "id": "subarrays-with-xor-k",
        "title": "Count Subarrays with XOR K",
        "step_id": 3,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["arrays", "xor", "hashing"],
        "what_this_teaches": "Prefix-XOR analog of prefix-sum: subarray XOR is the XOR of two prefix XORs.",
        "pattern": "Counter of prefix XORs; for each new prefix p, add count of (p XOR K).",
        "prerequisite_lessons": ["arrays", "hashing"],
        "prerequisite_problems": ["subarrays-with-sum-k", "single-number"],
        "next_problems": [],
        "resources": [_SHEET],
        "understanding": r'''
Count the number of contiguous subarrays whose XOR is K.

XOR has the same "prefix" property as sum:

> If P_i = XOR of arr[0..i-1], then XOR of arr[i..j] = P_j+1 XOR P_i.

Want this to equal K. So P_i = P_j+1 XOR K.

For each new prefix XOR `p`, we want to count earlier prefixes
equal to `p XOR K`.

```python
from collections import Counter

def count_xor_k(arr, k):
    prefix_count = Counter({0: 1})       # empty prefix XOR is 0
    prefix = 0
    count = 0
    for x in arr:
        prefix ^= x
        count += prefix_count.get(prefix ^ k, 0)
        prefix_count[prefix] += 1
    return count
```

*O(n)* time, *O(n)* space.

Same shape as `subarrays-with-sum-k`; we swapped `+` for `^` and
the algebraic structure carries over because XOR is its own
inverse (`a XOR a = 0`).

This is the magic of prefix-X techniques: they work for any
operation with an inverse (sum has subtraction; XOR is self-
inverse). For operations without inverses (max, min, product
with zeros), prefix decomposition does not apply directly.
''',
        "summary": "**Pattern**: prefix-XOR + Counter. For each new prefix p, add count of (p XOR K).",
    },
    {
        "id": "merge-two-sorted-no-extra-space",
        "title": "Merge Two Sorted Arrays Without Extra Space",
        "step_id": 3,
        "lecture_id": 3,
        "difficulty": "hard",
        "tags": ["arrays", "merge", "two-pointers"],
        "what_this_teaches": "Two clever in-place merge tricks: gap-method and swap-from-the-ends. Both *O((n+m) log(n+m))* but constant extra memory.",
        "pattern": "Swap elements between arr1 and arr2 where order is violated; then sort each.",
        "prerequisite_lessons": ["arrays", "sorting"],
        "prerequisite_problems": ["merge-sort"],
        "next_problems": [],
        "resources": [_SHEET, _lc(88, "merge-sorted-array")],
        "understanding": r'''
Given two sorted arrays `arr1` and `arr2`, merge them so the
**smallest** elements end up in `arr1` and the **largest** end
up in `arr2`, both still sorted.

`[1, 4, 7]` and `[2, 5, 6]` → `[1, 2, 4]` and `[5, 6, 7]`.

## Approach 1: swap-then-sort

For each pair of positions `(i, j)` with `arr1[-1 - i] >
arr2[j]`, swap them. After the swap loop, sort each array.

```python
def merge_no_extra(arr1, arr2):
    i, j = len(arr1) - 1, 0
    while i >= 0 and j < len(arr2):
        if arr1[i] > arr2[j]:
            arr1[i], arr2[j] = arr2[j], arr1[i]
            i -= 1
            j += 1
        else:
            break
    arr1.sort()
    arr2.sort()
```

*O((n + m) log(n + m))* due to the sorts. *O(1)* extra space.

## Approach 2: gap method (Shellsort-inspired)

Use a "gap" that starts at `ceil((n + m) / 2)` and halves each
iteration. Compare element pairs that are `gap` apart (across
both arrays as if concatenated); swap if out of order.

```python
def merge_gap(arr1, arr2):
    n, m = len(arr1), len(arr2)
    total = n + m
    def get(idx):
        return arr1[idx] if idx < n else arr2[idx - n]
    def set_(idx, val):
        if idx < n:
            arr1[idx] = val
        else:
            arr2[idx - n] = val
    gap = (total + 1) // 2
    while gap > 0:
        for i in range(total - gap):
            j = i + gap
            if get(i) > get(j):
                a, b = get(i), get(j)
                set_(i, b)
                set_(j, a)
        gap = 0 if gap == 1 else (gap + 1) // 2
```

*O((n + m) log(n + m))* time, *O(1)* space.

Both approaches achieve constant extra memory. Approach 1 is
simpler to write; approach 2 is more elegant once you see it.

For the LeetCode 88 variant (one array has extra slots), the
trick is to merge from the **back**, placing the larger element
first. That avoids overwriting elements you still need to read.
''',
        "summary": "**Pattern**: swap-then-sort or gap method for in-place merge. Both O((n+m) log(n+m)).",
    },
    {
        "id": "repeating-and-missing",
        "title": "Find the Repeating and Missing Number",
        "step_id": 3,
        "lecture_id": 3,
        "difficulty": "hard",
        "tags": ["arrays", "math", "xor"],
        "what_this_teaches": "Two equations recover two unknowns. Sum-difference and sum-of-squares (or sum and XOR) are the canonical pair.",
        "pattern": "Pair (sum, sum-of-squares) or (XOR, bit-partition) to solve for both unknowns.",
        "prerequisite_lessons": ["arrays", "hashing"],
        "prerequisite_problems": ["missing-number", "single-number"],
        "next_problems": ["count-inversions"],
        "resources": [_SHEET],
        "understanding": r'''
An array of size `n` contains values `1..n` with exactly one
value repeated and one missing. Find both.

`[1, 2, 2, 4]` (n = 4): repeating = 2, missing = 3.

## Hash-set approach

Walk the array; track seen values. Detect the repeat. Then scan
1..n for the missing.

*O(n)* time, *O(n)* space.

## Math approach (sum + sum-of-squares)

Let `r` = repeating, `m` = missing.

- `actual_sum - expected_sum = r - m`.
- `actual_sum_squares - expected_sum_squares = r² - m²
  = (r - m)(r + m)`.

So `r + m = (squares_diff) / (sum_diff)`, and `r - m =
sum_diff`. Solve the 2x2 system.

```python
def repeating_and_missing(arr):
    n = len(arr)
    expected_sum = n * (n + 1) // 2
    expected_sq = n * (n + 1) * (2 * n + 1) // 6
    actual_sum = sum(arr)
    actual_sq = sum(x * x for x in arr)
    sum_diff = actual_sum - expected_sum            # r - m
    sq_diff = actual_sq - expected_sq               # (r - m)(r + m)
    plus = sq_diff // sum_diff                      # r + m
    r = (plus + sum_diff) // 2
    m = (plus - sum_diff) // 2
    return r, m
```

*O(n)* time, *O(1)* space.

## XOR approach

XOR all of `1..n` with all of `arr`. The result is `r XOR m`.
Pick any bit where this result is 1; that bit differs between
`r` and `m`. Partition all numbers (input and 1..n) by this bit;
XOR each partition. One partition contains `r`, the other
contains `m`.

This is the same trick used in "Single Number III." Beautiful
but more code to write.

Choose based on the constraints:
- Memory tight, simplicity okay: math approach.
- Avoiding multiplication overflow in typed languages: XOR
  approach.
- Quick and dirty: hash set.
''',
        "summary": "**Pattern**: sum + sum-of-squares = two equations for two unknowns. Or use XOR + bit partition.",
    },
    {
        "id": "count-inversions",
        "title": "Count Inversions in an Array",
        "step_id": 3,
        "lecture_id": 3,
        "difficulty": "hard",
        "tags": ["arrays", "merge-sort", "divide-and-conquer"],
        "what_this_teaches": "Merge sort modified to count inversions during the merge step. The classic *O(n log n)* algorithm for an *O(n²)* counting problem.",
        "pattern": "Modify merge: when picking from the right list, count remaining left elements.",
        "prerequisite_lessons": ["sorting"],
        "prerequisite_problems": ["merge-sort", "bubble-sort"],
        "next_problems": ["reverse-pairs"],
        "resources": [_SHEET, _lc(493, "reverse-pairs")],
        "understanding": r'''
An **inversion** is a pair `(i, j)` with `i < j` and `arr[i] >
arr[j]`. Count the total inversions.

`[2, 4, 1, 3, 5]` has 3 inversions: (2, 1), (4, 1), (4, 3).

## Brute force

Two loops: *O(n²)*. For each `i`, count how many `j > i` have
`arr[j] < arr[i]`.

## Merge-sort modified — *O(n log n)*

During the merge step, when picking an element from the **right**
half, all remaining elements in the **left** half form
inversions with it (because the left half is sorted and they
are all smaller than the right element... wait, no — we are
comparing values, not indices).

Actually: when merging left[i] and right[j], if `left[i] >
right[j]`, then right[j] forms an inversion with **all
remaining** left[i..end]. Because the left half is sorted, all
those are also `> right[j]`.

```python
def count_inversions(arr):
    def merge_count(a):
        if len(a) <= 1:
            return a, 0
        mid = len(a) // 2
        left, left_inv = merge_count(a[:mid])
        right, right_inv = merge_count(a[mid:])
        merged = []
        i = j = 0
        cross_inv = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                cross_inv += len(left) - i       # count!
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, left_inv + right_inv + cross_inv

    _, count = merge_count(arr)
    return count
```

*O(n log n)* time, *O(n)* space.

The key line: `cross_inv += len(left) - i`. When right[j] is the
smaller one, every remaining left element forms an inversion
with right[j].

This is one of the prettiest applications of merge sort beyond
sorting itself. The merge step is doing double duty — combining
sorted halves AND counting inversions between them.
''',
        "summary": "**Pattern**: merge sort + 'count remaining left' during merge.",
    },
    {
        "id": "reverse-pairs",
        "title": "Reverse Pairs",
        "step_id": 3,
        "lecture_id": 3,
        "difficulty": "hard",
        "tags": ["arrays", "merge-sort", "divide-and-conquer"],
        "what_this_teaches": "Generalized inversion counting: pairs where `arr[i] > 2 * arr[j]` and `i < j`. Same merge-sort approach, separate counting pass.",
        "pattern": "Merge sort; count cross-pairs in a separate pass before the merge.",
        "prerequisite_lessons": ["sorting"],
        "prerequisite_problems": ["count-inversions"],
        "next_problems": [],
        "resources": [_SHEET, _lc(493, "reverse-pairs")],
        "understanding": r'''
Count pairs `(i, j)` with `i < j` and `arr[i] > 2 * arr[j]`.

This is "count inversions" with a twist — the comparison is
`arr[i] > 2 * arr[j]` instead of `arr[i] > arr[j]`.

The twist means we can't count during merge (because the merge
uses the original `<=` comparison). Instead, do the counting
in a **separate pass before** the merge.

```python
def reverse_pairs(arr):
    def merge_count(a):
        if len(a) <= 1:
            return a, 0
        mid = len(a) // 2
        left, lc = merge_count(a[:mid])
        right, rc = merge_count(a[mid:])
        # Count cross pairs BEFORE merging
        count = lc + rc
        j = 0
        for x in left:
            while j < len(right) and x > 2 * right[j]:
                j += 1
            count += j
        # Now merge normally
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, count

    _, c = merge_count(arr)
    return c
```

*O(n log n)* time, *O(n)* space.

The counting pass is itself *O(n)* per level — both `left` and
`right` are sorted, so a single linear sweep counts all valid
pairs. The merge happens afterward as usual.

This problem cements the pattern: **modify merge sort to count
something during or near the merge step**. The same template
works for "number of pairs where ___" problems involving
ordered indices.
''',
        "summary": "**Pattern**: merge sort + linear cross-count before merge.",
    },
    {
        "id": "max-product-subarray",
        "title": "Maximum Product Subarray",
        "step_id": 3,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["arrays", "dp"],
        "what_this_teaches": "Kadane-like DP, but track both max and min because a negative × negative could be the new max.",
        "pattern": "Two running scalars: max_ending_here, min_ending_here. Swap when multiplying a negative.",
        "prerequisite_lessons": ["arrays", "dp"],
        "prerequisite_problems": ["kadane-algorithm"],
        "next_problems": [],
        "resources": [_SHEET, _lc(152, "maximum-product-subarray")],
        "understanding": r'''
Find the maximum product of any contiguous subarray.

`[2, 3, -2, 4]` → 6 (`[2, 3]`).
`[-2, 0, -1]` → 0 (the standalone 0).

## Why Kadane doesn't work directly

Kadane tracks `best_ending_here = max(arr[i], best_ending_here +
arr[i])`. But with **multiplication**, a current "minimum"
(very negative) can become the new "maximum" if multiplied by
a negative number.

So we must track **both** the running max and the running min.

```python
def max_product(arr):
    if not arr:
        return 0
    max_end = min_end = best = arr[0]
    for i in range(1, len(arr)):
        x = arr[i]
        # Multiplying by a negative swaps roles
        if x < 0:
            max_end, min_end = min_end, max_end
        max_end = max(x, max_end * x)
        min_end = min(x, min_end * x)
        best = max(best, max_end)
    return best
```

*O(n)* time, *O(1)* space.

The trick: when `x < 0`, the new max comes from `min × x` (very
negative × negative = large positive). The swap accomplishes
this elegantly.

## Why does it work?

At each position, the maximum-product subarray ending here is
either:
- Just `arr[i]` (start fresh).
- `max_end_previous × arr[i]` (extend).
- `min_end_previous × arr[i]` (extend, with sign flip).

The Kadane recurrence is *O(1)* per step. Same as the sum
version.

This is one of the prettiest variations on Kadane's. Negatives
make the problem subtly harder; tracking the min is the cure.
''',
        "summary": "**Pattern**: Kadane + track both max and min. Swap on negative.",
    },
]
