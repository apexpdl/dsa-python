"""Linked lists — the first pointer-based data structure."""

LESSON = {
    "id": "linked-lists",
    "title": "Linked Lists — Boxes Connected by Arrows",
    "tags": ["linked-list", "pointers"],
    "summary": (
        "A full beginner chapter. A linked list is a chain of nodes "
        "where each node points to the next. Mastering it builds the "
        "pointer intuition you need for trees, graphs, and everything "
        "else that follows."
    ),
    "body": r'''
## 0. What this chapter teaches

Linked lists are the first **pointer-based** data structure most
beginners meet. They look strange at first — you cannot index
them, you have to chase pointers everywhere — and a beginner's
biggest hurdle is learning to *think* in pointers instead of
indices.

Once you have it, trees, graphs, tries, and many other structures
suddenly feel familiar. They are all "pointer-based" too.

This chapter is the slow walk through linked-list mechanics: the
node, the head, the dummy-head trick, the three-pointer reversal
dance, the tortoise-and-hare cycle trick, and the common pitfalls.
By the end, "linked list" should feel like just another array
with a different access pattern.

## 1. The treasure hunt analogy

Picture a treasure hunt. You find a slip of paper at the start.
It says *"Walk to the big oak tree."* You walk. There you find
another slip: *"Walk to the red bench."* And so on. To get to
the end, you must follow every step in order. You cannot
teleport to the fifth slip — you do not even know where it
physically lives.

A linked list is exactly that. Each **node** carries a value and
a pointer to the next node. To get to the fifth element, you
start at the head and follow `next` pointers four times.

So random access is *O(n)* — you walk. But inserting at the
front, or right after a known node, is *O(1)* — you just rewire
two pointers without moving anything.

That trade-off — slow access, fast splicing — is the whole
personality of a linked list:

- **Array**: instant random access, expensive insertion at
  front.
- **Linked list**: linear-time access, instant front insertion.

## 2. The node

A linked list node in Python is just a tiny class:

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

A value, and a pointer to the next node. The pointer is `None`
for the last node — that is how we recognize the end.

Building a short list:

```python
# Build 1 -> 2 -> 3 -> None
head = ListNode(1, ListNode(2, ListNode(3)))
```

Walking the list:

```python
node = head
while node is not None:
    print(node.val)
    node = node.next
```

This walking pattern is the most reused snippet in linked-list
problems. Write it five times until your fingers know it.

## 3. The dummy-head trick

Beginners get burned over and over by edge cases involving the
head. "What if I am deleting the head node?" "What if the new
node should be inserted before everything?"

The seasoned move: plant a **dummy node** (sometimes called a
sentinel) just before the real head. The dummy never holds a
real value — its only job is to be a stable anchor that
simplifies edge cases.

```python
dummy = ListNode(0)
dummy.next = head
# ... do whatever, treating the head as just "dummy.next" ...
# At the end, return dummy.next as the new head.
```

With the dummy in place, the "head" becomes "the node after
dummy," and you no longer special-case head insertions or
deletions. The code shrinks dramatically.

Whenever you find yourself writing two versions of the same
logic ("one for the head, one for everyone else"), try the dummy
trick. The code usually halves in size.

## 4. The three-pointer reversal

The canonical linked-list problem: reverse a linked list in
place. You flip every `next` pointer to point backwards.

The trick: at each step, you need **three** pointers — the
previous node (the new "tail"), the current node (whose pointer
we're flipping), and the next node (where we were about to go,
which we need to save before flipping).

```python
def reverse(head):
    prev = None
    curr = head
    while curr is not None:
        nxt = curr.next      # save where we were heading
        curr.next = prev     # flip the arrow backwards
        prev = curr          # advance prev
        curr = nxt           # advance curr
    return prev              # prev is the new head
```

Read it as: *"remember where I was going; flip the arrow; step
forward."* Each iteration moves the dance one node to the right.

This three-pointer pattern (`prev / curr / nxt`) is the
**bread-and-butter** of linked-list problems. Reverse k-group,
palindrome detection, reorder list — they all use variations of
this dance.

The recursive version is shorter but uses *O(n)* stack space:

```python
def reverse(head):
    if head is None or head.next is None:
        return head
    new_head = reverse(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

Learn both, prefer iterative in real code (no recursion limit).

## 5. The fast-and-slow trick (Floyd's tortoise and hare)

Two pointers, one moving 1 step per iteration, one moving 2.
Famous uses:

**Find the middle of a list.** Slow ends at the middle when
fast hits the end.

```python
def middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

**Detect a cycle.** If a cycle exists, fast eventually laps slow
and they meet. If no cycle, fast walks off the end.

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
```

**Find the start of the cycle.** After collision, reset one
pointer to head and advance both by 1 step at a time. They meet
at the cycle entry. (See the `ll-detect-loop` problem write-up
for the arithmetic proof.)

This algorithm — Floyd's tortoise and hare — is one of the
prettiest ideas in beginner DSA. It uses constant memory to
detect periodicity in any deterministic step function, not just
linked lists.

## 6. Doubly linked lists

A **doubly linked list** adds a `prev` pointer to each node. You
can walk in both directions, and you can splice out a node in
*O(1)* if you have a pointer to it (because you have both
neighbors).

```python
class DListNode:
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next
```

Doubly linked lists are the foundation of:

- **LRU cache**: doubly linked list of access order plus a hash
  map for *O(1)* lookup. Move-to-front in *O(1)*.
- **Browser history**: walk back and forward.
- **Implementing deque** at a low level.

The cost is more pointers to maintain. Twice the bookkeeping,
twice the chance of bugs.

## 7. Walking discipline — the pointer dance

Linked-list bugs are almost always one of these:

1. **NullPointerException** style: accessing `.next` on `None`.
2. **Lost reference**: overwriting a pointer before stashing the
   old value.
3. **Infinite loop**: introducing a cycle accidentally by
   forgetting to set `.next = None` somewhere.

The cures:

- Always check `if node and node.next` before `node.next.next`.
- Always stash `next_node = curr.next` before mutating
  `curr.next`.
- After splitting a list, always set the boundary `.next = None`.

These three habits, drilled, eliminate most linked-list bugs.

## 8. Recursive thinking on linked lists

Many linked-list problems have elegant recursive solutions
because the structure is itself recursive: a node plus a tail
(which is itself a list).

```python
def length(head):
    if head is None:
        return 0
    return 1 + length(head.next)
```

The leap of faith from the Recursion chapter applies: trust that
`length(head.next)` returns the right count for the tail; add 1
for the current node.

Recursive linked-list code is concise and beautiful, but uses
*O(n)* stack space. For very long lists, prefer iteration.

## 9. Common beginner mistakes

**Mistake 1: losing the reference.** Always stash before
mutating. `next_node = curr.next` is mandatory in reversal.

**Mistake 2: forgetting that the head changes.** When you
modify the list near the head, the original `head` variable
might no longer point to the right node. Use a dummy head, or
return the new head explicitly.

**Mistake 3: infinite loops in cycle problems.** A `while node:`
loop on a cyclic list runs forever. Cycle detection or a node
limit during testing is mandatory.

**Mistake 4: comparing with `==` when you mean `is`.** Two
different `ListNode` objects with the same value are still
different nodes. Use `is` for identity comparisons.

**Mistake 5: forgetting to None-out the tail of a split.** A
half-cut list is a classic source of subtle bugs in problems
like "sort a linked list" or "reorder list."

## 10. End-of-chapter exercise

1. **Reverse a linked list.** Already covered. LeetCode 206.
2. **Middle of a linked list.** Fast/slow pointers. LeetCode 876.
3. **Linked list cycle detection.** Already covered. LeetCode
   141.
4. **Merge two sorted lists.** Dummy head + two pointers.
   LeetCode 21.
5. **Reverse nodes in K-Group.** Hard. Combines reversal with
   carefully splicing the boundaries. LeetCode 25.

Do all five. The last one is the payoff — it forces you to
combine reversal, head replacement, and dummy-head all at once.

## 11. Where to go next

- **Step 6** — the dedicated linked-list curriculum step.
- **Step 13** — trees, which are linked lists with two children.
- **Step 15** — graphs, where every node has many children.

Linked lists are the gateway to all pointer-based structures.
The mental discipline you build here pays off for years.

## 12. Dummy head — the universal life-saver

Many linked-list problems have a special case for the head:
"what if I delete the first node?" "what if the first node
matches?" Special-casing creates branchy code. The dummy head
trick eliminates this:

```python
dummy = ListNode(0)
dummy.next = head
# ... work with prev = dummy and cur = prev.next ...
return dummy.next       # may have changed
```

Now the head is just another node, no special case needed. The
final return is `dummy.next` (which may have been updated).
Common uses: remove-Nth-from-end, remove-duplicates, partition,
merge-two-sorted, insertion-sort-list.

## 13. The fast/slow pointer family

Floyd's tortoise and hare. The slow pointer moves one step at
a time; the fast moves two. Their relative speeds let you
answer questions without knowing the list's length:

- **Find the middle:** when fast reaches the end, slow is at
  the middle.
- **Detect a cycle:** if fast and slow ever meet, there's a
  cycle.
- **Find the cycle's start:** after they meet, reset one
  pointer to head, then move both one step at a time; they
  meet at the cycle's start.
- **Nth-from-end:** start fast N nodes ahead, then move both
  together; when fast reaches the end, slow is at the answer.

All of these run in *O(n)* time and *O(1)* space, with no
auxiliary data structure.

## 14. Reversing a linked list — in detail

The canonical pattern. Master it; reversal appears in dozens
of problems.

```python
def reverse(head):
    prev = None
    cur = head
    while cur:
        nxt = cur.next         # save next before we overwrite
        cur.next = prev        # flip the pointer
        prev = cur             # advance prev
        cur = nxt              # advance cur
    return prev                # new head
```

The dance: three pointers (`prev`, `cur`, `nxt`), each lagging
one step. We save `nxt` first because the next line overwrites
`cur.next`. Then we flip, advance prev, advance cur. At the end,
prev is the new head (the original tail).

**Reversing a sub-range** is the same dance with care at the
boundaries — connect the pre-reversal "before" node to the new
head of the reversed segment, and the reversed tail to the
"after" node.

## 15. Common bugs

**Losing the head reference.** Save the original head before
mutating; if you forget, you can't return it.

**Forgetting `.next = None` on a new tail.** When extracting
or splitting, the new tail's `.next` should be `None`, else
it dangles.

**Off-by-one in N-from-end.** Start fast N nodes ahead, then
move both. Trace it once on a small example.

**Cycles you didn't expect.** If a problem doesn't mention
cycles, your "walk until None" is safe. If cycles are possible,
you must check.

**Recursion on long lists.** Recursive reversal works but
stacks O(n) frames. For lists of 100,000+, use the iterative
version.

## 16. Mental exercises

1. *Reverse `1 -> 2 -> 3 -> 4` step by step. What are `prev,
   cur, nxt` after each iteration?*

2. *Floyd's tortoise and hare: prove (informally) why they
   must meet inside a cycle. What if there's no cycle?*

3. *Remove the 2nd node from end of `1 -> 2 -> 3 -> 4 -> 5`.
   Use the fast/slow trick with a dummy head. Where does
   `slow.next` point after the loop?*

4. *Merge `1 -> 3 -> 5` and `2 -> 4 -> 6` using a dummy head.
   What is the dummy.next chain at the end?*

5. *Why do linked lists win over arrays for "insert in the
   middle"? Where do they lose?*
''',
}
