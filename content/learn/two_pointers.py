"""Two pointers — when one index isn't enough."""

LESSON = {
    "id": "two-pointers",
    "title": "Two Pointers — One Index Isn't Always Enough",
    "tags": ["two-pointers", "patterns"],
    "summary": (
        "A full beginner chapter. Two indices walking together — "
        "sometimes from opposite ends, sometimes in lockstep, "
        "sometimes at different speeds. The pattern that collapses "
        "many nested-loop solutions into a single pass."
    ),
    "body": r'''
## 0. What this chapter teaches

Two pointers is one of those patterns that, once it clicks,
makes a class of problems suddenly easy. Before it clicks, those
problems look impossible. After, they look mechanical.

This chapter is the friendly tour. We will see the three flavors
of two-pointer (opposite ends, same direction, fast/slow), the
monotonicity argument that makes each correct, and the kinds of
problems that announce themselves as two-pointer candidates.

## 1. The motivating example: pair sum on a sorted array

> Given a sorted array and a target, find any pair of elements
> summing to the target.

Brute force: try every pair. Two nested loops. *O(n²)*.

Two pointers: one at the start, one at the end. Walk inward.

```python
def has_pair(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        s = arr[left] + arr[right]
        if s == target:
            return True
        elif s < target:
            left += 1
        else:
            right -= 1
    return False
```

This is *O(n)*. Each iteration moves exactly one pointer. The
window between them strictly shrinks. So the total iterations are
bounded by `n`.

The reason this works: **monotonicity**. After sorting, if `arr[
left] + arr[right]` is too small, every other pair `(left, k)`
for `k < right` is at most as big, so increasing `left` is the
only productive move. Same logic on the other side.

Without sortedness, we lose monotonicity and the algorithm falls
apart. Hence the prerequisite "sorted array."

## 2. The three flavors of two-pointer

### Flavor A: opposite ends

Two pointers, one at the start, one at the end, walking toward
each other. Use when the array is sorted or when the problem has
symmetric structure.

Examples:
- Pair sum on sorted array.
- Reverse an array in place.
- Container with most water.
- Check palindrome.
- Trapping rain water (two-pointer version).
- 3-Sum (after fixing one element).

### Flavor B: same direction, different rules

Two pointers, both moving rightward, but with different rules for
when they advance. Often used for in-place compaction.

Examples:
- Remove duplicates from sorted array (slow writes, fast reads).
- Move zeros to end.
- Remove element with given value.
- Partition by predicate.

### Flavor C: fast and slow

Both pointers move rightward, but at different speeds (typically
1 and 2). Used for cycle detection and finding middles.

Examples:
- Detect cycle in linked list (Floyd's tortoise and hare).
- Find the middle node of a linked list.
- Find the start of a cycle.
- Find the duplicate number (with the array-as-pointer trick).

Recognize the flavor early. The mechanics differ slightly across
the three, but the discipline (each pointer moves only forward,
bounded by `n`) is the same.

## 3. Worked example: remove duplicates from a sorted array

> Given a sorted array, modify it in place to remove duplicates,
> and return the new length.

Brute force: copy uniques to a new array. *O(n)* time, *O(n)*
space.

Two pointers (flavor B): one pointer tracks "the last unique we
kept" (the **slow** pointer), the other scans the array (the
**fast** pointer).

```python
def remove_duplicates(arr):
    if not arr:
        return 0
    slow = 0
    for fast in range(1, len(arr)):
        if arr[fast] != arr[slow]:
            slow += 1
            arr[slow] = arr[fast]
    return slow + 1
```

The slow pointer marks where the next unique value will be
written. The fast pointer scans for new values. When the fast
finds something different from the most recent unique, the slow
advances and writes the new value into the new slot.

Because the input is sorted, "different from the most recent
unique" = "a brand new value." That single observation is what
makes the algorithm work without an extra hash set.

*O(n)* time, *O(1)* extra space. The classic upgrade from the
brute force.

## 4. Worked example: container with most water

> Given an array of heights, pick two indices to form a
> container. The area is `min(height[i], height[j]) × (j - i)`.
> Maximize the area.

Brute force: every pair. *O(n²)*.

Two pointers (flavor A): start at the widest container — left at
0, right at the end — and shrink intelligently. Move the
**shorter side** inward each step.

```python
def max_area(heights):
    left, right = 0, len(heights) - 1
    best = 0
    while left < right:
        width = right - left
        area = min(heights[left], heights[right]) * width
        best = max(best, area)
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    return best
```

Why move the shorter side? Because moving the taller side cannot
help — the area is bounded by the **shorter** side, so reducing
the taller does nothing for the height, and we lose width.
Moving the shorter side at least has a chance of giving us a
taller new value.

This argument — "moving X can only hurt, moving Y might help" —
is the heart of the two-pointer correctness proof in this kind
of problem. Internalize it.

## 5. Worked example: 3-Sum

> Given an array of integers, find all unique triples summing to
> zero.

Brute force: three nested loops. *O(n³)*.

Two pointers (flavor A inside flavor B):

1. Sort the array.
2. For each index `i`, fix `arr[i]` as the first element.
3. On the suffix `arr[i + 1:]`, run a two-pointer search for a
   pair summing to `-arr[i]`.

```python
def three_sum(arr):
    arr.sort()
    n = len(arr)
    result = []
    for i in range(n - 2):
        if i > 0 and arr[i] == arr[i - 1]:
            continue  # skip duplicate first elements
        target = -arr[i]
        left, right = i + 1, n - 1
        while left < right:
            s = arr[left] + arr[right]
            if s == target:
                result.append([arr[i], arr[left], arr[right]])
                left += 1
                right -= 1
                while left < right and arr[left] == arr[left - 1]:
                    left += 1
                while left < right and arr[right] == arr[right + 1]:
                    right -= 1
            elif s < target:
                left += 1
            else:
                right -= 1
    return result
```

*O(n²)* total — `n` outer iterations each doing an *O(n)*
two-pointer scan. The sort is *O(n log n)*. Net *O(n²)*.

The duplicate-skipping is the fiddly part. It is what turns "all
triples" into "all **unique** triples." Spend the time on it; it
generalizes to 4-Sum and K-Sum.

## 6. When two pointers does NOT work

Two pointers needs **monotonicity in the decision rule**. If,
after moving a pointer, the answer could swing either way
unpredictably, the pattern breaks down.

Examples where two pointers fails:

- Unsorted arrays for pair sum: lose monotonicity, fall back to
  hashing.
- "Longest subarray with sum exactly K" on arrays with negatives:
  growing or shrinking the window changes the sum unpredictably.
  Use prefix-sum + hash instead.
- "Longest subsequence with property P": subsequences are not
  contiguous, two pointers does not apply.

The instinct to develop: ask "is the decision monotonic in the
pointer's direction?". If yes, two pointers. If no, hashing,
sorting, or DP.

## 7. The pitfalls (and their fixes)

**Pitfall 1: forgetting to move a pointer.** A two-pointer loop
that does not advance is an infinite loop. Always end each branch
with `left += 1`, `right -= 1`, or both. If you find a match in
flavor A, advance **both** pointers — otherwise you'd compare
the same match forever.

**Pitfall 2: not handling duplicates.** When a problem asks for
"unique" pairs/triples, you must skip over equal values after
recording a match. The skip is the canonical 3-Sum boilerplate.

**Pitfall 3: confusing two pointers with sliding window.** A
sliding window IS a special case of two same-direction pointers
where the "window" is the range `[left, right]`. We give sliding
window its own chapter because the bookkeeping is distinct.

**Pitfall 4: using two pointers when sortedness is not really
there.** If you're tempted to two-pointer on an unsorted array,
ask yourself whether the monotonicity holds. Often it does not.

**Pitfall 5: incorrect inner-loop boundary.** `while left <
right` is the canonical condition for opposite-end pointers. `<=`
would let the pointers meet at the same element — usually
incorrect, since pairing an element with itself is rarely
allowed.

## 8. End-of-chapter exercise

Solve these five problems with two pointers as the central tool.

1. **Two sum on sorted array.** Already covered; reimplement.
   LeetCode 167.
2. **Valid palindrome (alphanumeric only).** Two pointers from
   the ends, skipping non-alphanumeric. LeetCode 125.
3. **Remove duplicates from sorted array.** Already covered;
   reimplement. LeetCode 26.
4. **Container with most water.** Already covered; reimplement.
   LeetCode 11.
5. **3-Sum.** Already covered; reimplement and verify the
   duplicate-skipping. LeetCode 15.

After all five, two pointers should feel like a reflex.

## 9. Where to go next

- **Step 3** — many medium array problems lean on two pointers.
- **Step 5** — string problems often use two pointers.
- **Step 6** — linked-list problems use the fast/slow flavor a lot.
- **Step 10** — sliding window, the close cousin of same-direction
  two pointers.

Two pointers is one of the small handful of patterns you will use
constantly. Practice the three flavors, the monotonicity
argument, and the duplicate-skipping discipline.
''',
}
