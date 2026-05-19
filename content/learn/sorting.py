"""Sorting — the warm-up gym for algorithmic thinking."""

LESSON = {
    "id": "sorting",
    "title": "Sorting — Comparisons, Swaps, and Divide-and-Conquer",
    "tags": ["sorting", "fundamentals"],
    "summary": (
        "A full beginner chapter. Why sorting is the gateway drug to "
        "algorithmic thinking, how each of the classic sorts tells a "
        "different story, the loop-invariant discipline that proves "
        "them correct, and the rules for choosing one over another in "
        "real code."
    ),
    "body": r'''
## 0. Why this chapter matters

You will almost never write a sorting algorithm in production code
— `sorted()` already does it better than you will. So why spend a
whole chapter on classical sorts?

Three reasons.

**Reason 1: sorting is the cleanest possible introduction to
algorithm analysis.** Loop invariants, big-O reasoning,
divide-and-conquer recurrences, in-place vs. extra-memory trade-
offs — all of them show up in sorting first, in their simplest
forms.

**Reason 2: "sort first, then walk" is one of the most reliable
problem-solving moves you have.** Many array problems become
trivial after sorting. Recognizing when sorting unlocks a
problem is half the battle.

**Reason 3: the underlying ideas reappear constantly.** Merge
sort's merge step powers external sorting and merging K sorted
lists. Quick sort's partition powers Quickselect and the Dutch
National Flag. Insertion sort lives inside production hybrid
sorts.

So read this chapter not as "memorize five algorithms" but as "see
how five different mental moves combine to solve the same
problem." The moves matter more than the algorithms.

## 1. What does it mean to "sort"?

Given an array of comparable items, **sorting** is rearranging
them into non-decreasing (or non-increasing) order. "Comparable"
means there is a `<` or `>` operation defined between any two
items.

Numerical sorting is the prototype: `[3, 1, 4, 1, 5, 9, 2, 6]`
becomes `[1, 1, 2, 3, 4, 5, 6, 9]`. But we can sort strings
(lexicographic), tuples (lexicographic over fields), custom
objects with a comparison function, and so on.

The output of a sort is determined by the **comparator** — the
function that decides which of two items comes first. For
integers and strings, Python uses the natural comparator (`<`).
For custom orders, you pass `key=` or wrap the data.

## 2. The four classic sorts in one paragraph each

**Selection sort.** Find the smallest unsorted element; swap it to
the front; repeat. *O(n²)* always. Simple to write, slow to run,
makes only `n` swaps (which is unusually low).

**Bubble sort.** Walk left to right swapping out-of-order
neighbours; repeat until a clean pass. *O(n²)* worst, *O(n)* on
already-sorted input (with the early-exit trick). Famous for
being slow on real data and beautiful for the inversion
connection.

**Insertion sort.** Walk left to right; for each element, slide it
leftward into its correct place in the sorted prefix. *O(n²)*
worst, *O(n)* on nearly-sorted. The fastest *O(n²)* sort in
practice; production sorts use it as the small-array base case.

**Merge sort.** Split, recursively sort each half, merge. *O(n
log n)* worst case always. Uses *O(n)* extra memory. Stable.

**Quick sort.** Pick a pivot, partition, recursively sort the two
halves. *O(n log n)* average, *O(n²)* worst (mitigated by random
pivots). In-place, very fast constants.

That's the field. Read each algorithm's full problem write-up
in Step 2 of the curriculum for line-by-line code, complexity
arguments, and confusion notes.

## 3. The loop invariant — the discipline that proves sorts correct

A **loop invariant** is a statement that is true at the start of
every iteration of a loop. It captures what the loop has
accomplished so far.

For selection sort: "Before iteration `i`, `arr[0..i-1]` contains
the smallest `i` elements of the array, in sorted order."

That sentence — properly verified at the start (true for `i = 0`)
and preserved by each iteration — proves the sort correct
without tracing a single iteration. Once you state the
invariant, the code's correctness is a one-paragraph argument
rather than a forest of cases.

Writing the invariant first is not just a teaching tool. It is
how serious programmers verify their loops are right. Whenever
you write a loop, ask yourself: *"what is true before iteration
`i`, and how does iteration `i` extend it?"*. If you cannot
answer, your loop probably has a bug.

This discipline pays off enormously in trickier loops: binary
search, sliding window, two pointers, partition algorithms. Each
of those has subtle off-by-ones that an invariant catches before
the first bug report.

## 4. Stability — what it is and when it matters

A sort is **stable** if elements that compare equal keep their
original relative order. **Unstable** sorts may swap them around.

Concretely, suppose you sort a list of records by **age**, and
two records share age 30. A stable sort keeps them in their
original input order. An unstable sort may rearrange them.

When does stability matter? When you sort by one field and want
to preserve order for ties on that field. For example:

- Sort employees by department; within each department keep them
  in alphabetical order (from a previous sort).
- Sort log entries by timestamp; same-timestamp entries in
  original arrival order.

When stability does not matter: sorting plain numbers. There is
nothing distinguishing the two 5s.

The stable / unstable status of common sorts:

- Selection sort: usually **unstable**.
- Bubble sort: **stable**.
- Insertion sort: **stable**.
- Merge sort: **stable** (with the `<=` comparison convention).
- Quick sort: usually **unstable**.
- Python's `sorted` / `list.sort`: **stable** (Timsort).
- C++'s `std::sort`: **unstable**; use `std::stable_sort` if you
  need stability.

A pro trick: if your sort is unstable but you want stability,
sort by `(primary_key, original_index)`. The tie-breaker on
original index makes the result deterministic and stable.

## 5. In-place vs. extra-memory

An **in-place** sort uses only *O(1)* (or *O(log n)*) extra
memory beyond the input. The sort rearranges the array
"on top of itself." Quick sort and most heap sort
implementations are in-place.

An **out-of-place** sort allocates *O(n)* (or more) extra memory.
Merge sort is the canonical example.

When in-place matters: very large data sets where you cannot
afford double the memory. Real numerics on big arrays.

When in-place does not matter: most interview problems, most
production code on modern hardware. Memory is cheap.

A subtle point: even "in-place" Python sorts allocate a small
buffer for stability tracking. Truly in-place is hard to
guarantee in any high-level language. Asymptotic in-place is
usually what we mean.

## 6. Comparison sort lower bound (a brief glimpse)

A theorem: **any comparison-based sort takes Ω(n log n)
comparisons in the worst case**. This is a lower bound — you
cannot beat it without using something other than comparisons.

The proof sketch: each comparison gives one bit of information
("a < b? yes or no"). To distinguish among `n!` possible
permutations, you need at least `log₂(n!) ≈ n log n` bits, hence
`n log n` comparisons.

So merge sort and quick sort are asymptotically optimal among
comparison sorts.

**Non-comparison sorts** can beat this bound by using more
information about the values:

- **Counting sort**: *O(n + k)* where `k` is the value range.
  Works only for small bounded integer values.
- **Radix sort**: *O(d × (n + k))* where `d` is the number of
  digits.
- **Bucket sort**: *O(n + k)* under uniform distribution
  assumptions.

These appear in specialized contexts but are rarely the right
answer in interview settings. Mention them when you spot a
bounded-value sort; otherwise reach for `sorted`.

## 7. The "sort first" pattern

Sorting is often a setup move that makes another algorithm
trivial. The pattern:

```
# Step 1: sort.
arr.sort()
# Step 2: linear or two-pointer or sliding-window scan.
```

Examples:

- **Two Sum on sorted input**: two pointers from the ends.
- **Find duplicates**: after sorting, duplicates are adjacent.
- **Merge intervals**: sort by start, sweep once.
- **3-Sum**: fix one element, two-pointer the rest.
- **Meeting rooms / minimum platforms**: sort events.
- **K closest points to origin**: sort by distance (or use a
  heap).

Whenever you sit down to a new problem, one of the first
questions to ask is: *"would sorting first make this easier?"*.
Often the answer is yes, and the cost is the trivially small
*O(n log n)*.

## 8. When NOT to sort

Sorting is not free. *O(n log n)* is fast, but it is more than
*O(n)*. If your problem can be solved in *O(n)* without sorting
(typically with hashing), do not sort.

Examples:

- "Find the duplicate" → hash set, *O(n)*. Sorting would be
  *O(n log n)*.
- "Two Sum on unsorted input" → hash map, *O(n)*. Sorting then
  two-pointer is *O(n log n)*.
- "Count frequencies" → Counter, *O(n)*. Sorting is *O(n log n)*.

And sometimes sorting destroys information you need:

- "Two Sum with original indices" — sorting loses the original
  positions. Either save (value, index) pairs before sorting, or
  use a hash.
- "Stable rearrangement" — some operations require preserving
  order; sorting may scramble it.

The rule of thumb: prefer hashing for "find / count / pair" with
no ordering. Prefer sorting when ordering or proximity matters.

## 9. Python's `sorted` is the right choice in real code

In Python, you almost always want `sorted(iterable, key=...)` or
`list.sort(key=...)`. Both use **Timsort**, which is:

- *O(n log n)* worst case (proven).
- Stable.
- Highly optimized for partially-sorted inputs (often *O(n)* on
  real-world data).
- Available in optimized C, so no Python-level loops.

The `key=` argument is your friend. It takes a function that
extracts the comparison key from each element:

```python
words = ["banana", "apple", "cherry"]
sorted(words)                         # alphabetic
sorted(words, key=len)                # by length
sorted(words, key=lambda w: w[-1])    # by last letter
sorted(items, key=lambda x: (x[0], -x[1]))  # by x[0] ascending, x[1] descending
```

Avoid the older `cmp` parameter. Use `key=` or, in rare cases,
`functools.cmp_to_key`.

## 10. Common beginner mistakes

**Mistake 1: writing your own sort when `sorted()` exists.**
Unless the interviewer explicitly asks, `sorted()` is the right
production answer. Knowing the classical sorts is for
understanding, not for use.

**Mistake 2: re-sorting inside a loop.** Sorting before the loop
is *O(n log n)* once. Sorting inside the loop is *O(n² log n)*
and almost always wrong.

**Mistake 3: forgetting stability when records have multiple
fields.** When sorting tuples, equal first-fields stay in input
order under a stable sort. Use this for "sort by score, break
ties by name."

**Mistake 4: using `sorted()` when you only need the smallest K.**
For large `n` and small `k`, a heap is much faster (`O(n log k)`).

**Mistake 5: assuming `sort` modifies a copy.** `list.sort()`
mutates the list in place and returns `None`. `sorted(list)`
returns a new list and leaves the original alone. Don't write
`new = list.sort()` — `new` will be `None`.

## 11. End-of-chapter exercise

Solve these five problems using sorting as the central move.

1. **Sort an almost-sorted array.** Each element is at most K
   positions from its sorted location. *O(n log k)* with a heap.
2. **Anagram groups.** Group strings that are anagrams. The
   canonical form (sorted tuple) is the dict key.
3. **Largest number from array of integers.** Concatenate them
   in the order that produces the largest number. Custom sort
   comparator. LeetCode 179.
4. **K closest points to origin.** Two solutions: sort by
   distance (*O(n log n)*), or heap of size K (*O(n log k)*).
   LeetCode 973.
5. **Meeting rooms II / minimum platforms.** Sort starts and
   ends separately, sweep both. LeetCode 253.

These five problems each lean on sorting in a slightly different
way. After all five, you should be reflexively asking "should I
sort?" for every array problem you see.

## 12. Where to go next

- **Step 2** — classical sorts, each in detail.
- **Step 3** — many array problems that begin with "sort, then
  walk."
- **Step 11** — heaps, which are sorting's faster cousins when
  you only need the top K.
- **Step 16** — DP, which uses sorting in some setup steps.

Sorting is foundational. Spend the time. The "sort first" reflex
pays off for years.
''',
}
