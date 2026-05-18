"""Trees — branching linked lists."""

LESSON = {
    "id": "trees",
    "title": "Trees — Linked Lists That Branch",
    "tags": ["tree", "recursion"],
    "summary": (
        "A binary tree is a node with two children, each of which is "
        "a tree. Once you accept that recursive definition, every tree "
        "problem turns into 'do something here, ask each child'."
    ),
    "body": r'''
## The family tree analogy

Think of a family tree, but tidier. Every person has at most two
children. The "root" is the oldest ancestor; everyone descends from
there. Each person is either a leaf (no children), has one child, or
has two children. That entire structure is a **binary tree**.

The node is the building block. Each node carries a value and two
pointers — to the left child and to the right child.

```python
class TreeNode:
    def __init__(self, val: int = 0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

This is the same shape as a linked list node, except with **two**
`next` pointers instead of one. The fact that the structure
**branches** is what makes trees both more powerful and a bit
trickier than linked lists.

## The recursive definition

This is the most important sentence in this whole lesson:

> **A tree is either empty, or a node with a value and two subtrees.**

That recursive definition is why recursion is the natural tool for
trees. Almost every tree algorithm has the shape:

```
def f(node):
    if node is None:
        return ...        # base case
    # do something at this node
    left_result = f(node.left)
    right_result = f(node.right)
    # combine into the answer for this subtree
```

You see this pattern over and over: ask the left subtree, ask the
right subtree, combine. The leap of faith of recursion is exactly:
*"the children already know their answers, what do I do at this
node?"*

## The four traversals

A traversal is a recipe for visiting every node in the tree. The
order in which you visit determines the algorithm's flavour.

### Preorder: root, left, right

```python
def preorder(node, out):
    if node is None:
        return
    out.append(node.val)
    preorder(node.left, out)
    preorder(node.right, out)
```

Preorder is the order in which you would describe the tree out loud
to someone, top-down. Used to **copy** a tree, to **serialize** it,
and as a building block in many constructive problems.

### Inorder: left, root, right

```python
def inorder(node, out):
    if node is None:
        return
    inorder(node.left, out)
    out.append(node.val)
    inorder(node.right, out)
```

Inorder on a **binary search tree** gives you the values in sorted
order — that single fact is the source of many BST tricks.

### Postorder: left, right, root

```python
def postorder(node, out):
    if node is None:
        return
    postorder(node.left, out)
    postorder(node.right, out)
    out.append(node.val)
```

Postorder is the order in which you would safely **delete** a tree —
you destroy the children before the parent. Many problems that ask
"what does each subtree contribute?" naturally use postorder, because
both children's answers are ready before the parent decides.

### Level order: layer by layer

This one is not recursive. It is BFS with a queue:

```python
from collections import deque

def level_order(root):
    if not root:
        return []
    levels, q = [], deque([root])
    while q:
        size = len(q)
        layer = []
        for _ in range(size):
            node = q.popleft()
            layer.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        levels.append(layer)
    return levels
```

## The decision pattern: postorder is your friend

If a problem asks "for each subtree, compute X", postorder is almost
always the right shape. The child answers are ready before you decide
what to return. Height, diameter, "max path sum", "is balanced",
"is BST" — all postorder.

```python
def max_depth(node) -> int:
    if node is None:
        return 0
    left_depth = max_depth(node.left)
    right_depth = max_depth(node.right)
    return 1 + max(left_depth, right_depth)
```

Read it as a sentence: *"the depth of a tree is 1 plus the deeper of
its two children's depths, and the depth of an empty tree is zero."*
That is the entire algorithm.

## When a tree problem is really two problems

Many medium-hard problems require **two answers** from each subtree:
something for the parent, and something for the global answer. The
classic example is "diameter of a tree".

```python
def diameter(root) -> int:
    best = 0
    def depth(node):
        nonlocal best
        if node is None:
            return 0
        ld = depth(node.left)
        rd = depth(node.right)
        # The longest path THROUGH this node uses both children.
        best = max(best, ld + rd)
        # But what we return up to our parent is the depth, not the diameter.
        return 1 + max(ld, rd)
    depth(root)
    return best
```

The trick is "return one thing, also update a shared global". This
shape recurs constantly: "max path sum", "longest path with same
value", "count subtrees with property X".

## BFS vs DFS in trees

DFS (the recursive traversals above) goes deep first. It uses *O(h)*
memory where `h` is tree height. For balanced trees that is
*O(log n)*; for degenerate trees it is *O(n)*.

BFS (level order) goes wide first. It uses *O(w)* memory where `w`
is the maximum width of the tree. For balanced trees the bottom
layer is *O(n / 2)*, so BFS can use more memory than DFS on a
balanced tree.

Use BFS when the problem cares about depth/distance (level-order
output, minimum depth, "rotten oranges" style spread). Use DFS for
everything else.

## Common beginner mistakes

**Mistake 1: forgetting the `None` base case.** Every recursive tree
function should handle `node is None` first. Otherwise you crash with
`AttributeError: 'NoneType' object has no attribute 'left'`.

**Mistake 2: returning the wrong thing.** When a problem needs two
answers, you have to decide carefully what to return to the parent
and what to maintain as a global. Be explicit.

**Mistake 3: confusing inorder of a BST with inorder of an arbitrary
binary tree.** Inorder of a BST is sorted. Inorder of a random binary
tree is not. Many "validate BST" beginners try to use inorder; this
is a valid approach but you must keep state between visits, not just
collect values.

**Mistake 4: thinking BFS is always cheaper.** It is not. For
non-shortest-path problems, DFS usually wins on memory and
simplicity.

**Mistake 5: writing parent pointers when you do not need them.**
Recursion already gives you a "way back up" via the call stack. Add
parent pointers only when the problem really needs them (e.g.,
distance-k from a node).

## The mental model

A tree is a recursive structure: a node plus two subtrees. Whenever
you face a tree problem, ask: *"what should I do at this node, and
what do I need from my left and right children?"* Write a recursive
function in that shape. Use a global only when one return value is
not enough. That recipe handles a stunning fraction of binary-tree
problems.
''',
}
