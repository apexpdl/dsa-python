"""Stacks — LIFO and why it shows up everywhere."""

LESSON = {
    "id": "stacks",
    "title": "Stacks — Last In, First Out",
    "tags": ["stack", "patterns"],
    "summary": (
        "A full beginner chapter. A stack is a pile — you put things "
        "on top, take things off the top. From parentheses to "
        "monotonic patterns, this tiny shape powers a surprising "
        "number of clever algorithms."
    ),
    "body": r'''
## 0. What this chapter teaches

Stacks look almost too simple to deserve their own chapter. A
pile of things, last in first out. Done.

The reason they get a full chapter: the **monotonic stack** is
one of the most powerful linear-time patterns in DSA, and you
will not see how to use it without first internalizing the
basic stack behavior. Many medium / hard problems collapse from
`O(n²)` to `O(n)` purely through a clever stack maintenance
trick.

By the end of this chapter you should be able to spot "stack-
shaped" problems immediately and write the monotonic stack
template without thinking.

## 1. The pile analogy

Picture a stack of plates in a cafeteria. You add a fresh plate
on top. You take a plate off the top. You cannot pull a plate
from the middle without lifting everything above it. That is a
stack: **last in, first out**, or LIFO.

In Python a regular list works as a stack:

```python
stack = []
stack.append(7)          # push
stack.append(3)
stack.append(9)
top = stack[-1]          # peek (returns 9, doesn't remove)
v = stack.pop()          # pop (returns 9, removes it)
# stack is now [7, 3]
```

`append` and `pop` from the end are both amortized *O(1)*. So
list-as-stack is fast and idiomatic.

Avoid using `pop(0)` for stack operations — that is *O(n)* and a
completely different data structure (a queue).

## 2. Three big use cases

Stacks earn their keep in three situations.

**Use case 1: matching pairs.** Brackets, opening and closing
tags, function call nesting. The stack remembers what is "open"
and lets you confirm that the next "close" matches.

**Use case 2: reversing implicitly.** A function call stack
reverses execution order. Postorder traversal of a tree is
naturally stack-based. Any "process in reverse arrival order"
flow uses a stack.

**Use case 3: monotonic patterns.** "Next greater element,"
"largest rectangle in histogram," "trapping rain water." These
problems use a stack to remember a *monotonically increasing*
(or decreasing) sequence of indices.

The first two are intuitive. The third is what makes stacks
truly powerful in DSA — and it deserves the most attention.

## 3. Pattern: balanced parentheses

```python
def is_balanced(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in ")]}":
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
    return not stack
```

The skeleton:

- Every opener gets pushed.
- Every closer must match the top of the stack; pop on match,
  fail on mismatch.
- At the end, the stack must be empty (no unmatched openers).

If you can write this in your sleep, you understand stacks well
enough to move on to monotonic stacks.

## 4. Pattern: monotonic stack (the powerhouse)

> For each element of an array, find the next element to its
> right that is strictly greater.

Brute force: *O(n²)*. For each element, scan rightward until you
find a bigger one.

Monotonic stack: *O(n)*. As we walk through the array, the stack
holds **indices of elements that are still waiting** for their
next greater. When a bigger element arrives, it resolves
everyone on the stack who is smaller than it.

```python
def next_greater(arr):
    n = len(arr)
    answer = [-1] * n
    stack = []  # stores INDICES; corresponding values are decreasing
    for i in range(n):
        while stack and arr[stack[-1]] < arr[i]:
            idx = stack.pop()
            answer[idx] = arr[i]
        stack.append(i)
    return answer
```

Read it slowly. We walk every element. We push its index onto
the stack. The stack always holds indices of elements **still
waiting for their next greater**. When a bigger element arrives,
it clears out everyone shorter than itself; for each of them,
the answer is the new element. After the cleanup, we push the
new element onto the stack to wait its own turn.

Total work: *O(n)*. Each index is pushed once and popped at most
once, even though the inner `while` *looks* unbounded. This is
an amortization argument — see the Stacks and Queues curriculum
step for the full discussion.

Once you internalize this pattern, several siblings become
direct adaptations:

- **Previous greater**: scan right-to-left, same logic.
- **Next smaller**: flip the comparison.
- **Previous smaller**: flip and walk backwards.

## 5. Larger applications of the monotonic stack

The monotonic stack is the engine behind several famous
algorithms:

- **Largest rectangle in histogram**: for each bar, find the
  previous-smaller and next-smaller bar. The rectangle's height
  is the bar; the width is the distance between the two
  boundaries.
- **Trapping rain water**: pop bars to compute water trapped
  between them.
- **Sum of subarray minimums** / **Sum of subarray ranges**:
  for each element, find how many subarrays it dominates (or
  is dominated in).
- **Online stock span**: the number of consecutive days before
  today with price `<=` today's. Previous-greater problem in
  disguise.

The unifying observation: whenever you need to answer "for each
position, find the nearest X to the left/right with property
P," reach for a monotonic stack.

## 6. Stack from a queue, queue from a stack

A common interview classic: implement a stack using only queues,
or a queue using only stacks. The exercises teach the duality
between LIFO and FIFO.

- **Stack from queues**: every push reverses the queue (push to
  one queue, rotate everything from the other queue behind it).
- **Queue from stacks**: maintain two stacks — `in_stack` for
  pushes, `out_stack` for pops. Transfer from `in` to `out` when
  `out` is empty.

Both are *O(1)* amortized per operation when implemented
carefully. They are wonderful little exercises to internalize
the LIFO / FIFO distinction.

## 7. Recursion is secretly a stack

A recursive function uses Python's **call stack** behind the
scenes. Each recursive call pushes a frame; each return pops
one. The recursion's depth is the stack's maximum size.

This is why every recursive algorithm can be rewritten with an
explicit stack — you just simulate what Python does for you.
Sometimes the explicit version is preferable: deeper inputs
(no recursion limit), more memory control, or clearer
backtracking.

DFS, postorder traversal, expression evaluation, and many
"process and rewind" algorithms can be written either way. Knowing
both forms is valuable.

## 8. Common beginner mistakes

**Mistake 1: storing values when you need indices.** Many
monotonic stack problems require knowing the position. Store
indices; look up values when needed.

**Mistake 2: forgetting the empty-stack check.** `stack.pop()`
on an empty stack raises `IndexError`. Always guard with `if
stack:` or use a sentinel value.

**Mistake 3: using `pop(0)` for stack operations.** That's a
queue, not a stack. And it's *O(n)*, silently making your
algorithm quadratic.

**Mistake 4: building a monotonic stack with the wrong
direction.** "Next greater" needs a decreasing stack. "Next
smaller" needs an increasing one. Get this match wrong and your
algorithm pops the wrong values.

**Mistake 5: forgetting that the stack might still hold elements
at the end.** For "next greater" problems, leftover indices on
the stack have no next greater — they keep their `-1` answer.
Don't try to pop them all at the end; the answer array already
contains the right defaults.

## 9. End-of-chapter exercise

1. **Valid parentheses.** Already covered above. LeetCode 20.
2. **Min stack.** A stack that supports `push`, `pop`, `top`,
   and `getMin` all in *O(1)*. Hint: keep a parallel stack of
   running minimums. LeetCode 155.
3. **Next greater element.** Already covered. LeetCode 496.
4. **Daily temperatures.** For each day, how many days until a
   warmer one? Monotonic stack. LeetCode 739.
5. **Largest rectangle in histogram.** Monotonic stack with two-
   sided boundaries. LeetCode 84.

Do all five. The fifth one is the gateway to "maximal rectangle"
and several other matrix problems. Worth the time.

## 10. Where to go next

- **Step 9** — the dedicated stacks & queues curriculum step,
  with implementations and monotonic-stack problems.
- **Step 13** — tree traversals that use stacks (iterative
  preorder / inorder / postorder).
- **Step 15** — iterative DFS uses an explicit stack.

Stacks are tiny but mighty. The monotonic stack pattern alone
will save you hours of brute-force coding in the months ahead.
''',
}
