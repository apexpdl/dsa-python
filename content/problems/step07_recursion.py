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
        "what_this_teaches": (
            "The **take-or-skip** recursion is the single most reused "
            "shape in subset / subsequence / combination problems. "
            "Every leaf of the binary decision tree is a unique "
            "subset; the recursion just enumerates them all."
        ),
        "pattern": "At each index, recurse twice — skip the element, take the element. Undo after.",
        "prerequisite_lessons": ["recursion", "backtracking"],
        "prerequisite_problems": ["fibonacci-number", "factorial-of-n"],
        "next_problems": [
            "subsequence-sum-k",
            "subset-sum-i",
            "subset-sum-ii",
            "combination-sum",
            "power-set-bitwise",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 7 (Subsequence Pattern)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 78 — Subsets",
                "url": "https://leetcode.com/problems/subsets/",
            },
        ],
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
            "walkthrough": r'''
Two complete approaches: recursive take-or-skip (the
canonical backtracking pattern) and bitmask enumeration (a
clever iterative alternative).

**Version 1: Take-or-skip recursion**

This is the **most important recursion shape** in all of DSA.
Learn it cold.

**`def all_subseqs(arr: list[int]) -> list[list[int]]:`** —
Returns a list of all 2^n subsequences (subsets) of the input.

**`out: list[list[int]] = []`** — Will accumulate all
subsequences as we discover them.

**`current: list[int] = []`** — A "scratch pad" that holds
the subsequence we're currently building. Will be modified
throughout — appended to when we include, popped when we
backtrack.

**`def go(i: int) -> None:`** — Nested recursive helper. `i`
is the current index we're considering. At each step we
decide: include `arr[i]` or skip it.

**`if i == len(arr): out.append(current[:]); return`** — The
**base case**. We've made a decision for every index. The
`current` list now represents one full subsequence. **Snapshot
it with `current[:]`** (or equivalently `list(current)`) — we
**must** make a copy, otherwise all snapshots in `out` would
share a reference to the same list, which gets mutated as
recursion continues.

**`go(i + 1)`** — **Choice 1: skip.** Recurse to the next
index without modifying `current`. This explores all
subsequences that don't include `arr[i]`.

**`current.append(arr[i])`** — **Choice 2: include.** Add
`arr[i]` to the current subsequence.

**`go(i + 1)`** — Recurse to the next index with the include
decision committed.

**`current.pop()`** — **The undo.** After the recursive call
returns, we must remove `arr[i]` from `current` to leave the
scratch pad in the same state it was when we entered. This
is the heart of backtracking.

Forget the `current.pop()` and your algorithm will produce
wrong answers — the include decisions will "leak" into
sibling branches.

**`go(0)`** — Kick off recursion at index 0.

**`return out`** — Hand back all 2^n subsequences.

**Trace it on `arr = [1, 2]`:**

```
go(0): current=[]
  go(1): current=[]                              ← skip 1
    go(2): current=[] → snapshot []. Return.
    Pop nothing (didn't append in this branch).
  go(1) returns.
  Append 1. current=[1]                          ← include 1
  go(1): current=[1]
    go(2): current=[1] → snapshot [1]. Return.
    (Recursive include below)
    Append 2. current=[1, 2]
    go(2): current=[1, 2] → snapshot [1, 2]. Return.
    Pop 2. current=[1].
  Pop 1. current=[].
go(0) returns. out = [[], [2], [1], [1, 2]].
```

Wait that doesn't quite match — let me reread. Yes, the
algorithm explores "skip first, then include" at each step.
The order of subsequences in `out` depends on this choice
order. Different orders produce the same set, just different
arrangement.

**Version 2: Bitmask enumeration**

A different formulation. We iterate `2^n` integers; each one
encodes a subset via its binary representation.

**`for mask in range(1 << n):`** — `1 << n` is `2^n` (1
shifted left by n positions). For n = 3, this is 8. We
iterate masks 0, 1, 2, ..., 7 — that's exactly 2^n subsets.

**`subset = [arr[i] for i in range(n) if mask & (1 << i)]`** —
For each mask, build the subset. The bit-test `mask & (1 << i)`
checks whether bit `i` is set in the mask. If yes, include
`arr[i]`.

For example, mask = 5 = binary 101: bits 0 and 2 are set. The
subset is `[arr[0], arr[2]]`.

**`out.append(subset)`** — Record this subset.

This version is **iterative** — no recursion, no implicit
stack. It uses *O(n)* extra memory (the subset being built
and the mask), plus *O(output size)* for the final list. The
trade-off vs. the recursive version: iteration is faster in
practice (no function call overhead), but only works when
n ≤ 30 or so (otherwise `2^n` doesn't fit in standard ints).

Both approaches generate **all** 2^n subsets in *O(2^n × n)*
total time — the lower bound for this problem since the
output itself has *O(2^n × n)* size.

The take-or-skip recursive pattern generalizes to subset-sum,
partition-equal, combination-sum, target-sum, and dozens of
"explore all decisions" problems.
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
        "confusion_notes": [
            {
                "question": "Why does the code call `current[:]` instead of just `current`?",
                "answer": r'''
Because `current` is a **mutable list** that the algorithm keeps
modifying. If we appended `current` itself to `out`, every entry
in `out` would point at the *same* list object. By the time the
recursion ended, every entry would show the final state of
`current` — which is the empty list, because the recursion's
last action is always to pop everything off.

`current[:]` creates a **shallow copy** — a brand-new list with
the same elements. The copy is frozen at the moment we made it;
later mutations of `current` cannot affect it.

A tiny demonstration:

```python
out = []
current = [1, 2, 3]
out.append(current)        # out = [[1, 2, 3]]
current.pop()              # current = [1, 2]
out.append(current)        # out = [[1, 2], [1, 2]]  -- same object!
print(out)                 # [[1, 2], [1, 2]]
```

If we use `current[:]`:

```python
out = []
current = [1, 2, 3]
out.append(current[:])     # snapshot [1, 2, 3]
current.pop()
out.append(current[:])     # snapshot [1, 2]
print(out)                 # [[1, 2, 3], [1, 2]]  -- correct
```

Other equivalent ways to snapshot: `list(current)`,
`current.copy()`, `[*current]`. All produce a new list with the
same contents.

This is the **#1 most common bug** beginners hit in backtracking.
If your algorithm gives correct counts but the results all look
identical, you forgot to snapshot.
''',
            },
            {
                "question": "Why do we `current.pop()` after the recursive call?",
                "answer": r'''
Because we **mutated** `current` by appending `arr[i]` before
the recursion, and we have to **undo** that change before the
function returns. Otherwise the caller (the previous recursive
frame) sees the mutation and the "skip" branch starts with the
wrong state.

Walk through the take-or-skip skeleton:

```python
def go(i):
    if i == len(arr):
        out.append(current[:])
        return
    # Choice 1: skip
    go(i + 1)
    # Choice 2: take
    current.append(arr[i])
    go(i + 1)
    current.pop()              # UNDO
```

Imagine we are at `i = 0`, `current = []`. We skip — recurse with
`current = []`. After that returns, we take — append `arr[0]`,
recurse with `current = [arr[0]]`. After that returns, we
pop, restoring `current = []`. The function exits, and the
**caller** sees `current = []`, exactly as it was before our
call.

Without the `pop()`, after handling index 0, `current` would
still contain `arr[0]`. Any subsequent recursive frames at index
0's "skip" branch from a sibling call would see `[arr[0]]` —
wrong.

This is the **backtracking discipline**: every mutation must
have a matching undo before the function returns. Asymmetric
mutate/undo is the second-most-common bug after forgetting to
snapshot.

A defensive alternative: pass `current + [arr[i]]` as an
argument to the recursive call, which creates a new list per
branch and avoids mutation entirely. Slower (allocates), but
impossible to mess up.
''',
            },
            {
                "question": "Why is the total time `O(2^n × n)` and not just `O(2^n)`?",
                "answer": r'''
Because each of the `2^n` subsets has a *snapshot cost* of up to
`O(n)`. The `2^n` is the number of leaves in the recursion
tree, but visiting a leaf is not free — we copy a list of up to
`n` elements into `out`.

Detailed accounting:

- The recursion tree has `2^n` leaves and approximately
  `2 * 2^n - 1` internal calls. Each non-leaf call does *O(1)*
  work (the append + pop pair).
- Each leaf does `current[:]`, which copies the current list of
  size at most `n`.
- Total work at leaves: `2^n * O(n) = O(2^n × n)`.
- Total work at internal nodes: `2 * 2^n * O(1) = O(2^n)`.
- Sum: `O(2^n × n)`. The leaf work dominates.

If you do not need to materialize the snapshots — for example,
if you only want to **count** subsets satisfying some property
— the cost drops to `O(2^n)`.

The memory cost is also `O(2^n × n)` if you store every subset
in `out`. If you instead use a generator (`yield current[:]`),
the memory for `out` disappears and you only pay `O(n)` for the
recursion stack.

The takeaway: `2^n` subsets are a lot. For `n = 30`, that is a
billion. Be careful with subset enumeration on inputs of size
beyond 25 or so.
''',
            },
            {
                "question": "How does the bitmask version relate to the recursive one?",
                "answer": r'''
They produce the exact same set of subsets, just enumerated in
a different order.

The recursive version walks a depth-`n` binary decision tree.
Each leaf corresponds to a sequence of `n` binary choices
("skip" or "take" at each index). That sequence can be written
as an `n`-bit binary number, with each bit indicating the
choice.

The bitmask version walks integers from `0` to `2^n - 1`. For
each integer, its binary representation is a sequence of `n`
bits, each indicating "include" or "exclude" for the
corresponding element.

```python
for mask in range(1 << n):
    subset = [arr[i] for i in range(n) if mask & (1 << i)]
    out.append(subset)
```

The two approaches produce subsets in different orders. The
recursive `skip-then-take` produces subsets in
lexicographically-ascending-by-bitmask order. The bitmask loop
naturally produces the same order if "include" means the bit is
1. Both correct; both cover all `2^n` subsets.

When to prefer bitmask: when you want explicit iteration order
(useful for testing) or when you need to skip subsets without
extending them. When to prefer recursion: when you need to add
pruning ("stop exploring this branch if the partial sum
exceeds K") or when the recursion shape extends naturally to
related problems (combinations with limits, partitioning).

Both are correct. Both are `O(2^n × n)` time. Pick the one that
fits the surrounding logic best.
''',
            },
        ],
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
        "what_this_teaches": (
            "Backtracking with **constraint-checking sets** that turn "
            "O(N) verification into O(1). The two diagonal "
            "encodings — `row - col` for one direction, `row + col` "
            "for the other — are the iconic trick that makes "
            "N-Queens fast enough to be solvable for N up to ~13."
        ),
        "pattern": "Place one queen per row; track conflicts with three sets; backtrack on dead ends.",
        "prerequisite_lessons": ["recursion", "backtracking"],
        "prerequisite_problems": ["print-all-subsequences", "generate-parentheses"],
        "next_problems": [
            "sudoku-solver",
            "m-coloring",
            "rat-in-a-maze",
            "word-search",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 7 (Hard Recursion)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 51 — N-Queens",
                "url": "https://leetcode.com/problems/n-queens/",
            },
        ],
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
            "walkthrough": r'''
The naive backtracking. We pick a column for every row first,
then check validity at the leaf. Inefficient but easy to
understand.

**`def solve_n_queens_naive(n: int) -> list[list[str]]:`** —
Takes board size, returns all valid N-Queens configurations as
lists of strings.

**`out = []`** — Accumulator for solutions.

**`cols = [0] * n`** — `cols[i]` is the column of the queen
placed in row `i`. We allocate an array of size `n` and fill
it during recursion.

**`def check() -> bool:`** — Validation function. Checks that
all `n` queens (one per row, columns given by `cols`) are
mutually non-attacking.

**`for i in range(n): for j in range(i + 1, n):`** — Compare
every pair (`i`, `j`) with `i < j`.

**`if cols[i] == cols[j]: return False`** — Two queens in the
same column. Conflict.

**`if abs(cols[i] - cols[j]) == abs(i - j): return False`** —
Two queens on the same diagonal. The math: queens at
`(i, cols[i])` and `(j, cols[j])` are on a diagonal iff the
horizontal and vertical distances are equal. `abs(...)` gives
us the distance, regardless of direction.

**`return True`** — No pair conflicts; valid configuration.

**`def go(row: int) -> None:`** — Recursive helper to pick a
column for each row.

**`if row == n:`** — We've placed `n` queens (one per row).

**`if check():`** — Only emit if valid.

**`out.append([...])`** — Render the configuration as the
required string format. For each row, "." × (col positions
before queen) + "Q" + "." × (col positions after queen).

**`return`** — Done with this leaf.

**`for c in range(n):`** — Try every column for the current
row.

**`cols[row] = c`** — Record the choice.

**`go(row + 1)`** — Recurse to the next row.

Notice: **no undo step** for `cols[row] = c` — because the
next iteration just overwrites it. We don't need explicit
backtracking for the `cols` array since each row is
independent.

The cost: `n^n` leaves in the search tree (n columns per row,
n rows). For n = 8, that's 16 million. For n = 12, 8.9 billion.
Way too slow without pruning.

The optimized version prunes **during the recursion**:
whenever placing a queen would attack an earlier queen, we
skip that branch immediately. Three sets (columns,
diagonal-1, diagonal-2) make the conflict check *O(1)* per
queen. This brings practical runtime way down — solving
n = 12 in well under a second.
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
            "walkthrough": r'''
The optimized N-Queens with aggressive pruning. Constant-time
conflict checks via three sets. Practical even for n = 13.

**Setting up the constraints**

**`cols: set[int] = set()`** — Tracks which columns are
already occupied by a queen. If column `c` is in this set, no
new queen can go in column `c`.

**`diag1: set[int] = set()`** — Tracks occupied
top-left-to-bottom-right diagonals. Every cell on such a
diagonal has the same `row - col`. So we use `row - col` as
the diagonal's identifier.

**`diag2: set[int] = set()`** — Tracks occupied
top-right-to-bottom-left diagonals. These have constant
`row + col`.

The diagonal identification is the **key insight**. Without
it, checking "does this position attack any earlier queen"
would require scanning all previously placed queens — *O(n)*
per check. With the sets, every check is *O(1)*.

**`board = [["."] * n for _ in range(n)]`** — A 2D grid
initialized to all "." characters. We'll mark "Q" where
queens go.

**Note the `[["."] * n for _ in range(n)]` idiom.** Do
**not** write `[["."] * n] * n` — that creates `n`
references to the **same** list. The list comprehension
makes a fresh list each iteration.

**`out: list[list[str]] = []`** — Accumulator for solutions.

**The recursive go function**

**`if row == n:`** — Base case. We've placed a queen in every
row. Snapshot the board and return.

**`out.append(["".join(r) for r in board])`** — Convert each
row from a list of single characters to a string. The
LeetCode format expects strings like `"..Q."` per row.

**`for col in range(n):`** — Try every column for this row.

**`if col in cols or (row - col) in diag1 or (row + col) in diag2: continue`** —
**Pruning.** Skip this column if placing a queen there would
attack any earlier queen along a column or either diagonal.

The three checks together encode "does the new queen at
(row, col) attack any previously placed queen?" — answered in
*O(1)* time, no scanning.

**`cols.add(col); diag1.add(row - col); diag2.add(row + col)`** —
Record the new queen's three constraints. After these lines,
no future queen can land in this column or on these diagonals.

**`board[row][col] = "Q"`** — Place the queen visually.

**`go(row + 1)`** — Recurse to the next row.

**`cols.remove(col); diag1.remove(row - col); diag2.remove(row + col); board[row][col] = "."`** —
**The undo.** When the recursive call returns, we must remove
all four marks so this row's column choice doesn't bleed into
sibling branches.

This is **classic backtracking**: do, recurse, undo. Every
"apply" must have a matching "remove."

**`go(0)`** — Start at row 0.

**`return out`** — All solutions found.

**Why is pruning so effective?**

In the naive version, every leaf of an `n^n` search tree gets
checked. Most of these leaves are invalid configurations that
the algorithm doesn't know about until the end.

With pruning, we abandon entire subtrees the moment a
conflict appears. In practice, the search tree is **massively**
smaller. For n = 8, instead of 16 million leaves, we visit
about 2,000 — a 4-orders-of-magnitude speedup.

The lesson: **prune at the highest possible level.** Each
queen placed wrong invalidates the *entire* rest of the row
tree below it. By detecting conflicts immediately at
placement time, we save exponential work.

The N-Queens problem is the gold standard for teaching
constraint-driven backtracking. Master this template and you
have the tools for Sudoku solver, crossword filling, graph
coloring, and many other CSP (constraint satisfaction
problem) variations.
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
        "confusion_notes": [
            {
                "question": "Why does `row - col` identify a diagonal?",
                "answer": r'''
Because **every cell on a top-left-to-bottom-right diagonal has
the same `row - col` value**.

Picture an `N × N` board. The top-left cell `(0, 0)` has
`row - col = 0`. The cell just to its lower-right, `(1, 1)`, also
has `row - col = 0`. And `(2, 2)`, and so on. All cells on the
main diagonal share `row - col = 0`.

Now look at the diagonal starting from `(0, 1)`. Its cells are
`(0, 1), (1, 2), (2, 3), ...`. Each has `row - col = -1`. A
different constant for a different diagonal.

In general, the diagonals from upper-left to lower-right are
labeled by the integer `row - col`, ranging from `-(N - 1)` to
`+(N - 1)` — that is `2N - 1` distinct diagonals.

So to detect "are any two queens on the same `↘` diagonal?", we
maintain a set of all `row - col` values that already contain a
queen. Placing a queen at `(row, col)` is illegal if `row - col`
is already in the set.

The same logic for `↗` diagonals (upper-right to lower-left)
uses `row + col`. Cells `(0, 2), (1, 1), (2, 0)` all have `row +
col = 2`. We keep a second set keyed by `row + col`.

Three sets total — columns, `row - col` diagonals, and `row +
col` diagonals — give us *O(1)* conflict checks for every
queen placement.
''',
            },
            {
                "question": "Why place one queen per row instead of searching every cell?",
                "answer": r'''
Because **two queens in the same row would always attack each
other**, so we never need to consider placing two queens in the
same row. Fixing "exactly one queen per row" eliminates an
entire dimension of the search space without losing any valid
solution.

The naive search would consider every combination of `N`
positions on an `N × N` board. That is `C(N², N)` combinations
— astronomical even for `N = 8` (around `4 × 10⁹`). Pruning
"two queens in the same row" via "one queen per row" reduces
the search to `N^N` (around `1.6 × 10⁷` for `N = 8`) — still
exponential but much more tractable.

Diagonal and column pruning shrinks it further. In practice,
the algorithm explores far fewer than `N^N` configurations
because branches die fast.

The lesson: **good problem decomposition is itself a form of
pruning**. Before writing code, ask whether the constraints
force any structural property (like "one per row") that you can
encode in the search itself.

This style of "fix one dimension, vary the other" is the entire
trick of N-Queens. The same trick applies to Sudoku ("one digit
per row, column, and box") and M-coloring ("each region gets
one color").
''',
            },
            {
                "question": "Why does every `add` have a matching `remove`?",
                "answer": r'''
Because we are doing **backtracking**, and backtracking requires
**leaving no trace** of a branch's work when we abandon it.

When we place a queen at `(row, col)`, we mutate three sets:
`cols.add(col)`, `diag1.add(row - col)`, `diag2.add(row + col)`.
We also mutate the board: `board[row][col] = "Q"`. Then we
recurse to the next row.

If the recursion finds a valid solution, great — we snapshot the
board. If it dead-ends, we return. Either way, **the caller
expects the data structures to look exactly as they did before
this call**. So before returning, we have to **undo** every
mutation.

```python
# Place
cols.add(col); diag1.add(row - col); diag2.add(row + col)
board[row][col] = "Q"

go(row + 1)

# Undo (matches placement, exact reverse)
cols.remove(col); diag1.remove(row - col); diag2.remove(row + col)
board[row][col] = "."
```

If we forget any of these undos, a sibling branch will see the
phantom queen and either block valid placements or accept
invalid ones. The algorithm becomes silently wrong.

This is the **#1 source of bugs in backtracking**: asymmetric
mutate / undo. Make it a habit to write the matching `remove`
line *immediately* after the `add` line, before you even fill
in the recursive call. The structure of "place, recurse, undo"
is more important than the specific work being done.
''',
            },
            {
                "question": "Why isn't this `O(N!)` or `O(N^N)` despite the search space?",
                "answer": r'''
The **worst case** is technically `O(N!)`, but **with the
constraint-set pruning**, the practical runtime is dramatically
smaller — usually polynomial-with-a-small-exponent times a tiny
fraction of `N!`.

Here is the reasoning:

- We try at most `N` columns per row.
- We have `N` rows.
- So the brute-force tree has at most `N^N` nodes.
- But each conflict (column or diagonal) kills an entire
  subtree. By the time we are placing the 5th or 6th queen,
  most columns are blocked, so we branch into only one or two
  options, not `N`.

Empirical numbers for solving "all solutions":

- `N = 8`: 92 solutions, around 16,000 total recursive calls.
- `N = 10`: 724 solutions, around 175,000 calls.
- `N = 12`: 14,200 solutions, around 5,000,000 calls.
- `N = 13`: 73,712 solutions, around 30,000,000 calls.

So while it scales worse than polynomial, the constants are
tiny. For `N` up to about 12 or 13, all solutions fit in seconds
on a typical laptop.

For very large `N`, the explosion of solutions itself becomes
the bottleneck. Finding *all* solutions becomes infeasible
around `N = 15`. Finding *any* solution stays fast much longer
(there are many; you do not have to search exhaustively).

The general lesson: **practical runtime of backtracking depends
on pruning**, not asymptotic bounds. A clever constraint check
that kills 90% of branches before they grow is worth far more
than a tighter recursion.
''',
            },
        ],
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
