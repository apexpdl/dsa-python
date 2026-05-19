"""Step 6 extras — remaining linked-list problems.

Lecture 1 (Singly LL Basics): ll-introduction, ll-insert-node,
ll-delete-node, ll-length, ll-search.

Lecture 2 (Doubly LL Basics): dll-introduction, dll-insert,
dll-delete, dll-reverse.

Lecture 3 (Medium Singly LL): ll-middle, ll-loop-start, ll-loop-length,
ll-palindrome, ll-odd-even, ll-remove-nth-from-end, ll-delete-middle,
ll-sort, ll-sort-012, ll-intersection, ll-add-one, ll-add-two-numbers.

Lecture 4 (Medium DLL): dll-delete-occurrences, dll-pairs-with-sum,
dll-remove-duplicates.

Lecture 5 (Hard LL): ll-reverse-k-group, ll-rotate, ll-flatten,
ll-clone-random-pointer.
"""
from __future__ import annotations

_SHEET = {
    "label": "Striver's A2Z DSA Course Sheet",
    "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
}


def _lc(num: int, slug: str) -> dict:
    return {
        "label": f"LeetCode {num} — {slug.replace('-', ' ').title()}",
        "url": f"https://leetcode.com/problems/{slug}/",
    }


_LL_NODE_CLASS = r'''class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next
'''


PROBLEMS: list[dict] = [
    # ============================ Lecture 1 — Basics ============================
    {
        "id": "ll-introduction",
        "title": "Introduction to Linked Lists",
        "step_id": 6,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["linked-list", "fundamentals"],
        "what_this_teaches": "What a linked list is — a chain of nodes where each holds a value and a pointer to the next.",
        "pattern": "Build, walk, and visualize linked lists.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": [],
        "next_problems": ["ll-insert-node", "ll-delete-node", "ll-length"],
        "resources": [_SHEET],
        "understanding": r'''
A linked list is a sequence of **nodes**. Each node carries a
**value** and a **pointer** to the next node. The first node is
called the **head**. The last node points to `None` (or `null`).

To find the k-th element, you must walk from the head, one step
at a time. There is no random access — *O(k)* to reach
position k.

Compare with an array: array access is *O(1)*, but inserting in
the middle is *O(n)* (shift everyone). Linked-list access is
*O(n)*, but inserting after a known node is *O(1)* (rewire two
pointers).

The trade-off is fundamental: array trades slow inserts for
fast access; linked list trades slow access for fast inserts.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Build 1 -> 2 -> 3 -> None
head = ListNode(1, ListNode(2, ListNode(3)))

# Walk and print.
node = head
while node is not None:
    print(node.val)
    node = node.next
```

That walking loop is the fundamental operation for every linked-
list algorithm.
''',
        "optimized": {
            "explanation": "Build and walk a linked list.",
            "code": _LL_NODE_CLASS + r'''

def build_from_array(arr):
    # Build a linked list from a Python list.
    dummy = ListNode(0)
    tail = dummy
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_array(head):
    # Walk the linked list, collecting values.
    result = []
    node = head
    while node is not None:
        result.append(node.val)
        node = node.next
    return result
''',
            "complexity": "**Time**: *O(n)* for build and walk. **Space**: *O(n)* for the nodes.",
        },
        "summary": "**Pattern**: nodes connected by 'next' pointers; walk by following pointers.",
    },
    {
        "id": "ll-insert-node",
        "title": "Insert a Node in a Linked List",
        "step_id": 6,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["linked-list", "fundamentals"],
        "what_this_teaches": "Pointer rewiring for insertion. Insert at head is O(1); insert at the end requires walking to the tail.",
        "pattern": "Save next, point new node at it, point predecessor at new node.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": ["ll-introduction"],
        "next_problems": ["ll-delete-node", "ll-search"],
        "resources": [_SHEET],
        "understanding": r'''
**Insert at head**: create a new node whose `next` points to
the old head. The new node becomes the new head. *O(1)*.

**Insert at tail**: walk from head to the last node; set its
`next` to the new node. *O(n)*.

**Insert after a known node**: rewire two pointers in *O(1)*.

The pattern is always: save the existing `next` pointer, then
overwrite carefully so you don't lose access to the rest of the
list.
''',
        "optimized": {
            "explanation": "Three insertion variants.",
            "code": _LL_NODE_CLASS + r'''

def insert_head(head, val):
    # Create a node whose next points at the current head.
    return ListNode(val, head)


def insert_tail(head, val):
    # Walk to the last node, then attach.
    new_node = ListNode(val)
    if head is None:
        return new_node
    node = head
    while node.next is not None:
        node = node.next
    node.next = new_node
    return head


def insert_after(node, val):
    # Insert a new node right after `node`.
    # Save the old next so we don't lose it.
    new_node = ListNode(val, node.next)
    node.next = new_node
''',
            "complexity": "Head: *O(1)*. Tail: *O(n)*. After-known-node: *O(1)*.",
        },
        "summary": "**Pattern**: save the old next; point new node at it; rewire predecessor.",
    },
    {
        "id": "ll-delete-node",
        "title": "Delete a Node from a Linked List",
        "step_id": 6,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["linked-list", "fundamentals"],
        "what_this_teaches": "Deletion by bypassing the target node. The predecessor's next jumps over the doomed node.",
        "pattern": "Find predecessor; rewire predecessor.next to skip target.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": ["ll-insert-node"],
        "next_problems": ["ll-length", "ll-search"],
        "resources": [_SHEET, _lc(237, "delete-node-in-a-linked-list")],
        "understanding": r'''
To delete a node by **value**: walk until you find the
predecessor of the target; rewire `predecessor.next = target.next`.
*O(n)* worst case.

To delete the **head**: the new head is `head.next`.

To delete by **position** (k-th node): walk k - 1 steps,
then rewire.

The "dummy head" trick simplifies the special case of deleting
the head. Plant a dummy node before the real head; all deletions
become "find predecessor, rewire" with no special cases.
''',
        "optimized": {
            "explanation": "Delete by value with a dummy head.",
            "code": _LL_NODE_CLASS + r'''

def delete_value(head, target):
    # Dummy head simplifies head deletion.
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next is not None and prev.next.val != target:
        prev = prev.next
    if prev.next is not None:
        # Bypass the target node.
        prev.next = prev.next.next
    return dummy.next
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: find predecessor; rewire predecessor.next to skip target.",
    },
    {
        "id": "ll-length",
        "title": "Find the Length of a Linked List",
        "step_id": 6,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["linked-list", "fundamentals"],
        "what_this_teaches": "The most basic linked-list walk: count nodes.",
        "pattern": "Walk from head; increment a counter until None.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": ["ll-introduction"],
        "next_problems": ["ll-search", "ll-middle"],
        "resources": [_SHEET],
        "understanding": r'''
Walk from head; count each node. Stop at `None`. *O(n)*.

```python
def length(head):
    count = 0
    node = head
    while node is not None:
        count += 1
        node = node.next
    return count
```

This walking loop is the foundational pattern for every
linked-list algorithm.
''',
        "optimized": {
            "explanation": "Walk and count.",
            "code": _LL_NODE_CLASS + r'''

def length(head):
    count = 0
    node = head
    while node is not None:
        count += 1
        node = node.next
    return count
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: walk + count.",
    },
    {
        "id": "ll-search",
        "title": "Search an Element in a Linked List",
        "step_id": 6,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["linked-list", "fundamentals"],
        "what_this_teaches": "Linear search in a linked list. There is no binary search on linked lists (no random access).",
        "pattern": "Walk and compare.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": ["ll-length"],
        "next_problems": ["ll-middle", "ll-reverse"],
        "resources": [_SHEET],
        "understanding": r'''
Walk from head; compare each node's value with the target.
Return True (or the node, or the index) when found.

*O(n)* time. There is no logarithmic search for linked lists
because you cannot jump to the middle in *O(1)*.
''',
        "optimized": {
            "explanation": "Walk and compare.",
            "code": _LL_NODE_CLASS + r'''

def search(head, target):
    node = head
    while node is not None:
        if node.val == target:
            return True
        node = node.next
    return False
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: walk + compare.",
    },
    # ============================ Lecture 2 — Doubly LL ============================
    {
        "id": "dll-introduction",
        "title": "Introduction to Doubly Linked Lists",
        "step_id": 6,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["linked-list", "doubly-linked-list"],
        "what_this_teaches": "Doubly linked nodes have prev and next pointers. They enable O(1) deletion given a node and bidirectional traversal.",
        "pattern": "Two pointers per node: prev and next.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": ["ll-introduction"],
        "next_problems": ["dll-insert", "dll-delete", "dll-reverse"],
        "resources": [_SHEET],
        "understanding": r'''
A **doubly linked list** node has two pointers: `prev` (to the
previous node) and `next` (to the next). The first node's `prev`
is `None`; the last node's `next` is `None`.

The two pointers enable:

- **Walk both directions**: head-to-tail via `next`, tail-to-head via `prev`.
- **O(1) deletion given a node**: rewire its neighbors directly.

Cost: more pointers to maintain on insert/delete (4 pointers
instead of 2).

```python
class DListNode:
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next
```
''',
        "optimized": {
            "explanation": "Build a DLL from an array.",
            "code": r'''class DListNode:
    def __init__(self, val: int = 0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next


def build_dll(arr):
    if not arr:
        return None
    head = DListNode(arr[0])
    tail = head
    for v in arr[1:]:
        node = DListNode(v, prev=tail)
        tail.next = node
        tail = node
    return head
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(n)*.",
        },
        "summary": "**Pattern**: each node has prev and next; bidirectional traversal.",
    },
    {
        "id": "dll-insert",
        "title": "Insert a Node in a Doubly Linked List",
        "step_id": 6,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["linked-list", "doubly-linked-list"],
        "what_this_teaches": "DLL insertion rewires four pointers instead of two — both directions need updating.",
        "pattern": "Set new.prev, new.next, prev.next, next.prev.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": ["dll-introduction"],
        "next_problems": ["dll-delete", "dll-reverse"],
        "resources": [_SHEET],
        "understanding": r'''
To insert a new node `n` between two existing nodes `a` and `b`:

1. `n.prev = a`
2. `n.next = b`
3. `a.next = n`
4. `b.prev = n`

Four pointer assignments. Watch for boundary cases (a or b being
None for head/tail insertion).
''',
        "optimized": {
            "explanation": "Insert after a known node.",
            "code": r'''class DListNode:
    def __init__(self, val: int = 0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next


def insert_after(node, val):
    new_node = DListNode(val, prev=node, next=node.next)
    if node.next is not None:
        node.next.prev = new_node
    node.next = new_node
''',
            "complexity": "**Time**: *O(1)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: rewire four pointers, two in each direction.",
    },
    {
        "id": "dll-delete",
        "title": "Delete a Node in a Doubly Linked List",
        "step_id": 6,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["linked-list", "doubly-linked-list"],
        "what_this_teaches": "DLL deletion is O(1) given a node pointer — rewire two neighbors. Compare with singly LL where you must first find the predecessor.",
        "pattern": "node.prev.next = node.next; node.next.prev = node.prev.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": ["dll-insert"],
        "next_problems": ["dll-reverse", "dll-delete-occurrences"],
        "resources": [_SHEET],
        "understanding": r'''
Given a pointer to a node, delete it in *O(1)*:

```python
if node.prev: node.prev.next = node.next
if node.next: node.next.prev = node.prev
```

This is the killer feature of DLLs. The LRU cache uses it for
*O(1)* move-to-front.
''',
        "optimized": {
            "explanation": "Delete a known node in O(1).",
            "code": r'''def delete_node(node):
    if node.prev is not None:
        node.prev.next = node.next
    if node.next is not None:
        node.next.prev = node.prev
    # The deleted node still has prev and next set; if it's important,
    # null them out:
    node.prev = node.next = None
''',
            "complexity": "**Time**: *O(1)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: rewire neighbors' pointers; node is bypassed in O(1).",
    },
    {
        "id": "dll-reverse",
        "title": "Reverse a Doubly Linked List",
        "step_id": 6,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["linked-list", "doubly-linked-list"],
        "what_this_teaches": "Reversing a DLL is just swapping prev and next on every node. The structure makes it elegant.",
        "pattern": "For each node, swap its prev and next pointers. Return the old tail as the new head.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": ["dll-introduction", "ll-reverse"],
        "next_problems": [],
        "resources": [_SHEET],
        "understanding": r'''
For a DLL, reversal is beautifully simple: swap each node's
`prev` and `next` pointers. The head becomes the tail and vice
versa.

```python
def reverse_dll(head):
    node = head
    new_head = head
    while node is not None:
        new_head = node
        node.prev, node.next = node.next, node.prev
        node = node.prev   # we just swapped, so this is the OLD next
    return new_head
```
''',
        "optimized": {
            "explanation": "Swap prev/next on every node.",
            "code": r'''def reverse_dll(head):
    node = head
    last = None
    while node is not None:
        # Swap prev and next.
        node.prev, node.next = node.next, node.prev
        # We just swapped; the OLD next is now in node.prev.
        last = node
        node = node.prev
    return last
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: swap prev/next per node; the old tail is the new head.",
    },
    # ============================ Lecture 3 — Medium Singly LL ============================
    {
        "id": "ll-middle",
        "title": "Find the Middle of a Linked List",
        "step_id": 6,
        "lecture_id": 3,
        "difficulty": "easy",
        "tags": ["linked-list", "two-pointers"],
        "what_this_teaches": "Floyd's tortoise-and-hare for finding the middle in one pass.",
        "pattern": "Two pointers, slow moves 1 step, fast moves 2 steps; when fast hits end, slow is at the middle.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": ["ll-length", "ll-detect-loop"],
        "next_problems": ["ll-palindrome", "ll-sort"],
        "resources": [_SHEET, _lc(876, "middle-of-the-linked-list")],
        "understanding": r'''
Find the middle node of a linked list in one pass.

Two pointers, slow and fast. Slow moves 1 step, fast moves 2.
When fast reaches the end, slow is at the middle.

For even-length lists, slow ends at the **second middle** (the
LC convention) or the **first middle** (depending on
initialization).

```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
return slow
```

*O(n)* time, *O(1)* space.
''',
        "optimized": {
            "explanation": "Tortoise and hare.",
            "code": _LL_NODE_CLASS + r'''

def middle(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: slow/fast pointers; slow ends at the middle.",
    },
    {
        "id": "ll-loop-start",
        "title": "Find the Starting Point of a Loop",
        "step_id": 6,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["linked-list", "two-pointers", "cycle-detection"],
        "what_this_teaches": "Floyd's algorithm phase 2: after the collision, reset one pointer to head; both advance at speed 1 until they meet at the cycle start.",
        "pattern": "Phase 1: detect collision with tortoise/hare. Phase 2: reset, walk in lockstep.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": ["ll-detect-loop", "ll-middle"],
        "next_problems": ["ll-loop-length"],
        "resources": [_SHEET, _lc(142, "linked-list-cycle-ii")],
        "understanding": r'''
After Floyd's collision detects a cycle, the start of the cycle
can be found with a small arithmetic trick.

Let `L` = distance from head to cycle start.
Let `C` = cycle length.
Let `m` = distance from cycle start to the collision point.

At collision, slow walked `L + m`; fast walked `2(L + m)`. The
difference is a multiple of `C`: `L + m = k * C` for some `k >=
1`. Rearranging: `L = k * C - m`.

If we reset one pointer to head and advance both pointers
1-step-at-a-time, after `L` more steps the head-pointer reaches
the cycle start, and the cycle-pointer also reaches the cycle
start (`m + L = m + kC - m = kC`, which is exactly `k` laps).

They meet at the cycle start.
''',
        "optimized": {
            "explanation": "Two-phase Floyd.",
            "code": _LL_NODE_CLASS + r'''

def detect_cycle_start(head):
    # Phase 1: detect collision.
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

    # Phase 2: reset one pointer to head; advance both at speed 1.
    p = head
    while p is not slow:
        p = p.next
        slow = slow.next
    return p
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: Floyd's phase 1 + phase 2. Phase 2 uses the arithmetic identity L = kC - m.",
    },
    {
        "id": "ll-loop-length",
        "title": "Length of the Loop in a Linked List",
        "step_id": 6,
        "lecture_id": 3,
        "difficulty": "easy",
        "tags": ["linked-list", "two-pointers", "cycle-detection"],
        "what_this_teaches": "Once we know two pointers collide inside a cycle, count loop length by advancing one pointer until it meets the other again.",
        "pattern": "Floyd's detect; then walk one pointer around the cycle counting.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": ["ll-detect-loop", "ll-loop-start"],
        "next_problems": [],
        "resources": [_SHEET],
        "understanding": r'''
After detecting collision, hold one pointer still; advance the
other one step at a time. Count steps until they meet again.
That count is the cycle length.
''',
        "optimized": {
            "explanation": "Detect, then count.",
            "code": _LL_NODE_CLASS + r'''

def loop_length(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            # Count the loop.
            count = 1
            current = slow.next
            while current is not slow:
                count += 1
                current = current.next
            return count
    return 0
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: Floyd's detect + walk-and-count around the cycle.",
    },
    {
        "id": "ll-palindrome",
        "title": "Check if a Linked List is a Palindrome",
        "step_id": 6,
        "lecture_id": 3,
        "difficulty": "easy",
        "tags": ["linked-list", "palindrome", "two-pointers"],
        "what_this_teaches": "Reverse the second half in place; walk both halves comparing values. O(n) time, O(1) space.",
        "pattern": "Find middle (slow/fast) → reverse second half → compare both halves.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": ["ll-reverse", "ll-middle"],
        "next_problems": ["ll-odd-even"],
        "resources": [_SHEET, _lc(234, "palindrome-linked-list")],
        "understanding": r'''
Brute force: copy values to an array; check palindrome on the
array. *O(n)* time, *O(n)* space.

Optimal: do it in place.

1. Find the middle using slow/fast pointers.
2. Reverse the second half.
3. Walk from head and from new-second-half-head; compare.
4. (Optional) Reverse the second half again to restore the list.
''',
        "optimized": {
            "explanation": "Middle + reverse + compare.",
            "code": _LL_NODE_CLASS + r'''

def is_palindrome(head):
    if head is None or head.next is None:
        return True

    # 1. Find middle.
    slow = fast = head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next
        fast = fast.next.next

    # 2. Reverse the second half (starting at slow.next).
    prev = None
    curr = slow.next
    while curr is not None:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt

    # 3. Compare halves.
    left, right = head, prev
    while right is not None:
        if left.val != right.val:
            return False
        left = left.next
        right = right.next
    return True
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: middle + reverse-second-half + lockstep compare.",
    },
    {
        "id": "ll-odd-even",
        "title": "Segregate Odd-Indexed and Even-Indexed Nodes",
        "step_id": 6,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["linked-list", "pointer-rewiring"],
        "what_this_teaches": "Rewire pointers to weave the list into two sublists (odd-indexed and even-indexed), then attach.",
        "pattern": "Two pointers walking the odd and even chains; alternate next-of-next; finally attach.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": ["ll-reverse"],
        "next_problems": ["ll-sort-012"],
        "resources": [_SHEET, _lc(328, "odd-even-linked-list")],
        "understanding": r'''
Rearrange so all odd-indexed nodes come first, then all
even-indexed (1-indexed positions, so head is position 1 = odd).

`1 -> 2 -> 3 -> 4 -> 5` → `1 -> 3 -> 5 -> 2 -> 4`.

Maintain two chains: `odd` and `even`. Walk both simultaneously,
each taking next-of-next. At the end, link odd's tail to
even's head.
''',
        "optimized": {
            "explanation": "Two-chain interleaving.",
            "code": _LL_NODE_CLASS + r'''

def odd_even_list(head):
    if head is None or head.next is None:
        return head
    odd = head
    even = head.next
    even_head = even
    while even is not None and even.next is not None:
        odd.next = even.next
        odd = odd.next
        even.next = odd.next
        even = even.next
    odd.next = even_head
    return head
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: two chains; alternate next-of-next; link at the end.",
    },
    {
        "id": "ll-remove-nth-from-end",
        "title": "Remove the N-th Node from the End",
        "step_id": 6,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["linked-list", "two-pointers"],
        "what_this_teaches": "Two-pointer technique with a gap of n. The trailing pointer ends at the predecessor of the doomed node.",
        "pattern": "Move first pointer n steps ahead; then move both in lockstep until first is at the end.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": ["ll-middle"],
        "next_problems": ["ll-delete-middle"],
        "resources": [_SHEET, _lc(19, "remove-nth-node-from-end-of-list")],
        "understanding": r'''
Use a dummy head + two pointers with a gap of n.

1. Move the **first** pointer n steps ahead of the dummy.
2. Move both **first** and **second** in lockstep until first
   reaches None.
3. Second now points at the predecessor of the n-th-from-end
   node. Rewire to skip it.
''',
        "optimized": {
            "explanation": "Two pointers with a gap.",
            "code": _LL_NODE_CLASS + r'''

def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    first = second = dummy
    # Move first n steps ahead.
    for _ in range(n):
        first = first.next
    # Move both until first is at the last node.
    while first.next is not None:
        first = first.next
        second = second.next
    # Second is now at the predecessor of the doomed node.
    second.next = second.next.next
    return dummy.next
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: two pointers with a gap of n; trailing pointer ends at predecessor.",
    },
    {
        "id": "ll-delete-middle",
        "title": "Delete the Middle Node",
        "step_id": 6,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["linked-list", "two-pointers"],
        "what_this_teaches": "Slow/fast with a one-step trailing pointer; delete when slow reaches middle.",
        "pattern": "Modified middle-finder that also tracks the previous node.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": ["ll-middle"],
        "next_problems": [],
        "resources": [_SHEET, _lc(2095, "delete-the-middle-node-of-a-linked-list")],
        "understanding": r'''
Find the middle using slow/fast. Maintain a `prev` pointer
trailing slow. When slow is at the middle, rewire `prev.next =
slow.next` to bypass it.
''',
        "optimized": {
            "explanation": "Slow/fast + prev pointer.",
            "code": _LL_NODE_CLASS + r'''

def delete_middle(head):
    if head is None or head.next is None:
        return None
    slow = fast = head
    prev = None
    while fast is not None and fast.next is not None:
        prev = slow
        slow = slow.next
        fast = fast.next.next
    prev.next = slow.next
    return head
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: middle-finder + prev pointer to enable deletion.",
    },
    {
        "id": "ll-sort",
        "title": "Sort a Linked List",
        "step_id": 6,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["linked-list", "sorting", "merge-sort"],
        "what_this_teaches": "Merge sort adapted to linked lists. Splitting and merging are O(1) memory in linked lists.",
        "pattern": "Find middle, split, recursively sort each half, merge.",
        "prerequisite_lessons": ["linked-lists", "sorting"],
        "prerequisite_problems": ["ll-middle", "merge-sort"],
        "next_problems": ["ll-sort-012", "ll-flatten"],
        "resources": [_SHEET, _lc(148, "sort-list")],
        "understanding": r'''
Merge sort is the natural fit for linked lists because:

- Splitting a linked list at the middle is *O(n)* time but
  doesn't need extra memory.
- Merging two sorted linked lists is *O(n)* with constant
  extra memory (rewire pointers).

So merge-sort on linked lists is *O(n log n)* time with *O(log
n)* recursion stack and *O(1)* extra structures.

Quick sort doesn't work as well on linked lists because random
access is required for typical partition schemes.
''',
        "optimized": {
            "explanation": "Recursive merge sort on linked list.",
            "code": _LL_NODE_CLASS + r'''

def merge_two_sorted(a, b):
    # Merge two sorted linked lists into one.
    dummy = ListNode(0)
    tail = dummy
    while a and b:
        if a.val <= b.val:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
    tail.next = a if a else b
    return dummy.next


def sort_list(head):
    if head is None or head.next is None:
        return head
    # Find middle; split.
    slow = fast = head
    prev = None
    while fast and fast.next:
        prev = slow
        slow = slow.next
        fast = fast.next.next
    prev.next = None     # cut the list
    # Recursively sort each half.
    left = sort_list(head)
    right = sort_list(slow)
    return merge_two_sorted(left, right)
''',
            "complexity": "**Time**: *O(n log n)*. **Space**: *O(log n)* recursion.",
        },
        "summary": "**Pattern**: merge sort with linked-list split and merge.",
    },
    {
        "id": "ll-sort-012",
        "title": "Sort a Linked List of 0s, 1s, and 2s",
        "step_id": 6,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["linked-list", "sorting"],
        "what_this_teaches": "Counting-sort-style two-pass: count occurrences; rewrite values. Or three-list approach by value.",
        "pattern": "Build three sublists (0s, 1s, 2s); concatenate.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": ["ll-sort", "sort-0s-1s-2s"],
        "next_problems": [],
        "resources": [_SHEET],
        "understanding": r'''
Two approaches:

**1. Two-pass counting**: count 0s, 1s, 2s; overwrite the list.

**2. Three-list partition**: build three sublists; concatenate.

The three-list approach preserves the original node objects
(no value mutation), which can matter when nodes carry
additional data.
''',
        "optimized": {
            "explanation": "Three-list partition.",
            "code": _LL_NODE_CLASS + r'''

def sort_012(head):
    # Three dummy heads, one per value.
    zero = ListNode(0)
    one = ListNode(0)
    two = ListNode(0)
    z, o, t = zero, one, two
    node = head
    while node is not None:
        if node.val == 0:
            z.next = node
            z = z.next
        elif node.val == 1:
            o.next = node
            o = o.next
        else:
            t.next = node
            t = t.next
        node = node.next
    # Concatenate: 0s -> 1s -> 2s.
    z.next = one.next if one.next else two.next
    o.next = two.next
    t.next = None
    return zero.next
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: three-list partition by value; concatenate.",
    },
    {
        "id": "ll-intersection",
        "title": "Find the Intersection of Two Linked Lists",
        "step_id": 6,
        "lecture_id": 3,
        "difficulty": "easy",
        "tags": ["linked-list", "two-pointers"],
        "what_this_teaches": "Two pointers that switch heads; after at most two passes, they meet at the intersection (or both at None).",
        "pattern": "Walk both lists; when reaching the end, switch to the other list's head.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": ["ll-length"],
        "next_problems": [],
        "resources": [_SHEET, _lc(160, "intersection-of-two-linked-lists")],
        "understanding": r'''
Two linked lists may "merge" at a shared node. Find that node
(or None if they don't intersect).

Elegant algorithm: two pointers, each starting at one head.
Walk both. When a pointer reaches None, redirect it to the
other list's head. After at most `m + n` total steps, both
pointers are at the same node (the intersection, or None).

Why does this work? Both pointers walk a total distance of
`m + n` before they meet. If there's an intersection, they
arrive there together. If not, they both reach None.

*O(m + n)* time, *O(1)* space.
''',
        "optimized": {
            "explanation": "Switch-heads two-pointer.",
            "code": _LL_NODE_CLASS + r'''

def intersection(headA, headB):
    if headA is None or headB is None:
        return None
    a, b = headA, headB
    while a is not b:
        a = a.next if a is not None else headB
        b = b.next if b is not None else headA
    return a
''',
            "complexity": "**Time**: *O(m + n)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: two pointers that switch heads; meet at intersection or at None.",
    },
    {
        "id": "ll-add-one",
        "title": "Add 1 to a Number Represented as a Linked List",
        "step_id": 6,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["linked-list", "math"],
        "what_this_teaches": "Reverse-add-reverse. Or recursion with a carry. The trick is handling the carry from least-significant to most.",
        "pattern": "Reverse, add 1 with carry, reverse back.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": ["ll-reverse"],
        "next_problems": ["ll-add-two-numbers"],
        "resources": [_SHEET],
        "understanding": r'''
The linked list stores digits with the most significant digit
first. Add 1 and return the resulting linked list.

`1 -> 2 -> 9` represents 129. After +1: `1 -> 3 -> 0`.

Two approaches:

1. **Reverse-add-reverse**: reverse the list; add 1 with carry
   from head (now LSB); reverse back. Three passes; *O(n)*.
2. **Recursion with carry**: recurse to the tail; add 1 to the
   tail; propagate carry back up. *O(n)* time, *O(n)* recursion.

Both are fine. Reverse-add-reverse is more intuitive; recursion
is cleaner.
''',
        "optimized": {
            "explanation": "Recursive add-with-carry.",
            "code": _LL_NODE_CLASS + r'''

def add_one(head):
    def helper(node):
        if node is None:
            return 1     # add 1 to the rightmost (least significant) digit
        carry = helper(node.next)
        total = node.val + carry
        node.val = total % 10
        return total // 10

    carry = helper(head)
    if carry:
        # Need a new leading digit.
        return ListNode(carry, head)
    return head
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(n)* recursion.",
        },
        "summary": "**Pattern**: recurse to tail; add 1; propagate carry.",
    },
    {
        "id": "ll-add-two-numbers",
        "title": "Add Two Numbers Represented as Linked Lists",
        "step_id": 6,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["linked-list", "math"],
        "what_this_teaches": "Digit-by-digit addition with carry. The classic linked-list arithmetic problem.",
        "pattern": "Walk both lists in parallel; maintain carry; emit a node per digit.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": ["ll-add-one"],
        "next_problems": [],
        "resources": [_SHEET, _lc(2, "add-two-numbers")],
        "understanding": r'''
Two linked lists represent non-negative integers with the
**least-significant digit first**. Return their sum as a linked
list in the same format.

`(2 -> 4 -> 3) + (5 -> 6 -> 4)` = 342 + 465 = 807 = `(7 -> 0 -> 8)`.

Walk both lists; maintain a carry; emit a new node per digit.
''',
        "optimized": {
            "explanation": "Parallel walk with carry.",
            "code": _LL_NODE_CLASS + r'''

def add_two_numbers(l1, l2):
    dummy = ListNode(0)
    tail = dummy
    carry = 0
    while l1 or l2 or carry:
        a = l1.val if l1 else 0
        b = l2.val if l2 else 0
        total = a + b + carry
        carry = total // 10
        tail.next = ListNode(total % 10)
        tail = tail.next
        if l1: l1 = l1.next
        if l2: l2 = l2.next
    return dummy.next
''',
            "complexity": "**Time**: *O(max(m, n))*. **Space**: *O(max(m, n))* for output.",
        },
        "summary": "**Pattern**: parallel walk + carry; emit one node per digit.",
    },
    # ============================ Lecture 4 — Medium DLL ============================
    {
        "id": "dll-delete-occurrences",
        "title": "Delete All Occurrences of a Key in a DLL",
        "step_id": 6,
        "lecture_id": 4,
        "difficulty": "medium",
        "tags": ["linked-list", "doubly-linked-list"],
        "what_this_teaches": "Walk a DLL; delete nodes by value using the O(1) DLL deletion.",
        "pattern": "Walk; on key match, unlink in O(1) via prev/next pointers.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": ["dll-delete"],
        "next_problems": ["dll-pairs-with-sum", "dll-remove-duplicates"],
        "resources": [_SHEET],
        "understanding": r'''
Walk through the DLL. When a node's value equals the key, unlink
it by rewiring its prev and next neighbors. Handle head and tail
specially.
''',
        "optimized": {
            "explanation": "Walk + O(1) unlink.",
            "code": r'''class DListNode:
    def __init__(self, val: int = 0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next


def delete_all(head, key):
    node = head
    while node is not None:
        nxt = node.next
        if node.val == key:
            # Unlink this node.
            if node.prev: node.prev.next = node.next
            else: head = node.next
            if node.next: node.next.prev = node.prev
        node = nxt
    return head
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: walk + DLL O(1) unlink on key match.",
    },
    {
        "id": "dll-pairs-with-sum",
        "title": "Find Pairs with Given Sum in a Sorted DLL",
        "step_id": 6,
        "lecture_id": 4,
        "difficulty": "medium",
        "tags": ["linked-list", "doubly-linked-list", "two-pointers"],
        "what_this_teaches": "Two-pointer from both ends in a sorted DLL. The prev pointer enables walking right-to-left.",
        "pattern": "Two pointers from head and tail; compare sums; advance accordingly.",
        "prerequisite_lessons": ["linked-lists", "two-pointers"],
        "prerequisite_problems": ["two-sum", "dll-introduction"],
        "next_problems": ["dll-remove-duplicates"],
        "resources": [_SHEET],
        "understanding": r'''
The DLL is sorted ascending. Find all pairs of nodes whose
values sum to the target.

Two pointers: left at head, right at tail. Compare sums:

- Equal: record pair; advance both.
- Less: advance left.
- Greater: advance right.

Continue until pointers meet.
''',
        "optimized": {
            "explanation": "Two pointers in sorted DLL.",
            "code": r'''class DListNode:
    def __init__(self, val: int = 0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next


def pairs_with_sum(head, target):
    # Find tail.
    tail = head
    while tail and tail.next:
        tail = tail.next
    left, right = head, tail
    result = []
    while left is not None and right is not None and left is not right and left.prev is not right:
        s = left.val + right.val
        if s == target:
            result.append((left.val, right.val))
            left = left.next
            right = right.prev
        elif s < target:
            left = left.next
        else:
            right = right.prev
    return result
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: two pointers from both ends of a sorted DLL.",
    },
    {
        "id": "dll-remove-duplicates",
        "title": "Remove Duplicates from a Sorted DLL",
        "step_id": 6,
        "lecture_id": 4,
        "difficulty": "easy",
        "tags": ["linked-list", "doubly-linked-list"],
        "what_this_teaches": "Walk; skip duplicates by unlinking them via DLL pointers.",
        "pattern": "Walk; when next.val == current.val, unlink next.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": ["dll-delete", "remove-duplicates-sorted"],
        "next_problems": [],
        "resources": [_SHEET],
        "understanding": r'''
Walk through the DLL. When two adjacent nodes have the same
value, unlink the second one.
''',
        "optimized": {
            "explanation": "Walk + unlink duplicates.",
            "code": r'''class DListNode:
    def __init__(self, val: int = 0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next


def remove_duplicates(head):
    node = head
    while node is not None and node.next is not None:
        if node.val == node.next.val:
            # Unlink node.next.
            dup = node.next
            node.next = dup.next
            if dup.next:
                dup.next.prev = node
        else:
            node = node.next
    return head
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: walk + unlink consecutive duplicates.",
    },
    # ============================ Lecture 5 — Hard LL ============================
    {
        "id": "ll-reverse-k-group",
        "title": "Reverse Nodes in K-Group",
        "step_id": 6,
        "lecture_id": 5,
        "difficulty": "hard",
        "tags": ["linked-list", "reverse"],
        "what_this_teaches": "Reverse the list k nodes at a time. The challenge is correctly stitching the reversed groups back together.",
        "pattern": "For each k-group, reverse it; link previous group's tail to new head; advance.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": ["ll-reverse"],
        "next_problems": ["ll-rotate"],
        "resources": [_SHEET, _lc(25, "reverse-nodes-in-k-group")],
        "understanding": r'''
Reverse the linked list in groups of k. If the last group has
fewer than k nodes, leave it as is.

`1 -> 2 -> 3 -> 4 -> 5`, k = 2 → `2 -> 1 -> 4 -> 3 -> 5`.

For each group:
1. Check if k nodes remain. If not, stop.
2. Reverse the k nodes.
3. Link the previous group's tail to the new head of this group.
4. Move on.

The bookkeeping for "previous group's tail" is what makes this
problem hard.
''',
        "optimized": {
            "explanation": "Reverse k at a time with careful stitching.",
            "code": _LL_NODE_CLASS + r'''

def reverse_k_group(head, k):
    dummy = ListNode(0, head)
    group_prev = dummy
    while True:
        # Find the kth node ahead.
        kth = group_prev
        for _ in range(k):
            kth = kth.next
            if kth is None:
                return dummy.next
        group_next = kth.next
        # Reverse [group_prev.next ... kth].
        prev, curr = group_next, group_prev.next
        while curr is not group_next:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        # Stitch: group_prev.next (was head of this group) becomes the tail.
        tmp = group_prev.next
        group_prev.next = kth
        group_prev = tmp
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: reverse-then-stitch for each k-group.",
    },
    {
        "id": "ll-rotate",
        "title": "Rotate a Linked List",
        "step_id": 6,
        "lecture_id": 5,
        "difficulty": "medium",
        "tags": ["linked-list"],
        "what_this_teaches": "Connect tail to head (making a circle); walk to the new tail; cut.",
        "pattern": "Compute length; reduce k mod length; find new tail; cut after it.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": ["ll-length"],
        "next_problems": [],
        "resources": [_SHEET, _lc(61, "rotate-list")],
        "understanding": r'''
Rotate the list right by k positions.

`1 -> 2 -> 3 -> 4 -> 5`, k = 2 → `4 -> 5 -> 1 -> 2 -> 3`.

Algorithm:
1. Find length n; the old tail's index.
2. Reduce `k = k % n`.
3. Walk to the new tail (at position n - k - 1).
4. The new head is at position n - k. Cut.
5. Connect the old tail to the old head.

Alternative: connect old tail to old head first (making a
circle); then walk to the new tail; cut.
''',
        "optimized": {
            "explanation": "Make circular; walk; cut.",
            "code": _LL_NODE_CLASS + r'''

def rotate_right(head, k):
    if head is None or head.next is None or k == 0:
        return head
    # Find length and old tail.
    n = 1
    tail = head
    while tail.next is not None:
        tail = tail.next
        n += 1
    k %= n
    if k == 0:
        return head
    # Connect old tail to old head.
    tail.next = head
    # Walk to the new tail (n - k - 1 steps from head).
    new_tail = head
    for _ in range(n - k - 1):
        new_tail = new_tail.next
    new_head = new_tail.next
    new_tail.next = None
    return new_head
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: make the list circular; walk to the new tail; cut.",
    },
    {
        "id": "ll-flatten",
        "title": "Flatten a Multi-Level Linked List",
        "step_id": 6,
        "lecture_id": 5,
        "difficulty": "medium",
        "tags": ["linked-list", "merge"],
        "what_this_teaches": "Repeatedly merge two sorted vertical chains via the 'bottom' pointer.",
        "pattern": "Recursively flatten; merge using 'bottom' pointer as the next direction.",
        "prerequisite_lessons": ["linked-lists"],
        "prerequisite_problems": ["ll-sort", "merge-sort"],
        "next_problems": [],
        "resources": [
            _SHEET,
            {"label": "GFG — Flattening a Linked List",
             "url": "https://www.geeksforgeeks.org/flattening-a-linked-list/"},
        ],
        "understanding": r'''
Each node has a `next` (right) and `bottom` (down) pointer.
Each vertical chain (going down via `bottom`) is sorted. The
entire list, when flattened along `bottom`, should be sorted.

Algorithm: starting from the last column, repeatedly merge the
current column with the result of flattening everything to its
right. The final answer is the head of the leftmost (now
fully-merged) column.

Recursion handles "flatten everything to the right" cleanly.
''',
        "optimized": {
            "explanation": "Recursive flatten + merge.",
            "code": r'''class FlatNode:
    def __init__(self, val=0, next=None, bottom=None):
        self.val = val
        self.next = next
        self.bottom = bottom


def merge(a, b):
    # Merge two sorted chains via the 'bottom' pointer.
    if a is None: return b
    if b is None: return a
    if a.val < b.val:
        a.bottom = merge(a.bottom, b)
        return a
    b.bottom = merge(a, b.bottom)
    return b


def flatten(root):
    if root is None or root.next is None:
        return root
    # Recursively flatten everything to the right first.
    root.next = flatten(root.next)
    # Then merge the current column with the flattened rest.
    return merge(root, root.next)
''',
            "complexity": "**Time**: *O(total nodes * columns)*. **Space**: *O(columns)* recursion.",
        },
        "summary": "**Pattern**: recursive right-to-left merge using 'bottom' as next.",
    },
    {
        "id": "ll-clone-random-pointer",
        "title": "Clone a Linked List with Random Pointers",
        "step_id": 6,
        "lecture_id": 5,
        "difficulty": "medium",
        "tags": ["linked-list", "hashing"],
        "what_this_teaches": "Two approaches: a hash map old→new (O(n) space), or the in-place 'interleave then split' trick (O(1) extra space).",
        "pattern": "Hash map approach is straightforward; interleave-and-split is the elegant O(1) trick.",
        "prerequisite_lessons": ["linked-lists", "hashing"],
        "prerequisite_problems": ["ll-introduction"],
        "next_problems": [],
        "resources": [_SHEET, _lc(138, "copy-list-with-random-pointer")],
        "understanding": r'''
Each node has `val`, `next`, and `random` (which points to any
node in the list or None). Deep-copy the list.

**Approach 1: Hash map**. Walk once, creating new nodes and
storing old→new. Walk again, setting `next` and `random` of
each new node using the map. *O(n)* time and space.

**Approach 2: Interleave-and-split**. *O(n)* time, *O(1)* extra
space:

1. For each old node A, create a new node A' and insert it
   right after A: `A -> A' -> B -> B' -> ...`.
2. Set each A'.random = A.random.next (which is the cloned
   version of A's random target).
3. Split the interleaved list into the original and the clone.
''',
        "optimized": {
            "explanation": "Hash map approach (simplest).",
            "code": r'''class RandNode:
    def __init__(self, val=0, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random


def copy_random_list(head):
    if head is None:
        return None
    # First pass: clone each node, store old -> new mapping.
    old_to_new = {}
    node = head
    while node is not None:
        old_to_new[node] = RandNode(node.val)
        node = node.next
    # Second pass: set next and random on each clone.
    node = head
    while node is not None:
        clone = old_to_new[node]
        clone.next = old_to_new.get(node.next)
        clone.random = old_to_new.get(node.random)
        node = node.next
    return old_to_new[head]
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(n)* for the map.",
        },
        "summary": "**Pattern**: hash map old → new; two passes (clone, then connect).",
    },
]
