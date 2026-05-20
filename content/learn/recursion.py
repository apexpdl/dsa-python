"""Recursion — the brain of advanced DSA."""

LESSON = {
    "id": "recursion",
    "title": "Recursion — Solving by Trusting Yourself",
    "tags": ["recursion", "fundamentals"],
    "summary": (
        "A full beginner chapter. What recursion really is, why the "
        "'leap of faith' is the key mental move, what the call stack "
        "looks like inside the machine, every common shape (linear, "
        "binary, branching, tail), and the discipline of backtracking."
    ),
    "body": r'''
## 0. A promise to the reader

Recursion is the topic where more beginners give up than at any
other point in a DSA curriculum. The cause is almost always the
same: they try to *follow* the recursive calls by tracing every
function frame in their head. Within seconds the picture is
hopeless — a stack of stacks of stacks — and they conclude that
they "just do not get recursion."

The good news: **you do not have to follow**. There is a different,
much cheaper way to think about recursion that works the moment
you accept it. This chapter teaches that way. By the end, recursion
should feel less like a parlor trick and more like the most natural
shape for many problems.

We are going to go slowly. We will explain the same idea in three
different ways, because it really is that important. If a paragraph
feels obvious, that is great — read it anyway. If a paragraph feels
slippery, that is normal — read it a second time before moving on.

## 1. The one-sentence definition

> **Recursion is solving a problem by solving a smaller version of
> the same problem and combining the result.**

That is the whole game. There is no other secret. Everything in
this chapter — base cases, the call stack, memoization, backtracking
— is bookkeeping around this single idea.

Take a moment with the sentence. Notice three pieces:

1. *Smaller version of the same problem.* Not a different problem,
   not a fancier one — literally the same problem, just with a
   smaller input.
2. *Solving it.* You assume the smaller problem can be solved.
3. *Combining the result.* You take whatever the smaller call gives
   you and do one extra step to turn it into the answer for the
   bigger problem.

If you can describe a problem in those three pieces, you can write
a recursive solution.

## 2. The leap of faith

Now the move that makes recursion easy. Beginners trip because they
try to *trace* the recursive call — follow it down into its own
recursive call, then into the next, and so on. Stop doing that.

Instead, **trust** the recursive call. Pretend, by magic, that the
smaller call already returns the correct answer for the smaller
input. Then ask yourself: *"given that the smaller call's answer is
correct, what one extra step do I add to make the answer correct
for the bigger input?"*

That is it. You write the one extra step. You trust the call. You
move on.

This is called the **leap of faith**, and it is the single most
important habit in recursion. Beginners who learn it can solve
recursive problems in their head; beginners who do not are stuck
tracing call stacks forever.

Why is the leap of faith justified? Because of **mathematical
induction**. You prove that the function is correct for the
smallest input (the base case). You then *assume* it is correct
for input size `n - 1` and show that the one extra step makes it
correct for input size `n`. By induction, the function is correct
for every `n`.

In day-to-day coding, you do not write proofs. You just take the
leap. The mental motion is: *"trust the call, do one step."* If you
write that on a sticky note above your monitor and look at it every
time you face a recursive problem, you will be ahead of half the
internet.

## 3. The three pillars of a well-formed recursion

Every recursive function has three pieces. If any of them is
missing or wrong, the recursion misbehaves. Memorize them.

**Pillar 1: A base case.** A smallest input where you return an
answer directly, without calling yourself. Without this, the
recursion has no floor and Python eventually crashes with
`RecursionError: maximum recursion depth exceeded`.

**Pillar 2: A strictly smaller subproblem.** Each recursive call
must work on a strictly smaller input. "Smaller" can mean a shorter
list, a smaller number, a deeper tree node, or simply "closer to
the base case." If the input is not smaller, the recursion never
reaches the base case and loops forever.

**Pillar 3: A correct combine step.** This is where the leap of
faith lives. You take the smaller call's result and add one tiny
step to lift it back to the full answer. This is also where most
bugs hide — get the combine wrong and the function gives wrong
answers even though it terminates.

When you sit down to write a recursive function, do not start with
the body. Start by naming the base case, the smaller subproblem,
and the combine step. Once those three are clear, the code writes
itself.

## 4. Example 1: sum of first n integers

Let's apply the recipe to a concrete problem. *"Compute 1 + 2 + 3
+ ... + n."*

**Base case.** What is the smallest `n` where the answer is
obvious? `n = 0`. The sum of zero numbers is 0. That is our base
case.

**Smaller subproblem.** If I can compute the sum up to `n - 1`,
that is one size smaller. So the recursive call is `total(n - 1)`.

**Combine step.** Take the smaller answer (sum up to `n - 1`) and
add `n` to it. That gives the sum up to `n`.

In code:

```python
def total(n):
    if n == 0:
        return 0                  # base case
    return n + total(n - 1)       # combine: smaller + one step
```

Read it as a sentence: *"The sum up to `n` is the sum up to `n - 1`
plus `n`. And the sum up to zero is zero."* That sentence is the
algorithm. There is no need to trace the call stack.

Try this exercise: rewrite the same problem with the base case at
`n = 1` instead of `n = 0`. (The body becomes `if n == 1: return
1`.) Both versions are correct; the second is a tiny bit shorter
in execution. Practice naming base cases that are clean and
correct.

## 5. Example 2: factorial

The same recipe, with one variable change.

**Definition**: `n! = n × (n - 1) × ... × 1`, and `0! = 1` by
convention.

**Base case**: `n = 0`. Answer 1.

**Smaller subproblem**: `factorial(n - 1)`.

**Combine step**: multiply by `n`.

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

We folded `0` and `1` into one base case because both give `1`.
That is a small optimization — both are correct, but the combined
one saves a recursive call.

The key insight you should be feeling by now: the structure of the
*math* — `n! = n × (n - 1)!` — translates almost mechanically into
the structure of the *code*. Recursion is exquisite when the
problem itself is recursive.

## 6. What is happening under the hood

You do not need this to *use* recursion. You should understand it
once, so the magic stops feeling magical.

When a function calls itself, Python pushes a new **stack frame**
onto the call stack. A frame contains the function's local
variables and the place to return to when the call finishes.

For `total(3)`:

```
Call total(3): waiting for total(2) + 3
  Call total(2): waiting for total(1) + 2
    Call total(1): waiting for total(0) + 1
      Call total(0): return 0
    total(1) returns 0 + 1 = 1
  total(2) returns 1 + 2 = 3
total(3) returns 3 + 3 = 6
```

Each call pushes a frame; each return pops a frame and resumes the
caller with the returned value substituted in. The recursion
unwinds in reverse order — the deepest call returns first, then
its caller, then its caller's caller, and so on.

This unwinding is essential to understand for two reasons.

**Reason one: memory.** Each frame is real memory. A recursion of
depth `n` uses `O(n)` stack space. For a balanced binary tree of
height `log n`, the recursion is shallow and stack space is fine.
For a linked-list-shaped tree of height `n`, stack space is `O(n)`
and Python crashes around `n = 1000` by default.

**Reason two: order of operations.** The order in which you do
your *own work* relative to the recursive call decides whether the
result comes out top-down or bottom-up. Print before recursing →
output is top-down. Print after recursing → output is bottom-up.
This is the difference between preorder and postorder tree
traversals, and we will see it constantly.

But again, **you do not have to think about the frames to write
the function.** Trust the call. Do one step.

## 7. The shapes recursion takes

There are not infinitely many shapes of recursion. Almost every
recursive function fits into a small number of templates. Knowing
the templates helps you recognize them quickly.

### Shape A: linear recursion (one self-call per frame)

`n!`, `sum(1..n)`, "print 1 to n", "reverse a linked list" — one
recursive call per frame, depth `n`. The recursion tree is a
straight line.

```python
def f(x):
    if base_case(x):
        return base_value
    return combine(x, f(smaller(x)))
```

### Shape B: binary recursion (two self-calls per frame)

Fibonacci, "tree height," "number of subsets" — two recursive
calls per frame. The recursion tree branches into two children.
Depth is still bounded by the input size, but the *total* number
of calls can be exponential if subproblems repeat.

```python
def f(x):
    if base_case(x):
        return base_value
    return combine(f(smaller_a(x)), f(smaller_b(x)))
```

This shape is the **doorway to dynamic programming**. When two
recursive calls share subproblems (like Fibonacci), the algorithm
is exponential without a cache. With a cache, it becomes linear.

### Shape C: branching recursion (many self-calls per frame)

Permutations, combinations, N-queens, "try every option" — the
function loops over a set of choices and recurses on each. The
recursion tree branches into many children.

```python
def f(state):
    if is_solution(state):
        record(state)
        return
    for choice in choices(state):
        apply(state, choice)
        f(state)
        undo(state, choice)   # backtracking
```

This is **backtracking** — recursion plus the discipline of undoing
every mutation before returning. We give it its own chapter.

### Shape D: divide-and-conquer recursion

Merge sort, quick sort, binary search (recursive form). The
function recurses into two equally-sized halves. The depth is
`log n`, the total work `O(n log n)` or similar.

```python
def f(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = f(arr[:mid])
    right = f(arr[mid:])
    return merge(left, right)
```

Each of these four shapes appears repeatedly in DSA. When you see
a new problem, ask yourself: *"is this linear, binary, branching,
or divide-and-conquer?"* Naming the shape often points you at the
right algorithm.

## 8. Backtracking: recursion with an eraser

Whenever a recursive function **mutates shared state**, every
recursive call must **undo** its mutation before it returns.
Otherwise, sibling branches see each other's leftover state and
the algorithm produces garbage.

Picture yourself in a maze with a piece of chalk. At each
junction, you mark which direction you took. You walk forward. If
you hit a dead end, you walk back to the junction and **erase**
your mark before trying a different direction. That erase is the
backtracking.

In code:

```python
def go(state):
    if is_solution(state):
        record(state)
        return
    for choice in choices(state):
        apply(state, choice)        # mark on the floor
        go(state)                   # explore further
        undo(state, choice)         # erase before trying the next sibling
```

Every `apply` has a matching `undo`. Every mutation has a matching
restoration. If you skip a single undo, the algorithm is wrong.

The classic mistakes:

1. **Forgetting to copy on record.** When you save the current
   state to your results, you must snapshot it (`current[:]` in
   Python). Otherwise every saved result points at the same evolving
   object, and at the end they all look identical.
2. **Forgetting to undo.** The matching pair `apply` / `undo`
   must be exact. Asymmetric apply/undo is the single largest
   source of backtracking bugs.
3. **Mutating shared state by accident.** Sometimes you reach into
   a parent variable without realizing it. The cure is to be
   explicit about what you mutate, or to use immutable arguments
   (pass `current + [x]` instead of mutating `current`).

The mental discipline is "every change is paid back before
returning." Once you internalize it, backtracking becomes
mechanical.

## 9. The tail-call temptation (and why Python does not optimize it)

In some languages (Scheme, Scala, Haskell), a recursion that ends
with a single recursive call — a **tail call** — is optimized into
a loop by the compiler. The stack does not grow. The recursion is
as memory-efficient as iteration.

Python does **not** do tail-call optimization. Every recursive
call grows the stack, even if the recursion is "tail-shaped." So
in Python, deep tail-recursive functions still hit the recursion
limit. There is no free lunch.

The practical consequence: when your recursion depth is high (say,
more than a few thousand), prefer iteration. Either rewrite the
algorithm with an explicit loop, or use an explicit stack to
simulate the recursion.

## 10. Common beginner mistakes and how to avoid them

**Mistake 1: forgetting the base case.** Symptoms:
`RecursionError: maximum recursion depth exceeded`. Cure: every
recursive function should start with a base case at the top. Ask
yourself "what is the smallest input where I know the answer
without recursing?" and write that line first.

**Mistake 2: not making the call smaller.** Symptoms: same as
above. The recursion runs forever because the input never reaches
the base. Cure: explicitly trace what gets smaller — the index,
the number, the list length — and make sure it strictly shrinks
each call.

**Mistake 3: mutating shared state without undoing.** Symptoms:
wrong answers, with results that look interrelated in weird ways.
Cure: backtracking discipline. Every `apply` paired with `undo`.

**Mistake 4: tracing the call stack in your head.** Symptoms: a
strong feeling that you "don't get recursion." Cure: stop tracing.
Trust the call. Do one step. The leap of faith.

**Mistake 5: hitting `RecursionError` on huge inputs.** Symptoms:
Python crashes once the input grows. Cure: convert to iteration,
or `sys.setrecursionlimit(...)` for a temporary fix.

**Mistake 6: thinking recursion is slow.** Recursion has a small
constant-factor overhead per call, but **the real performance
killer is repeated work**, not function calls themselves. A
memoized recursion is just as fast as an iterative DP for the same
problem.

## 11. The end-of-chapter exercise (do this before you leave)

Solve the following five problems recursively, using only the leap
of faith. Do not trace. Do not draw call stacks. Just name the
base case, the smaller subproblem, and the combine step.

1. **Sum of digits of a positive integer `n`.** Hint: base case `n
   == 0`, smaller is `n // 10`, combine is `+ (n % 10)`.
2. **Reverse a string `s` (return a new string).** Hint: base case
   empty string, smaller is `s[1:]`, combine is `+ s[0]`.
3. **Check if a list is sorted ascending.** Hint: base case length
   ≤ 1, smaller is "tail is sorted", combine is "first ≤ second
   and tail is sorted".
4. **Compute `x^n` for non-negative integer `n`.** Hint: base case
   `n == 0`, smaller is `x^(n - 1)`, combine is `* x`.
5. **Print all binary strings of length `n` without two
   consecutive 1s.** Hint: branching shape; at each position
   choose '0' (always) or '1' (if last char was not '1');
   recursively extend.

Doing these five problems on paper, with no tracing, is the
single best way to confirm recursion has clicked. If any of them
feels hard, reread the relevant section above.

## 12. Where to go next

Once recursion feels comfortable, the world of DSA opens up. Your
next stops in this curriculum:

- **Step 1, Lecture 5** — basic recursion problems. Mostly direct
  translations of math definitions.
- **Step 6** — linked-list operations like reverse and palindrome
  via recursion.
- **Step 7** — subsequence and "try every option" problems.
  Backtracking lives here in earnest.
- **Step 13** — tree problems. Every tree algorithm is recursive
  by nature.
- **Step 15** — graph DFS. Same shape, slightly more bookkeeping.
- **Step 16** — dynamic programming. Recursion + a sticky note.

That progression is the entire arc of intermediate DSA. The faster
recursion feels natural, the smoother the rest of the journey.

Take a breath. If anything in this chapter felt fast, reread the
relevant section. Then go solve the five exercises above. The
investment pays for itself for years.

## 14. The call stack — what it really is

Almost every confusion beginners have about recursion comes from
not picturing the **call stack**. Let me draw it for you.

When a function calls another function, the computer needs to
remember *where it was* in the caller so it can return there
later. To do this, it pushes a small bookkeeping record (called
a **stack frame**) onto a special region of memory called the
**call stack**. Each frame holds:
- The local variables of that invocation.
- The arguments passed in.
- The instruction pointer (where to return to).

When the called function returns, its frame is popped off the
stack. The caller's frame is exposed, and the caller picks up
where it left off.

For recursion, each recursive call adds a new frame. So
`fib(5) → fib(4) → fib(3) → fib(2) → fib(1)` produces a stack
five frames deep. Each frame has its own copy of `n`, its own
local variables, its own "where to go next." They cannot see
each other's locals — each frame is isolated.

```
fib(5)  ← arguments n=5; awaiting two recursive results
fib(4)  ← arguments n=4; awaiting two recursive results
fib(3)  ← arguments n=3; awaiting two recursive results
fib(2)  ← arguments n=2; awaiting two recursive results
fib(1)  ← arguments n=1; returns 1 immediately
```

The stack lives in a memory region with **bounded** size. Each
language has a default limit. CPython's default recursion limit
is 1000. If you exceed it, Python raises
`RecursionError: maximum recursion depth exceeded`. That's stack
overflow — not because memory is full but because the soft limit
was reached.

**When does this bite?** When you write a recursion that recurses
n times on input of size n, and n is huge. A 100,000-element
linked list reverse via recursion will blow the stack. A
balanced tree of a million nodes won't (the depth is ~20). A
degenerate tree (linked-list-shaped) of a million nodes will.

Two cures: convert to iteration with an explicit stack, or call
`sys.setrecursionlimit(100_000)` to raise the soft limit. The
former is safer; the latter is a quick fix that can crash the
process if you go too high.

## 15. Tail recursion — and why Python ignores it

A **tail call** is a recursive call that is the very last action
of the function. Languages like Scheme and Haskell optimize tail
calls into iteration: they don't push a new stack frame, they
reuse the current one. So in those languages, tail recursion
runs in constant stack space.

**Python does not do this.** Even tail-recursive Python eats one
stack frame per call. There are philosophical reasons (Guido
prefers loops for performance; tracebacks become harder to read
without each frame). The practical upshot: if you write deeply
tail-recursive code in Python, convert it to a `while` loop.

```python
# tail recursive (Python: O(n) stack)
def fact_tail(n, acc=1):
    if n <= 1: return acc
    return fact_tail(n - 1, n * acc)

# iterative (Python: O(1) stack — preferred)
def fact_iter(n):
    acc = 1
    for i in range(2, n + 1):
        acc *= i
    return acc
```

For interview / DSA work, this rarely matters because depths are
small. But for production code that handles arbitrary input
sizes, prefer iteration.

## 16. Memoization — the bridge to DP

I gave you a brief glimpse earlier. Let me make it concrete.

The naive recursive Fibonacci is exponential because subproblems
are computed many times. `fib(5)` calls `fib(4)` and `fib(3)`.
`fib(4)` calls `fib(3)` again and `fib(2)`. `fib(3)` was computed
twice. Drawing the full tree for `fib(6)` reveals dozens of
duplicate subtrees.

**Memoization** is the act of storing the result of every
subproblem the first time it is computed, and returning the
stored result on every subsequent call. The transformation is
mechanical: add a dictionary, check it first, store before
returning.

```python
def fib(n, memo={}):
    if n < 2: return n
    if n in memo: return memo[n]
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]
```

Or, cleaner, use `functools.lru_cache`:

```python
from functools import lru_cache
@lru_cache(maxsize=None)
def fib(n):
    if n < 2: return n
    return fib(n - 1) + fib(n - 2)
```

The decorator wraps the function in a cache that maps argument
tuples to return values. Same algorithm, no manual dict
management.

**What just happened?** We turned an exponential algorithm into
a linear one without changing its shape. The recursion tree had
2^n nodes; the *distinct subproblems* are only n in number. Each
node in the original tree corresponds to one of n distinct
subproblems. Memoization computes each distinct subproblem
*once*, even though the recursion would naively visit some
subproblems many times.

This is the essence of **dynamic programming**: the recursive
structure of a problem plus a memo of subproblem answers. Every
DP problem can be written this way (top-down). Many DP problems
can also be written bottom-up (tabulation), where you compute
the smallest subproblems first and build up. Both are equivalent
in complexity.

## 17. The "passing state down" vs "returning state up" idioms

Two ways to thread information through a recursion:

**Passing state down**: an extra parameter carries information
*to* the recursive call.

```python
def path(node, current_path):       # current_path passed in
    if not node: return
    current_path.append(node.val)
    if not node.left and not node.right:
        print(current_path)
    path(node.left, current_path)
    path(node.right, current_path)
    current_path.pop()              # backtrack
```

**Returning state up**: the recursive call returns information
*from* its subtree.

```python
def height(node):
    if not node: return 0
    return 1 + max(height(node.left), height(node.right))
```

**Both at once**: very common in tree problems.

```python
def diameter(node):
    best = [0]
    def h(n):
        if not n: return 0
        lh = h(n.left)
        rh = h(n.right)
        best[0] = max(best[0], lh + rh)   # passing UP (height)
        return 1 + max(lh, rh)
    h(node)
    return best[0]
```

Recognize which idiom you need by asking: *does the parent need
to know what the children found, or do the children need to know
what the parents decided?* Or both?

## 18. Backtracking — recursion with undo

Backtracking is recursion plus the discipline of **undoing** your
choice when you return from a recursive call. The template:

```python
def backtrack(state):
    if is_solution(state):
        record(state)
        return
    for choice in choices(state):
        apply(choice, state)         # make the choice
        backtrack(state)             # recurse
        undo(choice, state)          # take the choice back
```

The "undo" step lets us reuse the same `state` structure across
many recursive branches, instead of copying it. This is the
canonical pattern for: all subsets, all permutations, N-queens,
sudoku solver, word search, palindromic partitioning, and most
"try every option" problems in Step 7.

A classic example — generate all subsets:

```python
def subsets(nums):
    out = []
    cur = []
    def back(i):
        if i == len(nums):
            out.append(cur.copy())   # snapshot the current subset
            return
        # choice 1: exclude nums[i]
        back(i + 1)
        # choice 2: include nums[i]
        cur.append(nums[i])
        back(i + 1)
        cur.pop()                    # undo
    back(0)
    return out
```

Walk the tree. At each level i, we make a binary choice (include
or exclude `nums[i]`). The leaves correspond to all 2^n subsets.
The `cur.pop()` is the **undo** — when we return from the
recursive call, `cur` looks exactly like it did when we entered.

The undo is the single most-forgotten step in backtracking
problems. If your subsets / permutations / paths are coming out
weird, check that every `apply` has a matching `undo`.

## 19. The recursion-tree analysis cheat sheet

Time complexity of a recursive algorithm = number of nodes in the
recursion tree × work per node. The classic recurrences:

- `T(n) = T(n-1) + O(1)` → *O(n)*. Linear recursion: factorial,
  sum of a list.
- `T(n) = 2·T(n/2) + O(n)` → *O(n log n)*. Divide-and-conquer
  with combination: merge sort, quicksort (average).
- `T(n) = 2·T(n-1) + O(1)` → *O(2^n)*. Subsets / Hanoi.
- `T(n) = T(n-1) + T(n-2) + O(1)` → *O(φ^n)* ≈ exponential.
  Naive Fibonacci.
- `T(n) = T(n/2) + O(1)` → *O(log n)*. Binary search recursion.
- `T(n) = T(n/2) + O(n)` → *O(n)*. Quickselect, master theorem.

You don't need to memorize the master theorem; just learn to
sketch a recursion tree and count nodes. Most interview-level
recursion fits one of the shapes above.

## 20. Common bugs

**No base case.** The recursion never stops. Stack overflow
immediately.

**Wrong base case.** Either too narrow (function infinite-loops
on edge cases like empty input) or too broad (function returns
before doing the work it should). Always trace base cases by hand
on tiny inputs.

**Mutating shared state without undo.** If you forget the `undo`
in backtracking, your branches contaminate each other.

**Returning the wrong thing.** A recursive function should always
have one clear meaning: "given this subproblem, return X." If
the meaning drifts mid-function ("sometimes I return the height,
sometimes the diameter"), the algorithm is wrong. Pick one
contract and stick to it.

**Forgetting to combine results.** If your recursion has two
children, the combine step is where the magic happens. Don't
just recurse and throw the results away.

**Off-by-one in the recurrence parameters.** The classic: you
think `recurse(n)` means "first n" but actually it means "index
n," or vice versa. Decide what your parameter means and write
it as a comment at the top of the function.

**Forgetting to memoize.** If subproblems repeat (DP), and you
don't memoize, you have an exponential blowup. Always ask: *does
this recursion compute the same subproblem more than once?* If
yes, add a memo.

## 21. Mental practice exercises

Do these without writing code.

1. *Trace `fib(5)` step by step. Without memoization, how many
   total function calls are made?*

2. *In the subsets backtracking algorithm above, at the moment
   we record the subset `[1, 3]`, what does the call stack look
   like?*

3. *Why does the height-of-tree recursion work even on an empty
   tree? What does `height(None)` return, and why is that the
   right value to combine with the rest?*

4. *Could you write quicksort without using recursion? What
   would replace the recursive calls?*

5. *In the "passing state down" pattern, what would happen if
   you passed a copy of `current_path` to each recursive call
   instead of mutating? Same algorithm; different cost.*

If all five feel comfortable, you have absorbed the chapter.
''',
}
