"""Binary search — the algorithmic answer to 'half it'."""

LESSON = {
    "id": "searching",
    "title": "Searching — Linear, Binary, and Searching the Answer",
    "tags": ["binary-search", "searching", "fundamentals"],
    "summary": (
        "A full beginner chapter. How linear search becomes binary "
        "search when the data is sorted, the half-open vs. closed "
        "loop conventions, the 'binary search on the answer' lifting "
        "move, and the mental discipline of finding monotonic "
        "decision rules where they hide."
    ),
    "body": r'''
## 0. The promise

Binary search is the single most useful *O(log n)* pattern in
DSA. Master it and a third of medium-hard array problems
collapse into clean two-pointer halving algorithms.

The hard part of binary search is not the idea — "halve the
search range each iteration" is obvious — but **the bookkeeping**.
Off-by-one bugs flourish in binary search like nowhere else. The
cure is to pick one boundary convention and stick to it religiously.

This chapter teaches the conventions, the lifting move ("binary
search on the answer"), and a checklist for spotting when binary
search applies. By the end, you should be able to look at any
"minimum / maximum X such that ___" problem and reach for binary
search without thinking.

## 1. Linear search — the honest baseline

You have an array; you want to know if value `x` is in it. With
no preparation:

```python
def linear_search(arr, target):
    for i, v in enumerate(arr):
        if v == target:
            return i
    return -1
```

*O(n)*. Honest. Works on any array, sorted or not.

Do not be embarrassed by linear search. For tiny arrays (say,
fewer than 50 elements), constants matter more than asymptotics
— linear search can be faster than the binary-search overhead.
Use it when applicable.

## 2. Binary search — what sortedness buys you

The moment your array is sorted, you have a superpower. The same
"look at the middle, decide which half" reasoning you would use
for a paper dictionary applies.

Each look gives you a one-bit answer — "is the target before or
after this element?" — and that bit eliminates half the
remaining candidates. So instead of *n* comparisons, you need
about `log₂ n`. For one million elements, that is roughly twenty
comparisons. For a billion, thirty.

```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

Three invariants make binary search correct:

1. **The data is sorted** (or at least monotonic in some sense).
2. **The answer must lie in the current window** `[lo, hi]`. We
   never move the boundary toward the answer; we only move it
   *away*.
3. **The window strictly shrinks each iteration.** Without this,
   the loop runs forever.

If any of those three is missing or wrong, binary search becomes
a parade of off-by-one bugs.

## 3. The two boundary conventions

This is where most binary search bugs live. There are two main
conventions for the window:

**Closed interval `[lo, hi]`**: both endpoints are inclusive.
The window is non-empty when `lo <= hi`. When we discard
`arr[mid]`, the new bound excludes it (`hi = mid - 1` or `lo =
mid + 1`).

**Half-open interval `[lo, hi)`**: `lo` inclusive, `hi`
exclusive. The window is non-empty when `lo < hi`. When we
include `mid` as a candidate, the new bound keeps it (`hi =
mid`). When we exclude it, the new bound moves past it (`lo =
mid + 1`).

Both work. Mixing them does not. **Pick one, write the invariant
down, and stay consistent**.

For "find an exact match" the closed-interval style is most
common. For "find the first index satisfying property P" — the
**lower bound** style — the half-open is cleaner.

```python
def lower_bound(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

`lower_bound` returns the first index whose value is `>= target`,
or `len(arr)` if no such index exists. Powerful enough to
implement everything else.

## 4. The lower / upper bound family

Once you have lower bound, almost every sorted-array query is one
line away:

- **First occurrence of `x`**: `lower_bound(x)`, then check `arr[
  result] == x`.
- **Last occurrence of `x`**: `upper_bound(x) - 1`, then check.
- **Number of `x` in array**: `upper_bound(x) - lower_bound(x)`.
- **Number of values `< x`**: `lower_bound(x)`.
- **Number of values in range `[L, R]`**: `upper_bound(R) -
  lower_bound(L)`.
- **Where to insert `x` to keep sorted order**: `lower_bound(x)`
  (before existing duplicates) or `upper_bound(x)` (after).

Python ships these as `bisect.bisect_left` (lower bound) and
`bisect.bisect_right` (upper bound). In production code, use
them. In interview practice, write them from memory.

## 5. The leap: binary search on the answer

This is the lifting move that turns binary search from "search a
sorted array" into "search any monotonic decision space." Once
you see this, an enormous family of medium / hard problems
becomes mechanical.

The shape:

- The problem asks for the **smallest** (or **largest**) integer
  value satisfying some property.
- The candidate values form a known range.
- The property is **monotonic**: if it holds for some value, it
  holds for every value above (or below).

When you see that shape, you binary search the **candidate
values** instead of any array.

The recipe:

1. **Identify the candidate range** `[lo, hi]` — the smallest and
   largest values the answer can take.
2. **Write a feasibility checker** `is_feasible(x)` that returns
   True / False in linear (or otherwise polynomial) time.
3. **Verify monotonicity**: if `is_feasible(x)` is True, then
   `is_feasible(x + 1)` is also True (or some equivalent
   ordering).
4. **Binary search the range** using the checker.

Worked example: Koko Eating Bananas. Find the minimum integer
eating speed such that Koko finishes all piles within `h` hours.

- Candidate range: `[1, max(piles)]`.
- `is_feasible(k)`: simulate eating at speed `k`, return True if
  total time `<= h`. *O(n)*.
- Monotonic: if she can finish at speed `k`, she can finish at
  any speed `> k`.
- Binary search: find smallest `k` with `is_feasible(k) == True`.

Total time: *O(n × log(max(piles)))*.

This recipe applies to dozens of problems on this sheet: minimum
days to make M bouquets, smallest divisor with threshold,
capacity to ship packages, k-th missing positive, aggressive
cows, book allocation, painter's partition, minimize max
distance. They all follow the same five-step structure with
different checkers.

## 6. When binary search does NOT work

Binary search needs a **monotonic decision rule**. If the
decision flickers between true and false in some non-monotonic
pattern, you lose the ability to halve the search.

For example: "find any peak element in an array." This is *not*
sorted, but binary search still works because the *slope* is
monotonic enough (going uphill at `mid` implies a peak is to the
right). But "find the maximum subarray sum" is not amenable to
binary search; longer is not always better.

The skill: ask yourself, *"is there any property that, once true
at some value, stays true for everything above (or below)?"*. If
yes, binary search applies even if the input array is not sorted
in the usual sense.

If no, fall back to sorting + sweeping, hashing, or DP.

## 7. The common off-by-one bugs

These are the bugs that have plagued binary search for fifty
years. Memorize each and the fix.

**Bug 1: infinite loop on a one-element window.** Happens when
`lo == hi` and the bound update sets `lo = mid` instead of `lo
= mid + 1` (or symmetrically for `hi`). Cure: make sure the
window strictly shrinks each iteration.

**Bug 2: missing the answer at the boundary.** Happens when you
write `while lo < hi` with a closed-interval window, or `while
lo <= hi` with a half-open window. Cure: pick one convention and
write down the invariant.

**Bug 3: overflow on `(lo + hi) // 2`.** In Python this is fine.
In C++ or Java with 32-bit ints, `lo + hi` can overflow. Cure:
write `lo + (hi - lo) // 2` instead.

**Bug 4: returning the wrong index after the loop.** When the
loop exits with `lo == hi`, that single value is usually the
answer for lower-bound style. For closed-interval style, the
loop exits with `lo > hi`, and "not found" returns -1. Know
which style you are in.

**Bug 5: using the wrong comparison.** For lower bound: `if arr[
mid] < target: lo = mid + 1, else: hi = mid`. For upper bound:
swap `<` to `<=`. Get the comparison off by one and you find
the wrong boundary.

## 8. A small habit: write the invariant first

When you sit down to a binary search problem:

1. **Name the question**: "what am I looking for?" (e.g., "the
   smallest index where `arr[i] >= target`").
2. **Name the window's meaning**: "the answer, if it exists,
   lies in `[lo, hi]` (or `[lo, hi)`)".
3. **Write the invariant**: "at all times, `arr[lo..]` may
   contain the answer; `arr[..lo)` does not."
4. **Pick the boundary convention** and stick to it.
5. **Write the loop body** so that each branch strictly shrinks
   the window in a way that preserves the invariant.

This sounds bureaucratic. It saves hours of debugging. Once you
have done it five times it becomes reflexive.

## 9. The Python `bisect` module

Python ships everyday binary search as the `bisect` module:

```python
import bisect

bisect.bisect_left(arr, x)    # lower bound
bisect.bisect_right(arr, x)   # upper bound
bisect.insort(arr, x)         # insert in sorted order, O(n) for the shift
```

For interview practice, write the algorithm by hand. For
production code, use the module — it is well-tested and
optimized.

A subtle point about `bisect.insort`: the **search** is *O(log
n)*, but the **insertion** is *O(n)* because of the shift. For
truly fast sorted insertion, you need a tree or skip-list
structure (rare in Python interviews).

## 10. End-of-chapter exercise

Solve these five problems with binary search as your central tool.

1. **Search insert position.** Standard lower-bound application.
   LeetCode 35.
2. **Find first and last position of element in sorted array.**
   Two binary searches. LeetCode 34.
3. **Search in rotated sorted array.** Binary search with the
   "one half is sorted" twist. LeetCode 33.
4. **Koko Eating Bananas.** Binary search on the answer.
   LeetCode 875.
5. **Median of two sorted arrays.** Hard binary search on the
   partition index. LeetCode 4.

Do all five. By the end of (5), the lifting move "binary search
on the answer" should feel familiar even on hard problems.

## 11. Where to go next

- **Step 4 Lecture 1**: BS on 1D arrays — first / last
  occurrence, rotated arrays, peak elements.
- **Step 4 Lecture 2**: BS on answers — Koko, aggressive cows,
  book allocation, painter's partition, median of two sorted.
- **Step 4 Lecture 3**: BS on 2D arrays — search 2D matrix.
- **Step 14**: BSTs, which are sorted trees admitting their own
  binary search.

Binary search is *the* lever that turns "linear scan" into
"logarithmic look-up." Spend the practice time on the
boundary-convention discipline and the "BS on answer" lifting
move. Both pay dividends for years.
''',
}
