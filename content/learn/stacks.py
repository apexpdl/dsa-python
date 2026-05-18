"""Stacks — LIFO and why it shows up everywhere."""

LESSON = {
    "id": "stacks",
    "title": "Stacks — Last In, First Out",
    "tags": ["stack", "patterns"],
    "summary": (
        "A stack is a pile. You can put things on top, and take things "
        "off the top. From parentheses to monotonic patterns, this "
        "tiny shape powers a surprising number of clever algorithms."
    ),
    "body": r'''
## The pile analogy

Picture a stack of plates in a cafeteria. You add a fresh plate on
top. You take a plate off the top. You cannot pull a plate from the
middle without lifting everything above it. That is a stack: **last
in, first out**, or LIFO.

In Python you do not need a special class. A regular list works:

```python
stack: list[int] = []
stack.append(7)   # push
stack.append(3)
stack.append(9)
top = stack[-1]   # peek: 9
v = stack.pop()   # pop: returns 9, stack becomes [7, 3]
```

`append` and `pop` from the end are both amortized constant time, so
the list-as-stack pattern is fast.

## Where does a stack actually help?

Three big situations:

1. **Matching pairs.** Brackets, tags, opening and closing things. The
   stack remembers what is "open" and lets you confirm that the next
   "close" matches.
2. **Reversing implicitly.** A function call stack reverses execution
   order. Postorder traversal of a tree is naturally a stack problem.
3. **Monotonic patterns.** "Next greater element", "largest rectangle
   in histogram", "trapping rain water". These problems all use a
   stack to remember a *monotonically increasing* (or decreasing)
   sequence of indices.

The first two are intuitive. The third one is what makes the stack
truly powerful in DSA — and it deserves more attention.

## Pattern: balanced parentheses

```python
def is_balanced(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)              # remember an unmatched opener
        elif ch in ")]}":
            if not stack or stack[-1] != pairs[ch]:
                return False              # nothing to match, or mismatch
            stack.pop()                   # matched; remove the opener
    return not stack                      # nothing left unmatched
```

The pattern: every opener gets pushed, every closer must match the
top of the stack. If the stack is empty at the end, everything paired
up. If anything is left, an opener never found its closer.

## Pattern: next greater element

> For each element of an array, find the next element to the right
> that is strictly greater. If there is none, return -1.

Brute force is *O(n²)*: for each element, scan rightward until you
find a bigger one. A monotonic stack solves it in *O(n)*.

```python
def next_greater(nums: list[int]) -> list[int]:
    n = len(nums)
    answer = [-1] * n
    stack: list[int] = []                 # stores INDICES, not values
    for i in range(n):
        # Pop everything that is strictly smaller than nums[i].
        # We have just found their "next greater": it is nums[i].
        while stack and nums[stack[-1]] < nums[i]:
            top = stack.pop()
            answer[top] = nums[i]
        stack.append(i)
    return answer
```

Read it slowly. We walk through every element. We push its index onto
the stack. The stack always holds **indices of elements still
waiting for their next greater**. When a bigger element arrives, it
clears out everyone shorter than itself, because for each of them,
the answer is "this new element". After the cleanup, we push the new
element onto the stack to wait its own turn.

The total work is *O(n)*, because each index is pushed once and
popped once — even though the inner `while` loop *looks* like it
could run many times per outer iteration.

Once you internalize this, "next smaller", "previous greater", and
"previous smaller" are all simple variations: flip the comparison or
walk right-to-left.

## Pattern: monotonic stack

A monotonic stack maintains a strictly increasing (or decreasing)
sequence of values (or values at the indices it stores). When a new
element arrives that breaks the order, you pop elements off until
the order is restored, **and you do useful work on each pop**.

That phrase "useful work on each pop" is the heart of the pattern.
In next-greater, the work is "record this answer". In trapping rain
water, the work is "compute water trapped between two boundaries".
In largest-rectangle-in-histogram, the work is "compute the rectangle
that has this bar as its shortest".

The stack is the bookkeeping device. The actual algorithm lives in
the "useful work" you do on each pop.

## When does a stack feel wrong?

Stacks help when the order of processing is naturally LIFO. If the
problem is "first in, first out" (a checkout line, a BFS queue), a
queue is the right tool. If the problem requires random access or
sorted order, you want a list, dict, or heap instead.

Be careful with recursion: a recursive function is using the **call
stack** behind your back. Sometimes the cleanest "stack-based
algorithm" is just a recursive function — but for very deep inputs in
Python, an explicit stack avoids `RecursionError`.

## Common beginner mistakes

**Mistake 1: storing values when you need indices.** Many monotonic
stack problems require knowing the position. Store indices; look up
values when needed.

**Mistake 2: forgetting the empty-stack check.** `stack.pop()` on an
empty stack raises `IndexError`. Always guard with `if stack:` or a
sentinel value.

**Mistake 3: using a queue's `pop(0)`.** That is *O(n)* because it
shifts every other element. For real FIFO you want
`collections.deque`. (For a stack, `list.pop()` from the end is
already correct.)

**Mistake 4: building a monotonic stack with the wrong direction.**
If the problem asks "next greater on the right", you scan left to
right, popping smaller values. If it asks "previous greater on the
left", you also scan left to right, but you read from the top of the
stack instead of popping for the answer. Draw it on paper once.

## The mental model

Stack is a pile. Use it when the past matters and you only need the
most recent past. The monotonic-stack pattern is a specific weapon
that turns many *O(n²)* "for each, look outward" problems into
*O(n)* single passes. When you see "next greater / previous smaller /
how far back / how far forward", reach for a monotonic stack first.
''',
}
