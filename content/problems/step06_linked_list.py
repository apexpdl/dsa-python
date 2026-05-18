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
        "summary": r'''
**Pattern**: tortoise and hare — two pointers at speed 1 and 2.

**Lesson**: cycle detection in constant memory is achievable via
the speed difference between two pointers. Beautiful.

**Recognize next time**: any "is there periodicity / cycle?"
question on a sequence generated by a deterministic step function.
''',
    },
]
