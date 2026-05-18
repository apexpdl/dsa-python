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
