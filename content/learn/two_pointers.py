"""Two pointers — when one index isn't enough."""

LESSON = {
    "id": "two-pointers",
    "title": "Two Pointers — One Index Isn't Always Enough",
    "tags": ["two-pointers", "patterns"],
    "summary": (
        "Two indices walking together — sometimes from opposite ends, "
        "sometimes in lockstep — collapse many nested-loop solutions "
        "into a single pass."
    ),
    "body": r'''
## What problem does it solve?

Suppose you want to find a pair of values in a sorted array that sums
to a target. The naive solution is a double loop: for every left,
try every right. That is *O(n²)*. The two-pointer pattern solves the
same problem in a single *O(n)* pass.

The reason it works is **monotonicity**. If the current left + right
is too small, the left must move right (no smaller right will help).
If it is too big, the right must move left. Each pointer marches
forward only — no backtracking — so the total work is linear.

## Two flavours

### Flavour A: opposite ends

Two pointers, one at the start, one at the end, walking toward each
other. This is the right tool when the array is sorted or when the
problem has symmetric structure.

```python
def has_pair_with_sum(nums: list[int], target: int) -> bool:
    """Assumes nums is sorted."""
    left, right = 0, len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return True
        elif s < target:
            # The sum is too small; we need a bigger value on the left
            # side. The right value is already as big as it can be.
            left += 1
        else:
            # The sum is too big; we need a smaller value on the right.
            right -= 1
    return False
```

Notice how every iteration moves exactly one pointer. The window
between them strictly shrinks. So total iterations are bounded by
`n`. That is the *O(n)* guarantee.

### Flavour B: same direction (fast and slow)

Two pointers both moving left to right, but at different rules or
different speeds. The classic use is "compact in place": one pointer
reads, another writes.

```python
def move_zeros_to_end(nums: list[int]) -> None:
    """Move all zeros to the end, keeping the order of non-zeros."""
    write = 0
    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write], nums[read] = nums[read], nums[write]
            write += 1
```

The `read` pointer scans every element. The `write` pointer marks
"where the next non-zero should go". They advance independently, and
together they compact the array in a single pass.

## Worked example: remove duplicates from a sorted array

> Given a sorted array, remove duplicates **in place**. Return the
> new length.

The brute force is a copy: walk through, push to a new list only when
the value differs from the last one pushed. *O(n)* time, *O(n)*
extra space.

Two pointers do it in place. The slow pointer marks the last unique
position. The fast pointer scans for the next new value.

```python
def remove_duplicates(nums: list[int]) -> int:
    if not nums:
        return 0
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1
```

Read it as a sentence: *"slow is where the latest unique value lives.
When fast finds a new value, slow moves one step right and adopts it.
Otherwise slow stays put."*

## Worked example: container with most water (preview)

This is a famous problem, and two pointers solve it in one pass.
Given heights, pick two indices to form a container; the area is
`min(left_height, right_height) * (right - left)`. The trick: start
with the widest container and shrink intelligently. Move the shorter
side inward — the longer side has slack and moving it inward can only
hurt.

```python
def max_area(heights: list[int]) -> int:
    left, right = 0, len(heights) - 1
    best = 0
    while left < right:
        width = right - left
        area = min(heights[left], heights[right]) * width
        best = max(best, area)
        # Move the shorter side inward — moving the taller side can
        # only make the height the same or shorter while losing width.
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    return best
```

## When two pointers does *not* work

Two pointers requires a monotonic decision rule. If, after moving a
pointer, the answer could go in either direction unpredictably, the
pattern breaks down. In those cases, sliding window or hashing is
usually the right alternative.

If the array is **unsorted** and the problem benefits from sortedness
(like "pair with sum"), you have a choice: sort first (then two
pointers), or use a hash set. Sorting adds *O(n log n)*; hashing adds
*O(n)* extra space. Often the right call depends on whether you also
need to return indices in original order.

## Common beginner mistakes

**Mistake 1: forgetting to move at least one pointer per iteration.**
A two-pointer loop that does not advance is an infinite loop. Always
end each branch with `left += 1` or `right -= 1` (or both, when you
find a match).

**Mistake 2: not handling duplicates when the problem asks for unique
pairs.** After finding a match, skip over equal values to avoid
reporting `(2, 2, 2, 2, ...)`.

**Mistake 3: confusing two pointers with a sliding window.** A sliding
window is a special case of two same-direction pointers where the
"window" is the range `[left, right]`. We cover that pattern in its
own lesson because it has its own bookkeeping.

## The mental model

Two pointers is "walk toward each other (or in lockstep) and use the
fact that one move is enough to learn something new". Whenever you
catch yourself writing a nested loop on a sorted array, pause and
ask: *can I use the sortedness to move only one pointer per step?*
Often the answer is yes.
''',
}
