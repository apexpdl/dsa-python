"""Dynamic programming — recursion with a sticky note."""

LESSON = {
    "id": "dp",
    "title": "Dynamic Programming — Recursion with a Sticky Note",
    "tags": ["dp", "recursion", "memoization", "tabulation"],
    "summary": (
        "A full beginner chapter. What DP really is, why naive "
        "recursion can be unusably slow, the five-step recipe that "
        "solves almost every DP problem, the four canonical shapes, "
        "and the discipline of refining naive → memoize → tabulate "
        "→ space-optimize."
    ),
    "body": r'''
## 0. The promise of this chapter

If you read DSA forums or watch tutorials, you have probably seen
beginners describe DP as "the topic I cannot crack." It is the
single most cited stumbling block in interview preparation.

The good news: **DP is not a separate topic**. It is recursion
that has learned to remember. Every DP problem you will ever solve
is a recursive function plus a cache, possibly rewritten as a
loop. There is no special "DP technique" beyond that.

The bad news: many beginners learn DP backwards. They are taught
to write the table first, fill it in with magic formulas, and
pray. That order is brutal. The natural order is the opposite:
*write the recursion first, slap a cache on it, then optionally
convert to a loop*.

This chapter teaches the natural order. By the end you should be
able to look at any "find the best / count / minimum" problem
and ask the five questions that crack it open.

Read slowly. Try the exercises. The investment is worth it.

## 1. The big idea in one sentence

> **Dynamic programming is recursion that refuses to solve the
> same subproblem twice.**

That is the entire concept. The recursion gives you the answer
shape. The cache prevents redundant work. The combination of the
two is what we call DP.

Why does this matter? Because many natural recursive solutions
*are* exponentially slow without the cache. The classic example
is Fibonacci: the naive `fib(n) = fib(n - 1) + fib(n - 2)` makes
billions of calls for `n = 50`, almost all of them recomputing the
same values. With a cache, every distinct subproblem is computed
exactly once. The runtime collapses from `O(φⁿ)` to `O(n)`.

If you remember nothing else from this chapter, remember this:
**don't redo. Remember.**

## 2. The motivating example: Fibonacci

Pretty much every DP introduction starts here, and for good
reason: Fibonacci is the smallest possible example where the cache
matters dramatically.

The math: `F(0) = 0, F(1) = 1, F(n) = F(n - 1) + F(n - 2)`.

The naive code, written directly from the math:

```python
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

Five lines, correct, easy to read. Now run `fib(40)` on your
laptop. It takes a few seconds. Run `fib(50)`. It takes minutes.
Run `fib(60)`. Go make tea.

The slowness is not a bug. The function is correct. It is just
recomputing the same values an absurd number of times. `fib(30)`
gets evaluated about a million times during `fib(50)`. The
recursion tree is exponentially bushy.

Now add three magic words:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

Run `fib(50)` again. Instant. Run `fib(1000)`. Instant. The
underlying algorithm has not changed at all. We have only stopped
it from recomputing.

That, in five words, is dynamic programming. *Recursion. Plus a
cache.*

## 3. The five-step recipe

Almost every DP problem cracks open with the same five questions.
Memorize them. Apply them every time. They are not optional
heuristics — they are the spine of DP problem solving.

**Step 1: Define the state.**

What inputs uniquely identify a subproblem? This is the hardest
step and often the only one that takes thought. The number of
distinct states multiplied by the work per state is your time
complexity.

**Step 2: Define the transition.**

Given the state, what choices do you have? Each choice leads to a
smaller subproblem (or several smaller subproblems). The
recurrence is the formula that combines the smaller answers into
the current answer.

**Step 3: Define the base case.**

The smallest state(s) where the answer is known without recursing.
Usually "empty input" or "index past the end."

**Step 4: Memoize.**

Wrap the recursion with a cache. In Python, `@lru_cache(maxsize=
None)` does it for free as long as your state is hashable.

**Step 5 (optional): Tabulate.**

If you want to avoid recursion or eliminate stack usage, rewrite
the memoized recursion as a bottom-up loop. Compute base cases
first, then fill the table in dependency order.

Step 5 is optional. Many production DP solutions stay in the
memoized recursive form. Tabulation is the move when you need to
space-optimize or escape recursion limits.

## 4. The recipe in action: climbing stairs

**Problem.** You climb a staircase with `n` steps. Each move you
take 1 or 2 steps. How many distinct ways can you reach step `n`?

**Step 1: state.** "How many ways to reach step `k`?" — one
integer `k`. State = `k`.

**Step 2: transition.** The last move to reach step `k` was either
a 1-step (from step `k - 1`) or a 2-step (from step `k - 2`). The
total number of ways is the sum: `ways(k) = ways(k - 1) + ways(k
- 2)`.

**Step 3: base case.** `ways(0) = 1` (one way to "stay" at step
0 — the empty path). `ways(1) = 1` (one way: take a single
1-step).

**Step 4: memoize.**

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def ways(k):
    if k <= 1:
        return 1
    return ways(k - 1) + ways(k - 2)
```

**Step 5: tabulate (optional).**

```python
def ways(n):
    if n <= 1:
        return 1
    dp = [0] * (n + 1)
    dp[0] = dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

And one more step that we often take after tabulation:
**space optimization**. The recurrence only reads the last two
values, so we replace the table with two scalars:

```python
def ways(n):
    if n <= 1:
        return 1
    a, b = 1, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

Naive → memoized → tabulated → space-optimized. All four versions
give the same answers. They differ only in style and memory cost.
The naive recursion is shortest to write; the space-optimized
version uses the least memory.

This canonical refinement path applies to almost every 1D DP. Get
it in your bones on `climbing-stairs`, and you will not have to
re-derive it on `frog-jump`, `house-robber`, `decode-ways`, and a
dozen others. They are all the same shape with a slightly
different recurrence.

## 5. The four canonical shapes

DP problems are not random. They cluster into a small number of
canonical shapes. Recognizing the shape narrows the problem
dramatically.

### Shape A: 1D DP over an index

State = a single index. Transitions = "what choice do I make at
this index?".

Examples: climbing stairs, house robber, frog jump, decode ways,
maximum subarray (Kadane), longest increasing subsequence (with a
trick).

Recurrence shape: `dp[i]` depends on `dp[i - 1]`, `dp[i - 2]`, or
some small window of recent values. Space-optimizable to a handful
of scalars.

### Shape B: 2D DP over two indices

State = a pair of indices, often one per input string or array.
Transitions = match or skip on either side.

Examples: longest common subsequence, edit distance, distinct
subsequences, wildcard matching, shortest common supersequence.

Recurrence shape: `dp[i][j]` depends on `dp[i - 1][j]`, `dp[i][j
- 1]`, and `dp[i - 1][j - 1]`. Space-optimizable to two rows.

### Shape C: DP over a range (interval / partition DP)

State = a pair of indices `(i, j)` representing an interval of the
input. Transitions = try every possible split point in the
interval.

Examples: matrix chain multiplication, burst balloons, palindrome
partitioning II, minimum cost to cut a stick.

Recurrence shape: `dp[i][j] = min over k of (dp[i][k] + dp[k +
1][j] + cost(i, j, k))`. Time complexity is typically `O(n³)`.

### Shape D: DP on subsets (bitmask DP)

State = a bitmask representing a subset of items. Transitions =
add or remove an item.

Examples: traveling salesman (small N), partition into K subsets,
"can you partition this into ___".

Recurrence shape: `dp[mask] = ...`. Time complexity is typically
`O(2ⁿ × n)`, feasible for `n ≤ 20`.

These four shapes cover **the vast majority** of DP problems in
typical curricula. When you see a new DP problem, the first
question to ask is: *"which shape is this?"*. The answer points
you at the right state design.

## 6. The mental model: a fork in the road

For every DP problem, imagine you are at a fork in the road. The
problem says "minimize this," or "count those," or "find the best
of these." At each fork you have two or more options. Each option
takes you to a smaller version of the same problem.

The recurrence is: *take the best (or sum, or count) over all
options at this fork*. The base case is *what to do at the end of
the road*.

Example: house robber. State = "house index `i`." At each house
you have two options:

- **Skip**: leave this house alone. Move to `i + 1` with the same
  money.
- **Rob**: take this house's money. Move to `i + 2` (you cannot
  rob adjacent houses, so skip the next one).

The recurrence: `rob(i) = max(rob(i + 1), nums[i] + rob(i + 2))`.
Base case: `rob(i >= n) = 0` (no houses left).

Two forks, one recurrence, base case at the end. That is DP.

If you can describe a problem as "at each step I have these
choices, and each choice leaves me with a smaller version of the
same problem," you have written the DP.

## 7. Memoization vs tabulation: when to use which?

Both compute the same answers. Both have the same asymptotic time
complexity. The differences are stylistic and operational.

**Memoization (top-down)**:
- Closest to the recursive definition.
- Easier to write when the recurrence is complex.
- Only computes the subproblems actually needed.
- Uses recursion (stack space, can hit Python's recursion limit).

**Tabulation (bottom-up)**:
- Requires you to choose an iteration order.
- Computes every subproblem from base cases up.
- Avoids recursion entirely.
- Usually faster constants (no function call overhead).
- Easier to space-optimize because you see exactly which earlier
  cells you read from.

In practice: write memoization first to confirm the recurrence.
Convert to tabulation if you need to space-optimize, avoid
recursion limits, or get the small speedup. For interview
purposes, knowing both is valuable.

A piece of practical advice: do not feel pressured to write
tabulation if memoization fits the problem. The interviewer cares
that you understand the recurrence; the specific style is
secondary.

## 8. Space optimization: the trick that demystifies tables

Many DP tables look intimidating but only ever read from a tiny
window of recent cells. The space optimization trick is to keep
just that window.

**1D DP recurrence touches `dp[i - 1]`**: keep one scalar.

**1D DP recurrence touches `dp[i - 1]` and `dp[i - 2]`**: keep
two scalars.

**2D DP recurrence touches `dp[i - 1][j]`, `dp[i][j - 1]`,
`dp[i - 1][j - 1]`**: keep two rows (`prev` and `curr`), or one
row with careful updates.

The mental motion: look at the recurrence. Identify which earlier
cells it reads. The answer needs to remember exactly that many.
Everything else can be thrown away as you move forward.

Space optimization rarely changes asymptotic memory complexity by
a large factor — it usually goes from `O(n²)` to `O(n)`, or from
`O(n)` to `O(1)`. But it is a small thing that interviewers love
to see, and it confirms you actually understand the dependency
structure.

## 9. Common pitfalls

**Pitfall 1: skipping the state design.** Beginners jump straight
into writing a table without naming the state. They end up with
recurrences that are off by one, wrong dimensions, or mysteriously
incorrect. Always name the state first.

**Pitfall 2: caching unhashable state.** `lru_cache` requires
hashable arguments. If your state is a list, convert to a tuple.
If it is a dict, encode it as a frozenset of items. Or use
manual memoization with a dict whose keys are tuples.

**Pitfall 3: assuming tabulation is "the right way."** It is not.
Memoization is fine. Tabulation is a sometimes-useful
optimization. Many seasoned DP solvers stay top-down.

**Pitfall 4: forgetting that DP is just structured search.** When
a DP solution feels mysterious, write out the recursion tree by
hand for a small input. The cache becomes obvious.

**Pitfall 5: jumping to optimization without correctness.** A
correct `O(n²)` DP is better than a buggy `O(n)`. Always confirm
the naive memoized version works on examples before space-
optimizing.

**Pitfall 6: trusting the "DP formula" from a tutorial without
re-deriving it.** Tutorials are great, but memorizing formulas
gets you only so far. The skill that scales is *deriving the
recurrence yourself*. Practice that.

## 10. Visual mental model — the table as a graph

If you like pictures, here is one that helps. Imagine the DP
table as a graph. Each cell is a node. The recurrence draws edges
from the cell to the cells it depends on.

For LCS, the cell `(i, j)` has three incoming edges from `(i - 1,
j)`, `(i, j - 1)`, and `(i - 1, j - 1)`. The base row and column
are the "source" of the graph (they have no incoming edges).

To compute the answer, you topologically sort the graph and visit
cells in dependency order. For LCS the order is left-to-right,
top-to-bottom. For interval DP it is "shortest intervals first."

When you see DP this way, **the algorithm is just a graph
traversal**. The cache is just remembering nodes you have already
computed. Backwards-walking the table to reconstruct an answer is
just retracing a path in the graph.

If table-filling feels mechanical and uninspired, try this
graph view once. It can reframe DP as "traverse a DAG of
subproblems" — which is closer to what is really happening.

## 11. End-of-chapter exercise

Solve these five problems, applying the five-step recipe. Name the
state, the transition, and the base case **before** writing code.

1. **Climb stairs with cost.** Each step has a cost; you start
   from step 0 or step 1, take 1 or 2 steps at a time, and want
   to minimize total cost to reach step `n`. LeetCode 746.

2. **House robber.** An array of house values; you cannot rob two
   adjacent houses. Maximize total robbed. LeetCode 198.

3. **Coin change.** Given coin denominations and a target amount,
   find the minimum number of coins to make the target. LeetCode
   322.

4. **Unique paths.** A robot in an `m × n` grid wants to go from
   top-left to bottom-right, moving only right or down. How many
   unique paths exist? LeetCode 62.

5. **Longest common subsequence.** Two strings; find the length
   of the longest sequence of characters that appears in both in
   the same relative order. LeetCode 1143.

Do all five. Naming the state for each before coding is the most
valuable skill you can build. Once that part feels natural, the
rest is mechanical.

## 12. Where to go next

After this chapter, the natural curriculum order is:

- **Step 16 Lecture 1**: this chapter as a recap.
- **Step 16 Lecture 2**: 1D DP problems (Shape A).
- **Step 16 Lecture 3**: 2D / grid DP (Shape A extension).
- **Step 16 Lecture 4**: DP on subsequences (Shape B with arrays).
- **Step 16 Lecture 5**: DP on strings (Shape B canonical).
- **Step 16 Lecture 6**: DP on stocks (state-machine DP).
- **Step 16 Lecture 7**: DP on LIS.
- **Step 16 Lecture 8**: MCM / partition DP (Shape C).
- **Step 16 Lecture 9**: DP on squares.

That is the entire DP curriculum. Twelve to twenty hours of
practice if you stay focused. The shapes repeat; the recurrences
vary; the recipe stays the same.

Take a breath. Reread anything that felt slippery. Then go solve
the five exercises above. DP rewards practice more than reading,
so the sooner you put hands on keyboard, the better.

## 13. The DP design recipe in full

Every DP problem submits to the same five-step recipe. Drill it
on each new problem until your fingers do it automatically.

**Step 1: Identify the state.** What information uniquely
describes a subproblem? Common choices: an index, two indices, a
"current row + previous choice," "remaining budget," etc.

**Step 2: Write the recurrence.** Express `f(state)` in terms
of smaller states. There are usually 2-4 candidate transitions
(include / exclude, left / right, take / skip).

**Step 3: Identify base cases.** What are the smallest
subproblems whose answer is direct? Set them up so the
recurrence has something to build on.

**Step 4: Choose memoization or tabulation.** Memoization mirrors
the recursive shape. Tabulation iterates from base cases upward.
Both are equivalent in big-O.

**Step 5: Space-optimize.** Many 1D DPs only need O(1) extra
(rolling-pair). Many 2D DPs only need O(min(m, n)) (rolling
row). Identify which prior states you actually need.

## 14. The shapes catalog — full reference

DP problems fall into a small number of *shapes*. Learn the
shapes; once recognized, the recurrence usually writes itself.

**Shape A: Linear / 1D.** State is an index. Examples: fib,
climbing stairs, frog jump, house robber, max subarray. Time
*O(n)*, space *O(1)* with rolling.

**Shape B: 2D pair.** State is a pair of indices into two arrays
or strings. Examples: LCS, edit distance, distinct subsequences,
wildcard matching. Time *O(n·m)*, space optimization rolls one
dimension.

**Shape C: Interval / partition.** State is an interval `(i, j)`.
Recurrence tries every split point. Examples: matrix chain,
burst balloons, palindromic partitioning II, MCM. Time
*O(n³)*.

**Shape D: State machine.** State is index + a categorical
variable (current "mode"). Examples: stock with k transactions,
ninja's training. Time depends on the state.

**Shape E: Knapsack / subsequence.** State is index + remaining
capacity (or remaining target). Examples: 0/1 knapsack, subset
sum, coin change, target sum. Time *O(n·W)*, where W is
capacity.

**Shape F: Grid / 2D walk.** State is (row, col). Examples:
unique paths, min path sum, falling path, maximal square. Time
*O(m·n)*.

**Shape G: LIS / monotone sequence.** State is "longest /
shortest / count of sequences ending at i with some property."
Examples: LIS, longest divisible subset, longest string chain,
number of LIS. Time *O(n²)* naive, *O(n log n)* with bisect.

## 15. Top-down vs bottom-up — which to choose?

Both produce the same answer. Choose based on:

- **Easier to write?** Top-down (memoization) mirrors the
  natural recursion. Often faster to code under time pressure.
- **Need space optimization?** Bottom-up is easier to
  space-optimize. Rolling arrays are the standard technique.
- **Need partial answers?** Top-down only computes what's
  needed. Bottom-up computes everything up to the answer.
- **Stack depth concerns?** Top-down recurses; bottom-up
  iterates. For very deep recursion, bottom-up is safer.

In interviews, I recommend: start with top-down for clarity,
then convert to bottom-up if asked to optimize space.

## 16. Common bugs

**Wrong base case.** The most subtle DP bug. Especially in
counting problems — `dp[0] = 1` (one way to make sum 0, the
empty set) vs `dp[0] = 0` (no items selected). Decide
deliberately.

**Off-by-one in transitions.** `dp[i-1]` vs `dp[i+1]`. Sketch
a tiny example by hand to catch these.

**Forgetting to handle the empty input.** `dp[0]` or `dp[""]`
often need a special case. Set them up before the loop.

**Mutating state in memoized recursion.** If you memoize a
function that mutates global state, the memo returns stale
results on later calls. Memoized functions should be **pure**.

**Wrong loop order in tabulation.** For 2D, sometimes the order
of i and j matters; sometimes the order within a row matters
(0/1 vs unbounded knapsack — iterate weight up or down).

**Premature space optimization.** Get the 2D version right
first. Then optimize to 1D once you can see what's reused.

## 17. Mental exercises

1. *Define the state for "longest common subsequence of two
   strings." What does `dp[i][j]` mean? Write the recurrence
   in words.*

2. *0/1 knapsack vs unbounded knapsack: the only code
   difference is the iteration order on the inner loop. Why?
   Trace a tiny example.*

3. *Climbing stairs in O(1) space: what two variables do you
   keep? What is the recurrence?*

4. *MCM has time complexity O(n³). Why? Sketch the recursion
   tree and count.*

5. *In the "subset sum" DP, you can use a boolean array or an
   integer array (counting ways). What's the difference in
   semantics and code?*
''',
}
