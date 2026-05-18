"""Step 9 — Stacks and Queues."""
from __future__ import annotations

PROBLEMS: list[dict] = [
    {
        "id": "balanced-parentheses",
        "title": "Valid Parentheses",
        "step_id": 9,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["stack", "strings"],
        "understanding": r'''
We are given a string containing only the characters `()`, `[]`, and
`{}`. Return `True` if the string is balanced — every opener has a
matching closer of the same kind, and pairs are properly nested.

Examples: `"()[]{}"` → True. `"([{}])"` → True. `"(]"` → False.
`"([)]"` → False (crossed pairs).

This is the gateway stack problem. Master it; many bracket-matching
and expression-evaluation problems are built on the same idea.
''',
        "brute_force": {
            "explanation": r'''
A really naive approach repeatedly removes all `()`, `[]`, and `{}`
substrings until the string is empty (balanced) or no further
reductions help (unbalanced). It works but is *O(n²)* per
reduction step.

The stack solution is *O(n)* and reads like a story.
''',
            "code": r'''def is_balanced_replace(s: str) -> bool:
    # Naive: repeatedly remove neighbour pairs until stable.
    prev = None
    while prev != s:
        prev = s
        s = s.replace("()", "").replace("[]", "").replace("{}", "")
    return s == ""
''',
            "complexity": (
                "**Time**: *O(n²)* worst case. **Space**: *O(n)*."
            ),
        },
        "thought_process": r'''
Read a string of brackets and your eyes naturally do this: when you
see an opener, you remember it. When you see a closer, you check it
matches the **most recent** opener. The "most recent" makes this a
**stack** — last in, first out.

The algorithm:

1. Walk through the string.
2. For each opener (`(`, `[`, `{`), push onto the stack.
3. For each closer (`)`, `]`, `}`):
   - If the stack is empty, fail (closer with nothing to match).
   - Else pop and check the popped value is the matching opener.
4. At the end, the stack must be empty (no unmatched openers).

Why does this work? Because nested brackets have a strict
"first-in, last-out" structure. Whatever opens last must close
first. The stack enforces exactly that invariant.

This problem is also a great teaching tool for **why we need
stacks**. The same problem with just one bracket type could use a
counter (increment on `(`, decrement on `)`). But with multiple
bracket types, we need to remember **which** opener we saw, in
order — and a stack is the smallest data structure that does that.
''',
        "optimized": {
            "explanation": r'''
Single pass with a stack of openers.
''',
            "code": r'''def is_balanced(s: str) -> bool:
    # Map each closer to its expected opener.
    matches = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for ch in s:
        if ch in "([{":
            # Remember the opener.
            stack.append(ch)
        else:
            # ch is a closer. It must match the most recent opener.
            if not stack or stack[-1] != matches[ch]:
                return False
            stack.pop()
    # Anything left unmatched fails.
    return not stack
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(n)*.",
        },
        "deep_concept": r'''
The stack-with-matching-pairs pattern recurs:

- **Min stack** — augment with a running min so `getMin` is O(1).
- **Largest rectangle in histogram** — a monotonic stack of bar
  heights answers the question in O(n).
- **Asteroid collision** — a stack of survivors, with collision
  rules at the top.
- **Trapping rain water** — a stack tracks "boundaries" while
  computing water trapped between them.
- **Evaluate expression / Reverse Polish notation** — stacks of
  operands and operators.

The unifying principle: **whenever you need to remember the recent
history and combine it with the current item**, a stack is the
default tool. Reach for it before anything fancier.
''',
        "summary": r'''
**Pattern**: stack of openers; closer must match the top.

**Lesson**: nested structures are LIFO by nature. A stack matches
their grammar.

**Recognize next time**: any nesting / matching / 'most recent
pair' problem. Bracket languages, function call nesting, XML/HTML
tags — all stacks.
''',
    },
    {
        "id": "next-greater-element-i",
        "title": "Next Greater Element I",
        "step_id": 9,
        "lecture_id": 3,
        "difficulty": "easy",
        "tags": ["stack", "monotonic-stack"],
        "understanding": r'''
Given an array `nums`, for each element find the next element to
its right that is **strictly greater**. If none exists, return `-1`
for that position.

Example: `[2, 1, 2, 4, 3]` → `[4, 2, 4, -1, -1]`. The element `2`
at index 0 finds `4` at index 3. The element `1` finds `2` at index
2. And so on.

The brute force is *O(n²)*. The optimized **monotonic stack**
approach is *O(n)* and is one of the most important techniques in
all of intermediate DSA.
''',
        "brute_force": {
            "explanation": r'''
For each element, walk forward until you find one greater or hit the
end. *O(n²)*.
''',
            "code": r'''def next_greater_brute(nums: list[int]) -> list[int]:
    n = len(nums)
    out = [-1] * n
    for i in range(n):
        for j in range(i + 1, n):
            if nums[j] > nums[i]:
                out[i] = nums[j]
                break
    return out
''',
            "complexity": "**Time**: *O(n²)*. **Space**: *O(n)* for output.",
        },
        "thought_process": r'''
The monotonic stack idea: as we walk through the array, the stack
holds **indices of elements that are still waiting** for their next
greater. When a new element `nums[i]` arrives, it might be the
"next greater" for some of the indices on the stack.

We pop from the stack while the top's value is strictly less than
`nums[i]`. For each popped index, the answer is `nums[i]`. Then we
push `i` onto the stack — it now waits for its own answer.

The stack values, by index, are in **monotonic decreasing** order.
Hence "monotonic stack". The invariant: at every moment, the stack
contains indices `i1 < i2 < ... < ik` such that
`nums[i1] >= nums[i2] >= ... >= nums[ik]`.

Why is this *O(n)*? Each index is pushed exactly once and popped
at most once, so the total work across all iterations is `O(n)`
even though the inner `while` loop *looks* unbounded.

This pattern is one of the most reused tricks. Variations:

- **Previous greater** — walk right-to-left, same logic.
- **Next smaller** — flip the comparison.
- **Largest rectangle in histogram** — use the stack to determine
  the previous and next smaller bar for each bar.
- **Trapping rain water** — stack tracks "boundaries"; each pop
  computes water trapped between two boundaries.
- **Sum of subarray minimums** — for each element, find its
  "domain" using previous and next smaller.

Investing time in the monotonic stack pattern pays back enormously.
''',
        "optimized": {
            "explanation": r'''
Monotonic decreasing stack. *O(n)* time.
''',
            "code": r'''def next_greater(nums: list[int]) -> list[int]:
    n = len(nums)
    answer = [-1] * n
    stack: list[int] = []        # indices, with decreasing nums values
    for i in range(n):
        # Resolve everyone the new element is greater than.
        while stack and nums[stack[-1]] < nums[i]:
            idx = stack.pop()
            answer[idx] = nums[i]
        stack.append(i)
    return answer
''',
            "complexity": "**Time**: *O(n)* amortized. **Space**: *O(n)*.",
        },
        "deep_concept": r'''
The stack stores **unresolved indices**. When a new element arrives,
it resolves any indices in the stack that it dominates. The stack
naturally maintains a decreasing sequence because: every element
that gets pushed is smaller than the one already on top (otherwise
the top would have been popped).

The amortized linear time follows from this single invariant: each
index is pushed and popped at most once.

The same template, with tiny variations:

- **Previous Greater**: scan right to left, decreasing stack.
- **Next Smaller**: increasing stack, scan left to right.
- **Stock Span**: previous greater-or-equal; the span at day `i` is
  `i - previous_greater_index`.

These problems form a tight family. After you write three or four
of them, the pattern becomes muscle memory.
''',
        "summary": r'''
**Pattern**: monotonic stack of indices. When a new element
"defeats" stack entries, they get resolved.

**Lesson**: linear-time solutions to "for each i, find the nearest
X to the left/right" come from monotonic stacks.

**Recognize next time**: "next/previous greater/smaller" problems,
histogram problems, rain water, stock span, subarray min/max sums.
''',
    },
]
