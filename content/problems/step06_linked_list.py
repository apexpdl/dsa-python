"""Step 6 — Linked List."""
from __future__ import annotations

PROBLEMS: list[dict] = [
    {
        "id": "ll-reverse",
        "title": "Reverse a Linked List",
        "step_id": 6,
        "lecture_id": 3,
        "difficulty": "easy",
        "tags": ["linked-list", "pointers"],
        "what_this_teaches": (
            "The three-pointer **prev / curr / next** dance is the "
            "atomic move of linked-list work. Once you have it in "
            "your fingers, palindrome detection, reverse-in-k-groups, "
            "reorder list, and 'add two numbers' all become small "
            "variations on this same choreography."
        ),
        "pattern": "Three-pointer pointer flip: stash next, flip curr.next backward, slide forward.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": ["ll-introduction"],
        "next_problems": [
            "ll-palindrome",
            "ll-reverse-k-group",
            "ll-add-two-numbers",
            "reverse-doubly-linked-list",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 6 (Linked List)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 206 — Reverse Linked List",
                "url": "https://leetcode.com/problems/reverse-linked-list/",
            },
        ],
        "understanding": r'''
We are given the head of a singly linked list like
`1 -> 2 -> 3 -> 4 -> None`. We need to produce the reversed list
`4 -> 3 -> 2 -> 1 -> None` and return its new head.

This is **the** foundational linked-list problem. Every harder
linked-list problem (palindrome detection, reverse-in-k-groups,
add two numbers) uses reversal as a building block.
''',
        "brute_force": {
            "explanation": r'''
**Naive**: copy all values into a list, reverse the list, rebuild
the linked list. *O(n)* time and *O(n)* extra space. Wasteful — the
real solution does it in place with three pointers.
''',
            "code": r'''class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def reverse_via_list(head: ListNode | None) -> ListNode | None:
    if head is None:
        return None
    # Step 1: collect values.
    values = []
    node = head
    while node:
        values.append(node.val)
        node = node.next
    # Step 2: walk the original list again, writing values in reverse.
    node = head
    for v in reversed(values):
        node.val = v
        node = node.next
    return head
''',
            "walkthrough": r'''
The "use auxiliary memory" approach. Collect the values into
a list, then write them back in reverse order. Works correctly
but uses extra memory. Walking through every line:

**The node class:**

**`class ListNode:`** — Defines a linked list node. Each node
has a value and a pointer to the next node.

**`def __init__(self, val: int = 0, next: "ListNode | None" = None):`** —
Constructor. The defaults `val=0, next=None` let us create
nodes with `ListNode()` (an empty node) or `ListNode(5)` (a
single-value node) or `ListNode(5, other)` (linked to another).

The type hint `"ListNode | None"` is in quotes because Python
needs the string version for forward references — the type
`ListNode` doesn't exist yet at the moment we're defining the
class itself.

**`self.val = val; self.next = next`** — Just store the args
as attributes. Standard initializer.

**The reverse function:**

**`def reverse_via_list(head: ListNode | None) -> ListNode | None:`** —
Takes the head of a linked list, returns the new head after
reversal.

**`if head is None: return None`** — An empty list reverses
to an empty list. Handle it cleanly so the rest of the
function can assume `head` is real.

**`values = []`** — Will hold all the node values in their
original order.

**`node = head`** — A walker pointing to the current node.
Initially the head.

**`while node:`** — Walk the list. `while node` is True as
long as `node` is not None.

**`values.append(node.val)`** — Record the current value.

**`node = node.next`** — Move to the next node. After all
iterations, `node` is None and we exit.

**`node = head`** — Reset the walker to the head for a second
pass.

**`for v in reversed(values):`** — Walk the values list in
reverse. `reversed(values)` is an iterator that yields the
last element first, second-to-last second, etc.

**`node.val = v`** — Overwrite the current node's value with
the next value from the reversed sequence.

**`node = node.next`** — Move to the next node and continue.

After the loop, the **structure** of the list is unchanged
(nodes are still linked the same way), but their **values**
have been overwritten in reverse order — effectively
reversing the list's content.

**`return head`** — The head node is the same object as
before (its `val` was changed, but it's the same memory).
Return it.

This is *O(n)* time and *O(n)* memory. The optimized version
(below) does it in *O(n)* time but *O(1)* memory by
rearranging the **pointers** instead of copying values.
That's the canonical linked-list reversal.
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(n)*.",
        },
        "thought_process": r'''
The classic iterative algorithm uses three pointers: `prev`, `curr`,
`next`. The idea is to flip each pointer one at a time.

Imagine standing at `curr`. You hold the chain `... -> curr -> next -> ...`
and want to make it `... <- prev <- curr <- ...`. Before you flip
`curr.next` to point backward, you must remember the old `curr.next`
(otherwise you lose access to the rest of the list). So:

1. Save `next = curr.next`.
2. Flip `curr.next = prev`.
3. Advance `prev = curr`, `curr = next`.

Repeat until `curr` is `None`. The new head is `prev`.

Read it as: "remember where I was going, flip the arrow, step
forward". Once you write this three or four times, it becomes
finger memory.

There is also a recursive version that some find more elegant. It
uses *O(n)* call stack which can be a problem for very long lists.
For interviews, learn both and ship the iterative version.
''',
        "optimized": {
            "explanation": r'''
Iterative three-pointer reversal, in place.
''',
            "code": r'''def reverse_iter(head: ListNode | None) -> ListNode | None:
    prev: ListNode | None = None    # the new "tail" that grows forward
    curr = head
    while curr is not None:
        # Stash where we are heading before we flip the arrow.
        next_node = curr.next
        # Flip the arrow to point backward.
        curr.next = prev
        # Slide prev and curr one step forward.
        prev = curr
        curr = next_node
    # prev is now the new head; the original head's next has been flipped
    # to None implicitly because it became "prev" before curr became None.
    return prev


def reverse_recursive(head: ListNode | None) -> ListNode | None:
    # Base: empty list or single node — already reversed.
    if head is None or head.next is None:
        return head
    # Reverse the tail (everything after head).
    new_head = reverse_recursive(head.next)
    # Now make the node that head pointed at point back to head.
    head.next.next = head
    # And cut head's old forward pointer.
    head.next = None
    return new_head
''',
            "walkthrough": r'''
The canonical linked-list reversal. Three pointers, one pass,
constant memory. Memorize the shape — it's one of the most
asked interview problems.

**Version 1: Iterative three-pointer reversal**

**`def reverse_iter(head: ListNode | None) -> ListNode | None:`** —
Takes the head, returns the new head (the original tail).

**`prev: ListNode | None = None`** — `prev` tracks the
already-reversed portion. Initially None because the reversed
prefix is empty. By the end of the algorithm, `prev` will
point to the new head.

**`curr = head`** — `curr` is the node we're currently
processing. Initially the head of the original list.

**`while curr is not None:`** — Loop until we've processed
every node.

**`next_node = curr.next`** — **Save the next pointer** before
we overwrite `curr.next`. This is the most-forgotten line in
the algorithm. If we skip it, the next iteration loses access
to the rest of the list.

**`curr.next = prev`** — **Flip the arrow.** The current node
now points **backward** to the previously processed node. This
is the actual reversal step.

For example, after processing the second node, the list looks
like `1 ← 2  3 → 4 → 5` (the 1-2 arrow has been flipped; the
2-3 link is broken because `2.next` was just overwritten,
but we saved it as `next_node`).

**`prev = curr`** — Slide `prev` forward. The current node
is now part of the reversed prefix.

**`curr = next_node`** — Slide `curr` to the next node (which
we saved at the top of the loop). Without the save, this line
would crash.

**`return prev`** — When the loop exits, `curr` is None and
`prev` is the last node we processed — which was the original
tail and is now the new head.

The mental movie: imagine three fingers on the page. `prev`
trails one position behind `curr`. On each iteration, you
flip the arrow of the node `curr` is pointing at (so it
points back at `prev`), then both fingers slide one step
forward. The "saved next_node" finger temporarily points to
where you're going.

Total: *O(n)* time, *O(1)* memory. No extra data structure.

**Version 2: Recursive reversal**

Same idea, recursive form.

**`if head is None or head.next is None: return head`** —
Base case. An empty list or single-node list is already
reversed; just return it.

**`new_head = reverse_recursive(head.next)`** — **Trust the
recursive call.** It promises to reverse the rest of the list
(`head.next` onward) and return the new head of that reversed
sublist.

For example, on `1 → 2 → 3`: this recursively reverses
`2 → 3` into `3 → 2` and returns `3` as the new head. After
the call: `1 → 2 ← 3` (the recursion has flipped 2 and 3, but
1 still points forward).

**`head.next.next = head`** — Now we need to flip the edge
between `head` and `head.next` too. `head.next` is the node
that was originally next; its `.next` is now set to point
back at `head`.

In the example: `head` is `1`, `head.next` is `2`. The line
`head.next.next = head` makes `2.next = 1`. Now:
`1 → 2 ← 3` becomes `1 ⇄ 2 ← 3` — but `1.next` still points
to `2`, creating a cycle. We fix it next.

**`head.next = None`** — Break `head`'s forward arrow. Now
`head` is the new tail.

After: `1 ← 2 ← 3` with `1.next = None`. Done.

**`return new_head`** — Return whatever the recursive call
returned — which is the original tail, now the new head.

The recursive version uses *O(n)* stack space, which is worse
than the iterative *O(1)*. For lists of millions of nodes, the
recursion may overflow Python's stack. The iterative version
is preferred in practice.

The lesson here: both algorithms maintain the same invariant.
Iterative tracks `prev` explicitly; recursive uses the call
stack to remember. They're conceptually identical.
''',
            "complexity": (
                "**Time**: *O(n)* both versions. **Space**: *O(1)* "
                "iterative, *O(n)* call stack recursive."
            ),
        },
        "deep_concept": r'''
The three-pointer pattern (`prev`, `curr`, `next`) is **the**
linked-list move. It shows up in:

- **Reverse k-group** — same reversal, applied to chunks.
- **Palindrome linked list** — reverse second half, walk both.
- **Reorder list** — split, reverse second half, interleave.
- **Swap nodes in pairs** — adapted three-pointer dance.

The recursive version teaches a different lesson: trust the
recursive call, then add one rewiring step. After the recursive
call, the rest of the list is already reversed; we just have to
make the current node the new tail.

The trade-offs:

- **Iterative**: O(1) memory; verbose but explicit.
- **Recursive**: short but uses O(n) stack; will hit
  RecursionError on very long lists in Python.

Real interviews favor the iterative version. But if asked "can you
do it recursively?", you should be able to write it from memory.
''',
        "confusion_notes": [
            {
                "question": "Why do we need to stash `next_node = curr.next` *before* flipping the pointer?",
                "answer": r'''
Because the very next line, `curr.next = prev`, **overwrites**
`curr.next`. The old forward link is gone. If we did not save it
first, we would have no way to reach the rest of the list.

Walk through `1 -> 2 -> 3 -> None` with `prev = None, curr =
1`:

- Without the stash:
  - `curr.next = prev` makes node 1 point at `None`. The link to
    node 2 is lost.
  - We try `curr = curr.next` to advance — but `curr.next` is now
    `None`, so `curr = None`. The loop exits, but we never even
    saw nodes 2 and 3.

- With the stash:
  - `next_node = curr.next` remembers node 2.
  - `curr.next = prev` flips node 1's pointer to `None` (the new
    tail).
  - `prev = curr` advances `prev` to node 1.
  - `curr = next_node` advances `curr` to node 2. We continue.

The stash is the linked-list version of the "save before you
mutate" discipline you saw in `count-digits` (saving `original`
before destroying `n`) and `insertion-sort` (saving `current`
before sliding). Whenever a write would erase information you
still need, save the information in a local variable first.

Without the stash, the algorithm is **fast, in-place, and
wrong**. The discipline is what separates working code from
broken code in pointer-heavy problems.
''',
            },
            {
                "question": "Why does `prev = None` at the start? Shouldn't it be `head`?",
                "answer": r'''
Because after the reversal, the **original head** becomes the
**new tail**, and the new tail's `next` must be `None`. The
`prev` variable starts at `None` so that, by the time it gets
flipped onto the original head's `next`, the head correctly
points to `None`.

Walk through `1 -> 2 -> 3 -> None`:

- Initial: `prev = None, curr = 1`.
- After first iteration: node 1's `next` is now `None` (the new
  tail's terminator). `prev = 1, curr = 2`.
- After second iteration: node 2's `next` is now node 1. `prev =
  2, curr = 3`.
- After third iteration: node 3's `next` is now node 2. `prev =
  3, curr = None`.
- Loop exits. Return `prev = 3`, which is the new head.

Final structure: `3 -> 2 -> 1 -> None`. Correct.

If we had initialized `prev = head`, the very first iteration
would set `head.next = head`, creating a self-loop. The
algorithm would either crash or loop forever.

The `prev = None` initialization is exactly the boundary
condition that turns the original head into a properly
terminated tail. Internalize it.
''',
            },
            {
                "question": "Why does the recursive version do `head.next.next = head`?",
                "answer": r'''
Because at that line, `head.next` is still pointing at the
*old* next node (which is now the *last* node of the reversed
suffix). We want that node to point back at `head`, completing
the reversal of the link at this level.

Walk through `1 -> 2 -> 3 -> None` recursively:

- `reverse(1)` calls `reverse(2)`.
  - `reverse(2)` calls `reverse(3)`.
    - `reverse(3)` returns 3 (base case: single node).
  - Back in `reverse(2)`: `head = 2`. `head.next = 3`. So
    `head.next.next = head` means `3.next = 2`. Now node 3
    points back at node 2. Then `head.next = None` cuts node 2's
    old forward pointer. Return `new_head = 3`.
- Back in `reverse(1)`: `head = 1`. `head.next` is still pointing
  at node 2 (because we have not modified it yet at this level).
  `head.next.next = head` means `2.next = 1`. Now node 2 points
  back at node 1. Then `head.next = None`. Return `new_head =
  3`.

Final structure: `3 -> 2 -> 1 -> None`.

The key trick: at the moment we execute `head.next.next = head`,
`head.next` is the *previous* tail of the partially-reversed
suffix. By the time we return, every node has had its `next`
flipped exactly once.

It is one of those one-liners that takes a paper trace to fully
absorb. Walk through it on a three-node list and the pattern
clicks.
''',
            },
            {
                "question": "Why use `is` and not `==` when comparing nodes?",
                "answer": r'''
Because we want **identity** (the same object in memory), not
**equality** (two different objects that happen to compare
equal).

Two different `ListNode` instances might have the same `val`
field but represent different positions in the list. `==`
without a custom `__eq__` defaults to identity, so for
`ListNode` they happen to behave the same — but the cleaner,
more defensive practice is to use `is` for object-identity
comparisons.

For example, in the cycle-detection algorithm `if slow is fast`,
we are checking *"are these two pointers pointing at the same
node?"*, not *"do they have the same value?"*. A two-element
list `[7, 7]` has nodes with equal values but at different
addresses. Using `==` could mislead the reader into thinking we
care about values; `is` makes the intent unambiguous.

The same convention applies to `None` checks: write `if node
is None` rather than `if node == None`. PEP 8 and Python's
official style guide explicitly recommend `is None`.

Internalize: `is` for "same object," `==` for "equivalent
content." For linked-list nodes you almost always want `is`.
''',
            },
        ],
        "summary": r'''
**Pattern**: three-pointer `prev / curr / next` dance to flip
pointers in place.

**Lesson**: linked-list rewiring problems are nearly always about
remembering one node before you change a pointer.

**Recognize next time**: any "reverse / rearrange / merge a linked
list" problem. The same three-pointer choreography reappears.
''',
    },
    {
        "id": "ll-detect-loop",
        "title": "Detect a Cycle in a Linked List (Floyd's)",
        "step_id": 6,
        "lecture_id": 3,
        "difficulty": "easy",
        "tags": ["linked-list", "two-pointers", "cycle-detection"],
        "what_this_teaches": (
            "Floyd's tortoise and hare — periodicity detection in "
            "*O(1)* extra memory. The trick generalizes to any "
            "deterministic step function on a finite state space, "
            "powering 'find the duplicate number' and Pollard's rho "
            "factorization."
        ),
        "pattern": "Two pointers at speed 1 and 2; collision implies a cycle.",
        "prerequisite_lessons": ["linked-lists", "two-pointers"],
        "prerequisite_problems": ["ll-reverse", "ll-middle"],
        "next_problems": [
            "ll-loop-start",
            "ll-loop-length",
            "find-duplicate-number",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 6 (Linked List)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 141 — Linked List Cycle",
                "url": "https://leetcode.com/problems/linked-list-cycle/",
            },
        ],
        "understanding": r'''
A linked list may contain a **cycle** — a node whose `next` points
back to some earlier node. Detect whether the list has a cycle.

Example: `1 -> 2 -> 3 -> 4 -> 5 -> 3` (the 5 loops back to 3) is a
cyclic list. Naively walking from head with `while node:` would
spin forever.

There are two approaches:

1. **Hashing**: walk and store seen nodes; cycle detected when you
   revisit one. *O(n)* time, *O(n)* space.
2. **Floyd's tortoise and hare**: two pointers at different speeds.
   *O(n)* time, *O(1)* space.

The Floyd version is one of the most elegant algorithms you will
meet in beginner DSA.
''',
        "brute_force": {
            "explanation": r'''
Walk through and store visited nodes in a set. As soon as you see
a node twice, you have a cycle. *O(n)* time, *O(n)* extra space.
''',
            "code": r'''def has_cycle_hash(head) -> bool:
    seen = set()
    node = head
    while node is not None:
        if node in seen:
            return True
        seen.add(node)
        node = node.next
    return False
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(n)*.",
        },
        "thought_process": r'''
**Floyd's tortoise and hare** uses two pointers: `slow` advances
one step at a time, `fast` advances two. If there is no cycle,
`fast` will reach the end of the list. If there is a cycle, `fast`
will enter the cycle, then "lap" `slow` — and at some moment
`fast` will land on the same node as `slow`.

The proof is gentle modular arithmetic. Once both pointers are
inside the cycle, `fast` is gaining one step on `slow` per
iteration. The gap between them shrinks modulo the cycle length,
so within a number of iterations equal to the cycle length they
meet.

The aha moment: **fast at twice slow's speed catches slow inside
the cycle, no matter where they entered it**. Trace this on a
small example like `1 -> 2 -> 3 -> 2` (with cycle from 3 back to
2). Slow goes 1, 2, 3, 2, 3, 2, ... Fast goes 1, 3, 3, 3, ... and
they collide at 3.

A small but lovely follow-up: **find the start of the cycle**.
After detecting the meeting point, reset one pointer to the head
and advance both one step at a time. They meet at the cycle's
entry. The proof is more arithmetic but the *result* is one of the
prettiest algorithms in CS.
''',
        "optimized": {
            "explanation": r'''
Floyd's tortoise and hare. Two pointers, different speeds.
''',
            "code": r'''def has_cycle(head) -> bool:
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next          # 1 step
        fast = fast.next.next     # 2 steps
        # If they ever collide, there is a cycle.
        if slow is fast:
            return True
    # fast reached the end → no cycle.
    return False


def find_cycle_start(head):
    # Phase 1: detect the meeting point inside the cycle.
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None
    if fast is None or fast.next is None:
        return None
    # Phase 2: reset one pointer to head; advance both one step.
    # They meet at the cycle entrance.
    p = head
    while p is not slow:
        p = p.next
        slow = slow.next
    return p
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "deep_concept": r'''
Floyd's algorithm generalizes to any function `f` from a finite set
to itself. The orbit of a starting point eventually enters a cycle
(because the set is finite). The tortoise-and-hare detects that
cycle in `O(cycle_length)` time and `O(1)` space.

That generalization powers some non-linked-list problems:

- **Find the duplicate number** — interpret the array as a function
  `f(i) = arr[i]` and detect the cycle.
- **Random number generators with periods** — Floyd detects when
  the generator repeats.
- **Pollard's rho factorization** — uses Floyd inside.

The pattern is broader than "two pointers on a linked list". It is
"detect periodicity with constant extra memory".
''',
        "confusion_notes": [
            {
                "question": "Why must `fast` and `slow` collide if a cycle exists?",
                "answer": r'''
Because once both are inside the cycle, `fast` gains one step on
`slow` per iteration. The "gap" between them shrinks by exactly
one each step. Inside a cycle of length `c`, the gap can take
only the values `0, 1, 2, ..., c - 1` (mod `c`). So within at
most `c` iterations after both are inside, the gap reaches `0`
— that is, they coincide.

A bit more carefully: suppose `slow` is at position `s` (inside
the cycle) and `fast` is at position `f`. Each iteration, `slow`
moves to `s + 1`, `fast` to `f + 2`, both reduced modulo `c`.
The difference `f - s` (mod `c`) becomes `(f + 2) - (s + 1) =
(f - s) + 1` (mod `c`). So the gap increases by 1 per step. From
any starting gap in `[0, c - 1]`, after at most `c` iterations
the gap wraps around to `0`. They meet.

If there is no cycle, `fast` reaches the end of the list (a
`None`) without ever meeting `slow`. The condition `while fast
and fast.next` handles that case: it exits cleanly the moment
`fast` would step off the end.

The proof might feel slippery the first time. Run the algorithm
on a tiny cyclic list like `1 -> 2 -> 3 -> 2` (cycle from 3 back
to 2) on paper. Watch `slow` and `fast` chase each other. The
mechanics are simpler than the algebra suggests.
''',
            },
            {
                "question": "Why move `fast` by 2 and not by 3 or some other amount?",
                "answer": r'''
Because **two is the smallest speed difference that guarantees
collision**, and smaller is better for both simplicity and
robustness.

With speed 1 for slow and speed 2 for fast, the gap closes by
exactly 1 each iteration. The algorithm meets inside the cycle
within `c` iterations after both are inside.

If you used speed 3 instead, the gap closes by 2 per iteration.
On odd-length cycles, the gap parity might cause `fast` to skip
past `slow` without colliding. (E.g., cycle of length 3: gap
goes `1 -> 0` then wraps to `2`, then `1`, then `0`... they
collide eventually, but you have to think harder about why.)
Speed 2 has no such parity gotchas.

Any speed difference larger than 1 would work in principle, but
speed 2 is conventional because:
- It is the simplest non-trivial speed difference.
- It guarantees collision regardless of cycle length parity.
- The boundary checks (`while fast and fast.next`) stay simple.

There is a variant called **Brent's algorithm** that uses
different mechanics (doubling the search distance) and has
slightly better constants in some cases. But Floyd's
tortoise-and-hare is the canonical "always works, easy to
explain" approach.
''',
            },
            {
                "question": "How does the 'find the start of the cycle' second phase work?",
                "answer": r'''
The second phase relies on a beautiful piece of arithmetic.
After the first phase, `slow` and `fast` collide somewhere
inside the cycle. Let's call:

- `L` = distance from head to the cycle's entry point.
- `C` = length of the cycle.
- `m` = distance from the cycle's entry to the collision point.

At collision, `slow` has walked `L + m` steps. `fast` has walked
`2 * (L + m)` steps. Both end at the same node, so the
difference must be a whole number of laps around the cycle:
`(2L + 2m) - (L + m) = L + m = k * C` for some integer `k`.

Rearrange: `L = k * C - m`. That is, the distance from the head
to the cycle entry equals "some number of laps, minus the
distance from the entry to the collision point."

Now reset one pointer to the head and advance both pointers one
step at a time. After `L` steps:
- The head pointer is at the cycle entry (it has walked `L`
  steps along the non-cyclic tail).
- The slow pointer (still inside the cycle) has walked `L =
  k * C - m` steps. From the collision point (`m` steps past
  the entry), walking `kC - m` more steps lands it at... the
  cycle entry too (modulo `C`).

So both pointers meet **exactly at the cycle's entry**. Beautiful.

The algorithm: detect collision, then reset one pointer to the
head and walk both at speed 1 until they meet. The meeting point
is the cycle start.

This is one of those algorithms that feels miraculous until you
write out the arithmetic. After that it feels obvious.
''',
            },
            {
                "question": "Why is `fast and fast.next` the loop condition?",
                "answer": r'''
Because `fast` moves *two* steps per iteration, so we need both
its current node and its next node to exist before we can
safely jump.

The `fast.next.next` access requires `fast` non-None **and**
`fast.next` non-None. Skipping either check would crash with
`AttributeError: 'NoneType' object has no attribute 'next'`.

The condition `while fast and fast.next` covers both:

- `fast` is not None (so `fast.next` is defined).
- `fast.next` is not None (so `fast.next.next` is defined,
  though possibly `None` itself, which is fine because we are
  just assigning).

When the list has no cycle and `fast` walks off the end, one of
these two checks fails and the loop exits.

A common rookie bug: writing `while fast.next` and crashing on
single-node lists. With one node, `fast.next` is `None`, and
trying to evaluate `fast.next` is fine, but the next access
`fast.next.next` is the explosion. Always include both `fast`
and `fast.next` in the loop condition.

For a related variant — moving `slow` by 1 and `fast` by 3 — the
condition becomes `while fast and fast.next and fast.next.next`.
The general rule: every `.next` you intend to follow must be
guarded.
''',
            },
        ],
        "summary": r'''
**Pattern**: tortoise and hare — two pointers at speed 1 and 2.

**Lesson**: cycle detection in constant memory is achievable via
the speed difference between two pointers. Beautiful.

**Recognize next time**: any "is there periodicity / cycle?"
question on a sequence generated by a deterministic step function.
''',
    },
]
