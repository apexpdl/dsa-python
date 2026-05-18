"""Step 3 — Arrays.

The biggest single lecture in this curriculum. Almost every array
problem boils down to a combination of: walk once, remember
something, use a hash, or sort first.
"""
from __future__ import annotations

PROBLEMS: list[dict] = [
    {
        "id": "largest-element",
        "title": "Largest Element in an Array",
        "step_id": 3,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["arrays", "linear-scan"],
        "understanding": r'''
We have an array of numbers like `[3, 8, 1, 9, 2, 4]`. We want to
return the largest one — in this example, `9`. That is the entire
problem.

It is the first array problem in the sheet for a reason. It teaches
the single most reused pattern in all of array work:

> *Walk through the array once, carrying along "the best so far",
> and update it whenever you see something better.*

Once that move is in your fingers, you have it forever.
''',
        "brute_force": {
            "explanation": r'''
For each element, ask: "is this the largest?". To answer, walk the
entire array and compare. *O(n²)* if you take the question literally.

```python
for i in range(n):
    if all(arr[i] >= arr[j] for j in range(n)):
        return arr[i]
```

Nobody writes this seriously, but it is a useful "wrong" baseline to
contrast with the correct one-pass solution.
''',
            "code": r'''def largest_brute(arr: list[int]) -> int:
    # For each candidate index i, verify it is at least as big as
    # every other element. The first one that passes is the max.
    n = len(arr)
    for i in range(n):
        ok = True
        for j in range(n):
            if arr[j] > arr[i]:
                ok = False
                break
        if ok:
            return arr[i]
    # Defensive return; should not reach here for non-empty arrays.
    raise ValueError("empty array")
''',
            "complexity": (
                "**Time**: *O(n²)* — we re-scan for each candidate.\n\n"
                "**Space**: *O(1)*."
            ),
        },
        "thought_process": r'''
After writing the brute force you immediately notice the wasted
work. We do not need to know "is `arr[i]` the largest?" for every
`i`. We only need the largest overall. So we walk once, carrying
"best so far", and update it whenever we see a bigger value.

The mental model is "tournament": every new element challenges the
current champion. If the challenger is bigger, it becomes the new
champion. After we have walked through everyone, the champion is
the winner.

A subtle detail: we should initialize the champion to something
sensible. Two choices:

1. **Start with `arr[0]`** and loop from index 1. Clean and
   intention-revealing.
2. **Start with `float('-inf')`** and loop from index 0. Also fine,
   handles empty arrays gracefully (returns `-inf`).

Both work. Choice (1) is more common in interviews and more honest
about the precondition that the array is non-empty.
''',
        "optimized": {
            "explanation": r'''
Single pass with a running maximum. *O(n)* time, *O(1)* extra space.
''',
            "code": r'''def largest(arr: list[int]) -> int:
    # Treat the first element as the initial champion.
    best = arr[0]
    # Walk through the rest and replace the champion when challenged.
    for i in range(1, len(arr)):
        if arr[i] > best:
            best = arr[i]
    return best
''',
            "complexity": (
                "**Time**: *O(n)*. **Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
"Walk once and track the best so far" is the kernel of an immense
family of array problems. Some examples on this very sheet:

- **Second largest** — track two best-so-far values.
- **Max consecutive ones** — track the current run and the best run.
- **Stock buy/sell** — track the minimum price so far and the max
  profit so far.
- **Maximum subarray sum (Kadane)** — track the best subarray
  ending here and the best overall.

The common structure: as you walk, you carry one or two scalars that
summarize "everything seen so far". The output is one of those
scalars at the end.

When you start solving harder problems, you will find that the
biggest difficulty is **choosing what to carry**. "What single
number captures everything I need to know about the prefix I have
seen so far?" — that is the central question. For "largest", the
answer is obvious: the largest value seen. For Kadane, the answer
takes some thought. For longest-consecutive-sequence, the answer
involves a hash. But the shape is the same.
''',
        "summary": r'''
**Pattern**: linear scan with a running scalar.

**Lesson**: the simplest array problem teaches the most reused
move. Walk once, carry a summary, return it.

**Recognize next time**: anywhere "find the maximum / minimum /
longest / smallest" applies. Always reach for the single-pass
running-scalar pattern first.
''',
    },
    {
        "id": "second-largest-element",
        "title": "Second Largest Element (No Sorting)",
        "step_id": 3,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["arrays", "linear-scan"],
        "understanding": r'''
Find the second-largest distinct value in the array. For
`[3, 8, 1, 9, 2, 4]` the answer is `8`. For `[5, 5, 5]` there is no
second-largest (only one distinct value); we typically return `-1`
or `None`.

The "no sorting" constraint is the whole point. Sorting would solve
the problem in *O(n log n)* trivially. The challenge is to do it in
**one pass**, *O(n)*, with a few constant slots of memory.
''',
        "brute_force": {
            "explanation": r'''
**Two passes**: first pass finds the largest. Second pass finds the
largest among elements not equal to the global largest. Correct and
*O(n)*, but requires two scans. We can do better with one.

```python
biggest = max(arr)
second = -1
for x in arr:
    if x != biggest and x > second:
        second = x
```
''',
            "code": r'''def second_largest_two_pass(arr: list[int]) -> int:
    # First pass: find the actual largest.
    biggest = arr[0]
    for x in arr:
        if x > biggest:
            biggest = x
    # Second pass: find the largest value strictly less than biggest.
    second = -1
    for x in arr:
        if x < biggest and x > second:
            second = x
    return second
''',
            "complexity": (
                "**Time**: *O(n)* but two passes. **Space**: *O(1)*."
            ),
        },
        "thought_process": r'''
The single-pass version asks: can we maintain "largest" and "second
largest" *simultaneously* as we walk?

Yes. We hold two variables. When a new element arrives, three cases:

1. It is larger than `largest`. The current `largest` is dethroned
   — it now becomes the new `second`. The newcomer becomes
   `largest`.
2. It is between `largest` and `second`. It dethrones `second` only.
3. It is no bigger than `second`. We ignore it.

Read those three cases slowly. Many beginners forget case 1 — they
update `largest` without saving the old `largest` into `second`,
and the algorithm silently produces wrong answers. The trap is so
common it is worth practicing on paper once.

Edge cases to think about: duplicates of the largest value should
not count as a "second largest". If the array is all equal, there
is no second largest and we return `-1`. Our implementation handles
both correctly because we use strict `>` for the "dethrone largest"
case and exclude equality in the "dethrone second" case.
''',
        "optimized": {
            "explanation": r'''
A single pass maintaining both `largest` and `second`.
''',
            "code": r'''def second_largest(arr: list[int]) -> int:
    # Sentinels: a value lower than any expected input. -inf works
    # universally but for typical int arrays a large negative is fine.
    largest = float("-inf")
    second = float("-inf")
    for x in arr:
        if x > largest:
            # x is the new champion; demote the old champion.
            second = largest
            largest = x
        elif x < largest and x > second:
            # x slots between the two; replace second.
            second = x
    # If second never moved, the array had no second-largest value.
    if second == float("-inf"):
        return -1
    return int(second)
''',
            "complexity": (
                "**Time**: *O(n)* single pass. **Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
The deep idea: when you need the **top K** of something, you
maintain a structure of size K and update it as you scan. For
K = 2, two variables suffice. For larger K, you typically use a
**min-heap of size K**: when you see a new element, push it; if the
heap is larger than K, pop the smallest. That keeps the heap as the
"best K so far". This generalizes to "top K largest", "top K most
frequent", and other heap problems in Step 11.

The single-pass habit also matters operationally. In a streaming
setting (data arrives one item at a time and you cannot rewind), a
two-pass algorithm is impossible. The "carry top-K so far" pattern
is the only viable approach.
''',
        "summary": r'''
**Pattern**: maintain top-K best-so-far as you scan.

**Lesson**: when promoting a new champion, demote the old champion
carefully. Missing the demote step is the classic bug.

**Recognize next time**: "top K largest/smallest/most frequent" of
a stream — two variables for K = 2, a heap for general K.
''',
    },
    {
        "id": "remove-duplicates-sorted",
        "title": "Remove Duplicates from a Sorted Array",
        "step_id": 3,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["arrays", "two-pointers", "in-place"],
        "understanding": r'''
We have a **sorted** array like `[1, 1, 2, 2, 3, 4, 4]` and we need
to remove duplicates **in place**. The output array should contain
each distinct value exactly once, kept in sorted order:
`[1, 2, 3, 4, _, _, _]`. We return the new length `k = 4`; the tail
of the array can hold anything (the problem usually does not care).

Two things to pay attention to:

1. **The input is sorted.** That single fact unlocks a slick
   *O(n)* in-place solution. Duplicates of any value must sit next
   to each other.
2. **In place.** No allocating a brand new array. We modify the
   given one and return the new length.
''',
        "brute_force": {
            "explanation": r'''
A simple non-in-place approach uses a set:

```python
return sorted(set(arr))
```

It is correct, but it loses the in-place property and is *O(n log n)*
or *O(n)* depending on details. For interview purposes the in-place
version is the canonical answer.
''',
            "code": r'''def remove_dups_set(arr: list[int]) -> int:
    # Build a sorted list of unique values, then write them back
    # into the front of arr in place.
    uniques = sorted(set(arr))
    for i, v in enumerate(uniques):
        arr[i] = v
    return len(uniques)
''',
            "complexity": (
                "**Time**: *O(n log n)* due to sorting the set. "
                "**Space**: *O(n)* for the set."
            ),
        },
        "thought_process": r'''
Because the input is **sorted**, duplicates are guaranteed to be
adjacent. That means we can detect a duplicate by comparing each
element with its immediate predecessor. If they differ, we have a
new unique value.

This is the **slow-and-fast pointer** pattern. `slow` is the index
where the next unique value should be written; `fast` is the index
we are currently reading from. When the value at `fast` is new (i.e.
different from the value at `slow`), we advance `slow` and copy it
in. Otherwise we ignore `fast` and keep moving.

Read the pattern once more:

- `slow` points to the last unique value we kept.
- `fast` walks through everything.
- When `arr[fast] != arr[slow]`, we have a fresh unique value;
  promote `slow` by one and overwrite.

By the end, `slow + 1` is the count of unique values, and the front
of the array `arr[0..slow]` is the deduplicated content.

This pattern — slow pointer for "where to write", fast pointer for
"where to read" — is one of the most reused moves in array
problems. It shows up in "move zeroes to end", "remove element", and
"sort 0s/1s/2s".
''',
        "optimized": {
            "explanation": r'''
Two pointers walking the array once. *O(n)* time, *O(1)* extra
space.
''',
            "code": r'''def remove_duplicates(arr: list[int]) -> int:
    # An empty array trivially has zero unique elements.
    if not arr:
        return 0
    # slow points to the last index that holds a confirmed unique value.
    slow = 0
    # fast walks through the rest of the array.
    for fast in range(1, len(arr)):
        # If arr[fast] differs from the most-recent unique, it is a
        # new unique value.
        if arr[fast] != arr[slow]:
            slow += 1                 # reserve the next slot
            arr[slow] = arr[fast]     # write the new unique there
    # Number of unique elements = slow + 1 (because we are 0-indexed).
    return slow + 1
''',
            "complexity": (
                "**Time**: *O(n)*. **Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
The deep idea is **the slow pointer is a write head**. We use it to
compact the array in place by overwriting the duplicates. Because
the input is sorted, the front of the array stays valid the entire
time — we never overwrite something we still need to read, because
slow ≤ fast always.

The general pattern: any time the problem says "remove all X from
the array in place" or "compact the array", reach for slow/fast. The
question becomes: "what is the condition under which I keep an
element?". Here it is "different from the previous kept value".
Elsewhere it might be "nonzero" (move zeroes), "doesn't equal val"
(remove element), or "satisfies predicate".

A nice variation: **at most twice** instead of "at most once". We
keep a count of how many times the current value has been kept, and
allow up to two. The slow/fast structure is identical; only the
"keep?" condition changes.
''',
        "summary": r'''
**Pattern**: slow/fast pointer for in-place compaction on a sorted
array.

**Lesson**: sortedness puts duplicates next to each other, so a
single comparison detects them. The slow pointer marks where to
write; the fast pointer marks where to read.

**Recognize next time**: any in-place array compaction. The general
pattern is `for fast: if keep(arr[fast]): slow += 1; arr[slow] = arr[fast]`.
''',
    },
    {
        "id": "max-consecutive-ones",
        "title": "Maximum Consecutive Ones",
        "step_id": 3,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["arrays", "linear-scan"],
        "understanding": r'''
Given a binary array (only 0s and 1s) like `[1, 1, 0, 1, 1, 1, 0, 1]`,
find the length of the longest run of consecutive 1s. The answer for
that example is `3` (the run `1, 1, 1` in the middle).

This is one of the cleanest examples of the running-scalar pattern,
with a small twist: we maintain *two* running scalars — the current
run length and the best run length seen so far.
''',
        "brute_force": {
            "explanation": r'''
For each starting index, scan forward as long as we see 1s and count
the run. Record the longest. This is *O(n²)* worst case (mostly 1s)
and we can do better with one pass.
''',
            "code": r'''def max_ones_brute(arr: list[int]) -> int:
    n = len(arr)
    best = 0
    # For each start, count the run of 1s.
    for i in range(n):
        run = 0
        j = i
        while j < n and arr[j] == 1:
            run += 1
            j += 1
        if run > best:
            best = run
    return best
''',
            "complexity": (
                "**Time**: *O(n²)* worst case. **Space**: *O(1)*."
            ),
        },
        "thought_process": r'''
The brute force wastes time by restarting the run count for each
starting index. But there is no need to restart. We can maintain
a single running count as we walk:

- When we see a 1, increment the current run.
- When we see a 0, reset the current run to 0.
- At every step, update the best with the current run.

That is it. One pass, two scalars.

The mental model is "current streak vs all-time record". The
algorithm is exactly how a sports broadcaster would narrate: the
current streak goes up while the team wins, resets on a loss, and
the record updates whenever the current streak exceeds it.
''',
        "optimized": {
            "explanation": r'''
Single pass with two scalars: current run and best run.
''',
            "code": r'''def max_consecutive_ones(arr: list[int]) -> int:
    best = 0          # longest run seen so far
    current = 0       # length of the run we are currently inside
    for x in arr:
        if x == 1:
            # Extend the current run by one.
            current += 1
            # Update the all-time record if we just broke it.
            if current > best:
                best = current
        else:
            # The run ends here; reset the counter.
            current = 0
    return best
''',
            "complexity": (
                "**Time**: *O(n)*. **Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
The "current streak vs record" pattern is one of the cheapest and
most reused tricks in array work. A surprising number of problems
are this same shape with a slightly different reset condition:

- **Max consecutive ones** — reset on 0.
- **Longest substring with at most K zeroes** — reset is more
  subtle and uses sliding window.
- **Maximum subarray sum** (Kadane) — reset is "if current sum
  drops below zero, reset to 0".
- **Longest increasing run** — reset is "if `arr[i] <= arr[i-1]`,
  reset to 1".

You will see the same `current` / `best` pair across many array
problems. Get to know the rhythm: extend on a positive signal,
reset on a negative signal, always update the best.
''',
        "summary": r'''
**Pattern**: current streak + all-time record.

**Lesson**: don't restart counts when you can extend them. Two
scalars, one pass, *O(n)*.

**Recognize next time**: any "longest run / streak / consecutive"
problem. The reset condition is the only thing that changes.
''',
    },
    {
        "id": "single-number",
        "title": "Find the Number That Appears Once (Others Twice)",
        "step_id": 3,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["arrays", "xor", "bit-manipulation"],
        "understanding": r'''
We have an array where every integer appears **exactly twice**,
except one integer that appears exactly **once**. Find the loner.

Example: `[2, 3, 5, 4, 5, 3, 4]` — the loner is `2`.

The hashing solution is obvious. The optimized solution is one of
the prettiest tricks in all of beginner DSA: **XOR everything
together, and the answer drops out**.
''',
        "brute_force": {
            "explanation": r'''
Count frequencies with a hash map; return the value whose count is
1. *O(n)* time, *O(n)* space.

```python
from collections import Counter
[k for k, v in Counter(arr).items() if v == 1][0]
```

Correct and simple. The XOR solution improves the **space** to
*O(1)*, which is the real prize.
''',
            "code": r'''def single_number_hash(arr: list[int]) -> int:
    from collections import Counter
    counts = Counter(arr)
    for k, v in counts.items():
        if v == 1:
            return k
    raise ValueError("no unique element found")
''',
            "complexity": (
                "**Time**: *O(n)*. **Space**: *O(n)* for the counter."
            ),
        },
        "thought_process": r'''
The leap to the XOR solution requires knowing **three properties of
XOR**:

1. **XOR is commutative and associative.** `a ^ b == b ^ a` and
   `(a ^ b) ^ c == a ^ (b ^ c)`. So the order in which you XOR a
   list of numbers does not matter.
2. **`x ^ x == 0`.** XOR-ing a number with itself produces zero.
3. **`x ^ 0 == x`.** XOR-ing a number with zero leaves it unchanged.

Now imagine XOR-ing every element of the array together. Because
order does not matter, we can mentally pair up the duplicates.
Every pair contributes `x ^ x == 0` to the final result. The loner
has no partner, so it contributes itself. The final XOR is
`0 ^ 0 ^ ... ^ loner == loner`.

That is the entire algorithm. One pass, one variable.

When does this work? Whenever the "duplicates" are exact pairs.
There are gorgeous variations:

- **Every value appears three times except one** — needs a
  different trick (counting bits modulo 3).
- **Two unique values, others appear twice** — XOR everything, then
  split by a bit position where the two unique values differ.

Step 8 covers these. For now, the basic XOR trick is the headliner.
''',
        "optimized": {
            "explanation": r'''
XOR all elements together. The duplicates cancel out; only the
loner survives.
''',
            "code": r'''def single_number(arr: list[int]) -> int:
    # Start with 0 because x ^ 0 == x.
    result = 0
    # XOR every element. Duplicates cancel to zero in pairs; the loner
    # has no partner and stays.
    for x in arr:
        result ^= x
    return result
''',
            "complexity": (
                "**Time**: *O(n)*. **Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
XOR is *bit-by-bit* "are these two bits different?". The
self-cancellation property comes from the fact that any bit XORed
with itself is 0. So XOR-ing a list of values is, at each bit
position, asking "did this bit appear an odd number of times?". For
pairs the answer is always "even, so 0". For the loner the answer is
whatever its own bit is.

This is the foundation for several beautiful algorithms:

- **Detecting differences** between two arrays. XOR them together;
  the result is the XOR of the differing elements.
- **Finding the missing number 1..n**. XOR `1..n` and the array
  together; everything cancels except the missing number.
- **Encoding pair sums** in O(1) — useful in tricky bit-trick problems.

XOR feels like magic the first time you see it, then like a tool the
tenth time you see it. Get comfortable.
''',
        "summary": r'''
**Pattern**: XOR as "cancel out the pairs".

**Lesson**: when duplicates appear in pairs and you want O(1)
space, XOR is the answer. The three core properties are
commutativity, `x ^ x == 0`, and `x ^ 0 == x`.

**Recognize next time**: "every element appears N times except one"
problems. Pairs → XOR. Triples → bit-counting mod 3. Two singles
in pairs → XOR + split by bit.
''',
    },
    {
        "id": "missing-number",
        "title": "Find the Missing Number",
        "step_id": 3,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["arrays", "math", "xor"],
        "understanding": r'''
We are given an array of size `n` that contains `n` distinct numbers
from the range `[0, n]`. Exactly one number from that range is
missing. Find it.

Example: for `n = 4` and array `[3, 0, 1]`, the missing number is
`2` (because we expected `0, 1, 2, 3` but only saw `0, 1, 3`).

Three solutions of increasing cleverness solve this:

1. **Hashing** — store the seen set, then walk `0..n` looking for
   the absentee.
2. **Sum formula** — the sum of `0..n` is `n(n+1)/2`. Subtract the
   sum of the array. The difference is the missing number.
3. **XOR** — XOR `0..n` together, then XOR every element of the
   array; everything cancels except the missing one.

All three are *O(n)*. The sum and XOR approaches are *O(1)* space.
''',
        "brute_force": {
            "explanation": r'''
Hash-set approach: put every element in a set, then scan 0..n.

```python
seen = set(arr)
for i in range(n + 1):
    if i not in seen:
        return i
```

Correct and intuitive but uses *O(n)* extra memory.
''',
            "code": r'''def missing_set(arr: list[int]) -> int:
    seen = set(arr)
    n = len(arr)
    # The expected values are 0..n (inclusive), and exactly one is missing.
    for i in range(n + 1):
        if i not in seen:
            return i
    # Should not get here if the problem's promise holds.
    raise ValueError("no missing number found")
''',
            "complexity": (
                "**Time**: *O(n)*. **Space**: *O(n)*."
            ),
        },
        "thought_process": r'''
The sum trick comes from a tiny piece of math: the sum
`0 + 1 + 2 + ... + n` equals `n(n + 1) / 2`. That formula was first
written down (according to legend) by a very young Carl Gauss. We
do not need to know its history; we just need to know it.

So **expected_sum** = `n(n + 1) / 2`, where `n` is the largest
possible value. **actual_sum** = `sum(arr)`. The missing number is
`expected_sum - actual_sum`. One line of arithmetic.

There is one trap to avoid: **integer overflow**. In Python this is
a non-issue, but in C++/Java with 32-bit ints, `n(n + 1) / 2` can
overflow for large `n`. The XOR version sidesteps that completely
because XOR does not grow the bit width.

The XOR version uses the same idea as "single number": pair the
array's values with the indices 0..n. Each pair (value, same value
in the index range) cancels. The missing index has no partner and
survives.
''',
        "optimized": {
            "explanation": r'''
Both the sum and XOR approaches work in *O(n)* time and *O(1)*
space. The sum approach is the most beginner-friendly. The XOR
approach is overflow-proof.
''',
            "code": r'''def missing_number_sum(arr: list[int]) -> int:
    n = len(arr)
    # Gauss formula: expected sum of 0..n inclusive.
    expected = n * (n + 1) // 2
    # Subtract what we actually saw; the difference is what's missing.
    return expected - sum(arr)


def missing_number_xor(arr: list[int]) -> int:
    n = len(arr)
    result = 0
    # XOR all integers 0..n (the expected set).
    for i in range(n + 1):
        result ^= i
    # XOR all elements of arr (the actually-present set).
    for x in arr:
        result ^= x
    # Everything present in both cancels; what remains is the missing one.
    return result
''',
            "complexity": (
                "**Time**: *O(n)*. **Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
Both clever solutions use the same principle: **encode the expected
state in O(1), then "remove" the actual state, and what is left is
the difference**. The sum approach uses arithmetic (subtract). The
XOR approach uses XOR (which is its own inverse). Both are clean
ways to compute "set difference" without storing the set.

This trick generalizes powerfully. Need to find **two** missing
numbers from a range? XOR everything; the result is the XOR of the
two missing numbers. Then split by a differing bit to recover them
individually. That is one of the hidden gems of Step 8.

Need to find a **repeating** number in a 1..n array where exactly
one repeats? Use a Floyd cycle on the array-as-pointer interpretation,
or use sum/XOR with adjustments. There is a whole family.
''',
        "summary": r'''
**Pattern**: encode the expected total (sum or XOR), subtract the
actual, recover the difference.

**Lesson**: O(1) memory + arithmetic invariants can replace a hash
set in many "find the missing / extra / odd-one-out" problems.

**Recognize next time**: any "exactly one is different from the
expected set" question. Sum, XOR, or product invariants are usually
the path.
''',
    },
    {
        "id": "longest-subarray-with-sum-k",
        "title": "Longest Subarray with Sum K",
        "step_id": 3,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["arrays", "prefix-sum", "hashing", "sliding-window"],
        "understanding": r'''
Find the length of the **longest contiguous subarray** whose sum
equals a target `K`. The array may contain positives, negatives, and
zeros.

Example: `[1, -1, 5, -2, 3]`, `K = 3` → the longest subarray summing
to 3 is `[1, -1, 5, -2]`, of length 4.

A "subarray" must be contiguous — no skipping. That contiguity is
the whole game. It rules out greedy "skip the bad ones" tricks and
points us at two beautiful patterns: **sliding window** (for
non-negative arrays) and **prefix sums with hashing** (the general
case).

We will discuss both.
''',
        "brute_force": {
            "explanation": r'''
Try every subarray, sum it, track the longest matching length. Two
nested loops: outer for the start, inner for the end.

A small optimization: keep a running sum for each start, so the
inner loop adds one element at a time instead of re-summing.

```python
best = 0
for i in range(n):
    s = 0
    for j in range(i, n):
        s += arr[j]
        if s == K:
            best = max(best, j - i + 1)
```

This is *O(n²)*. With careful pruning it can sometimes be
worthwhile, but for general arrays we want better.
''',
            "code": r'''def longest_subarray_sum_k_brute(arr: list[int], k: int) -> int:
    n = len(arr)
    best = 0
    # Outer loop fixes the start index.
    for i in range(n):
        # Inner loop extends the end index, maintaining a running sum.
        s = 0
        for j in range(i, n):
            s += arr[j]
            if s == k:
                best = max(best, j - i + 1)
    return best
''',
            "complexity": (
                "**Time**: *O(n²)*. **Space**: *O(1)*."
            ),
        },
        "thought_process": r'''
The key idea behind the optimized approach is the **prefix sum**.
Define `prefix[i]` = sum of `arr[0..i - 1]`. So `prefix[0] = 0`,
`prefix[1] = arr[0]`, `prefix[2] = arr[0] + arr[1]`, and so on.

The sum of the subarray `arr[i..j]` (inclusive on both ends) equals
`prefix[j + 1] - prefix[i]`. That single identity transforms
"sum of every subarray" from *O(n²)* into *O(n)*-with-a-hash.

We want subarrays whose sum is `K`. Using the identity:
`prefix[j + 1] - prefix[i] == K`, equivalently
`prefix[i] == prefix[j + 1] - K`.

So as we scan and compute prefix sums, we ask at each step: *"have
I previously seen a prefix sum equal to `current_prefix - K`?"* If
yes, the subarray between that earlier index and the current one
sums to K. We want the **longest**, so we record the **earliest**
index at which each prefix sum first appeared.

This pattern — "as I scan, ask a question about earlier prefix sums
using a hash" — is one of the heaviest hitters in array DSA. It is
the optimized version of subarray sum equals K, count of subarrays
with sum K, longest subarray with zero sum, count of subarrays with
XOR K, and many more.

For arrays of **non-negative integers**, there is a simpler
**sliding window** approach because the prefix sum is
monotonically non-decreasing. We discuss it for completeness, but
the prefix-sum-with-hash approach is the general solution.
''',
        "optimized": {
            "explanation": r'''
Walk the array maintaining a running prefix sum. Use a dict that
maps prefix sums to their **earliest** index. At each step, check
whether `prefix - K` has been seen; if so, the length is `i -
earliest_index_of_that_prefix`.
''',
            "code": r'''def longest_subarray_sum_k(arr: list[int], k: int) -> int:
    # first_index[s] = the earliest index i such that prefix[i] == s.
    # We seed it with prefix sum 0 at index -1 (the empty prefix sits
    # "before" index 0). That handles subarrays that start at index 0.
    first_index = {0: -1}
    prefix = 0
    best = 0
    for i, x in enumerate(arr):
        prefix += x
        # If prefix - k appeared earlier at some index j, then
        # arr[j + 1 .. i] sums to k.
        if prefix - k in first_index:
            best = max(best, i - first_index[prefix - k])
        # Only record THIS prefix sum if it is new — we want the
        # earliest occurrence to maximize length.
        if prefix not in first_index:
            first_index[prefix] = i
    return best
''',
            "complexity": (
                "**Time**: *O(n)*. **Space**: *O(n)* for the hash."
            ),
        },
        "deep_concept": r'''
Prefix sums turn "range sum queries" into "point subtractions". Once
you internalize that, an enormous class of problems become tractable.

The pattern's full skeleton, which you should commit to memory:

1. Compute prefix sums on the fly as you scan.
2. As you compute each new prefix, ask one or both of:
   - "Has this exact prefix appeared before?" (zero-sum subarrays)
   - "Has prefix - K appeared before?" (sum-K subarrays)
   - "Has the XOR-equivalent appeared before?" (subarray XOR
     problems)
3. Store either the first or count of occurrences in a hash.

The "first index" version computes the **longest** matching
subarray. The "count of occurrences" version computes **how many**
matching subarrays exist. Same prefix sum trick; different bookkeeping.

For **non-negative arrays**, there is the cheaper sliding window:
maintain a window `[left, right]` with running sum; if the sum
exceeds K, advance `left`; if it equals K, record the length. This
is *O(n)* with *O(1)* space — better when applicable. The prefix
sum approach is the *general* solution that handles negatives too.
''',
        "summary": r'''
**Pattern**: prefix sum + hash map.

**Lesson**: range sums become point subtractions in the prefix sum
world. The question "is there a subarray summing to K ending here?"
becomes "have I seen `prefix - K` before?".

**Recognize next time**: any subarray-sum question. Some variants:
count of subarrays with sum K, longest with sum K, presence with
sum K, XOR variants, divisible by M variants. The prefix-sum-hash
pattern handles them all.
''',
    },
    {
        "id": "two-sum",
        "title": "Two Sum",
        "step_id": 3,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["arrays", "hashing", "two-pointers"],
        "what_this_teaches": (
            "The most reused idea in all of array DSA: trade memory for "
            "time by remembering what you have already seen. Two Sum is "
            "the cleanest possible demonstration that a hash map can "
            "collapse a nested loop into a single pass."
        ),
        "pattern": "Hash the past; query the complement for each new element.",
        "prerequisite_lessons": ["arrays", "hashing"],
        "prerequisite_problems": ["count-frequencies"],
        "next_problems": [
            "three-sum",
            "four-sum",
            "longest-subarray-with-sum-k",
            "subarrays-with-sum-k",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 3 (Medium Arrays)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 1 — Two Sum",
                "url": "https://leetcode.com/problems/two-sum/",
            },
            {
                "label": "Python docs — dict",
                "url": "https://docs.python.org/3/library/stdtypes.html#dict",
            },
        ],
        "understanding": r'''
Let's slow down and really see what is being asked.

You are handed an array of integers and one target number. Your job
is to find two elements in the array whose **sum** equals the
target, and return their indices. The problem promises that exactly
one such pair exists, and you are not allowed to use the same index
twice — that is, you cannot pair an element with itself.

For example, with `nums = [2, 7, 11, 15]` and `target = 9`, the
answer is `(0, 1)`, because `nums[0] + nums[1] = 2 + 7 = 9`. With
`nums = [3, 2, 4]` and `target = 6`, the answer is `(1, 2)`,
because `nums[1] + nums[2] = 2 + 4 = 6`. Notice that we report
the **indices**, not the values themselves.

Read the problem one more time with a beginner's eye and notice
two subtleties that trip people up.

First: the array is not sorted. We cannot binary search. We cannot
walk inward from the ends. Whatever algorithm we use has to work on
a jumbled list.

Second: the problem asks for *any* valid pair (since exactly one
exists), and it asks for *indices*, not values. That second detail
is the reason we will reach for a dictionary that maps **value →
index** rather than just a set of values. A set would tell us "yes,
the partner exists somewhere," but we want to actually *return*
where. A dict gives us both: presence *and* position.

Two Sum is famous not because it is hard — once you see the trick
it is almost embarrassingly simple — but because it is the
**textbook moment** when a beginner first feels in their bones the
power of using extra memory to shortcut time. After Two Sum, the
sentence *"I could remember what I have already seen"* turns into a
reflex. That reflex unlocks 3-Sum, 4-Sum, subarray sums, longest
substring without repeating, and a long tail of medium / hard
problems.
''',
        "brute_force": {
            "explanation": r'''
Try every pair of indices. For each `i`, scan all `j > i` looking
for `arr[i] + arr[j] == target`. Two nested loops, *O(n²)*.
''',
            "code": r'''def two_sum_brute(arr: list[int], target: int) -> tuple[int, int] | None:
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] + arr[j] == target:
                return (i, j)
    return None
''',
            "complexity": (
                "**Time**: *O(n²)*. **Space**: *O(1)*."
            ),
        },
        "thought_process": r'''
Watch yourself solve this problem on paper for `nums = [2, 7, 11,
15]`, `target = 9`. The very natural first move is to point at
`2` and ask, *"what would I have to add to this to get 9?"* The
answer is `7`. You scan forward, find `7`, done. Now point at `7`
and ask the same question — the answer is `2`, and you remember
you just walked past it.

That little inner monologue is the **whole algorithm**. Every step
boils down to:

1. Look at the current element `x`.
2. Compute the **complement**: `target - x`. That is the partner
   we would need.
3. Ask: have I already seen the complement somewhere earlier in
   the array? If yes, we have our pair. If not, file `x` away in
   memory and move on.

The brute force version does step 3 by re-scanning the array. That
re-scan is what makes the brute force *O(n²)*: for each starting
element, we look at every later element again, repeating work we
could have done once.

The optimization is to make step 3 *O(1)*. A dictionary (or hash
map) does exactly that. We keep a dict that maps "every value we
have already seen" → "the index where we saw it". When we look at
a new element `x`, we compute its complement and ask the dict in
constant time, "do you remember seeing this value?" If yes, the
answer is the stored index plus the current one. If no, we add
`x` to the dict and continue.

This compresses two passes (build the dict, then query it) into a
**single** pass, because at the moment we look at `nums[i]`, the
dict already contains exactly the right set of candidates — every
element strictly to the left of `i`. We never accidentally pair an
element with itself, because we **check the dict before inserting
the current element**. The order matters.

A small mental model that helps: imagine you are walking through
the array left to right, carrying a notebook. The notebook is your
dict. Every time you see a new number, you do two things in this
exact order — *first ask* "is my complement already in the
notebook?", *then write down* my own number so future steps can
ask about me. Check, then file. Check, then file. That is the
loop, and that is why it works in one pass.

One last beautiful detail: this trick generalizes. The instant you
catch yourself writing "for each element, look at every other
element," ask whether a hash of "what I have already seen" could
turn the inner loop into a single dictionary lookup. The answer is
*yes* embarrassingly often.
''',
        "optimized": {
            "explanation": r'''
Walk once. Maintain a dict from value to index. For each new
element, check whether `target - current` is in the dict.
''',
            "code": r'''def two_sum(arr: list[int], target: int) -> tuple[int, int] | None:
    # seen[value] = first index at which `value` was encountered.
    seen: dict[int, int] = {}
    for i, x in enumerate(arr):
        partner = target - x
        # If we've seen `partner` before, we have our pair.
        if partner in seen:
            return (seen[partner], i)
        # Otherwise record the current value for future lookups.
        # Note: we record AFTER the check, so we never pair an
        # element with itself.
        seen[x] = i
    return None
''',
            "complexity": (
                "**Time**: *O(n)*. **Space**: *O(n)* for the hash."
            ),
        },
        "deep_concept": r'''
Step back from the code and look at the deeper move.

We started with a question that *sounds* relational — "find two
things that interact" — and turned it into a question that is
**personal**: at each element, given only the element and a
notebook of the past, can I decide? The dictionary did the
relational work for us by encoding "I have seen these values
before" as a constant-time check.

That conversion — from "for every pair, ask a question" to "for
every element, ask the past one question" — is the deeper move
behind almost every "hash trick" in DSA. Once you can spot it, you
can do it on your own:

- **Subarray sum equals K** — running prefix sum + hash of "which
  prefix sums have I seen?". For each new prefix, ask "have I
  seen `prefix - K` before?". Same shape as Two Sum.
- **Longest substring without repeating characters** — hash of
  "last index of each character." For each new character, ask
  "is the last index of this character inside my window?".
- **Group anagrams** — hash from canonical form to list of
  members.
- **Pair sum in a binary search tree** — same as Two Sum but
  iterating the tree in order.

The unifying principle: a hash gives you *O(1)* "have I seen this
before?" lookups. Whenever a problem can be re-cast so that each
new element needs to ask exactly one such question, the hash will
collapse a nested loop into a single pass.

Two Sum also has a beautiful **alternative** solution when the
array is sorted (or you sort it first): the two-pointer sweep.
Left at index 0, right at the end. If `nums[left] + nums[right]`
is too small, move left right; if too big, move right left; if
equal, you have your pair. *O(n)* time, *O(1)* space — better
memory than hashing, at the cost of *O(n log n)* up-front sorting.
This trade-off — "more memory vs. more comparisons" — is one you
will see in many problems. Pick the right tool for the specific
constraints.
''',
        "confusion_notes": [
            {
                "question": "Why do we check the dict *before* inserting the current value?",
                "answer": r'''
This is the most common bug when writing Two Sum, and the answer
gets at a subtle correctness invariant.

The line order matters. Our algorithm goes:

```python
for i, x in enumerate(arr):
    partner = target - x
    if partner in seen:        # check first
        return (seen[partner], i)
    seen[x] = i                # then insert
```

If we flipped the order — insert first, then check — and an
element happened to equal exactly half the target, we would
"find" it pairing with itself. For example, `arr = [3, 4, 5]`,
`target = 6`. The element `3` has complement `3`. If we inserted
first, the dict would contain `{3: 0}`, then we would look up
`3` in the dict, find ourselves, and return the pair `(0, 0)`.
But the problem forbids using the same index twice. The pair `(0,
0)` is wrong.

By checking *before* inserting, the dict at the moment of the
check contains **only elements strictly to the left** of the
current index. So when we find a partner, it must live at an
earlier index. The invariant is "the dict holds the past, not
the present." That invariant is the entire correctness argument.

A close cousin of this question is "what if the same value appears
twice in the array?" Try `arr = [3, 3]`, `target = 6`. On `i = 0`,
the dict is empty, so `partner = 3` is not there. We insert
`{3: 0}` and move on. On `i = 1`, we compute `partner = 3` and
find it in the dict with value `0`. We return `(0, 1)`. Correct.
The check-then-insert order naturally handles duplicates because
the previous occurrence is already in the dict by the time we get
to the second one.
''',
            },
            {
                "question": "Why store the index instead of just `True` for each seen value?",
                "answer": r'''
Because the problem asks us to return **indices**, not just to
confirm that a pair exists.

If we used a set (just storing values), the algorithm would tell
us "yes, a partner exists," but we would have no way to report
*where* the partner lives. We would either have to do a second
pass to find it, or restructure the loop.

The dict lets us do both with one structure: the **key** is the
value (so we can ask "have I seen this value?"), and the **value
in the dict** is the index (so when we get a hit, we know where).
Same lookup cost, more information per lookup.

A subtle bonus: if the same value appears in the array multiple
times, the dict stores the **most recent** index (or the
**first**, depending on whether you overwrite). For Two Sum it
does not matter — any valid pair works. But for related problems
("longest substring without repeating characters," for example),
you specifically want the last index, and that is what the dict
naturally gives you when you assign on every iteration.

Mental model: a set is a guest list (just names); a dict is a
guest list with seating chart (names and table numbers). For Two
Sum we need the table number, not just the name.
''',
            },
            {
                "question": "Why does this work in a single pass? Doesn't the partner need to come *after* the current element?",
                "answer": r'''
This is a beautiful subtlety. The answer is that **for every
valid pair, one of the two elements comes before the other**. So
if we look at the *later* one of the two, the *earlier* one is
already in our dictionary.

Concretely: suppose the valid pair is at indices `i` and `j` with
`i < j`. When the loop reaches index `i`, we don't see the pair
yet — `nums[j]` hasn't appeared. We just file `nums[i]` away.
When the loop reaches index `j`, `nums[i]` is already in the
dict. We compute `partner = target - nums[j]`, and that
`partner` equals `nums[i]`, which is in the dict. Match.

So one single pass catches every pair, as long as we process
elements left to right and only ever pair "current" with "past."

A useful image: the dict is a **growing memory** of everything
we have seen. As we walk forward, the memory grows by one each
step, and at each step we ask one question of the memory. The
loop and the memory grow together, like two pointers moving in
lockstep.

If we tried to look for the pair by walking left from each `j`,
we would do nested-loop work and lose our speed. The dict
replaces the inner loop with a constant-time question.
''',
            },
            {
                "question": "What if the same number appears twice and is part of the pair? Like `nums = [3, 3]`, `target = 6`.",
                "answer": r'''
Walk through it slowly to make sure you really see what happens.

Initial state: `seen = {}` (empty dict).

**Iteration 0**: `i = 0`, `x = 3`.
- `partner = 6 - 3 = 3`.
- Is `3` in `seen`? `seen` is empty, so no.
- We did *not* find a pair. Insert: `seen = {3: 0}`. Continue.

**Iteration 1**: `i = 1`, `x = 3`.
- `partner = 6 - 3 = 3`.
- Is `3` in `seen`? Yes — `seen[3] == 0`.
- Return `(0, 1)`. Done.

So duplicates are handled naturally. The key is that we **insert
after checking**, so the duplicate that appears later finds its
predecessor in the dict without the predecessor accidentally
"matching itself."

What if `nums = [3]` and `target = 6`? On iteration 0, partner is
3, the dict is empty, we insert. The loop ends with no match.
Function returns `None`. Correct — there is no pair to find when
there is only one element.

What if `nums = [3, 3, 4]` and `target = 6`? We return `(0, 1)`
on iteration 1. The 4 is never even examined. Also correct.

The takeaway: as long as you check-then-insert, duplicates and
single-element arrays behave the way you expect. No special
cases.
''',
            },
            {
                "question": "When should I use the two-pointer version instead of the hash version?",
                "answer": r'''
Use the **two-pointer** version when the input is **already
sorted**, or when the problem context says you should not use
*O(n)* extra memory. Use the **hash** version when the array is
**unsorted**, when memory is plentiful, or when you need to
preserve the original indices.

A side-by-side comparison:

| Aspect | Hash (this solution) | Two pointers |
|---|---|---|
| Requires sort? | No | Yes (sort first if needed) |
| Time | *O(n)* | *O(n)* after sort, *O(n log n)* total |
| Extra space | *O(n)* for the dict | *O(1)* |
| Preserves indices? | Yes | No (sort scrambles them) |
| Handles duplicates? | Naturally | Naturally |

If the LeetCode problem says "return the indices in the input
array," the hash version is the cleaner answer because sorting
would lose the original positions (you would have to track them
separately).

If the problem is a follow-up like "given a sorted array, find a
pair summing to target," the two-pointer version is the cleaner
answer. *O(1)* memory and no hash overhead.

For the higher-order family (3-Sum, 4-Sum), the **two-pointer
version is preferred**, because once you fix one or two elements,
the remaining subproblem on the sorted suffix is exactly a
two-pointer search. Step 3's "Hard" section will use this idea.

Bottom line: both are good. They are not competing — they are
**complementary tools** for different shapes of the same family
of problems. Knowing both makes you flexible.
''',
            },
            {
                "question": "Why is the hash version *O(n)* space? Isn't that wasteful for a small array?",
                "answer": r'''
It is *O(n)* in the worst case because, if no pair exists or the
pair is at the very end, we end up inserting every single element
into the dict before finding (or failing to find) the answer.
For an array of size `n`, the dict can grow to `n` entries.

Is this wasteful? It depends on the scale. For an array of size
100, the dict holds at most 100 entries — a few kilobytes of
memory. Negligible. For an array of size one billion, the dict
holds up to a billion entries, which could be tens of gigabytes.
That matters.

But here is the perspective shift: the algorithm runs in *O(n)*
**time**, which beats the brute-force *O(n²)*. For `n = 10⁴`,
that is `10⁴` operations versus `10⁸` — a ten-thousand-times
speedup. The price you pay is *O(n)* memory instead of *O(1)*.
For most real-world inputs, this is a great trade.

If memory is genuinely tight, the two-pointer-after-sort approach
gives you *O(1)* extra memory at the cost of *O(n log n)* time
and losing original indices. Pick the trade that fits your
constraints.

A general lesson from this: **the cheapest speedups in DSA come
from using extra memory to remember work you have already done**.
Almost every "O(n²) → O(n)" improvement on this sheet uses
exactly this trick. Sometimes it is a hash; sometimes a precomputed
prefix array; sometimes a memo table. The mental motion is the
same.
''',
            },
        ],
        "summary": r'''
**Pattern**: hash "values seen so far" while scanning; for each
new element, query the dict for its complement.

**Lesson**: when a brute force "for every pair, check..." loop
appears, the first question to ask is *"can a hash of what I have
already seen reduce the inner question to one lookup?"*. For Two
Sum the answer is yes, and the algorithm collapses from *O(n²)*
to *O(n)*.

**Recognize next time**: any "find two / three / four elements
satisfying property P" problem. K-Sum, subarray sums, anagram
grouping, longest-substring problems — they all build on this
exact instinct.

**Bigger picture**: Two Sum is the **kindergarten classroom** of
hash-based algorithm design. Master the check-then-insert order,
internalize "the dict holds the past, not the present," and you
have unlocked an entire family of medium / hard problems with
almost no extra learning.
''',
    },
    {
        "id": "sort-0s-1s-2s",
        "title": "Sort 0s, 1s, and 2s (Dutch National Flag)",
        "step_id": 3,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["arrays", "three-pointers", "partition"],
        "understanding": r'''
We have an array containing only the values 0, 1, and 2 — in any
order. Sort it in place. Example: `[2, 0, 1, 2, 1, 0]` becomes
`[0, 0, 1, 1, 2, 2]`.

You could call Python's `sort()` and be done. The interesting
challenge is to do it in **one pass**, **in place**, with **only
three pointers**. The algorithm is famous enough to have a name:
**Dutch National Flag**, named for the Dutch flag's three colored
stripes.
''',
        "brute_force": {
            "explanation": r'''
**Two passes (counting sort)**: first pass counts the number of 0s,
1s, and 2s. Second pass overwrites the array with those counts.
*O(n)* time, *O(1)* extra space. Correct and simple.

```python
c0 = arr.count(0); c1 = arr.count(1); c2 = arr.count(2)
arr[:] = [0] * c0 + [1] * c1 + [2] * c2
```

But it is two passes, and the slicing creates a new list. The real
algorithmic gem is the **one-pass three-pointer** approach.
''',
            "code": r'''def sort_012_count(arr: list[int]) -> None:
    c0 = arr.count(0)
    c1 = arr.count(1)
    c2 = arr.count(2)
    # Overwrite in place.
    i = 0
    for _ in range(c0):
        arr[i] = 0; i += 1
    for _ in range(c1):
        arr[i] = 1; i += 1
    for _ in range(c2):
        arr[i] = 2; i += 1
''',
            "complexity": (
                "**Time**: *O(n)* (two passes). **Space**: *O(1)*."
            ),
        },
        "thought_process": r'''
The three-pointer one-pass version is wonderful. We maintain three
indices:

- `low` — the next position to fill with a 0.
- `mid` — the position we are currently inspecting.
- `high` — the next position to fill with a 2.

Invariants we maintain throughout the loop:

- `arr[0 .. low - 1]` contains only 0s.
- `arr[low .. mid - 1]` contains only 1s.
- `arr[high + 1 .. n - 1]` contains only 2s.
- `arr[mid .. high]` is the "unprocessed" zone.

At each step we look at `arr[mid]`:

- If `arr[mid] == 0`: it belongs at the front. Swap with `arr[low]`,
  advance both `low` and `mid`. (The swapped-in value was a 1 from
  the middle zone, so `mid` moves on.)
- If `arr[mid] == 1`: it is already where it should be. Just advance
  `mid`.
- If `arr[mid] == 2`: it belongs at the back. Swap with `arr[high]`,
  decrement `high`. **Do not advance `mid`**, because the swapped-in
  value is unprocessed and we have to look at it next.

That `mid` does not advance on the "swap with high" case is the
subtle, critical detail. Most beginners get this wrong on their
first try. Walk through `[2, 0, 1]` on paper to feel it.
''',
        "optimized": {
            "explanation": r'''
Single pass with three pointers (low, mid, high), in place.
''',
            "code": r'''def sort_012(arr: list[int]) -> None:
    low = 0
    mid = 0
    high = len(arr) - 1
    # Continue while there is still an unprocessed zone.
    while mid <= high:
        if arr[mid] == 0:
            # The element belongs to the 0-zone at the front.
            arr[low], arr[mid] = arr[mid], arr[low]
            low += 1
            mid += 1
        elif arr[mid] == 1:
            # The element is already in the 1-zone where it belongs.
            mid += 1
        else:  # arr[mid] == 2
            # The element belongs to the 2-zone at the back.
            # Crucial: we do NOT advance mid, because we just swapped in
            # an unprocessed value from the high side and need to inspect it.
            arr[mid], arr[high] = arr[high], arr[mid]
            high -= 1
''',
            "complexity": (
                "**Time**: *O(n)* — each element is inspected at most "
                "a constant number of times.\n\n"
                "**Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
The Dutch flag is the generalization of quick sort's partition step
to **three** groups instead of two. Once you see this, you realize
that the same idea handles:

- **Quick sort with three-way partitioning** (useful when many
  duplicates exist; degenerate quick sort behaves badly on those).
- **Three-way merge sort** variants.
- **In-place rearrangement** problems like "move all evens before
  all odds" — same shape, simpler.
- **Partition around a pivot value** in selection algorithms.

The deep mental shift: **partitioning** is a primitive operation
that buys you a lot. Every time you face an array problem with
"rearrange so that all X come before all Y", a partition pass is
nearly always the right answer.

And the loop invariant we wrote in plain English ("arr[0..low - 1]
contains only 0s" etc.) is the kind of careful thinking that makes
this category of problems tractable. Write the invariant first, the
code second.
''',
        "summary": r'''
**Pattern**: three-pointer partition with explicit invariants.

**Lesson**: the trick is `mid` *not* advancing on the
swap-with-high case. The reason is that you just imported an
unprocessed element from the unknown zone.

**Recognize next time**: any "rearrange so all X come first, then
Y, then Z" with a small fixed set of categories. Dutch flag
generalizes naturally to 3, 4, or more colors.
''',
    },
    {
        "id": "kadane-algorithm",
        "title": "Maximum Subarray Sum (Kadane's Algorithm)",
        "step_id": 3,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["arrays", "dp", "kadane"],
        "understanding": r'''
Given an array of integers (possibly with negatives), find the
**maximum sum** of any **contiguous subarray**. A subarray must be
non-empty.

Example: `[-2, 1, -3, 4, -1, 2, 1, -5, 4]` → best is `[4, -1, 2, 1]`
with sum `6`.

The brilliance of this problem is that the naive answer is *O(n²)*
or *O(n³)*, and the optimal is *O(n)* with one *brilliant* insight.
The optimal algorithm is so well known it has a name: **Kadane's
algorithm**.
''',
        "brute_force": {
            "explanation": r'''
**Most brute force (O(n³))**: every subarray is a pair (start, end).
For each pair, sum and track the max. Three nested loops.

**Slightly better (O(n²))**: for each start, run a running sum as
end advances. Drops one factor of n.

We will show the *O(n²)* version because the *O(n³)* is unkind.
''',
            "code": r'''def max_subarray_brute(arr: list[int]) -> int:
    n = len(arr)
    best = arr[0]
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += arr[j]
            if s > best:
                best = s
    return best
''',
            "complexity": (
                "**Time**: *O(n²)*. **Space**: *O(1)*."
            ),
        },
        "thought_process": r'''
Kadane's insight is the cleverest single line in beginner DSA. Let
me try to reproduce the *aha* moment.

Define `best_ending_here[i]` as the maximum sum of any subarray that
**ends at index i**. The final answer is the maximum of
`best_ending_here[i]` over all `i`.

Now: what is the relationship between `best_ending_here[i]` and
`best_ending_here[i - 1]`? Two possibilities for the best subarray
ending at `i`:

1. It extends the best subarray ending at `i - 1` by adding `arr[i]`.
2. It starts fresh at `i`, sum equal to `arr[i]`.

The first option gives `best_ending_here[i - 1] + arr[i]`. The
second gives `arr[i]`. We pick the larger.

So: `best_ending_here[i] = max(arr[i], best_ending_here[i - 1] + arr[i])`.

Now read that recurrence in plain English: *"to find the best
subarray ending here, either I extend the best one from yesterday,
or I start fresh today. Pick the better option."*

And the implementation does not even need an array. We only need
the previous value:

```python
best_ending_here = arr[0]
best_overall = arr[0]
for i in range(1, n):
    best_ending_here = max(arr[i], best_ending_here + arr[i])
    best_overall = max(best_overall, best_ending_here)
```

That's Kadane's. The algorithm fits on a beer mat and it's *O(n)*.

The mental rule of thumb: **if your running sum drops to a value
worse than starting fresh, start fresh.** The previous prefix has
already done its damage; carrying it forward only hurts.
''',
        "optimized": {
            "explanation": r'''
Single pass tracking two scalars: the best subarray ending at the
current index, and the global best.
''',
            "code": r'''def max_subarray(arr: list[int]) -> int:
    # Initialize both running scalars to the first element. Any best
    # subarray contains at least one element, so this is the floor.
    best_ending_here = arr[0]
    best_overall = arr[0]
    for i in range(1, len(arr)):
        # Either extend the previous subarray by adding arr[i], or
        # start a fresh subarray of just arr[i]. Pick whichever sum
        # is larger.
        best_ending_here = max(arr[i], best_ending_here + arr[i])
        # Update the global best whenever we've topped it.
        if best_ending_here > best_overall:
            best_overall = best_ending_here
    return best_overall
''',
            "complexity": (
                "**Time**: *O(n)*. **Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
Kadane's algorithm is the **simplest example of dynamic
programming**. The recurrence `best_ending_here[i] = max(arr[i],
best_ending_here[i - 1] + arr[i])` is a one-dimensional DP. The
state is "the index `i`", and the value is "best subarray ending
exactly there". The transition takes constant time, so total work is
*O(n)*.

Because the DP only depends on the previous value, we collapse the
array of `best_ending_here` values to a single scalar. That is a
common DP optimization, "space optimization", which we cover in
detail in Step 16.

A variant: **circular maximum subarray sum**. The subarray can wrap
around. The trick is to also compute the minimum subarray sum, and
the circular max equals `total_sum - min_subarray_sum` (unless the
entire array is negative). One Kadane forward, one Kadane backward,
and a tiny adjustment.

Another variant: **find the indices of the best subarray**. Track
the current start whenever we "start fresh", and update best_start
/ best_end whenever we update the global best. The algorithm grows
by two scalars but remains *O(n)*.
''',
        "summary": r'''
**Pattern**: 1D DP collapsed to a running scalar.

**Lesson**: if extending the previous subarray makes the sum
worse than starting fresh, start fresh. That single rule is
Kadane's.

**Recognize next time**: any "maximum sum of a contiguous range"
problem. With negatives, Kadane's is the go-to. With only positives,
sliding window or prefix sum are alternatives.
''',
    },
    {
        "id": "stock-buy-sell",
        "title": "Best Time to Buy and Sell Stock",
        "step_id": 3,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["arrays", "linear-scan", "dp"],
        "understanding": r'''
You have an array of stock prices, one per day. You can buy on one
day and sell on a later day. Find the maximum profit you can make
from a **single** buy-sell transaction. If no profit is possible,
return 0.

Example: `[7, 1, 5, 3, 6, 4]` → buy on day 1 at price 1, sell on
day 4 at price 6 → profit 5.

The "single transaction" constraint matters. The harder variations
(multiple transactions, with fees, with cooldown) are covered in
Step 16's DP-on-stocks lecture.
''',
        "brute_force": {
            "explanation": r'''
For each day `i`, consider buying on day `i` and check every later
day `j > i` for the maximum profit `prices[j] - prices[i]`. *O(n²)*.

The optimized algorithm collapses this to *O(n)* with the same
"carry the best so far" trick we have been using.
''',
            "code": r'''def max_profit_brute(prices: list[int]) -> int:
    best = 0
    n = len(prices)
    for i in range(n):
        for j in range(i + 1, n):
            profit = prices[j] - prices[i]
            if profit > best:
                best = profit
    return best
''',
            "complexity": "**Time**: *O(n²)*. **Space**: *O(1)*.",
        },
        "thought_process": r'''
For each day `j`, the best profit if I sell on `j` is
`prices[j] - min(prices[0..j - 1])`. If I have been tracking the
running minimum price so far as I walk forward, then computing the
best-if-sold-today is one subtraction per day.

So: walk forward, carry `min_so_far`, and for each day update
`best_profit = max(best_profit, prices[j] - min_so_far)` before
updating `min_so_far = min(min_so_far, prices[j])`.

The order matters. We must compute the profit (which uses today's
price as the sell) **before** updating `min_so_far` to include
today's price (which would be using today as both buy and sell).
Actually it does not change the result here because the profit
would be zero, but for clarity many people compute profit first.

This is yet another instance of the running-scalar pattern. By now
you should be noticing how many array problems collapse to "walk
once, carry one or two scalars".
''',
        "optimized": {
            "explanation": r'''
Walk left to right. Maintain the minimum price seen so far. For
each day, the best profit "if I sold today" is `price - min_so_far`.
Track the maximum of those.
''',
            "code": r'''def max_profit(prices: list[int]) -> int:
    # The cheapest price we have seen so far.
    min_so_far = prices[0]
    # The best profit we have found so far.
    best = 0
    for price in prices[1:]:
        # If we sold today at `price`, our profit is `price - min_so_far`.
        # Update the best with that, but never go below 0.
        if price - min_so_far > best:
            best = price - min_so_far
        # Now update min_so_far to potentially include today.
        if price < min_so_far:
            min_so_far = price
    return best
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "deep_concept": r'''
This is **Kadane in disguise**. If we look at the *differences*
between consecutive days — `prices[1] - prices[0]`, `prices[2] -
prices[1]`, ... — the maximum profit equals the maximum subarray
sum of those differences. The "running min" version and the
"max-subarray-of-differences" version are equivalent expressions of
the same idea.

This connection between a stock problem and Kadane is one of the
prettiest little jokes in interview DSA. Once you see it, you know
that "max profit (1 transaction)" is just a renamed array problem.

The more advanced stock problems (multiple transactions, cooldowns,
fees) are DP. They each maintain state for "do I currently hold
stock?" and possibly "how many transactions left?". The single-pass
trick generalizes via DP recurrences. We tackle those in Step 16.
''',
        "summary": r'''
**Pattern**: walk once carrying min-so-far and best-so-far.

**Lesson**: every "buy low, sell high" problem reduces to "at each
point, what is the best partner from the past?". A scan with a
running scalar gives the answer.

**Recognize next time**: any optimization problem where you need
"the best earlier value" as you walk forward.
''',
    },
    {
        "id": "longest-consecutive-sequence",
        "title": "Longest Consecutive Sequence",
        "step_id": 3,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["arrays", "hashing", "sets"],
        "understanding": r'''
Given an unsorted array of integers, return the length of the
longest **consecutive** sequence of values present in the array. The
values do not need to be in order in the array — they just need to
exist.

Example: `[100, 4, 200, 1, 3, 2]` → consecutive sequence is
`[1, 2, 3, 4]`, length 4. (The array also contains 100 and 200 but
those don't extend any run.)

The problem looks like a sorting problem (sort and walk), but the
real prize is doing it in *O(n)* without sorting.
''',
        "brute_force": {
            "explanation": r'''
**Sort then walk**: sort the array, then walk linearly counting runs
of consecutive integers. *O(n log n)* time due to sort. Simple and
arguably the right answer when the array is small.

```python
arr = sorted(set(arr))
best = current = 1
for i in range(1, len(arr)):
    if arr[i] == arr[i - 1] + 1:
        current += 1
        best = max(best, current)
    else:
        current = 1
```

We can do better. *O(n)* with a hash set.
''',
            "code": r'''def longest_consec_sort(arr: list[int]) -> int:
    if not arr:
        return 0
    arr = sorted(set(arr))
    best = current = 1
    for i in range(1, len(arr)):
        if arr[i] == arr[i - 1] + 1:
            current += 1
            best = max(best, current)
        else:
            current = 1
    return best
''',
            "complexity": "**Time**: *O(n log n)*. **Space**: *O(n)*.",
        },
        "thought_process": r'''
The clever *O(n)* algorithm uses a set and a single observation:
**every consecutive sequence has a unique starting point**, which is
the smallest number in it. A number `x` is a starting point if and
only if `x - 1` is **not** in the set.

So we walk through every element. For each element that is a
starting point (i.e., `x - 1` is missing), we extend forward by
checking `x + 1`, `x + 2`, ... in the set until we run out. We
record the length.

The trick is that we only spend time extending when we are at a
starting point. Every consecutive run is extended exactly once. So
the total work is *O(n)*, not *O(n²)* — even though there is a
nested `while` loop.

Read the previous paragraph again. It is subtle. The total work
inside the inner `while` loop is bounded by the total length of all
consecutive runs, which is at most `n`. So the inner loop adds *O(n)*
across the whole algorithm, not *O(n)* per outer iteration.

This is one of those clever amortized arguments that interviewers
love to see explained out loud.
''',
        "optimized": {
            "explanation": r'''
Put all elements in a set. For each element that starts a run
(no `x - 1` in the set), extend the run forward and track the
longest.
''',
            "code": r'''def longest_consecutive(arr: list[int]) -> int:
    s = set(arr)
    best = 0
    for x in s:
        # Only START extending from values that are run-starters.
        # A run-starter has no predecessor x - 1 in the set.
        if x - 1 not in s:
            length = 1
            current = x
            # Extend forward as long as the next value exists.
            while (current + 1) in s:
                current += 1
                length += 1
            if length > best:
                best = length
    return best
''',
            "complexity": (
                "**Time**: *O(n)* amortized. **Space**: *O(n)* for "
                "the set."
            ),
        },
        "deep_concept": r'''
The "skip non-starting values" optimization is a beautiful instance
of an **amortization argument**. We have a nested loop that *looks*
quadratic but is actually linear because each consecutive run is
extended exactly once.

This pattern recurs:

- **Number of distinct islands** in a 2D grid — flood-fill starts
  only at "fresh" cells, so the total work is bounded by grid size.
- **Visiting nodes in a graph** during BFS/DFS — each node is
  visited once, even though we have an outer "for each node" loop.
- **Sliding window** — each element enters and exits the window
  exactly once.

Whenever you see a nested loop that you think might secretly be
linear, ask: "is there an invariant that bounds the inner work
globally?". If yes, you have a smart algorithm masquerading as a
slow one.

A variation: instead of "longest consecutive run", count "how many
consecutive runs of length ≥ k". Same set scaffolding, different
bookkeeping.
''',
        "summary": r'''
**Pattern**: hash set + only-extend-from-starting-points.

**Lesson**: a nested loop is not always quadratic. Find the global
invariant that bounds inner work.

**Recognize next time**: "longest sequence of consecutive things"
without the array being sorted. The set lookup is the magic
ingredient.
''',
    },
    {
        "id": "majority-element",
        "title": "Majority Element (> N/2 times) — Boyer-Moore",
        "step_id": 3,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["arrays", "boyer-moore", "voting"],
        "understanding": r'''
Given an array of integers, return the **majority element** — the
one that appears **more than N/2 times**. The problem guarantees one
exists.

Example: `[3, 2, 3]` → majority is 3 (appears twice in a length-3
array, which is more than 3/2).

The hashing solution is trivial. The optimized solution is one of
the most elegant tricks in algorithms: **Boyer-Moore voting**. It
finds the majority element in *O(n)* time and *O(1)* space — no
sorting, no hashing.
''',
        "brute_force": {
            "explanation": r'''
**Count with a hash**: walk once, increment a counter for each
value, then return the key with count > N/2. *O(n)* time, *O(n)*
space.

The Boyer-Moore version achieves *O(1)* space. That is the
distinguishing trick.
''',
            "code": r'''def majority_hash(arr: list[int]) -> int:
    from collections import Counter
    counts = Counter(arr)
    n = len(arr)
    for k, v in counts.items():
        if v > n // 2:
            return k
    raise ValueError("no majority element")
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(n)*.",
        },
        "thought_process": r'''
Boyer-Moore voting is the kind of algorithm that feels like a magic
trick. Imagine a knockout tournament where each element of the
array "votes" — but every time two different values appear together,
they cancel each other out. The majority element survives the
cancellations because it has more votes than everyone else
combined.

Concretely we maintain a **candidate** and a **vote count**. We
walk through the array:

- If `count == 0`, we adopt the current element as our new
  candidate and set count to 1.
- If the current element matches the candidate, increment count.
- If it does not match, decrement count.

At the end, the candidate is the majority element (assuming one
exists). If you are not sure a majority exists, do a second pass to
verify.

**Why does this work?** Picture the votes as a battle: matching
votes increase the candidate's lead, non-matching votes decrease
it. Since the majority appears more than `N/2` times and everyone
else combined appears less than `N/2` times, the majority's lead
cannot be wiped out by the combined opposition. The candidate at
the end is guaranteed to be the majority.

This argument is one of those *aha* moments. Don't be surprised if
it takes a few rereads. The leap of faith — that the running
candidate, despite being overwritten multiple times, lands on the
right answer — is part of the algorithm's charm.
''',
        "optimized": {
            "explanation": r'''
Boyer-Moore Majority Vote. One pass, two scalars.
''',
            "code": r'''def majority_element(arr: list[int]) -> int:
    candidate = None
    count = 0
    # First pass: identify the candidate.
    for x in arr:
        if count == 0:
            candidate = x
            count = 1
        elif x == candidate:
            count += 1
        else:
            count -= 1
    # If a majority is guaranteed to exist, candidate IS the answer.
    # Otherwise verify with a second pass:
    # if arr.count(candidate) > len(arr) // 2: return candidate else None
    return candidate  # type: ignore[return-value]
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "deep_concept": r'''
The Boyer-Moore voting algorithm generalizes to **finding the K
elements that appear more than N/(K+1) times**. The classic case
is `K = 2` ("more than N/3 times"), which is in this curriculum's
hard section: there can be at most two such elements. We maintain
two candidates and two counters instead of one. The generalization
to general `K` is called the **Boyer-Moore generalized vote**.

The underlying principle — "pair up opposing votes and let the
majority survive" — is a beautiful instance of cancellation
arguments. We saw similar cancellation in the XOR-based "single
number" problem. Cancellation is a recurring algorithmic idea: if
two things "destroy" each other when paired, the surplus survives.
''',
        "summary": r'''
**Pattern**: Boyer-Moore vote — pair off non-matching elements;
the majority survives.

**Lesson**: certain problems that *look* like they need a hash can
actually be solved in *O(1)* space via cancellation arguments.

**Recognize next time**: any "appears more than N/K times" problem.
Boyer-Moore voting generalizes to K candidates.
''',
    },
    {
        "id": "merge-overlapping-intervals",
        "title": "Merge Overlapping Intervals",
        "step_id": 3,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["arrays", "intervals", "sorting", "greedy"],
        "understanding": r'''
Given a list of intervals `[start, end]`, merge any that overlap.
Two intervals `[a, b]` and `[c, d]` overlap if `c <= b` (assuming
`a <= c`). Output the list of merged intervals.

Example: `[[1, 3], [2, 6], [8, 10], [15, 18]]` → `[[1, 6], [8, 10],
[15, 18]]`. The first two overlap and merge into `[1, 6]`.

This is the canonical "sort first" problem. Sorting the intervals
by start time is the unlock.
''',
        "brute_force": {
            "explanation": r'''
You can repeatedly look for any pair of overlapping intervals, merge
them, and repeat until no overlaps remain. That is *O(n² log n)* or
worse. Painful and unnecessary.

The "sort by start time, walk once" approach is the textbook answer
and is fast and clean.
''',
            "code": r'''def merge_intervals_brute(intervals: list[list[int]]) -> list[list[int]]:
    # Naive: keep merging the first overlapping pair until stable.
    out = [list(iv) for iv in intervals]
    changed = True
    while changed:
        changed = False
        for i in range(len(out)):
            for j in range(i + 1, len(out)):
                a, b = out[i]
                c, d = out[j]
                # Overlap test that does not assume ordering.
                if a <= d and c <= b:
                    out[i] = [min(a, c), max(b, d)]
                    out.pop(j)
                    changed = True
                    break
            if changed:
                break
    return sorted(out)
''',
            "complexity": (
                "**Time**: poor — *O(n³)* or worse in pathological "
                "cases. **Space**: *O(n)*."
            ),
        },
        "thought_process": r'''
The key insight: **if we sort intervals by start time**, then for
any pair of overlapping intervals, the one with the smaller start
comes first. So we can walk through the sorted list and, for each
new interval, only need to compare it with the **most recent
merged interval** in our output. If it overlaps, we extend the
merged interval's end. If it does not, we append it as a new
interval.

That observation reduces the problem to a single pass after sorting.

Why? Because once intervals are sorted by start, an interval cannot
overlap with anyone that comes after the next one without also
overlapping the next one. Overlaps are "transitive forward" — if
A overlaps B and B overlaps C, then the merge so far includes a
single chunk containing all three.

The runtime is dominated by the sort: *O(n log n)*. The walk is
*O(n)*. The space is *O(n)* for the output.
''',
        "optimized": {
            "explanation": r'''
Sort by start. Walk through; either extend the last output interval
or append a new one.
''',
            "code": r'''def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    # Sort by start time. If starts are equal, sort by end (does not
    # affect correctness here, but tidier).
    intervals = sorted(intervals, key=lambda iv: (iv[0], iv[1]))
    merged: list[list[int]] = [list(intervals[0])]
    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            # The new interval overlaps with the last merged one.
            # Extend the last one's end (keep the maximum).
            merged[-1][1] = max(last_end, end)
        else:
            # No overlap; this interval starts after the last one ends.
            merged.append([start, end])
    return merged
''',
            "complexity": (
                "**Time**: *O(n log n)* due to sorting. **Space**: "
                "*O(n)* for the output."
            ),
        },
        "deep_concept": r'''
The "sort by start time, then walk" approach is the **interval
processing pattern**. It shows up in many shapes:

- **Insert interval** — given sorted non-overlapping intervals,
  insert a new one and re-merge. The single new interval keeps the
  algorithm *O(n)*.
- **Meeting rooms / number of platforms** — count concurrent
  intervals. Sort start times and end times separately, then sweep.
- **Skyline problem** — events at each interval's start and end,
  sorted, then swept with a priority queue.
- **Non-overlapping intervals** — sort by end time and greedily
  keep intervals that fit. (The greedy choice "earliest end first"
  is what unlocks the problem.)

The unifying idea: **time is one-dimensional and orderable**. Any
problem about ranges, durations, or schedules tends to benefit from
sorting along the time axis and sweeping forward.

A second deep idea is the **sort key choice**. For merging, we sort
by **start**. For non-overlapping, we sort by **end**. Why? Because
the optimal greedy choice depends on what you want to keep. The
start-sort lets us decide "does this overlap the previous?" without
backtracking; the end-sort lets us decide "what is the latest
interval I can finish to leave room for the most future ones?".
''',
        "summary": r'''
**Pattern**: sort by start, sweep once, merge or append.

**Lesson**: interval problems are sort-and-sweep problems in
disguise. The sort key matters — pick it for the question you are
asking.

**Recognize next time**: any problem about merging, scheduling, or
counting overlapping intervals. Always start by sorting.
''',
    },
]
