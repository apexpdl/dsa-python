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
    # The remaining Step 4 problems will be added in subsequent commits,
    # written at this same depth bar. For now, the two 2D-matrix problems
    # serve as the exemplars matching the user's Search 2D Matrix example.
    # =================================================================
]
