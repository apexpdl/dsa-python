"""The Striver A-Z DSA Sheet, organized as a tree of steps and lectures.

Each problem here is referenced by its `id`. The actual long-form content
lives in `content/problems/...`. Keeping the structure separate from the
content lets us list the whole sheet even for problems whose deep write-up
is not finished yet.
"""
from __future__ import annotations

CURRICULUM: list[dict] = [
    # ---------------------------------------------------------------
    # STEP 1: Learn the Basics
    # ---------------------------------------------------------------
    {
        "id": 1,
        "title": "Learn the Basics",
        "summary": (
            "The starting line. Before solving real problems, we make sure "
            "the fundamentals — input/output, data types, loops, functions, "
            "basic math, recursion, and hashing — feel completely natural."
        ),
        "lectures": [
            {
                "id": 1,
                "title": "Things to Know in Python",
                "problems": [
                    "user-input-output",
                    "data-types",
                    "if-else-statements",
                    "match-case-statement",
                    "arrays-and-strings",
                    "for-while-loops",
                    "functions",
                    "time-space-complexity",
                ],
            },
            {
                "id": 2,
                "title": "Build-up Logical Thinking (Patterns)",
                "problems": [
                    "pattern-square",
                    "pattern-right-triangle",
                    "pattern-inverted-triangle",
                    "pattern-number-pyramid",
                    "pattern-diamond",
                ],
            },
            {
                "id": 3,
                "title": "Learn Python Collections (the STL of Python)",
                "problems": [
                    "python-list-collection",
                    "python-deque",
                    "python-stack-queue",
                    "python-heapq",
                    "python-set",
                    "python-dict",
                    "python-sorting",
                ],
            },
            {
                "id": 4,
                "title": "Know Basic Maths",
                "problems": [
                    "count-digits",
                    "reverse-number",
                    "check-palindrome-number",
                    "gcd-lcm",
                    "armstrong-number",
                    "print-all-divisors",
                    "check-for-prime",
                ],
            },
            {
                "id": 5,
                "title": "Learn Basic Recursion",
                "problems": [
                    "print-n-times",
                    "print-1-to-n",
                    "print-n-to-1",
                    "sum-first-n",
                    "factorial-of-n",
                    "reverse-an-array-recursion",
                    "check-string-palindrome-recursion",
                    "fibonacci-number",
                ],
            },
            {
                "id": 6,
                "title": "Learn Basic Hashing",
                "problems": [
                    "count-frequencies",
                    "highest-lowest-frequency",
                ],
            },
        ],
    },
    # ---------------------------------------------------------------
    # STEP 2: Sorting
    # ---------------------------------------------------------------
    {
        "id": 2,
        "title": "Learn Important Sorting Techniques",
        "summary": (
            "Sorting is the warm-up gym for algorithmic thinking. Every "
            "sort teaches a reusable pattern: comparisons, swaps, "
            "divide-and-conquer, partitions."
        ),
        "lectures": [
            {
                "id": 1,
                "title": "Sorting - I",
                "problems": [
                    "selection-sort",
                    "bubble-sort",
                    "insertion-sort",
                ],
            },
            {
                "id": 2,
                "title": "Sorting - II",
                "problems": [
                    "merge-sort",
                    "recursive-bubble-sort",
                    "recursive-insertion-sort",
                    "quick-sort",
                ],
            },
        ],
    },
    # ---------------------------------------------------------------
    # STEP 3: Arrays
    # ---------------------------------------------------------------
    {
        "id": 3,
        "title": "Solve Problems on Arrays",
        "summary": (
            "Arrays are where most algorithmic patterns first show up. "
            "Linear scans, two pointers, prefix sums, hashing — they all "
            "make their first appearance here."
        ),
        "lectures": [
            {
                "id": 1,
                "title": "Easy",
                "problems": [
                    "largest-element",
                    "second-largest-element",
                    "check-array-sorted",
                    "remove-duplicates-sorted",
                    "left-rotate-by-one",
                    "left-rotate-by-d",
                    "move-zeros-to-end",
                    "linear-search",
                    "union-of-sorted-arrays",
                    "intersection-of-sorted-arrays",
                    "missing-number",
                    "max-consecutive-ones",
                    "single-number",
                    "longest-subarray-with-sum-k",
                ],
            },
            {
                "id": 2,
                "title": "Medium",
                "problems": [
                    "two-sum",
                    "sort-0s-1s-2s",
                    "majority-element",
                    "kadane-algorithm",
                    "print-max-subarray",
                    "stock-buy-sell",
                    "rearrange-alternating",
                    "next-permutation",
                    "leaders-in-array",
                    "longest-consecutive-sequence",
                    "set-matrix-zeros",
                    "rotate-matrix-90",
                    "spiral-traversal",
                    "subarrays-with-sum-k",
                ],
            },
            {
                "id": 3,
                "title": "Hard",
                "problems": [
                    "pascals-triangle",
                    "majority-element-n3",
                    "three-sum",
                    "four-sum",
                    "longest-subarray-zero-sum",
                    "subarrays-with-xor-k",
                    "merge-overlapping-intervals",
                    "merge-two-sorted-no-extra-space",
                    "repeating-and-missing",
                    "count-inversions",
                    "reverse-pairs",
                    "max-product-subarray",
                ],
            },
        ],
    },
    # ---------------------------------------------------------------
    # STEP 4: Binary Search
    # ---------------------------------------------------------------
    {
        "id": 4,
        "title": "Binary Search",
        "summary": (
            "Binary search is not just a search algorithm — it's a way of "
            "thinking. Once you see 'monotonic decision space', you can "
            "binary search over the answer itself."
        ),
        "lectures": [
            {
                "id": 1,
                "title": "BS on 1D Arrays",
                "problems": [
                    "binary-search",
                    "lower-bound",
                    "upper-bound",
                    "search-insert-position",
                    "floor-ceil-sorted",
                    "first-last-occurrence",
                    "count-occurrences",
                    "search-rotated-i",
                    "search-rotated-ii",
                    "min-in-rotated",
                    "rotations-count",
                    "single-element-sorted",
                    "find-peak-element",
                ],
            },
            {
                "id": 2,
                "title": "BS on Answers",
                "problems": [
                    "sqrt-using-bs",
                    "nth-root",
                    "koko-bananas",
                    "min-days-bouquets",
                    "smallest-divisor-threshold",
                    "ship-packages-d-days",
                    "kth-missing-positive",
                    "aggressive-cows",
                    "book-allocation",
                    "split-array-largest-sum",
                    "painters-partition",
                    "minimize-max-distance",
                    "median-two-sorted",
                    "kth-element-two-sorted",
                ],
            },
            {
                "id": 3,
                "title": "BS on 2D Arrays",
                "problems": [
                    "search-2d-matrix",
                    "search-2d-matrix-ii",
                    "peak-element-2d",
                    "matrix-median",
                ],
            },
        ],
    },
    # ---------------------------------------------------------------
    # STEP 5: Strings
    # ---------------------------------------------------------------
    {
        "id": 5,
        "title": "Strings",
        "summary": (
            "Strings are arrays of characters with extra rules. They "
            "force you to think about characters, indices, and substrings."
        ),
        "lectures": [
            {
                "id": 1,
                "title": "Basic and Easy",
                "problems": [
                    "remove-outer-parentheses",
                    "reverse-words",
                    "largest-odd-number",
                    "longest-common-prefix",
                    "isomorphic-strings",
                    "rotation-of-string",
                ],
            },
            {
                "id": 2,
                "title": "Medium",
                "problems": [
                    "sort-characters-by-frequency",
                    "max-nesting-depth",
                    "roman-to-integer",
                    "integer-to-roman",
                    "atoi",
                    "substrings-k-distinct",
                    "longest-palindromic-substring",
                    "beauty-of-substrings",
                ],
            },
        ],
    },
    # ---------------------------------------------------------------
    # STEP 6: Linked List
    # ---------------------------------------------------------------
    {
        "id": 6,
        "title": "Linked List",
        "summary": (
            "A linked list is the simplest example of a pointer-based "
            "data structure. Mastering it builds intuition for trees, "
            "graphs, and complex pointer manipulation."
        ),
        "lectures": [
            {
                "id": 1,
                "title": "Singly Linked List Basics",
                "problems": [
                    "ll-introduction",
                    "ll-insert-node",
                    "ll-delete-node",
                    "ll-length",
                    "ll-search",
                ],
            },
            {
                "id": 2,
                "title": "Doubly Linked List Basics",
                "problems": [
                    "dll-introduction",
                    "dll-insert",
                    "dll-delete",
                    "dll-reverse",
                ],
            },
            {
                "id": 3,
                "title": "Medium Singly LL Problems",
                "problems": [
                    "ll-middle",
                    "ll-reverse",
                    "ll-detect-loop",
                    "ll-loop-start",
                    "ll-loop-length",
                    "ll-palindrome",
                    "ll-odd-even",
                    "ll-remove-nth-from-end",
                    "ll-delete-middle",
                    "ll-sort",
                    "ll-sort-012",
                    "ll-intersection",
                    "ll-add-one",
                    "ll-add-two-numbers",
                ],
            },
            {
                "id": 4,
                "title": "Medium Doubly LL Problems",
                "problems": [
                    "dll-delete-occurrences",
                    "dll-pairs-with-sum",
                    "dll-remove-duplicates",
                ],
            },
            {
                "id": 5,
                "title": "Hard LL Problems",
                "problems": [
                    "ll-reverse-k-group",
                    "ll-rotate",
                    "ll-flatten",
                    "ll-clone-random-pointer",
                ],
            },
        ],
    },
    # ---------------------------------------------------------------
    # STEP 7: Recursion patterns
    # ---------------------------------------------------------------
    {
        "id": 7,
        "title": "Recursion (Pattern-wise)",
        "summary": (
            "Recursion is the brain of advanced DSA. Once you see "
            "subsequence, subset, and 'try every option' problems "
            "through a recursion lens, half of DSA opens up."
        ),
        "lectures": [
            {
                "id": 1,
                "title": "Get a Strong Hold",
                "problems": [
                    "atoi-recursive",
                    "pow-x-n",
                    "count-good-numbers",
                    "sort-stack-recursion",
                    "reverse-stack-recursion",
                ],
            },
            {
                "id": 2,
                "title": "Subsequence Pattern",
                "problems": [
                    "binary-strings-no-consecutive-ones",
                    "generate-parentheses",
                    "print-all-subsequences",
                    "subsequence-sum-k",
                    "combination-sum",
                    "combination-sum-ii",
                    "subset-sum-i",
                    "subset-sum-ii",
                    "combination-sum-iii",
                    "letter-combinations-phone",
                ],
            },
            {
                "id": 3,
                "title": "Trying out all Combos / Hard",
                "problems": [
                    "palindrome-partitioning",
                    "word-search",
                    "n-queens",
                    "sudoku-solver",
                    "m-coloring",
                    "rat-in-a-maze",
                    "word-break",
                    "expression-add-operators",
                ],
            },
        ],
    },
    # ---------------------------------------------------------------
    # STEP 8: Bit Manipulation
    # ---------------------------------------------------------------
    {
        "id": 8,
        "title": "Bit Manipulation",
        "summary": (
            "Bits feel intimidating but reward huge speedups. Most bit "
            "tricks reduce to: 'use AND, OR, XOR to ask one yes/no "
            "question per bit position'."
        ),
        "lectures": [
            {
                "id": 1,
                "title": "Learn Bit Manipulation",
                "problems": [
                    "bit-introduction",
                    "check-odd-even-bits",
                    "check-power-of-two",
                    "count-set-bits",
                    "set-unset-rightmost",
                    "swap-using-xor",
                    "divide-without-mul-div",
                ],
            },
            {
                "id": 2,
                "title": "Interview Problems",
                "problems": [
                    "min-bit-flips",
                    "single-number-i",
                    "single-number-ii",
                    "single-number-iii",
                    "power-set-bitwise",
                    "xor-product-subarray",
                ],
            },
            {
                "id": 3,
                "title": "Advanced Maths",
                "problems": [
                    "prime-factors",
                    "sieve-of-eratosthenes",
                    "segmented-sieve",
                    "gcd-euclidean",
                    "all-divisors",
                ],
            },
        ],
    },
    # ---------------------------------------------------------------
    # STEP 9: Stack and Queues
    # ---------------------------------------------------------------
    {
        "id": 9,
        "title": "Stack and Queues",
        "summary": (
            "Stacks and queues are the simplest 'memory shapes'. Once "
            "you internalize LIFO and FIFO thinking, monotonic stacks "
            "and sliding windows feel natural."
        ),
        "lectures": [
            {
                "id": 1,
                "title": "Learning",
                "problems": [
                    "stack-using-arrays",
                    "queue-using-arrays",
                    "stack-using-queue",
                    "queue-using-stack",
                    "stack-using-ll",
                    "queue-using-ll",
                    "balanced-parentheses",
                    "min-stack",
                ],
            },
            {
                "id": 2,
                "title": "Prefix / Infix / Postfix Conversions",
                "problems": [
                    "infix-to-postfix",
                    "infix-to-prefix",
                    "postfix-to-infix",
                    "prefix-to-infix",
                    "postfix-to-prefix",
                    "prefix-to-postfix",
                ],
            },
            {
                "id": 3,
                "title": "Monotonic Stack/Queue",
                "problems": [
                    "next-greater-element-i",
                    "next-greater-element-ii",
                    "next-smaller-element",
                    "count-nges-right",
                    "trapping-rain-water",
                    "sum-subarray-minimums",
                    "asteroid-collision",
                    "sum-subarray-ranges",
                    "largest-rectangle-histogram",
                    "maximal-rectangle",
                    "remove-k-digits",
                    "sliding-window-maximum",
                ],
            },
            {
                "id": 4,
                "title": "Implementation Problems",
                "problems": [
                    "online-stock-span",
                    "celebrity-problem",
                    "lru-cache",
                    "lfu-cache",
                ],
            },
        ],
    },
    # ---------------------------------------------------------------
    # STEP 10: Sliding Window & Two Pointer
    # ---------------------------------------------------------------
    {
        "id": 10,
        "title": "Sliding Window & Two Pointer",
        "summary": (
            "Two beautiful patterns that look like magic to beginners "
            "but make complete sense once you see them as 'don't redo "
            "work you already did'."
        ),
        "lectures": [
            {
                "id": 1,
                "title": "Medium",
                "problems": [
                    "longest-substring-no-repeat",
                    "max-consecutive-ones-iii",
                    "fruit-into-baskets",
                    "longest-substring-k-distinct",
                    "substrings-containing-three",
                    "longest-repeating-replacement",
                    "binary-subarrays-with-sum",
                    "nice-subarrays",
                    "subarrays-k-different-integers",
                ],
            },
            {
                "id": 2,
                "title": "Hard",
                "problems": [
                    "min-window-substring",
                    "min-window-subsequence",
                ],
            },
        ],
    },
    # ---------------------------------------------------------------
    # STEP 11: Heaps
    # ---------------------------------------------------------------
    {
        "id": 11,
        "title": "Heaps",
        "summary": (
            "A heap is the right tool whenever you need the 'next best' "
            "thing repeatedly. Top-K problems, schedulers, median "
            "streams — all heaps."
        ),
        "lectures": [
            {
                "id": 1,
                "title": "Learning",
                "problems": [
                    "heap-introduction",
                    "min-max-heap-impl",
                    "heap-array-impl",
                    "is-max-heap",
                ],
            },
            {
                "id": 2,
                "title": "Medium",
                "problems": [
                    "kth-largest",
                    "kth-smallest",
                    "replace-by-rank",
                    "task-scheduler",
                    "hand-of-straights",
                    "design-twitter",
                    "merge-k-sorted-lists",
                ],
            },
            {
                "id": 3,
                "title": "Hard",
                "problems": [
                    "median-from-stream",
                    "max-sum-combinations",
                    "k-most-frequent",
                    "top-k-frequent",
                ],
            },
        ],
    },
    # ---------------------------------------------------------------
    # STEP 12: Greedy
    # ---------------------------------------------------------------
    {
        "id": 12,
        "title": "Greedy Algorithms",
        "summary": (
            "Greedy is 'take the best local choice and hope it leads to "
            "the best global outcome'. Sometimes it works, sometimes it "
            "lies — you need to learn the difference."
        ),
        "lectures": [
            {
                "id": 1,
                "title": "Easy",
                "problems": [
                    "assign-cookies",
                    "fractional-knapsack",
                    "lemonade-change",
                    "valid-parenthesis-string",
                    "job-sequencing",
                ],
            },
            {
                "id": 2,
                "title": "Medium / Hard",
                "problems": [
                    "n-meetings",
                    "jump-game-i",
                    "jump-game-ii",
                    "min-platforms",
                    "candy",
                    "ip-address-restoration",
                    "insert-intervals",
                    "merge-intervals",
                    "non-overlapping-intervals",
                    "sjf-scheduling",
                ],
            },
        ],
    },
    # ---------------------------------------------------------------
    # STEP 13: Binary Trees
    # ---------------------------------------------------------------
    {
        "id": 13,
        "title": "Binary Trees",
        "summary": (
            "Trees feel scary until you realize every tree problem "
            "reduces to: 'what should I do at this node, and what do I "
            "want from my left and right children?'"
        ),
        "lectures": [
            {
                "id": 1,
                "title": "Traversals",
                "problems": [
                    "tree-introduction",
                    "binary-tree-representation",
                    "preorder",
                    "inorder",
                    "postorder",
                    "level-order",
                    "all-traversals-one-pass",
                ],
            },
            {
                "id": 2,
                "title": "Medium",
                "problems": [
                    "tree-height",
                    "tree-balanced",
                    "tree-diameter",
                    "max-path-sum",
                    "trees-identical",
                    "zigzag-traversal",
                    "boundary-traversal",
                    "vertical-order",
                    "top-view",
                    "bottom-view",
                    "right-left-view",
                    "symmetric-tree",
                ],
            },
            {
                "id": 3,
                "title": "Hard",
                "problems": [
                    "root-to-node-path",
                    "lca-binary-tree",
                    "max-width",
                    "children-sum",
                    "nodes-at-k-distance",
                    "burning-tree",
                    "count-complete-tree-nodes",
                    "unique-tree-requirements",
                    "construct-pre-in",
                    "construct-post-in",
                    "serialize-deserialize",
                    "morris-inorder",
                    "morris-preorder",
                    "flatten-tree",
                ],
            },
        ],
    },
    # ---------------------------------------------------------------
    # STEP 14: BST
    # ---------------------------------------------------------------
    {
        "id": 14,
        "title": "Binary Search Trees (BST)",
        "summary": (
            "A BST is what happens when you ask 'how can I keep a "
            "sorted set that still supports fast insert and delete?'"
        ),
        "lectures": [
            {
                "id": 1,
                "title": "Concepts",
                "problems": [
                    "bst-introduction",
                    "bst-search",
                    "bst-min-max",
                ],
            },
            {
                "id": 2,
                "title": "Practice",
                "problems": [
                    "bst-ceil",
                    "bst-floor",
                    "bst-insert",
                    "bst-delete",
                    "bst-kth-smallest-largest",
                    "validate-bst",
                    "bst-lca",
                    "bst-from-preorder",
                    "bst-iterator",
                    "bst-two-sum",
                    "recover-bst",
                    "largest-bst-in-tree",
                ],
            },
        ],
    },
    # ---------------------------------------------------------------
    # STEP 15: Graphs
    # ---------------------------------------------------------------
    {
        "id": 15,
        "title": "Graphs",
        "summary": (
            "Graphs unify maps, networks, dependencies, social "
            "connections — anywhere with 'things' and 'relationships'. "
            "BFS and DFS are the alphabets you build everything from."
        ),
        "lectures": [
            {
                "id": 1,
                "title": "Learning",
                "problems": [
                    "graph-introduction",
                    "graph-representation",
                    "connected-components",
                    "graph-bfs",
                    "graph-dfs",
                ],
            },
            {
                "id": 2,
                "title": "BFS / DFS Problems",
                "problems": [
                    "number-of-provinces",
                    "connected-components-undirected",
                    "rotten-oranges",
                    "flood-fill",
                    "cycle-undirected-bfs",
                    "cycle-undirected-dfs",
                    "distance-of-nearest-1",
                    "surrounded-regions",
                    "number-of-enclaves",
                    "number-of-distinct-islands",
                    "bipartite-bfs",
                    "bipartite-dfs",
                    "cycle-directed-dfs",
                ],
            },
            {
                "id": 3,
                "title": "Topo Sort",
                "problems": [
                    "topo-sort-dfs",
                    "kahns-algorithm",
                    "cycle-directed-bfs",
                    "course-schedule-i",
                    "course-schedule-ii",
                    "eventual-safe-states",
                    "alien-dictionary",
                ],
            },
            {
                "id": 4,
                "title": "Shortest Path",
                "problems": [
                    "shortest-path-undirected-unit",
                    "shortest-path-dag",
                    "dijkstra",
                    "shortest-path-weighted-undirected",
                    "path-min-effort",
                    "cheapest-flights-k-stops",
                    "network-delay-time",
                    "number-of-ways-shortest",
                    "city-with-smallest-neighbors",
                    "bellman-ford",
                    "floyd-warshall",
                ],
            },
            {
                "id": 5,
                "title": "MST / DSU",
                "problems": [
                    "prims-algorithm",
                    "kruskals-algorithm",
                    "dsu-rank-size",
                    "provinces-dsu",
                    "ops-to-make-connected",
                    "account-merge",
                    "number-of-islands-ii",
                    "making-large-island",
                    "swim-in-water",
                ],
            },
            {
                "id": 6,
                "title": "Other Algorithms",
                "problems": [
                    "kosaraju",
                    "tarjan-bridges",
                    "articulation-points",
                ],
            },
        ],
    },
    # ---------------------------------------------------------------
    # STEP 16: Dynamic Programming
    # ---------------------------------------------------------------
    {
        "id": 16,
        "title": "Dynamic Programming",
        "summary": (
            "DP is just recursion + a sticky note that remembers "
            "answers. Almost every DP solution is born from a recursive "
            "brute force that you stop repeating."
        ),
        "lectures": [
            {
                "id": 1,
                "title": "Introduction",
                "problems": [
                    "dp-introduction",
                ],
            },
            {
                "id": 2,
                "title": "1D DP",
                "problems": [
                    "climbing-stairs",
                    "frog-jump",
                    "frog-jump-k",
                    "house-robber-i",
                    "house-robber-ii",
                ],
            },
            {
                "id": 3,
                "title": "2D/3D DP on Grids",
                "problems": [
                    "ninjas-training",
                    "grid-unique-paths",
                    "grid-unique-paths-ii",
                    "min-path-sum-grid",
                    "min-path-sum-triangle",
                    "min-max-falling-path",
                    "chocolate-pickup",
                ],
            },
            {
                "id": 4,
                "title": "DP on Subsequences",
                "problems": [
                    "subset-sum-target",
                    "partition-equal-subset-sum",
                    "partition-min-diff",
                    "count-subsets-sum-k",
                    "count-partitions-given-diff",
                    "knapsack-01",
                    "min-coins",
                    "target-sum",
                    "coin-change-2",
                    "unbounded-knapsack",
                    "rod-cutting",
                ],
            },
            {
                "id": 5,
                "title": "DP on Strings",
                "problems": [
                    "lcs",
                    "print-lcs",
                    "longest-common-substring",
                    "longest-palindromic-subseq",
                    "min-insertions-palindrome",
                    "min-ops-convert-a-to-b",
                    "shortest-common-supersequence",
                    "distinct-subsequences",
                    "edit-distance",
                    "wildcard-matching",
                ],
            },
            {
                "id": 6,
                "title": "DP on Stocks",
                "problems": [
                    "stock-i",
                    "stock-ii",
                    "stock-iii",
                    "stock-iv",
                    "stock-cooldown",
                    "stock-fee",
                ],
            },
            {
                "id": 7,
                "title": "DP on LIS",
                "problems": [
                    "lis",
                    "print-lis",
                    "lis-binary-search",
                    "largest-divisible-subset",
                    "longest-string-chain",
                    "longest-bitonic-subseq",
                    "number-of-lis",
                ],
            },
            {
                "id": 8,
                "title": "MCM / Partition DP",
                "problems": [
                    "matrix-chain-multiplication",
                    "min-cost-cut-stick",
                    "burst-balloons",
                    "boolean-parenthesization",
                    "palindrome-partitioning-ii",
                    "partition-max-sum",
                ],
            },
            {
                "id": 9,
                "title": "DP on Squares",
                "problems": [
                    "maximal-square",
                    "count-square-submatrices",
                ],
            },
        ],
    },
    # ---------------------------------------------------------------
    # STEP 17: Tries
    # ---------------------------------------------------------------
    {
        "id": 17,
        "title": "Tries",
        "summary": (
            "A trie is a tree of characters. It's the perfect tool "
            "whenever you need to answer 'is this a prefix?' fast."
        ),
        "lectures": [
            {
                "id": 1,
                "title": "Theory & Implementation",
                "problems": [
                    "trie-impl-i",
                    "trie-impl-ii",
                ],
            },
            {
                "id": 2,
                "title": "Practice",
                "problems": [
                    "longest-word-all-prefixes",
                    "distinct-substrings-count",
                    "max-xor-two-numbers",
                    "max-xor-with-element-queries",
                ],
            },
        ],
    },
    # ---------------------------------------------------------------
    # STEP 18: Advanced Strings
    # ---------------------------------------------------------------
    {
        "id": 18,
        "title": "Advanced Strings",
        "summary": (
            "The string algorithms that make pattern matching fast. "
            "These are not beginner topics — but every motivated learner "
            "should at least know what they are."
        ),
        "lectures": [
            {
                "id": 1,
                "title": "Hard Patterns",
                "problems": [
                    "z-algorithm",
                    "kmp-algorithm",
                    "rabin-karp",
                    "shortest-palindrome",
                ],
            },
        ],
    },
]
