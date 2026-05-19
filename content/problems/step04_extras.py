"""Step 4 extras — binary search, written at the deep narrative bar.

Each problem is written to be a learning chapter: multi-paragraph brute
force walking through the most natural human first attempt; multi-
paragraph "better" approach explaining how observing the structure
unlocks a smarter algorithm; multi-paragraph "best" approach for the
optimal solution; a walked example on concrete numbers; and code with
line-by-line comments explaining the *why*.
"""
from __future__ import annotations

_SHEET = {
    "label": "Striver's A2Z DSA Course Sheet",
    "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
}


def _lc(num: int, slug: str) -> dict:
    return {
        "label": f"LeetCode {num} — {slug.replace('-', ' ').title()}",
        "url": f"https://leetcode.com/problems/{slug}/",
    }


PROBLEMS: list[dict] = [
    # =================================================================
    # Lecture 3 — BS on 2D arrays
    # =================================================================
    {
        "id": "search-2d-matrix",
        "title": "Search in a 2D Matrix",
        "step_id": 4,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["binary-search", "matrix"],
        "what_this_teaches": (
            "How a 2D problem can be reframed as a 1D problem the "
            "moment you notice that the rows are globally chained — "
            "the last element of row i is less than the first element "
            "of row i+1. Once you see that, binary search on a 'virtual' "
            "1D array unlocks O(log(m × n))."
        ),
        "pattern": (
            "Reframe the 2D grid as a 1D sorted array; binary search; "
            "convert the midpoint back to (row, col) using divmod."
        ),
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["binary-search", "lower-bound"],
        "next_problems": [
            "search-2d-matrix-ii",
            "peak-element-2d",
            "matrix-median",
        ],
        "resources": [
            _SHEET,
            _lc(74, "search-a-2d-matrix"),
            {
                "label": "Wikipedia — Binary search",
                "url": "https://en.wikipedia.org/wiki/Binary_search_algorithm",
            },
        ],
        "understanding": r'''
We are handed a 2D matrix of integers. The matrix has two specific
properties that make it more than a random grid:

1. **Every row is sorted in non-decreasing order from left to
   right.** Within any single row, reading left to right gives
   you a sequence that only stays the same or grows.
2. **The first integer of each row is strictly greater than the
   last integer of the previous row.** This second property is
   the powerful one. It chains the rows together so that the
   matrix as a whole, if you read it top-to-bottom and left-to-
   right, is one fully sorted sequence.

We are also given an integer target. The job is to return
`True` if the target exists anywhere in the matrix, `False`
otherwise.

Example matrix:

```
 1   3   5   7
10  11  16  20
23  30  34  60
```

For `target = 3`: the answer is `True` (row 0, column 1).
For `target = 13`: the answer is `False` (it would belong
between 11 and 16, but there's no 13 in the matrix).

Treat this problem as a story in three acts. In Act I you forget
all the structure and just look at the matrix as a bag of
numbers. In Act II you notice the row-by-row sorting and use
binary search on each row. In Act III you notice the *global*
sorting across rows and use a single binary search over the
entire matrix.

The lesson is not "memorize the optimal solution." The lesson is
"observe the structure given to you, and let each observation
unlock a better algorithm." That is the central habit of
algorithm design.
''',
        "brute_force": {
            "explanation": r'''
Start from the most basic idea: forget all the sorting properties
and just think, *"where could the target be?"*. The answer, in
the absence of any structure, is *"anywhere in the matrix."* So
the most straightforward approach is to check every single
element one by one.

You go row by row. Inside each row, you scan column by column.
At every cell you compare the value with the target. If it
matches, you return `True` immediately — there is no reason to
keep looking once you've found what you came for. If you finish
scanning the entire matrix without ever matching, you return
`False`.

This works because you are not using any structure or ordering
information. You are treating the matrix as just a collection
of `m × n` numbers with no special rules. That naturally
produces a nested loop — one loop for rows, one for columns —
which guarantees you visit every element exactly once.

In this brute-force mindset, the logic is intentionally
simple: *"check everything until you find it."* There is no
optimization, no skipping, no early structure-based decision-
making. You are relying purely on direct comparison.

Because of that full scan, the time complexity is **O(m × n)**.
In the worst case (target absent, or target at the very last
cell), you touch every element. Space is **O(1)** — we only
need a few index variables.

This is fine **logically** — it always returns the correct
answer — but it ignores the most important information the
problem hands you. The rows are sorted. The matrix is globally
ordered. Those facts are not decorations; they are an
invitation to use a better algorithm. In the brute force, we
ignore the invitation.

Still, write the brute force out at least once. Two reasons.
First, having a known-correct baseline lets you test the
faster algorithm against it on small inputs. Second, the
brute force is your fallback when the optimization turns out
to be more bug-prone than expected.
''',
            "code": r'''def search_2d_matrix_brute(matrix: list[list[int]], target: int) -> bool:
    # m is the number of rows. We will iterate the outer index
    # from 0 up to m - 1, so we need to know how many rows exist.
    m = len(matrix)
    # Defensive guard. If there are no rows, there's nothing to search.
    # Returning False on an empty matrix is the natural answer.
    if m == 0:
        return False
    # n is the number of columns. Because the matrix is rectangular,
    # every row has the same number of columns — so reading the length
    # of matrix[0] gives the column count for the entire grid.
    n = len(matrix[0])
    # Outer loop: walk through every row index from 0 to m - 1.
    for i in range(m):
        # Inner loop: for the current row i, walk through every column
        # index from 0 to n - 1. The pair (i, j) covers every cell of
        # the matrix exactly once.
        for j in range(n):
            # The comparison. If this cell holds the target value, we
            # can return True immediately — there's no value in checking
            # any other cell once we already have a definite "yes".
            if matrix[i][j] == target:
                return True
    # Both loops finished without finding the target, so it is not in
    # the matrix. Return False.
    return False
''',
            "complexity": (
                "**Time**: *O(m × n)*. We touch every cell in the "
                "worst case.\n\n"
                "**Space**: *O(1)*. Only a constant number of index "
                "variables."
            ),
        },
        "thought_process": r'''
Now the better idea. Start from what the problem is really giving
you.

You are given a 2D matrix, but it is not a random grid. It has a
very strong structure: every row is sorted, **and** the first
number of each row is bigger than the last number of the
previous row. That second condition is the most important one,
because it links all rows together in order.

If you line up the rows one after another — imagine taking row 0,
then concatenating row 1's elements after it, then row 2's, and
so on — something interesting happens. The numbers do not just
stay sorted *within* each row. They are sorted *across rows
too*. The last number of row 0 is smaller than the first number
of row 1, so when you concatenate, the boundary is also in
order. By chaining this across all the rows, the entire
matrix reads as **one long globally sorted sequence**.

Once you see that, the problem becomes familiar. You are no
longer searching in a 2D grid; you are searching in a sorted
1D list. And whenever you have a sorted list and you want to
find something efficiently, the natural algorithm is **binary
search**. Linear search would check every element one by one.
Binary search uses order to eliminate half the search space at
each step.

Now the only challenge is: the data is still *physically* stored
in a 2D matrix. We do not want to actually flatten it into a 1D
array, because that would cost *O(m × n)* memory and defeat the
purpose. Instead, we **simulate** a 1D array without converting
anything. We use indices `0, 1, 2, ..., m * n - 1` as if there
were a virtual 1D sorted array, and whenever we need to read a
value at virtual index `k`, we convert `k` back to a 2D
position.

The conversion is divmod. Index `k` in the virtual array
corresponds to `(k // n, k % n)` in the 2D matrix. Dividing by
`n` gives the row (because each row holds exactly `n`
elements); the remainder gives the column. So `matrix[k // n][k
% n]` reads the value at virtual position `k`.

With that mapping, the rest is plain binary search. Two pointers
`lo` and `hi` over the virtual indices. Compute the midpoint.
Read the value at that mid via divmod. Compare with target.
Halve the search space.

So the full idea is: **recognize global sorting → treat the
matrix as a virtual 1D sorted array → apply binary search →
map indices back to 2D positions only when accessing values.**

This is `O(log(m × n))` time — about thirty comparisons for a
million-element matrix. The space remains `O(1)`. Massive win
over the brute force `O(m × n)`.
''',
        "optimized": {
            "explanation": r'''
Set up the idea once more: you are no longer thinking in rows and
columns separately. You imagine the matrix as one continuous
sorted list of length `m × n`. Your search space is not 2D
anymore — it is a range of virtual indices from `0` to `m * n
- 1`.

You define two pointers, `lo` and `hi`, that bound this virtual
range. At each step, you look at the midpoint `mid = (lo + hi)
// 2`. This midpoint is your "guess" of where the target might
be.

But the data is still stored in a 2D grid, so to actually read
the value at virtual position `mid`, you must convert `mid` back
to a (row, column) pair. The row is `mid // n` (each row holds
`n` elements, so dividing the virtual index by `n` gives which
row); the column is `mid % n` (the remainder tells you how far
into that row you are). The value is `matrix[mid // n][mid %
n]`.

Now the comparison decides the next step. If the value equals
the target, you are done — return `True`. If the value is
smaller than the target, every virtual position from `lo` up to
`mid` (inclusive) is also smaller (because the virtual array is
globally sorted), so the target — if present — must be strictly
to the right of `mid`. You move `lo = mid + 1`. If the value is
larger, symmetrically, the target — if present — is strictly to
the left of `mid`. You move `hi = mid - 1`.

You repeat until you either find the target or your search space
becomes empty (`lo > hi`). If the loop exits without finding,
return `False`.

The key invariant: at every iteration, if the target exists in
the matrix at all, then its virtual index lies in `[lo, hi]`.
Each iteration strictly shrinks `[lo, hi]` by at least one,
so the loop must terminate. And the new bound exclusion is
*safe* — we only ever move the bound away from positions that
cannot possibly hold the target.

Walking through the example matrix above with `target = 11`:

```
 1   3   5   7        Row 0: virtual indices 0..3
10  11  16  20        Row 1: virtual indices 4..7
23  30  34  60        Row 2: virtual indices 8..11
```

- `lo = 0, hi = 11`. `mid = 5`. `5 // 4 = 1, 5 % 4 = 1`, so we
  read `matrix[1][1] = 11`. Match! Return `True`.

Just two iterations would suffice in this case. For a more
spread-out search, log2(12) ≈ 3.6, so at most four iterations.
''',
            "code": r'''def search_2d_matrix(matrix: list[list[int]], target: int) -> bool:
    # Get the row count m. We need it to define m * n, the total
    # number of cells in the virtual 1D array.
    m = len(matrix)
    # Defensive guard. An empty matrix contains nothing to find.
    if m == 0:
        return False
    # Get the column count n. We need this both for the total cell
    # count (m * n) AND for the divmod that translates a virtual 1D
    # index back into (row, column). Since the matrix is rectangular,
    # every row has the same number of columns; reading matrix[0]'s
    # length is sufficient.
    n = len(matrix[0])
    # Initialize the binary-search bounds on the VIRTUAL 1D array.
    # The smallest virtual index is 0 (top-left cell). The largest is
    # m * n - 1 (bottom-right cell). The window [lo, hi] is inclusive
    # on both ends.
    lo, hi = 0, m * n - 1
    # Binary search loop. We continue while the window is non-empty,
    # i.e., lo has not crossed hi.
    while lo <= hi:
        # Compute the midpoint of the current search window. Integer
        # division rounds toward zero, which is what we want — the mid
        # is a valid virtual index in [lo, hi].
        mid = (lo + hi) // 2
        # Convert the virtual midpoint into a real (row, column) pair.
        # Dividing by n gives the row: each row holds exactly n elements,
        # so the row number is mid divided by n.
        # The remainder mid % n gives how many elements into that row we
        # have walked — i.e., the column.
        # Read the actual matrix value at that position.
        value = matrix[mid // n][mid % n]
        # Three branches in the comparison:
        if value == target:
            # We found the target. There is no need to keep searching.
            return True
        elif value < target:
            # The value at mid is too small. Because the virtual array
            # is globally sorted, every virtual position from lo to mid
            # (inclusive) is also too small. We can safely throw all of
            # them away. The target, if it exists, must be at some
            # virtual position strictly greater than mid.
            lo = mid + 1
        else:
            # The value at mid is too large. By the symmetric argument,
            # every virtual position from mid to hi is at least mid's
            # value, so it is also too large. The target, if it exists,
            # is at a position strictly less than mid.
            hi = mid - 1
    # The window emptied without finding the target. The target is not
    # in the matrix.
    return False
''',
            "complexity": (
                "**Time**: *O(log(m × n))*. The search space halves "
                "each iteration. For a 1000 × 1000 matrix, that is "
                "about 20 comparisons.\n\n"
                "**Space**: *O(1)*. We use only a constant number of "
                "index variables; we never materialize the virtual 1D "
                "array."
            ),
        },
        "deep_concept": r'''
Step back from the code and look at the deeper move. The
problem hands us data laid out in two dimensions and asks an
ordering question. Our instinct as beginners is to operate
directly in two dimensions. But the moment we notice that the
two dimensions can be linearized — by virtue of the "first of
next row > last of previous row" promise — the problem reduces
to a one-dimensional classic. Binary search on a sorted array
is one of the first algorithms anyone learns. By reducing the
unfamiliar 2D problem to the familiar 1D problem, we make the
whole thing tractable.

This pattern — **reduce the unfamiliar to the familiar** — is
one of the deepest moves in algorithm design. Many "new"
problems are old problems wearing a costume. The skill is to
strip off the costume and recognize the bones underneath.

There is also a fascinating duality with the next problem,
"Search in a 2D Matrix II" (LeetCode 240). In LC 240, the
matrix is sorted differently — each row sorted left-to-right
*and* each column sorted top-to-bottom — but **without** the
"first of next row > last of previous row" guarantee. That
weakening of the structure breaks the 1D linearization! A
flattened LC 240 matrix is not globally sorted in general. So
binary search on a virtual 1D array no longer works. We need a
different algorithm (the staircase search) to exploit the
remaining row/column ordering. We cover that algorithm in the
next problem.

The lesson, broadened: **the algorithm you can use depends on
exactly which structural property holds**. Read the problem
statement carefully — the difference between "first of next row
> last of previous row" and "each column sorted top to bottom"
is small in English but enormous in algorithm choice.
''',
        "confusion_notes": [
            {
                "question": "Why convert via `mid // n` and `mid % n` instead of just storing two pointers per row?",
                "answer": r'''
Because the conversion is `O(1)` and lets us do a single
binary search over the entire matrix as if it were a 1D array.

If we instead stored "current row" and "left/right bounds within
that row," we would need to first find which row the target
might be in (one binary search on the first column, *O(log m)*),
then find the target within that row (another binary search,
*O(log n)*). The total is *O(log m + log n)* = *O(log(mn))*
— same complexity, but two phases of bookkeeping and two
separate binary searches.

The virtual-1D approach collapses this into a single binary
search whose iterations span the entire matrix. The bookkeeping
is simpler: only `lo`, `hi`, and `mid`. The conversion from
virtual index to (row, col) costs two arithmetic operations.

Both algorithms are correct and have the same big-O. The
single-search version is preferred because it's easier to
write without bugs and the constant factor is slightly better
(fewer function calls or branches).
''',
            },
            {
                "question": "Could I just use Python's bisect on a flattened copy of the matrix?",
                "answer": r'''
Yes — and it's a perfectly clean one-liner:

```python
import bisect

def search(matrix, target):
    flat = [v for row in matrix for v in row]
    i = bisect.bisect_left(flat, target)
    return i < len(flat) and flat[i] == target
```

But this approach costs **O(m × n) extra memory** to materialize
the flattened list. For huge matrices that's wasteful — we are
copying every element just to search.

The virtual-1D binary search achieves the same *O(log(mn))*
time at *O(1)* extra memory. That is the real benefit of doing
the divmod conversion: we never allocate the flat array.

In an interview, mention both. Write the binary search version
to show you understand the divmod trick. Mention the bisect
version to show you know Python's standard library — but
acknowledge it uses extra memory.
''',
            },
            {
                "question": "Why exactly is the matrix globally sorted? Walk me through the proof.",
                "answer": r'''
We're given two properties:
1. Each row is sorted left to right.
2. The first element of every row is strictly greater than the
   last element of the previous row.

Pick any two virtual indices `i < j`. We need to show that
`flat[i] <= flat[j]` (where `flat` is the imagined 1D
flattening).

Two cases.

**Case A: `i` and `j` are in the same row.** Then by property
(1), since `i` comes before `j` in the row, `flat[i] <=
flat[j]`. Done.

**Case B: `i` is in row `r_i`, `j` is in row `r_j`, with `r_i <
r_j`.** By property (1), `flat[i] <= last_of(row r_i)`. By
property (2) applied repeatedly, `last_of(row r_i) <
first_of(row r_i + 1) <= last_of(row r_i + 1) < ... <=
first_of(row r_j)`. By property (1) again, `first_of(row r_j)
<= flat[j]`. Chaining: `flat[i] <= last_of(row r_i) <
first_of(row r_j) <= flat[j]`. Done.

So the entire flattening is sorted. This justifies the binary
search on the virtual 1D array.

Notice that property (2) is doing the heavy lifting. Without
it (as in LC 240, "Search a 2D Matrix II"), Case B falls apart
— a value in row `r_i` could exceed a value in row `r_j`. That
is why LC 240 needs the different staircase algorithm.
''',
            },
            {
                "question": "What's the time complexity? It feels like there are two log factors.",
                "answer": r'''
It's *O(log(m × n))*, which equals *O(log m + log n)* by
logarithm rules — a single combined log, not two multiplied.

To see this: log(m × n) = log m + log n. So whether you write
the complexity as "log of total cells" or "sum of log of rows
plus log of cols," it's the same number. Both are
asymptotically equivalent.

For a 1000 × 1000 matrix (one million cells), `log2(10⁶) ≈
20` — twenty comparisons in the worst case. Compare with the
brute force's `10⁶` operations: a 50,000× speedup.

The same analysis applies to the binary-search-per-row
approach: *O(log m + log n)* total, which is the same as
*O(log(m × n))*. The two approaches differ in constants and
clarity but not in asymptotic complexity.
''',
            },
            {
                "question": "What if `n = 1` (a single column) or `m = 1` (a single row)?",
                "answer": r'''
The algorithm handles both gracefully — they are just degenerate
versions of the general matrix.

**Single row (`m = 1`)**: The virtual 1D array is just that
row. Binary search runs normally over indices `0..n-1`. The
divmod conversion gives `(0, j)` for every virtual index — we
always read from row 0. Equivalent to a plain 1D binary search.

**Single column (`n = 1`)**: The virtual 1D array is the column,
top to bottom. Binary search runs over `0..m-1`. The divmod
gives `(i, 0)` for every virtual index — we always read column
0. Equivalent to a 1D binary search down the column.

**Edge case: matrix is `[[]]` (one empty row).** The product `m
* n = 1 * 0 = 0`, so `hi = -1` and the loop body never
executes. We return `False`. Correct.

**Edge case: matrix is `[]` (no rows at all).** The defensive
guard at the top catches this and returns `False`. Without the
guard, `matrix[0]` would raise an `IndexError`.

The algorithm is dimensionally robust. The only edge cases that
need explicit handling are the truly empty inputs.
''',
            },
        ],
        "summary": r'''
**Pattern**: reframe a structured 2D matrix as a virtual 1D
sorted array; binary search the virtual indices; use divmod to
convert between virtual indices and real (row, column) pairs.

**Lesson**: when a 2D problem's structure chains across rows in
a totally-ordered way, you can collapse the search space to one
dimension. The conversion is `O(1)` and saves memory compared
to actually flattening.

**Recognize next time**: any problem where 2D data has a "row
i ends below row i+1 begins" property. Wherever you can prove
global ordering across the flattening, binary search wins.

**Closely related**: Search in a 2D Matrix II (LeetCode 240).
That problem has weaker structure (only row-wise and column-
wise sorting), so this algorithm does not apply directly. The
next problem covers it.
''',
    },
    {
        "id": "search-2d-matrix-ii",
        "title": "Search in a Row-wise and Column-wise Sorted Matrix",
        "step_id": 4,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["binary-search", "matrix", "staircase"],
        "what_this_teaches": (
            "The staircase search algorithm — exploit row sortedness "
            "and column sortedness directly, without trying to "
            "linearize. Each move eliminates either an entire row or "
            "an entire column, giving O(m + n) time."
        ),
        "pattern": (
            "Start at top-right (or bottom-left); compare with target; "
            "move left to shrink columns or down to shrink rows."
        ),
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["search-2d-matrix", "binary-search"],
        "next_problems": ["peak-element-2d", "matrix-median"],
        "resources": [
            _SHEET,
            _lc(240, "search-a-2d-matrix-ii"),
        ],
        "understanding": r'''
This is the trickier cousin of the previous problem. We are
given a 2D matrix with weaker structure than before:

1. **Every row is sorted in non-decreasing order from left to
   right.**
2. **Every column is sorted in non-decreasing order from top to
   bottom.**

That is **all**. Notice what is **missing**: there is no
guarantee that the first element of a row is greater than the
last element of the previous row. The matrix is **not**
globally sorted when flattened.

Example:

```
 1   4   7  11  15
 2   5   8  12  19
 3   6   9  16  22
10  13  14  17  24
18  21  23  26  30
```

Row 0 ends at 15. Row 1 starts at 2. Two is less than 15. So if
you flatten this matrix into a 1D list, you get a sequence
that is *not* sorted: `1, 4, 7, 11, 15, 2, 5, 8, ...`. The
virtual-1D-array trick from the previous problem does not work.

We need a fundamentally different algorithm that uses the row
sortedness and column sortedness *directly*, without assuming
global sortedness. That algorithm is the **staircase search**,
and it is one of the most elegant ideas in array DSA.

The output: return `True` if the target appears anywhere in the
matrix, `False` otherwise.

This problem is on Striver's sheet because it teaches the
broader lesson that **the available algorithm depends on the
exact structural property of the input**. A change in one
clause — "first of next row > last of previous row" — completely
changes which approach works. Read problem statements
carefully.
''',
        "brute_force": {
            "explanation": r'''
The brute force is the same as before. Forget the structure;
just check every cell.

You walk row by row, column by column, comparing each cell with
the target. If a cell matches, return `True`. If you finish the
walk without finding, return `False`.

Nested loop, *O(m × n)* time, *O(1)* extra space. It will work
correctly on any matrix, sorted or not. The price is that you
ignore all the structural information the problem gives you.

For a 1000 × 1000 matrix, that's a million comparisons. The
optimal staircase algorithm does it in 2000.
''',
            "code": r'''def search_2d_matrix_ii_brute(matrix: list[list[int]], target: int) -> bool:
    # Defensive: empty matrix contains nothing.
    if not matrix or not matrix[0]:
        return False
    # m is the number of rows, n is the number of columns.
    m, n = len(matrix), len(matrix[0])
    # Outer loop over rows, inner loop over columns. Total cells
    # visited = m * n in the worst case.
    for i in range(m):
        for j in range(n):
            # Direct comparison. The brute force does no skipping
            # based on order.
            if matrix[i][j] == target:
                return True
    # No cell matched. The target is not in the matrix.
    return False
''',
            "complexity": "**Time**: *O(m × n)*. **Space**: *O(1)*.",
        },
        "thought_process": r'''
Now the better idea. Better, but not best.

We can still apply binary search **per row**. Each row is sorted,
so within a single row we can search in `O(log n)`. We loop
over rows and binary-search each one. The total time is
`O(m × log n)`.

That's a clear improvement over `O(m × n)`, but for large `m`
it can still be slow. For a 1000 × 1000 matrix: `1000 × log2(
1000) ≈ 1000 × 10 = 10,000` comparisons. Better than a million,
but the staircase search does it in 2000.

We mention this middle-tier approach because it demonstrates a
useful habit: **always try the obvious application of binary
search first, even before reaching for cleverness**. Often the
obvious version is fast enough, and the cleverer version isn't
worth the implementation risk.

But for this specific problem, we have a beautifully tight
*O(m + n)* algorithm waiting in Act III. Let's get there.
''',
        "optimized": {
            "explanation": r'''
The best algorithm — the **staircase search** — comes from
noticing a different kind of structure in this 2D matrix.

Instead of flattening like we did in the previous problem, we
now use the fact that each row is sorted left-to-right **and**
each column is sorted top-to-bottom. That gives us a directional
guide inside the grid.

Imagine you are standing at a special starting position in the
matrix, and at every step you want to decide where to move so
that you eliminate as much of the search space as possible. The
best place to start is the **top-right corner**.

Why top-right? Because it gives you a perfect decision point.
At the top-right corner:

- Everything to the **left** is smaller (because the row is
  sorted ascending left-to-right).
- Everything **below** is larger (because the column is sorted
  ascending top-to-bottom).

So from this single position, you can decide the direction of
movement based on a comparison with the target:

- If the current value **equals** the target → you found it.
- If the current value is **greater** than the target → you
  need smaller values → move **left**.
- If the current value is **smaller** than the target → you
  need larger values → move **down**.

This creates a "staircase" path through the matrix, because at
each step you go either left or down, gradually narrowing the
search space.

What makes this powerful is that each move eliminates an entire
row or column:

- Moving **left** removes a column. The current column (the
  rightmost one you've considered) contains only values *too
  large* — everything below the current cell in that column is
  even bigger, so none of them can be the target.
- Moving **down** removes a row. The current row (the topmost
  one you've considered) contains only values *too small* —
  everything to the left of the current cell in that row is
  even smaller.

So instead of checking everything, you keep shrinking the search
area in a very controlled way until you either find the target
or step outside the matrix.

That is the core idea: **start at a position where every move
gives you maximum information, then eliminate rows or columns
step by step.**

Why does this give *O(m + n)*? Because each move shrinks the
search region by at least one row or one column. You start with
`m` rows and `n` columns; you can eliminate at most `m + n - 1`
rows-or-columns before the search region becomes empty. So the
loop runs at most `m + n` times.

Let's walk through it on a concrete example. Take this matrix:

```
 1   4   7  11
 2   5   8  12
 3   6   9  16
10  13  14  17
```

Target = 6. Start at the top-right corner, which is `11`.

- At `11`: compare with `6`. `11 > 6`, so we need a smaller
  number. Look at what "smaller" means here. The row is sorted,
  so moving **left** gives smaller values. The column is sorted,
  so moving **down** gives **larger** values. From `11`, only
  the leftward direction makes sense. We move left. This
  eliminates the entire rightmost column from consideration —
  everything below `11` in that column is at least `11`, so
  cannot be `6`.
- At `7`: `7 > 6`. Move left again.
- At `4`: `4 < 6`. Now leftward would only make things smaller,
  so it's useless. Move **down**.
- At `5`: `5 < 6`. Move down again.
- At `6`: match. Return `True`.

Five steps total. Compared to the 16 cells in the brute force,
we examined only 5. For larger matrices the savings explode.

Why must we start at top-right (or, symmetrically, bottom-left)
and not, say, top-left? Because at the **top-left** corner, both
the value to the right and the value below are **larger** than
the current cell. The comparison "current > target" does not
tell us a clean direction — we could decrease in either
direction. So the top-left corner is **not** a useful starting
position. The same problem occurs at the bottom-right corner.

The corners that work are **top-right** and **bottom-left** —
the ones where one direction increases and the other decreases.
That is the directional asymmetry that makes the algorithm
work.

This problem teaches one of the prettiest small algorithms in
DSA. Internalize it. Once you have it, the entire family of
"search in a sorted matrix" variants becomes mechanical.
''',
            "code": r'''def search_2d_matrix_ii(matrix: list[list[int]], target: int) -> bool:
    # Defensive guard. An empty matrix contains nothing.
    if not matrix or not matrix[0]:
        return False
    # m is the number of rows, needed because we walk DOWN. When the
    # row index reaches m, we have moved off the bottom of the matrix.
    m = len(matrix)
    # n is the number of columns, needed because we walk LEFT. When the
    # column index drops below 0, we have moved off the left edge.
    n = len(matrix[0])
    # Initialize at the TOP-RIGHT corner: row 0, column n - 1. This is
    # the special starting position where moving left gives smaller
    # values and moving down gives larger values. That asymmetry is
    # what makes each comparison decisive.
    i, j = 0, n - 1
    # Continue while we are still inside the matrix. i < m guards
    # against walking off the bottom; j >= 0 guards against walking
    # off the left.
    while i < m and j >= 0:
        # Read the current cell. This is the point where we decide
        # the next move.
        value = matrix[i][j]
        if value == target:
            # We found the target. Done.
            return True
        elif value > target:
            # The current value is too large. We need a smaller value.
            # Within this row, smaller values are to the LEFT (because
            # the row is sorted ascending). So we move left.
            # Equivalently: this entire column is eliminated. Every
            # cell at (i + 1, j), (i + 2, j), ..., (m - 1, j) is at
            # least value (because the column is sorted ascending), so
            # none of them can be the target.
            j -= 1
        else:
            # value < target. We need a larger value. Within this
            # column, larger values are BELOW (because the column is
            # sorted ascending). So we move down.
            # Equivalently: this entire row is eliminated. Every cell
            # at (i, 0), (i, 1), ..., (i, j - 1) is at most value
            # (because the row is sorted ascending), so none of them
            # can be the target.
            i += 1
    # We walked off the matrix without finding the target. Return False.
    return False
''',
            "complexity": (
                "**Time**: *O(m + n)*. Each iteration eliminates at "
                "least one row or one column. Total iterations are "
                "bounded by `m + n`.\n\n"
                "**Space**: *O(1)*. Only the two pointers `i` and `j`."
            ),
        },
        "deep_concept": r'''
The staircase search is a beautiful example of "exploit the
exact structure the problem gives you." LC 74 ("Search a 2D
Matrix") gives you a strong global ordering, so binary search
on a virtual 1D array works in `O(log(mn))`. LC 240 (this
problem) weakens the structure — only row and column sortedness
— so the global ordering breaks. Binary search on the
virtual 1D array no longer applies; we use a different
algorithm tuned to the new structure.

The deeper lesson: **algorithms are not magic.** Each one
exploits a specific structural property. When the problem's
structure changes, the algorithm must change. Read the problem
statement carefully; the differences between superficially
similar problems are exactly where the algorithm choice lives.

There is also a beautiful symmetry: you can start at the
top-right OR the bottom-left. At bottom-left:

- Up gives smaller values.
- Right gives larger values.

So the comparison flips:

- If current > target: move up (toward smaller).
- If current < target: move right (toward larger).

Both versions are correct. Pick whichever feels natural.

**What if the matrix had a third property** — say, every value
unique — would the algorithm change? No. Duplicates and
uniqueness do not affect this algorithm. The staircase only
cares about the row and column ordering.

**Could we have started in the middle of the matrix instead of
a corner?** No. Starting at an interior cell, **all four**
neighbors give one direction larger and one smaller, but there
is no single direction that uniquely "reduces the search
space." At a corner, one direction is *outside* the matrix and
one direction inside, so a comparison cleanly decides which
half of the remaining region to discard.

A small mind-bender: the algorithm's path is monotone. We only
ever move left or down (from top-right). Once we move left,
we never move right; once we move down, we never move up. The
result is a "staircase" path from top-right toward bottom-left.
That path is at most `m + n - 1` cells long, which gives the
linear time bound.
''',
        "confusion_notes": [
            {
                "question": "Why can't I use binary search on the flattened matrix like in LC 74?",
                "answer": r'''
Because LC 240's matrix is **not globally sorted** when
flattened. The previous problem (LC 74) guaranteed that the
last element of row `i` is less than the first element of row
`i + 1`. That guarantee chains the rows into a global ordering
and makes binary search on the virtual 1D array valid.

LC 240 has only row-wise and column-wise sortedness. The
example matrix above has row 0 ending at 15 and row 1 starting
at 2. So 15, 2 is the boundary in the flattened version —
descending! Binary search on that flattened sequence would
give wrong answers because it relies on monotonic ordering.

The structural property has weakened. The algorithm must change.

If you find yourself unable to remember which problem has which
structure, the rule of thumb: **if the problem says "first of
next row > last of previous row," use binary search on flattened
view; if not, use staircase.**
''',
            },
            {
                "question": "Why top-right and not top-left?",
                "answer": r'''
The top-left corner doesn't give a useful decision rule. At
the top-left:

- Right gives **larger** values (row is sorted ascending).
- Below gives **larger** values (column is sorted ascending).

So both possible moves go in the *same* direction (toward
larger). If the current value is greater than the target, we
need smaller, but neither move helps. If the current value is
less than the target, we need larger, and either move helps —
but which one?

There's no way to deterministically eliminate a row or column
from the top-left corner. The corner that works needs **one
direction increasing and one decreasing**, so a comparison
cleanly chooses.

Those corners are top-right (left smaller, down larger) and
bottom-left (right larger, up smaller). Either works.

The bottom-right corner has the same problem as top-left, just
mirrored: both moves go in the same direction (toward smaller).

So out of the four corners, exactly two are usable. Pick either.
''',
            },
            {
                "question": "Could I do better than O(m + n)?",
                "answer": r'''
For arbitrary matrices satisfying only the row/column sorted
property, **no** — *O(m + n)* is provably optimal in the
worst case.

The intuition: an adversary can place the target along the
anti-diagonal in such a way that every possible search path
must visit at least one cell from each row or each column. So
any correct algorithm makes at least `m + n - 1` cell visits in
the worst case.

There are theoretical algorithms (e.g., based on divide-and-
conquer) that achieve `O(m + n)` with smaller constants, but
the asymptotic bound cannot improve.

For more restrictive matrix shapes (like LC 74's globally
sorted flattening), you can get `O(log(mn))`. But in the
general row/column-sorted case, the staircase search is
asymptotically tight.

In an interview, if asked "can you do better?", confidently
say "no — *O(m + n)* is optimal for this problem class." Then
ask the interviewer if there's additional structure (uniqueness,
specific value ranges, etc.) that might unlock a smarter
approach.
''',
            },
            {
                "question": "What if there are duplicates in the matrix?",
                "answer": r'''
The algorithm handles duplicates correctly without modification.
The `==` comparison still finds them; the `<` and `>`
comparisons still direct us in valid directions.

If you wanted to count occurrences of the target (instead of
just detecting presence), you'd need a small variant: continue
the search after finding the first match. Move both `i` and `j`
appropriately to find the next occurrence. The path remains
staircase-shaped, so the total complexity stays *O(m + n)*.

```python
def count_occurrences(matrix, target):
    if not matrix or not matrix[0]:
        return 0
    m, n = len(matrix), len(matrix[0])
    i, j = 0, n - 1
    count = 0
    while i < m and j >= 0:
        if matrix[i][j] == target:
            count += 1
            # Move down — the row contains other potential
            # occurrences only at column j (and we've already
            # passed them).
            i += 1
        elif matrix[i][j] > target:
            j -= 1
        else:
            i += 1
    return count
```

When you find a match, deciding which direction to move is
slightly delicate (move down OR left both work, depending on
whether you want to count in row or column order). Just pick
one and stick with it.
''',
            },
        ],
        "summary": r'''
**Pattern**: staircase search — start at top-right (or bottom-
left); move left when too big, down when too small. Each move
eliminates an entire row or column.

**Lesson**: when a 2D matrix has row sortedness *and* column
sortedness but no global flattening, exploit the directional
asymmetry from a corner. Each comparison gives an unambiguous
direction.

**Recognize next time**: any "search in a 2D matrix with
row/column sorting" problem. Memorize the four-corner reasoning:
top-right and bottom-left are the usable starting positions.

**Closely related**: kth smallest in a sorted matrix, find a
target in a Young tableau — all variants of the staircase
pattern.
''',
    },
    # =================================================================
    # Lecture 1 — BS on 1D arrays (the foundational variants)
    # =================================================================
    {
        "id": "upper-bound",
        "title": "Upper Bound",
        "step_id": 4,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["binary-search", "fundamentals"],
        "what_this_teaches": (
            "The mirror of lower bound — find the first index whose "
            "value is *strictly greater* than the target. Together "
            "with lower bound, this is one of the two atomic "
            "operations from which every other sorted-array query "
            "is built."
        ),
        "pattern": (
            "Half-open binary search; move `hi = mid` when arr[mid] > "
            "target, `lo = mid + 1` otherwise."
        ),
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["binary-search", "lower-bound"],
        "next_problems": [
            "search-insert-position",
            "first-last-occurrence",
            "count-occurrences",
            "floor-ceil-sorted",
        ],
        "resources": [
            _SHEET,
            {
                "label": "Python docs — bisect.bisect_right",
                "url": "https://docs.python.org/3/library/bisect.html#bisect.bisect_right",
            },
        ],
        "understanding": r'''
Given a sorted array `arr` and a target `x`, the **upper bound**
of `x` is the smallest index `i` such that `arr[i] > x`. In
other words: it is the first position whose value is *strictly
greater* than the target. If every element in the array is at
most `x`, the upper bound is `len(arr)` — one past the last
valid index, meaning "no such position exists."

Examples on `arr = [1, 2, 3, 3, 5, 8]`:

- `x = 3`: upper bound is index `4` (the first index with value
  > 3). The value at that index is `5`.
- `x = 2`: upper bound is index `2`. Value `3`.
- `x = 0`: upper bound is index `0`. Value `1`.
- `x = 10`: upper bound is index `6` (= `len(arr)`). No element
  is greater than 10.

Why do we care about this? Because upper bound is one of the
two *atomic* operations of sorted-array work. The other is
lower bound (first index with `arr[i] >= x`). Together they
answer almost every interesting range query on a sorted array
in `O(log n)`:

- **Count of x**: `upper_bound(x) - lower_bound(x)`.
- **Number of values strictly less than x**: `lower_bound(x)`.
- **Number of values less than or equal to x**: `upper_bound(x)`.
- **Index of the last occurrence of x**: `upper_bound(x) - 1`,
  then verify `arr[result] == x`.
- **Number of values in `[L, R]`**: `upper_bound(R) -
  lower_bound(L)`.

Master upper and lower bound, and you have the keys to a wide
family of sorted-array problems.

Python ships these as `bisect.bisect_left` (lower bound) and
`bisect.bisect_right` (upper bound). In real code you should
use them. For interview practice, you should be able to write
both from memory.
''',
        "brute_force": {
            "explanation": r'''
Start with the slow, obvious idea. Walk through the array
left-to-right. The moment you find an element strictly greater
than the target, return its index. If you finish the array
without ever finding such an element, return `len(arr)`.

```python
def upper_bound_linear(arr, x):
    for i in range(len(arr)):
        if arr[i] > x:
            return i
    return len(arr)
```

This is `O(n)` time. Correct on any array. It does not use the
sortedness — exactly the same algorithm would work on an
unsorted array (though for unsorted the "first index with value
> x" question is weirdly defined).

The brute force is useful as a baseline. If you have a test
suite, run your binary-search version against the linear
version on small inputs to verify correctness.

In real code, on a small array (a few dozen elements), linear
scan is sometimes faster than binary search because of cache
effects and branch prediction. But for inputs above a few
hundred elements, binary search dominates.
''',
            "code": r'''def upper_bound_linear(arr: list[int], x: int) -> int:
    # Walk every index from 0 to len(arr) - 1.
    for i in range(len(arr)):
        # The first index whose value is strictly greater than x is
        # the upper bound. Return immediately.
        if arr[i] > x:
            return i
    # No element was strictly greater than x. By convention, return
    # len(arr) — one past the end — to indicate "no such index."
    return len(arr)
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "thought_process": r'''
The optimized algorithm is binary search using the **half-open**
convention. Half-open here means: the search window is `[lo,
hi)` — inclusive on the left, exclusive on the right. This is
the cleanest style for "find the first index satisfying property
P" problems because the answer can naturally be `len(arr)`
(no index satisfies) and the half-open convention represents
that gracefully.

Why half-open instead of the inclusive `[lo, hi]` style we used
in plain binary search? Because in plain binary search we are
looking for an *exact match*, and a result of -1 (or "not found")
is a special case. In upper/lower bound, there is no "not
found" — the answer is always a valid index in `[0, len(arr)]`,
where `len(arr)` is the convention for "all elements are at
most x." The half-open convention makes that "one past the end"
case natural.

The mental model is this. The window `[lo, hi)` represents the
range of indices that could *still* be the answer. We start
with `lo = 0` and `hi = len(arr)` — every index from 0 up to
len(arr) (inclusive of len(arr), to represent "no valid index"
as the worst-case answer). We then halve the window each
iteration.

At each step, look at `mid = (lo + hi) // 2`. Compare
`arr[mid]` with the target:

- If `arr[mid] > x`: `mid` is a valid **candidate** for the
  answer (it has the property "arr[mid] > x"). But there might
  be an even earlier index also satisfying the property. So we
  keep `mid` in the window and try smaller indices: `hi = mid`.
- If `arr[mid] <= x`: `mid` is **disqualified** (its value is
  not strictly greater than x). The answer must be at some
  later index: `lo = mid + 1`.

When `lo == hi`, the window has collapsed to a single point.
That point is the answer.

Notice the asymmetry: on the candidate branch we use `hi = mid`
(keep mid in the window); on the disqualified branch we use
`lo = mid + 1` (exclude mid). This asymmetry is what makes
lower/upper bound work. Get it wrong and the algorithm either
returns the wrong index or loops forever.

The lower-bound version differs in exactly one place: the
condition. Lower bound uses `arr[mid] >= x` for the candidate
branch (because we want "first index with value at least x"),
while upper bound uses `arr[mid] > x` (strict). Same skeleton,
strict comparison flipped.

Worked example on `arr = [1, 2, 3, 3, 5, 8]`, `x = 3`:

- `lo = 0, hi = 6`. `mid = 3`. `arr[3] = 3`. Is `3 > 3`? No.
  Disqualified: `lo = mid + 1 = 4`.
- `lo = 4, hi = 6`. `mid = 5`. `arr[5] = 8`. Is `8 > 3`? Yes.
  Candidate: `hi = mid = 5`.
- `lo = 4, hi = 5`. `mid = 4`. `arr[4] = 5`. Is `5 > 3`? Yes.
  Candidate: `hi = mid = 4`.
- `lo = 4, hi = 4`. Loop exits.
- Return `lo = 4`. Correct — the first index with value > 3 is
  index 4 (value `5`).

Three iterations on a six-element array. `log2(6) ≈ 2.6`, so the
worst case is about 3 iterations. The math checks out.
''',
        "optimized": {
            "explanation": r'''
Half-open binary search with the "strict greater than" decision
rule. `O(log n)` time, `O(1)` space.
''',
            "code": r'''def upper_bound(arr: list[int], x: int) -> int:
    # Initialize the half-open window [lo, hi). The smallest possible
    # answer is 0 (the very first index satisfies the property — i.e.,
    # arr[0] > x). The largest possible answer is len(arr) (no index
    # satisfies; the answer is "one past the end").
    lo, hi = 0, len(arr)
    # Continue while the window is non-empty. The half-open
    # convention says the window is non-empty when lo < hi.
    while lo < hi:
        # Midpoint of the current window. Integer division rounds
        # toward zero, giving a valid index in [lo, hi - 1].
        mid = (lo + hi) // 2
        # Read the value at the midpoint.
        if arr[mid] > x:
            # arr[mid] is strictly greater than x. So mid IS a valid
            # candidate for the answer — it satisfies the "first index
            # with value > x" requirement. But there might be an even
            # earlier index that also satisfies. So we KEEP mid in the
            # window and try the left half.
            # Note the assignment: hi = mid, NOT mid - 1. This is the
            # critical detail of half-open lower/upper bound. We are
            # NOT excluding mid; we are still considering it.
            hi = mid
        else:
            # arr[mid] <= x. So mid is DISQUALIFIED. The answer must
            # be strictly to the right. We can safely exclude mid by
            # setting lo = mid + 1.
            lo = mid + 1
    # The window has collapsed to lo == hi. That single index is the
    # answer. It might be len(arr) if no element exceeds x.
    return lo
''',
            "complexity": (
                "**Time**: *O(log n)*. The window halves each "
                "iteration.\n\n"
                "**Space**: *O(1)*. Just three integer variables."
            ),
        },
        "deep_concept": r'''
Upper and lower bound are *the* atomic operations of sorted
arrays. Every higher-level sorted-array query factors through
one or both of them. Internalize the half-open convention and
the asymmetric `hi = mid` / `lo = mid + 1` updates, and you
have built a powerful primitive.

The half-open style scales beautifully. The same algorithm with
a different comparison handles:

- **First index with value >= x**: change `arr[mid] > x` to
  `arr[mid] >= x` (this is `lower_bound`).
- **First index satisfying any monotonic predicate** `pred(i)`:
  change the comparison to `pred(mid)`. This is the
  "generalized binary search" template that solves "find the
  smallest k such that property holds" problems.

This generalization is the beautiful unifying view of binary
search. You are not just searching arrays — you are searching
any **monotonic decision space** for the threshold where the
decision flips. Whether the decision is "is arr[mid] > x?",
"can Koko eat this fast?", or "is this candidate divisor
small enough?", the skeleton is identical.

This is the doorway to **binary search on the answer**, which
we covered in `koko-bananas` and which appears throughout Step
4 Lecture 2.
''',
        "confusion_notes": [
            {
                "question": "Why `hi = len(arr)` and not `hi = len(arr) - 1`?",
                "answer": r'''
Because the answer can legitimately be `len(arr)` — meaning
"no index in the array satisfies the condition; the answer is
one past the end." The half-open convention represents this as
a real candidate value in the window.

If we initialized `hi = len(arr) - 1` and used the inclusive
convention, we would not be able to represent "no match" as
a normal window collapse. We would need an external "not
found" sentinel (like -1), and the boundary logic would become
muddier.

By starting `hi` at `len(arr)`, the search naturally returns
`len(arr)` when no element satisfies the condition. The
"no match" case is just a normal answer in the half-open
universe.

Walk through `arr = [1, 2, 3]`, `x = 5`:

- `lo = 0, hi = 3`. `mid = 1`. `arr[1] = 2`. Is `2 > 5`? No.
  `lo = 2`.
- `lo = 2, hi = 3`. `mid = 2`. `arr[2] = 3`. Is `3 > 5`? No.
  `lo = 3`.
- `lo = 3, hi = 3`. Loop exits.
- Return `3` = `len(arr)`. Correct: "no element is greater than
  5; the upper bound would be just past the end."

If `hi` had started at `len(arr) - 1 = 2`, we would lose this
case.
''',
            },
            {
                "question": "When would I use upper bound instead of lower bound?",
                "answer": r'''
Use **upper bound** when you want "strictly greater than" or
"first position past the duplicates" semantics.

Use **lower bound** when you want "at least" or "first position
of x or where x would be inserted before duplicates" semantics.

Concrete distinctions:

- **Lower bound** of x: first index with value ≥ x.
- **Upper bound** of x: first index with value > x.

When inserting `x` to keep the array sorted:

- If you want `x` inserted *before* any existing copies of `x`
  → use lower bound as the insertion position.
- If you want `x` inserted *after* any existing copies of `x`
  → use upper bound.

When counting occurrences of `x`:

- `count_of_x = upper_bound(x) - lower_bound(x)`.

When finding the *last* occurrence of `x`:

- `last_index = upper_bound(x) - 1`, then verify `arr[last_index]
  == x`.

So the choice depends entirely on the question you're asking.
For "where does x belong (before duplicates)?", lower bound.
For "where does x end (after duplicates)?", upper bound.
''',
            },
            {
                "question": "What if there are no elements equal to x in the array?",
                "answer": r'''
Both upper and lower bound still return meaningful values —
specifically, the **insertion position** that would keep the
array sorted.

For `arr = [1, 3, 5, 7]` and `x = 4`:

- `lower_bound(arr, 4) = 2` (first index with value ≥ 4 is
  index 2, value 5).
- `upper_bound(arr, 4) = 2` (first index with value > 4 is also
  index 2).

Notice that when `x` is *not* in the array, `lower_bound(x) ==
upper_bound(x)`. The count of `x` is `0`, which is exactly
`upper_bound - lower_bound`.

This is the elegance of the lower/upper bound abstraction. They
work uniformly whether `x` is present, absent, present once,
or present many times. No special cases.

For your test code, check both presence and position:

```python
def find_exact(arr, x):
    i = lower_bound(arr, x)
    if i < len(arr) and arr[i] == x:
        return i           # x is present at index i
    return -1              # x is not present
```

This composition — lower bound plus a presence check — is the
cleanest way to implement "find x exactly" using the half-open
style.
''',
            },
            {
                "question": "Why not just use `bisect.bisect_right` from the standard library?",
                "answer": r'''
You absolutely should, in production code. `bisect.bisect_right`
is `upper_bound`, written in optimized C, and well-tested.
Same for `bisect.bisect_left` (which is `lower_bound`).

```python
import bisect

upper = bisect.bisect_right(arr, x)
lower = bisect.bisect_left(arr, x)
```

For real code, these are the right answers.

For interview practice, you should still write the algorithm by
hand. The interview is testing whether you understand binary
search, not whether you know the standard library. The
hand-rolled version proves the understanding.

A balanced answer in an interview: "I'd use `bisect.bisect_right`
in production. Here's how I'd implement it by hand to show
I understand what's happening underneath." Then write the
function. Best of both worlds.

A subtle point: `bisect.insort` exists for "insert x in sorted
order." It uses `bisect_left` internally and then `list.insert`,
making the total cost `O(n)` (the insert shifts elements). For
truly fast sorted insertion, you'd need a tree or skip list,
which is rare in Python interview contexts.
''',
            },
        ],
        "summary": r'''
**Pattern**: half-open binary search with `hi = mid` on the
candidate branch, `lo = mid + 1` otherwise. Comparison: `arr[
mid] > x` (strict).

**Lesson**: upper bound and lower bound are the atomic
operations of sorted-array work. Master them and a whole family
of range queries becomes one-liners.

**Recognize next time**: "where does this value fit (after
duplicates)?", "count of values ≤ x", "last occurrence of x" —
all upper bound. For "where does this value fit (before
duplicates)?" and "count of values < x", use lower bound.
''',
    },
    {
        "id": "search-insert-position",
        "title": "Search Insert Position",
        "step_id": 4,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["binary-search", "fundamentals"],
        "what_this_teaches": (
            "How lower bound is the SAME as 'where would I insert "
            "this value to keep the array sorted?'. The two questions "
            "are different costumes on the same algorithm."
        ),
        "pattern": "Lower bound on the sorted array gives the insert position.",
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["binary-search", "lower-bound", "upper-bound"],
        "next_problems": ["first-last-occurrence", "floor-ceil-sorted"],
        "resources": [
            _SHEET,
            _lc(35, "search-insert-position"),
        ],
        "understanding": r'''
You are given a sorted array of distinct integers and a target
value. Return the index where the target would be **inserted to
keep the array sorted**. If the target already exists, return
its index.

Examples on `arr = [1, 3, 5, 6]`:

- `target = 5`: return `2` (target already at index 2).
- `target = 2`: return `1` (would be inserted between 1 and 3).
- `target = 7`: return `4` (would go at the end).
- `target = 0`: return `0` (would go at the start).

At first glance this looks different from "binary search for
target." But it is the **same operation** wearing a different
costume. The answer is literally the **lower bound** of the
target.

Why? Because "insert position to keep sorted" means "the first
index whose existing value is at least the target." If we
insert there, every existing element greater-or-equal stays to
the right; every smaller element stays to the left; sortedness
is preserved.

Recognizing this equivalence is one of the small but important
moments in DSA practice. "Search insert position" is just the
search for the target's lower bound, with a slight
re-interpretation of the return value: "this is where the
target lives now, or where it would be inserted."

This is also why Python's `bisect.bisect_left` is called
"bisect" — it's the bisection (binary search) that splits the
sorted array into elements `< target` and elements `≥ target`,
returning the split point.
''',
        "brute_force": {
            "explanation": r'''
The naive idea: walk the array left to right; return the first
index whose value is at least the target. If you finish without
finding such an index, return `len(arr)`.

```python
def search_insert_linear(arr, target):
    for i in range(len(arr)):
        if arr[i] >= target:
            return i
    return len(arr)
```

`O(n)` time. Correct on any array. Uses sortedness implicitly —
if the array weren't sorted, the answer wouldn't make sense.

Useful as a baseline and for very small arrays. For anything
larger, binary search wins.
''',
            "code": r'''def search_insert_linear(arr: list[int], target: int) -> int:
    # Walk the array from left to right.
    for i in range(len(arr)):
        # The first index where the existing value is >= target is
        # where we would insert.
        if arr[i] >= target:
            return i
    # Every element was smaller than target. Insert at the end.
    return len(arr)
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "thought_process": r'''
The optimized algorithm is **lower bound** — exactly the
algorithm from the previous problem, no modifications. The
"insert position" is just another name for lower bound.

The recognition is the key. When you read the problem and notice
"keep the array sorted," your brain should immediately translate
to "lower bound." Then the rest is mechanical.

Same half-open binary search. Same `hi = mid` on the candidate
branch. Same `lo = mid + 1` on the disqualified branch. The
only change is the comparison: lower bound uses `>=` (we want
the first index whose value is at least the target).

Worked example on `arr = [1, 3, 5, 6]`, `target = 5`:

- `lo = 0, hi = 4`. `mid = 2`. `arr[2] = 5`. Is `5 >= 5`? Yes.
  Candidate: `hi = 2`.
- `lo = 0, hi = 2`. `mid = 1`. `arr[1] = 3`. Is `3 >= 5`? No.
  `lo = 2`.
- `lo = 2, hi = 2`. Loop exits.
- Return `2`. Correct.

Another example, `target = 2`:

- `lo = 0, hi = 4`. `mid = 2`. `arr[2] = 5`. Is `5 >= 2`? Yes.
  `hi = 2`.
- `lo = 0, hi = 2`. `mid = 1`. `arr[1] = 3`. Is `3 >= 2`? Yes.
  `hi = 1`.
- `lo = 0, hi = 1`. `mid = 0`. `arr[0] = 1`. Is `1 >= 2`? No.
  `lo = 1`.
- `lo = 1, hi = 1`. Loop exits.
- Return `1`. Correct (between 1 and 3).

About 2-3 iterations on a four-element array. Logarithmic
scaling.
''',
        "optimized": {
            "explanation": r'''
Lower bound, by another name. Half-open binary search.
''',
            "code": r'''def search_insert(arr: list[int], target: int) -> int:
    # Initialize the half-open window [lo, hi). The answer ranges
    # from 0 to len(arr) inclusive.
    lo, hi = 0, len(arr)
    while lo < hi:
        # Midpoint of the current window.
        mid = (lo + hi) // 2
        if arr[mid] >= target:
            # mid IS a candidate — its value is at least target. There
            # might be an earlier candidate, so keep mid in the window
            # and try smaller indices.
            hi = mid
        else:
            # arr[mid] is strictly less than target. mid is NOT a
            # candidate. The answer is strictly to the right.
            lo = mid + 1
    # Window has collapsed to a single point. That is the answer.
    return lo
''',
            "complexity": "**Time**: *O(log n)*. **Space**: *O(1)*.",
        },
        "deep_concept": r'''
The deep observation: a sorted array has many "queries" that
*look* different but all reduce to lower bound or upper bound
with small variations. Memorize the mapping:

- "find x (or -1)" → lower bound + presence check.
- "where does x belong?" → lower bound (insert position).
- "first occurrence of x" → lower bound + presence check.
- "last occurrence of x" → upper bound - 1 + presence check.
- "count of x" → upper bound - lower bound.
- "floor of x" (largest value ≤ x) → lower bound - 1 (with
  guards).
- "ceil of x" (smallest value ≥ x) → lower bound.
- "number of values < x" → lower bound.
- "number of values ≤ x" → upper bound.
- "number of values in [L, R]" → upper bound(R) - lower
  bound(L).

Twelve different questions, two underlying operations. Once you
have lower bound and upper bound, every other query is a small
adjustment.

This is why investing time in mastering these two operations
pays off so much: they are the foundation of an entire
problem family.
''',
        "confusion_notes": [
            {
                "question": "How is this different from plain binary search?",
                "answer": r'''
Plain binary search returns -1 (or some "not found" sentinel)
when the target is absent. Search insert position returns the
position where the target *would be* if inserted to keep the
array sorted.

They overlap when the target *is* present: both return the
index of the target.

The difference is in the "not found" case:

- **Plain binary search** on `[1, 3, 5, 6]` with target `2`:
  returns `-1`.
- **Search insert position** on the same: returns `1` (between
  1 and 3).

Lower bound (and therefore search insert position) is the more
general operation. It handles both "present" and "absent" cases
with the same return value semantics. Plain binary search needs
the extra "not found" sentinel.

In practice, when interviewers ask "find x in a sorted array,"
you can solve it with lower bound + a presence check:

```python
i = lower_bound(arr, x)
return i if i < len(arr) and arr[i] == x else -1
```

That's cleaner than rolling your own binary search with -1
return.
''',
            },
            {
                "question": "Does this work if the array has duplicates?",
                "answer": r'''
The problem statement usually says "distinct integers," but the
algorithm works on arrays with duplicates too.

For `arr = [1, 3, 3, 5]` and `target = 3`:

- Lower bound returns `1` (first index with value ≥ 3).
- Upper bound returns `3` (first index with value > 3).

So if the problem asks "where would I insert target?" with
duplicates allowed, the answer depends on convention:

- Insert **before** any existing duplicates → use lower bound.
- Insert **after** any existing duplicates → use upper bound.

The LeetCode 35 problem assumes distinct elements, so both
interpretations give the same answer. But if you encounter a
variant with duplicates, the choice between lower/upper bound
encodes the desired insert position.

Internalize: lower bound is "insert before equals"; upper bound
is "insert after equals." That single distinction handles
every duplicate-handling decision in sorted-array problems.
''',
            },
            {
                "question": "What if I get an empty array as input?",
                "answer": r'''
The algorithm handles it gracefully. With `arr = []` and any
target:

- `lo = 0, hi = 0`. The window is empty (lo == hi).
- The loop body never executes.
- Return `lo = 0`.

Which is correct: an empty array has only one possible insert
position — index 0 (the start, which is also the end).

This is one of those edge cases that the algorithm handles
without special-casing. The half-open convention is robust to
empty inputs because "the window is empty" naturally
corresponds to "the answer is exactly where lo started."

This is a small but real advantage of the half-open style over
the inclusive style for this kind of problem.
''',
            },
            {
                "question": "Why is the time complexity O(log n) and not O(log n + k) for some constant k?",
                "answer": r'''
Because the loop terminates as soon as `lo == hi`, and the
window strictly shrinks by at least half each iteration.

To be precise: at each iteration, the window size is at most
`(hi - lo + 1) / 2 + 1`. Starting at size `n`, after `k`
iterations the size is at most `n / 2^k`. The loop exits when
the size is 1, which happens when `k ≈ log2(n)`.

Plus or minus a few constants for the boundary cases, the total
iteration count is `floor(log2(n)) + 1`. For `n = 10⁶`, that's
about 20.

In terms of actual operations per iteration: a comparison, an
arithmetic operation (the midpoint), and a single bound update.
All `O(1)`. So total time is `O(log n)`.

No hidden `+ k` term. The algorithm is asymptotically tight at
`O(log n)`.

For very small `n` (say, n < 10), linear search can be faster
than binary search because of cache and branch-prediction
constants. But for any non-trivial `n`, binary search wins by
orders of magnitude.
''',
            },
        ],
        "summary": r'''
**Pattern**: lower bound — half-open binary search with `arr[
mid] >= target` as the candidate condition.

**Lesson**: "where would I insert x?" is the same question as
"first index with value ≥ x." Recognize the equivalence and the
problem becomes lower bound with a different name.

**Recognize next time**: any "insert position," "place in sorted
order," or "where would x go" problem reduces to lower (or upper)
bound. Choose based on duplicate-handling semantics.
''',
    },
    {
        "id": "count-occurrences",
        "title": "Count Occurrences of a Number in a Sorted Array",
        "step_id": 4,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["binary-search", "fundamentals"],
        "what_this_teaches": (
            "How upper bound and lower bound, subtracted, give the "
            "count of a value in *O(log n)* — far better than a "
            "linear scan even though the linear version is much "
            "easier to write."
        ),
        "pattern": "count = upper_bound(x) - lower_bound(x).",
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["lower-bound", "upper-bound", "first-last-occurrence"],
        "next_problems": ["search-rotated-i", "search-rotated-ii"],
        "resources": [_SHEET],
        "understanding": r'''
Given a sorted array and a target, return the number of
occurrences of the target.

For `arr = [1, 2, 2, 2, 3, 4, 5]` and `target = 2`, the answer
is 3.

The brute force is *O(n)* — walk the array, count matches.
Simple, correct, and totally adequate for small arrays:

```python
def count_brute(arr, x):
    return arr.count(x)
```

But the problem specifically lists this in Striver's "BS on 1D
arrays" lecture because there is an *O(log n)* solution using
the lower-bound / upper-bound composition we already mastered
in `first-last-occurrence`.

The formula is one line:

> **count = upper_bound(target) - lower_bound(target).**

The reasoning: the run of duplicates of `target` in the sorted
array occupies the half-open range `[lower_bound, upper_bound)`.
The length of that range — that is, the count of duplicates —
is `upper_bound - lower_bound`. If the target is absent, both
bounds are equal and the count is zero.

Worked example on `arr = [1, 2, 2, 2, 3, 4, 5]`, `target = 2`:

- `lower_bound(2)` = 1 (first index with value ≥ 2).
- `upper_bound(2)` = 4 (first index with value > 2).
- count = 4 - 1 = 3. Correct.

For an absent target: `arr`, `target = 6`.

- `lower_bound(6)` = 7 (past the end).
- `upper_bound(6)` = 7.
- count = 0. Correct.

For target equal to the maximum: `target = 5`.

- `lower_bound(5)` = 6 (the last index, where 5 sits).
- `upper_bound(5)` = 7 (past the end).
- count = 1. Correct.

The formula handles every case — present once, present many
times, absent, at the edges — uniformly.
''',
        "brute_force": {
            "explanation": r'''
Linear scan. Walk and count. *O(n)*.

This is the answer most beginners reach for, and it's correct.
The optimal *O(log n)* exists only because the array is sorted,
but if you didn't notice that detail, the brute force still
works.

```python
return arr.count(x)
```

One line via Python's built-in. Or write it yourself:

```python
count = 0
for v in arr:
    if v == x:
        count += 1
return count
```

For arrays up to ~10,000 elements, the linear version is often
fast enough that the *O(log n)* improvement is not worth the
extra code. For large datasets — say, querying a million-element
array many times — the binary-search version is essential.
''',
            "code": r'''def count_brute(arr: list[int], x: int) -> int:
    # Python's list has a built-in .count() that walks the list and
    # counts equality matches. O(n).
    return arr.count(x)
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "thought_process": r'''
The optimal algorithm is two binary searches — one for lower
bound, one for upper bound. The composition is so clean that
the entire function is three lines:

```python
def count(arr, x):
    return upper_bound(arr, x) - lower_bound(arr, x)
```

Why does this work? The values equal to `x` in a sorted array
form a contiguous block. Lower bound is the first index of that
block (or the insertion position if x is absent). Upper bound
is one past the last index of the block. The block length is
the difference.

Even better: the formula handles the "x is absent" case
automatically. When x is absent, lower bound and upper bound
coincide (both pointing at the insertion position). The
difference is 0.

This is the same composition we used in `first-last-occurrence`.
There we returned `[first, last]`; here we return `last - first
+ 1` (equivalently, `upper - lower`). Same two searches; different
interpretation of the result.

For an array of size 10 million, this counts in about 50
operations total. The linear scan would do 10 million.
''',
        "optimized": {
            "explanation": r'''
Two half-open binary searches; difference of their results.
''',
            "code": r'''def count_occurrences(arr: list[int], x: int) -> int:
    # Helper: find the first index whose value is >= x.
    def lower_bound(target):
        lo, hi = 0, len(arr)
        while lo < hi:
            mid = (lo + hi) // 2
            if arr[mid] >= target:
                hi = mid
            else:
                lo = mid + 1
        return lo

    # Helper: find the first index whose value is > x.
    def upper_bound(target):
        lo, hi = 0, len(arr)
        while lo < hi:
            mid = (lo + hi) // 2
            if arr[mid] > target:
                hi = mid
            else:
                lo = mid + 1
        return lo

    # The count is the length of the half-open range
    # [lower_bound, upper_bound). If x is absent, lower == upper
    # and the count is zero.
    return upper_bound(x) - lower_bound(x)
''',
            "complexity": (
                "**Time**: *O(log n)*. Two binary searches of *O(log n)* "
                "each.\n\n"
                "**Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
The count formula `upper_bound(x) - lower_bound(x)` is the
canonical example of "compose two atomic operations to answer
a richer query in the same complexity class."

This composition generalizes:

- **Count of values in `[L, R]`** (range count): `upper_bound(R)
  - lower_bound(L)`. Two binary searches, *O(log n)*.
- **Count of values strictly less than x**: `lower_bound(x)`.
- **Count of values strictly greater than x**: `len(arr) -
  upper_bound(x)`.

All of these reduce to one or two lower/upper bound calls.
Master the primitives; the queries become one-liners.

For very many queries on the same array, you can preprocess
(sort once) and then answer each query in *O(log n)*. This is
the **offline-query** pattern that powers many problems
involving repeated range queries.
''',
        "confusion_notes": [
            {
                "question": "Why is this in the binary search lecture if Python has `arr.count()`?",
                "answer": r'''
Because Python's `arr.count()` is `O(n)` — it walks the entire
list, comparing each element. The interview challenge is to
beat that by exploiting the sortedness.

For sorted data, you should never need a linear scan to count.
The bisect functions get you to `O(log n)`, which for a million-
element array means about 40 operations versus a million.

If your data isn't sorted, you'd sort first (*O(n log n)*) and
then count (*O(log n)*) for a total of *O(n log n)*. For a
one-shot count, that's worse than just `arr.count(x)`. The
trade-off is worthwhile only when you'll do many counts on the
same array.

The interview question tests two things:
1. Did you notice the sortedness?
2. Can you reduce the problem to lower bound / upper bound?

If both yes, you write the *O(log n)* solution. If you reach
for `arr.count(x)`, you've passed up the harder lesson.
''',
            },
            {
                "question": "What if I want to count occurrences in a range `[L, R]` of values?",
                "answer": r'''
Same idea, slightly different bounds.

```python
def count_in_range(arr, low, high):
    # Count values v with low <= v <= high.
    # That's lower_bound(low) ... upper_bound(high) - 1 (inclusive).
    # Equivalently, upper_bound(high) - lower_bound(low).
    return upper_bound(arr, high) - lower_bound(arr, low)
```

Two binary searches, *O(log n)*. Beautiful.

This is the engine behind many problems involving "how many
elements satisfy a range condition?". For 2D ranges, you'd
need a 2D indexing structure (k-d tree, BIT), but for 1D
this is enough.
''',
            },
        ],
        "summary": r'''
**Pattern**: count = upper_bound(x) - lower_bound(x).

**Lesson**: a single formula composing two binary searches
counts the occurrences of any value in a sorted array in
*O(log n)*. The same composition handles range counts.

**Recognize next time**: "how many ___ in sorted array" → reach
for upper - lower.
''',
    },
    {
        "id": "min-in-rotated",
        "title": "Find Minimum in Rotated Sorted Array",
        "step_id": 4,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["binary-search", "rotated"],
        "what_this_teaches": (
            "The 'one half is sorted' insight applied to finding the "
            "pivot point in a rotated array. Binary search adapts by "
            "comparing the midpoint to the right endpoint."
        ),
        "pattern": "Compare arr[mid] with arr[hi]; one side is sorted, the other contains the pivot.",
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["binary-search", "search-rotated-i"],
        "next_problems": ["rotations-count", "single-element-sorted"],
        "resources": [
            _SHEET,
            _lc(153, "find-minimum-in-rotated-sorted-array"),
        ],
        "understanding": r'''
A sorted array has been rotated some unknown number of times.
Find its minimum element.

`[4, 5, 6, 7, 0, 1, 2]` was originally `[0, 1, 2, 4, 5, 6, 7]`
rotated four positions to the left. The minimum is `0`, at
index 4 in the rotated array.

If the array were not rotated, the minimum would be at index 0
— trivial. But because of the rotation, the minimum is at some
unknown "pivot" point where the original sequence wraps around.

Brute force is *O(n)* — scan and track the minimum. The
optimal is *O(log n)* using a clever binary search that
exploits the partial sortedness.

The key insight: at every midpoint of the rotated array, **one
of the two halves is fully sorted**. The minimum lives either in
the *unsorted* half (which contains the wrap-around point) or
at the very start of the sorted half (the smallest element of
that half, which equals the leftmost element of the sorted
half).

Concretely, at any `mid`, compare `arr[mid]` with `arr[hi]`
(the right endpoint of the current window):

- If `arr[mid] < arr[hi]`: the right half (from `mid` to `hi`)
  is sorted, because values rise smoothly from mid to hi. The
  minimum is either at `mid` itself or somewhere strictly to
  its left. So set `hi = mid` (keeping mid as a candidate).
- If `arr[mid] > arr[hi]`: the right half is NOT sorted. The
  pivot lies somewhere in `(mid, hi]`. So set `lo = mid + 1`.

When the loop terminates, `lo == hi` is the index of the
minimum.

Why compare with `arr[hi]` and not `arr[lo]`? Because the
comparison with the right endpoint cleanly distinguishes "the
right half is sorted" (then mid could be the min) from "the
right half contains the pivot" (then min is past mid). The
left-endpoint comparison is muddier because the left half is
*always* sorted if there is no rotation — it doesn't help us
locate the pivot.

This problem assumes the array has **no duplicates**. With
duplicates, the comparison `arr[mid] vs arr[hi]` can be
ambiguous (they might be equal), and the worst-case complexity
degrades to *O(n)*. That variant is "Find Minimum in Rotated
Sorted Array II" (LC 154).
''',
        "brute_force": {
            "explanation": r'''
Walk the array; track the minimum.

```python
def find_min_linear(arr):
    return min(arr)
```

`O(n)` time. Correct on any array, rotated or not. For small
arrays, this is faster than the binary search version because
of branch prediction and cache effects.

The interview challenge is to do it in *O(log n)*. The binary
search version exploits the partial sortedness.
''',
            "code": r'''def find_min_linear(arr: list[int]) -> int:
    # Python's min() walks the iterable once. O(n).
    return min(arr)
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "thought_process": r'''
The *O(log n)* algorithm uses binary search with the comparison
`arr[mid] vs arr[hi]`. This comparison detects whether the right
half is fully sorted (no wrap-around) or contains the pivot.

Walk through `arr = [4, 5, 6, 7, 0, 1, 2]`:

- `lo = 0, hi = 6`. `mid = 3`, `arr[3] = 7`, `arr[6] = 2`.
  `7 > 2`, so the right half is NOT sorted — the pivot is to
  the right of mid. Set `lo = 4`.
- `lo = 4, hi = 6`. `mid = 5`, `arr[5] = 1`, `arr[6] = 2`.
  `1 < 2`, so the right half IS sorted. The minimum could be at
  mid (= 5) or to its left. Set `hi = 5`.
- `lo = 4, hi = 5`. `mid = 4`, `arr[4] = 0`, `arr[5] = 1`.
  `0 < 1`, right half is sorted. Set `hi = 4`.
- `lo = 4, hi = 4`. Loop exits.
- Return `arr[4] = 0`. Correct.

Three iterations on a seven-element array. `log2(7) ≈ 2.8`, so
the math checks out.

Why does comparing `arr[mid]` with `arr[hi]` work? Because in a
rotated sorted array, exactly one place has a "drop" (where the
original maximum is followed by the original minimum). If
`arr[mid] < arr[hi]`, there is no drop between mid and hi — that
half is sorted. If `arr[mid] > arr[hi]`, the drop is somewhere
in `(mid, hi]`, meaning the minimum is in the right half.

The candidate / disqualified asymmetry in the bound update
matters: on the sorted-right-half branch, we set `hi = mid`
(keeping mid as a candidate, because mid could be the minimum
of that sorted right half). On the other branch, we set `lo =
mid + 1` (excluding mid, because the actual minimum is strictly
past it).

This same "one half is sorted" insight powers `search-rotated-
i` (search for an arbitrary target in a rotated array). The two
problems are siblings.
''',
        "optimized": {
            "explanation": r'''
Binary search comparing midpoint to the right endpoint. The
half-open / inclusive convention is mixed here because we use
`hi = mid` (keep mid as candidate) and `lo = mid + 1` (exclude).
''',
            "code": r'''def find_min(arr: list[int]) -> int:
    # Initialize the search window as inclusive endpoints.
    lo, hi = 0, len(arr) - 1
    # Continue while the window has more than one element. When
    # lo == hi, that single index is the minimum's location.
    while lo < hi:
        # Midpoint of the current window.
        mid = (lo + hi) // 2
        # Compare the midpoint with the RIGHT endpoint. This is the
        # key. The right half [mid, hi] is fully sorted iff
        # arr[mid] < arr[hi]. If sorted, the minimum of that half
        # is at mid itself (the leftmost). So mid is a candidate.
        if arr[mid] < arr[hi]:
            # mid IS a candidate. Keep it in the window and try
            # smaller indices.
            hi = mid
        else:
            # arr[mid] > arr[hi]. The right half is not sorted; the
            # pivot (and thus the minimum) is strictly past mid.
            lo = mid + 1
    # Loop exits with lo == hi. That index holds the minimum.
    return arr[lo]
''',
            "complexity": "**Time**: *O(log n)*. **Space**: *O(1)*.",
        },
        "deep_concept": r'''
The `arr[mid] vs arr[hi]` comparison is the heart of every
rotated-array binary search. It lets us answer "which half is
sorted?" in *O(1)*, and from that we can decide which half to
keep.

The reason we compare with `arr[hi]` instead of `arr[lo]` is
subtle and worth understanding. The left endpoint is **always**
the same value (the start of the window doesn't necessarily
have any sortedness signal), so `arr[lo] vs arr[mid]` doesn't
distinguish "left half is sorted" from "left half has the
pivot" cleanly. The right endpoint, by contrast, sits at the
end of the unrotated tail (or at the rotated minimum's
neighbor), so it gives a reliable signal.

A symmetric algorithm exists comparing with `arr[lo]`, but the
boundary updates are slightly trickier. The `arr[mid] vs arr[
hi]` style is the cleanest.

For **rotated array with duplicates** (LC 154), this algorithm
breaks down when `arr[mid] == arr[hi]`. We can't tell which
half is sorted. The fix is to decrement `hi` by 1 in that case
(skip past the duplicate). The worst case degrades to *O(n)*
when the array is mostly duplicates, but the average case stays
*O(log n)*.

The related problem "search for a target in a rotated sorted
array" (LC 33) uses the same "one half is sorted" insight, but
with two comparisons per iteration: first identify the sorted
half, then check if the target lies in that half's range.
''',
        "confusion_notes": [
            {
                "question": "Why not compare with the left endpoint?",
                "answer": r'''
Because the left-endpoint comparison is ambiguous about where
the pivot lives.

If `arr[mid] > arr[lo]`: the left half is sorted (no drop
between lo and mid). The pivot is somewhere in `[mid+1, hi]`.
But the minimum of the whole array could be either at the start
of the sorted left half (`arr[lo]`) or in the right half. We
can't tell which.

If `arr[mid] < arr[lo]`: the left half contains the pivot. The
minimum is in `[lo+1, mid]`.

So we can use the left-endpoint comparison to drive a binary
search, but it requires comparing the global minimum candidate
to `arr[lo]` at each step. Messier.

The right-endpoint comparison is cleaner: `arr[mid] < arr[hi]`
unambiguously means "right half is sorted, mid could be the
minimum." `arr[mid] > arr[hi]` unambiguously means "the
minimum is strictly past mid."

So we go with `arr[hi]`. The algorithm has a beautiful single
comparison per iteration.
''',
            },
            {
                "question": "Does this work if the array is not actually rotated?",
                "answer": r'''
Yes. An unrotated array is trivially a "rotation by 0," and
the algorithm finds index 0 as the minimum.

Walk through `arr = [1, 2, 3, 4, 5]`:

- `lo = 0, hi = 4`. `mid = 2`, `arr[2] = 3`, `arr[4] = 5`. `3 <
  5`, so right half is sorted. `hi = 2`.
- `lo = 0, hi = 2`. `mid = 1`, `arr[1] = 2`, `arr[2] = 3`. `2 <
  3`, right half is sorted. `hi = 1`.
- `lo = 0, hi = 1`. `mid = 0`, `arr[0] = 1`, `arr[1] = 2`. `1 <
  2`, right half is sorted. `hi = 0`.
- `lo = 0, hi = 0`. Loop exits.
- Return `arr[0] = 1`. Correct.

The algorithm is robust to the "no rotation" edge case.
''',
            },
            {
                "question": "What if the array has a single element?",
                "answer": r'''
The loop doesn't execute (since `lo == hi == 0`), and we
return `arr[0]`. The single element is trivially the minimum.

What about two elements?

`arr = [2, 1]`:

- `lo = 0, hi = 1`. `mid = 0`, `arr[0] = 2`, `arr[1] = 1`. `2 >
  1`, right half is NOT sorted. `lo = 1`.
- `lo = 1, hi = 1`. Loop exits.
- Return `arr[1] = 1`. Correct.

`arr = [1, 2]`:

- `lo = 0, hi = 1`. `mid = 0`, `arr[0] = 1`, `arr[1] = 2`. `1 <
  2`, right half IS sorted. `hi = 0`.
- `lo = 0, hi = 0`. Loop exits.
- Return `arr[0] = 1`. Correct.

The algorithm handles all small cases correctly.
''',
            },
        ],
        "summary": r'''
**Pattern**: binary search with `arr[mid] vs arr[hi]`
comparison; the right-endpoint comparison detects which half is
sorted and hence where the minimum lives.

**Lesson**: rotated arrays preserve enough sortedness for
*O(log n)* search. The trick is comparing with the right
endpoint, which gives the cleanest sorted-half signal.

**Recognize next time**: rotated-sorted-array problems —
finding the minimum, the rotation count, or any specific value.
They all hinge on "one half is always sorted."
''',
    },
    {
        "id": "rotations-count",
        "title": "Number of Times a Sorted Array Has Been Rotated",
        "step_id": 4,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["binary-search", "rotated"],
        "what_this_teaches": (
            "Same algorithm as find-minimum-in-rotated, but return "
            "the *index* of the minimum instead of the value. The "
            "index *is* the rotation count."
        ),
        "pattern": "Find the index of the minimum; that index is the rotation count.",
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["min-in-rotated"],
        "next_problems": ["single-element-sorted"],
        "resources": [_SHEET],
        "understanding": r'''
A sorted array has been rotated some unknown number of times.
Find the **rotation count** — the number of left rotations
that would produce the array from the original sorted version.

For `arr = [4, 5, 6, 7, 0, 1, 2]`: the original sorted array
was `[0, 1, 2, 4, 5, 6, 7]`, rotated 4 times to the left. The
minimum (`0`) is now at index 4. So the rotation count is 4.

The key insight: **the index of the minimum element in the
rotated array IS the rotation count**. Why? Because rotating
the sorted array `k` times to the left moves the original
minimum (which was at index 0) to index `n - k` (mod n)…
wait, actually a left rotation by 1 moves arr[0] to arr[n-1],
so a left rotation by k moves arr[0] to arr[n-k]. Equivalently,
the original index 0 (the minimum) lands at index `n - k mod
n`. Hmm.

Let me re-examine: actually, a left rotation by `k` shifts
every element `k` positions to the left, with wrapping. So
`arr[i]` ends up at position `(i - k) mod n`. The original
index 0 (the minimum) lands at `(0 - k) mod n = -k mod n = n - k`.

For `n = 7`, `k = 4`: original index 0 lands at `n - k = 3`.
But our example has the minimum at index 4, not 3.

Let me reconsider. In the example `[4, 5, 6, 7, 0, 1, 2]`,
the minimum `0` is at index 4. To get this from the sorted
`[0, 1, 2, 4, 5, 6, 7]`, we left-rotate by 4 positions:

- After 1 left rotation: `[1, 2, 4, 5, 6, 7, 0]`. Min at index 6.
- After 2: `[2, 4, 5, 6, 7, 0, 1]`. Min at index 5.
- After 3: `[4, 5, 6, 7, 0, 1, 2]`. Min at index 4.

So actually 3 rotations, not 4. Looking at this carefully, the
formula is: **the rotation count equals the index of the
minimum** (if we count rotations toward the right) or **n minus
the index of the minimum** (if we count left rotations).

The convention varies by problem. LeetCode and Striver usually
use "the position of the minimum is the answer," which is the
right-rotation count.

The algorithm: find the index of the minimum using the
`min-in-rotated` algorithm. Return that index (not the value).
This is *O(log n)*.

The brute force is *O(n)* — scan to find the minimum's index.
''',
        "brute_force": {
            "explanation": r'''
Linear scan; find the index of the minimum.

```python
def rotation_count_linear(arr):
    return arr.index(min(arr))
```

Two passes (one for `min`, one for `index`), but both *O(n)*.
Combined, the function is *O(n)* time.

A single-pass version walks once tracking the min and its
index:

```python
def rotation_count_one_pass(arr):
    min_val = arr[0]
    min_idx = 0
    for i, v in enumerate(arr):
        if v < min_val:
            min_val = v
            min_idx = i
    return min_idx
```

Same complexity, slightly more efficient on big arrays. Both
correct.
''',
            "code": r'''def rotation_count_linear(arr: list[int]) -> int:
    # The Python idiom: index of the minimum value.
    # arr.index(x) is O(n) and finds the first occurrence of x.
    # min(arr) is O(n).
    # Total: O(n).
    return arr.index(min(arr))
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "thought_process": r'''
The optimal *O(log n)* algorithm is identical to
`find-minimum-in-rotated-sorted-array`, but instead of returning
`arr[lo]` at the end, we return `lo` itself.

This is one of those wonderful moments where two different
problems share the same algorithm — they just disagree on what
to return. The algorithm finds where the minimum lives; one
problem cares about the value, the other about the index. The
binary search code is identical.

Walking through `arr = [4, 5, 6, 7, 0, 1, 2]` produces (as we
saw in `min-in-rotated`):

- After three iterations, `lo = hi = 4`.
- Return `4`. That's the rotation count.

The rotation count is 4 (the answer matches our earlier
analysis, modulo whether we count "right" rotations or "left"
rotations).
''',
        "optimized": {
            "explanation": r'''
Identical to `min-in-rotated`'s algorithm; return the index
instead of the value.
''',
            "code": r'''def rotation_count(arr: list[int]) -> int:
    # Same binary search as find-minimum-in-rotated. The loop
    # converges to the index of the minimum.
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < arr[hi]:
            # Right half is sorted; minimum is at mid or to its left.
            hi = mid
        else:
            # Right half is not sorted; minimum is past mid.
            lo = mid + 1
    # lo == hi at this point. That is the index of the minimum,
    # which is also the rotation count.
    return lo
''',
            "complexity": "**Time**: *O(log n)*. **Space**: *O(1)*.",
        },
        "deep_concept": r'''
The lesson: **the index of the minimum in a rotated sorted array
is a useful piece of information by itself**. It tells you the
rotation count, which lets you "unrotate" the array mentally
or via slicing if needed.

If you wanted to actually unrotate the array (restore it to the
original sorted order), you'd find the minimum's index `k` and
then `arr = arr[k:] + arr[:k]`. *O(n)* but no extra storage
beyond the slicing.

Knowing the rotation count also unlocks other algorithms. For
example, "search in a rotated sorted array" (LC 33) can be
solved by first finding the rotation count, then doing a normal
binary search on the unrotated logical view. That's the "two
phases" version of the algorithm we saw in `search-rotated-i`.

The shared algorithm with `min-in-rotated` is the meta-lesson:
**many problems share an underlying algorithm and differ only in
what they report**. Recognizing this lets you batch your
learning.
''',
        "confusion_notes": [
            {
                "question": "Is this counting left rotations or right rotations?",
                "answer": r'''
By the convention used here (the minimum's index = the rotation
count), it counts **how many positions the array has been
rotated to the right** to produce the current state — or
equivalently, how many positions to the left of the original
minimum the current minimum sits.

For `[4, 5, 6, 7, 0, 1, 2]` (n = 7), the minimum is at index 4.
This means the array has been rotated 4 positions to the right
from the sorted state (or 3 positions to the left, which is
`n - 4 = 3`).

Different problems use different conventions. Read the problem
statement carefully. The most common convention in LeetCode /
Striver is "the minimum's index is the rotation count."

If a problem instead asks "how many left rotations would
produce this from the sorted version?", the answer is `n -
index_of_min` (for n > 0).
''',
            },
            {
                "question": "What if the array is not rotated (already sorted)?",
                "answer": r'''
The algorithm correctly returns 0 — the rotation count is zero.

For `arr = [1, 2, 3, 4, 5]`:

- The minimum is at index 0.
- The algorithm finds it: at every iteration, `arr[mid] < arr[
  hi]` (the right half is fully sorted), so `hi = mid` until
  `lo == hi == 0`.
- Return 0.

This makes sense: the array hasn't been rotated, so the count
is zero.
''',
            },
        ],
        "summary": r'''
**Pattern**: same as min-in-rotated; return the index instead
of the value.

**Lesson**: the rotation count of a rotated sorted array is the
index of its minimum element.

**Recognize next time**: any problem about "how rotated is this
array?" reduces to finding the minimum's index.
''',
    },
    {
        "id": "single-element-sorted",
        "title": "Single Element in a Sorted Array (Pairs Otherwise)",
        "step_id": 4,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["binary-search", "parity"],
        "what_this_teaches": (
            "How to binary-search using a *parity-of-index* signal. "
            "Every element appears twice except one; we use the "
            "index pattern of the pairs to decide which half "
            "contains the loner."
        ),
        "pattern": "Compare arr[mid] with its pair partner; the half where the pair pattern is broken contains the loner.",
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["binary-search", "single-number"],
        "next_problems": ["find-peak-element"],
        "resources": [
            _SHEET,
            _lc(540, "single-element-in-a-sorted-array"),
        ],
        "understanding": r'''
You are given a **sorted** array in which every element appears
exactly twice except for one element that appears once. Find
the single element.

Examples:

- `[1, 1, 2, 3, 3, 4, 4, 8, 8]` → `2`.
- `[3, 3, 7, 7, 10, 11, 11]` → `10`.

The brute force is *O(n)* — scan the array, return the first
element that isn't followed by its duplicate. Or use XOR on the
entire array (every duplicate cancels, the loner remains).

But the array is sorted, and the LeetCode problem asks for
*O(log n)* time and *O(1)* space. That requires exploiting the
sortedness in a clever way.

The key observation: **before the loner**, pairs occupy adjacent
indices `(0, 1), (2, 3), (4, 5), ...` — the first element of
each pair is at an **even** index. **After the loner**, pairs
shift by one and occupy `(odd, odd+1)` — the first element of
each pair is at an **odd** index.

So we can binary search: at each midpoint, check whether the
midpoint is part of a pair whose first index is even (before-
loner pattern) or odd (after-loner pattern).

If `mid` is **even** and `arr[mid] == arr[mid + 1]`, then `mid`
is the first element of an unbroken pair — we are still in the
before-loner region. The loner is to the right. Set `lo = mid +
2`.

If `mid` is **even** and `arr[mid] != arr[mid + 1]`, the pair
pattern is broken — the loner is at or before `mid`. Set `hi =
mid`.

Similar logic for odd `mid`: check pair with `mid - 1`.

A cleaner version uses bitwise XOR: `mid ^ 1` gives the partner
of `mid` (flips the last bit). If `mid` is even, partner is
`mid + 1`; if odd, partner is `mid - 1`.

```python
if arr[mid] == arr[mid ^ 1]:
    # pair is unbroken; loner is to the right
    lo = mid + 1
else:
    # pair is broken; loner is at or before mid
    hi = mid
```

This is one of the most elegant binary-search variants. It uses
**parity** as the decision signal instead of value comparison.
''',
        "brute_force": {
            "explanation": r'''
Linear scan, comparing adjacent pairs. Or XOR all values.

```python
def single_linear(arr):
    for i in range(0, len(arr) - 1, 2):
        if arr[i] != arr[i + 1]:
            return arr[i]
    return arr[-1]      # the loner is the last element
```

`O(n)` time, `O(1)` space. Correct on any "sorted array with
one loner" input.

The XOR version:

```python
def single_xor(arr):
    result = 0
    for v in arr:
        result ^= v
    return result
```

Also `O(n)`, but doesn't use the sortedness. Either is fine
for a baseline.

The challenge is the *O(log n)* solution that exploits
sortedness. The parity trick gets us there.
''',
            "code": r'''def single_linear(arr: list[int]) -> int:
    # Walk in steps of 2. Compare adjacent pairs.
    for i in range(0, len(arr) - 1, 2):
        # If a pair is broken, the loner is the first element of the
        # broken pair.
        if arr[i] != arr[i + 1]:
            return arr[i]
    # No pair was broken. The loner is the last (unpaired) element.
    return arr[-1]
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "thought_process": r'''
The *O(log n)* algorithm exploits the parity insight.

**Before the loner**, pairs are at `(even, even + 1)` indices.
That is, `arr[i] == arr[i + 1]` when `i` is even.

**After the loner**, pairs are at `(odd, odd + 1)` indices.
That is, `arr[i] == arr[i + 1]` when `i` is odd, but `arr[i]
!= arr[i + 1]` when `i` is even.

So the question "is `mid` before or after the loner?" reduces
to checking the pair-parity at `mid`.

The XOR trick `mid ^ 1` is elegant: it flips the last bit,
giving the "partner" of `mid`. If `mid` is even (binary ends
in 0), `mid ^ 1` is `mid + 1`. If `mid` is odd (ends in 1),
`mid ^ 1` is `mid - 1`. So `arr[mid ^ 1]` is the value that
should equal `arr[mid]` if `mid` is part of an unbroken pair.

```python
if arr[mid] == arr[mid ^ 1]:
    # Pair is unbroken; we're still before the loner. Loner is right.
    lo = mid + 1
else:
    # Pair is broken; loner is at or before mid.
    hi = mid
```

When the loop terminates with `lo == hi`, that index is the
loner.

Worked example on `arr = [1, 1, 2, 3, 3, 4, 4, 8, 8]`:

- `lo = 0, hi = 8`. `mid = 4`, `mid ^ 1 = 5`. `arr[4] = 3,
  arr[5] = 4`. `3 != 4`, pair broken. Loner at or before mid.
  `hi = 4`.
- `lo = 0, hi = 4`. `mid = 2`, `mid ^ 1 = 3`. `arr[2] = 2,
  arr[3] = 3`. Different. Pair broken. `hi = 2`.
- `lo = 0, hi = 2`. `mid = 1`, `mid ^ 1 = 0`. `arr[1] = 1,
  arr[0] = 1`. Equal! Pair unbroken. `lo = 2`.
- `lo = 2, hi = 2`. Loop exits.
- Return `arr[2] = 2`. Correct.

Three iterations on a nine-element array. Logarithmic.
''',
        "optimized": {
            "explanation": r'''
Half-open binary search with the parity-based decision rule
using XOR.
''',
            "code": r'''def single_non_duplicate(arr: list[int]) -> int:
    # Half-open binary search. The window [lo, hi] is inclusive
    # on both ends, but we use < as the loop condition to converge
    # when lo == hi.
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        # Midpoint of the current window. Integer division.
        mid = (lo + hi) // 2
        # The "partner" of mid in its pair. If mid is even, partner
        # is mid + 1. If mid is odd, partner is mid - 1. The XOR
        # with 1 flips the last bit, giving the partner cleanly.
        partner = mid ^ 1
        # Check whether the pair is intact.
        if arr[mid] == arr[partner]:
            # Pair is unbroken. We're still in the before-loner region.
            # The loner is strictly to the right of this pair.
            # If mid is even, the pair is (mid, mid+1); we can safely
            # jump to mid + 2. If mid is odd, partner = mid - 1 and
            # the pair is (mid - 1, mid); we can jump to mid + 1.
            # Both reduce to lo = mid + 1 (for odd mid) or lo = mid + 2
            # (for even mid). The simplest unified update is lo = mid + 1.
            lo = mid + 1
        else:
            # Pair is broken. The loner is at or before mid.
            # If mid is even and arr[mid] != arr[mid + 1], the loner
            # could be at mid itself.
            # If mid is odd and arr[mid] != arr[mid - 1], the loner
            # could be at mid - 1.
            # The safe update is hi = mid (keeping mid as a candidate).
            hi = mid
    # Loop exits with lo == hi. That index holds the loner.
    return arr[lo]
''',
            "complexity": "**Time**: *O(log n)*. **Space**: *O(1)*.",
        },
        "deep_concept": r'''
This problem teaches a beautiful generalization of binary search:
**the decision rule does not have to be a value comparison**.
Any monotonic property over the index space lets us halve the
search.

Here, the property is "is `mid` in the before-loner half?",
detected by the parity of the pair partner. The property is
monotonic: if `mid` is before the loner, every smaller index is
also before; if `mid` is at or after the loner, every larger
index is also at or after.

This kind of "predicate binary search" is the foundation of
**binary search on the answer** (covered in Step 4 Lecture 2).
The same skeleton — half-open window, monotonic predicate,
asymmetric bound updates — applies whether the predicate is
"value < x," "pair is unbroken," "Koko can finish at this
speed," or "this many books per painter." Recognize the shape
and the algorithm writes itself.

The `mid ^ 1` trick is also delightful in its own right. XOR
with 1 toggles parity in one operation. This shows up
constantly in algorithms involving index pairs.
''',
        "confusion_notes": [
            {
                "question": "What does `mid ^ 1` actually compute?",
                "answer": r'''
`mid ^ 1` (XOR with 1) flips the last bit of `mid`.

If `mid` is even, its last bit is 0. XOR with 1 makes it 1, so
`mid ^ 1 = mid + 1`.

If `mid` is odd, its last bit is 1. XOR with 1 makes it 0, so
`mid ^ 1 = mid - 1`.

So `mid ^ 1` is the **other** index in the pair containing
`mid`. The pairs are `(0, 1), (2, 3), (4, 5), ...`, so the
partner of any index is found by flipping the last bit.

The equivalent without XOR: `mid - 1 if mid % 2 else mid + 1`.
More verbose; XOR is the clean version.

This kind of bit trick is one of the prettiest small details in
binary search. Memorize it.
''',
            },
            {
                "question": "Why `hi = mid` instead of `hi = mid - 1` on the broken-pair branch?",
                "answer": r'''
Because `mid` itself could be the loner.

If `mid` is even and the pair is broken (`arr[mid] != arr[mid +
1]`), then either `arr[mid]` is the loner (and `arr[mid + 1]`
is the first of a new pair) OR `arr[mid]` is the second of the
previous pair shifted by one (meaning the loner is before mid).
Both cases say the loner is at or before mid.

If `mid` is odd and the pair is broken (`arr[mid] != arr[mid -
1]`), similar reasoning.

In both cases, `mid` is a candidate. Setting `hi = mid - 1`
would exclude it.

This is the asymmetric "candidate" branch we see in lower-
bound style. Setting `hi = mid` keeps `mid` in the window;
the binary search will eventually converge to it (or to an
earlier candidate).
''',
            },
            {
                "question": "What if the array has only one element?",
                "answer": r'''
The loop doesn't execute (`lo == hi == 0`), and we return
`arr[0]`. The single element is the loner by definition.

What about two elements? The problem statement says every
element appears twice except one, so a valid two-element input
would have one repeated and one unique. But that violates the
"every other element appears twice" constraint. The valid
inputs all have odd length.

For testing, you can use the algorithm on any odd-length input
where elements are sorted and exactly one element appears once.
The algorithm makes no assumption that all other elements
must be in pairs — it just uses the parity-of-pairs signal to
locate the loner.
''',
            },
        ],
        "summary": r'''
**Pattern**: half-open binary search using parity as the
decision signal. `mid ^ 1` is the pair partner.

**Lesson**: binary search works on any monotonic predicate
over the index space, not just value comparisons. The parity-
of-pairs predicate is monotonic and shifts at the loner.

**Recognize next time**: any "find the odd one in a sorted
array with a regular pattern" problem. The parity / pair-pattern
trick generalizes.
''',
    },
    # =================================================================
    # Lecture 2 — Binary search on the answer
    # =================================================================
    {
        "id": "aggressive-cows",
        "title": "Aggressive Cows (Maximize Minimum Distance)",
        "step_id": 4,
        "lecture_id": 2,
        "difficulty": "hard",
        "tags": ["binary-search", "bs-on-answer", "greedy"],
        "what_this_teaches": (
            "The maximize-the-minimum pattern. Binary search the "
            "answer (the minimum spacing); the feasibility checker "
            "uses a greedy placement; binary search picks the largest "
            "feasible spacing."
        ),
        "pattern": (
            "Sort stalls; binary search the minimum spacing in "
            "[1, max - min]; greedy check that K cows fit with at "
            "least that spacing."
        ),
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["koko-bananas", "binary-search"],
        "next_problems": ["book-allocation", "split-array-largest-sum", "painters-partition"],
        "resources": [
            _SHEET,
            {
                "label": "SPOJ — Aggressive Cows",
                "url": "https://www.spoj.com/problems/AGGRCOW/",
            },
        ],
        "understanding": r'''
You are given the positions of `n` stalls on a number line and
a number `k` of aggressive cows. You want to place each cow in
a distinct stall such that the **minimum distance between any
two cows is as large as possible**. Return that maximum
possible minimum distance.

This is one of the cleanest "binary search on the answer"
problems. Read it carefully — the phrasing "the minimum distance
between any two cows is as large as possible" is what makes it
a min-max optimization.

Example: stalls = `[1, 2, 4, 8, 9]`, `k = 3`. We need to place
3 cows in 3 of these 5 stalls. Possible placements include:

- `(1, 2, 4)`: pairwise distances are 1, 2, 3. Minimum is 1.
- `(1, 4, 8)`: distances 3, 4, 7. Minimum is 3.
- `(1, 4, 9)`: distances 3, 5, 8. Minimum is 3.
- `(1, 8, 9)`: distances 1, 7, 8. Minimum is 1.

Among all valid placements, the **maximum** of these
**minimums** is 3, achieved by placing cows at positions 1, 4,
8 or 1, 4, 9.

So the answer is 3. The question is how to compute this
efficiently. There are `C(n, k)` possible placements — far too
many to enumerate.

The trick is to **binary search on the answer**. The candidate
answer is the minimum distance, ranging from 1 (any two cows
are at least 1 apart) up to `max_stall - min_stall` (the
maximum possible spread). For each candidate distance `d`, we
ask the feasibility question:

> *"Can we place at least `k` cows with every pairwise distance
> at least `d`?"*

That feasibility question has a greedy answer: walk the sorted
stalls left to right, place a cow at the leftmost stall (or any
fixed first choice), then place each subsequent cow at the
first stall that is at least `d` away from the previously
placed cow. Count how many we successfully placed. If at least
`k`, feasibility is true.

The greedy "place at the leftmost available, then the first
stall d away, etc." works because of an **exchange argument**:
any placement using more than the greedy minimum could be
shifted left without violating constraints, and the greedy
chooses the smallest valid set of stalls for a given count.

Once you have the feasibility checker, binary search becomes
mechanical:

- `lo = 1, hi = max(stalls) - min(stalls)`.
- At each `mid`, check feasibility. If feasible, try a larger
  d (`lo = mid + 1`); record `mid` as the best so far. If not,
  try smaller (`hi = mid - 1`).

The largest `d` for which feasibility holds is the answer.
''',
        "brute_force": {
            "explanation": r'''
The naive approach: enumerate every possible placement and
compute its minimum pairwise distance, tracking the maximum.

There are `C(n, k)` placements. For `n = 10^5, k = 50`, that's
astronomically many. Infeasible.

A slightly less naive approach: try every possible minimum
distance `d` from 1 up to `max - min`, and for each, check
feasibility. That's `O((max - min) × n)` time. For small max-
min, possibly OK; for large ranges, slow.

The optimal is binary search on `d`, giving `O(n log (max -
min))`. Far better.

We won't even write the *O(C(n,k))* brute force because it's
totally impractical. The "try every d" linear search is
mentioned only as a stepping stone.
''',
            "code": r'''def aggressive_cows_linear(stalls: list[int], k: int) -> int:
    # Sort the stalls so that we can place greedily left-to-right.
    stalls = sorted(stalls)
    # Try every candidate minimum distance from 1 up to the range.
    best = 0
    for d in range(1, stalls[-1] - stalls[0] + 1):
        if can_place(stalls, k, d):
            best = d
        else:
            # If d failed, every larger d also fails (monotonic),
            # so we could break here. But linear search ignores this.
            pass
    return best


def can_place(stalls, k, d):
    # Greedy: place the first cow at the leftmost stall.
    count = 1
    last = stalls[0]
    for s in stalls[1:]:
        if s - last >= d:
            count += 1
            last = s
            if count >= k:
                return True
    return count >= k
''',
            "complexity": (
                "**Time**: *O((max - min) × n)*. For wide stall "
                "ranges, this is too slow.\n\n"
                "**Space**: *O(1)*."
            ),
        },
        "thought_process": r'''
The optimization is binary search on `d`. Let's set up the
recipe.

**Step 1: Identify the candidate range.** The minimum distance
must be at least 1 (cows must be in distinct stalls) and at
most `max(stalls) - min(stalls)` (the maximum possible
spread). So `d` ranges over `[1, max - min]`.

**Step 2: Write the feasibility checker.** Given a candidate
`d`, can we place at least `k` cows with every pairwise distance
≥ `d`?

Greedy: sort the stalls. Place the first cow at `stalls[0]`.
For each subsequent stall, if its distance from the last
placed cow is at least `d`, place a cow there. Count placements.
Feasibility holds if count ≥ k.

**Step 3: Verify monotonicity.** If `d = D` is feasible, then
every `d < D` is also feasible (with the same or more placements
possible). And if `d = D` is infeasible, every `d > D` is also
infeasible. This is the monotonic boundary.

**Step 4: Binary search.** Use the half-open style. The answer
is the **largest** `d` for which feasibility holds. So we're
looking for the last feasible candidate.

```python
lo, hi = 1, max(stalls) - min(stalls)
while lo <= hi:
    mid = (lo + hi) // 2
    if can_place(stalls, k, mid):
        # mid is feasible; try larger.
        lo = mid + 1
    else:
        # mid is infeasible; try smaller.
        hi = mid - 1
# After the loop, hi is the largest feasible d.
return hi
```

The "record the best feasible" version is also valid:

```python
best = 0
while lo <= hi:
    mid = (lo + hi) // 2
    if can_place(stalls, k, mid):
        best = mid
        lo = mid + 1
    else:
        hi = mid - 1
return best
```

Both compute the same answer.

Worked example on stalls = `[1, 2, 4, 8, 9]`, `k = 3`:

- Sort: already sorted.
- `lo = 1, hi = 8`. `mid = 4`. `can_place(d = 4)`? Place cow at
  1. Next stall: 2, distance 1, not ≥ 4 — skip. Next: 4,
  distance 3 — skip. Next: 8, distance 7 — place. Cows so far:
  2. Next: 9, distance 1 — skip. Total: 2 < k. Infeasible.
  `hi = 3`.
- `lo = 1, hi = 3`. `mid = 2`. `can_place(d = 2)`? Place at 1.
  Next: 2, distance 1 — skip. Next: 4, distance 3 — place.
  Next: 8, distance 4 — place. Total: 3 ≥ k. Feasible.
  `lo = 3`.
- `lo = 3, hi = 3`. `mid = 3`. `can_place(d = 3)`? Place at 1.
  Next: 2 — skip. Next: 4, distance 3 — place. Next: 8,
  distance 4 — place. Total: 3 ≥ k. Feasible. `lo = 4`.
- `lo = 4, hi = 3`. Loop exits.
- Return `hi = 3`. Correct.

The answer is 3, matching our hand analysis above. Three to
four iterations on a five-element array; logarithmic in the
range.
''',
        "optimized": {
            "explanation": r'''
Binary search on the minimum-distance answer with a greedy
feasibility checker.
''',
            "code": r'''def aggressive_cows(stalls: list[int], k: int) -> int:
    # Sort the stalls. Without sorting, the greedy placement does not
    # work — we need to walk in increasing position order.
    stalls = sorted(stalls)
    n = len(stalls)

    def can_place(d: int) -> bool:
        # Can we place at least k cows with all pairwise distances >= d?
        # Greedy: place the first cow at the leftmost stall.
        count = 1                       # we always start with one cow
        last = stalls[0]                # position of the most recently placed cow
        # Try each subsequent stall in order.
        for s in stalls[1:]:
            # If this stall is at least d away from the last placed cow,
            # we can place another cow here.
            if s - last >= d:
                count += 1
                last = s
                # Early exit: once we hit k, the placement is feasible.
                # Further iterations can only add more cows; no need to count them.
                if count >= k:
                    return True
        # We finished the stalls; check whether we placed enough.
        return count >= k

    # Binary search the candidate minimum distance d.
    # The smallest meaningful d is 1 (cows in distinct stalls).
    # The largest possible d is max - min (the full range of the stalls).
    lo, hi = 1, stalls[-1] - stalls[0]
    # Track the largest feasible d we have found so far.
    best = 0
    # Closed-interval binary search. The condition lo <= hi means the
    # window has at least one candidate.
    while lo <= hi:
        # Midpoint of the candidate range.
        mid = (lo + hi) // 2
        # Test feasibility at d = mid.
        if can_place(mid):
            # mid is feasible. Update best and try a larger d.
            best = mid
            lo = mid + 1
        else:
            # mid is infeasible. Every d >= mid is also infeasible
            # (monotonicity). Try smaller.
            hi = mid - 1
    return best
''',
            "complexity": (
                "**Time**: *O(n log(max - min))*. The binary search "
                "has *O(log(max - min))* iterations, each doing an "
                "*O(n)* feasibility check. Sorting is *O(n log n)*, "
                "absorbed into the total.\n\n"
                "**Space**: *O(1)* beyond the sort."
            ),
        },
        "deep_concept": r'''
This problem is the canonical example of **binary search on
the answer** with a greedy feasibility checker.

The shape generalizes to a whole family:

- **Aggressive cows**: maximize the minimum pairwise distance.
- **Painter's partition**: minimize the maximum painter's
  workload.
- **Split array largest sum**: minimize the maximum subarray
  sum across `k` partitions.
- **Book allocation**: minimize the maximum books per student.
- **Minimum days to make M bouquets**: minimize the day count
  while ensuring enough bouquets can be made.
- **Capacity to ship packages in D days**: minimize the
  capacity needed to ship within D days.

All of them are "binary search on the answer" with a feasibility
test. The recipe:

1. Identify the candidate range for the answer.
2. Write a polynomial-time feasibility checker.
3. Verify the monotonic boundary (if feasible at X, feasible
   at all Y on the correct side of X).
4. Binary search.

Once you can mechanically apply this recipe, an entire lecture
of "hard" problems collapses into mechanical work. The hard part
is recognizing that the problem fits the pattern. The
implementation is rote.

The recognition signal: **the problem asks for the maximum or
minimum of some integer quantity, and a feasibility test for
"can we achieve this value?" runs in polynomial time**.

When you see that combination, binary search on the answer is
the move.

The greedy feasibility checker also deserves a moment. Why does
"place cows leftmost-first" work? Because of an **exchange
argument**: any valid placement can be transformed into the
greedy placement by shifting cows leftward (which preserves the
minimum distance), without changing the count. So the greedy
gives the maximum possible count of cows that can be placed
with spacing ≥ d. If even the greedy can't reach k cows, no
placement can. This is the kind of argument that justifies
greedy choices throughout the binary-search-on-answer family.
''',
        "confusion_notes": [
            {
                "question": "Why does the greedy 'place leftmost first' approach work?",
                "answer": r'''
Because of an **exchange argument**. Suppose there exists a
valid placement of `k` cows with minimum spacing ≥ `d`. Consider
the leftmost cow in this placement. We can move it to `stalls[
0]` (the leftmost stall) without decreasing any pairwise
distance — its new neighbors are at least as far away as its
old neighbors. So there's a valid placement with the first cow
at `stalls[0]`.

By induction, we can keep shifting cows leftward to the
"greedy" positions: cow `i` is at the smallest stall at least
`d` away from cow `i - 1`'s position. The result has the same
count as the original placement and is the unique greedy
placement.

So the greedy placement uses the **same** number of cows as
any optimal placement. If the greedy places fewer than `k`,
no placement can place `k`.

This is the formal correctness argument. In practice, you don't
have to prove it in interviews — just state "the leftmost-first
greedy is optimal for this kind of placement problem."

The same exchange argument justifies the greedy in painter's
partition, book allocation, and many other "binary search on
the answer" problems.
''',
            },
            {
                "question": "Why is the candidate range `[1, max - min]`?",
                "answer": r'''
- **Lower bound 1**: cows must be at distinct stalls, so any two
  cows are at least 1 apart. The minimum meaningful spacing is
  1. (For 0 we could place cows at the same stall — but the
  problem disallows that.)

- **Upper bound max - min**: the maximum possible pairwise
  distance is between the leftmost and rightmost stalls. If we
  place just two cows there, the spacing is `max - min`. With
  more cows, the minimum spacing can only decrease. So the
  maximum spacing for k cows is at most `max - min`.

A tighter upper bound: the maximum possible "minimum spacing"
for k cows fitting in a range of `max - min` is `(max - min) /
(k - 1)`. For 3 cows in a range of 8 (stalls 1 to 9), that's
`8 / 2 = 4`. Our example confirmed the answer is 3, which is
≤ 4. So `(max - min) / (k - 1)` is a tighter upper bound than
`max - min`.

Either bound works for correctness; the tighter one just reduces
the binary-search iteration count by a small constant factor.
''',
            },
            {
                "question": "What's the difference between this and binary search on a sorted array?",
                "answer": r'''
The structure is identical, but the search space is different.

- **Binary search on a sorted array**: search over the array
  indices for a target value.
- **Binary search on the answer**: search over the space of
  possible answer values, using a feasibility checker as the
  comparison.

In both cases, we have a monotonic property over a 1D space.
The difference is what the 1D space represents.

For array binary search, the property is "is arr[mid] ≥ target?"
and the 1D space is the array index set.

For binary search on the answer, the property is "is mid a
feasible answer?" and the 1D space is the set of candidate
answer values.

Same algorithm, different interpretation. Once you see the
generalization, "binary search" stops being just a sorted-array
algorithm and becomes a general optimization technique.
''',
            },
            {
                "question": "What if k = 1? Or k = n? Edge cases?",
                "answer": r'''
**k = 1**: only one cow. There's no "pairwise distance" to
optimize. The answer is conventionally 0 (or infinity, depending
on convention — but 0 is more common). Our algorithm with
`lo = 1, hi = max - min` and `best = 0` would return `best`,
which starts at 0 and never updates. Actually it might return
the upper bound — let me think.

For k = 1, every d in [1, max - min] is feasible (we can always
place 1 cow). So the binary search would push `lo` all the way
up to `max - min + 1`, and `best` would be updated to `max - min`.

For most problem statements, this is a meaningless edge case
that the constraints usually exclude (k >= 2).

**k = n**: place a cow at every stall. The minimum distance is
`min(stalls[i+1] - stalls[i] for i in range(n-1))`. Our binary
search would still work but is overkill; you could compute
directly with a single pass.

**k > n**: more cows than stalls. Impossible. The algorithm
would return 0 (or whatever `best` was initialized to) — the
feasibility checker would never return True.

For all edge cases, the algorithm gives sensible results, but
some are degenerate. In an interview, mention them out loud
when you state the algorithm.
''',
            },
        ],
        "summary": r'''
**Pattern**: binary search on the minimum-distance answer +
greedy feasibility checker.

**Lesson**: when a problem asks for the maximum or minimum of
some integer quantity and the feasibility test is monotonic
and polynomial, binary search the answer. This recipe applies
to an entire family of "min/max" optimization problems.

**Recognize next time**: any problem with the words "maximize
the minimum" or "minimize the maximum" — they are almost always
binary-search-on-answer problems.
''',
    },
    {
        "id": "book-allocation",
        "title": "Allocate Books to Students (Minimize Max Books)",
        "step_id": 4,
        "lecture_id": 2,
        "difficulty": "hard",
        "tags": ["binary-search", "bs-on-answer", "partition"],
        "what_this_teaches": (
            "The dual of aggressive cows. Where aggressive cows "
            "maximized the minimum, this minimizes the maximum. Same "
            "binary-search-on-answer recipe, with the feasibility "
            "direction flipped."
        ),
        "pattern": (
            "Binary search the maximum books per student in "
            "[max(books), sum(books)]; greedy partition checker."
        ),
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["aggressive-cows", "koko-bananas"],
        "next_problems": ["split-array-largest-sum", "painters-partition"],
        "resources": [
            _SHEET,
            {
                "label": "GFG — Allocate Minimum Number of Pages",
                "url": "https://www.geeksforgeeks.org/allocate-minimum-number-pages/",
            },
        ],
        "understanding": r'''
You have `n` books with given page counts, and `m` students.
You want to distribute the books to the students such that:

1. Each student gets at least one book.
2. Books are distributed in **contiguous chunks** (you cannot
   skip a book and give a later one to the same student).
3. Each book goes to exactly one student.
4. The **maximum number of pages any one student receives is
   minimized**.

Return the minimized maximum.

Examples:

- books = `[12, 34, 67, 90]`, m = 2 students. The four valid
  contiguous partitions:
  - `[12]` and `[34, 67, 90]`: max = 191.
  - `[12, 34]` and `[67, 90]`: max = 157.
  - `[12, 34, 67]` and `[90]`: max = 113.

  Minimum of these maxes is 113.

- books = `[10, 20, 30]`, m = 4 students: impossible (4 > 3
  books). Return -1.

This is **the dual of aggressive cows**. Where aggressive cows
maximized the minimum (give cows as much distance as possible),
book allocation minimizes the maximum (give students as
balanced a load as possible).

The same "binary search on the answer" recipe applies, with
the direction flipped.

**Candidate range** for the answer (the maximum pages any
student gets):

- Lower bound: `max(books)`. No student can receive less than
  the heaviest single book (because books can't be split).
- Upper bound: `sum(books)`. In the worst case (m = 1 student),
  one student takes everything.

**Feasibility checker**: given a candidate maximum `M`, can we
distribute the books to ≤ `m` students such that no student
exceeds `M` pages? Greedy: assign books to students one by one,
moving to the next student whenever adding the current book
would exceed `M`. Count students used. Feasible if count ≤ m.

**Monotonicity**: if a candidate `M` is feasible, every larger
`M` is also feasible. We want the **smallest** feasible `M`.

**Binary search**: half-open lower-bound style — find the first
M for which feasibility holds.
''',
        "brute_force": {
            "explanation": r'''
The naive brute force enumerates every possible partition of
the books into `m` contiguous groups and computes each
partition's maximum group sum. There are `C(n - 1, m - 1)`
partitions — combinatorially large.

A slightly better brute force: try every candidate max-pages
value from `max(books)` to `sum(books)` linearly. For each,
check feasibility. `O((sum - max) × n)` time. Still slow for
large books.

The optimal binary-search-on-answer brings this down to `O(n
log(sum - max))`.
''',
            "code": r'''# Linear scan over candidate maxes — works but slow for large ranges.
def book_allocation_linear(books: list[int], m: int) -> int:
    if m > len(books):
        return -1
    for max_pages in range(max(books), sum(books) + 1):
        if can_allocate(books, m, max_pages):
            return max_pages
    return -1


def can_allocate(books, m, max_pages):
    students = 1
    current = 0
    for b in books:
        if current + b <= max_pages:
            current += b
        else:
            students += 1
            current = b
            if students > m:
                return False
    return True
''',
            "complexity": (
                "**Time**: *O((sum - max) × n)* for the linear search "
                "over candidate maxes. Too slow when book sums are "
                "large.\n\n"
                "**Space**: *O(1)*."
            ),
        },
        "thought_process": r'''
The optimization: binary search the candidate answer `M`.

**Why is the feasibility checker greedy?** Given a candidate
`M`, we want to know if we can distribute books to ≤ `m`
students with no student exceeding `M`. The greedy algorithm:
walk through books left to right; keep adding to the current
student until the next book would push them past `M`; start a
new student. Count how many students we used.

This greedy is optimal because **any partition with fewer
students can be transformed into this one by merging adjacent
groups**. The greedy uses the minimum possible students for a
given `M`. So if even the greedy needs more than `m`, no
partition can fit in `m`. Conversely, if the greedy fits in
`m`, the partition is feasible.

**Monotonicity**: larger `M` lets each student carry more, so
fewer students are needed. So feasibility is monotonic in `M`:
if `M = X` works, every `M > X` works too. We want the
**smallest** feasible `M`.

**Binary search**: lower-bound style. Find the first `M` for
which feasibility holds.

```python
lo, hi = max(books), sum(books)
while lo < hi:
    mid = (lo + hi) // 2
    if can_allocate(books, m, mid):
        hi = mid          # mid is feasible; try smaller
    else:
        lo = mid + 1      # mid is infeasible; try larger
return lo
```

When the loop exits, `lo == hi` is the smallest feasible `M`.

Worked example on books = `[12, 34, 67, 90]`, m = 2:

- `lo = max = 90, hi = sum = 203`.
- `mid = 146`. Greedy: student 1 takes 12 + 34 + 67 = 113;
  adding 90 would exceed 146, so start student 2; student 2
  takes 90. Total students: 2 ≤ m. Feasible. `hi = 146`.
- `lo = 90, hi = 146`. `mid = 118`. Greedy: student 1 takes 12
  + 34 + 67 = 113; adding 90 would exceed 118, so start student
  2 with 90. Total: 2 ≤ m. Feasible. `hi = 118`.
- `lo = 90, hi = 118`. `mid = 104`. Greedy: student 1 takes 12
  + 34 = 46; adding 67 would exceed 104, so start student 2.
  Student 2 takes 67; adding 90 would exceed, so start student
  3. Student 3 takes 90. Total: 3 > m. Infeasible. `lo = 105`.
- `lo = 105, hi = 118`. `mid = 111`. Greedy: student 1 takes 12
  + 34 = 46; adding 67 = 113 > 111. Start student 2 = 67.
  Adding 90 > 111, start student 3. 3 > m. Infeasible. `lo = 112`.
- `lo = 112, hi = 118`. `mid = 115`. Greedy: student 1 takes
  12 + 34 = 46; + 67 = 113. Adding 90 > 115, start student 2 =
  90. Total: 2. Feasible. `hi = 115`.
- `lo = 112, hi = 115`. `mid = 113`. Greedy: student 1: 12 + 34
  + 67 = 113. Adding 90 > 113, start student 2 = 90. Total: 2.
  Feasible. `hi = 113`.
- `lo = 112, hi = 113`. `mid = 112`. Greedy: student 1: 12 + 34
  = 46; +67 = 113 > 112. Start student 2 = 67; +90 > 112, start
  student 3. Total: 3 > m. Infeasible. `lo = 113`.
- `lo = 113, hi = 113`. Exit. Return 113.

The answer matches our hand analysis. About 7 binary-search
iterations on a small example; `log2(113)` ≈ 7.
''',
        "optimized": {
            "explanation": r'''
Binary search the candidate maximum-pages answer; greedy
feasibility checker.
''',
            "code": r'''def book_allocation(books: list[int], m: int) -> int:
    # Edge case: fewer books than students. Impossible to give
    # every student at least one book.
    if m > len(books):
        return -1

    def can_allocate(max_pages: int) -> bool:
        # Greedy: assign books to students in order. Each student
        # accumulates books until adding the next one would exceed
        # max_pages; then start a new student.
        students = 1          # we always need at least one student
        current = 0           # pages assigned to the current student
        for b in books:
            # If a single book exceeds max_pages, allocation is
            # impossible at this candidate. (The binary search's
            # lower bound max(books) prevents this from happening
            # for valid inputs, but we guard anyway.)
            if b > max_pages:
                return False
            # If adding this book keeps the current student under
            # the cap, add it.
            if current + b <= max_pages:
                current += b
            else:
                # Otherwise, move to a new student starting with this book.
                students += 1
                current = b
                # Early exit: if we already need more than m students,
                # this candidate is infeasible.
                if students > m:
                    return False
        return students <= m

    # The candidate range for the answer.
    # Lower bound: max(books). No student can carry less than the
    # heaviest single book (books can't be split).
    # Upper bound: sum(books). With m = 1, the only student gets
    # everything.
    lo, hi = max(books), sum(books)
    # Half-open lower-bound binary search. We want the smallest
    # feasible candidate.
    while lo < hi:
        mid = (lo + hi) // 2
        if can_allocate(mid):
            # mid is feasible. Keep it in the window; try smaller.
            hi = mid
        else:
            # mid is infeasible. Try larger.
            lo = mid + 1
    return lo
''',
            "complexity": (
                "**Time**: *O(n × log(sum - max))*. The binary search "
                "has *O(log(range))* iterations, each doing an *O(n)* "
                "feasibility check.\n\n"
                "**Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
This problem cements the **min-max dual** of aggressive cows.
Both problems use binary search on the answer with a greedy
feasibility checker; they differ only in the direction of the
search.

- **Aggressive cows**: maximize the minimum. Search for the
  largest feasible distance.
- **Book allocation**: minimize the maximum. Search for the
  smallest feasible page cap.

A whole family of problems sits on this dual:

- **Split array largest sum** (LC 410): minimize the maximum
  subarray sum across `k` partitions.
- **Painter's partition**: minimize the time for `k` painters
  to finish.
- **Capacity to ship packages in D days**: minimize the
  capacity needed.
- **Find smallest divisor given a threshold**: minimize the
  divisor that keeps quotient sums under a threshold.

All of them fit the same template. The feasibility checker is
typically a greedy walk; the binary search picks the
optimal feasible value.

Once you recognize this pattern, an entire lecture of "hard"
problems becomes mechanical. The hard part is recognizing the
fit, not implementing the algorithm. So when you see "minimize
maximum" or "maximize minimum" in a problem statement, stop
and ask: "is this binary search on the answer?". If yes, the
recipe writes itself.
''',
        "confusion_notes": [
            {
                "question": "Why is the greedy feasibility checker optimal?",
                "answer": r'''
Because of an exchange argument. Suppose there's a valid
partition with ≤ m students and max pages ≤ `M`. We can
transform it into the greedy partition by **merging adjacent
non-greedy groups**:

If the greedy would put book `i` with the previous student but
the actual partition starts a new student at `i`, we can merge
the new student into the previous one. The merged group has
sum ≤ `M` (because the greedy was about to add it without
exceeding M).

By repeating this merge, we reach the greedy partition. Each
merge keeps the max page count ≤ `M` and decreases (or keeps
the same) the student count. So the greedy partition uses **at
most as many students** as any valid partition.

Therefore: if the greedy needs more than `m` students, no
partition can fit in `m`. The greedy is the tightest possible
test for feasibility.

This is the formal correctness. In practice you state "greedy
left-to-right is optimal here" and move on. But knowing the
underlying argument helps when adapting the algorithm to
variants.
''',
            },
            {
                "question": "Why `max(books)` as the lower bound?",
                "answer": r'''
Because no student can carry less than the heaviest single book.
Books can't be split. So any partition has at least one
student carrying at least `max(books)` pages.

If we tried `M = max(books) - 1` as the candidate, the
feasibility checker would fail immediately when it encountered
the largest book. So `max(books)` is the tightest possible
lower bound.

Some implementations use 1 or 0 as the lower bound — that's
still correct (the binary search will just take a few extra
iterations to converge to `max(books)`), but `max(books)` is
the tight choice.

Similarly, `sum(books)` is the tight upper bound: with one
student, the answer is the sum. With more students, the answer
can only decrease.

Setting tight bounds is a small optimization. The binary search
asymptotics are the same with loose bounds; the constant just
goes up.
''',
            },
            {
                "question": "What if a book has zero pages?",
                "answer": r'''
The algorithm handles it correctly — the greedy adds the
zero-page book to the current student without changing their
total, and we move on.

Zero-page books are a weird edge case usually not present in
practice, but if your input might include them, the algorithm
is robust.

What if a book has *negative* pages? That's mathematically
ill-defined for this problem and the problem statement should
exclude it. The algorithm would still run but produce
nonsensical results.
''',
            },
            {
                "question": "How does this differ from 'split array largest sum' (LC 410)?",
                "answer": r'''
They are the same problem! "Split Array Largest Sum" is
algorithmically identical to "Book Allocation" — both partition
an array into `k` contiguous groups and minimize the maximum
group sum.

The implementations are identical. Only the problem framing
differs ("students and books" vs "subarrays and sum").

Other equivalent framings:

- **Painter's partition**: minimize time for `k` painters to
  paint boards in order.
- **Capacity to ship packages in D days**: minimize ship
  capacity to deliver in D days. ("Days" plays the role of
  "students" / "subarrays".)

All four are the same algorithm with different surface stories.
Once you've solved one, you've effectively solved all four.

This is part of why DSA preparation is more efficient than it
looks — many "different" problems are really the same problem
in disguise.
''',
            },
        ],
        "summary": r'''
**Pattern**: binary search the minimum max-load + greedy
partition checker.

**Lesson**: minimize-the-maximum is the dual of maximize-the-
minimum. Same binary-search-on-answer recipe, opposite search
direction.

**Recognize next time**: "minimize the maximum X" or "minimize
the worst case Y" problems. All canonical BS-on-answer.

**Closely related**: split array largest sum (LC 410),
painter's partition, capacity to ship packages in D days. All
the same algorithm.
''',
    },
    {
        "id": "median-two-sorted",
        "title": "Median of Two Sorted Arrays",
        "step_id": 4,
        "lecture_id": 2,
        "difficulty": "hard",
        "tags": ["binary-search", "partition", "hard"],
        "what_this_teaches": (
            "Binary search the partition point — not the array values, "
            "and not the candidate answer, but the *cut* through the "
            "two arrays that gives equal-sized halves with the "
            "median-defining property. One of the hardest binary "
            "search variants in the curriculum."
        ),
        "pattern": (
            "Binary search the partition of the smaller array; derive "
            "the partition of the larger; check the four-element "
            "cross-condition."
        ),
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["binary-search", "lower-bound", "koko-bananas"],
        "next_problems": ["kth-element-two-sorted"],
        "resources": [
            _SHEET,
            _lc(4, "median-of-two-sorted-arrays"),
        ],
        "understanding": r'''
You are given two sorted arrays `nums1` and `nums2` of sizes
`m` and `n`. Find the median of the **combined** sorted array
in *O(log(min(m, n)))* time.

This is the LeetCode 4 problem — widely regarded as the hardest
binary-search problem on the platform. The recursive partition
algorithm is beautiful but unforgiving; any boundary mistake
gives the wrong answer.

Examples:

- `nums1 = [1, 3], nums2 = [2]`: combined sorted = `[1, 2, 3]`,
  median = 2.
- `nums1 = [1, 2], nums2 = [3, 4]`: combined = `[1, 2, 3, 4]`,
  median = (2 + 3) / 2 = 2.5.
- `nums1 = [0, 0], nums2 = [0, 0]`: combined = `[0, 0, 0, 0]`,
  median = 0.

The brute force is *O(m + n)* — merge the two arrays (or just
the lower half) and read off the median. Easy to write,
correct, and beats most production needs. But the
*O(log(min(m, n)))* algorithm is what the problem demands.

**Why binary search?** Because the median has a specific
structural property that lets us narrow down by halving. The
median of the combined array is the value such that exactly
half of all elements are at most it and half are at least it.
If we can find a "cut" through both arrays that puts the right
counts on each side, we have the median.

**The cut definition**: imagine inserting a vertical line at
position `i` in `nums1` (with `i` elements to the left and
`m - i` to the right) and at position `j` in `nums2` (`j` to
the left, `n - j` to the right). The total elements to the left
of the cut is `i + j`; to the right is `(m - i) + (n - j)`.

For the cut to define the median, we need:

1. **Equal-sized halves**: `i + j` should equal `(m + n + 1) //
   2`. (The "+1" handles odd total sizes — the left half gets
   the extra one when total is odd.)
2. **Crossing condition**: the largest left-element ≤ the
   smallest right-element. That is, `nums1[i-1] ≤ nums2[j]`
   AND `nums2[j-1] ≤ nums1[i]`.

If both conditions hold, the median is:

- If `m + n` is odd: `max(nums1[i-1], nums2[j-1])`.
- If even: average of `max(nums1[i-1], nums2[j-1])` and
  `min(nums1[i], nums2[j])`.

The algorithm binary searches over `i` in `nums1` (the smaller
array). Once `i` is fixed, `j` is determined by condition (1).
We check condition (2). If both crosses hold, we have the
answer. If `nums1[i-1] > nums2[j]`, we have too many small
elements on the left of nums1 — decrease `i`. If `nums2[j-1] >
nums1[i]`, we have too few — increase `i`.

This is the algorithm. It is *O(log(min(m, n)))* time.

The implementation has fiddly boundary cases (when `i = 0` or
`i = m`, some of the comparisons reference "out of bounds"
indices, which we handle with sentinel values `-∞` and `+∞`).
Get the boundaries right and the algorithm is one of the
prettiest in DSA. Get them wrong and it's debugging hell.
''',
        "brute_force": {
            "explanation": r'''
The easiest correct algorithm: merge the two arrays into one
sorted array, then read the median.

```python
def median_brute(nums1, nums2):
    merged = sorted(nums1 + nums2)
    n = len(merged)
    if n % 2 == 1:
        return merged[n // 2]
    return (merged[n // 2 - 1] + merged[n // 2]) / 2
```

`O((m + n) log(m + n))` due to the sort. Correct on any input.

A smarter brute force: two-pointer merge (since both inputs are
already sorted), stop at the median index. *O(m + n)* time,
*O(1)* extra space:

```python
def median_two_pointer(nums1, nums2):
    m, n = len(nums1), len(nums2)
    total = m + n
    i = j = 0
    prev = curr = 0
    for _ in range(total // 2 + 1):
        prev = curr
        if i < m and (j == n or nums1[i] <= nums2[j]):
            curr = nums1[i]
            i += 1
        else:
            curr = nums2[j]
            j += 1
    if total % 2 == 0:
        return (prev + curr) / 2
    return curr
```

This is the right answer for production code in most cases.
*O(m + n)* time is excellent. The LeetCode-required
*O(log(min(m, n)))* algorithm exists primarily as an
algorithmic exercise; the gain in practice is modest unless
`m + n` is enormous.
''',
            "code": r'''def median_two_pointer(nums1: list[int], nums2: list[int]) -> float:
    # Sizes of the two arrays and their total.
    m, n = len(nums1), len(nums2)
    total = m + n
    # Two pointers, one per array.
    i = j = 0
    # prev and curr track the last two values yielded by the merge.
    # We need them both because even-length merges average two
    # adjacent values.
    prev = curr = 0
    # Walk through the merged sequence up to position total // 2.
    # For odd total, the median is at this position. For even, the
    # median is the average of this and the previous position.
    for _ in range(total // 2 + 1):
        prev = curr
        # Pick the next smallest available element. If nums1 is
        # exhausted (i == m), take from nums2. Otherwise compare
        # nums1[i] with nums2[j] (or take from nums1 if nums2 is
        # exhausted).
        if i < m and (j == n or nums1[i] <= nums2[j]):
            curr = nums1[i]
            i += 1
        else:
            curr = nums2[j]
            j += 1
    # If total length is even, average the last two values.
    if total % 2 == 0:
        return (prev + curr) / 2
    # Odd: the median is the value we just stopped at.
    return curr
''',
            "complexity": (
                "**Time**: *O(m + n)*. We walk only the first half of "
                "the merged sequence.\n\n"
                "**Space**: *O(1)*. Just a handful of pointers."
            ),
        },
        "thought_process": r'''
The optimal *O(log(min(m, n)))* algorithm uses **binary search
on the partition point**. This is a different flavor of binary
search from anything we've seen — we are not searching for a
value, not searching for an index in a single array, and not
searching for the answer. We are searching for the *partition*
that splits both arrays into halves with a specific property.

Let `m = len(nums1), n = len(nums2)`. Assume WLOG `m <= n`
(swap if not — binary searching the smaller array gives the
better log factor).

We want to find positions `i ∈ [0, m]` and `j ∈ [0, n]` such
that:

1. **`i + j == (m + n + 1) // 2`** (the left half has exactly
   half the total, rounding up to handle odd totals).
2. **`nums1[i-1] <= nums2[j]`** AND **`nums2[j-1] <= nums1[i]`**
   (every element in the left half is at most every element in
   the right half).

If both hold, the median is computable from the four boundary
elements:

- For odd total: median = `max(nums1[i-1], nums2[j-1])`.
- For even total: median = average of `max(nums1[i-1], nums2[j-1])`
  and `min(nums1[i], nums2[j])`.

The binary search varies `i` over `[0, m]`. Once `i` is fixed,
`j = (m + n + 1) // 2 - i` is determined by condition (1). So
we have one variable and one constraint to verify (condition 2).

If condition 2 fails because `nums1[i-1] > nums2[j]`: there are
too many small elements in `nums1`'s left part. **Decrease i**.
Set `hi = i - 1`.

If condition 2 fails because `nums2[j-1] > nums1[i]`: there are
too few small elements in `nums1`'s left part. **Increase i**.
Set `lo = i + 1`.

The binary search converges to the unique `i` where both halves
of condition 2 hold.

**Boundary cases**: when `i = 0`, there's no `nums1[i-1]` to
read — we use `-∞` as a sentinel. When `i = m`, no `nums1[i]`;
use `+∞`. Same for `j = 0` and `j = n`. The sentinels make the
comparisons go through cleanly.

Worked example on `nums1 = [1, 3], nums2 = [2]`, m = 2, n = 1.
Wait — we need m <= n, so swap: `nums1 = [2], nums2 = [1, 3]`,
m = 1, n = 2. Total = 3. Left half size = `(3 + 1) // 2 = 2`.

- `lo = 0, hi = 1`. `i = 0`, `j = 2 - 0 = 2`.
  - `nums1[i-1] = nums1[-1] = -∞` (sentinel).
  - `nums1[i] = nums1[0] = 2`.
  - `nums2[j-1] = nums2[1] = 3`.
  - `nums2[j] = nums2[2] = +∞` (sentinel).
  - Check: `-∞ <= +∞`? Yes. `3 <= 2`? **No**. Condition fails
    because `nums2[j-1] = 3 > nums1[i] = 2`. Increase `i`. `lo
    = 1`.
- `lo = 1, hi = 1`. `i = 1`, `j = 2 - 1 = 1`.
  - `nums1[i-1] = 2`.
  - `nums1[i] = nums1[1] = +∞`.
  - `nums2[j-1] = nums2[0] = 1`.
  - `nums2[j] = nums2[1] = 3`.
  - Check: `2 <= 3`? Yes. `1 <= +∞`? Yes. Both pass.
- Total = 3 (odd). Median = `max(2, 1) = 2`. Correct.

Two iterations. Beautiful.

The hardest part of implementing this is the sentinel handling
and getting `i, j` initialization exactly right. Once those are
working, the algorithm is one of the slickest in DSA.
''',
        "optimized": {
            "explanation": r'''
Binary search the partition point on the smaller array. Sentinel
values handle the boundary cases.
''',
            "code": r'''def find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:
    # Ensure nums1 is the smaller array. Binary searching the
    # smaller one gives the better log factor (and simplifies the
    # boundary cases). Swap if needed.
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    m, n = len(nums1), len(nums2)
    # Total length of both arrays combined. We need to know the
    # size of the left half: half (rounded up) of the total.
    total = m + n
    # Size of the left half. The "+1" handles odd totals — the
    # left half gets the extra element.
    half = (total + 1) // 2
    # Binary search the partition position i in nums1.
    # i ranges over [0, m] (inclusive on both ends).
    lo, hi = 0, m
    while lo <= hi:
        # i is the count of elements taken from nums1 for the left
        # half. j is computed from the half-size constraint.
        i = (lo + hi) // 2
        j = half - i
        # The four boundary elements around the cut.
        # Sentinels: when i = 0 there's no nums1[i-1] — use -inf.
        # When i = m there's no nums1[i] — use +inf. Same for j.
        nums1_left = nums1[i - 1] if i > 0 else float('-inf')
        nums1_right = nums1[i] if i < m else float('inf')
        nums2_left = nums2[j - 1] if j > 0 else float('-inf')
        nums2_right = nums2[j] if j < n else float('inf')
        # Crossing condition: the largest left element from either
        # array must not exceed the smallest right element from the
        # other array.
        if nums1_left <= nums2_right and nums2_left <= nums1_right:
            # Found the correct partition.
            if total % 2 == 0:
                # Even total: median is the average of the largest left
                # and the smallest right.
                return (max(nums1_left, nums2_left) +
                        min(nums1_right, nums2_right)) / 2
            # Odd total: median is the largest element of the left half.
            return max(nums1_left, nums2_left)
        elif nums1_left > nums2_right:
            # Too many small elements in nums1's left. Decrease i.
            hi = i - 1
        else:
            # nums2_left > nums1_right: too few in nums1's left. Increase i.
            lo = i + 1
    # Should never reach here for valid input.
    raise ValueError("inputs not sorted")
''',
            "complexity": (
                "**Time**: *O(log(min(m, n)))*. The binary search "
                "halves the smaller array's possible partition "
                "points.\n\n"
                "**Space**: *O(1)*. Just a constant number of "
                "scalars."
            ),
        },
        "deep_concept": r'''
This problem teaches the deep idea that **binary search can
operate on any one-dimensional monotonic space, even when that
space is not the obvious index set or value set**.

Here, we binary search on the **partition point** `i` in nums1.
The decision predicate is "is the cross-condition satisfied?".
The space is `[0, m]`. Monotonicity: as `i` increases, we move
small-to-large elements across the cut from right to left;
the cross conditions shift in a predictable direction.

Once you internalize this, you start seeing binary-search
opportunities in problems that don't even mention "search."

The reason we binary-search the smaller array: it gives the
better log factor (`log(min(m, n))` instead of `log(max)`), and
the sentinels for `i = 0` / `i = m` are easier to reason about
when there are fewer boundary cases.

The reason for the `(total + 1) // 2` formula: it works for
both odd and even totals. For odd totals, the left half gets
one more element than the right (the median sits at the right
end of the left half). For even totals, the halves are equal
size. The `+1` rounding handles both cases in a single formula.

**Common interview pitfalls**:

1. Forgetting the sentinel values. Without them, `nums1[i - 1]`
   when `i = 0` raises `IndexError`.
2. Mixing up which array to binary search. Searching the larger
   one gives a worse log factor and more boundary cases.
3. Confusing the role of `i` and `j`. `j` is determined by `i`
   and the total; it is not a second binary-search variable.
4. Off-by-one in the `half` formula. Use `(total + 1) // 2`,
   not `total // 2` (the latter handles only even totals).

Once you've coded this once or twice, it becomes mechanical.
But the first time it bites everyone.
''',
        "confusion_notes": [
            {
                "question": "Why partition? Why not just find the k-th smallest?",
                "answer": r'''
You could! The median is just the k-th smallest where `k = (m +
n + 1) // 2` (for odd total) or "average of the (m+n)/2-th and
((m+n)/2 + 1)-th smallest" (for even total).

There is an *O(log(m + n))* algorithm for finding the k-th
smallest of two sorted arrays — it eliminates half of `k` each
iteration. Slightly different from the partition approach but
equivalent in complexity.

Both algorithms are *O(log)*. The partition approach is cleaner
once you understand the cross-condition; the k-th smallest is
arguably more intuitive but has its own boundary subtleties.

In an interview, mention both and implement whichever you find
clearer. The partition approach is more famous, so prefer it if
you've practiced it.

A related observation: the partition approach generalizes to
"k-th element of two sorted arrays" with minor changes — set
`half = k` instead of `(m + n + 1) // 2`. The same binary
search finds the partition; the k-th element is `max(nums1_left,
nums2_left)`.
''',
            },
            {
                "question": "Why the `(total + 1) // 2` formula instead of `total // 2`?",
                "answer": r'''
Because the partition needs to put the median (or the
"left half of the median pair," for even totals) into the left
side of the cut.

For **odd total** (e.g., 5 elements), the median is the 3rd
element. We want the left half to contain the first 3 elements
(including the median), and the right half to contain the last
2. `half = (5 + 1) // 2 = 3`. Correct.

For **even total** (e.g., 6 elements), the median is the
average of the 3rd and 4th. The cut should put the first 3 on
the left and the last 3 on the right. `half = (6 + 1) // 2 = 3`
(integer division of 7 by 2). Also correct.

With `total // 2`:

- Odd 5: `5 // 2 = 2`. Left half = first 2 elements, right =
  last 3. But the median is the 3rd, which is in the right
  half. The cross-condition formulas don't match this layout
  cleanly.
- Even 6: `6 // 2 = 3`. OK in this case.

So `(total + 1) // 2` is the unified formula that works for
both. It's a small but critical detail.
''',
            },
            {
                "question": "What if one of the arrays is empty?",
                "answer": r'''
The algorithm handles this gracefully.

If `nums1` is empty (`m = 0`), the binary search only allows
`i = 0`. Then `j = (n + 1) // 2 - 0 = (n + 1) // 2`, and the
median is computed directly from nums2.

`nums1_left = -inf` (sentinel), `nums1_right = +inf` (sentinel).
The cross-condition `-inf <= nums2[j]` is always true, and
`nums2[j-1] <= +inf` is always true. So the loop converges
immediately with `i = 0`.

The median is read from `nums2_left` and `nums2_right`. Correct.

If `nums2` is empty, we'd swap to put the empty one as nums1.
Same logic applies in mirror.

If both are empty, the problem is undefined (the median of
nothing). The problem statement usually excludes this case.

For input like `nums1 = [], nums2 = [1]`, the algorithm
correctly returns 1 (the only element).
''',
            },
            {
                "question": "Why is this so much harder than the average binary search?",
                "answer": r'''
Three reasons.

**First, the search space is non-obvious.** Most binary searches
look at an array's indices or a candidate-answer range. Here,
we search the partition position — a concept that requires you
to first understand what "partition" means in this context.

**Second, the cross-condition has multiple parts.** Most binary
searches compare a single value to a single target. Here, we
check four boundary elements against each other in a specific
crossing pattern. Getting the four `<=` comparisons right is
where most beginners trip.

**Third, the boundary sentinels.** When `i = 0` or `i = m`, the
formulas reference "out of bounds" elements. Without sentinels,
the code crashes. With wrong sentinels, the cross-condition is
miscomputed. Both kinds of bugs are subtle.

These three reasons together make this problem one of the
"hardest LeetCode binary search" by reputation. The fact that
the algorithm is *O(log)* makes it tempting to try, but the
implementation needs careful boundary handling.

For interview purposes: practice this problem at least three
times. Once is not enough. The boundary intuition only
develops with repetition.
''',
            },
        ],
        "summary": r'''
**Pattern**: binary search the partition point on the smaller
array. Use sentinels for out-of-bounds indices. Check the
four-element cross-condition.

**Lesson**: binary search applies to any 1D monotonic space.
Here, the space is "the partition point in the smaller array,"
not the usual array indices or candidate answers.

**Recognize next time**: "k-th element of two sorted arrays" is
the close cousin. Same partition idea, slightly different
half-size formula.
''',
    },
    {
        "id": "search-rotated-ii",
        "title": "Search in Rotated Sorted Array II (With Duplicates)",
        "step_id": 4,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["binary-search", "rotated"],
        "what_this_teaches": (
            "How duplicates degrade binary search. The 'one half is "
            "sorted' check fails when arr[lo] == arr[mid] == arr[hi]; "
            "we recover by shrinking the ambiguous boundary, "
            "accepting an O(n) worst case."
        ),
        "pattern": (
            "Same as search-rotated-i, but on the ambiguous "
            "arr[lo] == arr[mid] == arr[hi] case, shrink lo and hi "
            "by one."
        ),
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["search-rotated-i", "min-in-rotated"],
        "next_problems": ["single-element-sorted"],
        "resources": [
            _SHEET,
            _lc(81, "search-in-rotated-sorted-array-ii"),
        ],
        "understanding": r'''
Like the first "search in a rotated sorted array" problem, but
the array may now contain **duplicates**. Return `True` if the
target is present, `False` otherwise.

For `arr = [2, 5, 6, 0, 0, 1, 2]`, target = `0`: return `True`.
For target = `3`: return `False`.

The presence of duplicates breaks the previous algorithm's "one
half is always sorted" detection. Recall: in the no-duplicates
version, we determined which half was sorted by comparing
`arr[lo]` to `arr[mid]`. If `arr[lo] <= arr[mid]`, left half is
sorted; else right half is. That comparison is unambiguous when
all elements are distinct.

With duplicates, the comparison can be misleading. Consider
`arr = [3, 1, 2, 3, 3, 3, 3]`, target = `2`. At the first
midpoint, `arr[lo] = 3, arr[mid] = 3, arr[hi] = 3`. All three
are equal. Is the left half sorted? Could be. Could be that
the discontinuity is hidden in the run of duplicates. We don't
know.

The fix: when `arr[lo] == arr[mid] == arr[hi]`, we cannot
deterministically decide. We give up on this iteration and just
**shrink both boundaries by 1**: `lo += 1` and `hi -= 1`. This
loses the *O(log n)* guarantee in the worst case (e.g., the
array is all duplicates and the target is absent — we end up
walking the whole array). The worst case becomes *O(n)*.

In practice — when the array has only a few duplicates — the
algorithm still runs in *O(log n)*. The *O(n)* worst case
applies only to adversarial inputs.

This problem teaches an important meta-lesson: **algorithms
depend on the data's exact properties**. A small relaxation
(allowing duplicates) can break the *O(log n)* guarantee. When
porting an algorithm to a related problem, always ask: "what
properties did the original algorithm rely on, and do they
still hold?"
''',
        "brute_force": {
            "explanation": r'''
Linear scan. Walk every element. *O(n)*.

```python
def search_brute(arr, target):
    return target in arr
```

Correct, simple. The *in* operator is *O(n)* for lists.

For very small arrays or arrays with many duplicates (where the
optimized version is also *O(n)*), this is just as fast and
simpler to write.

The optimized binary-search version below has the same *O(n)*
worst case but does *O(log n)* on inputs without too many
duplicates.
''',
            "code": r'''def search_brute(arr: list[int], target: int) -> bool:
    return target in arr
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "thought_process": r'''
The optimized algorithm extends `search-rotated-i` with one new
branch: when `arr[lo] == arr[mid] == arr[hi]`, shrink both
boundaries by 1.

```python
def search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return True
        # NEW: handle the ambiguous case.
        if arr[lo] == arr[mid] == arr[hi]:
            lo += 1
            hi -= 1
            continue
        # Otherwise, same as search-rotated-i.
        if arr[lo] <= arr[mid]:
            if arr[lo] <= target < arr[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if arr[mid] < target <= arr[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return False
```

Why does the shrink work? When `arr[lo] == arr[mid] == arr[hi]`,
we don't lose any potential matches by trimming `lo` and `hi`
each by one: the values at `lo` and `hi` equal the value at `mid`,
which we just checked (and it didn't equal the target). So those
boundary values are also not the target. Removing them is safe.

The worst case is when the array is mostly duplicates. For
`arr = [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1]` (one off-pattern
element), the ambiguity branch fires many times before the
search narrows. The worst-case complexity becomes *O(n)*.

For most realistic inputs, the algorithm stays *O(log n)*. The
*O(n)* worst case applies only when the array is pathologically
dominated by duplicates.

A practical note: in interview settings, mention the *O(n)*
worst case upfront. If the interviewer asks for a strictly
*O(log n)* algorithm even with duplicates, the answer is:
"it cannot be done in the worst case; the duplicates break the
sortedness signal." Different problem formulations require
different acknowledgments.
''',
        "optimized": {
            "explanation": r'''
Binary search adapted for duplicates. When the boundary
comparison is ambiguous, shrink both ends by 1 and retry.
''',
            "code": r'''def search(arr: list[int], target: int) -> bool:
    # Standard binary search bounds.
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        # Midpoint of the current window.
        mid = (lo + hi) // 2
        # Exact match — return immediately.
        if arr[mid] == target:
            return True
        # The ambiguous case: all three boundary values are equal.
        # We cannot determine which half is sorted, because the
        # discontinuity could be hidden in a run of duplicates.
        # Safe fallback: trim one element from each end.
        # We know arr[lo] == arr[mid] != target, so removing arr[lo]
        # cannot remove the target. Same for arr[hi].
        if arr[lo] == arr[mid] == arr[hi]:
            lo += 1
            hi -= 1
            continue
        # Otherwise, determine which half is sorted using arr[lo]
        # vs arr[mid]. This is the same logic as search-rotated-i.
        if arr[lo] <= arr[mid]:
            # Left half [lo, mid] is fully sorted.
            if arr[lo] <= target < arr[mid]:
                # Target is in the sorted left half.
                hi = mid - 1
            else:
                # Target must be in the unsorted right half (if anywhere).
                lo = mid + 1
        else:
            # Right half [mid, hi] is fully sorted.
            if arr[mid] < target <= arr[hi]:
                # Target is in the sorted right half.
                lo = mid + 1
            else:
                # Target must be in the unsorted left half (if anywhere).
                hi = mid - 1
    # Window emptied without finding the target.
    return False
''',
            "complexity": (
                "**Time**: *O(log n)* average; *O(n)* worst case for "
                "arrays with many duplicates.\n\n"
                "**Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
This problem cements the meta-lesson from the previous "Search
in Rotated Sorted Array" (LC 33): **the algorithm depends on
the input's structural properties, and a small relaxation can
break the guarantees**.

LC 33 (no duplicates) → *O(log n)* guaranteed.
LC 81 (with duplicates) → *O(log n)* average, *O(n)* worst.

The worst-case degradation is unavoidable for this kind of
input. Consider `arr = [1, 1, 1, 1, 1, 1, 0, 1]` and target =
`0`. There is no constant-time check at any midpoint that
deterministically locates the `0` — the boundary values give
no signal. Any algorithm must scan past the duplicates, hence
*O(n)* worst case.

The general principle: when designing an algorithm, list the
properties it relies on. Then ask which problem inputs can
violate those properties. The complexity claim only holds for
inputs that don't violate.

A practical takeaway: in real code with truly large arrays
containing many duplicates, the binary-search approach is no
better than a linear scan. Don't reach for it expecting *O(log
n)* on adversarial inputs. For "almost sorted with some
duplicates," it's still faster than the linear scan on average.
''',
        "confusion_notes": [
            {
                "question": "Why shrink BOTH lo and hi when they're equal?",
                "answer": r'''
Symmetry. The ambiguous case is `arr[lo] == arr[mid] == arr[hi]`
— all three boundary values equal. Since we just checked
`arr[mid] != target`, we know all three are not the target.

Shrinking `lo` removes the leftmost equal value (which is not
the target). Shrinking `hi` removes the rightmost. Both moves
are safe.

You could shrink only one side, and the algorithm would still
be correct — just slightly slower (one ambiguity-clearing
step per iteration instead of two). Shrinking both is the
standard implementation.

A subtle point: shrinking only `lo` would still preserve
correctness because `lo += 1` advances toward the boundary
where we eventually leave the duplicate run. Same for `hi -=
1`. But doing both at once is twice as efficient — and the
implementation is no harder.
''',
            },
            {
                "question": "Can the worst case really hit O(n)?",
                "answer": r'''
Yes. Consider `arr = [1, 1, 1, 1, 0, 1]` and target = `0`.

- `lo = 0, hi = 5, mid = 2`. All equal (1, 1, 1). Shrink. `lo
  = 1, hi = 4`.
- `lo = 1, hi = 4, mid = 2`. arr[lo] = 1, arr[mid] = 1, arr[hi]
  = 0. Not all equal. arr[lo] <= arr[mid], so left is sorted.
  arr[lo] = 1 <= 0 < arr[mid] = 1? 1 <= 0 is False, so target
  is in the right half. lo = mid + 1 = 3.
- ...

Actually this particular example terminates pretty fast. But
for `arr = [1] * (n - 1) + [0]` and target = `0`, the algorithm
spends most iterations on ambiguity shrinks before finally
locating the `0`. The total iterations approach `n`.

For non-adversarial inputs, the algorithm typically converges
fast. But you cannot claim *O(log n)* worst case when
duplicates are present.

In interview settings, write the algorithm and quote *O(n)*
worst case, *O(log n)* average. That's the honest answer.
''',
            },
            {
                "question": "Is there a way to keep O(log n) worst case for the duplicates case?",
                "answer": r'''
No, not for arbitrary duplicates. The information-theoretic
argument: with all-duplicate inputs, no constant-time test at
any midpoint can reliably distinguish "target is to the left"
from "target is to the right." Without such a test, you cannot
halve the search space each iteration. So you cannot achieve
*O(log n)* in the worst case.

For specific structured duplicate patterns (e.g., "at most k
distinct values"), specialized algorithms might do better. But
for arbitrary "rotated sorted with duplicates," *O(n)* is the
proven lower bound.

This is one of those cases where the optimal answer depends on
the input restrictions. The interview answer for LC 81 is
"average *O(log n)*, worst *O(n)*" — exactly what we
implemented.
''',
            },
            {
                "question": "When does the algorithm beat linear scan in practice?",
                "answer": r'''
For arrays with few duplicates, the algorithm typically runs in
near-*O(log n)*. The ambiguity branch fires only when the
boundary values happen to all equal — rare for inputs with
mostly distinct values.

For arrays where the rotation pivot is far from the boundary
duplicates, the algorithm narrows the search quickly.

For all-duplicates or near-all-duplicates inputs, the algorithm
degrades to *O(n)*, no better than linear scan. The linear
scan in such cases is simpler and may actually be faster in
constant factors.

A real-world rule of thumb: if you expect the input to have at
most a small fraction of duplicates, the binary-search approach
is better. If duplicates are common, use the linear scan and
move on.
''',
            },
        ],
        "summary": r'''
**Pattern**: same as search-rotated-i, with an extra ambiguity-
handling branch when `arr[lo] == arr[mid] == arr[hi]`.

**Lesson**: duplicates degrade binary search from *O(log n)* to
*O(n)* worst case. The "one half is sorted" detection fails
when boundary values coincide.

**Recognize next time**: any "rotated sorted array with
duplicates" variant. Accept the worst-case degradation; quote
the honest complexity.
''',
    },
    {
        "id": "sqrt-using-bs",
        "title": "Square Root of a Number Using Binary Search",
        "step_id": 4,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["binary-search", "bs-on-answer", "math"],
        "what_this_teaches": (
            "The cleanest possible 'binary search on the answer' "
            "example. The answer space is `[0, n]`, the feasibility "
            "predicate is `mid * mid <= n`, monotonicity is obvious. "
            "Once you've written this, every other BS-on-answer "
            "problem feels familiar."
        ),
        "pattern": (
            "Binary search the candidate answer in [0, n]; predicate "
            "is `mid * mid <= n`."
        ),
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["koko-bananas", "lower-bound"],
        "next_problems": [
            "nth-root",
            "smallest-divisor-threshold",
            "ship-packages-d-days",
            "min-days-bouquets",
        ],
        "resources": [
            _SHEET,
            _lc(69, "sqrtx"),
        ],
        "understanding": r'''
Compute the **integer square root** of a non-negative integer
`n`. That is, return the largest integer `r` such that `r * r
<= n`.

For `n = 16`, return `4` (since `4 * 4 = 16`).
For `n = 17`, return `4` (since `4 * 4 = 16 <= 17` but `5 * 5
= 25 > 17`).
For `n = 0`, return `0`.

This is LeetCode 69 with a slight phrasing twist (LC 69 asks
for `floor(sqrt(n))`, which is the same as our "largest r with
r * r <= n").

You might be tempted to call Python's `math.isqrt(n)` and be
done — and in production code, that's the right answer. But
the educational point of this problem is to **practice the
"binary search on the answer" pattern on its cleanest possible
example**. Once you can do this from memory, the harder
BS-on-answer problems (aggressive cows, painter's partition,
ship packages) feel like variations on the same theme.

So let's solve it three ways: brute force linear search, binary
search on the answer, and the closed-form (`math.isqrt`).
''',
        "brute_force": {
            "explanation": r'''
Try every candidate from 0 upward. The largest `r` such that
`r * r <= n` is the integer square root.

```python
def isqrt_linear(n):
    r = 0
    while (r + 1) * (r + 1) <= n:
        r += 1
    return r
```

`O(sqrt(n))` time. For `n = 10^9`, that's about 31,623 iterations
— acceptable for one query but slow if you have many.

The brute force is correct and obvious. The binary search
version brings it down to `O(log n)` — about 30 iterations even
for `n = 10^9`.
''',
            "code": r'''def isqrt_linear(n: int) -> int:
    # Walk from 0 upward, increasing r until (r + 1)^2 exceeds n.
    # The largest r with r^2 <= n is the answer.
    r = 0
    while (r + 1) * (r + 1) <= n:
        r += 1
    return r
''',
            "complexity": "**Time**: *O(sqrt(n))*. **Space**: *O(1)*.",
        },
        "thought_process": r'''
The optimized algorithm is binary search on the answer. Let's
walk through the recipe.

**Step 1: Identify the candidate range.** The integer square
root is at least 0 (for `n = 0`) and at most `n` (a loose
bound; for `n >= 1`, the answer is at most `n` since `n * n >=
n`). So the candidate range is `[0, n]`.

A tighter upper bound: `n // 2 + 1` for `n >= 2` (because
`(n // 2)^2 >= n` for `n >= 4`). But `n` works fine as a loose
upper bound and the log factor barely changes.

**Step 2: Write the feasibility predicate.** Given a candidate
`r`, "is this a valid answer?" means `r * r <= n`. This is a
constant-time check.

**Step 3: Verify monotonicity.** If `r * r <= n`, then for any
`r' < r`, `r' * r' < r * r <= n`. So smaller candidates are
also valid. If `r * r > n`, every larger candidate also has
`r'^2 >= r^2 > n`. So feasibility is monotonic: the valid
candidates form a contiguous prefix `[0, ans]`, and we want
the largest one.

**Step 4: Binary search.** Use the "find the largest feasible
candidate" template:

```python
lo, hi = 0, n
ans = 0
while lo <= hi:
    mid = (lo + hi) // 2
    if mid * mid <= n:
        ans = mid       # feasible; record and try larger
        lo = mid + 1
    else:
        hi = mid - 1    # infeasible; try smaller
return ans
```

Worked example on `n = 17`:

- `lo = 0, hi = 17`. `mid = 8`. `8 * 8 = 64 > 17`. Infeasible.
  `hi = 7`.
- `lo = 0, hi = 7`. `mid = 3`. `3 * 3 = 9 <= 17`. Feasible. `ans
  = 3`. `lo = 4`.
- `lo = 4, hi = 7`. `mid = 5`. `5 * 5 = 25 > 17`. Infeasible.
  `hi = 4`.
- `lo = 4, hi = 4`. `mid = 4`. `4 * 4 = 16 <= 17`. Feasible.
  `ans = 4`. `lo = 5`.
- `lo = 5, hi = 4`. Loop exits.
- Return `ans = 4`. Correct.

Four iterations for `n = 17`. `log2(17) ≈ 4.1`, so this matches.

For `n = 10^18`, the binary search converges in about 60
iterations.
''',
        "optimized": {
            "explanation": r'''
Binary search on the candidate answer. The predicate is one
multiplication; the iteration count is logarithmic.
''',
            "code": r'''def isqrt(n: int) -> int:
    # Edge case: sqrt(0) is 0.
    if n < 2:
        return n
    # Candidate range: 0 to n inclusive. We will tighten it via
    # binary search.
    lo, hi = 1, n
    # Track the largest feasible candidate seen so far.
    ans = 0
    while lo <= hi:
        # Midpoint of the current candidate window.
        mid = (lo + hi) // 2
        # Feasibility check: is mid * mid still within n?
        # We use multiplication rather than computing the square root
        # because integer multiplication is exact and avoids the
        # floating-point pitfalls of math.sqrt.
        if mid * mid <= n:
            # mid is a valid answer (mid^2 fits within n). Could there
            # be a larger valid answer? Yes — try larger.
            ans = mid
            lo = mid + 1
        else:
            # mid^2 already exceeds n. No larger candidate will work.
            # Try smaller.
            hi = mid - 1
    return ans
''',
            "complexity": (
                "**Time**: *O(log n)*. The binary search halves the "
                "window each iteration.\n\n"
                "**Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
This problem is the canonical "binary search on the answer"
exercise. It is intentionally simple — the candidate range is
just `[0, n]`, the feasibility predicate is one multiplication,
and monotonicity is obvious. There is no greedy subroutine to
worry about.

Once this problem is in your fingers, the harder BS-on-answer
problems (Koko, aggressive cows, ship packages) feel like
small variations: identify the candidate range, write a
slightly more elaborate feasibility checker, verify monotonicity,
binary search.

A subtle technical point: **why not use `math.sqrt(n)` and cast
to int?**

```python
return int(math.sqrt(n))
```

This is `O(1)` and looks cleaner. But it has a subtle
floating-point pitfall: `math.sqrt` returns a float, and floats
have only about 15-17 significant digits of precision. For very
large `n` (close to `2^53`), `math.sqrt(n)` can be off by 1.
The cast then gives the wrong answer.

Example: `math.sqrt(2**52 - 1)` might return `67108863.99999998`
or `67108864.0` depending on rounding. The correct integer
square root is `67108863`. The float-based approach can give
`67108864`, which is wrong.

`math.isqrt(n)` (added in Python 3.8) avoids this entirely by
using integer arithmetic internally. **It is the right
production answer**.

But for interview practice, the binary search version
demonstrates understanding of BS-on-answer. Mention both: "I'd
use `math.isqrt` in production for safety; here's the binary
search to show I understand the underlying algorithm."

The connection to the algorithm hierarchy:

- `math.isqrt`: O(1) (or very fast), but a built-in.
- Binary search: O(log n), educational, what interviewers want.
- Linear scan: O(sqrt(n)), baseline.
- Newton's method: O(log log n), faster but more involved.

Newton's method is mentioned for completeness; it's rarely the
right interview answer because the algorithm is more complex
and the speedup over binary search is negligible for typical
inputs.
''',
        "confusion_notes": [
            {
                "question": "Why use `mid * mid <= n` instead of `mid <= sqrt(n)`?",
                "answer": r'''
Because `mid * mid` is **exact integer arithmetic** while
`sqrt(n)` returns a float with limited precision.

For large `n` (say, `n = 10^15`), `sqrt(n)` can be off by a
tiny amount due to floating-point rounding. That tiny error,
when used as a comparison threshold, can push the algorithm to
the wrong side of the boundary and give a wrong answer by 1.

`mid * mid` is exact in Python (arbitrary precision integers).
The comparison `mid * mid <= n` is precise regardless of how
large `n` is.

In C++ or Java with fixed-width integers, `mid * mid` can
**overflow** for very large `n`. In those languages, you have
to be careful: compute `mid` as a `long`, or use the comparison
`mid <= n / mid` (which avoids the multiplication).

In Python, the overflow concern doesn't exist. Always use
`mid * mid` and stay in integer-land for sqrt computations.
''',
            },
            {
                "question": "Why does the answer start at 0?",
                "answer": r'''
Because `sqrt(0) = 0` and `sqrt(1) = 1`, and for `n = 0` we
return `0` directly via the early-exit `if n < 2: return n`.

For `n >= 2`, the smallest candidate worth checking is `1` (since
`0 * 0 = 0 <= n` for any non-negative `n`). The `ans = 0`
initialization is the floor — even if the binary search
somehow narrows to nothing, returning `0` is a safe default.

In practice, the binary search always finds at least `ans = 1`
for `n >= 1`, so the `ans = 0` initialization is overkill but
defensive.
''',
            },
            {
                "question": "Could the algorithm overflow for very large n?",
                "answer": r'''
In Python, no. Integers are arbitrary precision.

In C++ / Java with 32-bit or 64-bit integers, yes. For `n
= 2^31 - 1` and `mid` near `sqrt(n) ≈ 46341`, `mid * mid` is
about `2.15 * 10^9` — fits in a 32-bit unsigned int but
overflows 32-bit signed. To be safe in C++, use `long long`
for `mid * mid`, or rewrite the comparison as `mid <= n / mid`
(which uses division to avoid the multiplication).

The Python solution is fully overflow-proof. One of the small
joys of working in Python — no overflow worry on sqrt
problems.
''',
            },
            {
                "question": "How is this different from finding the n-th root?",
                "answer": r'''
The square root is `n^(1/2)`. The n-th root is `n^(1/k)` for
arbitrary integer `k`. Same algorithm, different exponent in
the feasibility check.

For n-th root: feasibility is `mid^k <= n`. Computing `mid^k`
takes `O(log k)` time via fast exponentiation. Binary search
over candidates takes `O(log n)` iterations. Total: `O(log n
* log k)`.

The structure is identical: candidate range, monotonic predicate,
binary search. Only the "compute power" step changes.

We have a separate problem `nth-root` in this curriculum (Step
4 Lecture 2) that walks through it. It's a great follow-up
after you've mastered sqrt.
''',
            },
        ],
        "summary": r'''
**Pattern**: binary search on the candidate `[0, n]` with
predicate `mid * mid <= n`. The simplest possible BS-on-answer.

**Lesson**: when the feasibility predicate is `O(1)` and the
candidate range is `[low, high]`, binary search the range. This
problem is the cleanest demonstration of the pattern.

**Recognize next time**: any "find the largest integer `r`
such that property P(r) holds and P is monotonic" problem. The
recipe writes itself.
''',
    },
    {
        "id": "smallest-divisor-threshold",
        "title": "Find the Smallest Divisor Given a Threshold",
        "step_id": 4,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["binary-search", "bs-on-answer"],
        "what_this_teaches": (
            "Another canonical BS-on-answer. The candidate is the "
            "divisor; the feasibility predicate sums up ceiling-"
            "divisions and compares against a threshold. Same recipe "
            "as Koko, framed with arithmetic."
        ),
        "pattern": "Binary search divisor in [1, max(nums)]; check if ceiling-sum stays under threshold.",
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["koko-bananas", "sqrt-using-bs"],
        "next_problems": [
            "ship-packages-d-days",
            "min-days-bouquets",
            "aggressive-cows",
            "book-allocation",
        ],
        "resources": [
            _SHEET,
            _lc(1283, "find-the-smallest-divisor-given-a-threshold"),
        ],
        "understanding": r'''
You are given an array of positive integers `nums` and an
integer `threshold`. Choose a positive integer divisor `d`,
divide each number in `nums` by `d` (rounding up), and sum the
results. Return the **smallest** `d` such that the sum is at
most `threshold`.

Example: `nums = [1, 2, 5, 9]`, `threshold = 6`.

- `d = 1`: sum = `1 + 2 + 5 + 9 = 17`. Exceeds 6.
- `d = 2`: sum = `ceil(1/2) + ceil(2/2) + ceil(5/2) + ceil(9/2)
  = 1 + 1 + 3 + 5 = 10`. Exceeds.
- `d = 3`: sum = `1 + 1 + 2 + 3 = 7`. Exceeds.
- `d = 4`: sum = `1 + 1 + 2 + 3 = 7`. Wait, let me recompute:
  `ceil(1/4) = 1, ceil(2/4) = 1, ceil(5/4) = 2, ceil(9/4) = 3`.
  Sum = 7. Exceeds.
- `d = 5`: sum = `1 + 1 + 1 + 2 = 5`. Within threshold!
- `d = 4`: already computed as 7. Exceeds.

So the smallest feasible `d` is 5.

The brute force tries every `d` from 1 to `max(nums)` and
returns the first feasible one. *O(max(nums) × n)* time. For
large arrays with large values, too slow.

The optimization is **binary search on the divisor**. Same
recipe as Koko Eating Bananas (which we already covered): the
candidate range is `[1, max(nums)]`, the feasibility checker
computes the sum of ceiling-divisions, monotonicity is
straightforward (larger divisor → smaller sum), and binary
search picks the smallest feasible divisor.

This is yet another example of the BS-on-answer family.
Recognizing the pattern is the whole game.
''',
        "brute_force": {
            "explanation": r'''
Try every candidate divisor from 1 to `max(nums)`. Return the
first one that satisfies the threshold.

```python
def smallest_divisor_linear(nums, threshold):
    for d in range(1, max(nums) + 1):
        s = sum((x + d - 1) // d for x in nums)
        if s <= threshold:
            return d
    return -1  # should not happen if problem guarantees a solution
```

`O(max(nums) × n)`. For `nums` of size 50,000 with values up
to a million, that's 5 * 10^10 operations — way too slow.

The binary search version brings it to `O(n × log(max(nums)))`
— about 30 * 50,000 = 1.5 * 10^6 operations. Manageable.
''',
            "code": r'''def smallest_divisor_linear(nums: list[int], threshold: int) -> int:
    # Try every candidate divisor in increasing order.
    for d in range(1, max(nums) + 1):
        # Sum of ceiling divisions for this candidate.
        s = sum((x + d - 1) // d for x in nums)
        # First d for which the sum stays within threshold is the answer.
        if s <= threshold:
            return d
    return -1
''',
            "complexity": (
                "**Time**: *O(max(nums) × n)*. Slow for large value "
                "ranges.\n\n"
                "**Space**: *O(1)*."
            ),
        },
        "thought_process": r'''
The recipe is the same as Koko Eating Bananas. Let's apply it
verbatim.

**Step 1: Candidate range.** Divisor can be from 1 (no
division) up to `max(nums)` (large enough that every number
ceiling-divides to 1, giving sum = n which is the minimum
possible).

**Step 2: Feasibility checker.** Given a candidate `d`, compute
`sum(ceil(x / d) for x in nums)` and compare with threshold.
*O(n)* time. Use the standard ceiling-division trick
`(x + d - 1) // d`.

**Step 3: Monotonicity.** As `d` increases, each ceiling-
division `ceil(x / d)` decreases (or stays the same). So the
sum decreases monotonically with `d`. Feasibility is monotonic:
if `d = D` works, every `d > D` also works.

**Step 4: Binary search.** Find the smallest feasible `d`.
Half-open lower-bound style.

```python
lo, hi = 1, max(nums)
while lo < hi:
    mid = (lo + hi) // 2
    if sum_at(mid) <= threshold:
        hi = mid    # mid feasible; try smaller
    else:
        lo = mid + 1
return lo
```

Worked example on `nums = [1, 2, 5, 9]`, `threshold = 6`:

- `lo = 1, hi = 9`. `mid = 5`. Sum = 1+1+1+2 = 5. ≤ 6. Feasible.
  `hi = 5`.
- `lo = 1, hi = 5`. `mid = 3`. Sum = 1+1+2+3 = 7. > 6. Infeasible.
  `lo = 4`.
- `lo = 4, hi = 5`. `mid = 4`. Sum = 1+1+2+3 = 7. > 6. Infeasible.
  `lo = 5`.
- `lo = 5, hi = 5`. Exit. Return 5.

Three iterations on a four-element array. Correct.

The algorithm is virtually identical to Koko's. Once you
recognize the BS-on-answer pattern, these problems become
formula-fill exercises.
''',
        "optimized": {
            "explanation": r'''
Binary search on the divisor candidate range. Feasibility
checker is `O(n)` ceiling-division sum.
''',
            "code": r'''def smallest_divisor(nums: list[int], threshold: int) -> int:
    def total_for(d: int) -> int:
        # Sum of ceil(x / d) for x in nums.
        # The ceiling-division trick: ceil(a / b) = (a + b - 1) // b
        # for non-negative integers. We use it because integer ceiling
        # is faster and exact compared to math.ceil(a / b) which would
        # use floats.
        return sum((x + d - 1) // d for x in nums)

    # Candidate range: divisor in [1, max(nums)].
    # Lower bound 1: any smaller divisor isn't well-defined.
    # Upper bound max(nums): at this divisor, every number rounds up
    # to 1, giving the minimum possible sum of n.
    lo, hi = 1, max(nums)
    # Half-open binary search for the smallest feasible divisor.
    while lo < hi:
        mid = (lo + hi) // 2
        if total_for(mid) <= threshold:
            # mid is feasible. Try smaller divisors.
            hi = mid
        else:
            # mid is infeasible. Need larger.
            lo = mid + 1
    return lo
''',
            "complexity": (
                "**Time**: *O(n log(max(nums)))*. The binary search "
                "has *O(log)* iterations, each doing an *O(n)* "
                "feasibility check.\n\n"
                "**Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
This problem confirms that the BS-on-answer recipe is **truly
mechanical** once you recognize the pattern. The problem here
is identical to Koko Eating Bananas in structure:

- **Koko**: minimize the eating speed such that all piles
  finish within `h` hours.
- **Smallest divisor**: minimize the divisor such that the
  ceiling-sum stays within `threshold`.

Both have:
- A monotonic "smaller candidate → harder feasibility" relation.
- A polynomial-time feasibility checker.
- The same half-open lower-bound binary search structure.

The feasibility check in both uses ceiling division — which is
not a coincidence. Many "rate" or "capacity" problems use
ceiling-division accounting (you need to round up because you
can't split a discrete unit of work).

Memorize the ceiling-division idiom:

> `ceil(a / b) = (a + b - 1) // b` for non-negative integers.

It comes up constantly in BS-on-answer and many other contexts.

The lesson: once you internalize the BS-on-answer recipe, an
entire lecture's worth of "hard" problems collapses into
mechanical work. The challenge is recognition, not
implementation.
''',
        "confusion_notes": [
            {
                "question": "Why ceiling division and not regular division?",
                "answer": r'''
Because the problem specifies "round up" — each number's
contribution to the sum is `ceil(x / d)`, not `x / d`.

Why "round up"? In problems about discrete work units (like
"how many trips do I need to carry x items at d items per
trip"), partial trips still count as a full trip. If you have
5 items and a capacity of 3 per trip, you need 2 trips (not
1.67).

Floor division `x // d` would underestimate. Standard `/`
returns a float, which we'd have to ceiling anyway.

The integer trick `(x + d - 1) // d`:

- For `x = 5, d = 3`: `(5 + 2) // 3 = 7 // 3 = 2`. Correct.
- For `x = 6, d = 3`: `(6 + 2) // 3 = 8 // 3 = 2`. Correct
  (exactly 2, no rounding needed).
- For `x = 0, d = 3`: `(0 + 2) // 3 = 0`. Correct.

The "+ d - 1" pushes the dividend up by enough to force the
floor to round up when there's any remainder.

Alternative: `math.ceil(x / d)` works but uses floats.

For Python, the integer trick is preferred — exact, fast, no
float pitfalls.
''',
            },
            {
                "question": "Why is the upper bound max(nums) and not something larger?",
                "answer": r'''
Because at `d = max(nums)`, every number divides to 1 (or 0,
for a 0 in the array). The sum becomes exactly `n` (the number
of elements). Going higher doesn't reduce the sum further.

For example, `nums = [5, 7, 9]`. At `d = 9`, the ceiling-
divisions are `ceil(5/9) = 1, ceil(7/9) = 1, ceil(9/9) = 1`.
Sum = 3 = n. At `d = 10`, same result: 1 + 1 + 1 = 3. So `d >=
max(nums)` all give the same minimum sum.

If the threshold is at least `n` (the array size), the answer
is at most `max(nums)`. If the threshold is less than `n`, the
problem is infeasible (you can't get below `n` no matter what
divisor you pick).

Setting `hi = max(nums)` is the tight upper bound. You could
set `hi` to any larger number and the binary search would still
work; the tight choice just saves a couple of iterations.
''',
            },
            {
                "question": "Why is the lower bound 1 and not 0?",
                "answer": r'''
Because dividing by 0 is undefined (and Python raises
`ZeroDivisionError`). So 0 is not a valid divisor.

The problem statement also specifies positive divisors. So the
smallest meaningful candidate is 1.

A divisor of 1 means no division — each number contributes
itself to the sum. So the sum at `d = 1` is `sum(nums)`. If
`sum(nums) <= threshold`, the answer is 1.

The binary search starts at `lo = 1` for safety. The first
iteration's `mid = (1 + max(nums)) // 2`, which is well-defined.
''',
            },
            {
                "question": "What if no divisor satisfies the threshold?",
                "answer": r'''
The problem statement usually guarantees a solution exists
(i.e., `threshold >= n` so the answer is at most `max(nums)`).

If you wanted to handle infeasibility, you'd check after the
binary search whether `total_for(lo) <= threshold`. If not,
return -1 or raise an exception.

```python
result = ...  # binary search
if total_for(result) > threshold:
    return -1
return result
```

In LeetCode 1283, the constraints guarantee feasibility, so
this check isn't needed.

A simpler way to think about it: the minimum possible sum is
`n` (when `d` is large enough). If `threshold < n`, no
candidate works. Check this upfront and return -1 if so.
''',
            },
        ],
        "summary": r'''
**Pattern**: binary search the divisor in `[1, max(nums)]`;
feasibility predicate is `sum(ceil(x / mid) for x in nums) <=
threshold`.

**Lesson**: yet another instance of the BS-on-answer family.
The ceiling-division idiom `(x + d - 1) // d` is a small but
critical detail.

**Recognize next time**: any "minimize the divisor / rate /
capacity so a sum stays under a threshold" problem. The recipe
is mechanical.
''',
    },
    {
        "id": "ship-packages-d-days",
        "title": "Capacity to Ship Packages Within D Days",
        "step_id": 4,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["binary-search", "bs-on-answer", "greedy"],
        "what_this_teaches": (
            "BS-on-answer with a contiguous-greedy feasibility "
            "checker. The candidate is the ship capacity; the "
            "checker walks the packages in order, packing each ship "
            "greedily."
        ),
        "pattern": "Binary search capacity in [max(weights), sum(weights)]; greedy partition checks day count.",
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["book-allocation", "aggressive-cows", "koko-bananas"],
        "next_problems": [
            "min-days-bouquets",
            "split-array-largest-sum",
            "painters-partition",
        ],
        "resources": [
            _SHEET,
            _lc(1011, "capacity-to-ship-packages-within-d-days"),
        ],
        "understanding": r'''
You have packages with weights `weights[0], weights[1], ...`
that must be loaded onto a ship and delivered within `days`
days. Packages must be loaded **in the given order** (no
reordering allowed). Each day, the ship can carry packages up
to its capacity (in total weight). Find the **minimum ship
capacity** that allows all packages to be delivered within
`days` days.

Example: `weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`, `days =
5`. We need to partition this into 5 contiguous days such that
the maximum day's total is minimized.

One partition: `[1, 2, 3, 4, 5] | [6, 7] | [8] | [9] | [10]`.
Day totals: 15, 13, 8, 9, 10. Maximum is 15.

Another: `[1, 2, 3, 4] | [5, 6] | [7] | [8, 9] | [10]`. Totals:
10, 11, 7, 17, 10. Maximum 17. Worse.

The minimum-maximum across all valid partitions is the answer.
For this example, it's 15.

This is **exactly** the book-allocation pattern, with "days"
playing the role of "students" and "weights" of "books." The
feasibility checker walks weights left-to-right, accumulating
each day's load up to capacity; if the load would overflow,
start a new day. Count days used.

**Candidate range** for the capacity:

- **Lower bound: `max(weights)`**. No single package can be
  split; the ship must carry at least the heaviest package.
- **Upper bound: `sum(weights)`**. With unlimited capacity (or
  one day), one day takes everything.

**Monotonicity**: larger capacity → fewer days needed. So
feasibility is monotonic in capacity. We want the smallest
feasible capacity.

**Binary search**: half-open lower-bound; find the smallest
capacity where `days_needed(capacity) <= days`.

This is the same algorithm as book-allocation, frame-renamed.
Both are foundational BS-on-answer exercises.
''',
        "brute_force": {
            "explanation": r'''
Try every capacity from `max(weights)` to `sum(weights)`.
Return the first feasible one.

```python
def ship_capacity_linear(weights, days):
    for cap in range(max(weights), sum(weights) + 1):
        if days_needed(weights, cap) <= days:
            return cap
    return -1


def days_needed(weights, cap):
    d = 1
    cur = 0
    for w in weights:
        if cur + w > cap:
            d += 1
            cur = 0
        cur += w
    return d
```

`O((sum - max) × n)` time. Slow for large weight ranges.

The binary search version brings it to `O(n × log(sum - max))`,
about 30 * 1000 = 30,000 operations for typical inputs.
''',
            "code": r'''def ship_capacity_linear(weights: list[int], days: int) -> int:
    # Try each candidate capacity in increasing order.
    for cap in range(max(weights), sum(weights) + 1):
        if days_needed(weights, cap) <= days:
            return cap
    return -1


def days_needed(weights, cap):
    # Greedy: pack each day's load up to capacity.
    d = 1
    cur = 0
    for w in weights:
        if cur + w > cap:
            d += 1
            cur = 0
        cur += w
    return d
''',
            "complexity": "**Time**: *O((sum - max) × n)*. **Space**: *O(1)*.",
        },
        "thought_process": r'''
Same BS-on-answer recipe as book-allocation.

**Candidate range**: `[max(weights), sum(weights)]`.

**Feasibility checker**: given capacity `cap`, compute days
needed by greedy packing. Walk left-to-right; accumulate each
day's load; start a new day when the next package would
overflow.

**Monotonicity**: larger capacity → fewer days. So feasibility
is monotonic.

**Binary search**: find the smallest capacity for which
`days_needed(cap) <= days`.

```python
lo, hi = max(weights), sum(weights)
while lo < hi:
    mid = (lo + hi) // 2
    if days_needed(weights, mid) <= days:
        hi = mid
    else:
        lo = mid + 1
return lo
```

Worked example on `weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`,
`days = 5`:

- `lo = max = 10, hi = sum = 55`.
- `mid = 32`. Greedy: 1+2+3+4+5+6+7 = 28 (next would be 36 > 32).
  Start day 2: 8+9 = 17 (next would be 27 > 32). Start day 3: 10.
  Total: 3 ≤ 5. Feasible. `hi = 32`.
- `lo = 10, hi = 32`. `mid = 21`. Greedy: 1+2+3+4+5 = 15 (next
  6+15 = 21 = cap). 1+2+3+4+5+6 = 21. Next 7+21 = 28 > 21,
  start day 2. Day 2: 7+8 = 15. Day 3: 9+10 = 19. Total: 3 days.
  Feasible. `hi = 21`.

  Wait, let me recount. weights = [1,2,3,4,5,6,7,8,9,10], cap =
  21. Day 1: 1+2+3+4+5+6 = 21 (cap reached). Day 2: 7+8 = 15
  (next 9 would make 24 > 21). Day 3: 9+10 = 19. Total: 3
  days ≤ 5. Feasible.

  `hi = 21`.
- `lo = 10, hi = 21`. `mid = 15`. Day 1: 1+2+3+4+5 = 15. Day 2:
  6+7 = 13 (next 8 > 15-13). Day 3: 8 (next 9 > 15-8). Day 4:
  9 (next 10 > 15-9). Day 5: 10. Total 5 days. Feasible. `hi
  = 15`.
- `lo = 10, hi = 15`. `mid = 12`. Day 1: 1+2+3+4 = 10. Day 2:
  5+6 = 11. Day 3: 7 (next 8 > 12-7). Day 4: 8 (next 9 > 12-8).
  Day 5: 9 (next 10 > 12-9). Day 6: 10. Total 6 days. > 5.
  Infeasible. `lo = 13`.
- `lo = 13, hi = 15`. `mid = 14`. Day 1: 1+2+3+4 = 10 (next 5
  > 14-10). Day 2: 5+6 = 11 (next 7 > 14-11). Day 3: 7 (next 8
  > 14-7). Day 4: 8 (next 9 > 14-8). Day 5: 9 (next 10 > 14-9).
  Day 6: 10. Total 6 days. > 5. Infeasible. `lo = 15`.
- `lo = 15, hi = 15`. Exit. Return 15.

Correct — 15 is the answer, matching our hand analysis.

Five binary-search iterations on a ten-element array. `log2(45) ≈
5.5` iterations, matching.
''',
        "optimized": {
            "explanation": r'''
Binary search the capacity with a greedy day-counting
feasibility checker.
''',
            "code": r'''def ship_within_days(weights: list[int], days: int) -> int:
    def days_needed(cap: int) -> int:
        # Greedy packing: walk the packages in given order. Each day,
        # accumulate weight up to cap; start a new day when the next
        # package would overflow.
        d = 1            # we always need at least one day
        cur = 0          # weight loaded into the current day's ship
        for w in weights:
            # Sanity: a single package heavier than cap is impossible
            # to ship. (The binary search's lower bound max(weights)
            # prevents this for valid inputs, but we guard anyway.)
            if w > cap:
                return float('inf')
            # If this package fits in the current ship, add it.
            if cur + w <= cap:
                cur += w
            else:
                # Otherwise, start a new day with this package.
                d += 1
                cur = w
        return d

    # Candidate range:
    # - max(weights): no single package can be split.
    # - sum(weights): with one day, the ship carries everything.
    lo, hi = max(weights), sum(weights)
    # Half-open lower-bound binary search. Find the smallest feasible
    # capacity (smallest cap such that days_needed(cap) <= days).
    while lo < hi:
        mid = (lo + hi) // 2
        if days_needed(mid) <= days:
            # Feasible at this capacity; try smaller.
            hi = mid
        else:
            # Infeasible; need more capacity.
            lo = mid + 1
    return lo
''',
            "complexity": (
                "**Time**: *O(n log(sum - max))*. Logarithmic binary "
                "search with linear feasibility check.\n\n"
                "**Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
This is the **canonical** "capacity / rate / size" version of
BS-on-answer. The structure:

> Find the smallest `X` such that some greedy procedure can
> complete the task using `X` of some resource.

Examples in this family:

- **Ship packages in D days**: minimum capacity.
- **Koko bananas**: minimum eating speed.
- **Painter's partition**: minimum time.
- **Split array largest sum**: minimum maximum subarray sum.
- **Book allocation**: minimum maximum pages per student.
- **Smallest divisor given a threshold**: minimum divisor.

All are minimize-the-maximum or minimize-the-cost problems
with greedy feasibility checkers and monotonic constraints.

The only differences:

1. What is the candidate (capacity? speed? cost?).
2. What is the feasibility checker (greedy walk? cumulative
   sum? ceiling-division?).
3. What is the candidate range (problem-specific).

Master one, master all. The hard work is recognition; the
implementation is template.

When you see a problem with "minimum X such that...", run the
mental checklist:

1. What is X? That's the BS candidate.
2. What is the range of X?
3. What is the feasibility predicate?
4. Is feasibility monotonic in X?

If all four answer cleanly, the algorithm is mechanical.
''',
        "confusion_notes": [
            {
                "question": "Why must packages be loaded in the given order?",
                "answer": r'''
This is part of the problem constraint. We cannot reorder
packages to make the loading more efficient.

If we *could* reorder, the problem would be different — we'd
solve it greedily by sorting and packing differently. With the
"keep the original order" constraint, the algorithm must
partition the *original sequence* into contiguous groups.

This is what makes the greedy feasibility checker work: walking
left-to-right and starting a new day on overflow gives the
minimum number of days for a given capacity, *given the order
constraint*.

If reordering were allowed, the problem would essentially be
"bin packing," which is NP-hard in general but has good
approximation algorithms.

So the order-preservation is critical to the problem's
tractability via BS-on-answer.
''',
            },
            {
                "question": "Why max(weights) as the lower bound?",
                "answer": r'''
Because the heaviest single package must fit on the ship. We
cannot split a package across days.

If the heaviest package weighs `W` and capacity is less than
`W`, that single package can never be shipped. Infeasible.

So `max(weights)` is the tight lower bound: any smaller
capacity is impossible.

In practice, the feasibility checker has a guard: if any single
weight exceeds the candidate cap, return infinity (or
otherwise signal failure). With the `lo = max(weights)`
initialization, this guard never actually fires during the
binary search — but it's good defensive coding.
''',
            },
            {
                "question": "Why sum(weights) as the upper bound?",
                "answer": r'''
Because with capacity equal to the total weight, we can ship
everything in **one day**. So `days_needed(sum) == 1 <= days`
for any `days >= 1`. The answer is at most `sum(weights)`.

In practice, the answer is often much smaller (when `days` is
larger than 1, we can split the load across multiple days). The
upper bound is loose but safe.

A tighter upper bound: `max(max(weights), sum(weights) //
days)` — the smallest capacity that *could possibly* work
given the day count. But the loose `sum(weights)` works and
the binary search converges in `log` iterations regardless.

Setting tight bounds saves a few iterations but doesn't change
asymptotics.
''',
            },
            {
                "question": "How does the greedy feasibility checker know it's optimal?",
                "answer": r'''
Same exchange argument as in book-allocation. Given any valid
partition into `k` days with each day's load ≤ cap, you can
transform it into the greedy partition by **merging adjacent
day-boundaries** without exceeding cap:

If the greedy puts package `i` on the previous day but the
actual partition starts a new day at `i`, we can merge: the
combined load is the previous day's load plus package `i`,
which is ≤ cap (because the greedy was about to add it and the
greedy never exceeds cap).

By repeatedly merging, we reach the greedy partition. The
greedy uses **at most as many days** as any valid partition.

Therefore: if the greedy needs more than `days` days, no
partition fits. The greedy is the tightest possible test.

This justifies why greedy answers the feasibility question
correctly. The same argument appears in book-allocation,
painter's partition, split-array-largest-sum — all related
problems.
''',
            },
        ],
        "summary": r'''
**Pattern**: binary search the capacity in `[max(weights),
sum(weights)]` with a greedy day-count feasibility checker.

**Lesson**: identical to book-allocation, frame-renamed. The
"minimize X such that greedy can complete" family is large.
Recognize the pattern; implementation is mechanical.

**Recognize next time**: any "minimum capacity / rate / size to
finish within K time" problem.
''',
    },
    {
        "id": "floor-ceil-sorted",
        "title": "Floor and Ceil in a Sorted Array",
        "step_id": 4,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["binary-search", "fundamentals"],
        "what_this_teaches": (
            "Two more queries that factor through lower bound. Floor "
            "is 'largest value ≤ x'; ceil is 'smallest value ≥ x'. "
            "Both are one binary search away."
        ),
        "pattern": "ceil = lower_bound(x); floor = lower_bound(x) - 1 (with guard).",
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["lower-bound", "upper-bound"],
        "next_problems": ["search-insert-position", "search-rotated-i"],
        "resources": [_SHEET],
        "understanding": r'''
Given a sorted array and a target `x`, return:

- **Floor**: the largest value in the array that is at most `x`
  (`-1` or some sentinel if every value exceeds `x`).
- **Ceil**: the smallest value that is at least `x` (sentinel
  if every value is less than `x`).

For `arr = [3, 4, 7, 8, 10]`:

- `x = 5`: floor = 4, ceil = 7.
- `x = 7`: floor = 7, ceil = 7 (exact match).
- `x = 11`: floor = 10, ceil = sentinel (no value ≥ 11).
- `x = 0`: floor = sentinel, ceil = 3.

These are the array equivalents of mathematical floor and ceil
operations.

The clean formulation:

- **Ceil** is `arr[lower_bound(x)]` (with a bounds check —
  return sentinel if lower bound is past the end).
- **Floor** is `arr[lower_bound(x) - 1]` if `arr[lower_bound]
  != x`, otherwise `arr[lower_bound]` itself. More compactly:
  if `lower_bound(x) < n` and `arr[lower_bound(x)] == x`, floor
  is x. Else floor is `arr[lower_bound(x) - 1]` (with guard).

The brute force is *O(n)* — walk and check. The binary search
version is *O(log n)*.
''',
        "brute_force": {
            "explanation": r'''
Linear scan tracking floor and ceil as we walk.

```python
def floor_ceil_linear(arr, x):
    floor_val = ceil_val = None
    for v in arr:
        if v <= x and (floor_val is None or v > floor_val):
            floor_val = v
        if v >= x and (ceil_val is None or v < ceil_val):
            ceil_val = v
    return floor_val, ceil_val
```

`O(n)` time. Correct on any array, sorted or not.

For sorted arrays, binary search via lower bound brings us to
`O(log n)`.
''',
            "code": r'''def floor_ceil_linear(arr: list[int], x: int) -> tuple:
    floor_val = ceil_val = None
    for v in arr:
        if v <= x and (floor_val is None or v > floor_val):
            floor_val = v
        if v >= x and (ceil_val is None or v < ceil_val):
            ceil_val = v
    return floor_val, ceil_val
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "optimized": {
            "explanation": r'''
One binary search (lower bound) gives both floor and ceil.
''',
            "code": r'''def floor_ceil(arr: list[int], x: int) -> tuple:
    # Lower bound: first index with arr[i] >= x.
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] >= x:
            hi = mid
        else:
            lo = mid + 1
    # lo is now the lower bound.
    # CEIL: the smallest value >= x.
    # If lo is past the end, no such value exists.
    ceil_val = arr[lo] if lo < len(arr) else None
    # FLOOR: the largest value <= x.
    # If arr[lo] == x, floor is x itself.
    # Otherwise, floor is at position lo - 1 (if lo > 0).
    if lo < len(arr) and arr[lo] == x:
        floor_val = x
    elif lo > 0:
        floor_val = arr[lo - 1]
    else:
        floor_val = None
    return floor_val, ceil_val
''',
            "complexity": "**Time**: *O(log n)*. **Space**: *O(1)*.",
        },
        "thought_process": r'''
Lower bound returns the first index where `arr[i] >= x`. So:

- If `arr[lo] == x`, both floor and ceil are `x` (exact match).
- If `arr[lo] > x`, ceil is `arr[lo]` (smallest greater) and
  floor is `arr[lo - 1]` (largest smaller) if `lo > 0`.
- If `lo == len(arr)`, no value is ≥ x. Ceil is undefined; floor
  is `arr[-1]` (the largest value in the array).
- If `lo == 0` and `arr[0] > x`, floor is undefined; ceil is
  `arr[0]`.

One binary search; constant-time logic for the cases. *O(log n)*
overall.
''',
        "deep_concept": r'''
Yet another query that reduces to lower bound. The pattern:
**any "find the nearest value with property P" query on a
sorted array** is one or two lower/upper bound calls away.

This builds intuition for the family. Soon enough, "floor /
ceil / next-greater / next-smaller / count / first / last"
become reflexive.
''',
        "confusion_notes": [
            {
                "question": "Why does the same lower bound give both floor and ceil?",
                "answer": r'''
Because lower bound finds the "transition point" — the
boundary between elements < x and elements ≥ x. Floor lives
just left of this boundary; ceil lives at it (or to its
right).

If `arr[lo] == x`, both floor and ceil are x (exact match).
Otherwise floor is at `lo - 1` and ceil is at `lo`. One search,
two answers.
''',
            },
        ],
        "summary": "**Pattern**: lower bound + boundary handling = floor and ceil in *O(log n)*.",
    },
    {
        "id": "nth-root",
        "title": "Find the N-th Root of a Number",
        "step_id": 4,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["binary-search", "bs-on-answer", "math"],
        "what_this_teaches": "Generalization of sqrt to N-th root using binary search on the answer.",
        "pattern": "Binary search candidate in [0, m]; predicate is mid^n <= m.",
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["sqrt-using-bs"],
        "next_problems": ["koko-bananas", "smallest-divisor-threshold"],
        "resources": [
            _SHEET,
            {
                "label": "Coding Ninjas — Nth Root",
                "url": "https://www.codingninjas.com/studio/problems/1062679",
            },
        ],
        "understanding": r'''
Given two positive integers `n` and `m`, find the integer N-th
root of `m`. That is, return the largest integer `r` such that
`r^n <= m`. If `r^n == m` exactly, return `r`; otherwise some
problems return `-1` for "no integer root."

Examples:

- `n = 3, m = 27`: 3rd root of 27 is 3 (`3^3 = 27`).
- `n = 4, m = 69`: largest r with r^4 <= 69. `2^4 = 16, 3^4 =
  81`. So r = 2 (no exact root).
- `n = 2, m = 16`: 2nd root (square root) is 4.

The structure is identical to `sqrt-using-bs`, generalized from
2nd root to N-th root.

The brute force tries each candidate from 1 up. *O(m^(1/n))*
time — fewer iterations than for sqrt as n grows, but still
unnecessary.

Optimal: binary search on the candidate `r` in `[1, m]`.
Feasibility predicate: `r^n <= m`. Computing `r^n` takes `O(log
n)` via fast exponentiation, but Python's `**` operator handles
that automatically. Total time `O(log m * log n)`.
''',
        "brute_force": {
            "explanation": "Try each candidate from 1 upward; return the last whose n-th power doesn't exceed m.",
            "code": r'''def nth_root_linear(n: int, m: int) -> int:
    r = 1
    while r ** n <= m:
        r += 1
    return r - 1
''',
            "complexity": "**Time**: *O(m^(1/n))*. **Space**: *O(1)*.",
        },
        "optimized": {
            "explanation": "Binary search the candidate root with predicate r^n <= m.",
            "code": r'''def nth_root(n: int, m: int) -> int:
    # Candidate range: 1 to m (loose upper bound; for n >= 1, the
    # n-th root is at most m).
    lo, hi = 1, m
    ans = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        # Compute mid^n. Python's ** is fast and exact for integers.
        # For very large n, we could early-exit when the partial product
        # exceeds m, but for reasonable inputs Python's ** is fine.
        power = mid ** n
        if power == m:
            # Exact n-th root found.
            return mid
        if power < m:
            # mid is a feasible (but possibly not the largest) root.
            ans = mid
            lo = mid + 1
        else:
            # mid^n exceeds m; try smaller.
            hi = mid - 1
    # If we reached here, no exact root exists. Return the floor.
    # (Some problems require -1 if no exact root; adjust as needed.)
    return ans
''',
            "complexity": "**Time**: *O(log m × log n)*. **Space**: *O(1)*.",
        },
        "thought_process": "Same BS-on-answer recipe as sqrt-using-bs, just with mid^n instead of mid*mid in the predicate.",
        "deep_concept": "Demonstrates that the BS-on-answer pattern is fully parametric in the predicate. Change `mid * mid` to `mid ** n` and the same algorithm works.",
        "confusion_notes": [
            {
                "question": "Why not use math.pow or **(1/n)?",
                "answer": "Floating-point inaccuracy. `m ** (1/n)` can be off by tiny amounts that round wrong when cast to int. The integer-arithmetic binary search is exact.",
            },
        ],
        "summary": "**Pattern**: BS-on-answer with `mid ** n` predicate. Direct generalization of integer sqrt.",
    },
    {
        "id": "min-days-bouquets",
        "title": "Minimum Days to Make M Bouquets",
        "step_id": 4,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["binary-search", "bs-on-answer"],
        "what_this_teaches": "BS-on-answer where the candidate is a 'day count' and the feasibility checker counts how many bouquets we can make using flowers bloomed by that day.",
        "pattern": "Binary search the day in [min, max] of bloomDay; feasibility = count of bouquets makeable by that day >= m.",
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["ship-packages-d-days", "smallest-divisor-threshold"],
        "next_problems": ["aggressive-cows", "painters-partition"],
        "resources": [
            _SHEET,
            _lc(1482, "minimum-number-of-days-to-make-m-bouquets"),
        ],
        "understanding": r'''
You have a garden of `n` flowers; `bloomDay[i]` is the day on
which flower `i` blooms. You need to make `m` bouquets, each
containing exactly `k` **adjacent** bloomed flowers. Return the
minimum number of days required, or `-1` if impossible (not
enough flowers total).

Example: `bloomDay = [1, 10, 3, 10, 2], m = 3, k = 1`. We need
3 bouquets of 1 adjacent flower each. After day 3, the bloomed
flowers (indices where `bloomDay[i] <= 3`) are `[1, _, 3, _,
2]`. The bloomed positions are 0, 2, 4 — three of them. We can
make 3 bouquets of size 1 each. So answer is 3.

**Candidate range** for the day: from `min(bloomDay)` (the
earliest any flower blooms) to `max(bloomDay)` (the latest).

**Feasibility checker**: given a day `d`, count the maximum
number of bouquets makeable. Walk the array; for each bloomed
position (`bloomDay[i] <= d`), extend a "run" counter; every
`k` consecutive bloomed flowers gives one bouquet. Reset the
counter when an unbloomed flower interrupts.

**Monotonicity**: more days → more bloomed flowers → more
bouquets possible. So feasibility is monotonic in days. We
want the smallest feasible day.

**Binary search**: half-open lower-bound style.
''',
        "brute_force": {
            "explanation": "Try each day from min to max; count bouquets makeable.",
            "code": r'''def min_days_linear(bloomDay, m, k):
    if m * k > len(bloomDay):
        return -1
    for d in range(min(bloomDay), max(bloomDay) + 1):
        if can_make(bloomDay, d, k) >= m:
            return d
    return -1


def can_make(bloomDay, d, k):
    bouquets = 0
    run = 0
    for b in bloomDay:
        if b <= d:
            run += 1
            if run == k:
                bouquets += 1
                run = 0
        else:
            run = 0
    return bouquets
''',
            "complexity": "**Time**: *O((max - min) × n)*. **Space**: *O(1)*.",
        },
        "optimized": {
            "explanation": "Binary search the day with a greedy bouquet-counting feasibility checker.",
            "code": r'''def min_days(bloomDay: list[int], m: int, k: int) -> int:
    # Quick infeasibility check: need m*k flowers total.
    if m * k > len(bloomDay):
        return -1

    def can_make(d: int) -> int:
        # Count the maximum number of bouquets makeable by day d.
        # Walk the array; extend a run of bloomed flowers; harvest a
        # bouquet whenever the run reaches k.
        bouquets = 0
        run = 0
        for b in bloomDay:
            if b <= d:
                # This flower has bloomed by day d.
                run += 1
                if run == k:
                    bouquets += 1
                    run = 0  # reset; start a new run
            else:
                # Unbloomed; the run is broken.
                run = 0
        return bouquets

    # Candidate range: min(bloomDay) to max(bloomDay).
    lo, hi = min(bloomDay), max(bloomDay)
    while lo < hi:
        mid = (lo + hi) // 2
        if can_make(mid) >= m:
            # Feasible at this day; try earlier.
            hi = mid
        else:
            # Not enough bouquets; need later.
            lo = mid + 1
    return lo
''',
            "complexity": "**Time**: *O(n × log(max - min))*. **Space**: *O(1)*.",
        },
        "thought_process": "Same BS-on-answer recipe: identify candidate (the day), write feasibility checker (greedy bouquet count), verify monotonicity (more days = more bouquets), binary search.",
        "deep_concept": "The greedy 'harvest bouquets eagerly as runs reach k' is optimal because adjacent bloomed flowers must be used contiguously; delaying a harvest never helps.",
        "confusion_notes": [
            {
                "question": "Why reset `run` to 0 after harvesting a bouquet?",
                "answer": "Because each flower can only be used once. After harvesting k flowers into a bouquet, those flowers are 'spent' and the next bouquet must come from the next run.",
            },
            {
                "question": "Why is the infeasibility check `m * k > len(bloomDay)`?",
                "answer": "We need `m * k` flowers total to make `m` bouquets of size `k`. If the garden has fewer than that, no day count will work — return -1.",
            },
        ],
        "summary": "**Pattern**: BS-on-answer with greedy run-counting feasibility checker.",
    },
    {
        "id": "kth-missing-positive",
        "title": "K-th Missing Positive Number",
        "step_id": 4,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["binary-search", "arrays"],
        "what_this_teaches": "How to binary search using the count of missing positives up to each index — a clever transformation that turns 'find the k-th missing' into a lower-bound query.",
        "pattern": "Missing count at index i = arr[i] - (i + 1). Binary search for the first index where missing count >= k.",
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["lower-bound", "binary-search"],
        "next_problems": ["sqrt-using-bs"],
        "resources": [
            _SHEET,
            _lc(1539, "kth-missing-positive-number"),
        ],
        "understanding": r'''
Given a strictly-increasing array of positive integers and an
integer `k`, return the k-th **missing** positive integer.

For `arr = [2, 3, 4, 7, 11]`:
- The positive integers not in `arr`: 1, 5, 6, 8, 9, 10, 12, 13, ...
- The 5th missing positive is 9.

The brute force walks 1, 2, 3, ... and counts how many are
missing until k. *O(arr[-1] + k)*.

The clever optimization: notice that at index `i`, the number
of "missing" positive integers up to (and not including)
`arr[i]` is `arr[i] - (i + 1)`. (Because if no numbers were
missing, `arr[i]` would equal `i + 1`. Every extra is a missing
slot.)

So we binary search for the smallest index where
`arr[i] - (i + 1) >= k`. The answer is `k + i` (the k-th missing
sits just before `arr[i]`, at position `arr[i] - (count above i)`).
Or more precisely: the answer is `k + lo` after the binary
search, where `lo` is the lower bound.
''',
        "brute_force": {
            "explanation": "Walk positive integers in order; skip the ones in arr; count to k.",
            "code": r'''def kth_missing_linear(arr, k):
    missing = 0
    i = 0
    num = 0
    while True:
        num += 1
        if i < len(arr) and arr[i] == num:
            i += 1
        else:
            missing += 1
            if missing == k:
                return num
''',
            "complexity": "**Time**: *O(arr[-1] + k)*. **Space**: *O(1)*.",
        },
        "optimized": {
            "explanation": "Binary search on the 'missing count' function. At index i, missing = arr[i] - (i + 1).",
            "code": r'''def find_kth_missing(arr: list[int], k: int) -> int:
    # Binary search for the smallest index i where the number of
    # missing positives up to arr[i] is at least k.
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        # missing[mid] = arr[mid] - (mid + 1).
        # If this is < k, the k-th missing is past arr[mid]: lo = mid + 1.
        # Otherwise, the k-th missing is at or before arr[mid]: hi = mid.
        missing_count = arr[mid] - (mid + 1)
        if missing_count < k:
            lo = mid + 1
        else:
            hi = mid
    # After the search, lo is the first index where missing >= k.
    # The k-th missing positive is k + lo.
    # (If lo == len(arr), all of arr's elements have been considered;
    # the k-th missing is k + lo = k + len(arr).)
    return k + lo
''',
            "complexity": "**Time**: *O(log n)*. **Space**: *O(1)*.",
        },
        "thought_process": r'''
The transformation `missing(i) = arr[i] - (i + 1)` is the
clever step. Let me unpack it.

If `arr` were `[1, 2, 3, ..., n]` with no missing values, then
`arr[i] == i + 1` for all `i`, so missing(i) = 0.

Every time a positive integer is "skipped" (i.e., not in `arr`),
the values shift up. `arr[i]` becomes larger than `i + 1` by
exactly the number of values missing before `arr[i]`.

So `arr[i] - (i + 1) = number of missing positives less than
arr[i]`.

We want the **k-th** missing. Binary-search the smallest `i`
such that `missing(i) >= k`. Once found, the k-th missing is
sandwiched between `arr[i - 1]` and `arr[i]`. Working out the
arithmetic: the answer is `k + lo` (the lower bound returned).

This kind of "transform the data and binary search the
transform" trick is one of the prettiest patterns in DSA.
''',
        "deep_concept": "The transformation `arr[i] - (i + 1) = number of missing positives < arr[i]` is the heart of the algorithm. Recognizing such transformations turns linear scans into logarithmic searches.",
        "confusion_notes": [
            {
                "question": "Why is the answer `k + lo`?",
                "answer": "Because `lo` is the smallest index where `missing(lo) >= k`. Before index `lo`, `missing(lo - 1) < k`. So the k-th missing positive lies just past `arr[lo - 1]`, at position `k + lo`.",
            },
        ],
        "summary": "**Pattern**: transform the data so that 'find the k-th missing' becomes 'find the lower bound of missing-count'. Then binary search.",
    },
    {
        "id": "split-array-largest-sum",
        "title": "Split Array Largest Sum",
        "step_id": 4,
        "lecture_id": 2,
        "difficulty": "hard",
        "tags": ["binary-search", "bs-on-answer", "partition"],
        "what_this_teaches": "The same algorithm as book-allocation, painter's partition, and ship-packages-in-D-days, framed as 'split array into k contiguous subarrays minimizing the maximum sum'.",
        "pattern": "Binary search the candidate max sum in [max(arr), sum(arr)]; greedy subarray-counting feasibility checker.",
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["book-allocation", "ship-packages-d-days", "aggressive-cows"],
        "next_problems": ["painters-partition", "minimize-max-distance"],
        "resources": [
            _SHEET,
            _lc(410, "split-array-largest-sum"),
        ],
        "understanding": r'''
Given an array `nums` of non-negative integers and an integer
`k`, split `nums` into `k` **non-empty contiguous** subarrays
such that the largest subarray sum is minimized. Return that
minimized maximum.

Example: `nums = [7, 2, 5, 10, 8]`, `k = 2`. Possible splits:

- `[7] | [2, 5, 10, 8]`: sums 7, 25. Max 25.
- `[7, 2] | [5, 10, 8]`: 9, 23. Max 23.
- `[7, 2, 5] | [10, 8]`: 14, 18. Max 18.
- `[7, 2, 5, 10] | [8]`: 24, 8. Max 24.

Minimum of the maxes: 18.

This is **algorithmically identical to book-allocation** with
"subarrays" playing the role of "students" and "sums" of
"page totals." The same BS-on-answer recipe with greedy
partition checker applies directly.
''',
        "brute_force": {
            "explanation": "Enumerate all C(n-1, k-1) partitions. Infeasible for large inputs.",
            "code": r'''# Combinatorial brute force; not recommended.
def split_brute(nums, k):
    # Try all positions to insert k-1 split points.
    # Infeasible for large k; included only as a baseline.
    from itertools import combinations
    n = len(nums)
    best = float('inf')
    for splits in combinations(range(1, n), k - 1):
        groups = []
        prev = 0
        for s in list(splits) + [n]:
            groups.append(sum(nums[prev:s]))
            prev = s
        best = min(best, max(groups))
    return best
''',
            "complexity": "**Time**: *O(C(n-1, k-1) × n)*. Astronomically slow. **Space**: *O(k)*.",
        },
        "optimized": {
            "explanation": "Binary search the candidate max-sum; greedy partition checker counts how many subarrays are needed.",
            "code": r'''def split_array(nums: list[int], k: int) -> int:
    def partitions_needed(max_sum: int) -> int:
        # Greedy: extend the current subarray until adding the next
        # element would exceed max_sum; then start a new subarray.
        groups = 1
        current = 0
        for x in nums:
            if x > max_sum:
                # Even a single element exceeds the cap. Infeasible.
                return float('inf')
            if current + x <= max_sum:
                current += x
            else:
                groups += 1
                current = x
        return groups

    # Candidate range:
    # - Lower bound max(nums): no subarray can sum to less than its
    #   largest single element.
    # - Upper bound sum(nums): with k=1, the only subarray takes
    #   everything.
    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if partitions_needed(mid) <= k:
            # mid is feasible (we can do it with k or fewer subarrays).
            # Try smaller.
            hi = mid
        else:
            # Need more capacity per subarray.
            lo = mid + 1
    return lo
''',
            "complexity": "**Time**: *O(n × log(sum - max))*. **Space**: *O(1)*.",
        },
        "thought_process": "Same recipe as book-allocation, frame-renamed. The greedy 'extend current group until cap' is optimal by the exchange argument we covered there.",
        "deep_concept": "This problem is the 'canonical' LeetCode formulation of the partition family. Once you've solved book-allocation, this is the same algorithm with renamed variables.",
        "confusion_notes": [
            {
                "question": "Is this really the same problem as book-allocation?",
                "answer": "Yes — algorithmically identical. Book-allocation says 'distribute books to students in order, minimize max pages per student'. Split-array-largest-sum says 'split array into k contiguous subarrays, minimize max sum'. They are word-for-word the same partition problem with different stories.",
            },
        ],
        "summary": "**Pattern**: BS-on-answer with greedy partition checker. Same as book-allocation, ship-packages, painter's partition.",
    },
    {
        "id": "painters-partition",
        "title": "Painter's Partition Problem",
        "step_id": 4,
        "lecture_id": 2,
        "difficulty": "hard",
        "tags": ["binary-search", "bs-on-answer", "partition"],
        "what_this_teaches": "Yet another framing of the partition family. Painters paint boards in order; minimize the time the slowest painter takes.",
        "pattern": "Same as book-allocation / split-array-largest-sum / ship-packages.",
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["split-array-largest-sum", "book-allocation"],
        "next_problems": ["minimize-max-distance"],
        "resources": [
            _SHEET,
            {
                "label": "GFG — Painter's Partition Problem",
                "url": "https://www.geeksforgeeks.org/painters-partition-problem/",
            },
        ],
        "understanding": r'''
You have `k` painters and `n` boards (in order) with lengths
given. Each painter paints one or more **adjacent** boards.
Painting one unit of length takes one unit of time. All
painters work in parallel. Minimize the time when **the slowest
painter finishes** (i.e., when all boards are done).

This is **exactly** split-array-largest-sum and book-allocation,
with painters as the partitions and board lengths as the
weights.

The minimized maximum subarray sum = the time the slowest
painter takes = the time all boards are done.

Algorithm is identical to those problems.
''',
        "brute_force": {
            "explanation": "Enumerate all partitions. Infeasible.",
            "code": "# Same as split_brute; omitted.\n",
            "complexity": "Astronomical.",
        },
        "optimized": {
            "explanation": "Identical algorithm to split-array-largest-sum.",
            "code": r'''def painters_partition(boards: list[int], k: int) -> int:
    def painters_needed(max_time: int) -> int:
        painters = 1
        current = 0
        for length in boards:
            if length > max_time:
                return float('inf')
            if current + length <= max_time:
                current += length
            else:
                painters += 1
                current = length
        return painters

    lo, hi = max(boards), sum(boards)
    while lo < hi:
        mid = (lo + hi) // 2
        if painters_needed(mid) <= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
''',
            "complexity": "**Time**: *O(n × log(sum - max))*. **Space**: *O(1)*.",
        },
        "thought_process": "Same as split-array-largest-sum.",
        "deep_concept": "The partition family is broad. Once you recognize 'minimize the max partition sum / cost / time', the algorithm is mechanical.",
        "confusion_notes": [
            {
                "question": "What's the difference between painter's partition and book-allocation?",
                "answer": "Nothing algorithmic. Different stories, same problem. Both minimize the max sum across k contiguous partitions.",
            },
        ],
        "summary": "**Pattern**: same partition family. Painter / student / day / subarray — all interchangeable framings.",
    },
    {
        "id": "minimize-max-distance",
        "title": "Minimize Maximum Distance to Gas Station",
        "step_id": 4,
        "lecture_id": 2,
        "difficulty": "hard",
        "tags": ["binary-search", "bs-on-answer", "heap"],
        "what_this_teaches": "BS-on-answer where the candidate is a real-valued distance and the feasibility checker counts how many new stations are needed to keep the max gap under the candidate.",
        "pattern": "Real-valued binary search: lo, hi as floats; converge by tolerance instead of integer equality.",
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["aggressive-cows", "split-array-largest-sum"],
        "next_problems": ["median-two-sorted"],
        "resources": [
            _SHEET,
            _lc(774, "minimize-max-distance-to-gas-station"),
        ],
        "understanding": r'''
You have gas stations at sorted positions `stations[0] <
stations[1] < ... < stations[n-1]`. You can add `k` new
stations at any positions. Minimize the **maximum** distance
between any two adjacent stations.

Return the minimum possible max-distance as a float (rounded to
some precision).

Example: `stations = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`, `k = 9`.
Add 9 stations. The current gaps are all 1. Adding one station
splits a gap of 1 into two halves of 0.5. With 9 new stations,
we can split 9 gaps in half (or distribute differently). The
answer is 0.5.

**Real-valued binary search**: the candidate answer is a
positive real number, not an integer. We use a binary search
with floating-point bounds, converging when `hi - lo` is
smaller than some tolerance (typically `1e-6`).

**Feasibility checker**: given a candidate max-distance `d`,
count how many new stations are needed to ensure no gap exceeds
`d`. For each existing gap `g_i`, we need `ceil(g_i / d) - 1`
new stations. Sum these. Feasible iff sum ≤ k.

**Monotonicity**: smaller `d` → more stations needed.
Feasibility is monotonic in `d`.

**Binary search**: find the smallest feasible `d`. Use a real-
valued binary search with a tolerance.
''',
        "brute_force": {
            "explanation": "There's no clean integer enumeration. The brute force is the heap-based greedy that places stations one at a time in the largest gap. *O(k log n)* but doesn't generalize cleanly.",
            "code": r'''import heapq

def minimize_max_dist_heap(stations, k):
    # Max-heap of gaps; place each new station in the current largest.
    heap = []
    for i in range(len(stations) - 1):
        gap = stations[i + 1] - stations[i]
        heapq.heappush(heap, (-gap, 1))  # (-priority, parts so far)
    for _ in range(k):
        neg_g, parts = heapq.heappop(heap)
        g = -neg_g * parts / (parts + 1)
        heapq.heappush(heap, (-g, parts + 1))
    return -heap[0][0]
''',
            "complexity": "**Time**: *O((n + k) log n)*. **Space**: *O(n)*.",
        },
        "optimized": {
            "explanation": "Real-valued binary search on the candidate max-distance.",
            "code": r'''def minimize_max_distance(stations: list[int], k: int, tol: float = 1e-6) -> float:
    import math

    def stations_needed(d: float) -> int:
        # For each existing gap, count how many new stations are needed
        # to keep all sub-gaps <= d. A gap of g needs ceil(g / d) - 1
        # new stations (subtract 1 because one fewer split-point gives
        # ceil(g/d) parts).
        total = 0
        for i in range(len(stations) - 1):
            g = stations[i + 1] - stations[i]
            total += math.ceil(g / d) - 1
        return total

    lo, hi = 0.0, max(stations[i + 1] - stations[i]
                      for i in range(len(stations) - 1))
    # Real-valued binary search. Terminate when the window is smaller
    # than the tolerance.
    while hi - lo > tol:
        mid = (lo + hi) / 2
        if stations_needed(mid) <= k:
            # Feasible at this max-distance; try smaller.
            hi = mid
        else:
            # Need more stations than available; try larger.
            lo = mid
    return lo
''',
            "complexity": "**Time**: *O(n × log((max_gap) / tol))*. **Space**: *O(1)*.",
        },
        "thought_process": "Real-valued binary search has the same shape as integer binary search; we just use floats and a tolerance for the termination condition.",
        "deep_concept": "Real-valued binary search is rarely emphasized but appears in geometric and continuous-optimization problems. The tolerance-based convergence replaces integer equality.",
        "confusion_notes": [
            {
                "question": "Why tolerance-based convergence?",
                "answer": "Because floats can never reach exact equality. We stop when the window `hi - lo` is smaller than our acceptable error. Typical tolerance: `1e-6` or `1e-7` depending on the problem's required precision.",
            },
        ],
        "summary": "**Pattern**: real-valued binary search with tolerance termination. The feasibility checker uses ceiling-division on gap lengths.",
    },
    {
        "id": "kth-element-two-sorted",
        "title": "K-th Element of Two Sorted Arrays",
        "step_id": 4,
        "lecture_id": 2,
        "difficulty": "hard",
        "tags": ["binary-search", "partition"],
        "what_this_teaches": "Generalization of median-two-sorted: find the k-th smallest of the merged sequence. Same partition idea, different half-size.",
        "pattern": "Binary search the partition; half-size = k.",
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["median-two-sorted"],
        "next_problems": [],
        "resources": [
            _SHEET,
            {
                "label": "GFG — k-th element of two sorted arrays",
                "url": "https://www.geeksforgeeks.org/k-th-element-two-sorted-arrays/",
            },
        ],
        "understanding": r'''
Given two sorted arrays and an integer `k`, return the k-th
smallest element of the merged sequence.

This is the generalization of median-two-sorted. The median is
the `(m + n + 1) // 2`-th element; the general problem asks for
the k-th.

The brute force merges the two arrays and reads the k-th. *O((m
+ n) log(m + n))* with sort, or *O(m + n)* with two-pointer
merge (stopping at the k-th).

The optimal *O(log(min(m, n)))* algorithm uses the same
partition trick as median-two-sorted, with `half = k` instead of
`(m + n + 1) // 2`.
''',
        "brute_force": {
            "explanation": "Two-pointer merge until the k-th element.",
            "code": r'''def kth_element_brute(a, b, k):
    i = j = 0
    last = 0
    for _ in range(k):
        if i < len(a) and (j == len(b) or a[i] <= b[j]):
            last = a[i]
            i += 1
        else:
            last = b[j]
            j += 1
    return last
''',
            "complexity": "**Time**: *O(k)*. **Space**: *O(1)*.",
        },
        "optimized": {
            "explanation": "Partition-based binary search with half=k.",
            "code": r'''def kth_element(a: list[int], b: list[int], k: int) -> int:
    # Binary search the smaller array; ensure m <= n.
    if len(a) > len(b):
        a, b = b, a
    m, n = len(a), len(b)
    # Restrict the binary search range on i (the cut in array a) to
    # the valid window given k. i must be at least max(0, k - n) and
    # at most min(k, m).
    lo = max(0, k - n)
    hi = min(k, m)
    while lo <= hi:
        i = (lo + hi) // 2
        j = k - i
        # Boundary elements at the cut. Use sentinels for out-of-bounds.
        a_left = a[i - 1] if i > 0 else float('-inf')
        a_right = a[i] if i < m else float('inf')
        b_left = b[j - 1] if j > 0 else float('-inf')
        b_right = b[j] if j < n else float('inf')
        # Check the cross condition.
        if a_left <= b_right and b_left <= a_right:
            # The k-th element is the max of the left side.
            return max(a_left, b_left)
        elif a_left > b_right:
            hi = i - 1
        else:
            lo = i + 1
    raise ValueError("inputs not sorted")
''',
            "complexity": "**Time**: *O(log(min(m, n)))*. **Space**: *O(1)*.",
        },
        "thought_process": "Same as median-two-sorted, with `half = k`.",
        "deep_concept": "Demonstrates that the partition-based binary search generalizes from median to arbitrary k-th smallest.",
        "confusion_notes": [
            {
                "question": "Why restrict the search range on i?",
                "answer": "Because j = k - i must be in [0, n]. So i must be at least k - n (so j <= n) and at most k (so j >= 0). The tighter range avoids invalid partitions.",
            },
        ],
        "summary": "**Pattern**: partition-based binary search; half = k.",
    },
    {
        "id": "peak-element-2d",
        "title": "Find Peak Element in a 2D Matrix",
        "step_id": 4,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["binary-search", "matrix", "peaks"],
        "what_this_teaches": "Binary search on columns. For each candidate column, find the row of its max; then check whether that cell is a peak by comparing horizontally.",
        "pattern": "Binary search columns; check the max of the chosen column against its horizontal neighbors.",
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["find-peak-element", "search-2d-matrix"],
        "next_problems": ["matrix-median"],
        "resources": [
            _SHEET,
            _lc(1901, "find-a-peak-element-ii"),
        ],
        "understanding": r'''
Given a 2D matrix where no two adjacent cells are equal, find
any **peak element** — a cell strictly greater than all four
of its neighbors (with boundary cells comparing only to existing
neighbors).

The algorithm: binary search the columns. For each candidate
column `mid`, find the row index of its maximum value (one
linear scan, *O(m)*). The cell at `(max_row, mid)` is greater
than its vertical neighbors (since it's the column max).
Compare it with its horizontal neighbors. If it's greater than
both, it's a peak. Otherwise, move toward the larger horizontal
neighbor.

Why does this work? Because moving toward the larger neighbor
keeps a "ridge of locally large values" that must eventually
contain a peak. The argument is similar to the 1D peak
algorithm.

Time: *O(m log n)* (binary search on columns, linear scan per
column).
''',
        "brute_force": {
            "explanation": "Check every cell against its neighbors.",
            "code": r'''def peak_brute(matrix):
    m, n = len(matrix), len(matrix[0])
    for i in range(m):
        for j in range(n):
            ok = True
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and matrix[ni][nj] > matrix[i][j]:
                    ok = False
                    break
            if ok:
                return [i, j]
    return [-1, -1]
''',
            "complexity": "**Time**: *O(m × n)*. **Space**: *O(1)*.",
        },
        "optimized": {
            "explanation": "Binary search on columns; pick row by column max; move toward larger neighbor.",
            "code": r'''def find_peak_grid(matrix: list[list[int]]) -> list[int]:
    m, n = len(matrix), len(matrix[0])
    lo, hi = 0, n - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        # Find the row with the max value in column mid.
        max_row = 0
        for i in range(m):
            if matrix[i][mid] > matrix[max_row][mid]:
                max_row = i
        # Compare with horizontal neighbors.
        left_val = matrix[max_row][mid - 1] if mid > 0 else float('-inf')
        right_val = matrix[max_row][mid + 1] if mid < n - 1 else float('-inf')
        if matrix[max_row][mid] > left_val and matrix[max_row][mid] > right_val:
            return [max_row, mid]
        elif left_val > matrix[max_row][mid]:
            hi = mid - 1
        else:
            lo = mid + 1
    return [-1, -1]
''',
            "complexity": "**Time**: *O(m log n)*. **Space**: *O(1)*.",
        },
        "thought_process": "Binary search on columns instead of values. The 'max of the column' guarantees the chosen cell beats its vertical neighbors; we only check horizontally.",
        "deep_concept": "Generalizes 1D peak search to 2D. The key: pick a structural axis (columns) to binary search, and reduce the other dimension by argmax.",
        "confusion_notes": [
            {
                "question": "Why is the column max guaranteed to be greater than its vertical neighbors?",
                "answer": "By definition. The max of a column is at least as large as every other element in that column, including the cell directly above and below. Since the problem says no two adjacent cells are equal, the max is strictly greater.",
            },
        ],
        "summary": "**Pattern**: binary search on one matrix dimension; linear argmax on the other.",
    },
    {
        "id": "matrix-median",
        "title": "Median of a Sorted Matrix",
        "step_id": 4,
        "lecture_id": 3,
        "difficulty": "hard",
        "tags": ["binary-search", "matrix"],
        "what_this_teaches": "BS-on-answer where the candidate is the median value and the feasibility checker counts how many elements are <= that value.",
        "pattern": "Binary search the value in [matrix min, matrix max]; count elements <= mid using row-wise binary search.",
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["search-2d-matrix-ii", "upper-bound"],
        "next_problems": [],
        "resources": [
            _SHEET,
            {
                "label": "GFG — Median in a row-wise sorted Matrix",
                "url": "https://www.geeksforgeeks.org/find-median-row-wise-sorted-matrix/",
            },
        ],
        "understanding": r'''
Given an `m × n` matrix where each row is sorted, find the
median of all `m × n` elements. The total count `m × n` is
odd, so the median is well-defined as the `(m × n + 1) // 2`-th
element.

The brute force: flatten the matrix, sort, return the middle.
*O(mn log(mn))*.

A better approach: use a heap to merge-sort the rows and stop
at the middle. *O(mn log m)*.

The optimal: **binary search the median value**. The candidate
range is `[min, max]` of the matrix. For each candidate `v`,
count how many elements are `<= v` using row-wise upper bound
(*O(m log n)*). If count >= the target, `v` is at or past the
median; else not.

Total time: *O(m log n × log(max - min))*.

This is BS-on-answer with a row-wise count as the feasibility
checker.
''',
        "brute_force": {
            "explanation": "Flatten, sort, return middle.",
            "code": r'''def matrix_median_brute(matrix):
    flat = [v for row in matrix for v in row]
    flat.sort()
    return flat[len(flat) // 2]
''',
            "complexity": "**Time**: *O(mn log(mn))*. **Space**: *O(mn)*.",
        },
        "optimized": {
            "explanation": "Binary search the median value; row-wise upper-bound count as feasibility checker.",
            "code": r'''def matrix_median(matrix: list[list[int]]) -> int:
    import bisect
    m, n = len(matrix), len(matrix[0])
    # Candidate range: matrix min to matrix max.
    lo = min(row[0] for row in matrix)
    hi = max(row[-1] for row in matrix)
    # We want the (m*n+1)//2-th smallest element (the median).
    target = (m * n + 1) // 2
    while lo < hi:
        mid = (lo + hi) // 2
        # Count elements <= mid using row-wise upper bound.
        # bisect_right gives the count of values <= mid in each row.
        count = sum(bisect.bisect_right(row, mid) for row in matrix)
        if count < target:
            # Not enough elements <= mid; the median is larger.
            lo = mid + 1
        else:
            # Enough; the median is at or below mid.
            hi = mid
    return lo
''',
            "complexity": "**Time**: *O(m log n × log(max - min))*. **Space**: *O(1)*.",
        },
        "thought_process": "BS-on-answer for the value rather than the index. The feasibility checker counts how many elements are at most the candidate.",
        "deep_concept": "A classic example of binary searching the *value space* of the matrix rather than the index space.",
        "confusion_notes": [
            {
                "question": "Why is the answer `lo` and not the value found at `mid`?",
                "answer": "Because the binary search converges to the smallest value v such that at least `target` elements are <= v. That value is exactly the median.",
            },
        ],
        "summary": "**Pattern**: BS-on-answer on the value space; row-wise upper bound for the feasibility count.",
    },
    {
        "id": "first-last-occurrence",
        "title": "First and Last Occurrence in a Sorted Array",
        "step_id": 4,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["binary-search", "fundamentals"],
        "what_this_teaches": (
            "Two binary searches in sequence — lower bound for first "
            "occurrence, upper bound minus one for last. The "
            "canonical example of composing the atomic operations."
        ),
        "pattern": "first = lower_bound(x); last = upper_bound(x) - 1.",
        "prerequisite_lessons": ["arrays", "searching"],
        "prerequisite_problems": ["lower-bound", "upper-bound", "search-insert-position"],
        "next_problems": ["count-occurrences", "search-rotated-i"],
        "resources": [
            _SHEET,
            _lc(34, "find-first-and-last-position-of-element-in-sorted-array"),
        ],
        "understanding": r'''
Given a sorted array `arr` and a target `x`, return the first
and last positions where `x` appears. If `x` is not in the
array, return `[-1, -1]`.

The LeetCode 34 version requires `O(log n)` time. So a brute
linear scan, while correct, is not the optimal solution we
want to study.

Examples on `arr = [5, 7, 7, 8, 8, 10]`:

- `target = 8`: return `[3, 4]`.
- `target = 6`: return `[-1, -1]` (not present).
- `target = 10`: return `[5, 5]` (single occurrence).
- `target = 7`: return `[1, 2]`.

The natural approach: two binary searches. One finds the first
occurrence; the other finds the last.

For the **first occurrence**, the right tool is **lower bound**.
Lower bound returns the first index whose value is *at least*
the target. If `arr[lower_bound]` equals the target, that
index is the first occurrence. If it equals something else (or
lower bound is past the end), the target is absent.

For the **last occurrence**, the right tool is **upper bound
minus one**. Upper bound returns the first index whose value is
*strictly greater* than the target. Subtracting one gives the
last index whose value is at most the target. If that value
equals the target, it's the last occurrence; otherwise the
target is absent.

Two `O(log n)` searches gives a total of `O(log n)`. Optimal.

This problem is the canonical demonstration of "compose lower
and upper bound to answer richer queries." Internalize it.
''',
        "brute_force": {
            "explanation": r'''
Linear scan twice (or once with two variables). Find the first
index where `arr[i] == x`, find the last.

```python
def first_last_linear(arr, x):
    first = last = -1
    for i, v in enumerate(arr):
        if v == x:
            if first == -1:
                first = i
            last = i
    return [first, last]
```

`O(n)` time. Correct on any array, sorted or not.

The interview challenge requires `O(log n)`, so this brute force
is below the bar. But it's worth writing first to confirm
correctness — your `O(log n)` binary-search version can be
validated against it on small inputs.
''',
            "code": r'''def first_last_linear(arr: list[int], x: int) -> list[int]:
    # Track the first and last indices where x appears. Initialize
    # to -1 to signal "not yet seen."
    first = -1
    last = -1
    # Walk the array once.
    for i, v in enumerate(arr):
        if v == x:
            # First time we see x, record its index.
            if first == -1:
                first = i
            # Every time we see x, update the last-seen index. By
            # the end of the loop, this is the actual last occurrence.
            last = i
    # Return as a list, matching the LeetCode 34 signature.
    return [first, last]
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "thought_process": r'''
The optimal approach uses two binary searches.

**First occurrence**: lower bound. Lower bound on `arr` for the
target returns the first index whose value is at least the
target. If that value is exactly the target, it's the first
occurrence. If it's something else (e.g., 9 when we wanted 8),
the target is absent — return -1 for both first and last.

**Last occurrence**: upper bound minus 1. Upper bound returns
the first index whose value is *strictly greater* than the
target. So `upper_bound - 1` is the last index whose value is
at most the target. If `arr[upper_bound - 1]` equals the
target, it's the last occurrence.

A nice property: if lower bound found the target, upper bound is
guaranteed to be greater than lower bound (because the target
appears at least once between them). So the subtraction is
safe.

Conversely, if lower bound did not find the target (i.e.,
`arr[lower_bound] != target`), there's no need to compute upper
bound — we already know the answer is `[-1, -1]`. This is a
small optimization but it doesn't change the asymptotic
complexity.

Worked example on `arr = [5, 7, 7, 8, 8, 10]`, `target = 8`:

- `lower_bound(arr, 8)`:
  - `lo = 0, hi = 6, mid = 3, arr[3] = 8`. `8 >= 8`? Yes.
    `hi = 3`.
  - `lo = 0, hi = 3, mid = 1, arr[1] = 7`. `7 >= 8`? No.
    `lo = 2`.
  - `lo = 2, hi = 3, mid = 2, arr[2] = 7`. `7 >= 8`? No.
    `lo = 3`.
  - `lo = 3, hi = 3`. Exit. Return `3`.
- `upper_bound(arr, 8)`:
  - `lo = 0, hi = 6, mid = 3, arr[3] = 8`. `8 > 8`? No.
    `lo = 4`.
  - `lo = 4, hi = 6, mid = 5, arr[5] = 10`. `10 > 8`? Yes.
    `hi = 5`.
  - `lo = 4, hi = 5, mid = 4, arr[4] = 8`. `8 > 8`? No.
    `lo = 5`.
  - `lo = 5, hi = 5`. Exit. Return `5`.
- `arr[3] == 8` ✓, so first = 3.
- last = `upper_bound - 1 = 4`.
- Return `[3, 4]`.

For absent targets, the lower bound check fails and we return
`[-1, -1]`.
''',
        "optimized": {
            "explanation": r'''
Two half-open binary searches. The first finds the lower bound
of the target; the second finds the upper bound. Return based
on whether the lower bound actually points to the target.
''',
            "code": r'''def search_range(arr: list[int], target: int) -> list[int]:
    # Helper: lower bound. First index with arr[i] >= target.
    def lower_bound(target):
        lo, hi = 0, len(arr)
        while lo < hi:
            mid = (lo + hi) // 2
            if arr[mid] >= target:
                hi = mid
            else:
                lo = mid + 1
        return lo

    # Helper: upper bound. First index with arr[i] > target.
    def upper_bound(target):
        lo, hi = 0, len(arr)
        while lo < hi:
            mid = (lo + hi) // 2
            if arr[mid] > target:
                hi = mid
            else:
                lo = mid + 1
        return lo

    # Compute the first candidate for the first occurrence.
    first = lower_bound(target)
    # If first is past the end, or the value at first isn't the
    # target, then the target isn't in the array at all. Return
    # the not-found sentinel.
    if first == len(arr) or arr[first] != target:
        return [-1, -1]
    # The target is present. The last occurrence is upper_bound - 1.
    last = upper_bound(target) - 1
    # Return both as a list, matching the LeetCode signature.
    return [first, last]
''',
            "complexity": (
                "**Time**: *O(log n)*. Two binary searches, each "
                "*O(log n)*; the sum is *O(log n)*.\n\n"
                "**Space**: *O(1)*. Just a few integer variables."
            ),
        },
        "deep_concept": r'''
This problem is the cleanest demonstration of "compose atomic
operations to answer richer queries." Lower bound finds the
first occurrence. Upper bound finds one past the last. Together
they bracket the run of duplicates.

The number of occurrences of x is `upper_bound(x) -
lower_bound(x)`. That single formula answers a third common
query for free.

A nice property emerges from this composition: **the run of
duplicates of `x` in a sorted array is exactly the range
`[lower_bound(x), upper_bound(x))`**. The range is half-open,
so `upper_bound(x)` is one past the last copy. The count is the
range length, which is `upper_bound - lower_bound`.

Half-open ranges are the natural format for "groups of
duplicates." They behave nicely with arithmetic (you can
subtract endpoints to get the count) and they avoid the
"off-by-one for the closing boundary" trap.

Once you internalize "first occurrence is lower bound; last
occurrence is upper bound minus one; count is the difference,"
you have unlocked an entire family of sorted-array queries with
two underlying binary searches.
''',
        "confusion_notes": [
            {
                "question": "Why two separate binary searches? Can't I do one?",
                "answer": r'''
You can — but it's harder to write correctly and saves only a
constant factor.

The "one binary search" version finds *any* occurrence first,
then expands outward to find the boundaries:

```python
def search_range_one(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            # Expand outward.
            l, r = mid, mid
            while l > 0 and arr[l - 1] == target:
                l -= 1
            while r < len(arr) - 1 and arr[r + 1] == target:
                r += 1
            return [l, r]
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return [-1, -1]
```

The expansion can be linear in the worst case (when the target
fills most of the array), so this version is `O(n)` in the
worst case. Worse than the two-binary-search version.

To make the one-search version `O(log n)`, you'd have to
binary-search the boundaries — and that's exactly what two
separate binary searches do.

So two `O(log n)` searches is the cleanest implementation. The
"one search" version is either incorrect-on-complexity or
syntactically equivalent to two searches.

For interview clarity, write the two-search version. It's
shorter, easier to reason about, and demonstrably `O(log n)`.
''',
            },
            {
                "question": "What if the array has only the target value, like `[3, 3, 3, 3]`?",
                "answer": r'''
The algorithm handles it correctly.

For `arr = [3, 3, 3, 3]` and `target = 3`:

- `lower_bound(3)`: returns 0 (first index where value ≥ 3 is
  index 0).
- `upper_bound(3)`: returns 4 (first index where value > 3 is
  past the end).
- first = 0; check `arr[0] == 3`. ✓
- last = `upper_bound - 1 = 3`.
- Return `[0, 3]`.

The full range. Correct.

This is the case where lower bound and upper bound are at
opposite ends of the array — the longest possible run of
duplicates. The algorithm is robust to it because the half-open
representation handles "one past the end" naturally.
''',
            },
            {
                "question": "What does the answer look like when the target is present exactly once?",
                "answer": r'''
First and last are the same index.

For `arr = [1, 2, 5, 7]` and `target = 5`:

- `lower_bound(5)`: returns 2.
- `arr[2] == 5` ✓, so first = 2.
- `upper_bound(5)`: returns 3 (first index with value > 5).
- last = `upper_bound - 1 = 2`.
- Return `[2, 2]`.

This is the same index repeated. The general formula handles
unique elements and duplicates uniformly.

This is one of the prettiest properties of the lower/upper
bound abstraction: no special cases for "how many copies of x
are there?" The formulas work whether x has 0, 1, or many
copies.
''',
            },
            {
                "question": "Could I use bisect_left and bisect_right from Python?",
                "answer": r'''
Yes, and it's the cleanest production solution:

```python
import bisect

def search_range(arr, target):
    first = bisect.bisect_left(arr, target)
    if first == len(arr) or arr[first] != target:
        return [-1, -1]
    last = bisect.bisect_right(arr, target) - 1
    return [first, last]
```

`bisect.bisect_left` is lower bound (`O(log n)`,
optimized C). `bisect.bisect_right` is upper bound. The structure
is identical to our hand-rolled version.

In an interview, write the hand-rolled version to demonstrate
binary-search understanding. Then mention `bisect` as the
production answer. Some interviewers explicitly ask "without
using built-ins," in which case the hand-rolled version is
mandatory.

The hand-rolled version is also a great place to confirm you
have lower/upper bound truly memorized. The asymmetric
`hi = mid` vs `lo = mid + 1` updates are notorious for
off-by-one bugs. Practice writing them until it's automatic.
''',
            },
        ],
        "summary": r'''
**Pattern**: first = lower_bound(target); last = upper_bound(
target) - 1. Return [-1, -1] if the lower bound doesn't point
to the target.

**Lesson**: a run of duplicates in a sorted array is exactly
the half-open range `[lower_bound, upper_bound)`. Two
*O(log n)* searches answer first, last, and count in unison.

**Recognize next time**: any "first / last / count of x in a
sorted array" problem. The composition of lower and upper
bound is the canonical answer.
''',
    },
]
