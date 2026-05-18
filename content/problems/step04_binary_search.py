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
