"""Backtracking — try, undo, try something else."""

LESSON = {
    "id": "backtracking",
    "title": "Backtracking — Try Every Option, Cleanly",
    "tags": ["recursion", "backtracking"],
    "summary": (
        "A full beginner chapter. Backtracking is recursion plus a "
        "notebook eraser. You explore a choice, recurse deeper, and "
        "undo your mark before trying the next choice. It's how we "
        "solve N-Queens, Sudoku, permutations, and combinations."
    ),
    "body": r'''
## 0. What this chapter teaches

Backtracking is recursion with a disciplined undo. The mental
model is small (try a choice, recurse, undo, try the next), but
the discipline is what beginners struggle with most. One missing
undo, one missing snapshot, and the entire algorithm produces
garbage.

This chapter walks through the discipline step by step. By the
end, you should be able to write the backtracking skeleton from
memory and apply it confidently to subsets, permutations,
combinations, N-Queens, and Sudoku.

## 1. The maze analogy

Picture yourself in a maze with a piece of chalk. At each
junction, you have a few directions. You mark your choice on the
floor, walk forward, and either find the exit or hit a dead end.
On a dead end, you walk back to the last junction, **erase** your
old mark, and try a different direction. If every option dead-
ends, you walk back further, erase again, and try yet again.

That is backtracking. You **try a choice**, **recurse**, and
when you come back you **undo** the choice so the next sibling
attempt starts from a clean slate.

The chalk and the eraser are the discipline. Without them, the
maze fills with stale marks and you cannot tell which path you
have already tried.

## 2. The skeleton

Almost every backtracking problem follows the same template.
Memorize it; the details vary, the shape does not.

```python
def backtrack(state):
    if is_solution(state):
        results.append(snapshot(state))   # snapshot, never share
        return
    for choice in choices(state):
        if not is_valid(state, choice):
            continue
        apply_choice(state, choice)       # mark on the floor
        backtrack(state)                  # recurse
        undo_choice(state, choice)        # ERASE before trying the next
```

The five pieces:

1. **Base case**: if we have built a solution, record it and
   return.
2. **Choice enumeration**: list the options available at this
   state.
3. **Validity check**: skip choices that cannot lead to a
   solution.
4. **Apply, recurse, undo**: the mark-recurse-erase trinity.
5. **Snapshot on record**: never store the live state, always
   take a copy.

Drill the shape into your fingers. Once it's there, half of
Step 7 of the curriculum is mechanical.

## 3. Worked example: all subsets

> Print every subset of `[1, 2, 3]`.

At each index, you have two choices: **skip** or **include**.

```python
def subsets(nums):
    out = []
    current = []
    def go(i):
        if i == len(nums):
            out.append(current[:])   # snapshot!
            return
        # Skip nums[i]
        go(i + 1)
        # Include nums[i]
        current.append(nums[i])
        go(i + 1)
        current.pop()                # undo!
    go(0)
    return out
```

For `nums = [1, 2, 3]`, the recursion explores 2³ = 8 leaves,
each a unique subset. The recursion tree has depth 3.

Two beginner traps in this code:
- **`current[:]` not `current`**: snapshot, not reference.
- **`current.pop()` after the include branch**: undo the
  mutation so the caller sees clean state.

Get those two right and the algorithm works. Get either wrong
and the algorithm is silently broken.

## 4. Worked example: permutations

> Print every permutation of `[1, 2, 3]`.

Different from subsets: order matters, and we must use **every**
element exactly once.

```python
def permutations(nums):
    out = []
    current = []
    used = [False] * len(nums)
    def go():
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

The skeleton is identical to subsets: snapshot on solution,
mutate-recurse-undo. The only difference is that we maintain a
`used` array to avoid picking the same element twice, and the
choice enumeration is over indices rather than two branches.

For `n = 3`, we produce 6 = 3! permutations. The recursion tree
has depth 3 and branches factorially.

## 5. Worked example: N-Queens

> Place N queens on an N×N board so no two attack each other.

The "one queen per row" simplification immediately reduces the
search space. At each row, we try every column. We use three
sets to detect conflicts in *O(1)*:

```python
def solve_n_queens(n):
    cols = set()
    diag1 = set()       # row - col
    diag2 = set()       # row + col
    board = [["."] * n for _ in range(n)]
    out = []

    def go(row):
        if row == n:
            out.append(["".join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            board[row][col] = "Q"
            go(row + 1)
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
            board[row][col] = "."

    go(0)
    return out
```

Look at the **symmetry**: every `add` has a matching `remove`,
every `"Q"` has a matching `"."`. That symmetry is what makes the
algorithm correct — the undo restores the state exactly so the
next sibling iteration starts clean.

The `row - col` and `row + col` tricks encode the two diagonal
directions. Every cell on a `↘` diagonal has the same `row -
col`; every cell on a `↗` diagonal has the same `row + col`.
These two encodings let us reject conflicts in *O(1)*.

## 6. Pruning — the real speedup

A naive backtracker tries every combination. That is exponential.
**Pruning** is the art of recognizing "this branch cannot
possibly lead to a solution" and abandoning it early.

In N-Queens, the conflict set check is pruning. In Sudoku, the
"this digit already appears in this row/column/box" check is
pruning. In subset sum, "current total already exceeds target"
is pruning.

The same algorithm with the same skeleton can run in
milliseconds or in days, depending on how aggressive your
pruning is.

The instinct to develop: at every step of writing a backtracker,
ask "is there a cheap check I can do *now* that would
immediately rule out this branch?". If yes, add the check.
Pruning is what makes backtracking actually fast in practice.

## 7. The "snapshot" rule, in detail

When the recursion records a solution, it must store a **copy**
of the state, not the live state itself. The shorthand in Python
is `current[:]` (slice copy of a list).

Why? Because the live state is about to be mutated again on the
next iteration. If we stored a reference, every recorded
solution would point at the same object, and at the end they
would all show the final (usually empty) state.

```python
out.append(current)        # WRONG: every record points at the same list
out.append(current[:])     # RIGHT: snapshot is frozen at this moment
```

This is the **#1 beginner backtracking bug**. If your algorithm
records the right *count* of solutions but they all look
identical, you forgot to snapshot.

Other ways to snapshot in Python:
- `list(current)` — same as `[:]`.
- `current.copy()` — explicit, same as `[:]`.
- `tuple(current)` — if you want an immutable snapshot.

## 8. The mutate-vs-immutable style choice

You have two ways to manage state in backtracking.

**Style A: mutate and undo** (as shown above). Pass a shared
`current` list, modify it before each recursive call, undo
after.

**Style B: immutable arguments.** Pass `current + [choice]` as
an argument. Each recursive call gets a fresh list. No undo
needed.

```python
# Style B for subsets:
def subsets(nums):
    out = []
    def go(i, current):
        if i == len(nums):
            out.append(current)
            return
        go(i + 1, current)
        go(i + 1, current + [nums[i]])
    go(0, [])
    return out
```

Style B is clearer but allocates more (a new list per branch).
Style A is faster but requires the discipline of matching
mutate/undo pairs.

For interviews: write whichever you find easier to get right
under pressure. Both are correct. Style A is what most "DSA
textbook" implementations show; Style B is what functional
programmers prefer.

## 9. Common beginner mistakes

**Mistake 1: forgetting to snapshot.** `out.append(current)`
instead of `out.append(current[:])`. The classic. Always copy
when recording.

**Mistake 2: forgetting to undo.** Every mutation needs a
matching restoration before the function returns. Asymmetric
mutate/undo is the second-most-common bug.

**Mistake 3: not pruning.** A backtracking solution without
pruning is correct but slow. Always ask "what cheap check can I
do at this branch?".

**Mistake 4: using the wrong return value.** Many backtracking
functions return `None` and accumulate into a closed-over list.
Don't accidentally return early from the wrong branch.

**Mistake 5: recurring on the same subproblem repeatedly.** If
two different choice sequences lead to the same state, you may
be unintentionally exploring it twice. For problems where this
matters (often DP problems in disguise), memoization is the fix.

**Mistake 6: choosing the wrong "decision" axis.** N-Queens
benefits from "one queen per row." Permutations benefit from
"one position at a time." Choosing a bad decomposition can blow
up the search space.

## 10. Recognizing backtracking problems

Look for these signals:

- The problem asks for **all** solutions, or **count of**
  solutions, or **any one** solution.
- The state space is exponential but pruning could help.
- The problem has a clear "try every option" or "make a
  sequence of choices" structure.

Typical phrasing:

- "Generate all..."
- "Find all distinct..."
- "Place N items satisfying..."
- "Color the graph with K colors such that..."
- "Partition the input into..."

When you see these, reach for the backtracking skeleton first.

## 11. When NOT to use backtracking

If the problem only asks for a **count** and there's overlap
between subproblems, you usually want **DP** instead. The
classic example: number of ways to reach the top of stairs.
Backtracking would enumerate every path; DP collapses identical
intermediate states.

If the problem has a **greedy** solution (one optimal choice at
each step, no need to backtrack), use it. Backtracking is
expensive; greedy is linear.

If the problem has a clean **closed-form** solution (some
combinatorial identity), use that. Backtracking is for problems
where you really do need to try every option.

## 12. End-of-chapter exercise

1. **Subsets.** Already covered. LeetCode 78.
2. **Permutations.** Already covered. LeetCode 46.
3. **Combination sum.** Recurse with the choice "include this
   number or skip"; can reuse numbers. LeetCode 39.
4. **Generate parentheses.** Carefully balance open and close
   counts. LeetCode 22.
5. **Word search in a grid.** Backtrack with the grid as state;
   mark cells visited during the search and unmark on return.
   LeetCode 79.

After these five, the backtracking skeleton should feel
mechanical.

## 13. Where to go next

- **Step 7** — the dedicated recursion/backtracking step with
  many more problems.
- **Step 15** — graph DFS, which uses the same mark/unmark
  pattern.
- **Step 16** — DP, which is backtracking + memoization for
  count/optimization problems.

Backtracking is the brain of "try every option" algorithms.
Master the skeleton, develop the pruning instinct, and the rest
is execution.

## 14. The four-step skeleton, drilled

Every backtracking problem fits the same shape. Internalize this
template by writing it from scratch ten times:

```python
def backtrack(state):
    if is_solution(state):
        record(state)
        return
    for choice in legal_choices(state):
        apply(choice, state)         # commit
        backtrack(state)             # recurse
        undo(choice, state)          # rollback
```

The four steps:
1. **Base case** — am I done? Record the answer.
2. **Generate choices** — what options exist from here?
3. **Apply + recurse** — commit each choice, dive deeper.
4. **Undo** — roll back so the next sibling branch sees a clean
   state.

Forgetting step 4 is the #1 bug. The `undo` is the difference
between backtracking and naive recursion.

## 15. Subsets — the canonical example

The classic. Two choices per element: include or exclude.

```python
def subsets(nums):
    out = []
    cur = []
    def back(i):
        if i == len(nums):
            out.append(cur.copy())  # snapshot
            return
        # exclude
        back(i + 1)
        # include
        cur.append(nums[i])
        back(i + 1)
        cur.pop()                   # undo
    back(0)
    return out
```

Walk the recursion tree. At depth 0 we branch into 2 children
(include / exclude `nums[0]`). At depth 1 we branch again. By
depth n, we have 2^n leaves — one for each subset.

The `cur.copy()` is critical. Without it, `out` would contain
references to the same list, all empty by the end.

## 16. Permutations — and avoiding duplicates

Permutations are a "choose without replacement" backtracking.

```python
def permute(nums):
    out = []
    cur = []
    used = [False] * len(nums)
    def back():
        if len(cur) == len(nums):
            out.append(cur.copy())
            return
        for i in range(len(nums)):
            if used[i]: continue
            used[i] = True
            cur.append(nums[i])
            back()
            cur.pop()
            used[i] = False
    back()
    return out
```

For **permutations with duplicates** (e.g., `[1, 1, 2]`), sort
first, then add a "skip duplicates at the same depth" rule:

```python
nums.sort()
def back():
    ...
    for i in range(len(nums)):
        if used[i]: continue
        if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
            continue           # skip duplicate at same depth
        ...
```

The condition `not used[i-1]` says "the previous identical
element hasn't been chosen at this depth yet" — so picking the
current one would generate a permutation that the previous one
already generated.

## 17. Pruning — the secret to fast backtracking

A naive backtracking explores 2^n or n! states. With **pruning**,
many branches are cut before reaching leaves. Common pruning
strategies:

- **Early-exit on infeasible state.** If the current path has
  already violated a constraint, return immediately. Example:
  N-Queens — if two queens attack, prune.
- **Bound-based pruning.** Maintain the best answer so far; if
  the current branch can't beat it, prune.
- **Sorted choice pruning.** Sort choices to encourage early
  cuts (e.g., subset-sum: sort descending, take the big numbers
  first).
- **Symmetry pruning.** If two choices lead to symmetric
  configurations, only explore one. Example: N-Queens — first
  queen in left half only, then mirror.

Pruning can turn a 2^n algorithm into something practical even
for n = 30. The "branch and bound" technique is pruning
formalized: maintain a bound, only explore branches that could
beat it.

## 18. Common bugs

**Missing undo.** Causes branches to contaminate each other.

**Returning state instead of mutating.** Both styles work, but
mixing them leads to confusion. Pick one.

**Forgetting to snapshot.** When recording the answer, use
`cur.copy()` (or `list(cur)`) — not `cur` directly.

**Wrong starting index.** "Combinations from index i forward"
means starting at `i`, not 0. Off-by-one is easy here.

**Permutations vs combinations confused.** Permutations care
about order; combinations don't. The recursive shapes differ.

## 19. Mental exercises

1. *Generate all subsets of `[1, 2, 3]` by hand. List the
   order in which the include/exclude algorithm produces them.*

2. *In the permutations algorithm, what's the *purpose* of
   `used[]`? Could you do it without it?*

3. *For the duplicate-skip rule, walk `[1, 1, 2]` and show why
   `(1_a, 1_b, 2)` is generated but `(1_b, 1_a, 2)` is not.*

4. *N-Queens for n = 4: how many solutions, and what does the
   recursion tree look like with column-conflict pruning?*

5. *Why is recording with `cur.copy()` necessary? What happens
   if you `out.append(cur)` instead?*
''',
}
