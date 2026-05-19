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
''',
}
