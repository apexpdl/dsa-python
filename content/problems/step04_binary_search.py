"""Step 4 — Binary Search.

Binary search is far more than "find a value in a sorted array". The
real lesson of this step is "binary search on the answer", which
turns many medium/hard problems into one-pass checks.
"""
from __future__ import annotations

PROBLEMS: list[dict] = [
    {
        "id": "binary-search",
        "title": "Binary Search in a Sorted Array",
        "step_id": 4,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["binary-search", "fundamentals"],
        "what_this_teaches": (
            "The single most useful *O(log n)* pattern in DSA. The "
            "real lesson is not the algorithm but the **invariant** — "
            "'if the target exists, it lies inside [lo, hi]' — and "
            "the discipline of strictly shrinking the window each "
            "iteration."
        ),
        "pattern": "Two pointers lo, hi; halve the window each iteration.",
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["largest-element"],
        "next_problems": [
            "lower-bound",
            "upper-bound",
            "search-insert-position",
            "find-peak-element",
            "search-rotated-i",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 4 (BS on 1D Arrays)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 704 — Binary Search",
                "url": "https://leetcode.com/problems/binary-search/",
            },
            {
                "label": "Python docs — bisect module",
                "url": "https://docs.python.org/3/library/bisect.html",
            },
        ],
        "understanding": r'''
We have a sorted array `arr` and a target value `x`. Return the
index of `x` if it exists, otherwise `-1`. The array is sorted in
ascending order.

This is the prototype problem for binary search. Master it cold,
then watch as countless harder problems decompose into variations
of it.
''',
        "brute_force": {
            "explanation": r'''
Walk left to right comparing each element. *O(n)*. There is no
shame in linear search; for tiny arrays it is faster (constants
matter). But for large `n` it is dramatically beaten by binary
search.
''',
            "code": r'''def linear_search(arr: list[int], x: int) -> int:
    for i, v in enumerate(arr):
        if v == x:
            return i
    return -1
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "thought_process": r'''
Imagine a paper phone book — the kind that does not exist anymore
because phones do this for us. To find "Williams", you do not start
at "Aaron" and read every name. You open somewhere in the middle,
check which name you landed on, and then jump halfway through
whichever half contains "Williams". Each jump halves your search
range.

That is binary search. It exists because **sortedness gives you a
one-bit answer for free**: "is the target before this element or
after?". With that one bit, you eliminate half the candidates per
step.

To implement: keep two indices, `lo` and `hi`, bounding the
unsearched region. Inspect the midpoint `mid = (lo + hi) // 2`. If
`arr[mid] == x`, done. If `arr[mid] < x`, the target lies in the
right half, so `lo = mid + 1`. Otherwise `hi = mid - 1`. Repeat
until `lo > hi`.

Three things to get right:

1. **Window definition.** Are `lo` and `hi` both inclusive (closed
   interval), or is `hi` one past the end (half-open)? Both work;
   pick one and stick with it.
2. **Termination.** The window must shrink by at least one per
   iteration, or you loop forever.
3. **Off-by-one.** Decide whether `mid + 1` or `mid` is the correct
   new bound. Get this wrong and you either skip the answer or spin
   in place.
''',
        "optimized": {
            "explanation": r'''
Two pointers `lo` and `hi`, both inclusive. Halve the search range
each iteration.
''',
            "code": r'''def binary_search(arr: list[int], x: int) -> int:
    # Closed-interval style: lo and hi are both valid indices.
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        # Midpoint. In Python this is exact; in C++/Java the
        # equivalent is `lo + (hi - lo) // 2` to avoid overflow.
        mid = (lo + hi) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] < x:
            # Target lies to the right of mid.
            lo = mid + 1
        else:
            # Target lies to the left of mid.
            hi = mid - 1
    return -1
''',
            "complexity": (
                "**Time**: *O(log n)*. Each iteration halves the "
                "search range. **Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
Binary search's correctness rests on the **invariant**: at every
iteration, if `x` is in the array, it lies in `arr[lo..hi]`. The
invariant is preserved because we move the bound only away from
positions that cannot contain `x` (we move past elements smaller
than `x` by setting `lo = mid + 1`).

The depth of the recursion (or the number of iterations) is at
most `floor(log2(n)) + 1`, because each step halves the range, and
the range can halve at most that many times before it becomes
empty. That is where the *O(log n)* comes from.

If your input is **already sorted**, binary search is one of the
fastest things you can do — it really is `log2(n)` operations. For
`n = 1,000,000,000`, that is about 30 operations. Faster than the
human eye can register.

The pattern generalizes wildly:

- **Lower bound** (first index with value ≥ x).
- **Upper bound** (first index with value > x).
- **Search in a rotated sorted array** — adapt the comparison to
  detect which half is "in order".
- **Find peak element** — adapt the comparison to detect which
  side is uphill.
- **Binary search on the answer** — search over possible answers
  rather than array positions.

Each is binary search with a slightly different comparison rule.
''',
        "confusion_notes": [
            {
                "question": "Why `lo <= hi` and not `lo < hi`?",
                "answer": r'''
Because both `lo` and `hi` are **inclusive** indices in this
formulation, and the search range is the closed interval `[lo,
hi]`. The range is non-empty exactly when `lo <= hi`. When `lo`
exceeds `hi`, the range is empty and we exit.

If we used `lo < hi`, the loop would exit one iteration too
early — the single-element case `lo == hi` would never be
checked. For an input where the target happens to live at the
last remaining position, the algorithm would miss it and
incorrectly return `-1`.

There is an alternative convention, the **half-open** style,
where `hi` is one-past-the-end and the condition is `lo < hi`.
That style is equally valid; it just shifts every comparison
by one. The Python `bisect` module uses the half-open style.

The single most important rule: **decide once which convention
you are using, and stay consistent**. Mixing styles inside one
function is the most common source of off-by-one bugs in binary
search. Write the invariant down on paper if you are unsure.
''',
            },
            {
                "question": "Why `mid + 1` and `mid - 1` instead of just `mid`?",
                "answer": r'''
Because we have already checked `arr[mid]` in this iteration. It
is *not* the target (otherwise we would have returned). So we
should exclude `mid` from the next search window — including it
would risk infinite recursion.

Walk through it. Suppose `arr = [1, 3, 5]`, target = 2. First
iteration: `lo = 0, hi = 2, mid = 1, arr[mid] = 3`. Since `3 >
2`, we want to look at the left half. If we wrote `hi = mid`,
the next state would be `lo = 0, hi = 1`. We compute `mid = 0`,
check `arr[0] = 1 < 2`, set `lo = mid + 1 = 1`. Next state:
`lo = 1, hi = 1`. We compute `mid = 1`, check `arr[1] = 3 > 2`,
set `hi = mid = 1`. We are now in an infinite loop — `lo` and
`hi` never separate.

The fix is `hi = mid - 1`. After ruling out `mid`, the new
window strictly excludes it. Now the window shrinks by at least
one each iteration, guaranteeing termination.

Same reasoning applies to `lo = mid + 1` on the other branch.

The invariant: **the search window must strictly shrink in every
iteration**. If it does not, either the window is degenerate or
your bound update is wrong.
''',
            },
            {
                "question": "Why compute `mid = (lo + hi) // 2` instead of `mid = lo + (hi - lo) // 2`?",
                "answer": r'''
The two expressions are mathematically equivalent. Both compute
the midpoint of the window. So why the longer form sometimes?

**Overflow safety in fixed-width integers.** In C++ or Java
with 32-bit signed integers, `lo + hi` can overflow if both are
huge. For example, if `lo = 1,000,000,000` and `hi =
1,500,000,000`, then `lo + hi` is about `2.5 × 10⁹`, exceeding
the signed-int max of `~2.1 × 10⁹`. The overflow corrupts the
midpoint calculation.

The form `lo + (hi - lo) // 2` is overflow-safe because `hi -
lo` is always non-negative and bounded by the array size, and
adding half of it to `lo` stays within range.

**In Python**, integers are arbitrary precision, so neither form
overflows. Both work identically. Use `(lo + hi) // 2` for
readability if Python is the only target. Use `lo + (hi - lo) //
2` if you might port to a typed language, or if you want to
build the safer habit.

For interview purposes, mention the overflow concern explicitly:
"This is fine in Python, but in C++ I would write `lo + (hi -
lo) / 2` to avoid potential overflow." That signals to the
interviewer that you understand the underlying machine model.
''',
            },
            {
                "question": "What if the target appears multiple times in the array?",
                "answer": r'''
Plain binary search returns **some** valid index of the target,
not a specific one. Which exact occurrence you land on depends
on the array's structure and the comparison order.

If you specifically want the **first** occurrence (the leftmost
index of the target), use **lower bound**:

```python
def lower_bound(arr, x):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

After this returns, check `arr[lo] == x` to confirm presence. If
it matches, `lo` is the index of the leftmost occurrence.

If you want the **last** occurrence, use **upper bound** and
subtract 1: `upper_bound(arr, x) - 1`. Upper bound returns the
first index with value strictly greater than `x`, so one less
is the last index equal to `x`.

The **count of occurrences** of `x` is `upper_bound(x) -
lower_bound(x)`. Two binary searches, each *O(log n)*, total
*O(log n)*.

So plain binary search is good for "is it there?". Lower / upper
bound is what you reach for when you need a specific occurrence
or a count. We meet them in the next problem.
''',
            },
        ],
        "summary": r'''
**Pattern**: halve the search range each iteration.

**Lesson**: binary search is `O(log n)` because each step gives a
one-bit answer for free. The invariant "if x exists it lies in
[lo, hi]" is the proof of correctness.

**Recognize next time**: any sorted (or monotonic) data with a
yes/no query. Even non-arrays — see "binary search on the answer".
''',
    },
    {
        "id": "lower-bound",
        "title": "Lower Bound",
        "step_id": 4,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["binary-search", "fundamentals"],
        "what_this_teaches": (
            "The **half-open** binary-search style and its two atomic "
            "operations — lower bound and upper bound — that power "
            "every range query, first/last occurrence, and insert-"
            "position problem in the sorted-array world."
        ),
        "pattern": "Half-open binary search; `hi = mid` on candidate, `lo = mid + 1` otherwise.",
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["binary-search"],
        "next_problems": [
            "upper-bound",
            "search-insert-position",
            "first-last-occurrence",
            "count-occurrences",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 4 (BS on 1D Arrays)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "Python docs — bisect.bisect_left",
                "url": "https://docs.python.org/3/library/bisect.html#bisect.bisect_left",
            },
        ],
        "understanding": r'''
**Lower bound** of `x` in a sorted array is the smallest index `i`
such that `arr[i] >= x`. If every element is smaller than `x`, the
lower bound is `n` (one past the end).

Examples:
- `arr = [1, 2, 3, 3, 5, 8]`, `x = 3` → lower bound is 2 (the
  first index where `arr[i] >= 3`).
- `arr = [1, 2, 4]`, `x = 3` → lower bound is 2 (`4 >= 3`).
- `arr = [1, 2, 3]`, `x = 5` → lower bound is 3 (one past the end).

Lower bound is one of the most useful primitives in DSA. It powers
"first occurrence", "count of values ≥ x", "insert position
preserving sorted order", and many more.
''',
        "brute_force": {
            "explanation": r'''
Walk left to right and return the first index `i` with `arr[i] >= x`.
*O(n)*.

```python
for i, v in enumerate(arr):
    if v >= x:
        return i
return len(arr)
```

This is fine and arguably *more* readable than the binary search
version. But binary search drops the cost to *O(log n)*.
''',
            "code": r'''def lower_bound_linear(arr: list[int], x: int) -> int:
    for i, v in enumerate(arr):
        if v >= x:
            return i
    return len(arr)
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "thought_process": r'''
The half-open style works beautifully here. We use `lo = 0` and
`hi = n` (one past the end). The invariant: the answer lies in
`[lo, hi]` (note: hi is allowed to equal `n`, representing "no such
index exists in the array").

At each step we compute `mid = (lo + hi) // 2`. We compare
`arr[mid]` with `x`:

- If `arr[mid] < x`: index `mid` cannot be the answer (we need
  `>= x`). The answer is strictly to the right. Set `lo = mid + 1`.
- Otherwise (`arr[mid] >= x`): index `mid` is a *candidate* — it
  satisfies the condition. The answer might be `mid` itself, or
  something even earlier. Set `hi = mid`.

The loop continues while `lo < hi`. When they meet, `lo == hi` is
the answer.

The key subtlety is `hi = mid` (not `mid - 1`) when the midpoint is
a candidate. We do not want to exclude `mid` — we want to allow
ourselves to return it.

If this gives you that "off-by-one anxiety" feeling, the cure is to
walk through a tiny example on paper. `arr = [1, 3, 3, 5]`, `x = 3`.
Trace `lo`, `hi`, and `mid` at each iteration. Five minutes of
paper-walking saves five hours of debugging.
''',
        "optimized": {
            "explanation": r'''
Half-open binary search. *O(log n)* time.
''',
            "code": r'''def lower_bound(arr: list[int], x: int) -> int:
    lo, hi = 0, len(arr)            # half-open: hi can equal n
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < x:
            # mid is too small; the answer is strictly to the right.
            lo = mid + 1
        else:
            # mid is a candidate (arr[mid] >= x). Keep it in range,
            # but try to do better on the left.
            hi = mid
    return lo


def upper_bound(arr: list[int], x: int) -> int:
    """First index with value strictly greater than x."""
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] <= x:
            lo = mid + 1
        else:
            hi = mid
    return lo
''',
            "complexity": "**Time**: *O(log n)*. **Space**: *O(1)*.",
        },
        "deep_concept": r'''
Lower bound and upper bound are the **two atomic operations** of the
sorted-array world. Almost every "how many ___" or "where would I
insert ___" query factors through them.

Examples:

- **Count of value == x**: `upper_bound(x) - lower_bound(x)`.
- **First occurrence of x**: `lower_bound(x)`, then verify
  `arr[index] == x`.
- **Last occurrence of x**: `upper_bound(x) - 1`, then verify.
- **Number of values < x**: `lower_bound(x)`.
- **Number of values in range [L, R]**:
  `upper_bound(R) - lower_bound(L)`.
- **Where to insert x preserving sorted order**: `lower_bound(x)`
  (or `upper_bound(x)` for "after existing duplicates").

Python's `bisect` module ships these as `bisect_left` (lower bound)
and `bisect_right` (upper bound). In production code, use them. In
interview code, you should be able to write both versions from
memory.

The half-open style (`hi = n`, condition `lo < hi`) is the cleanest
formulation for these. It avoids the awkward `lo > hi` exit and the
"return -1" cases. Get used to it.
''',
        "confusion_notes": [
            {
                "question": "Why `hi = mid` instead of `hi = mid - 1` on the candidate branch?",
                "answer": r'''
Because in the half-open style, `hi` is **exclusive** — it
points one past the end of the search window, not at the last
valid index. When we find a candidate `mid` (an index that
satisfies `arr[mid] >= x`), we want to keep that candidate as a
possible answer **while also exploring earlier positions** that
might also satisfy.

If we wrote `hi = mid - 1`, we would *exclude* `mid` from the
next window. That is wrong: `mid` was a valid candidate, and a
better answer might equal `mid` itself.

Walk through `arr = [1, 3, 5, 7]`, `x = 5`. Initial state: `lo
= 0, hi = 4`. First iteration: `mid = 2, arr[mid] = 5 >= x`.
We want to keep mid 2 as a candidate but try smaller indices.
`hi = mid = 2`. Next state: `lo = 0, hi = 2`. `mid = 1, arr[mid]
= 3 < x`. So `lo = mid + 1 = 2`. State: `lo = 2, hi = 2`. Loop
exits. Return 2. Correct.

The contrasting branch — when `arr[mid] < x`, meaning `mid` is
**too small** — uses `lo = mid + 1` to exclude `mid`. That is
correct because we know `mid` is not the answer; it is strictly
smaller than what we need.

The asymmetry — `hi = mid` (inclusive of the candidate) versus
`lo = mid + 1` (exclusive of the disqualified) — is the heart
of the half-open style. It feels weird at first; after a few
practices it feels natural.
''',
            },
            {
                "question": "Why does the loop use `lo < hi` instead of `lo <= hi`?",
                "answer": r'''
Because the half-open window `[lo, hi)` (lo inclusive, hi
exclusive) is non-empty when `lo < hi`. When `lo == hi`, the
window contains zero elements and we should stop.

This is different from the inclusive-style binary search in the
previous problem (where the window `[lo, hi]` is non-empty when
`lo <= hi`). The two styles answer the same questions but use
different boundary conventions.

In the half-open style, when the loop exits with `lo == hi`,
that single value is the answer — the index where the lower
bound lives, or `len(arr)` if no element satisfies the
condition. No "return -1" sentinel needed; the half-open style
encodes "not found" by returning `len(arr)`.

The half-open style is cleaner for queries like "where would I
insert this value?" or "how many elements are less than this?"
— both naturally accept `len(arr)` as a valid answer.

Once you internalize "half-open windows are non-empty when `lo
< hi`," the boundary mechanics fall into place.
''',
            },
            {
                "question": "What's the difference between lower bound, upper bound, and `bisect_left/bisect_right`?",
                "answer": r'''
Lower bound = `bisect_left`. Upper bound = `bisect_right`. Just
different names for the same two operations.

- **Lower bound** of `x`: the first index where `arr[i] >= x`.
- **Upper bound** of `x`: the first index where `arr[i] > x`.

When `x` is not in the array, both return the same index —
where `x` *would* be inserted to maintain sorted order.

When `x` is in the array (possibly multiple times), `lower_bound`
returns the index of the **leftmost** occurrence, and
`upper_bound` returns the index *just past* the **rightmost**
occurrence.

The count of occurrences of `x` is `upper_bound(x) -
lower_bound(x)`. The position to insert `x` to keep order
(before existing duplicates) is `lower_bound(x)`; (after
existing duplicates) is `upper_bound(x)`.

Python ships them as `bisect.bisect_left` and
`bisect.bisect_right`. The C++ names are
`std::lower_bound` and `std::upper_bound`. Java's `Collections.
binarySearch` returns something slightly different — *some*
matching index or a negative encoded insertion point. Each
language has its quirks; the conceptual operations are the
same.

For interview practice, learn to write both from memory. They
are tiny and reusable.
''',
            },
            {
                "question": "Why does the function return `len(arr)` if nothing matches?",
                "answer": r'''
Because the answer "no element is `>= x`" naturally encodes as
"the insertion point is past the end of the array."

Suppose `arr = [1, 2, 3]` and `x = 5`. There is no element in
`arr` that is `>= 5`. The lower bound, by definition, is the
first index where `arr[i] >= 5` — but no such index exists. The
convention is to return `len(arr) = 3`, meaning *"to keep `arr`
sorted while preserving the lower-bound property, we would
insert `5` at index 3 (just after the last element)."*

This convention has two beautiful consequences:

1. **No special-case for "not found."** The same return value
   handles both "x exists at this index" and "x does not exist;
   would be inserted here." The caller can disambiguate by
   checking `arr[returned_index] == x`.
2. **The function is total over all inputs.** Every input
   produces a valid integer in `[0, len(arr)]`.

If you wanted a "true binary search" returning -1 on miss,
combine lower bound with a single check:

```python
def find_index(arr, x):
    lb = lower_bound(arr, x)
    if lb < len(arr) and arr[lb] == x:
        return lb
    return -1
```

This pattern — *"lower bound + presence check"* — is the cleanest
way to implement both "find" and "insert" in one toolkit.
''',
            },
        ],
        "summary": r'''
**Pattern**: half-open binary search, `lo < hi`, `hi = mid` (not
`mid - 1`) on the candidate branch.

**Lesson**: lower bound and upper bound are the atomic operations
of sorted-array queries. Every range count, insert position, and
first/last occurrence factors through them.

**Recognize next time**: "first index satisfying property P" where
P is monotonic. The half-open binary search is the move.
''',
    },
    {
        "id": "find-peak-element",
        "title": "Find Peak Element",
        "step_id": 4,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["binary-search", "peaks"],
        "what_this_teaches": (
            "Binary search works on **monotonic decisions**, not just "
            "sorted values. The slope test 'is `arr[mid] < arr[mid+1]`' "
            "gives a one-bit answer that eliminates half the array, "
            "even though the array itself is not sorted."
        ),
        "pattern": "Binary search on slope direction; uphill at mid means peak is to the right.",
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["binary-search", "lower-bound"],
        "next_problems": [
            "single-element-sorted",
            "search-rotated-i",
            "min-in-rotated",
            "peak-element-2d",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 4 (BS on 1D Arrays)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 162 — Find Peak Element",
                "url": "https://leetcode.com/problems/find-peak-element/",
            },
        ],
        "understanding": r'''
A **peak element** is one that is **strictly greater than its
neighbours**. Given an array where every consecutive pair of
elements is distinct (we will assume), return the index of **any**
peak. You may assume `arr[-1] = arr[n] = -∞`, so the ends are
peaks if they are greater than their single neighbour.

Example: `[1, 2, 3, 1]` → peak is `3` at index 2.

The interesting twist: the array is **not** sorted. Yet binary
search still works, because the **slope at the midpoint tells us
where a peak must exist**.
''',
        "brute_force": {
            "explanation": r'''
Walk through and return any index whose value is greater than both
its neighbours (handle the endpoints carefully). *O(n)*.

```python
for i in range(n):
    left = arr[i - 1] if i > 0 else float('-inf')
    right = arr[i + 1] if i < n - 1 else float('-inf')
    if arr[i] > left and arr[i] > right:
        return i
```
''',
            "code": r'''def find_peak_linear(arr: list[int]) -> int:
    n = len(arr)
    for i in range(n):
        left = arr[i - 1] if i > 0 else float('-inf')
        right = arr[i + 1] if i < n - 1 else float('-inf')
        if arr[i] > left and arr[i] > right:
            return i
    return -1
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "thought_process": r'''
The *aha* of this problem is realizing that **a peak must exist
somewhere on any "uphill" slope**, by the discrete equivalent of
the intermediate value theorem. If you stand at index `mid` and
look at `arr[mid + 1]`:

- If `arr[mid + 1] > arr[mid]`: the slope is uphill. Walk right.
  At some point — possibly at the very end — the slope must turn
  and a peak appears. The peak is in `[mid + 1, n - 1]`.
- If `arr[mid + 1] < arr[mid]`: the slope is downhill. The peak is
  to the left, in `[0, mid]`.

So at every step we discard half the array. Binary search applies.

This algorithm finds **a** peak — not all peaks, not the global
maximum. The problem only asks for any one, which is what we give.

A common rookie confusion: "but the array is not sorted, so why
binary search?". The answer is that binary search works on **any**
monotonic decision, not just sorted-comparisons. Here the decision
is "is the slope uphill at `mid`?", and the answer's existence in
one of the two halves is the monotonic property we exploit.
''',
        "optimized": {
            "explanation": r'''
Compare `arr[mid]` to `arr[mid + 1]` to decide which half contains
a peak.
''',
            "code": r'''def find_peak_element(arr: list[int]) -> int:
    lo, hi = 0, len(arr) - 1
    # Invariant: a peak exists somewhere in arr[lo..hi].
    while lo < hi:
        mid = (lo + hi) // 2
        # The crucial comparison is between mid and mid + 1, not mid - 1.
        # If arr[mid] < arr[mid + 1], the slope is uphill heading right.
        if arr[mid] < arr[mid + 1]:
            # A peak must exist in the right half (mid + 1..hi).
            lo = mid + 1
        else:
            # The slope is non-ascending. A peak exists in [lo..mid].
            # Note: we include mid because it might itself be a peak.
            hi = mid
    # lo == hi: the converged index is a peak.
    return lo
''',
            "complexity": "**Time**: *O(log n)*. **Space**: *O(1)*.",
        },
        "deep_concept": r'''
This problem is the cleanest example of **"binary search where the
data is not sorted, but the decision rule is monotonic"**. The
"sortedness" we exploit is not in the values themselves, but in
the **slope** — the relationship between adjacent values.

Once you internalize this, you start seeing binary search in places
that have nothing to do with sorted arrays:

- **Find any local minimum** — same idea, flipped slope.
- **Search in a rotated sorted array** — the monotonic property is
  "one of the halves is sorted; the target lies in that half if its
  value is in range".
- **Peak in a 2D matrix** — binary search the columns; within the
  chosen column, find the max in linear time.

The unifying principle: binary search works whenever you can compute
a comparison that **eliminates half the candidates**, regardless of
how those candidates are laid out.

A subtle point: this algorithm finds **any** peak. Finding **all**
peaks is necessarily *O(n)* because you must inspect every element.
Finding the **maximum** peak is also *O(n)* in general. We only get
*O(log n)* because we are happy with any peak.
''',
        "confusion_notes": [
            {
                "question": "How can binary search work when the array isn't sorted?",
                "answer": r'''
Binary search does not require sortedness — it requires
**monotonicity in a decision rule**. Whenever you can compute a
yes/no test at the midpoint that tells you which half contains
the answer, binary search applies.

For peak finding, the decision rule is *"is the slope going up
at index `mid`?"* — that is, *is `arr[mid] < arr[mid + 1]`?*. If
yes, the slope is climbing; somewhere to the right (possibly at
the very end) the climb must reverse, so a peak exists in `[mid
+ 1, hi]`. If no, the slope is non-ascending; a peak exists in
`[lo, mid]` (and `mid` itself might be one).

Each step eliminates half the array based on this slope check.
That gives *O(log n)*, even though the underlying values are not
sorted.

The bigger insight: **sortedness is one example of monotonic
structure, not the only one**. Whenever a problem has any
structural property that lets one comparison rule out half the
candidates, binary search applies. We will see this idea
explode in Lecture 2 of this step ("BS on Answers"), where the
sorted thing being searched is not even the input — it is the
*space of possible answers*.

For now, internalize: binary search needs a one-bit decision
that halves the candidates. The candidates can be array indices,
real numbers, or even abstract "settings" for a separate
algorithm.
''',
            },
            {
                "question": "Why compare `arr[mid]` with `arr[mid + 1]` instead of with `arr[mid - 1]`?",
                "answer": r'''
You could do either, but `arr[mid] < arr[mid + 1]` is the
convention because it tells you the slope *going forward*, which
matches how the search window narrows.

If `arr[mid] < arr[mid + 1]`, the slope is uphill heading right.
A peak must exist somewhere in `[mid + 1, hi]` (because the
array eventually descends or ends, and the highest point along
that ascent is a peak). So `lo = mid + 1`.

If `arr[mid] >= arr[mid + 1]`, the slope is flat or descending.
A peak must exist in `[lo, mid]` (mid itself might be one,
because either it is the local max or the descent will reverse
to the left). So `hi = mid`.

Using `arr[mid] vs arr[mid - 1]` would also work but you would
have to flip the bound updates. The forward-looking version is
slightly cleaner because it never accesses `arr[mid - 1]` (which
could be out of bounds when `mid == 0`).

A safer practice: always make sure your binary search loop **does
not access out-of-bounds indices**. Here, `arr[mid + 1]` is
always safe because the loop ends with `lo == hi`, never letting
`mid` equal the last index while `mid + 1` would be invalid.
The bounds work out exactly because we chose `hi = len(arr) -
1`, not `len(arr)`.
''',
            },
            {
                "question": "Why do the boundary conditions `arr[-1] = arr[n] = -∞` matter?",
                "answer": r'''
They are the **conceptual** trick that guarantees a peak always
exists. Without them, an array like `[1, 2, 3, 4]` has no peak
in the usual sense (every element except the last has a larger
neighbour to the right; the last element has no neighbour to
the right).

The convention `arr[-1] = arr[n] = -∞` says: pretend there are
imaginary `-∞` sentinels at both ends. Now:

- For `[1, 2, 3, 4]`, the rightmost `4` is bigger than its left
  neighbour `3` and bigger than the imaginary `-∞` to its right.
  So `4` is a peak.
- For `[4, 3, 2, 1]`, the leftmost `4` is bigger than the
  imaginary `-∞` to its left and bigger than its right neighbour
  `3`. So `4` is a peak.

This guarantees that any non-empty array has at least one peak,
which lets the binary search terminate on a valid answer.

In code, you do not actually create the sentinels. The loop's
boundary handling does it implicitly: when `lo` or `hi` is at an
end of the array, the slope comparison naturally treats "off the
end" as "lower than anything in the array," because the comparison
itself is forward-looking and stays in bounds.

The takeaway: the imaginary boundary values are a **mathematical
device** to make the problem well-defined. The code lives with
them invisibly.
''',
            },
            {
                "question": "What if the array has repeated values?",
                "answer": r'''
The standard problem assumes adjacent elements are **distinct**
(`arr[i] != arr[i + 1]` for all `i`). That assumption makes the
slope strictly increasing or decreasing at every position, so
the binary search always knows which way to go.

If the array can have plateaus (equal adjacent values), the
slope is flat at some positions and the binary search loses its
direction signal. The simple algorithm might still work
correctly on some inputs but fail on adversarial ones (long
plateaus).

The fix is more sophisticated:

- For 1D peaks with plateaus, fall back to *O(n)* linear scan,
  or use a more careful invariant.
- For 2D peaks, binary search on one dimension and linear scan
  on the other; this generalizes to handle plateaus naturally.

In an interview, ask up front: *"can adjacent elements be
equal?"*. If yes, switch to a different algorithm or argue why
the slope condition still works for your input class.

For LeetCode 162, the problem promise is "no two adjacent
elements are equal," so the simple binary search is correct.
''',
            },
        ],
        "summary": r'''
**Pattern**: binary search on slope direction.

**Lesson**: binary search needs only a monotonic decision rule, not
a globally sorted array. The "uphill or downhill at the midpoint?"
question splits the candidate space in half.

**Recognize next time**: any problem where you can decide which
half contains the answer based on a constant-time local test.
''',
    },
    {
        "id": "search-rotated-i",
        "title": "Search in Rotated Sorted Array (Unique Elements)",
        "step_id": 4,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["binary-search", "rotated"],
        "what_this_teaches": (
            "How a slight twist on a familiar shape (sorted, but "
            "rotated) keeps `O(log n)` alive. At every midpoint, "
            "**one half is fully sorted**, and that half admits a "
            "fast 'is the target in this range?' check."
        ),
        "pattern": "Detect which half is sorted at mid; check if target lies in it; recurse accordingly.",
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["binary-search", "find-peak-element"],
        "next_problems": [
            "search-rotated-ii",
            "min-in-rotated",
            "rotations-count",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 4 (BS on 1D Arrays)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 33 — Search in Rotated Sorted Array",
                "url": "https://leetcode.com/problems/search-in-rotated-sorted-array/",
            },
        ],
        "understanding": r'''
A sorted array (ascending, no duplicates) has been **rotated** at
some unknown pivot. Example: `[4, 5, 6, 7, 0, 1, 2]` is the array
`[0, 1, 2, 4, 5, 6, 7]` rotated by 4 positions. Given the rotated
array and a target value, return the target's index, or `-1` if
absent.

The naive linear search is *O(n)*. The interesting question is
whether we can still do *O(log n)* even though the array is no
longer fully sorted.

The answer is yes, with a small twist.
''',
        "brute_force": {
            "explanation": r'''
Walk left to right. *O(n)*. Simple and correct.

The real prize is the *O(log n)* version, which adapts binary
search to handle the "one rotation" structure.
''',
            "code": r'''def search_rotated_linear(arr: list[int], x: int) -> int:
    for i, v in enumerate(arr):
        if v == x:
            return i
    return -1
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "thought_process": r'''
The key observation: in a rotated sorted array, **at any midpoint,
at least one of the two halves is itself a fully sorted subarray**.
Specifically:

- If `arr[lo] <= arr[mid]`, the left half `arr[lo..mid]` is sorted.
- Otherwise, the right half `arr[mid..hi]` is sorted.

Once we know which half is sorted, we can check whether the target
falls in that half's range. If yes, recurse into that half. If no,
recurse into the other half.

This gives us an *O(log n)* algorithm with one extra constant of
work per iteration (the "is left half sorted?" check). Beautiful.

Walking through `[4, 5, 6, 7, 0, 1, 2]`, target = 0:

- `lo = 0, hi = 6, mid = 3, arr[mid] = 7`. Left half
  `[4, 5, 6, 7]` is sorted (`arr[lo] = 4 <= arr[mid] = 7`). Is
  target 0 in `[4, 7]`? No. Recurse right.
- `lo = 4, hi = 6, mid = 5, arr[mid] = 1`. Left half `[0, 1]` is
  sorted. Is target 0 in `[0, 1]`? Yes. Recurse left.
- `lo = 4, hi = 4, mid = 4, arr[mid] = 0`. Match. Return 4.

Three iterations, found.

The hardest part is the bookkeeping for the "in range" check.
Inclusive or exclusive bounds matter. Get a small example right on
paper, then translate to code.
''',
        "optimized": {
            "explanation": r'''
Binary search adapted to rotated sorted arrays. Each iteration
detects which half is sorted and recurses appropriately.
''',
            "code": r'''def search_rotated(arr: list[int], x: int) -> int:
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == x:
            return mid
        # Determine which half is sorted.
        if arr[lo] <= arr[mid]:
            # Left half is sorted: arr[lo..mid] is non-decreasing.
            if arr[lo] <= x < arr[mid]:
                # Target is somewhere in the sorted left half.
                hi = mid - 1
            else:
                # Target is in the unsorted right half.
                lo = mid + 1
        else:
            # Right half is sorted: arr[mid..hi] is non-decreasing.
            if arr[mid] < x <= arr[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
''',
            "complexity": "**Time**: *O(log n)*. **Space**: *O(1)*.",
        },
        "deep_concept": r'''
The lesson here is that **the property we binary search on does not
have to be "values are sorted globally"**. It can be any property
that lets us decide which half to throw away.

In rotated sorted arrays, the property is **"one half is sorted, and
sorted halves admit a fast range check"**. That single observation
takes a problem that *looks* unsortable and restores `O(log n)`.

Variations:

- **Rotated array with duplicates** — the "is left half sorted?"
  check fails when `arr[lo] == arr[mid]`, because we cannot tell
  which side the rotation point is on. The trick is to shrink the
  ambiguous boundary by 1 (`lo += 1`), which degrades the worst
  case to `O(n)` for adversarial inputs but stays `O(log n)` in
  most practical cases.
- **Find the rotation point** — binary search for the index of the
  minimum element. The same "one half is sorted" logic applies.
- **Find how many times the array was rotated** — same as finding
  the rotation index.

The unifying mental model: the rotation point divides the array
into two sorted "runs". Binary search learns to handle this
two-run structure with one extra comparison.
''',
        "confusion_notes": [
            {
                "question": "Why is it true that 'at least one half is always sorted'?",
                "answer": r'''
Because the rotation creates exactly **one discontinuity** — the
point where the values drop from the largest to the smallest. The
discontinuity lives in only one of the two halves around any
midpoint. The other half is a continuous slice of the original
sorted sequence and is therefore itself sorted.

Walk through `arr = [4, 5, 6, 7, 0, 1, 2]`. The discontinuity is
between indices 3 and 4 (the drop from 7 to 0). If we pick `mid
= 3`, the left half `[4, 5, 6, 7]` is fully sorted; the right
half `[0, 1, 2]` is also fully sorted (the discontinuity is
right at the boundary). If we pick `mid = 4`, the left half `[4,
5, 6, 7, 0]` contains the discontinuity but the right half `[0,
1, 2]` is sorted.

To detect which half is sorted, compare `arr[lo]` with
`arr[mid]`. If `arr[lo] <= arr[mid]`, the left half is sorted
(values rise from `lo` to `mid`). Otherwise the discontinuity
lives in the left half, which means the right half must be
sorted.

This `arr[lo] <= arr[mid]` check is one comparison per
iteration, on top of the usual binary search comparison. The
total work is still `O(log n)`, just with a slightly fatter
constant.
''',
            },
            {
                "question": "After detecting the sorted half, why check `arr[lo] <= x < arr[mid]` specifically?",
                "answer": r'''
Because that check answers *"is the target in the sorted half?"*.
A sorted half admits a fast range check.

If the left half `[lo..mid]` is sorted, its values run from
`arr[lo]` up to `arr[mid]`. The target `x` is in that half if
and only if `arr[lo] <= x < arr[mid]`. We use strict less-than
on the right side because the upper bound `arr[mid]` was
already checked at the top of the loop (and was not the target),
so we exclude it.

If the target is in the sorted half, recurse left (`hi = mid -
1`). If not, the target — if it exists — must be in the
**unsorted** half. Recurse right (`lo = mid + 1`).

The clever part: we never need to recursively "search" the
unsorted half. We just descend into it, and the next iteration
will again detect which half is sorted at the new midpoint. The
algorithm keeps narrowing the window until the target appears
or the window collapses.

The symmetric branch (when the right half is sorted) uses `arr[
mid] < x <= arr[hi]`. Again, strict on the side that has been
checked, inclusive on the other side.

Get the boundary `<=` versus `<` exactly right and the algorithm
works. Swap them and you get subtle off-by-ones. Trace a small
example on paper to be sure.
''',
            },
            {
                "question": "What happens with duplicates? Does the algorithm still work?",
                "answer": r'''
Not without modification. If `arr[lo] == arr[mid]`, we can no
longer tell which half is sorted — both halves might be flat
runs of the same value, or one might hide the discontinuity.

For example, `arr = [2, 2, 2, 0, 2, 2]` (rotated array with
duplicates) at `mid = 2`: `arr[lo] = 2 == arr[mid] = 2`. The
left half could be `[2, 2, 2]` (sorted) or `[2, 2, 2, 0]`
(unsorted because of the 0). We do not know.

The fix in the duplicate version (Step 4 has its own problem
"Search in Rotated Sorted Array II") is to **shrink the
ambiguous boundary by one** and retry:

```python
if arr[lo] == arr[mid] == arr[hi]:
    lo += 1
    hi -= 1
    continue
```

This restores the algorithm's ability to make progress, at the
cost of a `O(n)` worst case for adversarial inputs (all
duplicates). For typical inputs the average remains `O(log n)`.

The general lesson: equality in a binary-search-style comparison
often kills the bisection guarantee. When duplicates are
possible, ask whether your algorithm still has a strict slope to
search on; if not, add a fallback or use a different approach.
''',
            },
            {
                "question": "Could I just find the rotation point first, then binary search the right half?",
                "answer": r'''
Yes! That is a perfectly valid two-pass approach:

1. Binary search to find the index of the minimum element (the
   rotation point). This is `O(log n)`.
2. Binary search the relevant half for the target, also `O(log
   n)`.

Total: `O(log n)`. The two-pass version is sometimes easier to
explain — find the pivot, then do a plain binary search on the
correct subarray.

The one-pass version we covered does both jobs at once. It is
slightly more elegant but has more boundary conditions to get
right.

For interviews, either is acceptable. State both approaches,
explain the trade-off (clarity vs. compactness), and implement
whichever you find easier to write correctly under pressure.

The bigger lesson: many problems have **multiple correct
approaches** at the same complexity. Choose the one you can
write bug-free in five minutes, not the one that looks cleverest
on paper.
''',
            },
        ],
        "summary": r'''
**Pattern**: detect which half is sorted, then check whether the
target is in that half.

**Lesson**: rotated sorted arrays still admit `O(log n)` search,
because at every midpoint at least one half is fully sorted.

**Recognize next time**: any "binary search but the data has been
shifted / rotated / cyclically reordered". The same two-step
("which half is sorted? does target fall in it?") works.
''',
    },
    {
        "id": "koko-bananas",
        "title": "Koko Eating Bananas (BS on Answer)",
        "step_id": 4,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["binary-search", "bs-on-answer"],
        "what_this_teaches": (
            "The lifting move that turns binary search into a **general "
            "optimization technique**: search the *answer space* "
            "instead of the input. Whenever you can write a monotonic "
            "feasibility check, you can binary search the answer in "
            "`O(log(range) × check_cost)`."
        ),
        "pattern": "Binary search on the answer with a linear-time feasibility checker.",
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["binary-search", "lower-bound"],
        "next_problems": [
            "min-days-bouquets",
            "smallest-divisor-threshold",
            "ship-packages-d-days",
            "aggressive-cows",
            "book-allocation",
            "split-array-largest-sum",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 4 (BS on Answers)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 875 — Koko Eating Bananas",
                "url": "https://leetcode.com/problems/koko-eating-bananas/",
            },
        ],
        "understanding": r'''
Koko has `n` piles of bananas. Pile `i` has `piles[i]` bananas.
She has `h` hours to finish all the piles. Each hour she eats
**up to `k` bananas** from a single pile; if the pile has fewer
than `k` bananas left, she eats all of them and finishes the hour
without moving on to another pile.

Find the **minimum integer `k`** (eating speed) such that Koko
finishes within `h` hours.

Example: `piles = [3, 6, 7, 11]`, `h = 8` → answer `4`.

This problem is the **prototype** of "binary search on the answer".
The candidate answers (eating speeds) form a sorted range from `1`
to `max(piles)`. For each candidate speed we can check "can she
finish?" in *O(n)*. The "can she finish?" answer is monotonic: if
she can at speed `k`, she can at any speed > `k`. So binary search
the speeds.
''',
        "brute_force": {
            "explanation": r'''
Try every speed from 1 to `max(piles)` and return the first that
works. *O(max(piles) × n)* — slow but obviously correct.

```python
for k in range(1, max(piles) + 1):
    if can_finish(piles, h, k):
        return k
```
''',
            "code": r'''def hours_at_speed(piles: list[int], k: int) -> int:
    # Time to eat each pile is ceil(pile / k).
    total = 0
    for p in piles:
        total += (p + k - 1) // k    # ceiling division
    return total


def koko_brute(piles: list[int], h: int) -> int:
    for k in range(1, max(piles) + 1):
        if hours_at_speed(piles, k) <= h:
            return k
    raise ValueError("impossible")
''',
            "complexity": (
                "**Time**: *O(n × max(piles))*. **Space**: *O(1)*."
            ),
        },
        "thought_process": r'''
The brute force iterates speeds in order; the first feasible speed
is the answer. But speeds form a **monotonic boundary**: there is
some threshold `k*` below which she cannot finish and above which
she can. Binary search the threshold.

The recipe:

1. **Identify the candidate range.** Eating speed must be at least 1
   (she has to eat *something*) and at most `max(piles)` (any speed
   above that doesn't help — she finishes the biggest pile in 1
   hour, the others sooner or already).
2. **Write a checker** `can_finish(k)` that returns `True` if she
   finishes in ≤ `h` hours at speed `k`. The checker is *O(n)* using
   ceiling division: pile `p` takes `ceil(p / k)` hours.
3. **Verify monotonicity.** If she can at speed `k`, she can at any
   speed > `k`. Yes.
4. **Binary search**: half-open range `[1, max(piles) + 1)`. We
   want the smallest `k` with `can_finish(k) == True`. Use the
   half-open "lower bound" style.

That recipe is identical for every "binary search on the answer"
problem. Steps 1–4 every time.

Note the ceiling division trick: `(p + k - 1) // k` computes
`ceil(p / k)` using only integer ops. It is a very common idiom and
worth memorizing.
''',
        "optimized": {
            "explanation": r'''
Binary search the eating speed. Each check is *O(n)*.
''',
            "code": r'''def min_eating_speed(piles: list[int], h: int) -> int:
    def can_finish(k: int) -> bool:
        # Total hours at speed k. Ceiling division per pile.
        total = 0
        for p in piles:
            total += (p + k - 1) // k
            # Early exit if we already exceed h; saves time.
            if total > h:
                return False
        return total <= h

    # Candidate eating speeds. lo = 1 (cannot eat 0). hi = max(piles)
    # because at that speed every pile takes 1 hour, and there are at
    # most n piles, so total hours <= n <= h is guaranteed.
    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if can_finish(mid):
            # mid is feasible; try to do better (slower).
            hi = mid
        else:
            # mid is too slow; must speed up.
            lo = mid + 1
    return lo
''',
            "complexity": (
                "**Time**: *O(n log(max(piles)))*. The binary search "
                "has *O(log(max(piles)))* iterations, each doing "
                "*O(n)* checker work.\n\n"
                "**Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
"Binary search on the answer" is one of the most generalizable
patterns in DSA. The signal is: the problem asks for the **minimum**
(or **maximum**) integer value satisfying some constraint, and the
constraint is **monotonic** in the value.

Whole families of medium / hard problems collapse to this pattern.
Examples on this very sheet:

- **Minimum days to make M bouquets** — search the number of days.
- **Smallest divisor given a threshold** — search the divisor.
- **Capacity to ship packages in D days** — search the capacity.
- **K-th missing positive number** — search the value (using a
  count-of-present-numbers checker).
- **Aggressive cows** — search the minimum spacing.
- **Book allocation / split array largest sum / painter's
  partition** — search the maximum sum per partition.
- **Median of two sorted arrays** — search the partition position.

Each of those is the same recipe: identify candidate range, write a
checker, verify monotonicity, binary search.

The cleverness in "binary search on the answer" is that you do not
search the data — you **search the space of possible answers**. The
checker is the *O(n)* "given this candidate, is it feasible?"
function. The binary search is *O(log(answer range))*.

Once you have done a few of these, your brain rewires. The next
time you see "minimum integer X such that ___", you reach for
`while lo < hi: mid = ...` without thinking.
''',
        "confusion_notes": [
            {
                "question": "Why does the candidate range run from `1` to `max(piles)`?",
                "answer": r'''
The minimum sensible speed is `1` — Koko has to eat at least one
banana per hour, otherwise she never finishes anything.

The maximum useful speed is `max(piles)`. Any speed above that
finishes every pile in a single hour, so the total time is
exactly `len(piles)` hours. Speeds higher than `max(piles)` give
the same total time as `max(piles)` itself — increasing past it
buys nothing. So the answer cannot exceed `max(piles)`.

That gives us a candidate range of `[1, max(piles)]`. The binary
search runs over this range, calling the feasibility checker
`can_finish(k)` at each midpoint. The number of iterations is
`log₂(max(piles))`, typically about 30 for inputs that fit in
32-bit integers. Combined with the `O(n)` checker, the total
runtime is `O(n log(max(piles)))`.

The general rule for "binary search on the answer": identify the
**tightest** range of candidate answers. Both endpoints matter
— too loose a range wastes iterations; too tight a range can
miss valid answers.

For Koko, you could safely use `hi = 10⁹` as a generous upper
bound (every banana count fits in a billion), but `max(piles)`
is tighter and slightly faster. Use the tightest bound you can
prove.
''',
            },
            {
                "question": "Why is `can_finish` monotonic, and why does monotonicity matter?",
                "answer": r'''
*Monotonic* means: if `can_finish(k)` is true for some `k`, then
`can_finish(k')` is true for every `k' > k`. Eating faster can
only make the total time *shorter*, never longer. So feasibility
is preserved as you increase the speed.

Why does monotonicity matter for binary search? Because the
search relies on knowing which **half** of the candidate range
contains the answer. With monotonicity, the answer space splits
cleanly into "infeasible" speeds (slow) on the left and
"feasible" speeds (fast) on the right. We want the boundary
between them, i.e., the smallest feasible speed.

Without monotonicity — say, if `can_finish` flickered between
true and false in some weird pattern — binary search would lose
its sense of direction. You would not know whether `mid` being
feasible means the answer is to the left (try slower) or to the
right (try even slower).

This is the rule: **the feasibility test must be monotonic for
binary search on the answer to work**. Always verify this
explicitly before reaching for the technique.

The cousin pattern, "monotonic decision rule on a non-sorted
array," is what we used in `find-peak-element`. Both are
applications of the broader principle: *binary search needs
monotonicity, in whatever form the problem provides it.*
''',
            },
            {
                "question": "Why use ceiling division `(p + k - 1) // k`? What's wrong with `p // k`?",
                "answer": r'''
Because eating bananas in a pile that does not divide evenly
**still costs a full hour**, not a partial one. The problem
statement says: if a pile has fewer than `k` bananas left, Koko
eats all of them and *finishes the hour* without moving on.

So a pile of `p` bananas at speed `k` takes `ceil(p / k)` hours,
not `p / k`. For example, `p = 5, k = 3`: she eats 3 in hour 1
(2 left), then 2 in hour 2 (0 left). Two hours, not `5 / 3 =
1.67`.

`p // k` does **floor** division — it rounds toward zero. That
would give `5 // 3 = 1`, which says "1 hour," which is wrong.

`(p + k - 1) // k` is the standard integer-arithmetic
**ceiling** trick. Adding `k - 1` before dividing by `k` ensures
that any non-zero remainder bumps the result up by one.

Walk through: `(5 + 3 - 1) // 3 = 7 // 3 = 2`. Correct.

`(6 + 3 - 1) // 3 = 8 // 3 = 2`. Correct (`6 / 3 = 2` exactly).

`(3 + 3 - 1) // 3 = 5 // 3 = 1`. Correct (`3 / 3 = 1`).

This idiom appears constantly in DSA. Memorize it: `ceil(a / b)
= (a + b - 1) // b` for non-negative integers. In Python you can
also use `math.ceil(a / b)`, but that goes through floats and is
slower; the integer version is preferred.
''',
            },
            {
                "question": "Why `hi = mid` on feasible and `lo = mid + 1` on infeasible?",
                "answer": r'''
Because we want the **smallest** feasible speed, and the
half-open binary-search style we are using treats `hi` as
inclusive of candidate answers and `lo` as exclusive of
disqualified ones.

When `can_finish(mid)` is true:
- `mid` itself is a valid answer (Koko finishes in time).
- A smaller speed *might* also work.
- So we keep `mid` as a candidate and try smaller: `hi = mid`.

When `can_finish(mid)` is false:
- `mid` is too slow; she does not finish in time.
- Any speed `< mid` is even slower, so they cannot work either.
- Eliminate `mid` and everything smaller: `lo = mid + 1`.

The loop continues while `lo < hi`. When they meet, `lo == hi`
is the smallest feasible speed.

If we wrote `hi = mid - 1` on the feasible branch, we would
*exclude* the candidate we just confirmed works. The algorithm
could then converge to a value that was never verified — wrong.

This asymmetric handling — `hi = mid` on "good," `lo = mid + 1`
on "bad" — is the heart of the half-open lower-bound style. It
is exactly the same shape as the `lower-bound` problem; we are
just searching speeds instead of array indices.
''',
            },
        ],
        "summary": r'''
**Pattern**: binary search on the answer space (not the data).

**Lesson**: when the answer is an integer in a known range and the
feasibility test is monotonic, binary search the range. Each step
costs one checker invocation.

**Recognize next time**: "minimum / maximum X such that property P
holds". Verify monotonicity, write the *O(n)* checker, binary
search the range. The recipe is mechanical.
''',
    },
]
