"""Linked lists — the first pointer-based data structure."""

LESSON = {
    "id": "linked-lists",
    "title": "Linked Lists — Boxes Connected by Arrows",
    "tags": ["linked-list", "pointers"],
    "summary": (
        "A linked list is a chain of nodes where each node points to "
        "the next. Mastering it builds the pointer intuition you need "
        "for trees, graphs, and everything that comes after."
    ),
    "body": r'''
## The treasure hunt analogy

Picture a treasure hunt. You find a slip of paper at the start. It
says: *"Walk to the big oak tree."* You walk there. There you find
another slip: *"Walk to the red bench."* And so on. To get to the
end, you must follow every step in order. You cannot teleport to the
fifth slip — you do not even know where it is.

A linked list is exactly that. Each "node" carries a value and a
pointer to the next node. To get to the fifth element, you start at
the head and follow next pointers four times. Random access is
*O(n)*. But inserting at the front, or right after a known node, is
*O(1)* — you just rewire two pointers.

That trade-off is the whole personality of a linked list:

- **Array**: instant random access, expensive insertion at front.
- **Linked list**: linear-time access, instant front insertion.

## The node

A linked list node in Python is usually just a tiny class. Some
problem statements give you a `ListNode` class for free; here is the
canonical one.

```python
class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None) -> None:
        self.val = val
        self.next = next
```

That is it. A value, and a pointer to the next node. The pointer is
`None` for the last node — that is how we recognize the end.

## Building a linked list

```python
# Build the list 1 -> 2 -> 3 -> None
head = ListNode(1, ListNode(2, ListNode(3)))
```

To walk it, follow the chain:

```python
node = head
while node is not None:
    print(node.val)
    node = node.next
```

This walking pattern is the single most reused snippet in linked-list
problems. Stop and write it five times until your fingers know it.

## The dummy node trick

Beginners get burned over and over by edge cases involving the head.
"What if I am deleting the head node?" "What if the new node should
be inserted before everything?" The seasoned move is a **dummy node**
that sits before the real head.

```python
dummy = ListNode(0)
dummy.next = head
# ... now the head is just "dummy.next", which has no special case.
# At the end, return dummy.next.
```

Whenever you find yourself writing two versions of the code — one for
"the head" and one for "everyone else" — try the dummy trick. The
code halves in size.

## Pattern: two pointers (fast and slow)

The cleverest linked-list tricks come from running two pointers at
different speeds. Two famous uses:

**1. Find the middle.** Slow moves one step at a time; fast moves
two. When fast reaches the end, slow is exactly at the middle.

```python
def middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

**2. Detect a cycle.** If there is a cycle, fast and slow eventually
meet inside it. If there is no cycle, fast falls off the end.

```python
def has_cycle(head) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
```

This is Floyd's tortoise-and-hare algorithm, and it is one of those
results that feels like real magic the first time. The reason it
works is gentle modular arithmetic: in a cycle of length `c`, fast
gains one step per iteration on slow, so within `c` iterations after
both are in the cycle, they must coincide.

## Pattern: reverse a linked list

The classic. We need to flip every pointer to point backward.

```python
def reverse(head):
    prev = None
    curr = head
    while curr is not None:
        nxt = curr.next       # remember where we were heading
        curr.next = prev      # flip the arrow backward
        prev = curr           # advance prev
        curr = nxt            # advance curr
    return prev               # prev is the new head
```

Read it as: *"At each step, pry one arrow off, flip it backward, and
shift both pointers forward."* That sentence is the algorithm.

There is also a recursive version that some find more elegant:

```python
def reverse(head):
    if head is None or head.next is None:
        return head
    new_head = reverse(head.next)
    head.next.next = head     # the node after head now points back to head
    head.next = None          # head becomes the last node
    return new_head
```

It is shorter, but it uses *O(n)* stack space. For very long lists
the iterative version wins.

## Doubly linked lists

A doubly linked list adds a `prev` pointer to each node. The big
advantage is *O(1)* deletion when you have a pointer to a node —
because you have both neighbours and can rewire both sides. The cost
is more pointers to maintain and more bugs to introduce.

```python
class DListNode:
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next
```

Doubly linked lists are the building block of LRU caches: you keep
the items in a doubly linked list (so promotion to the front is
*O(1)*) and a dict mapping keys to nodes (so lookup is *O(1)*).

## Common beginner mistakes

**Mistake 1: losing the reference.** When you rewire pointers, if
you reassign `node.next` before stashing the old value, you lose
access to the rest of the list. Always grab a temporary first.

**Mistake 2: forgetting that the head changes.** Any operation that
might modify or replace the head should return the new head. Use a
dummy node if you want to avoid special-casing.

**Mistake 3: infinite loops in cycle problems.** A `while node:` loop
on a cyclic list runs forever. Detect cycles or use a node count
limit during testing.

**Mistake 4: comparing nodes with `==` when you mean `is`.** Two
different node objects with the same value are different nodes. Use
`is` for identity, `==` only when the class defines `__eq__`.

**Mistake 5: forgetting to `None`-out the previous node's `next` when
splitting.** Half-cut linked lists are a famous source of subtle bugs
in problems like "sort a linked list" or "reorder list".

## The mental model

A linked list is a chain of boxes connected by arrows. To do anything
to a node, you usually need its previous node. The two big weapons
are **two pointers at different speeds** and **the dummy head**. Most
of the famous linked-list problems are some combination of those.

Trees are linked lists with two children. Graphs are linked lists with
many children. So everything you learn here, you reuse forever.
''',
}
