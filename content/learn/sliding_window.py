"""Sliding window — don't redo work you already did."""

LESSON = {
    "id": "sliding-window",
    "title": "Sliding Window — Don't Recompute What You Already Know",
    "tags": ["sliding-window", "two-pointers", "patterns"],
    "summary": (
        "A window is a contiguous slice of the array that grows and "
        "shrinks. The whole pattern is about updating the answer "
        "incrementally instead of recomputing from scratch."
    ),
    "body": r'''
## The motivating example

> Given an array of integers, find the maximum sum of any contiguous
> subarray of length k.

The brute force solution computes the sum of every window of size
`k`. Each sum costs *O(k)*, and there are *O(n)* windows, so the
total cost is *O(n × k)*. For long arrays with big `k`, that is
painful.

But notice this: when the window slides one step right, the new sum
is almost the same as the old sum. The new sum is **old sum, minus
the element leaving on the left, plus the element entering on the
right**. That update is *O(1)*. Therefore total time is *O(n)*.

```python
def max_window_sum(nums: list[int], k: int) -> int:
    # Set up the first window's sum.
    current = sum(nums[:k])
    best = current
    # Slide the window one step at a time.
    for right in range(k, len(nums)):
        # Add the entering element, subtract the leaving one.
        current += nums[right] - nums[right - k]
        best = max(best, current)
    return best
```

This is the soul of sliding window: **maintain a running summary of
the window so that each slide is constant time.**

## Two kinds of windows

### Fixed-size window

The size `k` is given. The window is exactly `k` wide every iteration.
You add one entering element and remove one leaving element per step.
The example above is fixed-size.

### Variable-size window

The window grows or shrinks based on a constraint. You have two
indices, `left` and `right`. You move `right` forward; if the
constraint is violated, you move `left` forward until it is satisfied
again. Then you record the current window if it is the best.

The canonical example: longest substring without repeating characters.

```python
def longest_unique(s: str) -> int:
    seen = {}                     # char -> last index we saw it at
    left = 0                      # left edge of the window
    best = 0
    for right, ch in enumerate(s):
        # If ch is already in the window, shrink from the left
        # until it is no longer in the window.
        if ch in seen and seen[ch] >= left:
            left = seen[ch] + 1
        seen[ch] = right          # record / update the last index
        best = max(best, right - left + 1)
    return best
```

Read it carefully. `left` only ever moves forward. `right` only ever
moves forward. So in the worst case each character is visited at most
twice — once by `right`, once by `left`. The total work is *O(n)*.

That "each pointer moves only forward" property is what gives sliding
window its linear time. If you ever find yourself wanting to back up
a pointer, you have left sliding-window land and you need a different
idea.

## The general recipe

For variable-size sliding window, almost every problem follows the
same shape:

1. Use two indices `left = 0` and `right = 0`.
2. Use a data structure (a dict, a counter, a set, sometimes a sum)
   that summarizes the current window.
3. Move `right` forward. Add the new element to the summary.
4. While the summary violates the constraint, move `left` forward and
   remove `nums[left]` from the summary.
5. The window between `left` and `right` is the longest valid window
   ending at `right`. Update the answer.

That recipe handles "longest substring with at most k distinct
characters", "longest subarray with sum ≤ S" (for non-negative
arrays), "fruit into baskets", "max consecutive ones III", and
dozens more. Same skeleton, different summary.

## Worked example: at most K distinct characters

> Find the longest substring containing at most `k` distinct
> characters.

```python
from collections import defaultdict

def longest_k_distinct(s: str, k: int) -> int:
    count = defaultdict(int)
    left = 0
    best = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        while len(count) > k:
            count[s[left]] -= 1
            if count[s[left]] == 0:
                del count[s[left]]
            left += 1
        best = max(best, right - left + 1)
    return best
```

Notice the structure exactly matches the recipe. The summary is a
dict of character counts. The constraint is "fewer than k+1 distinct
keys". The shrink step removes the leaving character and prunes
zero-count entries.

## When does sliding window not work?

Sliding window relies on a key property: **whenever you shrink, the
answer for the new window is at least as easy to maintain as the old
one's**. If the constraint is something where shrinking does not help
(e.g., "sum is divisible by m"), the pattern breaks. Instead you need
**prefix sums** plus hashing.

Another failure mode: arrays with **negative numbers** combined with
constraints on sum. With negatives, growing the window does not
monotonically increase the sum, so "shrink until valid, then grow"
loses its meaning. In those cases, prefix sums + hash is again the
move.

## Common beginner mistakes

**Mistake 1: forgetting to update the summary on shrink.** When
`left` advances, you must update the running summary to *remove*
`nums[left]`. Forgetting that is the most common bug.

**Mistake 2: returning the answer at the wrong place.** The window
`[left, right]` is valid only *after* the shrink loop. Update the
answer **after** shrinking, not inside the shrink loop.

**Mistake 3: confusing "at most k" with "exactly k".** A common
trick: count of subarrays with exactly k distinct = count of
subarrays with at most k - count with at most (k-1). Sliding window
naturally handles "at most".

**Mistake 4: trying to slide a window when the array has negatives
and you need a fixed sum.** Use hashing on prefix sums instead.

## The mental model

Sliding window is "incremental maintenance". Anywhere you find
yourself wanting to recompute a property of a contiguous range from
scratch, ask: *can I update the property in O(1) when the range
shifts by one?* If the answer is yes, you have a sliding window and
your *O(n²)* solution just became *O(n)*.
''',
}
