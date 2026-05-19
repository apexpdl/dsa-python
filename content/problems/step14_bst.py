"""Step 14 — Binary Search Trees (15 problems).

Covers BST fundamentals (search, insert, delete, min/max, ceil/floor),
inorder-based properties (kth smallest/largest, validate, two-sum,
recover, iterator), construction from preorder, LCA on BST, and the
'largest BST in a tree' problem.
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
    # 1) BST Introduction
    # ------------------------------------------------------------------
    {
        "id": "bst-introduction",
        "title": "Introduction to Binary Search Trees",
        "step_id": 14,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["bst", "concept"],
        "what_this_teaches": "The BST invariant and why it enables O(log n) operations on average.",
        "pattern": "Conceptual overview.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["tree-introduction"],
        "next_problems": ["bst-search", "bst-min-max"],
        "resources": [
            {"label": "Wikipedia — Binary search tree", "url": "https://en.wikipedia.org/wiki/Binary_search_tree"},
            _SHEET,
        ],
        "understanding": r'''
A **Binary Search Tree** is a binary tree with an ordering invariant:
for every node, **all values in the left subtree are smaller, all
values in the right subtree are larger**. (Some definitions allow
equality on one side; we'll use *strict* inequality.)

**What does the invariant buy us?** At every node we can decide which
subtree to descend into using a single comparison. The search is
analogous to binary search on a sorted array — we halve the candidate
set at each step. If the tree is **balanced**, height ≈ log₂ n, so
search/insert/delete cost O(log n).

**What if the tree is *not* balanced?** Worst case (insert 1, 2, 3, …,
n in order), the tree degenerates into a right-skewed chain of height
n — operations cost O(n). That's why self-balancing variants exist:
AVL, Red-Black, Treap, Splay, B-tree. They guarantee O(log n) by
performing rotations on imbalance.

**Inorder traversal of a BST gives sorted output.** This is the most
important consequence of the invariant — many problems on BSTs reduce
to manipulating a sorted sequence.
''',
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Internalize: inorder = sorted. Almost every BST trick uses this.",
        "optimized": {
            "explanation": "Minimal BST node class.",
            "code": r'''
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right
''',
            "complexity": "—",
        },
        "deep_concept": r'''
The BST is the prototype of *comparison-based* search structures. The
same idea (cut work in half by comparison) underlies binary search,
heaps, merge sort, and so on. A balanced BST is asymptotically optimal
for ordered-set operations under the comparison model.
''',
        "confusion_notes": [
            {
                "question": "Plain BST vs balanced BST — which does Python use?",
                "answer": "Python's standard library has no balanced BST. Use `sortedcontainers.SortedList` from PyPI (skip list under the hood). For dictionaries, Python uses hash tables, not trees.",
            },
            {
                "question": "If inorder is sorted, why not just use a sorted array?",
                "answer": "Because arrays are slow to insert into (O(n)). BSTs trade away O(1) random access for O(log n) insert and delete, and they preserve the ordering invariant in-place.",
            },
        ],
        "summary": "BST = binary tree with left < node < right. Inorder = sorted. O(log n) ops on balanced trees, O(n) worst case on degenerate ones.",
    },

    # ------------------------------------------------------------------
    # 2) BST Search
    # ------------------------------------------------------------------
    {
        "id": "bst-search",
        "title": "Search in a Binary Search Tree",
        "step_id": 14,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["bst", "search"],
        "what_this_teaches": "The basic 'descend left or right by comparing to current' loop. Iterative is preferred — O(h) time, O(1) space.",
        "pattern": "BST descent.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["bst-introduction"],
        "next_problems": ["bst-min-max", "bst-ceil"],
        "resources": [
            _lc(700, "search-in-a-binary-search-tree"),
            _SHEET,
        ],
        "understanding": r'''
Given a BST and a target value, return the node with that value (or
null).
''',
        "brute_force": {
            "explanation": "DFS the whole tree ignoring the BST property — O(n).",
            "code": "",
            "complexity": "Time O(n).",
        },
        "thought_process": "Compare target to current node; descend left if smaller, right if larger, return when equal.",
        "optimized": {
            "explanation": "Iterative descent.",
            "code": r'''
def search_bst(root, target):
    while root:
        if root.val == target:
            return root
        root = root.left if target < root.val else root.right
    return None
''',
            "complexity": "Time O(h), space O(1).",
        },
        "deep_concept": "Iterative descent is structurally the same algorithm as binary search on an array, applied to the implicit ordering of a BST.",
        "confusion_notes": [
            {
                "question": "Why prefer iterative over recursive here?",
                "answer": "Each iteration is a single comparison and a single pointer move — no need for recursion's stack overhead. Same logic, less memory.",
            },
        ],
        "summary": "Walk down: if equal return, else left or right based on comparison. O(h).",
    },

    # ------------------------------------------------------------------
    # 3) Min / Max in BST
    # ------------------------------------------------------------------
    {
        "id": "bst-min-max",
        "title": "Find Min and Max in a BST",
        "step_id": 14,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["bst"],
        "what_this_teaches": "Leftmost = min, rightmost = max.",
        "pattern": "Single-direction descent.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["bst-search"],
        "next_problems": ["bst-ceil", "bst-floor"],
        "resources": [
            {"label": "GFG — Min/Max in BST", "url": "https://www.geeksforgeeks.org/find-the-minimum-element-in-a-binary-search-tree/"},
            _SHEET,
        ],
        "understanding": "The minimum is the leftmost node (keep going left). The maximum is the rightmost.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "—",
        "optimized": {
            "explanation": "Walk left/right.",
            "code": r'''
def bst_min(root):
    if not root: return None
    while root.left:
        root = root.left
    return root.val

def bst_max(root):
    if not root: return None
    while root.right:
        root = root.right
    return root.val
''',
            "complexity": "Time O(h), space O(1).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Min = leftmost, Max = rightmost. O(h).",
    },

    # ------------------------------------------------------------------
    # 4) BST Ceil
    # ------------------------------------------------------------------
    {
        "id": "bst-ceil",
        "title": "Ceil in a BST",
        "step_id": 14,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["bst"],
        "what_this_teaches": "Track the best candidate during descent.",
        "pattern": "Single descent with candidate update.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["bst-search"],
        "next_problems": ["bst-floor"],
        "resources": [
            {"label": "Striver — Ceil in a BST", "url": "https://takeuforward.org/data-structure/ceil-in-a-binary-search-tree/"},
            _SHEET,
        ],
        "understanding": r'''
Given a BST and a target x, find the smallest value in the BST that is
≥ x. Return -1 if no such value exists.
''',
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Descend; whenever the current node value ≥ x, it's a candidate — record it and try to find a smaller one in the left subtree. Otherwise go right.",
        "optimized": {
            "explanation": "Single descent.",
            "code": r'''
def bst_ceil(root, x):
    ceil = -1
    while root:
        if root.val == x:
            return root.val
        if root.val > x:
            ceil = root.val
            root = root.left              # try to find smaller candidate
        else:
            root = root.right
    return ceil
''',
            "complexity": "Time O(h), space O(1).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Track ceil candidate; descend left when current ≥ x, right when current < x.",
    },

    # ------------------------------------------------------------------
    # 5) BST Floor
    # ------------------------------------------------------------------
    {
        "id": "bst-floor",
        "title": "Floor in a BST",
        "step_id": 14,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["bst"],
        "what_this_teaches": "Symmetric to ceil.",
        "pattern": "Single descent with candidate update.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["bst-ceil"],
        "next_problems": ["bst-insert"],
        "resources": [
            {"label": "Striver — Floor in a BST", "url": "https://takeuforward.org/data-structure/floor-in-a-binary-search-tree/"},
            _SHEET,
        ],
        "understanding": "Largest value ≤ x in the BST. Return -1 if none.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "When current ≤ x, record and try right; when current > x, go left.",
        "optimized": {
            "explanation": "Single descent.",
            "code": r'''
def bst_floor(root, x):
    floor = -1
    while root:
        if root.val == x:
            return root.val
        if root.val < x:
            floor = root.val
            root = root.right             # try to find larger candidate
        else:
            root = root.left
    return floor
''',
            "complexity": "Time O(h), space O(1).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Track floor candidate; descend right when current ≤ x, left otherwise.",
    },

    # ------------------------------------------------------------------
    # 6) BST Insert
    # ------------------------------------------------------------------
    {
        "id": "bst-insert",
        "title": "Insert a Node in a BST",
        "step_id": 14,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["bst"],
        "what_this_teaches": "Insertion creates a new leaf — descend until you find an empty slot.",
        "pattern": "BST descent + leaf attach.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["bst-search"],
        "next_problems": ["bst-delete"],
        "resources": [
            _lc(701, "insert-into-a-binary-search-tree"),
            _SHEET,
        ],
        "understanding": "Insert a new value such that the BST property is preserved. New nodes always become leaves.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Standard BST descent; when you hit a None child, replace it with the new node.",
        "optimized": {
            "explanation": "Iterative insert.",
            "code": r'''
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right

def insert_into_bst(root, val):
    if not root:
        return TreeNode(val)
    cur = root
    while True:
        if val < cur.val:
            if cur.left is None:
                cur.left = TreeNode(val); return root
            cur = cur.left
        else:
            if cur.right is None:
                cur.right = TreeNode(val); return root
            cur = cur.right
''',
            "complexity": "Time O(h), space O(1).",
        },
        "deep_concept": "Insertions preserve the BST property but not balance — repeated insertions of sorted data create a degenerate chain. Balanced variants (AVL, RB) fix this with rotations.",
        "confusion_notes": [
            {
                "question": "What if the value already exists?",
                "answer": "By convention, duplicates go right (or are disallowed entirely). LeetCode 701 guarantees uniqueness, so this case doesn't arise.",
            },
        ],
        "summary": "Descend until you find a None child; attach a new node there.",
    },

    # ------------------------------------------------------------------
    # 7) BST Delete
    # ------------------------------------------------------------------
    {
        "id": "bst-delete",
        "title": "Delete a Node from a BST",
        "step_id": 14,
        "lecture_id": 2,
        "difficulty": "hard",
        "tags": ["bst"],
        "what_this_teaches": "Three deletion cases (leaf, one child, two children) and the inorder-successor swap.",
        "pattern": "BST descent + structural rewire.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["bst-insert"],
        "next_problems": ["validate-bst"],
        "resources": [
            _lc(450, "delete-node-in-a-bst"),
            _SHEET,
        ],
        "understanding": r'''
Delete a node with given value from a BST while preserving the BST
property. Three cases:
- **Leaf:** just remove it.
- **One child:** replace the node with its child.
- **Two children:** replace the node's value with its inorder successor
  (or predecessor), then delete the successor from the right subtree.
''',
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Recursive: walk to the target, then handle the three cases.",
        "optimized": {
            "explanation": "Recursive delete with inorder-successor swap.",
            "code": r'''
def delete_node(root, key):
    if not root:
        return None
    if key < root.val:
        root.left  = delete_node(root.left, key)
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else:
        # found the target
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        # two children: find successor (leftmost in right subtree)
        succ = root.right
        while succ.left:
            succ = succ.left
        root.val = succ.val
        root.right = delete_node(root.right, succ.val)
    return root
''',
            "complexity": "Time O(h), space O(h) recursion.",
        },
        "deep_concept": "The successor swap is the standard trick to delete a node with two children without violating the BST property — we 'replace' the node's identity with the smallest value still > it.",
        "confusion_notes": [
            {
                "question": "Why use the *inorder successor* instead of predecessor?",
                "answer": "Either works! Successor (smallest in right subtree) is conventional. Predecessor (largest in left subtree) is symmetric. Pick one and stick with it.",
            },
        ],
        "summary": "Recurse to the target. Leaf → remove. One child → replace with child. Two children → swap with inorder successor, then delete successor.",
    },

    # ------------------------------------------------------------------
    # 8) Kth Smallest / Largest
    # ------------------------------------------------------------------
    {
        "id": "bst-kth-smallest-largest",
        "title": "Kth Smallest / Largest Element in a BST",
        "step_id": 14,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["bst", "inorder"],
        "what_this_teaches": "Inorder traversal with an early-exit counter.",
        "pattern": "Counting via inorder.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["inorder"],
        "next_problems": ["validate-bst"],
        "resources": [
            _lc(230, "kth-smallest-element-in-a-bst"),
            _SHEET,
        ],
        "understanding": r'''
Return the kth smallest value in a BST. Kth largest is symmetric
(reverse inorder).
''',
        "brute_force": {"explanation": "Full inorder, then `out[k-1]`.", "code": "", "complexity": "Time O(n)."},
        "thought_process": "Do iterative inorder; stop when you've popped k nodes.",
        "optimized": {
            "explanation": "Iterative inorder with early exit.",
            "code": r'''
def kth_smallest(root, k):
    stack = []
    cur = root
    while True:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        k -= 1
        if k == 0:
            return cur.val
        cur = cur.right

def kth_largest(root, k):
    # symmetric: reverse inorder = right, root, left
    stack = []
    cur = root
    while True:
        while cur:
            stack.append(cur)
            cur = cur.right
        cur = stack.pop()
        k -= 1
        if k == 0:
            return cur.val
        cur = cur.left
''',
            "complexity": "Time O(h + k), space O(h).",
        },
        "deep_concept": "Inorder gives sorted output, so the kth pop = kth smallest. Early exit saves work when k ≪ n.",
        "confusion_notes": [],
        "summary": "Iterative inorder; stop after k pops.",
    },

    # ------------------------------------------------------------------
    # 9) Validate BST
    # ------------------------------------------------------------------
    {
        "id": "validate-bst",
        "title": "Validate Binary Search Tree",
        "step_id": 14,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["bst", "recursion"],
        "what_this_teaches": "Pass (lo, hi) bounds down the recursion; the BST property requires lo < node.val < hi at every node.",
        "pattern": "DFS with running bounds.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["bst-search"],
        "next_problems": ["bst-lca", "recover-bst"],
        "resources": [
            _lc(98, "validate-binary-search-tree"),
            _SHEET,
        ],
        "understanding": r'''
Decide whether a tree is a valid BST. A common bug: checking only
`node.left.val < node.val < node.right.val` is insufficient — that
only enforces local order, not the *subtree-wide* invariant.
''',
        "brute_force": {
            "explanation": "Compare every ancestor to every node — O(n²).",
            "code": "",
            "complexity": "Time O(n²).",
        },
        "thought_process": "Carry (lo, hi) bounds down the recursion. Every node must lie strictly inside its bounds; descending left tightens the upper bound, descending right tightens the lower bound.",
        "optimized": {
            "explanation": "DFS with bounds.",
            "code": r'''
def is_valid_bst(root, lo=float('-inf'), hi=float('inf')):
    if not root: return True
    if not (lo < root.val < hi):
        return False
    return (is_valid_bst(root.left,  lo, root.val) and
            is_valid_bst(root.right, root.val, hi))
''',
            "complexity": "Time O(n), space O(h).",
        },
        "deep_concept": "Passing bounds is a clean way to propagate ancestor constraints. The same technique appears in 'recover BST' and 'is balanced'.",
        "confusion_notes": [
            {
                "question": "Why use float('inf') for the initial bounds?",
                "answer": "Because the root has no ancestor constraints. Using ±inf makes the first comparison trivially true for any finite value.",
            },
            {
                "question": "Can I just inorder-traverse and check sorted?",
                "answer": "Yes — that's an alternative (O(n) time + O(n) space). The bounds-DFS uses O(h) space and stops early on the first violation.",
            },
        ],
        "summary": "DFS with (lo, hi) bounds; each node must satisfy lo < val < hi.",
    },

    # ------------------------------------------------------------------
    # 10) BST LCA
    # ------------------------------------------------------------------
    {
        "id": "bst-lca",
        "title": "Lowest Common Ancestor in a BST",
        "step_id": 14,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["bst"],
        "what_this_teaches": "Exploit BST property: descend until the two values straddle the current node.",
        "pattern": "BST descent on a divergence point.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["lca-binary-tree", "bst-search"],
        "next_problems": ["bst-from-preorder"],
        "resources": [
            _lc(235, "lowest-common-ancestor-of-a-binary-search-tree"),
            _SHEET,
        ],
        "understanding": r'''
Given a BST and two values p, q, find their LCA. The BST version is
much simpler than the general binary-tree LCA: walk down from the
root; when p and q both lie on the same side (both < or both >),
descend that way; otherwise the current node is the LCA.
''',
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "—",
        "optimized": {
            "explanation": "Iterative BST descent.",
            "code": r'''
def lowest_common_ancestor_bst(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root
    return None
''',
            "complexity": "Time O(h), space O(1).",
        },
        "deep_concept": "The BST invariant turns a tree-search problem into a one-dimensional one: 'where do p and q lie relative to the current node?'",
        "confusion_notes": [],
        "summary": "Descend until p and q straddle the current node — that's the LCA.",
    },

    # ------------------------------------------------------------------
    # 11) BST from Preorder
    # ------------------------------------------------------------------
    {
        "id": "bst-from-preorder",
        "title": "Construct a BST from Preorder",
        "step_id": 14,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["bst", "construction", "recursion"],
        "what_this_teaches": "Preorder + BST property → uniquely defined tree. Use bounds to know which subtree each value belongs to.",
        "pattern": "DFS with bounds + global pointer.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["construct-pre-in", "validate-bst"],
        "next_problems": ["bst-iterator"],
        "resources": [
            _lc(1008, "construct-binary-search-tree-from-preorder-traversal"),
            _SHEET,
        ],
        "understanding": r'''
Given the preorder traversal of a BST, reconstruct the tree.

**Key insight:** since this is a BST, the *inorder* is just the sorted
preorder — so preorder alone suffices.
''',
        "brute_force": {
            "explanation": "Build inorder by sorting preorder, then apply the general 'construct from pre+in' algorithm.",
            "code": "",
            "complexity": "Time O(n log n).",
        },
        "thought_process": r'''
**O(n) approach.** Walk the preorder array with an index. For each
value, place it under the current node if it's within the (lo, hi)
bounds; recurse into left subtree with bounds (lo, val), then right
subtree with bounds (val, hi).
''',
        "optimized": {
            "explanation": "Bounds-based recursion.",
            "code": r'''
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right

def bst_from_preorder(preorder):
    i = [0]
    def build(lo, hi):
        if i[0] == len(preorder):
            return None
        val = preorder[i[0]]
        if val < lo or val > hi:
            return None
        i[0] += 1
        node = TreeNode(val)
        node.left  = build(lo, val)
        node.right = build(val, hi)
        return node
    return build(float('-inf'), float('inf'))
''',
            "complexity": "Time O(n), space O(h).",
        },
        "deep_concept": "Bounds-propagation lets us decide *where* each preorder element belongs without searching.",
        "confusion_notes": [
            {
                "question": "Why doesn't the bounds approach revisit elements?",
                "answer": "Because we only `i[0] += 1` when the current value fits the bounds. If it doesn't fit, we return None without consuming, letting an ancestor (with looser bounds) handle it.",
            },
        ],
        "summary": "Walk preorder with running bounds (lo, hi). Build a node only if its value fits, then recurse with tightened bounds.",
    },

    # ------------------------------------------------------------------
    # 12) BST Iterator
    # ------------------------------------------------------------------
    {
        "id": "bst-iterator",
        "title": "Binary Search Tree Iterator",
        "step_id": 14,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["bst", "iterator", "design"],
        "what_this_teaches": "On-demand iterative inorder using a stack — amortized O(1) per next(), O(h) space.",
        "pattern": "Inorder via explicit stack.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["inorder", "bst-kth-smallest-largest"],
        "next_problems": ["bst-two-sum"],
        "resources": [
            _lc(173, "binary-search-tree-iterator"),
            _SHEET,
        ],
        "understanding": r'''
Design an iterator over the inorder traversal of a BST supporting:
- `next()` returns the next smallest element.
- `hasNext()` returns whether there are more elements.

Constraint: O(h) memory, amortized O(1) per `next()`.
''',
        "brute_force": {
            "explanation": "Materialize the full inorder list — O(n) memory.",
            "code": "",
            "complexity": "Memory O(n).",
        },
        "thought_process": "Maintain a stack of 'ancestors waiting to be visited'. Push all lefts initially. On `next()`, pop, save value, push all lefts of the right child.",
        "optimized": {
            "explanation": "Lazy stack-based iterator.",
            "code": r'''
class BSTIterator:
    def __init__(self, root):
        self.stack = []
        self._push_left(root)

    def _push_left(self, n):
        while n:
            self.stack.append(n)
            n = n.left

    def next(self):
        node = self.stack.pop()
        self._push_left(node.right)
        return node.val

    def hasNext(self):
        return bool(self.stack)
''',
            "complexity": "Time amortized O(1) per next, space O(h).",
        },
        "deep_concept": "This is the iterative inorder rewritten as an iterator pattern. The stack holds 'ancestors of the next-to-visit node'.",
        "confusion_notes": [
            {
                "question": "Why amortized O(1) and not strict O(1)?",
                "answer": "Because individual `next()` calls might walk down a long left spine. But across all `next()` calls, every node is pushed and popped exactly once — total work is O(n) for n calls, averaging O(1).",
            },
        ],
        "summary": "Stack of ancestors; push lefts on init and after each `next()` (via the right subtree).",
    },

    # ------------------------------------------------------------------
    # 13) BST Two Sum
    # ------------------------------------------------------------------
    {
        "id": "bst-two-sum",
        "title": "Two Sum IV — Input is a BST",
        "step_id": 14,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["bst", "two-pointer", "iterator"],
        "what_this_teaches": "Two BST iterators — one ascending, one descending — used as two pointers.",
        "pattern": "Two-pointer on a tree via iterators.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["bst-iterator"],
        "next_problems": ["recover-bst"],
        "resources": [
            _lc(653, "two-sum-iv-input-is-a-bst"),
            _SHEET,
        ],
        "understanding": "Return True iff there exist two distinct nodes whose values sum to k.",
        "brute_force": {
            "explanation": "Materialize inorder into a sorted list, then two-pointer. O(n) time, O(n) space.",
            "code": "",
            "complexity": "Time O(n), space O(n).",
        },
        "thought_process": r'''
**O(n) time, O(h) space.** Use two BST iterators: one going forward
(smallest first) and one going backward (largest first). Compare their
sum; advance the appropriate iterator. Same as two-sum on a sorted
array, but the array is virtual.
''',
        "optimized": {
            "explanation": "Forward + reverse iterators acting as two pointers.",
            "code": r'''
class BSTIteratorForward:
    def __init__(self, root):
        self.stack = []
        self._push(root)
    def _push(self, n):
        while n:
            self.stack.append(n); n = n.left
    def next(self):
        node = self.stack.pop()
        self._push(node.right)
        return node.val
    def has_next(self):
        return bool(self.stack)

class BSTIteratorReverse:
    def __init__(self, root):
        self.stack = []
        self._push(root)
    def _push(self, n):
        while n:
            self.stack.append(n); n = n.right
    def next(self):
        node = self.stack.pop()
        self._push(node.left)
        return node.val
    def has_next(self):
        return bool(self.stack)

def find_target(root, k):
    if not root: return False
    fwd = BSTIteratorForward(root)
    bwd = BSTIteratorReverse(root)
    a, b = fwd.next(), bwd.next()
    while a < b:
        s = a + b
        if s == k: return True
        if s < k:
            a = fwd.next() if fwd.has_next() else a + 1
        else:
            b = bwd.next() if bwd.has_next() else b - 1
        if not fwd.has_next() and not bwd.has_next() and a >= b:
            break
    return False
''',
            "complexity": "Time O(n), space O(h).",
        },
        "deep_concept": "Two iterators emulate two pointers on a sorted array without materializing it. Saves O(n) space.",
        "confusion_notes": [],
        "summary": "Two BST iterators (forward + reverse) used as two pointers; compare sum to k and advance the appropriate side.",
    },

    # ------------------------------------------------------------------
    # 14) Recover BST
    # ------------------------------------------------------------------
    {
        "id": "recover-bst",
        "title": "Recover Binary Search Tree",
        "step_id": 14,
        "lecture_id": 2,
        "difficulty": "hard",
        "tags": ["bst", "inorder"],
        "what_this_teaches": "Identifying *two* nodes whose values are swapped by detecting inorder descents.",
        "pattern": "Inorder with state machine.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["validate-bst"],
        "next_problems": ["largest-bst-in-tree"],
        "resources": [
            _lc(99, "recover-binary-search-tree"),
            _SHEET,
        ],
        "understanding": r'''
A BST has exactly two of its nodes accidentally swapped. Restore the
BST in-place without changing the structure.
''',
        "brute_force": {"explanation": "Materialize inorder, sort, write back — O(n log n) time, O(n) space.", "code": "", "complexity": "—"},
        "thought_process": r'''
In a valid BST, inorder is strictly increasing. After a single swap,
there will be either *one* descent (adjacent swap: a > b right next to
each other) or *two* descents (non-adjacent swap). Find them:
- First descent: `first = previous`, `second = current`.
- Second descent (if any): `second = current`.

After scanning, swap `first.val` and `second.val`.
''',
        "optimized": {
            "explanation": "Single-pass inorder tracking two violation nodes.",
            "code": r'''
def recover_tree(root):
    first = second = prev = None
    def inorder(n):
        nonlocal first, second, prev
        if not n: return
        inorder(n.left)
        if prev and prev.val > n.val:
            if not first:
                first = prev
            second = n
        prev = n
        inorder(n.right)
    inorder(root)
    first.val, second.val = second.val, first.val
''',
            "complexity": "Time O(n), space O(h).",
        },
        "deep_concept": "Inorder converts BST validity into a simple sortedness check on a sequence. Anomalies in the sequence localize to two positions for a single swap.",
        "confusion_notes": [
            {
                "question": "Why does the adjacent vs non-adjacent case need different handling?",
                "answer": "Adjacent swap (a, b with a > b right next to each other): just one descent at the boundary. Non-adjacent swap: two descents — one where the bigger value first appears too high, one where the smaller value first appears too low. The code handles both by setting `first` only on the *first* descent and always updating `second` on the *latest* descent.",
            },
        ],
        "summary": "Inorder; mark `first` on the 1st descent and `second` on the latest. Swap their values.",
    },

    # ------------------------------------------------------------------
    # 15) Largest BST in a Tree
    # ------------------------------------------------------------------
    {
        "id": "largest-bst-in-tree",
        "title": "Largest BST in a Binary Tree",
        "step_id": 14,
        "lecture_id": 2,
        "difficulty": "hard",
        "tags": ["bst", "dp-on-tree"],
        "what_this_teaches": "Post-order DFS returning (is_bst, min, max, size) from each subtree.",
        "pattern": "Bottom-up DP on tree.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["validate-bst"],
        "next_problems": [],
        "resources": [
            {"label": "GFG — Largest BST in a Binary Tree", "url": "https://www.geeksforgeeks.org/largest-bst-binary-tree-set-2/"},
            _SHEET,
        ],
        "understanding": r'''
Given a binary tree (not necessarily a BST), find the size (number of
nodes) of the largest subtree that is a valid BST.
''',
        "brute_force": {
            "explanation": "For every subtree, check if it's a BST and count its size — O(n²).",
            "code": "",
            "complexity": "Time O(n²).",
        },
        "thought_process": r'''
Single-pass post-order DFS. Each call returns a tuple
`(min_val, max_val, size)`:
- For a None subtree: (`+inf`, `-inf`, 0) — vacuously valid.
- For a leaf: (val, val, 1).
- For an internal node: combine with left/right. Subtree is a BST iff
  `left.max < node.val < right.min`. If yes, return
  `(left.min, right.max, left.size + right.size + 1)`. Otherwise
  return `(-inf, +inf, max(left.size, right.size))` — invalid marker
  with the best-so-far size.

Track the global best as we go.
''',
        "optimized": {
            "explanation": "Post-order with tuple return.",
            "code": r'''
def largest_bst(root):
    INF = float('inf')
    def dfs(n):
        if not n:
            return (INF, -INF, 0)
        lmin, lmax, lsize = dfs(n.left)
        rmin, rmax, rsize = dfs(n.right)
        if lmax < n.val < rmin:
            return (min(lmin, n.val), max(rmax, n.val), lsize + rsize + 1)
        return (-INF, INF, max(lsize, rsize))    # invalid marker
    return dfs(root)[2]
''',
            "complexity": "Time O(n), space O(h).",
        },
        "deep_concept": "Carrying just enough state (min, max, size) lets the parent decide validity in O(1). This is a classic example of 'tree DP' design.",
        "confusion_notes": [
            {
                "question": "Why use `-INF, INF` for the invalid marker?",
                "answer": "Because the parent checks `lmax < node.val < rmin`. If left was invalid we want this check to *always fail* for the parent — return `lmax = INF` (forcing INF < node.val to fail) or similar. The marker style we used works because `lmax = -INF` means parent's check `lmax < node.val` succeeds *only* if rmin is also `INF`, which forces the parent's check `node.val < rmin = INF` to succeed too. But that gives a false positive! Carefully: we should return `(-INF, INF, …)` (left side min = -INF which can never be a valid BST's min, but here we just need the bounds to fail the parent's BST check). In practice both forms can work; the cleanest is to also return a boolean.",
            },
            {
                "question": "Is the entire tree a BST counted?",
                "answer": "Yes — if the whole tree is a BST, the result is n (the total node count). We take 'size of largest BST subtree' literally.",
            },
        ],
        "summary": "Post-order DFS returning (min, max, size). Subtree is BST iff `lmax < val < rmin`. Track global max size.",
    },
]
