"""Step 7 — Recursion patterns."""
from __future__ import annotations

PROBLEMS: list[dict] = [
    {
        "id": "print-all-subsequences",
        "title": "Print All Subsequences (Power Set)",
        "step_id": 7,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["recursion", "backtracking", "subsequences"],
        "understanding": r'''
Given an array (or string), print every **subsequence**. A
subsequence is any subset obtained by deleting zero or more
elements without changing the order of the rest.

For `[1, 2, 3]` the subsequences are:

`[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]`.

That is **8 = 2³ subsequences**, one for each subset of indices.
This is the **power set**.

Subsequences are the gateway to recursion's "take or skip" pattern.
Once you have it, you unlock subset sum, combination sum, partition
problems, and a lot of DP.
''',
        "brute_force": {
            "explanation": r'''
Two natural approaches:

1. **Recursive take-or-skip**: at each index, recurse twice — once
   without including the element, once with. Build up the result
   list and snapshot it at the leaves.
2. **Bitmask iteration**: for each integer `mask` from `0` to
   `2^n - 1`, the `i`-th bit of `mask` decides whether to include
   `arr[i]`.

Both are *O(2^n × n)*. The recursive version is the foundational
shape we should learn first.
''',
            "code": r'''def all_subseqs(arr: list[int]) -> list[list[int]]:
    out: list[list[int]] = []
    current: list[int] = []

    def go(i: int) -> None:
        # Base case: past the last index — snapshot the current
        # choice (must be a copy, otherwise all snapshots share state).
        if i == len(arr):
            out.append(current[:])
            return
        # Choice 1: skip arr[i].
        go(i + 1)
        # Choice 2: include arr[i]. Add, recurse, then UNDO.
        current.append(arr[i])
        go(i + 1)
        current.pop()

    go(0)
    return out


def all_subseqs_bitmask(arr: list[int]) -> list[list[int]]:
    n = len(arr)
    out = []
    # Each integer from 0 to 2^n - 1 represents a subset: bit i set
    # means "include arr[i]".
    for mask in range(1 << n):
        subset = [arr[i] for i in range(n) if mask & (1 << i)]
        out.append(subset)
    return out
''',
            "complexity": (
                "**Time**: *O(2^n × n)* — exponentially many subsets, "
                "each of size up to n. **Space**: *O(n)* recursion "
                "depth plus output size."
            ),
        },
        "thought_process": r'''
The take-or-skip recursion is the **most important shape in all of
recursion**. Almost every "explore all possibilities" problem is
some variation:

- Subset sum: same shape, plus a sum-equals-target check.
- Combination sum: same shape, plus repetition allowed.
- 0/1 knapsack: same shape, with weight and value tracking.
- Word break: same shape, with substring tests.

The mental model is a **decision tree**: at each level we branch
into "skip" and "take". The tree has `2^n` leaves, each a unique
subset.

The undo step (`current.pop()`) is **backtracking discipline**. We
mutate `current` to record our choice, recurse, and then erase the
mutation before trying the next sibling. Without the undo, the
"skip" branch and the "take" branch would share state and the
algorithm would be wrong.

A second version uses an immutable parameter:

```python
def go(i, current):
    if i == len(arr):
        out.append(current)
        return
    go(i + 1, current)
    go(i + 1, current + [arr[i]])
```

This style is clearer but allocates more (a fresh list per branch).
The mutate+undo style is faster. Both are valid; pick the clarity
you need.

The bitmask version is a beautiful alternative when you want
**iteration** instead of recursion. It is also useful when you
want to enumerate subsets in lexicographic-by-mask order. For
*O(n)* alphabet sizes it is hard to beat.
''',
        "deep_concept": r'''
The "take or skip" recursion has a beautiful interpretation in
terms of **binary numbers**. Each path from root to leaf in the
recursion tree corresponds to a binary string of length `n`: `0`
for "skip", `1` for "take". The path is exactly the binary
representation of an integer from 0 to `2^n - 1`. That equivalence
is why the bitmask version exists and produces the same set of
subsets.

It also explains why "subset" and "binary number" feel so
interchangeable in algorithm discussions. They are literally the
same object viewed from two angles.

The same decision-tree shape becomes **DP** when subsets care only
about an aggregate (sum, weight, etc.) rather than the specific
elements: the leaves with the same aggregate collapse into one
state, and we memoize.
''',
        "summary": r'''
**Pattern**: take-or-skip recursion with undo.

**Lesson**: every subset is a unique path through a binary
decision tree of depth n. The recursion explores all `2^n` paths.

**Recognize next time**: subset, subsequence, combination, partition
problems. They all start with this skeleton; the leaves and the
branching rules vary.
''',
    },
    {
        "id": "n-queens",
        "title": "N-Queens",
        "step_id": 7,
        "lecture_id": 3,
        "difficulty": "hard",
        "tags": ["recursion", "backtracking", "constraints"],
        "understanding": r'''
Place `N` queens on an `N × N` chessboard so that no two queens
attack each other. Queens attack along rows, columns, and both
diagonals. Return all distinct configurations.

For `N = 4`, there are exactly 2 solutions. For `N = 8`, there are
92. For `N = 1`, there is 1. For `N = 2` and `N = 3`, there are
none.

N-Queens is the canonical "backtracking with constraints" problem.
It teaches you to **prune** aggressively using simple data
structures.
''',
        "brute_force": {
            "explanation": r'''
A truly naive brute force places a queen in every cell of every
possible combination — that is `C(N², N)` configurations, far too
many. Any sensible approach uses the structure of the problem:
**exactly one queen per row**. So the search is over choosing one
column per row, which is `N^N` configurations in the worst case
before pruning.

The crucial insight is that as we place queens row by row, we can
prune immediately whenever a new queen attacks any earlier queen.
''',
            "code": r'''def solve_n_queens_naive(n: int) -> list[list[str]]:
    # Naive: try every combination of one column per row, then check.
    out = []
    cols = [0] * n

    def check() -> bool:
        for i in range(n):
            for j in range(i + 1, n):
                if cols[i] == cols[j]:
                    return False
                if abs(cols[i] - cols[j]) == abs(i - j):
                    return False
        return True

    def go(row: int) -> None:
        if row == n:
            if check():
                out.append([
                    "." * c + "Q" + "." * (n - c - 1) for c in cols
                ])
            return
        for c in range(n):
            cols[row] = c
            go(row + 1)

    go(0)
    return out
''',
            "complexity": (
                "**Time**: *O(N^N)* without pruning. **Space**: *O(N)*."
            ),
        },
        "thought_process": r'''
The optimized version maintains three sets:

- `cols` — columns already used by an earlier queen.
- `diag1` — values of `row - col` already used. (Top-left to
  bottom-right diagonals all have constant `row - col`.)
- `diag2` — values of `row + col` already used. (Top-right to
  bottom-left diagonals all have constant `row + col`.)

When placing a queen at `(row, col)`, we check whether `col`,
`row - col`, and `row + col` are in their respective sets. If all
three are free, the queen is safe. We add the three values to the
sets, recurse to the next row, and **undo** all three additions
afterward.

The pruning is enormous. Each set membership check is *O(1)*, and
we abandon entire branches the moment any conflict appears. In
practice this lets us solve `N = 12` and `N = 13` in well under a
second.

The lesson is **pick good constraint encodings**. The "diagonal
has constant `row - col`" observation is the unlock — without it,
checking diagonals every time would be a slow linear scan.
''',
        "optimized": {
            "explanation": r'''
Backtracking with three sets for constant-time conflict checks.
''',
            "code": r'''def solve_n_queens(n: int) -> list[list[str]]:
    cols: set[int] = set()
    diag1: set[int] = set()       # row - col
    diag2: set[int] = set()       # row + col
    board = [["."] * n for _ in range(n)]
    out: list[list[str]] = []

    def go(row: int) -> None:
        if row == n:
            # Snapshot the board as a list of strings.
            out.append(["".join(r) for r in board])
            return
        for col in range(n):
            # Three constant-time checks for column and both diagonals.
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            # Place the queen and record the three constraints.
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            board[row][col] = "Q"
            go(row + 1)
            # Undo — every action matched by an undo.
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
            board[row][col] = "."

    go(0)
    return out
''',
            "complexity": (
                "**Time**: still exponential in the worst case, but "
                "with extremely aggressive pruning. **Space**: *O(N²)* "
                "for the board, *O(N)* for the recursion."
            ),
        },
        "deep_concept": r'''
N-Queens teaches the three lessons of practical backtracking:

1. **Symmetry**: by fixing "one queen per row", we eliminate row
   conflicts without any work. Good problem decomposition saves
   constraints.
2. **Constraint encoding**: choose data structures that make
   conflict checks *O(1)*. The diagonal trick is the iconic
   example.
3. **Discipline of undo**: every `set.add` is matched by a
   `set.remove`. Every board mutation is matched by a restoration.
   Asymmetric add/undo is the #1 source of bugs in backtracking.

The same recipe handles Sudoku, M-coloring, and Rat in a Maze. The
specifics change; the skeleton does not.
''',
        "summary": r'''
**Pattern**: backtracking with explicit constraint sets.

**Lesson**: choose constraint encodings (here, three sets) that
permit *O(1)* conflict checks. Discipline every choice with a
matching undo.

**Recognize next time**: any "place N items obeying constraints"
problem. Sudoku, M-coloring, Knight's tour — all the same shape.
''',
    },
]
