"""Step 13 — Binary Trees."""
from __future__ import annotations

PROBLEMS: list[dict] = [
    {
        "id": "tree-height",
        "title": "Height (Maximum Depth) of Binary Tree",
        "step_id": 13,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["tree", "recursion", "dfs"],
        "what_this_teaches": (
            "The **postorder recursion** template for tree problems: "
            "ask each subtree first, then combine. Once you can name "
            "the base value and the combine step, almost every "
            "'compute property of every subtree' problem becomes "
            "mechanical."
        ),
        "pattern": "height(node) = 1 + max(height(left), height(right)), base = 0.",
        "prerequisite_lessons": ["recursion", "trees"],
        "prerequisite_problems": [
            "factorial-of-n",
            "print-1-to-n",
        ],
        "next_problems": [
            "tree-balanced",
            "tree-diameter",
            "max-path-sum",
            "trees-identical",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 13 (Binary Trees)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 104 — Maximum Depth of Binary Tree",
                "url": "https://leetcode.com/problems/maximum-depth-of-binary-tree/",
            },
        ],
        "understanding": r'''
The **height** (or **maximum depth**) of a binary tree is the
number of nodes along the longest path from the root to any leaf.
An empty tree has height 0. A single-node tree has height 1.

The recursive definition is so clean that the algorithm writes
itself.
''',
        "brute_force": {
            "explanation": r'''
There is no real brute force here — the recursion is the natural
solution and is optimal.

You could enumerate every root-to-leaf path with DFS and track the
longest. But that explicitly enumerates `O(L)` paths where `L` is
the number of leaves. The recursive version computes the same
answer in `O(N)` total work because each subtree's height is
computed once.
''',
            "code": r'''class TreeNode:
    def __init__(self, val: int = 0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def height_enumerate(root) -> int:
    if root is None:
        return 0
    best = 0
    def go(node, depth):
        nonlocal best
        if node is None:
            return
        if node.left is None and node.right is None:
            best = max(best, depth)
            return
        go(node.left, depth + 1)
        go(node.right, depth + 1)
    go(root, 1)
    return best
''',
            "walkthrough": r'''
A reasonable but verbose first attempt. Walks every node,
tracks the depth as we go, updates the maximum when we hit a
leaf. Works correctly but doesn't show the elegant
"propagate-up" structure that recursion on trees naturally
supports.

**The TreeNode class**

**`class TreeNode:`** — Standard binary tree node.

**`def __init__(self, val: int = 0, left=None, right=None):`** —
Constructor with defaults. Lets us write `TreeNode(5)` for a
leaf, `TreeNode(5, left)` for a left-only, etc.

**`self.val = val; self.left = left; self.right = right`** —
Store the three fields.

**The height function**

**`def height_enumerate(root) -> int:`** — Takes the root,
returns the height.

**`if root is None: return 0`** — Empty tree has height 0.

**`best = 0`** — Will track the maximum depth encountered.

**`def go(node, depth):`** — Inner helper. `node` is the
current node being visited; `depth` is its depth (1-indexed
in this version).

**`nonlocal best`** — Tell Python this variable lives in the
enclosing function's scope, not the inner function. Without
this, `best = max(best, depth)` would create a new local
`best` and the outer one would never update.

**`if node is None: return`** — Skip null nodes. Equivalent
to "an empty subtree contributes no depth."

**`if node.left is None and node.right is None:`** — Leaf
detection.

**`best = max(best, depth); return`** — Update the running
max. Only leaves can be the **deepest** node — internal nodes
have children below them with greater depth.

**`go(node.left, depth + 1); go(node.right, depth + 1)`** —
Recurse into both children with incremented depth.

**`go(root, 1)`** — Start the recursion. Root is at depth 1.

**`return best`** — Return.

This works but feels awkward. We're using a side-effect
(updating `best`) to communicate across recursive calls. A
cleaner approach (the optimized version) returns the height
from each subtree and combines them at the parent.

The cleaner version highlights an important pattern:
**recursion that returns information up** is more natural for
tree problems than **recursion that updates external state**.
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(h)* recursion.",
        },
        "thought_process": r'''
The recursive definition: **height(node) = 1 + max(height(left),
height(right))**, with **height(None) = 0**. One line of math, one
line of code.

Read it as a sentence: *"the height of a tree is one plus the
greater of its two subtrees' heights, and the empty tree has height
zero."* That sentence is the algorithm.

This is the **postorder** pattern: compute the answer for each
subtree first, then combine. Postorder is the right shape whenever
the parent's answer depends on the children's answers.

The recursion uses *O(h)* stack memory where `h` is the height. For
a balanced tree that is *O(log n)*. For a degenerate (linked-list
shaped) tree that is *O(n)*.
''',
        "optimized": {
            "explanation": r'''
Direct recursion. *O(n)* time.
''',
            "code": r'''def max_depth(root) -> int:
    # Base case: an empty subtree has height 0.
    if root is None:
        return 0
    # Recurse into both subtrees and add 1 for the current node.
    left_height = max_depth(root.left)
    right_height = max_depth(root.right)
    return 1 + max(left_height, right_height)
''',
            "walkthrough": r'''
This is the canonical tree recursion. Four lines, beautifully
clear. The "return up" pattern that every tree problem
benefits from.

**`def max_depth(root) -> int:`** — Takes the root, returns
the height (max depth from root to deepest leaf).

**`if root is None: return 0`** — **Base case.** An empty
tree has height 0. This is the natural choice: it means an
empty left or right subtree contributes 0 to the height of
its parent.

**`left_height = max_depth(root.left)`** — Recursively
compute the height of the left subtree. **Trust the recursive
call** — it returns the correct height of whatever it's given.

**`right_height = max_depth(root.right)`** — Same for the
right.

**`return 1 + max(left_height, right_height)`** — The height
of the current subtree is one more than the height of its
deeper child. The `+ 1` accounts for the current node itself;
`max(left, right)` picks the deeper of the two children.

**Why does this work?**

The recursion contract is: "Given a tree, return its height."
The base case handles the empty tree. The recursive case
says: "If I know the heights of the two children, I can
compute my own height as `1 + max(left, right)`."

For an empty tree → return 0. For a leaf (both children are
None) → `left = 0, right = 0`, return `1 + 0 = 1`. For a tree
with a single left child that's a leaf → root sees
`left_height = 1, right_height = 0`, returns
`1 + max(1, 0) = 2`. And so on.

**Trace on a small tree:**
```
       3
      / \
     9   20
        /  \
       15   7
```

`max_depth(20)` → calls `max_depth(15)` and `max_depth(7)`.
Both are leaves, returning 1 each.
`max_depth(20)` returns `1 + max(1, 1) = 2`.

`max_depth(9)` is a leaf → returns 1.

`max_depth(3)` → `1 + max(1, 2) = 3`. Final answer: 3.

Total work: each node is visited exactly once. The function
does *O(1)* work per visit (two recursive calls, an add, a
max). Total *O(n)* time.

Stack space: *O(h)* where `h` is the height of the tree.
Worst case (skewed tree, like a linked list shape):
*O(n)*. Best case (perfectly balanced): *O(log n)*.

The lesson: **let the recursion return what the parent needs.**
For trees, "what the parent needs" is usually a property of
the subtree (height, count, sum, validity flag). The function
contract becomes simple: "input → subtree property output."
The pattern collapses many tree problems to 3-5 lines.
''',
            "complexity": (
                "**Time**: *O(n)* — each node visited once.\n\n"
                "**Space**: *O(h)* recursion depth, where h is tree "
                "height."
            ),
        },
        "deep_concept": r'''
The postorder pattern — *"compute each child first, then combine"*
— powers a huge family of tree problems:

- **Diameter of a tree** — at each node, the longest path through
  it equals `left_height + right_height`. Track the max globally.
- **Balanced tree check** — return height and a balanced flag.
- **Max path sum** — return the best single-side sum to the parent
  and track the best path through the current node globally.
- **Count nodes** — `1 + count(left) + count(right)`.
- **Check identical trees** — both children must match.

The shape is always the same:

```python
def f(node):
    if node is None:
        return base_value
    left = f(node.left)
    right = f(node.right)
    return combine(node, left, right)
```

Once you can name the `base_value` and `combine`, you have the
algorithm. Most "tree DP" problems are this exact shape.
''',
        "confusion_notes": [
            {
                "question": "Why is the base case `return 0` instead of `return 1`?",
                "answer": r'''
Because the base case represents an **empty subtree** (a `None`
pointer), not a leaf node. An empty subtree contributes zero
height; a leaf contributes one.

Walk through `node = single leaf`:
- We call `max_depth(node)`.
- `node` is not `None`, so we recurse into `node.left` and
  `node.right`. Both are `None`.
- Each recursive call hits the base case and returns `0`.
- Back in the leaf call, `left_height = 0, right_height = 0`.
- Return `1 + max(0, 0) = 1`.

Correct: a one-node tree has height 1.

If we had used `return 1` for `None`, the leaf would
incorrectly return `1 + max(1, 1) = 2`, and the whole height
computation would be off by one.

The general rule: **the base case answers the question for the
smallest valid input**, not for a "special" input you want to
handle. For "height of a tree," the smallest valid input is the
empty tree, and its height is by convention 0.

This is the same shape as `factorial(0) = 1` (smallest valid
input, mathematically reasonable) and `sum_of_array([]) = 0`
(empty array's sum is the additive identity).
''',
            },
            {
                "question": "What's the difference between *height* and *depth* of a tree?",
                "answer": r'''
Different sources use these words differently. The
**LeetCode/Striver convention** for this problem is:

- **Height (= maximum depth) of a tree**: the number of nodes
  on the longest path from the root to any leaf. An empty tree
  has height 0; a one-node tree has height 1.

That is what our algorithm computes, and what the LeetCode
problem statement asks for.

Some textbooks distinguish:

- **Height of a node**: the longest path from that node down to
  a leaf, in edges (not nodes). A leaf has height 0 (zero edges
  below it).
- **Depth of a node**: the longest path from the root down to
  that node, in edges. The root has depth 0.
- **Height of a tree**: height of the root.

By that strict convention, a one-node tree has height 0
(because the root is a leaf), not 1.

The off-by-one between "count edges" and "count nodes" matters!
For interview problems, always read the problem statement
carefully and pick a definition. Our `max_depth` returns
**number of nodes on the longest root-to-leaf path**, which is
the LeetCode convention.

If you ever feel uncertain, verify your function on a 1-node
tree. If it returns 1, you are counting nodes. If it returns 0,
you are counting edges.
''',
            },
            {
                "question": "Why is the recursion `O(n)` time but `O(h)` space?",
                "answer": r'''
**Time**: each node is visited exactly once. The function
performs constant work per node (two recursive calls, one
`max`, one `+`). So `n` nodes × constant work = `O(n)` total.

**Space**: the recursion uses the call stack, which holds one
frame per active recursive call. At any moment, the active
frames correspond to the **current path from root to the node
being processed**. The longest such path is the tree's height
`h`.

So peak stack usage is `O(h)`. For a **balanced** tree, `h =
O(log n)` — tiny. For a **degenerate** tree (essentially a
linked list), `h = n` — and the recursion can hit Python's
default 1000-frame recursion limit.

This matters in practice:

- For balanced trees of typical sizes (`n < 10⁶`), recursion
  is fine and uses negligible memory.
- For pathological inputs (a linked-list-shaped tree of 10,000
  nodes), recursion crashes with `RecursionError`. You would
  need iterative traversal with an explicit stack, or to raise
  the recursion limit.

A clean iterative version uses BFS:

```python
from collections import deque

def max_depth_iter(root):
    if root is None:
        return 0
    q = deque([root])
    depth = 0
    while q:
        depth += 1
        for _ in range(len(q)):
            node = q.popleft()
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
    return depth
```

`O(n)` time, `O(w)` space where `w` is the max width. For
balanced trees, `w = O(n / 2)`. So BFS can be **worse** than
DFS on memory for balanced trees but **better** for
degenerate ones. Pick based on the tree shape.
''',
            },
            {
                "question": "How does this generalize to other tree problems?",
                "answer": r'''
Almost every "compute property of each subtree" problem fits
the same skeleton. The variable parts are the **base case
value** and the **combine step**. Here is the family:

```python
def f(node):
    if node is None:
        return BASE_VALUE
    left_result = f(node.left)
    right_result = f(node.right)
    return COMBINE(node, left_result, right_result)
```

| Problem | BASE_VALUE | COMBINE |
|---|---|---|
| Height | 0 | 1 + max(left, right) |
| Count nodes | 0 | 1 + left + right |
| Sum of values | 0 | node.val + left + right |
| Max value | -inf | max(node.val, left, right) |
| Identical trees | True | a.val == b.val and left and right |
| Symmetric tree | True | (children mirror each other) and recurse |
| Is balanced | (0, True) | combine with abs(diff) <= 1 check |

For problems that need TWO answers (one for the parent, one
for a global) — like diameter, max path sum, longest path with
equal values — you use the same skeleton but return a tuple
*or* update a closure variable globally:

```python
best = 0
def f(node):
    nonlocal best
    if node is None:
        return 0
    left = f(node.left)
    right = f(node.right)
    best = max(best, left + right)    # update global
    return 1 + max(left, right)       # return what parent needs
```

Once you can spot "what does my parent need from me?" vs "what
am I trying to track globally?", you have unlocked the vast
majority of tree problems.
''',
            },
        ],
        "summary": r'''
**Pattern**: postorder recursion `combine(node, f(left), f(right))`.

**Lesson**: most tree problems collapse to this template. Identify
the base case (empty subtree) and the combine step.

**Recognize next time**: any "compute property of each subtree"
problem. Height, depth, count, sum, balance, identity — all this
shape.
''',
    },
]
