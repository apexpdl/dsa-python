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
