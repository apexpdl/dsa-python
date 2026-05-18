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
