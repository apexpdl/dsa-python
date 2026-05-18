"""Recursion — the brain of advanced DSA."""

LESSON = {
    "id": "recursion",
    "title": "Recursion — Solving by Trusting Yourself",
    "tags": ["recursion", "fundamentals"],
    "summary": (
        "Recursion is not a coding trick — it is a way of thinking. Once "
        "you accept the 'leap of faith', huge classes of problems become "
        "two-line solutions."
    ),
    "body": r'''
## The big idea in one sentence

> **Recursion is solving a problem by solving a smaller version of the
> same problem and combining the result.**

That is the whole game. Everything else — base cases, stack frames,
memoization — are details that grow out of that idea.

## The leap of faith

Beginners struggle with recursion because they try to "follow the
function down". They picture the call stack, then the call stack
inside the call stack, and within seconds the picture is impossible.

The professional trick is the opposite. **You do not follow.** You
assume the smaller call already works correctly, by magic, and you
just ask: "given that the smaller call gives me the right answer for
the smaller problem, what do I do to lift it back to the full one?"

This is called the **leap of faith**. Take it on faith that the
recursive call is correct, write the one line that combines its
result with the current step, and add a base case so the recursion
eventually stops. That is the entire recipe.

## Example: sum of first n natural numbers

> Compute 1 + 2 + 3 + ... + n.

The leap of faith says: "imagine I already had a function `sum(n - 1)`
that gives me 1 + 2 + ... + (n - 1). Then I just add `n` to it."

```python
def total(n: int) -> int:
    # Base case: the smallest problem we can solve without thinking.
    # Sum of zero numbers is zero.
    if n == 0:
        return 0
    # Recursive case: trust that total(n - 1) is correct.
    # Glue: add n to that smaller answer.
    return n + total(n - 1)
```

Read it as a sentence:
*"The sum up to n is the sum up to n - 1, plus n. And the sum up to
zero is zero."*

That is it. Do not picture the recursion tree. Do not trace the
stack. Read it as a definition.

## What makes a recursion well-formed?

Three rules, every time:

1. **There is a base case** — a smallest input where you just return
   an answer directly, no further calls. Without this, the recursion
   never stops and Python kills your program with `RecursionError`.
2. **The recursive call works on a strictly smaller subproblem.** If
   the call is not smaller, you might recurse forever even with a base
   case present. "Smaller" can mean shorter input, smaller number, or
   simply closer to the base case.
3. **The combine step does the right thing.** This is where most of
   your bugs will live, because the leap of faith is exactly: "assume
   the recursive call is correct; do I assemble it correctly?"

If any of those three rules are off, the recursion misbehaves. The
discipline of always thinking *base / smaller / combine* will save you
hours.

## How the computer actually runs it

You do not need to think this way to *write* recursion, but you
should understand it once. When a function calls itself, Python
pushes a new stack frame containing the local variables, returns to
the new function, eventually hits the base case, and unwinds.

For `total(3)`:

```
total(3) waits for total(2) + 3
  total(2) waits for total(1) + 2
    total(1) waits for total(0) + 1
      total(0) returns 0
    total(1) returns 0 + 1 = 1
  total(2) returns 1 + 2 = 3
total(3) returns 3 + 3 = 6
```

This is helpful to picture once, then forget. In day-to-day problem
solving you reason about recursion in English ("the sum up to n is
the sum up to n-1, plus n"), not by tracing frames.

## The shapes recursion takes

Almost every recursion problem belongs to one of a small set of shapes.

**1. Linear recursion: pick or skip the next element.**
Used for: subsequences, subset sum, knapsack.

```python
def subsequences(arr, i, current):
    if i == len(arr):
        print(current)
        return
    # Choice 1: skip arr[i]
    subsequences(arr, i + 1, current)
    # Choice 2: take arr[i]
    current.append(arr[i])
    subsequences(arr, i + 1, current)
    current.pop()                  # undo our choice to backtrack
```

The key idea: at each index, we have two choices — include or exclude.
The recursion explores both branches. Note the careful `pop` at the
end. We changed `current`, so we have to undo our change before we
return, or the caller sees stale state. This is **backtracking**.

**2. Binary recursion: two children.**
Used for: trees, fibonacci-style problems.

```python
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

The recursion tree branches. This shape often has overlapping
subproblems, which is the doorway to dynamic programming.

**3. Branching recursion: many children.**
Used for: permutations, N-queens, Sudoku, "try every option".

You loop through possible choices, recurse for each, and undo after.

## Common beginner mistakes

**Mistake 1: forgetting the base case.** Easy to forget when the
problem statement does not mention "stop". Always ask: "what is the
smallest input where the answer is obvious?"

**Mistake 2: not making the call smaller.** `f(n)` calling `f(n)` is
infinite. `f(n)` calling `f(n - 1)` is fine. Sometimes "smaller" is
"index moves forward" or "string shrinks by one character".

**Mistake 3: mutating shared state and forgetting to undo it.** When a
recursive call adds to a shared list, the next branch sees the
addition. Either backtrack with an explicit undo, or pass an
immutable snapshot. Both are valid; pick one consciously.

**Mistake 4: thinking recursion is slow because of function-call
overhead.** Function calls do have a cost, but the real performance
killer is **repeated work** — solving the same subproblem multiple
times. The fix is memoization (caching), which we cover in the DP
lesson.

**Mistake 5: hitting RecursionError on huge inputs.** Python's default
recursion limit is 1000. You can raise it with `sys.setrecursionlimit`,
but the right answer is often to convert deep recursion into iteration
with an explicit stack.

## A tiny pep-talk before you continue

For the first month, recursion will feel like falling backwards
through a glass floor. After two weeks of practice, it clicks — and
once it clicks, you start *seeing* recursive structure everywhere:
in linked lists, in trees, in graphs, in every "try all options"
problem.

The fastest way to make it click is to write recursive solutions to
problems you already know how to solve iteratively. Solve "sum of an
array" recursively. Solve "reverse an array" recursively. Solve
"check palindrome" recursively. Do five of those in one sitting and
your brain reshapes.
''',
}
