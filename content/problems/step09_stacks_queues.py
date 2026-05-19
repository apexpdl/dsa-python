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
        "what_this_teaches": (
            "Stacks model **nesting**. Whenever you have to keep track "
            "of the most-recent unmatched thing, a stack is the right "
            "tool. The pattern extends to HTML/XML tag matching, "
            "function-call nesting, and expression parsing."
        ),
        "pattern": "Stack of openers; closer must match the top.",
        "prerequisite_lessons": ["stacks", "strings"],
        "prerequisite_problems": [],
        "next_problems": [
            "min-stack",
            "infix-to-postfix",
            "valid-parenthesis-string",
            "remove-outer-parentheses",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 9 (Stacks & Queues)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 20 — Valid Parentheses",
                "url": "https://leetcode.com/problems/valid-parentheses/",
            },
        ],
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
        "confusion_notes": [
            {
                "question": "Why a stack and not just a counter?",
                "answer": r'''
Because the problem has **multiple bracket types** (`()`, `[]`,
`{}`). A counter could only track *how many* openers are
unmatched, not *which kind*.

If you had only `()`, a counter would suffice: increment on `(`,
decrement on `)`. If the counter ever goes negative, fail; if
it is not zero at the end, fail.

But for `([{}])`, a counter could not distinguish `(` from `[`.
It would happily accept `([)]` — three openers, three closers,
zero net count — even though that string is malformed because
the brackets cross.

A stack stores the **identity** of each unmatched opener, in
order. When a closer arrives, we check it against the top of
the stack. If it matches the kind we are expecting, pop and
continue. If it does not, fail immediately.

The general rule: counters track *quantity*, stacks track
*identity and order*. Whenever the problem has more than one
"kind" of unmatched thing, you need the structure that
remembers each one — that is the stack.

This is also why HTML / XML tag matching needs a stack: each
`<div>` must be matched by `</div>`, each `<span>` by `</span>`.
A counter cannot tell which kind of close-tag belongs where.
''',
            },
            {
                "question": "Why do we return `not stack` at the end instead of just `True`?",
                "answer": r'''
Because if the stack is **non-empty** at the end of the walk,
it means some openers were never closed. The string had
trailing unmatched openers.

Consider `s = "(("`. We push `(` twice. The loop ends. If we
returned `True`, we would be saying "balanced" for a clearly
unbalanced string.

`not stack` evaluates to `True` only when the stack is empty,
meaning every opener was matched by a closer. So the final
return correctly handles three cases:

- No openers, no closers: empty stack → balanced.
- All openers matched: empty stack → balanced.
- Trailing unmatched openers: non-empty stack → unbalanced.

We also need to handle the symmetric case of trailing
unmatched **closers** inside the loop:

```python
if not stack or stack[-1] != matches[ch]:
    return False
```

`not stack` catches "closer arrives but no opener to match."
`stack[-1] != matches[ch]` catches "closer arrives, but it
mismatches the top opener."

Both checks together cover all failure modes. Forgetting either
is a common bug. Walk through the strings `"(((`, `)))`, `([)]`,
and `()()` to confirm you understand each case.
''',
            },
            {
                "question": "Why use a `dict` to map closers to openers? Couldn't I just write `if/else`?",
                "answer": r'''
You could, but the dict is shorter, more declarative, and
easier to extend.

```python
matches = {")": "(", "]": "[", "}": "{"}
```

This one line replaces nine lines of `if/elif`:

```python
if ch == ")" and stack[-1] != "(":
    return False
elif ch == "]" and stack[-1] != "[":
    return False
elif ch == "}" and stack[-1] != "{":
    return False
```

With the dict, the loop body shrinks to:

```python
if not stack or stack[-1] != matches[ch]:
    return False
stack.pop()
```

Three lines, regardless of how many bracket types you support.
If a new bracket type is added (say angle brackets `<>`), you
add one entry to the dict — no logic change. If you used `if/
elif`, you would add three more lines and risk forgetting one.

This is a **data-driven** vs **code-driven** trade-off. Whenever
your code has many parallel `if`s that vary only by data
values, replacing them with a dict lookup or a list of tuples
is usually cleaner.

The dict version also documents the **invariant** that the
algorithm cares about: every closer has a unique matching
opener. The `if/elif` chain hides this invariant in a wall of
branches.
''',
            },
            {
                "question": "What's the time and space complexity?",
                "answer": r'''
*O(n)* time, *O(n)* space in the worst case.

The loop walks each character of the string exactly once. Each
iteration does constant work — a `dict` lookup, a list
`append`, or a list `pop`. So the total time is `O(n)`.

The space comes from the stack. In the worst case (all
openers, no closers — e.g., `"(((((((((("`), the stack grows
to size `n`. Even though that input is ultimately invalid, the
algorithm holds every opener until it fails at the end.

For "balanced" inputs, the stack peaks at the maximum nesting
depth. So *O(n)* is the true worst case, but in practice the
stack stays small for well-formed inputs.

The fundamental lower bound: you cannot do better than *O(n)*
time because you have to read every character at least once.
You cannot do better than *O(depth)* space because the
algorithm must remember every unmatched opener until its
closer arrives. So this algorithm is optimal asymptotically.

In Python, `list.append` and `list.pop` from the end are both
amortized *O(1)*, so using `list` as a stack is appropriate.
For very high-performance languages, you might use a `deque` or
preallocated array, but for normal-sized inputs `list` is
fine.
''',
            },
        ],
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
        "what_this_teaches": (
            "The **monotonic stack** pattern — one of the most powerful "
            "linear-time techniques in array DSA. It turns 'for each i, "
            "find the nearest X to the left/right' from O(n²) into O(n) "
            "by maintaining a stack of unresolved indices."
        ),
        "pattern": "Stack of indices in decreasing value order; pop and resolve when a bigger element arrives.",
        "prerequisite_lessons": ["stacks", "arrays"],
        "prerequisite_problems": ["balanced-parentheses"],
        "next_problems": [
            "next-greater-element-ii",
            "next-smaller-element",
            "trapping-rain-water",
            "largest-rectangle-histogram",
            "sum-subarray-minimums",
            "online-stock-span",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 9 (Monotonic Stack)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 496 — Next Greater Element I",
                "url": "https://leetcode.com/problems/next-greater-element-i/",
            },
        ],
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
        "confusion_notes": [
            {
                "question": "Why does the inner `while` loop not make this O(n²)?",
                "answer": r'''
This is the most counter-intuitive part of monotonic stack
problems, and the answer is an **amortized argument**: even
though the `while` loop *can* iterate many times in a single
outer step, **each element is pushed onto the stack exactly
once and popped at most once** over the entire algorithm.

So the total work the `while` loop does, summed across **all**
outer iterations, is bounded by `n` — the total number of pushes
and pops. Combined with the `n` outer iterations, the algorithm
does at most `2n` constant-time operations. That is `O(n)`.

Contrast with a naive "for each `i`, scan rightward" algorithm.
That algorithm rescans the same elements many times — if all
elements are equal except the last, every starting index would
walk to the end. *O(n²)* total.

The monotonic stack avoids the rescan because each element,
once popped (its answer recorded), never enters the stack again.
The bookkeeping ensures every element is "looked at" only twice
in its life — once when pushed, once when popped.

This kind of amortization argument appears in many "linear with
nested loops" algorithms: sliding window, longest consecutive
sequence, graph traversal. Whenever you see `while` inside `for`
and the inner work has a global budget tied to the input size,
the algorithm is linear despite appearances.
''',
            },
            {
                "question": "Why do we store *indices* on the stack instead of values?",
                "answer": r'''
Because for many monotonic stack problems we need to know the
**position** of the element, not just its value. Storing the
index lets us look up the value cheaply (`nums[stack[-1]]`)
while also knowing where it lives.

For "Next Greater Element," we only ever need the *answer
array*, indexed by position. So as soon as we pop, we write
`answer[popped_index] = nums[i]`. Without the index, we would
have no idea which slot of `answer` to fill.

For other problems in the family, the index gives us **distance
information**:

- **Largest Rectangle in Histogram**: when we pop index `j`,
  the rectangle's width is `i - left - 1`, where `left` is the
  new top of the stack and `i` is the current bar.
- **Stock Span**: the span at day `i` is `i -
  previous_greater_index`.
- **Trapping Rain Water**: the trapped water depends on the
  horizontal distance between the boundary indices.

In all cases, **the index carries more information** than the
value alone, and you can always recover the value with one
extra lookup. The reverse is not true.

The general rule: when in doubt, store indices. You lose
nothing and gain position information.
''',
            },
            {
                "question": "Why is the stack *decreasing* and not increasing?",
                "answer": r'''
Because we want to find the **next greater** element. The stack
holds indices that are **waiting for** their next greater. An
index is waiting because no element to its right (yet seen) is
greater than it. So everything still on the stack has a value
that has not been beaten — i.e., later (older) elements on the
stack have **smaller-or-equal values**.

Concretely, the invariant is: *stack values, read from bottom
to top, are non-increasing.*

Why? Because when a new element arrives that is greater than
the top, we pop the top (it found its answer). We keep popping
while the new element is bigger. Then we push the new element.
By the time we push, everything still on the stack is bigger
than (or equal to) the new element — so the new element fits at
the top of a still-non-increasing stack.

For the **next smaller** variant, the stack is **increasing**.
Same logic, flipped comparison.

For the **previous greater** variant, you walk the array
right-to-left with a decreasing stack. The "next" / "previous"
distinction is just the direction of the scan; the stack flavor
matches the comparison.

Memorize: **stack monotonicity matches the comparison direction
of the question**. "Next greater" → decreasing stack. "Next
smaller" → increasing stack. Get this match right and the
algorithm writes itself.
''',
            },
            {
                "question": "Why initialize `answer` to `-1` for every position?",
                "answer": r'''
Because `-1` is the **sentinel value** for "no next greater
element exists." After the loop ends, any indices still on the
stack were never resolved — they have no next greater to their
right. Their slot in `answer` stays at the initial `-1`.

```python
answer = [-1] * n        # default: no next greater
# ... loop fills in actual answers for resolved indices ...
return answer
```

We never explicitly set `answer[i] = -1`. The initialization
does it once, and the loop only overwrites slots when it
finds a real answer.

`-1` is a reasonable sentinel because the array values are
typically `0` or positive (or at least bounded below by some
known value). If your input could include `-1` as a real value
(say, negative integers), you would use a different sentinel —
`None`, `float('-inf')`, or whatever cannot collide with a real
answer.

The general pattern for sentinel choice: pick a value that is
*impossible* for the real answer to take. For indices, `-1` is
safe because indices are non-negative. For values, `None` is
universal but requires `Optional` typing.

Always state your sentinel choice explicitly in code or
comments. A reader scanning your function should not have to
guess what `-1` means.
''',
            },
        ],
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
