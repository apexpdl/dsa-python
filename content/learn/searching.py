"""Binary search — the algorithmic answer to 'half it'."""

LESSON = {
    "id": "searching",
    "title": "Searching — Linear, Binary, and Searching the Answer",
    "tags": ["binary-search", "searching", "fundamentals"],
    "summary": (
        "How linear search becomes binary search when the data is "
        "sorted, and how 'binary search on the answer' becomes a "
        "superweapon for a huge family of medium / hard problems."
    ),
    "body": r'''
## Linear search — the honest baseline

You have an array and you want to know if value `x` is in it. There is
nothing fancier than walking from left to right asking the question
one element at a time.

```python
def linear_search(arr: list[int], target: int) -> int:
    for i, v in enumerate(arr):
        if v == target:
            return i
    return -1
```

This is *O(n)*. It is honest, it works on any input, and it is
sometimes the right answer. Do not be embarrassed about it.

## Binary search — when sortedness changes everything

The moment your input is sorted, you have a superpower. Picture
yourself looking up a name in a paper phone book. You do not start at
"A" and read every name. You open to the middle, look at the name
there, and ask: "is my name before or after this?". You then look at
the middle of whichever half remains, and repeat.

Each step halves the haystack. So instead of *n* comparisons, you
need only about *log₂(n)*. For one million items, that is roughly
twenty steps — and not twenty thousand.

```python
def binary_search(arr: list[int], target: int) -> int:
    lo, hi = 0, len(arr) - 1
    # Loop while the search window is non-empty.
    while lo <= hi:
        # Midpoint, computed in a way that avoids overflow in other
        # languages. In Python it does not matter for correctness, but
        # the pattern is worth memorizing.
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid                  # found it
        elif arr[mid] < target:
            lo = mid + 1                # discard the left half
        else:
            hi = mid - 1                # discard the right half
    return -1                           # not found
```

Three invariants make binary search work:

1. **The data is sorted** (or at least monotonic in some sense).
2. **The answer must lie in the current window** `[lo, hi]`. Whenever
   we shrink, we shrink **away** from the answer.
3. **The window strictly shrinks each iteration.** That guarantees
   termination.

If any of those three break, binary search becomes a parade of
off-by-one bugs.

## Lower bound and upper bound

These are the two most useful variants. **Lower bound** finds the
first index whose value is at least the target. **Upper bound** finds
the first index whose value is strictly greater than the target.
Together they answer "how many copies of target are there?" — the
answer is `upper_bound - lower_bound`.

```python
def lower_bound(arr: list[int], target: int) -> int:
    lo, hi = 0, len(arr)              # note: hi is one past the end
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

This is the canonical "half-open interval" binary search. Many
beginners find it cleaner than the inclusive version above, because
the termination condition (`lo == hi`) is simpler.

## The leap: binary search on the answer

This is the trick that lifts binary search from "search a sorted
array" to "search any problem with a yes/no test that flips at some
threshold". Once you see this, an entire lecture of medium-hard
problems collapses.

The shape: you are asked for the **smallest** (or **largest**) value
that satisfies some property. There is a clear range of candidate
values. If the property holds for some value `x`, it also holds for
every value above `x` (or below — pick a direction). That
"monotonic yes/no" property is the door.

You binary-search the range. At every midpoint, you run the cheap
yes/no test. If yes, the answer lies in the cheaper half; if no, it
lies in the costlier half.

**Example: Koko Eating Bananas.** Koko has piles of bananas and `h`
hours. She eats `k` bananas per hour. Find the smallest `k` such
that she finishes in time.

The candidate `k` ranges from 1 to `max(piles)`. The test "can Koko
finish at speed k?" is a one-pass *O(n)* check. It is monotonic: if
she can finish at speed `k`, she can finish at any speed above `k`.
So we binary search the speed.

```python
def min_eating_speed(piles: list[int], h: int) -> int:
    def can_finish(k: int) -> bool:
        # ceil division: each pile takes ceil(p / k) hours.
        return sum((p + k - 1) // k for p in piles) <= h

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if can_finish(mid):
            hi = mid                  # mid is feasible; try smaller
        else:
            lo = mid + 1              # mid is too slow; try larger
    return lo
```

The pattern in english:

1. Identify the candidate range.
2. Write a yes/no checker that, given a candidate, runs in linear time.
3. Verify the checker is monotonic.
4. Binary search the range using the checker.

Whenever you find yourself trying to optimize a "minimum X such that
..." or "maximum X such that ...", reach for this pattern first.

## When does binary search not work?

When the data is not sorted, or the underlying decision is not
monotonic. For example, "find the index of any peak" works on the
binary-search idea because the comparison `arr[mid] vs arr[mid + 1]`
points reliably uphill. But "find the longest subarray with property
X" usually does not, because longer is not always better.

## Common beginner mistakes

**Mistake 1: off-by-one.** The classic trap. Decide once whether you
are using `[lo, hi]` (inclusive) or `[lo, hi)` (half-open) and stay
consistent. Mixing styles is bug heaven.

**Mistake 2: forgetting that the window must shrink.** A loop that
sets `lo = mid` instead of `lo = mid + 1` can spin forever. Check
that every branch makes progress.

**Mistake 3: testing equality first when you want a lower bound.** If
you want the first occurrence of duplicates, do not return on
`arr[mid] == target` — keep searching leftward.

**Mistake 4: forgetting `bisect`.** Python ships with the `bisect`
module: `bisect_left`, `bisect_right`, `insort`. For everyday code,
use them rather than rolling your own.

## The mental model

Linear search is a foot race. Binary search is a divide-and-conquer
elimination tournament. Binary search on the answer is an elimination
tournament where the *contestants are possible answers*, and a single
function call eliminates half of them at a time.

Once you can see "monotonic yes/no" in a problem, you are not just
solving the problem — you are wielding one of the most general
patterns in DSA. Step 4 of this curriculum is literally a whole
lecture devoted to spotting that pattern in disguise.
''',
}
