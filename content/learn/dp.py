"""Dynamic programming — recursion with a sticky note."""

LESSON = {
    "id": "dp",
    "title": "Dynamic Programming — Recursion with a Sticky Note",
    "tags": ["dp", "recursion", "memoization", "tabulation"],
    "summary": (
        "DP is not a separate topic — it is recursion that has learned "
        "to remember. Master the recipe: write a recursion, identify "
        "the state, cache it. Tabulation is the same idea written "
        "bottom-up."
    ),
    "body": r'''
## The big revelation

If recursion is "solve a problem by solving a smaller version", then
**dynamic programming is recursion that refuses to solve the same
subproblem twice**. That is the whole conceptual leap. There is no
magical "DP algorithm" — DP is what happens when you take a
recursive solution and prevent it from doing duplicate work.

## The motivating example: Fibonacci

```python
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

This is correct, but **disastrously slow**. `fib(40)` already takes a
noticeable while. Why? Because `fib(40)` calls `fib(38)` twice
(directly and through `fib(39)`). `fib(38)` is computed many times.
`fib(37)` is computed even more times. The recursion tree explodes.

Fix it with a sticky note.

```python
def fib(n: int, cache: dict | None = None) -> int:
    if cache is None:
        cache = {}
    if n < 2:
        return n
    if n in cache:
        return cache[n]
    cache[n] = fib(n - 1, cache) + fib(n - 2, cache)
    return cache[n]
```

`fib(40)` is now instant. We have not changed the algorithm. We have
only stopped repeating work. That single change is **memoization**,
and it is one of the two faces of DP.

In Python you can get memoization for free:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

`lru_cache` watches all your inputs and returns the cached result the
next time the same input shows up. As long as your arguments are
hashable (numbers, tuples, strings), this works beautifully.

## The two faces of DP

**Top-down (memoization)**: write the natural recursion, slap a cache
on it. Easy to write, easy to reason about, uses stack space.

**Bottom-up (tabulation)**: start from the base cases and build up
to the answer in a table. Uses less memory in some cases, avoids
recursion limits, but requires you to figure out the iteration order
yourself.

Both compute exactly the same answers. They are two presentations of
the same idea. Most people find top-down easier to *invent*, and
bottom-up easier to *optimize*.

### Top-down example: climbing stairs

> You can climb 1 or 2 steps at a time. How many distinct ways to
> reach step `n`?

```python
@lru_cache(maxsize=None)
def climb(n: int) -> int:
    if n <= 1:
        return 1
    return climb(n - 1) + climb(n - 2)
```

### Bottom-up version

```python
def climb(n: int) -> int:
    if n <= 1:
        return 1
    dp = [0] * (n + 1)
    dp[0] = dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

### Space-optimized version

```python
def climb(n: int) -> int:
    prev2, prev1 = 1, 1
    for _ in range(2, n + 1):
        prev2, prev1 = prev1, prev1 + prev2
    return prev1
```

Three versions, one algorithm. As you mature, you will write the
recursion first, add `@lru_cache`, convert to a table only if needed,
and space-optimize only if needed.

## The recipe (the most important section of this lesson)

Almost every DP problem yields to the same five-step recipe.

**1. Define the state.** What inputs uniquely identify a subproblem?
This is often "the index we are looking at" plus "any extra
constraints we need to remember". The number of distinct states
times the work per state is the total time complexity.

**2. Define the transition.** Given the state, what choices do you
have, and what subproblems do they delegate to? This is the body of
your recursive function.

**3. Define the base case.** The smallest state where the answer is
known directly.

**4. Memoize.** Add a cache so each state is computed once.

**5. (Optional) Tabulate.** If you want, rewrite as a loop over the
states in dependency order.

Once you can name the state for a problem, you have already done the
hardest 80% of the work.

## A worked example: 0/1 knapsack

> You have items with weights and values. Pick a subset whose total
> weight is at most `W` to maximize total value. Each item can be
> used at most once.

**State**: `(i, w)` — at item index `i`, with `w` capacity remaining,
what is the best value I can collect?

**Transition**: at each item we have two choices: skip it (move to
`i+1`, same `w`), or take it (move to `i+1`, capacity decreases by
its weight, value increases by its value — but only if it fits).

**Base case**: when `i == n`, no more items. Best value is 0.

```python
def knapsack(weights, values, W):
    n = len(weights)

    @lru_cache(maxsize=None)
    def best(i, w):
        if i == n:
            return 0
        skip = best(i + 1, w)
        take = 0
        if weights[i] <= w:
            take = values[i] + best(i + 1, w - weights[i])
        return max(skip, take)

    return best(0, W)
```

Notice we matched the recipe. State is `(i, w)`. Transition is the
two choices. Base case is `i == n`. The cache makes the whole thing
*O(n × W)* instead of *O(2^n)*.

## Recognizing a DP problem

DP shows up when:

1. The problem asks for a count, a maximum, a minimum, or a best.
2. The problem has obvious sub-decisions (pick / skip, go left / go
   right, partition here / partition there).
3. The same subproblem appears more than once if you write the brute
   force recursion.

If you can imagine the recursion tree and you see repeated nodes, DP
is the answer.

## Common beginner mistakes

**Mistake 1: jumping to a table.** Beginners try to write the
bottom-up loop directly and get tangled. Always start by writing the
recursion. Convert to a table only after the recursion works.

**Mistake 2: missing a state dimension.** If the answer depends on
"how much money I have left" or "whether I held a stock", that
dimension must be part of your state, or your cache will return
wrong results.

**Mistake 3: caching mutable state.** `lru_cache` requires hashable
arguments. If your state includes a list, convert to a tuple or
encode the state as numbers.

**Mistake 4: forgetting that DP is just structured search.** When a
DP solution feels mysterious, write out the recursion tree by hand
for a small input. The pattern becomes obvious.

**Mistake 5: optimizing too early.** A correct *O(n^2)* DP is better
than a buggy *O(n)* one. Get it correct first; optimize space and
time after.

## The mental model

DP = recursion + memory. Whenever you face an optimization or
counting problem, write the recursion first, identify the state,
slap a cache on it. If it is fast enough, ship it. If it is not,
think about whether you can iterate the states bottom-up, or
collapse the state space.

The most beautiful DP solutions are the ones where you stare at the
problem and the state — the answer-defining arguments — practically
announce themselves. That clarity takes practice, but it is a real
thing you can develop.
''',
}
