"""Step 13 extras — Binary Trees (32 problems).

Covers: traversals (preorder, inorder, postorder, level-order, all-in-one,
morris), tree shape/property checks, views (top/bottom/left/right/
vertical), path problems (root-to-node, LCA, k-distance, burning),
construction (pre+in, post+in), serialization, flatten, complete tree
counting, and more.
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


PROBLEMS: list[dict] = [
    # ------------------------------------------------------------------
    # 1) Tree Introduction
    # ------------------------------------------------------------------
    {
        "id": "tree-introduction",
        "title": "Introduction to Trees",
        "step_id": 13,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["tree", "concept"],
        "what_this_teaches": "What a tree is, vocabulary (root, leaf, parent, child, depth, height), and how a binary tree differs from a general tree.",
        "pattern": "Conceptual overview.",
        "prerequisite_lessons": [],
        "prerequisite_problems": [],
        "next_problems": ["binary-tree-representation", "preorder"],
        "resources": [
            {"label": "Wikipedia — Tree (data structure)", "url": "https://en.wikipedia.org/wiki/Tree_(data_structure)"},
            _SHEET,
        ],
        "understanding": r'''
A **tree** is a hierarchical data structure where each element (a *node*)
has at most one **parent** and any number of **children**. The single
node with no parent is the **root**; nodes with no children are
**leaves**. Crucially, trees have *no cycles* — if you follow any
parent-to-child chain you eventually hit a leaf.

A **binary tree** is the special case where each node has at most 2
children (called left and right). This restriction is huge: it makes
recursion natural (two recursive subcases per node) and lets us store
the tree in a flat array (used for heaps).

**Key terminology:**
- **Depth** of a node = distance from root (root has depth 0).
- **Height** of a node = distance to the *farthest* leaf below it.
- **Height of the tree** = height of the root.
- **Subtree** rooted at v = v and all of v's descendants.

**Why are trees everywhere?** Because hierarchies are everywhere: file
systems, DOM, JSON, decision logic, expression parsing, organization
charts, BSTs, tries, segment trees. Master binary trees and you've laid
the foundation for graphs.
''',
        "brute_force": {
            "explanation": "Conceptual lesson — no algorithm.",
            "code": "",
            "complexity": "—",
        },
        "thought_process": "Internalize the vocabulary before writing any code. Confusing 'depth' and 'height' is the #1 source of off-by-one bugs in tree problems.",
        "optimized": {
            "explanation": r'''
A minimal Python representation of a binary tree node:
''',
            "code": r'''
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
''',
            "complexity": "—",
        },
        "deep_concept": r'''
Mathematically, a binary tree with n nodes has exactly n − 1 edges
(every node except the root has one parent edge). The minimum possible
height is ⌊log₂ n⌋ (perfectly balanced); the maximum is n − 1
(degenerate chain).
''',
        "confusion_notes": [
            {
                "question": "Is the root at depth 0 or depth 1?",
                "answer": "Convention varies. In Striver and most DSA references, root depth = 0. In some textbooks (and the LeetCode problem 'Depth of binary tree') the root depth = 1. Always check the problem statement.",
            },
            {
                "question": "Are 'depth' and 'level' the same?",
                "answer": "Usually yes, with 'level' meaning depth + 1 (root = level 1). 'Depth' is more common in algorithm contexts; 'level' shows up in BFS / level-order traversal.",
            },
        ],
        "summary": "Tree = root + hierarchical parent-child links, no cycles. Binary tree restricts children to ≤ 2. Master the vocabulary: depth, height, leaf, subtree.",
    },

    # ------------------------------------------------------------------
    # 2) Binary Tree Representation
    # ------------------------------------------------------------------
    {
        "id": "binary-tree-representation",
        "title": "Binary Tree Representation in Memory",
        "step_id": 13,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["tree", "representation"],
        "what_this_teaches": "Linked-node and array-based representations.",
        "pattern": "Trade-offs in storage.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["tree-introduction"],
        "next_problems": ["preorder"],
        "resources": [
            {"label": "GFG — Binary Tree Representation", "url": "https://www.geeksforgeeks.org/binary-tree-set-1-introduction/"},
            _SHEET,
        ],
        "understanding": r'''
Two main representations:

**1. Linked-node** (what we'll use 99% of the time). Each node is an
object with `left`, `right`, and `val` fields. Adding/removing nodes is
cheap; memory is proportional to nodes.

**2. Array (heap-style)**. Store node i at index `i`, with children at
`2i + 1` and `2i + 2`. Works for *complete* binary trees (no gaps).
Sparse trees would waste huge swaths of array.

For competitive programming and most interview problems, linked nodes
win. Array representation excels for:
- Heaps (always complete).
- Segment trees and Fenwick trees (specialized layouts).
- Serialization formats (LeetCode's level-order strings).
''',
        "brute_force": {
            "explanation": "Demonstration of both forms.",
            "code": "",
            "complexity": "—",
        },
        "thought_process": "Linked nodes for flexibility; arrays for compact, complete structures.",
        "optimized": {
            "explanation": r'''
Linked-node and array representations side-by-side.
''',
            "code": r'''
# Linked
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val; self.left = left; self.right = right

# Array (heap-style)
# Tree:        1
#            /   \
#           2     3
#          / \
#         4   5
tree_array = [1, 2, 3, 4, 5]
def left_idx(i):  return 2 * i + 1
def right_idx(i): return 2 * i + 2
def parent_idx(i): return (i - 1) // 2
''',
            "complexity": "—",
        },
        "deep_concept": r'''
Array representation is **cache-friendly** because nodes near each other
in the tree are near each other in memory. That's why heaps in CPython
beat hand-rolled linked-heap implementations.
''',
        "confusion_notes": [
            {
                "question": "Why don't general (non-binary) trees use arrays?",
                "answer": "Because nodes can have any number of children, and we'd have to store children-counts and offsets — the simple `2i+1` / `2i+2` math doesn't work. Use linked nodes or adjacency lists for general trees.",
            },
        ],
        "summary": "Linked nodes for flexibility; arrays for complete binary trees (heaps). Most binary-tree problems use linked nodes.",
    },

    # ------------------------------------------------------------------
    # 3) Preorder Traversal
    # ------------------------------------------------------------------
    {
        "id": "preorder",
        "title": "Preorder Traversal (Root → Left → Right)",
        "step_id": 13,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["tree", "traversal", "dfs"],
        "what_this_teaches": "DFS traversal in preorder. Recursive and iterative (with a stack).",
        "pattern": "DFS pre-order.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["binary-tree-representation"],
        "next_problems": ["inorder", "postorder"],
        "resources": [
            _lc(144, "binary-tree-preorder-traversal"),
            _SHEET,
        ],
        "understanding": r'''
**Preorder** = process the *root* first, then recurse into the left
subtree, then the right.

For tree:
```
        1
       / \
      2   3
     / \
    4   5
```
Preorder: `1, 2, 4, 5, 3`.

Preorder is useful for **serializing** a tree (root-first encoding is
naturally reconstructable), for **copying** a tree, and for printing
nested expressions / outlines.
''',
        "brute_force": {
            "explanation": "The recursive version *is* the natural solution. The iterative version with an explicit stack is what we present as 'optimized' for the interview-friendly variant.",
            "code": r'''
def preorder_recursive(root):
    if not root:
        return []
    return [root.val] + preorder_recursive(root.left) + preorder_recursive(root.right)
''',
            "complexity": "Time O(n), space O(h) recursion stack (h = tree height).",
        },
        "thought_process": r'''
Iterative version uses an explicit stack. Push the root; pop and emit
its value; push the *right* child first then the *left* child (so left
is popped next, preserving order).
''',
        "optimized": {
            "explanation": "Stack-based iterative preorder.",
            "code": r'''
def preorder_iterative(root):
    if not root: return []
    out = []
    stack = [root]
    while stack:
        node = stack.pop()
        out.append(node.val)
        if node.right:
            stack.append(node.right)        # push right first
        if node.left:
            stack.append(node.left)         # so left pops next
    return out
''',
            "complexity": "Time O(n), space O(h).",
        },
        "deep_concept": r'''
DFS traversals correspond directly to the order in which the recursion
'visits' a node. Preorder visits when entering, inorder visits between
left and right, postorder visits when leaving.
''',
        "confusion_notes": [
            {
                "question": "Why push right *before* left when going iterative?",
                "answer": "A stack is LIFO. Whatever we push last is popped first. We want left visited next, so we push right first (it gets popped later) and left second (popped immediately).",
            },
        ],
        "summary": "Preorder = Root, Left, Right. Recursion is one-liner; iterative uses a stack with right pushed before left.",
    },

    # ------------------------------------------------------------------
    # 4) Inorder Traversal
    # ------------------------------------------------------------------
    {
        "id": "inorder",
        "title": "Inorder Traversal (Left → Root → Right)",
        "step_id": 13,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["tree", "traversal", "dfs"],
        "what_this_teaches": "Inorder DFS — recursive and iterative.",
        "pattern": "DFS in-order.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["preorder"],
        "next_problems": ["postorder", "morris-inorder"],
        "resources": [
            _lc(94, "binary-tree-inorder-traversal"),
            _SHEET,
        ],
        "understanding": r'''
**Inorder** = recurse left, then visit root, then recurse right.

For our example tree:
```
        1
       / \
      2   3
     / \
    4   5
```
Inorder: `4, 2, 5, 1, 3`.

**Inorder on a BST gives sorted output** — this is the most important
fact about inorder. Many BST problems reduce to "do inorder, then
process the resulting array".
''',
        "brute_force": {
            "explanation": "Recursion is natural.",
            "code": r'''
def inorder_recursive(root):
    if not root:
        return []
    return inorder_recursive(root.left) + [root.val] + inorder_recursive(root.right)
''',
            "complexity": "Time O(n), space O(h).",
        },
        "thought_process": "Iterative inorder uses a stack and the trick: keep going left, pushing nodes; when you can't go further, pop and emit, then go right.",
        "optimized": {
            "explanation": "Iterative inorder with explicit stack.",
            "code": r'''
def inorder_iterative(root):
    out, stack = [], []
    cur = root
    while cur or stack:
        while cur:
            stack.append(cur)
            cur = cur.left           # go as far left as possible
        cur = stack.pop()            # backtrack to the most recent unvisited
        out.append(cur.val)          # emit
        cur = cur.right              # now do right subtree
    return out
''',
            "complexity": "Time O(n), space O(h).",
        },
        "deep_concept": r'''
The iterative inorder algorithm is essentially simulating the recursive
call stack. The 'go left as long as possible' loop is equivalent to the
recursive descent, while the pop+emit+right captures the 'visit and
recurse right' step.
''',
        "confusion_notes": [
            {
                "question": "Why does inorder on a BST give sorted order?",
                "answer": "Because BST invariant: all of left subtree < root < all of right subtree. So inorder visits everything < root, then root, then everything > root — recursively, this yields sorted output.",
            },
        ],
        "summary": "Inorder = Left, Root, Right. On a BST: sorted. Iterative uses a stack and 'go left while you can'.",
    },

    # ------------------------------------------------------------------
    # 5) Postorder Traversal
    # ------------------------------------------------------------------
    {
        "id": "postorder",
        "title": "Postorder Traversal (Left → Right → Root)",
        "step_id": 13,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["tree", "traversal", "dfs"],
        "what_this_teaches": "Postorder DFS, recursive and iterative.",
        "pattern": "DFS post-order.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["inorder"],
        "next_problems": ["level-order", "morris-preorder"],
        "resources": [
            _lc(145, "binary-tree-postorder-traversal"),
            _SHEET,
        ],
        "understanding": r'''
**Postorder** = recurse left, recurse right, visit root.

For our example tree:
```
        1
       / \
      2   3
     / \
    4   5
```
Postorder: `4, 5, 2, 3, 1`.

Postorder is the order in which a tree must be deleted (free children
before parent), the order for evaluating postfix expressions, and the
natural order for computing 'value at this node depends on children'.
''',
        "brute_force": {
            "explanation": "Recursion is natural.",
            "code": r'''
def postorder_recursive(root):
    if not root:
        return []
    return (postorder_recursive(root.left)
          + postorder_recursive(root.right)
          + [root.val])
''',
            "complexity": "Time O(n), space O(h).",
        },
        "thought_process": "Iterative postorder is the trickiest of the three. Easiest trick: do *modified preorder* (root, right, left) iteratively, then reverse the result. Or use two stacks.",
        "optimized": {
            "explanation": "Modified-preorder-then-reverse for postorder.",
            "code": r'''
def postorder_iterative(root):
    if not root: return []
    out = []
    stack = [root]
    while stack:
        node = stack.pop()
        out.append(node.val)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    return out[::-1]                # reverse modified-preorder to get postorder
''',
            "complexity": "Time O(n), space O(h).",
        },
        "deep_concept": r'''
Postorder is the *natural* DFS finish order when treating the tree as a
graph. Every postorder property has a graph analog: topological sort,
SCC component IDs, dominator-tree post-numbers, etc.
''',
        "confusion_notes": [
            {
                "question": "Why does the 'preorder with right first, then reverse' trick work?",
                "answer": "Modified preorder (root, right, left) when reversed gives (left, right, root) — which is postorder. It's a clean way to avoid the more complex two-stack approach.",
            },
        ],
        "summary": "Postorder = Left, Right, Root. Iterative: do (root, right, left) preorder with a stack and reverse the result.",
    },

    # ------------------------------------------------------------------
    # 6) Level Order Traversal
    # ------------------------------------------------------------------
    {
        "id": "level-order",
        "title": "Level Order Traversal (BFS)",
        "step_id": 13,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["tree", "bfs", "queue"],
        "what_this_teaches": "BFS on a tree. Process nodes level by level using a queue.",
        "pattern": "Queue-based BFS.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["postorder"],
        "next_problems": ["all-traversals-one-pass", "zigzag-traversal"],
        "resources": [
            _lc(102, "binary-tree-level-order-traversal"),
            _SHEET,
        ],
        "understanding": r'''
Visit nodes level by level: root first, then all depth-1 nodes, then
all depth-2 nodes, and so on. Within a level, go left-to-right.

For:
```
        1
       / \
      2   3
     / \
    4   5
```
Level-order: `[[1], [2, 3], [4, 5]]`.

This is **BFS** applied to a tree.
''',
        "brute_force": {
            "explanation": "We jump to the standard BFS implementation.",
            "code": "",
            "complexity": "—",
        },
        "thought_process": r'''
Use a queue (deque in Python for O(1) popleft). For each level, pop
exactly `level_size = len(queue)` nodes before moving on. This separates
levels into groups.
''',
        "optimized": {
            "explanation": "BFS with deque.",
            "code": r'''
from collections import deque

def level_order(root):
    if not root: return []
    out = []
    q = deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        out.append(level)
    return out
''',
            "complexity": "Time O(n), space O(width) where width = max nodes at any level.",
        },
        "deep_concept": r'''
BFS on a binary tree is identical to BFS on a graph, with the key
difference that we never need a 'visited' set — trees have no cycles.
This makes tree BFS the cheapest BFS variant.
''',
        "confusion_notes": [
            {
                "question": "Why `for _ in range(len(q))` instead of just iterating?",
                "answer": "We capture the *current* level's size *before* the loop adds children. Otherwise the inner loop would keep extending into the next level. Saving `len(q)` at the start is the key idiom.",
            },
        ],
        "summary": "BFS with a deque; capture level size at the start of each iteration; append children, then append the level to output.",
    },

    # ------------------------------------------------------------------
    # 7) All Traversals in One Pass
    # ------------------------------------------------------------------
    {
        "id": "all-traversals-one-pass",
        "title": "Preorder + Inorder + Postorder in One Iteration",
        "step_id": 13,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["tree", "traversal", "stack"],
        "what_this_teaches": "Simulate the recursive call stack with a state machine; emit each node into one of three lists based on its visit phase.",
        "pattern": "Stack of (node, state) pairs.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["preorder", "inorder", "postorder"],
        "next_problems": ["max-path-sum"],
        "resources": [
            {"label": "Striver — All traversals", "url": "https://takeuforward.org/data-structure/preorder-inorder-postorder-traversals-in-one-traversal/"},
            _SHEET,
        ],
        "understanding": r'''
Compute preorder, inorder, and postorder simultaneously in a single
linear scan, using one stack.
''',
        "brute_force": {
            "explanation": "Three separate traversals. O(3n) time. The 'one-pass' version saves only a constant factor but is a beloved interview problem because it shows mastery of the DFS state machine.",
            "code": "",
            "complexity": "Time O(n).",
        },
        "thought_process": r'''
Each node has three 'phases' during DFS:
- Phase 1: emit to preorder, push (node, 2) back, then descend left.
- Phase 2: emit to inorder, push (node, 3) back, then descend right.
- Phase 3: emit to postorder.

Use a stack of (node, phase) tuples. Pop one, branch on phase.
''',
        "optimized": {
            "explanation": "State-machine DFS on a single stack.",
            "code": r'''
def all_traversals(root):
    pre = []; ino = []; post = []
    if not root:
        return pre, ino, post
    stack = [(root, 1)]
    while stack:
        node, phase = stack.pop()
        if phase == 1:
            pre.append(node.val)
            stack.append((node, 2))
            if node.left:
                stack.append((node.left, 1))
        elif phase == 2:
            ino.append(node.val)
            stack.append((node, 3))
            if node.right:
                stack.append((node.right, 1))
        else:                       # phase == 3
            post.append(node.val)
    return pre, ino, post
''',
            "complexity": "Time O(n), space O(h).",
        },
        "deep_concept": r'''
Each node is touched at most three times; the total work is O(3n) =
O(n). The state machine generalizes to many problems where DFS needs
to do work both 'on the way down' and 'on the way up'.
''',
        "confusion_notes": [
            {
                "question": "Why push (node, 2) *before* descending left?",
                "answer": "Because stack is LIFO. The left descent must happen first, so it's pushed last. The (node, 2) waits underneath until the left subtree finishes.",
            },
        ],
        "summary": "Stack of (node, phase). Phase 1 = preorder + go left; Phase 2 = inorder + go right; Phase 3 = postorder.",
    },

    # ------------------------------------------------------------------
    # 8) Check Balanced Tree
    # ------------------------------------------------------------------
    {
        "id": "tree-balanced",
        "title": "Check if Binary Tree is Height-Balanced",
        "step_id": 13,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["tree", "dfs", "recursion"],
        "what_this_teaches": "Compute height and balance flag in a *single* DFS, using a sentinel value to propagate failure.",
        "pattern": "Combined height + property DFS.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["tree-height"],
        "next_problems": ["tree-diameter"],
        "resources": [
            _lc(110, "balanced-binary-tree"),
            _SHEET,
        ],
        "understanding": r'''
A binary tree is **height-balanced** iff for *every* node, the heights
of its left and right subtrees differ by at most 1.

Return True iff the entire tree is height-balanced.
''',
        "brute_force": {
            "explanation": "For each node compute left and right heights and check the difference. That's O(n²) because each height call is itself O(n).",
            "code": r'''
def is_balanced_brute(root):
    def h(n):
        if not n: return 0
        return 1 + max(h(n.left), h(n.right))
    def check(n):
        if not n: return True
        if abs(h(n.left) - h(n.right)) > 1: return False
        return check(n.left) and check(n.right)
    return check(root)
''',
            "complexity": "Time O(n²).",
        },
        "thought_process": r'''
**Single-pass DFS.** From each subtree return either the height or a
sentinel (e.g., -1) meaning 'unbalanced'. The parent checks: if either
child returned -1, return -1; if |lh - rh| > 1, return -1; else return
1 + max(lh, rh).
''',
        "optimized": {
            "explanation": "Sentinel-propagating DFS.",
            "code": r'''
def is_balanced(root):
    def dfs(n):
        if not n: return 0
        lh = dfs(n.left)
        if lh == -1: return -1
        rh = dfs(n.right)
        if rh == -1: return -1
        if abs(lh - rh) > 1: return -1
        return 1 + max(lh, rh)
    return dfs(root) != -1
''',
            "complexity": "Time O(n), space O(h).",
        },
        "deep_concept": r'''
The 'compute height + property in one DFS' pattern is everywhere in
tree problems. It saves the redundant work of recomputing heights from
each node. The sentinel `-1` cleanly conveys 'unbalanced' without
needing a separate boolean.
''',
        "confusion_notes": [
            {
                "question": "Why use -1 as the failure sentinel and not raise an exception?",
                "answer": "Both work; -1 is simpler and idiomatic in iterative DSA. Exceptions add Python overhead and obscure the recursion. Choose whichever style matches the codebase.",
            },
        ],
        "summary": "DFS returning height or -1 (unbalanced). O(n) single pass.",
    },

    # ------------------------------------------------------------------
    # 9) Tree Diameter
    # ------------------------------------------------------------------
    {
        "id": "tree-diameter",
        "title": "Diameter of Binary Tree",
        "step_id": 13,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["tree", "dfs"],
        "what_this_teaches": "At each node, the longest path *through* it is `left_height + right_height`. Track the global max.",
        "pattern": "DFS returning height + side-effect on global max.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["tree-balanced"],
        "next_problems": ["max-path-sum"],
        "resources": [
            _lc(543, "diameter-of-binary-tree"),
            _SHEET,
        ],
        "understanding": r'''
**Diameter** = longest path between any two nodes in the tree (length
measured in edges).

The trick: for any node, the longest path through it equals
`height(left) + height(right)`. The diameter is the max of this over
all nodes.
''',
        "brute_force": {
            "explanation": "For each node compute both heights → O(n²).",
            "code": "",
            "complexity": "Time O(n²).",
        },
        "thought_process": "Combine: DFS returns height, but on the way back up also updates a global max with `lh + rh`.",
        "optimized": {
            "explanation": "Single-pass DFS.",
            "code": r'''
def diameter_of_binary_tree(root):
    best = [0]
    def h(n):
        if not n: return 0
        lh = h(n.left)
        rh = h(n.right)
        best[0] = max(best[0], lh + rh)        # longest path through n
        return 1 + max(lh, rh)
    h(root)
    return best[0]
''',
            "complexity": "Time O(n), space O(h).",
        },
        "deep_concept": r'''
A path *through* a node uses at most one edge to each child subtree.
That's why `lh + rh` (not `1 + lh + rh`) — edges, not nodes. If asked
for nodes instead, return `lh + rh + 1`.
''',
        "confusion_notes": [
            {
                "question": "Diameter in edges vs in nodes — which is asked?",
                "answer": "LeetCode 543: *edges*. Some books: *nodes*. Read the problem. If nodes, the formula becomes `lh + rh + 1` (and height is in nodes too).",
            },
        ],
        "summary": "DFS returns height; on the way up update global best with `lh + rh` (edges) or `lh + rh + 1` (nodes).",
    },

    # ------------------------------------------------------------------
    # 10) Maximum Path Sum
    # ------------------------------------------------------------------
    {
        "id": "max-path-sum",
        "title": "Binary Tree Maximum Path Sum",
        "step_id": 13,
        "lecture_id": 2,
        "difficulty": "hard",
        "tags": ["tree", "dfs", "dp-on-tree"],
        "what_this_teaches": "Path sums on a tree — only one child contributes upward. Clamp negative contributions to zero.",
        "pattern": "DFS returning best one-sided gain.",
        "prerequisite_lessons": ["dp-intro"],
        "prerequisite_problems": ["tree-diameter"],
        "next_problems": ["zigzag-traversal"],
        "resources": [
            _lc(124, "binary-tree-maximum-path-sum"),
            _SHEET,
        ],
        "understanding": r'''
Find the maximum sum of any non-empty path in a tree. A path goes from
some node to some node (no repeated nodes) along parent-child links.
The path may pass through the root or not, and may go up-then-down at
some pivot.
''',
        "brute_force": {
            "explanation": "Try every pair of nodes (n²) and find the path between them — too slow.",
            "code": "",
            "complexity": "—",
        },
        "thought_process": r'''
**DP-on-tree.** At each node, compute the best path *ending at this
node* going downward. The best path *passing through* this node uses
both children. Track the global max.

Key: a child's contribution upward can be at most the *one-sided* max
(picking the better of its two children). If a child's best is
negative, we ignore it (clamp to 0).
''',
        "optimized": {
            "explanation": "Single-pass DFS with clamped child contributions.",
            "code": r'''
def max_path_sum(root):
    best = [float('-inf')]
    def gain(n):
        if not n: return 0
        left  = max(gain(n.left), 0)          # ignore negative contributions
        right = max(gain(n.right), 0)
        best[0] = max(best[0], n.val + left + right)  # path through n
        return n.val + max(left, right)               # path *ending* at n
    gain(root)
    return best[0]
''',
            "complexity": "Time O(n), space O(h).",
        },
        "deep_concept": r'''
The clamp-to-zero trick is what makes this DP work cleanly: if a
subtree's best path has negative sum, ignoring it strictly improves the
total. So we treat the child's contribution as max(child_gain, 0).
''',
        "confusion_notes": [
            {
                "question": "Why return `n.val + max(left, right)` instead of `n.val + left + right`?",
                "answer": "Because the returned value will be used by the *parent*, which can only attach the path via *one* of its children. Using both subtrees would create a path with a 'fork' — invalid for a parent's upward continuation.",
            },
            {
                "question": "Why is `best` initialized to `-inf`?",
                "answer": "Because all node values may be negative, in which case the best path has a negative sum. Starting at 0 would wrongly report 0 for a tree like `[-3]`.",
            },
        ],
        "summary": "DFS returning best one-sided downward gain, updating a global max with `node + left + right` (where left/right are clamped to ≥ 0).",
    },

    # ------------------------------------------------------------------
    # 11) Identical Trees
    # ------------------------------------------------------------------
    {
        "id": "trees-identical",
        "title": "Check if Two Trees are Identical",
        "step_id": 13,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["tree", "recursion"],
        "what_this_teaches": "Simple structural equality recursion.",
        "pattern": "Parallel DFS on two trees.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["preorder"],
        "next_problems": ["symmetric-tree"],
        "resources": [
            _lc(100, "same-tree"),
            _SHEET,
        ],
        "understanding": r'''
Two trees are identical iff they have the same structure *and* the same
values at every corresponding node.
''',
        "brute_force": {
            "explanation": "—",
            "code": "",
            "complexity": "—",
        },
        "thought_process": "Recurse both trees in lockstep; bail out the moment a discrepancy is found.",
        "optimized": {
            "explanation": "Parallel DFS.",
            "code": r'''
def is_same_tree(p, q):
    if not p and not q: return True
    if not p or not q: return False
    return p.val == q.val and is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)
''',
            "complexity": "Time O(min(n, m)), space O(min(h_p, h_q)).",
        },
        "deep_concept": "—",
        "confusion_notes": [
            {
                "question": "Does the order of conjunctions matter?",
                "answer": "Yes for performance — Python short-circuits, so `p.val == q.val` is the cheapest test and should come first. The two recursive calls follow.",
            },
        ],
        "summary": "Recurse both trees in lockstep; if either is None or values differ → False.",
    },

    # ------------------------------------------------------------------
    # 12) Zigzag Level Order Traversal
    # ------------------------------------------------------------------
    {
        "id": "zigzag-traversal",
        "title": "Zigzag (Spiral) Level Order Traversal",
        "step_id": 13,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["tree", "bfs"],
        "what_this_teaches": "BFS with alternating direction per level.",
        "pattern": "Level-order with a 'reverse this level' flag.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["level-order"],
        "next_problems": ["boundary-traversal"],
        "resources": [
            _lc(103, "binary-tree-zigzag-level-order-traversal"),
            _SHEET,
        ],
        "understanding": r'''
Same as level-order, but alternate the direction of each level:
left-to-right, then right-to-left, then left-to-right, and so on.
''',
        "brute_force": {
            "explanation": "—",
            "code": "",
            "complexity": "—",
        },
        "thought_process": "Do plain BFS; flip a `left_to_right` flag each level; reverse the level list when going right-to-left.",
        "optimized": {
            "explanation": "BFS with a reverse flag.",
            "code": r'''
from collections import deque

def zigzag_level_order(root):
    if not root: return []
    out = []
    q = deque([root])
    ltr = True
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        if not ltr:
            level.reverse()
        out.append(level)
        ltr = not ltr
    return out
''',
            "complexity": "Time O(n), space O(n).",
        },
        "deep_concept": "—",
        "confusion_notes": [
            {
                "question": "Why reverse the *list* instead of swapping push direction?",
                "answer": "Swapping push direction with a deque is also valid (use appendleft for some levels) but easy to bug. Building the list left-to-right then reversing when needed is straightforward.",
            },
        ],
        "summary": "BFS, reverse alternate levels.",
    },

    # ------------------------------------------------------------------
    # 13) Boundary Traversal
    # ------------------------------------------------------------------
    {
        "id": "boundary-traversal",
        "title": "Boundary Traversal of a Binary Tree",
        "step_id": 13,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["tree", "dfs"],
        "what_this_teaches": "Combining three sub-traversals: left boundary (down), leaves (left-to-right), right boundary (up).",
        "pattern": "Composite traversal.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["preorder"],
        "next_problems": ["vertical-order"],
        "resources": [
            {"label": "GFG — Boundary Traversal of Binary Tree", "url": "https://www.geeksforgeeks.org/boundary-traversal-of-binary-tree/"},
            _SHEET,
        ],
        "understanding": r'''
Boundary = root + left boundary (excluding leaves) + all leaves (LTR)
+ right boundary in reverse (excluding leaves).

The 'boundary' is the outline of the tree as if traced on paper.
''',
        "brute_force": {
            "explanation": "—",
            "code": "",
            "complexity": "—",
        },
        "thought_process": "Three helpers: walk left boundary down, collect leaves with full DFS, walk right boundary down (and reverse).",
        "optimized": {
            "explanation": "Composite three-phase traversal.",
            "code": r'''
def boundary_of_binary_tree(root):
    if not root: return []
    out = [root.val] if not (root.left is None and root.right is None) else []

    def add_left(n):
        while n:
            if not (n.left is None and n.right is None):
                out.append(n.val)
            n = n.left if n.left else n.right

    def add_leaves(n):
        if not n: return
        if n.left is None and n.right is None:
            out.append(n.val); return
        add_leaves(n.left); add_leaves(n.right)

    def add_right(n):
        tmp = []
        while n:
            if not (n.left is None and n.right is None):
                tmp.append(n.val)
            n = n.right if n.right else n.left
        out.extend(reversed(tmp))

    if root.left or root.right:
        add_left(root.left)
        add_leaves(root)
        add_right(root.right)
    elif not out:
        out.append(root.val)            # single-node tree
    return out
''',
            "complexity": "Time O(n), space O(n).",
        },
        "deep_concept": "Trees can decompose into many shapes — the boundary is one of them. Practice composing simple traversals.",
        "confusion_notes": [
            {
                "question": "Why skip leaves in the left/right boundary?",
                "answer": "Because the leaf phase will visit them. Including them in the left/right boundary would duplicate.",
            },
        ],
        "summary": "Root + left boundary (no leaves) + leaves (LTR) + right boundary in reverse (no leaves).",
    },

    # ------------------------------------------------------------------
    # 14) Vertical Order Traversal
    # ------------------------------------------------------------------
    {
        "id": "vertical-order",
        "title": "Vertical Order Traversal",
        "step_id": 13,
        "lecture_id": 2,
        "difficulty": "hard",
        "tags": ["tree", "bfs", "hash-map"],
        "what_this_teaches": "Assign (column, row) coordinates via BFS; group by column.",
        "pattern": "BFS with coordinate tracking.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["level-order"],
        "next_problems": ["top-view"],
        "resources": [
            _lc(987, "vertical-order-traversal-of-a-binary-tree"),
            _SHEET,
        ],
        "understanding": r'''
Assign each node coordinates: root is (col 0, row 0); left child of
(c, r) is (c - 1, r + 1); right child is (c + 1, r + 1). Group all
nodes by column, return columns from leftmost to rightmost. Within a
column, order by row, then by value (LeetCode's tiebreak).
''',
        "brute_force": {
            "explanation": "—",
            "code": "",
            "complexity": "—",
        },
        "thought_process": r'''
BFS visiting (node, col, row). Bucket nodes into a dict keyed by col.
Within each bucket, sort by (row, val). Return columns in sorted key
order.
''',
        "optimized": {
            "explanation": "BFS + bucket + sort.",
            "code": r'''
from collections import defaultdict, deque

def vertical_traversal(root):
    if not root: return []
    cols = defaultdict(list)            # col -> list of (row, val)
    q = deque([(root, 0, 0)])
    while q:
        node, c, r = q.popleft()
        cols[c].append((r, node.val))
        if node.left:  q.append((node.left,  c - 1, r + 1))
        if node.right: q.append((node.right, c + 1, r + 1))
    out = []
    for c in sorted(cols):
        cols[c].sort()                  # sort by (row, val)
        out.append([v for _, v in cols[c]])
    return out
''',
            "complexity": "Time O(n log n), space O(n).",
        },
        "deep_concept": "Coordinate-based bucketing is a useful tree pattern for any 'view from a direction' question.",
        "confusion_notes": [
            {
                "question": "Why sort by (row, val) instead of (row, insertion order)?",
                "answer": "LeetCode 987's spec: ties broken by value. Older versions used insertion order. Match the spec.",
            },
        ],
        "summary": "BFS with (col, row), bucket by col, sort each bucket by (row, val), return columns in sorted col order.",
    },

    # ------------------------------------------------------------------
    # 15) Top View
    # ------------------------------------------------------------------
    {
        "id": "top-view",
        "title": "Top View of a Binary Tree",
        "step_id": 13,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["tree", "bfs"],
        "what_this_teaches": "First-encountered node per column wins.",
        "pattern": "BFS keyed by column, keep only the first.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["vertical-order"],
        "next_problems": ["bottom-view"],
        "resources": [
            {"label": "GFG — Top View of a Binary Tree", "url": "https://www.geeksforgeeks.org/print-nodes-top-view-binary-tree/"},
            _SHEET,
        ],
        "understanding": r'''
Looking at the tree from above, you see the first node in each vertical
column. Return them from leftmost to rightmost column.
''',
        "brute_force": {
            "explanation": "—",
            "code": "",
            "complexity": "—",
        },
        "thought_process": "BFS guarantees we encounter each column's topmost node first. Save it; skip later visits to the same column.",
        "optimized": {
            "explanation": "BFS + first-write-wins map.",
            "code": r'''
from collections import deque

def top_view(root):
    if not root: return []
    seen = {}
    q = deque([(root, 0)])
    while q:
        node, c = q.popleft()
        if c not in seen:
            seen[c] = node.val
        if node.left:  q.append((node.left, c - 1))
        if node.right: q.append((node.right, c + 1))
    return [seen[c] for c in sorted(seen)]
''',
            "complexity": "Time O(n log n), space O(n).",
        },
        "deep_concept": "—",
        "confusion_notes": [
            {
                "question": "Why does BFS guarantee 'first encounter is topmost'?",
                "answer": "Because BFS processes nodes in row order. A node at row r is visited before any node at row r+1. So the *first* node BFS sees in a column is the topmost in that column.",
            },
        ],
        "summary": "BFS with column tracking; keep the first node per column; return sorted by column.",
    },

    # ------------------------------------------------------------------
    # 16) Bottom View
    # ------------------------------------------------------------------
    {
        "id": "bottom-view",
        "title": "Bottom View of a Binary Tree",
        "step_id": 13,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["tree", "bfs"],
        "what_this_teaches": "Last-encountered node per column wins.",
        "pattern": "BFS keyed by column, last-write-wins.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["top-view"],
        "next_problems": ["right-left-view"],
        "resources": [
            {"label": "GFG — Bottom View of a Binary Tree", "url": "https://www.geeksforgeeks.org/bottom-view-binary-tree/"},
            _SHEET,
        ],
        "understanding": r'''
Looking up from below, you see the deepest node in each vertical column.
''',
        "brute_force": {
            "explanation": "—",
            "code": "",
            "complexity": "—",
        },
        "thought_process": "Same BFS, but *overwrite* the column entry on every visit. The last write is the deepest.",
        "optimized": {
            "explanation": "BFS + last-write-wins map.",
            "code": r'''
from collections import deque

def bottom_view(root):
    if not root: return []
    seen = {}
    q = deque([(root, 0)])
    while q:
        node, c = q.popleft()
        seen[c] = node.val               # last write wins
        if node.left:  q.append((node.left, c - 1))
        if node.right: q.append((node.right, c + 1))
    return [seen[c] for c in sorted(seen)]
''',
            "complexity": "Time O(n log n), space O(n).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Like top view, but always overwrite the column entry — last visit wins.",
    },

    # ------------------------------------------------------------------
    # 17) Right / Left View
    # ------------------------------------------------------------------
    {
        "id": "right-left-view",
        "title": "Right View and Left View of a Binary Tree",
        "step_id": 13,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["tree", "bfs", "dfs"],
        "what_this_teaches": "First/last node per *level* wins.",
        "pattern": "DFS prioritizing right (or left).",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["bottom-view"],
        "next_problems": ["symmetric-tree"],
        "resources": [
            _lc(199, "binary-tree-right-side-view"),
            _SHEET,
        ],
        "understanding": r'''
Right view: from the right side, you see the *rightmost* node at each
level. Left view: symmetric.
''',
        "brute_force": {
            "explanation": "—",
            "code": "",
            "complexity": "—",
        },
        "thought_process": "DFS visiting right first; first node seen at each depth is the rightmost.",
        "optimized": {
            "explanation": "DFS, prefer right child, first-write-wins per depth.",
            "code": r'''
def right_view(root):
    out = []
    def dfs(n, d):
        if not n: return
        if d == len(out):
            out.append(n.val)             # first node at this depth
        dfs(n.right, d + 1)               # right first
        dfs(n.left,  d + 1)
    dfs(root, 0)
    return out

def left_view(root):
    out = []
    def dfs(n, d):
        if not n: return
        if d == len(out):
            out.append(n.val)
        dfs(n.left,  d + 1)
        dfs(n.right, d + 1)
    dfs(root, 0)
    return out
''',
            "complexity": "Time O(n), space O(h).",
        },
        "deep_concept": "DFS with priority gives 'first in some ordering' problems an elegant O(n) solution without BFS overhead.",
        "confusion_notes": [],
        "summary": "DFS prioritizing right (or left) child; record the first node at each depth.",
    },

    # ------------------------------------------------------------------
    # 18) Symmetric Tree
    # ------------------------------------------------------------------
    {
        "id": "symmetric-tree",
        "title": "Symmetric Tree",
        "step_id": 13,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["tree", "recursion"],
        "what_this_teaches": "Mirror-image recursion: compare left subtree of one against right subtree of the other.",
        "pattern": "Parallel mirror DFS.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["trees-identical"],
        "next_problems": ["root-to-node-path"],
        "resources": [
            _lc(101, "symmetric-tree"),
            _SHEET,
        ],
        "understanding": r'''
A tree is symmetric iff its left subtree is a mirror image of its right
subtree.
''',
        "brute_force": {
            "explanation": "—",
            "code": "",
            "complexity": "—",
        },
        "thought_process": "Recurse with two pointers: compare `left.left vs right.right` and `left.right vs right.left`.",
        "optimized": {
            "explanation": "Mirror DFS.",
            "code": r'''
def is_symmetric(root):
    def mirror(a, b):
        if not a and not b: return True
        if not a or not b: return False
        return a.val == b.val and mirror(a.left, b.right) and mirror(a.right, b.left)
    return mirror(root.left, root.right) if root else True
''',
            "complexity": "Time O(n), space O(h).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Mirror DFS pairing left.left with right.right and left.right with right.left.",
    },

    # ------------------------------------------------------------------
    # 19) Root to Node Path
    # ------------------------------------------------------------------
    {
        "id": "root-to-node-path",
        "title": "Root-to-Node Path",
        "step_id": 13,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["tree", "dfs", "backtracking"],
        "what_this_teaches": "Track the path as you descend; bail out early when the target is found.",
        "pattern": "DFS with path-as-list backtracking.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["symmetric-tree"],
        "next_problems": ["lca-binary-tree"],
        "resources": [
            {"label": "GFG — Print path", "url": "https://www.geeksforgeeks.org/print-path-root-given-node-binary-tree/"},
            _SHEET,
        ],
        "understanding": r'''
Given a binary tree and a target value, return the list of node values
from the root to the target (inclusive). Assume the target exists and
values are unique.
''',
        "brute_force": {
            "explanation": "—",
            "code": "",
            "complexity": "—",
        },
        "thought_process": "DFS pushing node values onto a list; on success return True so callers know to keep the list intact.",
        "optimized": {
            "explanation": "Backtracking DFS.",
            "code": r'''
def root_to_node_path(root, target):
    path = []
    def dfs(n):
        if not n: return False
        path.append(n.val)
        if n.val == target:
            return True
        if dfs(n.left) or dfs(n.right):
            return True
        path.pop()                         # backtrack
        return False
    dfs(root)
    return path
''',
            "complexity": "Time O(n), space O(h).",
        },
        "deep_concept": "Backtracking with mutable state (the `path` list) avoids O(n) list copies on each recursive call.",
        "confusion_notes": [
            {
                "question": "Why `path.pop()` only when we fail?",
                "answer": "Because a successful match unwinds with the path intact — every level returns True without touching `path`. Only failed branches need to clean up.",
            },
        ],
        "summary": "DFS pushing to a list; return True up the chain when found; pop on backtrack.",
    },

    # ------------------------------------------------------------------
    # 20) LCA in Binary Tree
    # ------------------------------------------------------------------
    {
        "id": "lca-binary-tree",
        "title": "Lowest Common Ancestor in a Binary Tree",
        "step_id": 13,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["tree", "dfs"],
        "what_this_teaches": "DFS that returns a witness: if both children return a witness, the current node is the LCA.",
        "pattern": "DFS bubbling up witnesses.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["root-to-node-path"],
        "next_problems": ["nodes-at-k-distance"],
        "resources": [
            _lc(236, "lowest-common-ancestor-of-a-binary-tree"),
            _SHEET,
        ],
        "understanding": r'''
LCA(p, q) is the deepest node that has both p and q in its subtree.

Example: in a tree where p = 5 and q = 1, the LCA is the root (or
whichever common ancestor is deepest).
''',
        "brute_force": {
            "explanation": "Find root-to-node paths for p and q; the LCA is the last common element. O(n) but uses extra memory.",
            "code": "",
            "complexity": "Time O(n), space O(h).",
        },
        "thought_process": r'''
**Single DFS.** Return the *witness* (one of p, q, or LCA-so-far) from
each call. If both children return a witness, the current node is the
LCA. If only one returns a witness, propagate it up.
''',
        "optimized": {
            "explanation": "Classic LCA DFS.",
            "code": r'''
def lowest_common_ancestor(root, p, q):
    if not root or root is p or root is q:
        return root
    left  = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:                     # p in one subtree, q in the other
        return root
    return left if left else right
''',
            "complexity": "Time O(n), space O(h).",
        },
        "deep_concept": "Single-pass DFS with 'bubble up the witness' is a powerful pattern. It generalizes to LCA of K nodes, common ancestor with constraints, etc.",
        "confusion_notes": [
            {
                "question": "What if p == q?",
                "answer": "The function returns p (which is also q) — that's the LCA of a node with itself. Edge case handled by the `root is p or root is q` short-circuit.",
            },
        ],
        "summary": "DFS returning the witness; the node where left and right both produce a witness is the LCA.",
    },

    # ------------------------------------------------------------------
    # 21) Maximum Width of Binary Tree
    # ------------------------------------------------------------------
    {
        "id": "max-width",
        "title": "Maximum Width of Binary Tree",
        "step_id": 13,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["tree", "bfs"],
        "what_this_teaches": "Assigning heap-style indices to count *positions* — including null slots — across each level.",
        "pattern": "BFS with positional indexing.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["level-order"],
        "next_problems": ["count-complete-tree-nodes"],
        "resources": [
            _lc(662, "maximum-width-of-binary-tree"),
            _SHEET,
        ],
        "understanding": r'''
Width of a level = number of positions between the leftmost and
rightmost *non-null* nodes, *including* nulls between them.

**Example:** if level has positions 0, _, _, 3 (with nulls at 1, 2),
width = 4.
''',
        "brute_force": {
            "explanation": "—",
            "code": "",
            "complexity": "—",
        },
        "thought_process": r'''
BFS, but each node carries a heap-style index: root = 0; left child of
i is `2i + 1`, right is `2i + 2`. The width of a level is
`rightmost_idx − leftmost_idx + 1`. Track the max across levels.

To avoid integer overflow on deep trees, *re-anchor* the level by
subtracting the leftmost index of the level from every push.
''',
        "optimized": {
            "explanation": "BFS with positional indexing.",
            "code": r'''
from collections import deque

def width_of_binary_tree(root):
    if not root: return 0
    q = deque([(root, 0)])
    best = 0
    while q:
        size = len(q)
        _, first_idx = q[0]
        for _ in range(size):
            node, idx = q.popleft()
            idx -= first_idx                       # re-anchor to keep ints small
            if not q:
                best = max(best, idx + 1)
            if node.left:  q.append((node.left,  2 * idx + 1))
            if node.right: q.append((node.right, 2 * idx + 2))
        # the loop popped the entire level. best was updated when last element popped
        # but we want overall max — better: track every popped position
    # Simpler accurate version:
    q = deque([(root, 0)])
    best = 0
    while q:
        size = len(q)
        _, first_idx = q[0]
        last_idx = first_idx
        for _ in range(size):
            node, idx = q.popleft()
            last_idx = idx
            idx -= first_idx
            if node.left:  q.append((node.left,  2 * idx + 1))
            if node.right: q.append((node.right, 2 * idx + 2))
        best = max(best, last_idx - first_idx + 1)
    return best
''',
            "complexity": "Time O(n), space O(width).",
        },
        "deep_concept": "Heap-style indexing reveals positions even when nulls are not in the queue. Re-anchoring keeps indices small.",
        "confusion_notes": [
            {
                "question": "Why re-anchor (`idx - first_idx`)?",
                "answer": "Without it, a deep skewed tree balloons indices exponentially (2^h). Python handles big ints, but other languages overflow. Re-anchoring at each level keeps indices bounded by ≤ 2 · width.",
            },
        ],
        "summary": "BFS with heap-style positional indices; width = last_idx - first_idx + 1 at each level. Re-anchor to avoid overflow.",
    },

    # ------------------------------------------------------------------
    # 22) Children Sum Property
    # ------------------------------------------------------------------
    {
        "id": "children-sum",
        "title": "Children Sum Property",
        "step_id": 13,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["tree", "recursion"],
        "what_this_teaches": "Mutate the tree so every node's value equals the sum of its children. Two passes (top-down then bottom-up).",
        "pattern": "Recursive 'patch' via top-down boost + bottom-up sum.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["tree-height"],
        "next_problems": ["nodes-at-k-distance"],
        "resources": [
            {"label": "GFG — Children Sum Property", "url": "https://www.geeksforgeeks.org/check-children-sum-property-given-binary-tree/"},
            _SHEET,
        ],
        "understanding": r'''
Modify the tree (increasing values only) so that every node satisfies:
`node.val == left.val + right.val` (a missing child counts as 0).
You may increase values; you may not decrease them.
''',
        "brute_force": {
            "explanation": "—",
            "code": "",
            "complexity": "—",
        },
        "thought_process": r'''
**Top-down boost:** If `node.val > left.val + right.val`, push extra to
the children (give it to either). Recurse into the children. On the way
back up, *set* `node.val = left.val + right.val` (which now satisfies
the property given the top-down boost).
''',
        "optimized": {
            "explanation": "Two-phase recursion (top-down push, bottom-up sum).",
            "code": r'''
def fix_children_sum(root):
    if not root or (root.left is None and root.right is None):
        return
    left_val  = root.left.val  if root.left  else 0
    right_val = root.right.val if root.right else 0
    if left_val + right_val < root.val:
        if root.left:  root.left.val  = root.val      # push down arbitrarily
        elif root.right: root.right.val = root.val
    # otherwise children already exceed parent — that's fine for now
    fix_children_sum(root.left)
    fix_children_sum(root.right)
    # post-order: set node.val = sum of children
    s = (root.left.val  if root.left  else 0) + (root.right.val if root.right else 0)
    if s != 0:
        root.val = s
''',
            "complexity": "Time O(n), space O(h).",
        },
        "deep_concept": "Two-phase recursion (top-down → bottom-up) is essential when *both* directions of information flow matter.",
        "confusion_notes": [
            {
                "question": "Why do we push the parent's full value to a single child instead of dividing?",
                "answer": "Because we can only *increase*, never decrease. Giving the entire parent value to one child is always safe; if we tried to divide we might leave one child below the parent's needed total. Bottom-up phase then sums children back.",
            },
        ],
        "summary": "Top-down: ensure children sum ≥ parent (boost a child if not). Bottom-up: set parent = sum of children.",
    },

    # ------------------------------------------------------------------
    # 23) Nodes at K Distance from Target
    # ------------------------------------------------------------------
    {
        "id": "nodes-at-k-distance",
        "title": "Nodes at Distance K from a Target",
        "step_id": 13,
        "lecture_id": 3,
        "difficulty": "hard",
        "tags": ["tree", "bfs", "graph"],
        "what_this_teaches": "Convert the tree into an undirected graph (by adding parent pointers), then BFS from the target.",
        "pattern": "Tree → graph conversion + BFS.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["lca-binary-tree"],
        "next_problems": ["burning-tree"],
        "resources": [
            _lc(863, "all-nodes-distance-k-in-binary-tree"),
            _SHEET,
        ],
        "understanding": r'''
Given a binary tree, a target node, and integer k, return all nodes at
distance exactly k from the target.
''',
        "brute_force": {
            "explanation": "Recurse downward from target (easy) and then walk up to its ancestors, recursing downward from each ancestor minus the side that contains target. Doable but error-prone.",
            "code": "",
            "complexity": "Time O(n).",
        },
        "thought_process": r'''
Easier: build a parent-pointer map (`child → parent`) via one DFS, then
BFS from the target treating the tree as an undirected graph.
''',
        "optimized": {
            "explanation": "DFS to record parents, BFS from target with a visited set.",
            "code": r'''
from collections import deque

def distance_k(root, target, k):
    parent = {}
    def dfs(n, p):
        if not n: return
        parent[n] = p
        dfs(n.left,  n)
        dfs(n.right, n)
    dfs(root, None)

    q = deque([(target, 0)])
    visited = {target}
    out = []
    while q:
        node, d = q.popleft()
        if d == k:
            out.append(node.val)
            continue
        for nei in (node.left, node.right, parent[node]):
            if nei and nei not in visited:
                visited.add(nei)
                q.append((nei, d + 1))
    return out
''',
            "complexity": "Time O(n), space O(n).",
        },
        "deep_concept": "Treating a tree as an undirected graph unlocks BFS/shortest-path techniques that don't fit the parent-down DFS model.",
        "confusion_notes": [
            {
                "question": "Why do we need a visited set on a tree?",
                "answer": "Because once we add parent pointers, the graph is undirected — without `visited` we'd bounce back to the node we just came from. The tree no longer has the 'no backtracking' property of pure DFS.",
            },
        ],
        "summary": "Build parent map; BFS from target with visited set; record nodes at exactly distance k.",
    },

    # ------------------------------------------------------------------
    # 24) Burning Tree
    # ------------------------------------------------------------------
    {
        "id": "burning-tree",
        "title": "Minimum Time to Burn the Whole Tree",
        "step_id": 13,
        "lecture_id": 3,
        "difficulty": "hard",
        "tags": ["tree", "bfs", "graph"],
        "what_this_teaches": "BFS multi-source on a tree; track the *maximum* time taken to reach any node.",
        "pattern": "Same as 'nodes at distance k', but compute the farthest distance.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["nodes-at-k-distance"],
        "next_problems": ["count-complete-tree-nodes"],
        "resources": [
            _lc(2385, "amount-of-time-for-binary-tree-to-be-infected"),
            _SHEET,
        ],
        "understanding": r'''
Given a binary tree and a 'burning' starting node, fire spreads from a
node to its neighbors (parent and children) in one unit of time. Return
the minimum time for the entire tree to burn.

This is equivalently the *eccentricity* of the start node in the
undirected version of the tree.
''',
        "brute_force": {
            "explanation": "—",
            "code": "",
            "complexity": "—",
        },
        "thought_process": "Identical to nodes-at-k: build parent map, BFS, return the maximum distance seen.",
        "optimized": {
            "explanation": "BFS, track last-popped distance.",
            "code": r'''
from collections import deque

def amount_of_time(root, start):
    parent = {}
    start_node = None
    def dfs(n, p):
        nonlocal start_node
        if not n: return
        parent[n] = p
        if n.val == start:
            start_node = n
        dfs(n.left,  n)
        dfs(n.right, n)
    dfs(root, None)

    q = deque([(start_node, 0)])
    visited = {start_node}
    last = 0
    while q:
        node, d = q.popleft()
        last = d
        for nei in (node.left, node.right, parent[node]):
            if nei and nei not in visited:
                visited.add(nei)
                q.append((nei, d + 1))
    return last
''',
            "complexity": "Time O(n), space O(n).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Tree → undirected graph; BFS from start; answer = max distance reached.",
    },

    # ------------------------------------------------------------------
    # 25) Count Complete Tree Nodes
    # ------------------------------------------------------------------
    {
        "id": "count-complete-tree-nodes",
        "title": "Count Nodes in a Complete Binary Tree",
        "step_id": 13,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["tree", "binary-search"],
        "what_this_teaches": "Use the complete-tree invariant (leaves only on the last level, left-aligned) to count in O(log² n).",
        "pattern": "Compare leftmost and rightmost heights.",
        "prerequisite_lessons": [],
        "prerequisite_problems": [],
        "next_problems": ["unique-tree-requirements"],
        "resources": [
            _lc(222, "count-complete-tree-nodes"),
            _SHEET,
        ],
        "understanding": r'''
A *complete* binary tree fills levels left-to-right. We want to count
all nodes — but in O(log² n), not O(n).
''',
        "brute_force": {
            "explanation": "Plain DFS counts in O(n).",
            "code": r'''
def count_brute(root):
    return 0 if not root else 1 + count_brute(root.left) + count_brute(root.right)
''',
            "complexity": "Time O(n).",
        },
        "thought_process": r'''
At each node, compute the leftmost depth (always go left) and rightmost
depth (always go right). If they're equal, the subtree is a *perfect*
binary tree of size 2^h − 1. Otherwise, recurse into both children.

Each level of recursion does O(log n) work for the height comparison.
Total recursion depth is log n. So O(log² n).
''',
        "optimized": {
            "explanation": "Recursive with height shortcut.",
            "code": r'''
def count_nodes(root):
    if not root: return 0
    lh = 0; n = root
    while n: lh += 1; n = n.left
    rh = 0; n = root
    while n: rh += 1; n = n.right
    if lh == rh:
        return (1 << lh) - 1                      # perfect tree: 2^h - 1 nodes
    return 1 + count_nodes(root.left) + count_nodes(root.right)
''',
            "complexity": "Time O(log² n), space O(log n).",
        },
        "deep_concept": "Exploiting *shape constraints* of a tree can dramatically reduce work. Complete trees have a logarithmic height and a closed-form size for perfect subtrees.",
        "confusion_notes": [
            {
                "question": "Why O(log² n) and not O(log n)?",
                "answer": "Because at each of log n recursive levels we spend O(log n) computing the leftmost/rightmost heights. log n levels × log n work = log² n.",
            },
        ],
        "summary": "Leftmost vs rightmost height → if equal, use 2^h − 1; else recurse. O(log² n).",
    },

    # ------------------------------------------------------------------
    # 26) Unique Tree Requirements (which 2 traversals uniquely identify a tree)
    # ------------------------------------------------------------------
    {
        "id": "unique-tree-requirements",
        "title": "Which Two Traversals Uniquely Identify a Tree?",
        "step_id": 13,
        "lecture_id": 3,
        "difficulty": "easy",
        "tags": ["tree", "concept"],
        "what_this_teaches": "Theory — inorder + (pre or post) uniquely determines a tree; pre + post does not (without extra info).",
        "pattern": "Theory.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["all-traversals-one-pass"],
        "next_problems": ["construct-pre-in", "construct-post-in"],
        "resources": [
            {"label": "GFG — Inorder + Preorder constructs unique BT", "url": "https://www.geeksforgeeks.org/if-you-are-given-two-traversal-sequences-can-you-construct-the-binary-tree/"},
            _SHEET,
        ],
        "understanding": r'''
**Fact:** Inorder + (preorder OR postorder) uniquely identifies a binary
tree. Preorder + postorder alone does *not* (it can fail to disambiguate
when a node has only one child).

**Why?** Inorder gives us the *root's position within the sequence* —
once we know root (from pre or post), inorder tells us left vs right
subtrees. Pre+post lacks this disambiguation.
''',
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Internalize this for the next two problems.",
        "optimized": {"explanation": "—", "code": "", "complexity": "—"},
        "deep_concept": "When in doubt, sketch a counter-example: pre = [1, 2], post = [2, 1] — could be 2 as left child or right child of 1.",
        "confusion_notes": [],
        "summary": "Inorder + (preorder | postorder) → unique tree. Pre+post alone is ambiguous.",
    },

    # ------------------------------------------------------------------
    # 27) Construct Tree from Pre + In
    # ------------------------------------------------------------------
    {
        "id": "construct-pre-in",
        "title": "Construct Binary Tree from Preorder and Inorder",
        "step_id": 13,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["tree", "recursion", "construction"],
        "what_this_teaches": "Recursive divide-and-conquer using index maps.",
        "pattern": "Recursive construction with hash-map lookups.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["unique-tree-requirements"],
        "next_problems": ["construct-post-in"],
        "resources": [
            _lc(105, "construct-binary-tree-from-preorder-and-inorder-traversal"),
            _SHEET,
        ],
        "understanding": r'''
Given the preorder and inorder traversals of a binary tree (values
unique), reconstruct the tree.

**Idea:** First value of preorder is the root. Find it in inorder; all
values to its left form the left subtree, all to the right form the
right subtree. Recurse.
''',
        "brute_force": {
            "explanation": "Linear search in inorder for the root at each call → O(n²).",
            "code": "",
            "complexity": "Time O(n²).",
        },
        "thought_process": "Precompute a `value → index in inorder` map for O(1) lookups.",
        "optimized": {
            "explanation": "Recursive with index map.",
            "code": r'''
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right

def build_tree(preorder, inorder):
    idx = {v: i for i, v in enumerate(inorder)}
    pre_iter = iter(preorder)
    def build(lo, hi):
        if lo > hi: return None
        val = next(pre_iter)
        root = TreeNode(val)
        mid = idx[val]
        root.left  = build(lo,  mid - 1)
        root.right = build(mid + 1, hi)
        return root
    return build(0, len(inorder) - 1)
''',
            "complexity": "Time O(n), space O(n).",
        },
        "deep_concept": "Building a tree from traversals is a microcosm of divide-and-conquer: identify the root, partition, recurse.",
        "confusion_notes": [
            {
                "question": "Why iterate preorder with a *single* iterator instead of indices?",
                "answer": "Because preorder consumes its values *in order* during recursion (root, left subtree, right subtree, all in order). Using `next(pre_iter)` gives us this naturally without needing to track an index manually.",
            },
        ],
        "summary": "Iterate preorder; for each value, look up its inorder index, recurse on the left/right subranges of inorder.",
    },

    # ------------------------------------------------------------------
    # 28) Construct Tree from Post + In
    # ------------------------------------------------------------------
    {
        "id": "construct-post-in",
        "title": "Construct Binary Tree from Postorder and Inorder",
        "step_id": 13,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["tree", "recursion", "construction"],
        "what_this_teaches": "Mirror of pre+in: postorder is consumed *back-to-front*.",
        "pattern": "Recursive construction with hash-map lookups.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["construct-pre-in"],
        "next_problems": ["serialize-deserialize"],
        "resources": [
            _lc(106, "construct-binary-tree-from-inorder-and-postorder-traversal"),
            _SHEET,
        ],
        "understanding": r'''
Given inorder and postorder traversals, rebuild the tree. The *last*
value of postorder is the root; left subtree comes before it in
inorder, right subtree after.
''',
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Same as pre+in but consume postorder from the back. Recurse *right* subtree before *left* to match postorder's (L, R, root) reverse pattern.",
        "optimized": {
            "explanation": "Recursive consuming postorder from the back.",
            "code": r'''
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right

def build_tree_post(inorder, postorder):
    idx = {v: i for i, v in enumerate(inorder)}
    post = postorder[:]
    def build(lo, hi):
        if lo > hi: return None
        val = post.pop()                            # last of postorder is root
        root = TreeNode(val)
        mid = idx[val]
        root.right = build(mid + 1, hi)             # right first!
        root.left  = build(lo, mid - 1)
        return root
    return build(0, len(inorder) - 1)
''',
            "complexity": "Time O(n), space O(n).",
        },
        "deep_concept": "Postorder is preorder mirrored — consume from the back and process right subtree before left.",
        "confusion_notes": [
            {
                "question": "Why right before left here?",
                "answer": "Because postorder ends with (..., right subtree's postorder, root). Popping from the back gives root first, then right subtree's nodes — so we recurse right first to consume them correctly.",
            },
        ],
        "summary": "Postorder pops from the back; recurse right before left to mirror the (L, R, root) pattern.",
    },

    # ------------------------------------------------------------------
    # 29) Serialize/Deserialize Binary Tree
    # ------------------------------------------------------------------
    {
        "id": "serialize-deserialize",
        "title": "Serialize and Deserialize Binary Tree",
        "step_id": 13,
        "lecture_id": 3,
        "difficulty": "hard",
        "tags": ["tree", "design", "bfs"],
        "what_this_teaches": "Encoding null markers makes serialization unambiguous with a single traversal.",
        "pattern": "BFS / preorder serialization with null markers.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["construct-pre-in"],
        "next_problems": ["morris-inorder"],
        "resources": [
            _lc(297, "serialize-and-deserialize-binary-tree"),
            _SHEET,
        ],
        "understanding": r'''
Convert a binary tree to a string, then reconstruct the original tree
from that string.
''',
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Use preorder with `#` (or `null`) markers for missing children. Deserialize by consuming tokens.",
        "optimized": {
            "explanation": "Preorder serialization with null markers.",
            "code": r'''
class Codec:
    def serialize(self, root):
        out = []
        def go(n):
            if not n:
                out.append('#'); return
            out.append(str(n.val))
            go(n.left); go(n.right)
        go(root)
        return ','.join(out)

    def deserialize(self, s):
        from collections import deque
        tokens = deque(s.split(','))
        def go():
            t = tokens.popleft()
            if t == '#':
                return None
            n = TreeNode(int(t))
            n.left  = go()
            n.right = go()
            return n
        return go()
''',
            "complexity": "Time O(n), space O(n).",
        },
        "deep_concept": "Null markers convert an ambiguous serialization into a unique one — essentially encoding tree shape into the value stream.",
        "confusion_notes": [
            {
                "question": "Can we serialize with BFS instead?",
                "answer": "Yes — same idea, write level-by-level with '#' for missing children. Both styles work; preorder is more concise to deserialize.",
            },
        ],
        "summary": "Preorder serialization with '#' for null. Deserialize recursively consuming the token stream.",
    },

    # ------------------------------------------------------------------
    # 30) Morris Inorder
    # ------------------------------------------------------------------
    {
        "id": "morris-inorder",
        "title": "Morris Inorder Traversal (O(1) space)",
        "step_id": 13,
        "lecture_id": 3,
        "difficulty": "hard",
        "tags": ["tree", "morris", "traversal"],
        "what_this_teaches": "Inorder traversal using temporary 'threads' from predecessors back to current nodes — no stack, no recursion.",
        "pattern": "Threaded binary tree.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["inorder"],
        "next_problems": ["morris-preorder"],
        "resources": [
            {"label": "Wikipedia — Threaded binary tree", "url": "https://en.wikipedia.org/wiki/Threaded_binary_tree"},
            _SHEET,
        ],
        "understanding": r'''
Standard inorder uses O(h) stack space. Morris traversal achieves
**O(1) extra space** by temporarily rewiring the tree:
- For each node `cur` with a left subtree, find the rightmost node in
  the left subtree (the *inorder predecessor*).
- If predecessor's right is null, set it to `cur` (create a 'thread'),
  and move `cur` left.
- If predecessor's right is already `cur`, restore it to null (undo the
  thread), emit `cur.val`, and move `cur` right.

The rewiring lets us 'return' to `cur` after finishing its left subtree
without using a stack.
''',
        "brute_force": {"explanation": "Recursive inorder — O(h) stack.", "code": "", "complexity": "—"},
        "thought_process": "Threads are bookkeeping that allows iterative inorder in O(1) memory. The tree returns to its original shape at the end.",
        "optimized": {
            "explanation": "Morris inorder.",
            "code": r'''
def morris_inorder(root):
    out = []
    cur = root
    while cur:
        if not cur.left:
            out.append(cur.val)
            cur = cur.right
        else:
            # find predecessor
            pre = cur.left
            while pre.right and pre.right is not cur:
                pre = pre.right
            if pre.right is None:
                pre.right = cur          # create thread
                cur = cur.left
            else:
                pre.right = None         # undo thread
                out.append(cur.val)
                cur = cur.right
    return out
''',
            "complexity": "Time O(n) (amortized — each edge is traversed at most twice). Space O(1) extra.",
        },
        "deep_concept": "Morris demonstrates that we can sometimes 'borrow' unused pointers (null right-children) to do bookkeeping in-place. The space saving comes from this clever reuse.",
        "confusion_notes": [
            {
                "question": "Doesn't temporarily modifying the tree cause issues in concurrent code?",
                "answer": "Yes — Morris is not thread-safe. The tree is *broken* during traversal and only restored when traversal completes. Don't use Morris in environments where the tree may be read concurrently.",
            },
        ],
        "summary": "Use the inorder predecessor's right child as a temporary 'thread' back to the current node. O(1) extra space.",
    },

    # ------------------------------------------------------------------
    # 31) Morris Preorder
    # ------------------------------------------------------------------
    {
        "id": "morris-preorder",
        "title": "Morris Preorder Traversal",
        "step_id": 13,
        "lecture_id": 3,
        "difficulty": "hard",
        "tags": ["tree", "morris", "traversal"],
        "what_this_teaches": "Same Morris trick, but emit on the *first* visit instead of the second.",
        "pattern": "Threaded binary tree.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["morris-inorder"],
        "next_problems": ["flatten-tree"],
        "resources": [
            {"label": "GFG — Morris Preorder", "url": "https://www.geeksforgeeks.org/morris-traversal-for-preorder/"},
            _SHEET,
        ],
        "understanding": r'''
Morris preorder = Morris inorder with the emission moved to the *first*
visit (when we create the thread) rather than the second (when we
remove it).
''',
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Same as Morris inorder, except `out.append(cur.val)` happens when we set the thread.",
        "optimized": {
            "explanation": "Morris preorder.",
            "code": r'''
def morris_preorder(root):
    out = []
    cur = root
    while cur:
        if not cur.left:
            out.append(cur.val)
            cur = cur.right
        else:
            pre = cur.left
            while pre.right and pre.right is not cur:
                pre = pre.right
            if pre.right is None:
                out.append(cur.val)      # emit at first visit
                pre.right = cur
                cur = cur.left
            else:
                pre.right = None
                cur = cur.right
    return out
''',
            "complexity": "Time O(n), space O(1) extra.",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Same Morris trick; emit when creating the thread (first visit) instead of removing it.",
    },

    # ------------------------------------------------------------------
    # 32) Flatten Binary Tree to Linked List
    # ------------------------------------------------------------------
    {
        "id": "flatten-tree",
        "title": "Flatten Binary Tree to Linked List",
        "step_id": 13,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["tree", "morris", "in-place"],
        "what_this_teaches": "In-place tree restructuring via reverse-preorder DFS or Morris-style threading.",
        "pattern": "In-place transformation.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["morris-preorder"],
        "next_problems": [],
        "resources": [
            _lc(114, "flatten-binary-tree-to-linked-list"),
            _SHEET,
        ],
        "understanding": r'''
In-place, rewire the tree so that:
- All right-children point to the next node in preorder.
- All left-children are null.

The result is a right-skewed linked-list-shaped tree.
''',
        "brute_force": {
            "explanation": "Get the preorder traversal, then rebuild the tree using each node's right pointer.",
            "code": "",
            "complexity": "Time O(n), space O(n).",
        },
        "thought_process": r'''
**O(1) space solution.** Walk the tree iteratively. For each node:
- If it has a left subtree, find the rightmost node in that left
  subtree.
- Attach the current right subtree to that rightmost node.
- Move the left subtree to the right.
- Null the left.
- Move to the next right.
''',
        "optimized": {
            "explanation": "Morris-style in-place flatten.",
            "code": r'''
def flatten(root):
    cur = root
    while cur:
        if cur.left:
            pre = cur.left
            while pre.right:
                pre = pre.right
            pre.right = cur.right
            cur.right = cur.left
            cur.left  = None
        cur = cur.right
''',
            "complexity": "Time O(n), space O(1).",
        },
        "deep_concept": "This is essentially Morris preorder *as a permanent transformation* — instead of restoring threads, we keep them and discard the lefts.",
        "confusion_notes": [
            {
                "question": "Why does each node get visited O(1) times amortized?",
                "answer": "Because the inner `while pre.right` walk reuses paths only across the tree as a whole. Each edge is traversed a constant number of times across the algorithm, giving O(n).",
            },
        ],
        "summary": "For each node with a left subtree, attach the right subtree under the leftmost-rightmost descendant, then move left to right.",
    },
]
