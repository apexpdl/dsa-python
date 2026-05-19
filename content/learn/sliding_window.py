"""Sliding window — don't redo work you already did."""

LESSON = {
    "id": "sliding-window",
    "title": "Sliding Window — Don't Recompute What You Already Know",
    "tags": ["sliding-window", "two-pointers", "patterns"],
    "summary": (
        "A full beginner chapter. A window is a contiguous slice of "
        "the array that grows and shrinks. The whole pattern is about "
        "updating the answer incrementally instead of recomputing "
        "from scratch."
    ),
    "body": r'''
## 0. Why this chapter matters

Sliding window is the pattern that turns nested-loop substring /
subarray problems into single-pass *O(n)* algorithms. Once you
see the skeleton, dozens of medium / hard problems collapse into
the same shape with small tweaks.

This chapter is the slow walk through that skeleton. By the end
you should be able to read any "longest / shortest / count of
contiguous range with property P" problem and reach for sliding
window without thinking.

## 1. The motivating example: max sum of any window of size k

> Given an array of integers and an integer `k`, find the maximum
> sum of any contiguous subarray of length exactly `k`.

Brute force: for each starting index, compute the sum of the
next `k` elements. Two nested loops. *O(n × k)*.

The key observation: when the window slides one step right, the
new sum is *almost* the same as the old sum. Specifically:

> **new_sum = old_sum - leaving_element + entering_element.**

That update is *O(1)*. So the total work is *O(n)*, regardless
of `k`.

```python
def max_window_sum(arr, k):
    current = sum(arr[:k])
    best = current
    for right in range(k, len(arr)):
        current += arr[right] - arr[right - k]
        best = max(best, current)
    return best
```

This is the soul of sliding window: **maintain a running summary
of the window so each slide is constant time**.

If you can update some property of the window in *O(1)* per
slide, you can solve the problem in *O(n)* total time. The
"property" might be a sum, a count, a max, a hash of contents —
whatever the problem cares about.

## 2. Fixed vs. variable size windows

There are two flavors of sliding window. Tell them apart at the
start; they have different bookkeeping.

### Fixed-size window

The size `k` is fixed and given. The window is always `k` wide.
You add one entering element and remove one leaving element per
step. Maximum sum of size-k subarray is the prototype.

### Variable-size window

The size adapts based on a constraint. You move the right edge
forward; when the constraint is violated, you move the left edge
forward until it's satisfied again. You record the answer
whenever the window is valid.

The variable-size template is the more common and more powerful
of the two. Most "longest substring with property P" problems
fit this shape.

## 3. The variable-size template

Memorize this skeleton; it solves a huge family of problems.

```python
left = 0
state = ...  # something that summarizes the current window
best = 0     # or whatever "no answer yet" means

for right in range(len(arr)):
    # 1. Extend the window by including arr[right].
    add_to_state(state, arr[right])

    # 2. Shrink the window from the left until the constraint holds.
    while constraint_violated(state):
        remove_from_state(state, arr[left])
        left += 1

    # 3. The window [left, right] is now valid. Record the answer.
    best = max(best, right - left + 1)

return best
```

The three pieces:

- **Add** the new element to the state.
- **Shrink** while the state is invalid.
- **Record** the answer for the current window.

The "state" is problem-specific. For "longest without repeats"
it is a set or dict. For "longest with at most K distinct" it is
a Counter. For "longest with sum ≤ S" (non-negative array) it is
a running sum.

The constraint and the add/remove operations also vary. But the
skeleton stays.

## 4. Worked example: longest substring without repeating chars

> Find the longest substring of `s` with no repeated characters.

State: a dict mapping character → its index in the window.
Constraint: each character appears at most once.

```python
def longest_unique(s):
    last_index = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last_index and last_index[ch] >= left:
            left = last_index[ch] + 1
        last_index[ch] = right
        best = max(best, right - left + 1)
    return best
```

Notes:

- We don't always `remove` characters from the dict. Instead, we
  use the `last_index[ch] >= left` check to ignore stale entries
  from before the window's left edge. Functionally identical to
  removing.
- The "shrink" step happens in one big jump (`left = last_index[
  ch] + 1`) rather than one position at a time. This is a tiny
  optimization that works because the new left is *known* —
  there's no need to walk it incrementally.

*O(n)* time. Each character is visited at most twice (once by
right, once by left).

## 5. Worked example: longest substring with at most K distinct

> Find the longest substring of `s` containing at most `K`
> distinct characters.

State: a Counter mapping character → count in window.
Constraint: `len(counter) <= K`.

```python
from collections import defaultdict

def longest_k_distinct(s, k):
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

The shrink step removes characters from the left until the
distinct count drops back to K. We `del` the key when its count
reaches 0 so `len(count)` accurately reflects the number of
distinct characters in the window.

The same skeleton handles "fruit into baskets" (at most 2
distinct), "longest substring with at most K replacements,"
and many others.

## 6. The "at most K = exactly K - exactly (K-1)" trick

Some problems ask for **exact** counts: "number of subarrays
with exactly K distinct integers." Sliding window cannot
directly enforce "exactly" — it works on "at most" constraints.

The trick: solve "at most K" twice, and subtract.

```python
def subarrays_exactly_k_distinct(arr, k):
    return at_most(arr, k) - at_most(arr, k - 1)
```

Why does this work? Every "exactly K" subarray is counted in
"at most K" but not in "at most K - 1." Every "at most K - 1"
subarray is counted in both. The difference is exactly the count
of "exactly K" subarrays.

This is one of the prettiest tricks in sliding window. It turns
hard "exactly" problems into easy "at most" sliding windows.

## 7. When sliding window does NOT work

The variable-size sliding window relies on a key property:
**whenever you shrink, the new window is at least as easy to
maintain as the old one's**. If the constraint can be satisfied
by shrinking, the algorithm makes progress.

The pattern breaks down when:

1. **Negative numbers** combined with sum constraints. Growing
   the window doesn't monotonically increase the sum, so "shrink
   until valid" loses its meaning. Use prefix sum + hash instead.
2. **Non-contiguous selections**. Sliding window is for
   *contiguous* substrings/subarrays. If the problem asks for
   non-contiguous (subsequences), the pattern does not apply.
3. **The constraint is not monotonic in window size**. Sliding
   window needs "longer window → harder constraint" (or the
   reverse). If the constraint can be satisfied by a long window
   that fails for a shorter sub-window, the shrink logic breaks.

When sliding window fails, common fallbacks: prefix-sum + hash,
DP, divide-and-conquer.

## 8. Pitfalls

**Pitfall 1: forgetting to update the state on shrink.** When
`left` advances, you must update the state to *remove* `arr[
left]` from the summary. Forgetting this is the most common
sliding-window bug.

**Pitfall 2: returning the answer in the wrong place.** The
window `[left, right]` is valid only **after** the shrink loop.
Update the answer **after** the shrink, not inside it.

**Pitfall 3: confusing "at most" with "exactly."** These are
different problems. Read carefully and use the difference trick
when needed.

**Pitfall 4: trying to slide a window over negative-sum input.**
For "subarray with sum K" on arrays with negatives, sliding
window fails. Use prefix-sum + hash instead.

**Pitfall 5: incorrect length formula.** The window `[left,
right]` (inclusive on both ends) has length `right - left + 1`,
not `right - left`. Fence-post counting.

## 9. End-of-chapter exercise

1. **Maximum average subarray of size K.** Fixed-size window.
   LeetCode 643.
2. **Longest substring without repeating characters.** Already
   covered; reimplement. LeetCode 3.
3. **Longest substring with at most K distinct.** Already
   covered. LeetCode 340.
4. **Minimum window substring.** Shrink as long as the window
   covers all required characters. LeetCode 76.
5. **Subarrays with exactly K different integers.** Use the
   at-most-K minus at-most-(K-1) trick. LeetCode 992.

Do all five. The fifth one is the payoff — once you can apply
the difference trick, you have unlocked a whole sub-family.

## 10. Where to go next

- **Step 10** — the sliding window step in the curriculum has
  more practice problems.
- **Step 11** — sliding-window maximum uses a monotonic deque
  on top of the basic sliding window.
- **Step 9** — monotonic stack/queue, which is sliding window's
  close cousin for "nearest greater / smaller" problems.

Sliding window is a workhorse pattern. It will pay off for years.
Take the time.
''',
}
