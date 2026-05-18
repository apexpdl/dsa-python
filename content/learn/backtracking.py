"""Backtracking — try, undo, try something else."""

LESSON = {
    "id": "backtracking",
    "title": "Backtracking — Try Every Option, Cleanly",
    "tags": ["recursion", "backtracking"],
    "summary": (
        "Backtracking is recursion plus a notebook eraser. You explore "
        "a choice, recurse deeper, and undo your mark before trying "
        "the next choice. It's how we solve N-Queens, Sudoku, "
        "permutations, and combinations."
    ),
    "body": r'''
## The maze analogy

Picture yourself in a maze with a piece of chalk. At each junction
you have a few directions. You mark your choice on the floor, walk a
bit, and either find the exit or hit a dead end. On a dead end, you
walk back to the last junction, **erase** your old mark, and try a
different direction. If every option dead-ends, you walk back
further, erase again, and try yet again.

That is backtracking, exactly. You **try a choice**, **recurse**, and
when you come back you **undo** the choice so the next sibling
attempt starts from a clean slate.

## The skeleton

Almost every backtracking problem follows the same template:

```python
def backtrack(state, choices, results):
    if is_solution(state):
        results.append(snapshot(state))   # save a copy, not the live state
        return
    for choice in choices:
        if not valid(state, choice):
            continue
        apply_choice(state, choice)       # try it
        backtrack(state, next_choices(state, choice), results)
        undo_choice(state, choice)        # erase the mark
```

Drill that shape into your fingers. Once you have it, half the
recursion lectures of Step 7 collapse.

## Example: generate all subsets

```python
def subsets(nums: list[int]) -> list[list[int]]:
    out, current = [], []
    def go(i: int) -> None:
        if i == len(nums):
            out.append(current[:])    # snapshot
            return
        # Choice 1: skip nums[i]
        go(i + 1)
        # Choice 2: take nums[i]
        current.append(nums[i])
        go(i + 1)
        current.pop()                  # undo
    go(0)
    return out
```

The recursion tree has 2^n leaves — one for every possible subset.
The shape of the algorithm exactly matches the structure of the
question.

## Example: generate all permutations

```python
def permutations(nums: list[int]) -> list[list[int]]:
    out, current = [], []
    used = [False] * len(nums)
    def go() -> None:
        if len(current) == len(nums):
            out.append(current[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            current.append(nums[i])
            go()
            current.pop()
            used[i] = False
    go()
    return out
```

A permutation differs from a subset because **order matters** and
**all** elements must be used. The "used" array tracks which elements
are currently in our partial permutation.

## Example: N-Queens

> Place N queens on an N×N board so that none attack each other.

The trick: place exactly one queen per row. So we walk row by row.
At each row we try every column, check that the column and both
diagonals are free, place the queen, recurse, then remove the queen.

```python
def solve_n_queens(n: int) -> list[list[str]]:
    cols = set()
    diag1 = set()           # row - col
    diag2 = set()           # row + col
    board = [["."] * n for _ in range(n)]
    out = []

    def go(row: int) -> None:
        if row == n:
            out.append(["".join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            cols.add(col); diag1.add(row - col); diag2.add(row + col)
            board[row][col] = "Q"
            go(row + 1)
            board[row][col] = "."
            cols.remove(col); diag1.remove(row - col); diag2.remove(row + col)

    go(0)
    return out
```

Look at the symmetry: every `add` has a matching `remove`. Every
`"Q"` placement has a matching restoration to `"."`. That is the
backtracking discipline. Every change must be undone before we
return.

## Pruning — the real speedup

A naive backtracker tries every combination, which is exponential.
**Pruning** is the art of recognizing "this branch cannot possibly
lead to a solution" and abandoning it early. In N-Queens, our
attack-set check is pruning. In Sudoku, the constraint "this digit
already appears in this row/column/box" is pruning. In subset sum,
"current total already exceeds target" is pruning.

The same algorithm with the same skeleton can run in milliseconds or
in days, depending on how aggressive your pruning is.

## The "two-state" version: state passed by argument

You can carry state as function arguments instead of mutating shared
data:

```python
def subsets(nums: list[int]) -> list[list[int]]:
    out = []
    def go(i: int, current: list[int]) -> None:
        if i == len(nums):
            out.append(current)        # no copy needed; we never mutate
            return
        go(i + 1, current)
        go(i + 1, current + [nums[i]])  # new list per branch
    go(0, [])
    return out
```

This style is clearer but allocates more — a fresh list per branch.
The mutation+undo style is faster on tight problems. Pick the
clarity you need.

## Common beginner mistakes

**Mistake 1: forgetting to snapshot.** When you save `current` to the
results, you must save a **copy** (`current[:]`). Otherwise every
saved result points at the same evolving list, and at the end they
are all the same final state.

**Mistake 2: forgetting to undo.** Every mutation must be undone
before the function returns. If you forget, sibling branches see
each other's progress and the answer is garbage.

**Mistake 3: not pruning.** A backtracking solution without pruning
is correct but slow. Ask yourself at every step: *"is there any way
to detect right now that this branch is hopeless?"*

**Mistake 4: using the wrong return value.** Backtracking functions
often return `None` and accumulate results into a closed-over list.
Beginners sometimes accidentally return early after finding one
solution. Decide up front whether you want all solutions or any one.

**Mistake 5: recurring on the same subproblem repeatedly.** If two
different choice sequences lead to the same state, you may be
unintentionally exploring it twice. For problems where this matters
(many DP problems in disguise), memoization is the fix.

## The mental model

Backtracking is "depth-first search of a tree of choices, with
undo". You only ever have one path live at a time; the rest of the
tree is just future work. Whenever you see "find all ___", "is there
any ___", or "best ___ over all possible ___", reach for the
backtracking skeleton first.

Once you can write the skeleton without thinking, you have unlocked
the entire subsequence / subset / permutation lecture of Step 7 — and
half of the hard problems start to look mechanical.
''',
}
