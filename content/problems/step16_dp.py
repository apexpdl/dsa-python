"""Step 16 — Dynamic Programming."""
from __future__ import annotations

PROBLEMS: list[dict] = [
    {
        "id": "climbing-stairs",
        "title": "Climbing Stairs",
        "step_id": 16,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["dp", "fundamentals"],
        "what_this_teaches": (
            "The simplest possible **1D dynamic programming** "
            "recurrence. Once you walk the path naive → memoize → "
            "tabulate → space-optimize on this single problem, you "
            "have the full toolkit for an entire family of 1D DPs."
        ),
        "pattern": "dp[i] = dp[i - 1] + dp[i - 2] with two-scalar window.",
        "prerequisite_lessons": ["recursion", "dp"],
        "prerequisite_problems": ["fibonacci-number"],
        "next_problems": [
            "frog-jump",
            "frog-jump-k",
            "house-robber-i",
            "house-robber-ii",
            "ninjas-training",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 16 (1D DP)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 70 — Climbing Stairs",
                "url": "https://leetcode.com/problems/climbing-stairs/",
            },
        ],
        "understanding": r'''
You are climbing a staircase. It takes `n` steps to reach the top.
Each time you can climb either 1 step or 2 steps. In how many
distinct ways can you reach the top?

For `n = 2` there are 2 ways: `1+1` or `2`. For `n = 3` there are
3 ways: `1+1+1`, `1+2`, `2+1`. For `n = 4` there are 5 ways.

The sequence `1, 2, 3, 5, 8, 13, ...` is **Fibonacci** in disguise.
This problem is the cleanest possible introduction to dynamic
programming.
''',
        "brute_force": {
            "explanation": r'''
The recursive definition: to reach step `n`, the last move was
either from step `n-1` (taking 1 step) or from step `n-2` (taking
2 steps). So the number of ways to reach `n` is the sum of the
ways to reach `n-1` and `n-2`.

```python
def ways(n):
    if n <= 1:
        return 1
    return ways(n - 1) + ways(n - 2)
```

This is correct but exponential — same problem as naive Fibonacci.
''',
            "code": r'''def climb_brute(n: int) -> int:
    # Base cases: 0 steps (already at the top, 1 way to "stay") and
    # 1 step (one way: take 1 step).
    if n <= 1:
        return 1
    # Recursive case: the last move was 1 step or 2 steps.
    return climb_brute(n - 1) + climb_brute(n - 2)
''',
            "complexity": "**Time**: *O(2^n)*. **Space**: *O(n)* call stack.",
        },
        "thought_process": r'''
The brute force is exponential because subproblems are recomputed
many times. Adding **memoization** makes it linear:

```python
@lru_cache(maxsize=None)
def ways(n):
    if n <= 1:
        return 1
    return ways(n - 1) + ways(n - 2)
```

Now each `ways(k)` is computed once. *O(n)* total.

We can also write the **bottom-up** version, building up from
`ways(0) = 1` to `ways(n)`:

```python
dp = [0] * (n + 1)
dp[0] = dp[1] = 1
for i in range(2, n + 1):
    dp[i] = dp[i - 1] + dp[i - 2]
```

And finally **space-optimize** by noting we only ever need the
last two values:

```python
prev2, prev1 = 1, 1
for _ in range(2, n + 1):
    prev2, prev1 = prev1, prev1 + prev2
```

That progression — naive → memoized → tabulated → space-optimized
— is the canonical DP refinement path. You will follow it for
dozens of problems in Step 16.
''',
        "optimized": {
            "explanation": r'''
Space-optimized bottom-up: track only the last two values.
''',
            "code": r'''def climb_stairs(n: int) -> int:
    if n <= 1:
        return 1
    # prev2 holds ways(i - 2); prev1 holds ways(i - 1).
    prev2, prev1 = 1, 1
    for _ in range(2, n + 1):
        # ways(i) = ways(i - 1) + ways(i - 2).
        prev2, prev1 = prev1, prev1 + prev2
    return prev1
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "deep_concept": r'''
Climbing stairs is the perfect onramp to DP because:

1. The recurrence is **obvious**.
2. The naive version is **obviously exponential**.
3. The fix (memoization) is **obviously linear**.
4. The space optimization is **obviously O(1)**.

That clarity rarely persists in harder DP problems. But once you
have done climbing-stairs, frog-jump, and house-robber, you have
the muscle for all 1D DPs.

Variations:

- **Frog jump (k distances)** — instead of 1 or 2 steps, you can
  take any of 1, 2, ..., k. Same shape, one more term per
  recurrence step.
- **Min-cost climbing stairs** — instead of counting ways, minimize
  cost. Same recurrence shape; replace `+` with `min`.
- **Decode ways** — given a numeric string, count decodings.
  Recurrence: `dp[i] = dp[i - 1] + (dp[i - 2] if s[i-2:i] is valid two-digit)`.

The fact that these all share a shape is the **power of DP**: a
small toolkit of recurrence patterns handles huge problem families.
''',
        "confusion_notes": [
            {
                "question": "Why is `climb(0) = 1` (one way), not 0?",
                "answer": r'''
Because the **empty sequence of moves** is itself one valid way
to "stay" at step 0. There is exactly one way to do nothing.

This is the same convention as `0! = 1` and `sum of empty list
= 0` — pick a base value that makes the recurrence work out.

Walk through `climb(2)`:
- `climb(2) = climb(1) + climb(0)`.
- `climb(1) = 1` (one way: take a 1-step).
- `climb(0)` should be 1, so `climb(2) = 1 + 1 = 2`. Correct
  (paths: `1+1` and `2`).

If we used `climb(0) = 0`, we would get `climb(2) = 1 + 0 = 1`
— wrong. The empty path has to count as "one way to stay still"
for the recurrence to produce the right answer at the boundary.

There is a subtle alternative framing: define `climb(n) = `
"number of distinct walks ending at step `n`". A walk ending at
step 0 consists of zero moves. There is exactly one such walk
(the empty one). Hence `climb(0) = 1`.

This is one of those small philosophical decisions that recur
throughout DP: **what is the base value for the "no work has
been done" subproblem?** Get it right and the rest is
mechanical; get it wrong and the algorithm is off by one
everywhere.
''',
            },
            {
                "question": "Why does this have the same answers as Fibonacci?",
                "answer": r'''
Because the recurrence `climb(n) = climb(n - 1) + climb(n - 2)`
is **structurally identical** to the Fibonacci recurrence
`F(n) = F(n - 1) + F(n - 2)`. Only the base values differ
slightly.

- `climb(0) = 1, climb(1) = 1`. Sequence: `1, 1, 2, 3, 5, 8, ...`.
- `F(0) = 0, F(1) = 1`. Sequence: `0, 1, 1, 2, 3, 5, 8, ...`.

So `climb(n) = F(n + 1)` — the climbing-stairs sequence is just
Fibonacci shifted by one index.

That equivalence is more than trivia. It tells you that two
seemingly different counting problems are the **same problem
underneath**. Many DP problems hide this kind of equivalence;
recognizing them is one of the high-leverage skills.

The reason the recurrence appears: every walk to step `n` ends
with either a 1-step (from step `n - 1`) or a 2-step (from
step `n - 2`). Those two sets of walks are disjoint (the last
move differs) and exhaustive (no other move is possible). So
the count of walks to `n` is the sum of the counts to `n - 1`
and `n - 2`.

This "partition by the last decision" argument is the bread-
and-butter of combinatorial DP. Whenever you can describe a
solution by its last decision, the recurrence usually splits
into a small number of cases keyed by that decision.
''',
            },
            {
                "question": "Why does the space-optimized version work? What about `dp[0]`?",
                "answer": r'''
Because the recurrence at index `i` only touches `dp[i - 1]`
and `dp[i - 2]`. We never need any value older than two steps
back, so we can throw it away.

In the full-table version, we allocate `dp = [0] * (n + 1)`,
fill `dp[0] = dp[1] = 1`, then compute `dp[i]` for `i = 2..n`.
After computing `dp[i]`, we never look at `dp[i - 2]` again.

So instead of an array, we maintain two scalars: `prev2` (the
value at `i - 2`) and `prev1` (the value at `i - 1`). Each
iteration computes the new value and **slides the window**:

```python
prev2, prev1 = prev1, prev1 + prev2
```

After this assignment, `prev1` holds what was just computed
(the new `dp[i]`), and `prev2` holds the previous `prev1`
(which is `dp[i - 1]`, exactly what `prev2` should be for the
next iteration).

`dp[0]` does not exist anymore — its value (1) was used once,
when computing `dp[2]`, and then discarded. We do not lose
information because we **always slide the window forward**, and
the window only ever needs to remember the last two values.

This space optimization generalizes to any DP whose recurrence
depends on a fixed number of recent values. House robber needs
2 scalars; Tribonacci needs 3; LIS does not optimize this way
because its recurrence touches many earlier values.

The rule of thumb: **count how many earlier indices the
recurrence reads from**. Keep exactly that many scalars.
''',
            },
            {
                "question": "When should I use memoization vs tabulation?",
                "answer": r'''
Both are correct and compute the same answers. The differences
are stylistic and operational.

**Memoization (top-down)** keeps the recursion as written and
adds a cache:

```python
@lru_cache(maxsize=None)
def climb(n):
    if n <= 1:
        return 1
    return climb(n - 1) + climb(n - 2)
```

Pros: closest to the natural recurrence; easier to write when
the recurrence is complex; you only compute the subproblems
actually needed.

Cons: uses recursion (can hit Python's recursion limit on deep
inputs); has function-call overhead; harder to space-optimize.

**Tabulation (bottom-up)** computes the table iteratively from
the base cases up:

```python
def climb(n):
    if n <= 1: return 1
    dp = [0] * (n + 1)
    dp[0] = dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

Pros: no recursion (no stack limit issue); easier to space-
optimize (you can see exactly which earlier values you need);
typically faster constants because of fewer function calls.

Cons: you have to choose the iteration order yourself; computes
every subproblem from `0` up to `n`, even ones the recursion
would not have visited.

**Practical advice**: write memoization first (recursion is
easier to invent). Convert to tabulation if you need to space-
optimize, avoid recursion limit, or get the small constant-
factor speedup. Both are valuable to know.
''',
            },
        ],
        "summary": r'''
**Pattern**: `dp[i] = dp[i - 1] + dp[i - 2]` — Fibonacci-style 1D
DP.

**Lesson**: the canonical refinement path is naive → memoize →
tabulate → space-optimize. Each step is mechanical once you have
the recurrence.

**Recognize next time**: any "ways to reach state n given small
predecessors" problem. Frog jump, house robber, decode ways are
direct siblings.
''',
    },
    {
        "id": "lcs",
        "title": "Longest Common Subsequence",
        "step_id": 16,
        "lecture_id": 5,
        "difficulty": "medium",
        "tags": ["dp", "strings", "subsequence"],
        "what_this_teaches": (
            "The **2D DP on two strings** template. Once you can fill "
            "the `dp[i][j]` table for LCS, you have the muscle for "
            "edit distance, distinct subsequences, shortest common "
            "supersequence, and wildcard matching — all variations on "
            "the same recurrence."
        ),
        "pattern": "dp[i][j] = match? 1 + dp[i-1][j-1] : max(dp[i-1][j], dp[i][j-1]).",
        "prerequisite_lessons": ["dp", "strings"],
        "prerequisite_problems": ["climbing-stairs", "fibonacci-number"],
        "next_problems": [
            "print-lcs",
            "longest-common-substring",
            "longest-palindromic-subseq",
            "edit-distance",
            "shortest-common-supersequence",
            "wildcard-matching",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 16 (DP on Strings)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 1143 — Longest Common Subsequence",
                "url": "https://leetcode.com/problems/longest-common-subsequence/",
            },
        ],
        "understanding": r'''
Given two strings `text1` and `text2`, return the length of their
**longest common subsequence (LCS)**. A subsequence keeps relative
order but allows skipping characters. So `"ace"` is a subsequence
of `"abcde"`, while `"aec"` is not.

Example: `text1 = "abcde"`, `text2 = "ace"` → LCS is `"ace"`, length 3.

LCS is the **mother of all DP-on-strings problems**. Edit distance,
distinct subsequences, shortest common supersequence, and many
others are variations or extensions of LCS.
''',
        "brute_force": {
            "explanation": r'''
Recursion: at each step, look at the last character of each string:

- If they match, the LCS includes that character and is `1 +
  LCS(text1[:-1], text2[:-1])`.
- If they don't match, the LCS is the longer of `LCS(text1[:-1],
  text2)` and `LCS(text1, text2[:-1])`.

The recursion tree has many overlapping subproblems, so it is
exponential without memoization but linear once we cache.
''',
            "code": r'''def lcs_recursive(a: str, b: str) -> int:
    def go(i: int, j: int) -> int:
        # Base case: one of the strings is empty.
        if i == 0 or j == 0:
            return 0
        if a[i - 1] == b[j - 1]:
            # Characters match; the LCS includes them.
            return 1 + go(i - 1, j - 1)
        # Characters differ; try dropping one character from each side.
        return max(go(i - 1, j), go(i, j - 1))
    return go(len(a), len(b))
''',
            "complexity": (
                "**Time**: *O(2^(n+m))* without memoization. "
                "**Space**: *O(n + m)* recursion."
            ),
        },
        "thought_process": r'''
Define `dp[i][j]` = LCS length of the prefixes `a[0..i-1]` and
`b[0..j-1]`. The recurrence:

- If `a[i-1] == b[j-1]`: `dp[i][j] = 1 + dp[i-1][j-1]`.
- Else: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`.

Base: `dp[0][j] = 0` and `dp[i][0] = 0` (one prefix is empty).

We fill a 2D table of size `(n+1) × (m+1)`. *O(nm)* time and
space.

The mental model: at each cell `(i, j)`, we are asking "what is
the LCS of these two prefixes?". The recurrence chooses the better
of three options: extend the diagonal on a match, or copy the best
of the two adjacent cells.

The 2D table is one of the most viscerally rewarding DP structures.
Drawing it on paper for `"abcde"` and `"ace"` clarifies the whole
thing in two minutes.
''',
        "optimized": {
            "explanation": r'''
2D bottom-up DP. *O(nm)* time and space.
''',
            "code": r'''def lcs(a: str, b: str) -> int:
    n, m = len(a), len(b)
    # dp[i][j] = LCS length of a[..i-1] and b[..j-1].
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                # Match: extend the diagonal.
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                # No match: drop one character from one side.
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[n][m]
''',
            "complexity": "**Time**: *O(nm)*. **Space**: *O(nm)*.",
        },
        "deep_concept": r'''
LCS is the most generalizable DP pattern in this curriculum. Many
problems map directly to it:

- **Edit distance**: a 2D DP almost identical to LCS, with the
  recurrence allowing insertions, deletions, and substitutions.
- **Shortest common supersequence (SCS)**: SCS length = n + m -
  LCS length. The actual SCS string is reconstructed from the DP
  table.
- **Longest palindromic subsequence (LPS)**: LPS(s) = LCS(s,
  reverse(s)).
- **Distinct subsequences**: a count-version of LCS.
- **Wildcard matching, regex matching**: 2D DP on the same shape.

The 2D table itself can be **space-optimized to O(min(n, m))** by
keeping only two rows (or even one row with care). The technique
generalizes to many DP-on-strings problems.

The takeaway: invest in LCS. Master the 2D recurrence, the
reconstruction (walking back through the table), and the space
optimization. The investment compounds across many later problems.
''',
        "confusion_notes": [
            {
                "question": "Why does the table have dimensions `(n + 1) × (m + 1)` instead of `n × m`?",
                "answer": r'''
Because the extra row and column hold the **empty-prefix** base
cases. `dp[0][j]` represents "LCS of an empty string and the
first `j` characters of `b`" — that LCS is 0 by definition.
Similarly `dp[i][0] = 0` for "LCS of first `i` chars of `a` and
empty string."

Having an explicit empty-prefix row/column means we never have
to special-case the boundary inside the loop. The loop can
simply look at `dp[i - 1][j - 1]`, `dp[i - 1][j]`, or `dp[i][j
- 1]` without worrying about going out of bounds — those slots
exist and hold 0.

Without the extra row/column, we would have to wrap every
`dp[i - 1][j - 1]` access in `if i > 0 and j > 0`. The code
would be cluttered with edge-case checks.

The general lesson: **expand your DP table by one in each
dimension to absorb the boundary**. This trick recurs in edit
distance, distinct subsequences, and virtually every DP-on-
strings problem.

Pay one row and one column of memory; save a forest of `if`
statements. Excellent trade.
''',
            },
            {
                "question": "Why `a[i - 1]` and `b[j - 1]` instead of `a[i]` and `b[j]`?",
                "answer": r'''
Because the row index `i` represents *"the first `i` characters
of string `a`"*, and the **last** character of that prefix lives
at array index `i - 1` (since strings are zero-indexed).

If `a = "abcde"` and `i = 3`, "the first 3 characters" is
`"abc"`, whose last character is `'c'`, at index 2 = `i - 1`.

This off-by-one is the price we pay for the empty-prefix row.
The trade-off is mild — once you understand the convention, the
`-1` becomes invisible. But if you forget it and write `a[i]`,
the code reads the *wrong* character at every comparison.

There are two equivalent styles:
- **`dp[i][j]` = LCS of `a[..i-1]` and `b[..j-1]`** (our style;
  uses `a[i-1]`).
- **`dp[i][j]` = LCS of `a[..i]` and `b[..j]`** (1-indexed
  string view, uses `a[i]` but requires careful handling of
  `dp[0][.]`).

Pick the first style; it matches Python's natural indexing and
is what most textbooks use.
''',
            },
            {
                "question": "Why does the 'no match' branch take `max(dp[i-1][j], dp[i][j-1])` and not also `dp[i-1][j-1]`?",
                "answer": r'''
Because `dp[i - 1][j - 1]` is **never larger** than the other
two — including it in the max is harmless but redundant.

Recall that `dp[i][j]` represents the LCS of two prefixes.
`dp[i - 1][j - 1]` is the LCS of *both prefixes shortened by
one*. Compared to `dp[i - 1][j]` (only `a` shortened),
`dp[i - 1][j - 1]` is the LCS over a *subset* of the characters
— it cannot possibly be longer.

Formally: `dp[i - 1][j - 1] <= dp[i - 1][j]` because the LCS
of shorter prefixes cannot exceed the LCS of longer prefixes.
Same for `dp[i - 1][j - 1] <= dp[i][j - 1]`.

So `max(dp[i - 1][j], dp[i][j - 1])` already includes whatever
`dp[i - 1][j - 1]` could contribute. The two-way max is
sufficient.

There is a subtle point: in **edit distance**, all three cells
*do* appear in the recurrence (insert, delete, substitute).
That is because edit distance counts operations differently
than LCS counts characters. The two recurrences look similar
but have different combine logic.

For LCS specifically: just the two-way max. Save yourself a
comparison.
''',
            },
            {
                "question": "How do I reconstruct the actual LCS string, not just its length?",
                "answer": r'''
**Walk back through the table** from `dp[n][m]` to `dp[0][0]`,
choosing the direction that produced each cell's value.

```python
def lcs_string(a, b):
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    # ... fill the table the usual way ...
    # Reconstruct.
    result = []
    i, j = n, m
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            result.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return ''.join(reversed(result))
```

Logic:
- If `a[i - 1] == b[j - 1]`, that character is in the LCS.
  Move diagonally.
- Otherwise, move in the direction of the larger neighbor
  (whichever produced this cell's value).

We collect characters in reverse order (because we walk
backward) and reverse at the end.

Time: `O(n + m)` for the reconstruction (the longest path
through the table is `n + m`). Space: `O(LCS length)` for the
result, plus the `O(nm)` table we already had.

This reconstruction pattern — walk back through the DP table
following the choices that produced each cell — works for
nearly every DP problem. Edit distance reconstruction gives the
actual edit operations. Shortest path DP reconstructs the
path. The technique is universal.
''',
            },
        ],
        "summary": r'''
**Pattern**: 2D DP indexed by prefix lengths of both strings.

**Lesson**: at each cell, three transitions — match (extend the
diagonal), or drop a character from one side.

**Recognize next time**: any "common pattern between two strings"
problem. LCS, edit distance, SCS, distinct subsequences, regex
matching — all the same shape.
''',
    },
]
