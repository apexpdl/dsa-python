"""Trees — branching linked lists."""

LESSON = {
    "id": "trees",
    "title": "Trees — Linked Lists That Branch",
    "tags": ["tree", "recursion"],
    "summary": (
        "A full beginner chapter. A binary tree is a node with two "
        "children, each of which is a tree. Once you accept that "
        "recursive definition, every tree problem turns into 'do "
        "something here, ask each child'."
    ),
    "body": r'''
## 0. What this chapter teaches

Trees are where recursion finally pays off. Once you internalize
"a tree is a node plus two subtrees," every tree problem
collapses into the same template: do something at the current
node, recurse into the children, combine.

This chapter is the slow walk through that template. We will
cover the four traversals, the postorder pattern that powers
most tree DP, the BFS-on-trees trick for level problems, and
the "two return values" technique that solves harder problems
like diameter and max path sum.

By the end, "tree problem" should feel like a class of related
exercises with one shared mental model.

## 1. The family tree analogy

Think of a family tree, but tidier. Every person has at most two
children. The **root** is the oldest ancestor; everyone descends
from there. Each person is either a **leaf** (no children), has
one child, or has two children. That entire structure is a
**binary tree**.

In code:

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

Same shape as a linked-list node, but with **two** `next`
pointers instead of one — and we call them `left` and `right`.
The fact that the structure **branches** is what makes trees
both more powerful and more interesting than linked lists.

## 2. The recursive definition

This is the most important sentence in the chapter:

> **A tree is either empty (a `None` pointer), or a node with a
> value and two subtrees.**

That recursive definition is why recursion is the natural tool
for trees. Almost every tree algorithm has the shape:

```python
def f(node):
    if node is None:
        return BASE_VALUE
    left_result = f(node.left)
    right_result = f(node.right)
    return COMBINE(node, left_result, right_result)
```

This template handles dozens of problems with only the BASE and
COMBINE parts changing. Memorize the shape; the rest is filling
in two blanks.

## 3. The four traversals

A **traversal** is an order in which we visit every node. The
choice of order determines the algorithm's flavor.

### Preorder: root, then left, then right

```python
def preorder(node, out):
    if node is None:
        return
    out.append(node.val)
    preorder(node.left, out)
    preorder(node.right, out)
```

Preorder is "top-down." Used to **copy** a tree, **serialize**
it, or describe it level by level downward.

### Inorder: left, then root, then right

```python
def inorder(node, out):
    if node is None:
        return
    inorder(node.left, out)
    out.append(node.val)
    inorder(node.right, out)
```

Inorder on a **binary search tree** yields the values in **sorted
order**. That single fact is the source of many BST tricks.

### Postorder: left, then right, then root

```python
def postorder(node, out):
    if node is None:
        return
    postorder(node.left, out)
    postorder(node.right, out)
    out.append(node.val)
```

Postorder is "bottom-up." The order in which you would safely
delete a tree (children before parent). Almost every "compute
property of each subtree" problem is postorder — both children's
answers are ready before the parent decides.

### Level order: BFS, layer by layer

```python
from collections import deque

def level_order(root):
    if root is None:
        return []
    levels = []
    q = deque([root])
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

Level order is the BFS traversal. Used whenever the problem cares
about **depth**: minimum depth, level averages, level sums,
right-side view, etc.

## 4. The postorder mental model

Postorder is the most useful traversal for problem-solving.
Whenever the answer at a node depends on the answers at its
children, postorder is your shape.

Height of a tree:

```python
def height(node):
    if node is None:
        return 0
    return 1 + max(height(node.left), height(node.right))
```

Read it as a sentence: *"the height of a tree is one plus the
greater of its two subtrees' heights; an empty tree has height
zero."* That sentence is the algorithm.

Other problems with the same shape (postorder + combine):

- **Diameter**: longest path between any two leaves.
- **Max path sum**: largest sum on any path through the tree.
- **Count nodes**: 1 + count(left) + count(right).
- **Sum of values**: node.val + sum(left) + sum(right).
- **Balanced check**: height plus a balanced flag.
- **Identical trees**: check both children match.
- **Symmetric tree**: check children mirror each other.

The template stays the same; the BASE_VALUE and COMBINE change.

## 5. The "two return values" trick

Many medium problems need **two answers** at each subtree —
something for the parent, plus something for a global maximum.
The classic example: tree diameter.

The diameter of a tree is the longest path between any two
nodes. At each node, the longest path **through** it is `left
height + right height`. But the parent doesn't want that
through-path value — it wants the longest single-side downward
extension, which is `1 + max(left height, right height)`.

So we return one thing (the single-side height) and update a
global with the other (the through-path length):

```python
def diameter(root):
    best = 0
    def depth(node):
        nonlocal best
        if node is None:
            return 0
        ld = depth(node.left)
        rd = depth(node.right)
        best = max(best, ld + rd)         # update global
        return 1 + max(ld, rd)            # return what parent needs
    depth(root)
    return best
```

This pattern — "return one thing, also update a global" — recurs
constantly: max path sum, longest path with same value, count
subtrees with property P, longest univalue path. Once you can
identify what the parent needs versus what the answer is, the
solution writes itself.

## 6. BFS vs DFS on trees

DFS (the recursive traversals above) goes deep first. Uses *O(h)*
memory where `h` is tree height. For balanced trees that's
*O(log n)*; for degenerate trees, *O(n)*.

BFS (level order) goes wide first. Uses *O(w)* memory where `w`
is the maximum width of the tree. For balanced trees, the bottom
layer is *O(n/2)*, so BFS can use **more** memory than DFS on a
balanced tree.

Choose based on the question:

- **Depth/distance**: BFS. ("Minimum depth," "level sums,"
  "right side view.")
- **Subtree properties**: DFS (postorder). ("Height," "diameter,"
  "max path sum.")
- **Iterating in sorted order**: DFS (inorder on BST).
- **Serializing or constructing**: DFS (preorder or post-/inorder
  combo).

## 7. Iterative tree traversals

Recursion is the natural shape, but for very deep trees (long
chains), Python's recursion limit (~1000 by default) can crash.
Iterative traversals use an explicit stack and bypass the limit.

Iterative inorder (the most-tested):

```python
def inorder_iter(root):
    out = []
    stack = []
    node = root
    while node or stack:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        out.append(node.val)
        node = node.right
    return out
```

The trick: walk down the leftmost spine, push everything onto
the stack. Pop a node, output it, then jump to its right
subtree and repeat.

Iterative versions exist for preorder and postorder too — see
the curriculum's Step 13 for full implementations and the
Morris-traversal trick (which uses *O(1)* extra memory by
temporarily threading the tree).

## 8. Common beginner mistakes

**Mistake 1: forgetting the None base case.** Every recursive
tree function must check `if node is None` first. Without it,
you crash with `AttributeError: 'NoneType' object has no
attribute 'left'`.

**Mistake 2: returning the wrong thing.** When a problem needs
two answers (parent's plus global), be explicit about which one
you return. Mixing them up is the most common diameter bug.

**Mistake 3: confusing inorder of a BST with inorder of any
binary tree.** Inorder of a BST is sorted. Inorder of a random
binary tree is not. "Validate BST" beginners sometimes use
inorder; it works only if you carry the previous value across
recursive calls.

**Mistake 4: thinking BFS is always cheaper than DFS.** It is
not. For non-shortest-path problems, DFS usually wins on memory
and simplicity.

**Mistake 5: writing parent pointers when you do not need them.**
Recursion already gives you a "way back up" via the call stack.
Add parent pointers only when the problem really needs them
(e.g., distance-K from a node).

## 9. End-of-chapter exercise

1. **Maximum depth of binary tree.** Postorder, base 0, combine
   1 + max. LeetCode 104.
2. **Same tree.** Check two trees for equality. LeetCode 100.
3. **Symmetric tree.** Check children-mirror property.
   LeetCode 101.
4. **Diameter of binary tree.** The "two return values" trick.
   LeetCode 543.
5. **Binary tree level order traversal.** BFS with level_size
   snapshot. LeetCode 102.

Do all five. After the diameter problem, you should be able to
identify "two return values" problems on sight.

## 10. Where to go next

- **Step 13** — full binary tree curriculum, including hard
  problems and iterative traversals.
- **Step 14** — binary search trees, with the inorder-sorted
  property exploited.
- **Step 15** — graphs, the generalization of trees to many
  children and cycles.
- **Step 17** — tries, which are trees of characters.

Trees are the most natural home for recursion. Master the
template here and a third of the curriculum becomes mechanical.
''',
}
