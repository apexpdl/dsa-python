"""Step 16 extras — Dynamic Programming (53 problems).

Comprehensive coverage of Striver A-Z Step 16: DP intro, 1D DP, 2D/3D DP
on grids, DP on subsequences (knapsack family), DP on strings, DP on
stocks, DP on LIS, MCM / partition DP, and DP on squares.
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
    # ==================================================================
    # INTRODUCTION
    # ==================================================================
    {
        "id": "dp-introduction",
        "title": "Introduction to Dynamic Programming",
        "step_id": 16,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["dp", "concept"],
        "what_this_teaches": "What DP is, when to use it, memoization vs tabulation, and the key concepts of overlapping subproblems and optimal substructure.",
        "pattern": "Conceptual overview.",
        "prerequisite_lessons": ["recursion"],
        "prerequisite_problems": [],
        "next_problems": ["climbing-stairs", "frog-jump"],
        "resources": [
            {"label": "Striver — Introduction to DP", "url": "https://takeuforward.org/dynamic-programming/striver-dp-series-dynamic-programming-problems/"},
            _SHEET,
        ],
        "understanding": r'''
**Dynamic Programming** is a technique for solving problems that have:
1. **Optimal substructure** — the optimal answer for a problem can be
   built from optimal answers to smaller subproblems.
2. **Overlapping subproblems** — the same subproblems are solved many
   times by naive recursion.

DP avoids the redundant work by **memoizing** (caching) subproblem
answers, or **tabulating** them bottom-up.

**Memoization (top-down):** write the natural recursion, add a cache.
**Tabulation (bottom-up):** identify the smallest subproblems, fill a
table iteratively.

**Why does DP matter?** Naive recursive solutions to optimization
problems are often exponential. DP cuts them to polynomial.

**A canonical example: Fibonacci.** The naive recursion is O(2^n);
memoized, it's O(n). Same algorithm, dramatically different runtime.

**Steps to design a DP solution:**
1. Identify the *state* — the parameters that uniquely describe a
   subproblem.
2. Write the *recurrence* — express f(state) in terms of smaller states.
3. Identify *base cases*.
4. Memoize or tabulate.
5. (Optional) Optimize space — most 1-D DPs only need O(1) extra; many
   2-D DPs can be reduced to O(min dimension).
''',
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Master the framework: state → recurrence → base case → memoization. Tabulation is an optimization once the recurrence is clear.",
        "optimized": {
            "explanation": "Memoized Fibonacci as a sanity check.",
            "code": r'''
from functools import lru_cache
@lru_cache(maxsize=None)
def fib(n):
    if n < 2: return n
    return fib(n - 1) + fib(n - 2)
''',
            "complexity": "Time O(n), space O(n).",
        },
        "deep_concept": r'''
Every DP can be viewed as a shortest/longest path on a DAG where
vertices are subproblems and edges encode the recurrence. Bottom-up
tabulation is just topological order on this DAG.
''',
        "confusion_notes": [
            {
                "question": "When should I use memoization vs tabulation?",
                "answer": "Memoization is easier to write (mirrors the natural recursion). Tabulation usually has lower constant factors and allows space optimization. Both have the same asymptotic complexity. Start with memoization, convert to tabulation if performance matters.",
            },
            {
                "question": "How do I recognize a DP problem?",
                "answer": "Three signals: (1) the problem asks for a *count*, *minimum*, *maximum*, or *yes/no*; (2) the natural recursion has overlapping subproblems; (3) decisions are made step-by-step with each step's options depending only on a finite state.",
            },
        ],
        "summary": "DP = recursion + memoization. State + recurrence + base case. Memoize first, tabulate when needed for performance.",
    },

    # ==================================================================
    # 1D DP
    # ==================================================================
    {
        "id": "frog-jump",
        "title": "Frog Jump (1 or 2 steps)",
        "step_id": 16,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["dp", "1d-dp"],
        "what_this_teaches": "Minimum-cost path on a 1-D state space.",
        "pattern": "1-D DP with two transitions.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["climbing-stairs"],
        "next_problems": ["frog-jump-k"],
        "resources": [
            {"label": "Striver — Frog Jump", "url": "https://takeuforward.org/data-structure/dynamic-programming-frog-jump-dp-3/"},
            _SHEET,
        ],
        "understanding": "A frog is on stair 0 and wants to reach stair n-1. From stair i it can jump to i+1 or i+2. Each jump costs `|height[i] - height[dest]|`. Minimize total cost.",
        "brute_force": {
            "explanation": "Recurse from stair 0, try both jumps, take min.",
            "code": r'''
def frog_jump_brute(heights):
    n = len(heights)
    def go(i):
        if i == n - 1: return 0
        cost1 = abs(heights[i] - heights[i+1]) + go(i+1)
        cost2 = abs(heights[i] - heights[i+2]) + go(i+2) if i+2 < n else float('inf')
        return min(cost1, cost2)
    return go(0)
''',
            "complexity": "Time O(2^n).",
        },
        "thought_process": "State = current stair. Transitions: jump 1 or jump 2. Memoize → O(n). Tabulate → O(n) time, O(1) space.",
        "optimized": {
            "explanation": "Tabulation with O(1) space.",
            "code": r'''
def frog_jump(heights):
    n = len(heights)
    if n == 1: return 0
    prev2, prev1 = 0, abs(heights[1] - heights[0])
    for i in range(2, n):
        cur = min(
            prev1 + abs(heights[i] - heights[i-1]),
            prev2 + abs(heights[i] - heights[i-2])
        )
        prev2, prev1 = prev1, cur
    return prev1
''',
            "complexity": "Time O(n), space O(1).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "1-D DP with two transitions; rolling-pair O(1) space.",
    },
    {
        "id": "frog-jump-k",
        "title": "Frog Jump with K Steps",
        "step_id": 16,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["dp", "1d-dp"],
        "what_this_teaches": "Generalizes to K transitions per state.",
        "pattern": "1-D DP with K transitions.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["frog-jump"],
        "next_problems": ["house-robber-i"],
        "resources": [
            {"label": "Striver — Frog Jump K", "url": "https://takeuforward.org/data-structure/dynamic-programming-frog-jump-with-k-distance-dp-4/"},
            _SHEET,
        ],
        "understanding": "From stair i, the frog can jump to any of i+1, ..., i+k. Minimize total cost.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Same template, just iterate K transitions per state.",
        "optimized": {
            "explanation": "Tabulation O(n·k).",
            "code": r'''
def frog_jump_k(heights, k):
    n = len(heights)
    dp = [float('inf')] * n
    dp[0] = 0
    for i in range(1, n):
        for j in range(1, k+1):
            if i - j >= 0:
                dp[i] = min(dp[i], dp[i-j] + abs(heights[i] - heights[i-j]))
    return dp[-1]
''',
            "complexity": "Time O(n·k), space O(n).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "1-D DP with up to K transitions per state.",
    },
    {
        "id": "house-robber-i",
        "title": "House Robber",
        "step_id": 16,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["dp", "1d-dp"],
        "what_this_teaches": "Pick-or-skip 1-D DP. Adjacent picks not allowed.",
        "pattern": "Two-choice 1-D DP.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["frog-jump"],
        "next_problems": ["house-robber-ii"],
        "resources": [
            _lc(198, "house-robber"),
            _SHEET,
        ],
        "understanding": "Houses in a row each contain some money. You cannot rob two adjacent houses. Maximize total stolen.",
        "brute_force": {"explanation": "Recurse: rob current (skip next) or skip current. Exponential.", "code": "", "complexity": "—"},
        "thought_process": "State = current house. dp[i] = max(dp[i-1], dp[i-2] + nums[i]).",
        "optimized": {
            "explanation": "Rolling-pair O(1).",
            "code": r'''
def rob(nums):
    prev2, prev1 = 0, 0
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1
''',
            "complexity": "Time O(n), space O(1).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Pick-or-skip; rolling two-variable O(1) DP.",
    },
    {
        "id": "house-robber-ii",
        "title": "House Robber II (Circular)",
        "step_id": 16,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["dp", "1d-dp"],
        "what_this_teaches": "Reduce circular to linear by trying two cases.",
        "pattern": "Two linear-DP runs.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["house-robber-i"],
        "next_problems": ["ninjas-training"],
        "resources": [
            _lc(213, "house-robber-ii"),
            _SHEET,
        ],
        "understanding": "Houses arranged in a circle (first and last are adjacent). Otherwise same as House Robber I.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Run House Robber I twice: once excluding first, once excluding last. Take the max.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def rob_ii(nums):
    if len(nums) == 1: return nums[0]
    def rob_lin(arr):
        p2 = p1 = 0
        for x in arr:
            p2, p1 = p1, max(p1, p2 + x)
        return p1
    return max(rob_lin(nums[:-1]), rob_lin(nums[1:]))
''',
            "complexity": "Time O(n), space O(1).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Run House Robber I twice (exclude first or last); take max.",
    },

    # ==================================================================
    # 2D/3D DP on Grids
    # ==================================================================
    {
        "id": "ninjas-training",
        "title": "Ninja's Training",
        "step_id": 16,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["dp", "2d-dp"],
        "what_this_teaches": "DP with a 'last activity' state to enforce 'not same as previous'.",
        "pattern": "2-D DP with categorical state.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["house-robber-i"],
        "next_problems": ["grid-unique-paths"],
        "resources": [
            {"label": "Striver — Ninja's Training", "url": "https://takeuforward.org/data-structure/dynamic-programming-ninjas-training-dp-7/"},
            _SHEET,
        ],
        "understanding": "Each day choose one of 3 activities (each with a merit). Cannot pick the same activity on consecutive days. Maximize total merit.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "State = (day, last_activity). Recurrence: dp[d][last] = max over a ≠ last of points[d][a] + dp[d+1][a].",
        "optimized": {
            "explanation": "Tabulation.",
            "code": r'''
def ninja_training(points):
    n = len(points)
    dp = [0, 0, 0, 0]  # dp[last] where last=3 means 'no previous'
    # walk from last day backward
    for d in range(n - 1, -1, -1):
        new = [0] * 4
        for last in range(4):
            new[last] = 0
            for a in range(3):
                if a != last:
                    new[last] = max(new[last], points[d][a] + dp[a])
        dp = new
    return dp[3]
''',
            "complexity": "Time O(n·12), space O(1).",
        },
        "deep_concept": "Adding 'last choice' as a dimension is a recurring trick for 'no two consecutive same' problems.",
        "confusion_notes": [],
        "summary": "DP with (day, last activity); fold across days.",
    },
    {
        "id": "grid-unique-paths",
        "title": "Unique Paths in a Grid",
        "step_id": 16,
        "lecture_id": 3,
        "difficulty": "easy",
        "tags": ["dp", "grid"],
        "what_this_teaches": "Classic m × n grid DP. paths[i][j] = paths[i-1][j] + paths[i][j-1].",
        "pattern": "2-D grid DP.",
        "prerequisite_lessons": [],
        "prerequisite_problems": [],
        "next_problems": ["grid-unique-paths-ii", "min-path-sum-grid"],
        "resources": [
            _lc(62, "unique-paths"),
            _SHEET,
        ],
        "understanding": "Count paths from top-left to bottom-right of an m × n grid; only right and down moves allowed.",
        "brute_force": {"explanation": "Recurse → O(2^(m+n)).", "code": "", "complexity": "—"},
        "thought_process": "DP: paths(i,j) = paths(i-1,j) + paths(i,j-1). Or combinatorics: C(m+n-2, m-1).",
        "optimized": {
            "explanation": "1-D DP.",
            "code": r'''
def unique_paths(m, n):
    dp = [1] * n
    for _ in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j-1]
    return dp[-1]
''',
            "complexity": "Time O(m·n), space O(n).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "dp[j] += dp[j-1] across rows; O(n) space.",
    },
    {
        "id": "grid-unique-paths-ii",
        "title": "Unique Paths II (With Obstacles)",
        "step_id": 16,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["dp", "grid"],
        "what_this_teaches": "Same DP with obstacle cells set to 0.",
        "pattern": "2-D grid DP with constraints.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["grid-unique-paths"],
        "next_problems": ["min-path-sum-grid"],
        "resources": [
            _lc(63, "unique-paths-ii"),
            _SHEET,
        ],
        "understanding": "Same as Unique Paths, but some cells are blocked (1 in obstacleGrid).",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Walk DP; set dp = 0 if cell is blocked.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def unique_paths_with_obstacles(grid):
    m, n = len(grid), len(grid[0])
    if grid[0][0]: return 0
    dp = [0]*n
    dp[0] = 1
    for i in range(m):
        for j in range(n):
            if grid[i][j]:
                dp[j] = 0
            elif j > 0:
                dp[j] += dp[j-1]
    return dp[-1]
''',
            "complexity": "Time O(m·n), space O(n).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Standard unique-paths DP with obstacles zeroed out.",
    },
    {
        "id": "min-path-sum-grid",
        "title": "Minimum Path Sum",
        "step_id": 16,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["dp", "grid"],
        "what_this_teaches": "Same grid DP but minimizing path sum.",
        "pattern": "2-D grid DP.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["grid-unique-paths"],
        "next_problems": ["min-path-sum-triangle"],
        "resources": [
            _lc(64, "minimum-path-sum"),
            _SHEET,
        ],
        "understanding": "Find a path top-left → bottom-right with minimum sum, right/down only.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1]).",
        "optimized": {
            "explanation": "In-place 1-D DP.",
            "code": r'''
def min_path_sum(grid):
    m, n = len(grid), len(grid[0])
    dp = [0] * n
    dp[0] = grid[0][0]
    for j in range(1, n):
        dp[j] = dp[j-1] + grid[0][j]
    for i in range(1, m):
        dp[0] += grid[i][0]
        for j in range(1, n):
            dp[j] = grid[i][j] + min(dp[j], dp[j-1])
    return dp[-1]
''',
            "complexity": "Time O(m·n), space O(n).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Grid DP min; O(n) space rolling.",
    },
    {
        "id": "min-path-sum-triangle",
        "title": "Triangle Minimum Path Sum",
        "step_id": 16,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["dp", "triangle"],
        "what_this_teaches": "Bottom-up DP on a triangle.",
        "pattern": "Bottom-up triangle DP.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["min-path-sum-grid"],
        "next_problems": ["min-max-falling-path"],
        "resources": [
            _lc(120, "triangle"),
            _SHEET,
        ],
        "understanding": "Given a triangle (list of lists), find the minimum path sum from top to bottom; each step you may move to one of two adjacent cells in the row below.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Start from the bottom row and fold upward.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def minimum_total(triangle):
    dp = triangle[-1][:]
    for row in range(len(triangle) - 2, -1, -1):
        for col in range(row + 1):
            dp[col] = triangle[row][col] + min(dp[col], dp[col+1])
    return dp[0]
''',
            "complexity": "Time O(n²), space O(n).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Bottom-up fold; O(n) space.",
    },
    {
        "id": "min-max-falling-path",
        "title": "Min/Max Falling Path Sum",
        "step_id": 16,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["dp", "grid"],
        "what_this_teaches": "3-direction grid DP (down-left, down, down-right).",
        "pattern": "Grid DP with 3 transitions per cell.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["min-path-sum-triangle"],
        "next_problems": ["chocolate-pickup"],
        "resources": [
            _lc(931, "minimum-falling-path-sum"),
            _SHEET,
        ],
        "understanding": "Given an n × n matrix, find a path from any cell in the top row to any in the bottom row minimizing sum. From (i, j) you can step to (i+1, j-1), (i+1, j), (i+1, j+1).",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Fold from bottom up; dp[j] = matrix[i][j] + min of 3 below.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def min_falling_path_sum(mat):
    n = len(mat)
    dp = mat[-1][:]
    for i in range(n - 2, -1, -1):
        new = dp[:]
        for j in range(n):
            best = dp[j]
            if j > 0:   best = min(best, dp[j-1])
            if j < n-1: best = min(best, dp[j+1])
            new[j] = mat[i][j] + best
        dp = new
    return min(dp)
''',
            "complexity": "Time O(n²), space O(n).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Grid DP with 3 transitions; fold bottom up.",
    },
    {
        "id": "chocolate-pickup",
        "title": "Chocolate Pickup (Two-Robot Grid DP)",
        "step_id": 16,
        "lecture_id": 3,
        "difficulty": "hard",
        "tags": ["dp", "3d-dp", "grid"],
        "what_this_teaches": "DP on two simultaneous walkers — state is (row, col1, col2).",
        "pattern": "3-D DP with synchronized walks.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["min-max-falling-path"],
        "next_problems": ["subset-sum-target"],
        "resources": [
            _lc(741, "cherry-pickup"),
            _SHEET,
        ],
        "understanding": "Two robots start at (0, 0) and (0, m-1), both walk to row n-1. At each step they go down-left, down, or down-right. They collect chocolates; if they land on the same cell, count only once. Maximize total.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "State: (row, col1, col2). Both robots advance one row at a time. 3 × 3 = 9 transitions per state.",
        "optimized": {
            "explanation": "Memoized recursion.",
            "code": r'''
from functools import lru_cache
def cherry_pickup(grid):
    n, m = len(grid), len(grid[0])
    @lru_cache(maxsize=None)
    def go(r, c1, c2):
        if r == n:
            return 0
        if not (0 <= c1 < m and 0 <= c2 < m):
            return float('-inf')
        gain = grid[r][c1] + (grid[r][c2] if c1 != c2 else 0)
        best = float('-inf')
        for d1 in (-1, 0, 1):
            for d2 in (-1, 0, 1):
                best = max(best, go(r + 1, c1 + d1, c2 + d2))
        return gain + best
    return max(0, go(0, 0, m - 1))
''',
            "complexity": "Time O(n·m²·9), space O(n·m²).",
        },
        "deep_concept": "Synchronized walkers + 'collect once if same cell' is a recurring pattern; LeetCode 741 (Cherry Pickup) is the canonical example.",
        "confusion_notes": [],
        "summary": "3-D DP: (row, col1, col2). 9 transitions per state.",
    },

    # ==================================================================
    # DP on Subsequences (knapsack family)
    # ==================================================================
    {
        "id": "subset-sum-target",
        "title": "Subset Sum to a Target",
        "step_id": 16,
        "lecture_id": 4,
        "difficulty": "medium",
        "tags": ["dp", "subset", "knapsack"],
        "what_this_teaches": "Take-or-skip DP. dp[i][s] = is there a subset of nums[0..i-1] summing to s?",
        "pattern": "0/1 knapsack template.",
        "prerequisite_lessons": [],
        "prerequisite_problems": [],
        "next_problems": ["partition-equal-subset-sum", "count-subsets-sum-k", "knapsack-01"],
        "resources": [
            {"label": "Striver — Subset Sum", "url": "https://takeuforward.org/data-structure/subset-sum-equal-to-target-dp-14/"},
            _SHEET,
        ],
        "understanding": "Given an array of positives and a target, decide if any subset sums to target.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "dp[i][s] = dp[i-1][s] OR dp[i-1][s - nums[i]]. Roll dimension i to save space.",
        "optimized": {
            "explanation": "1-D bitset-style DP.",
            "code": r'''
def subset_sum_to_k(nums, k):
    dp = [False] * (k + 1)
    dp[0] = True
    for x in nums:
        for s in range(k, x - 1, -1):     # iterate down to avoid reuse
            dp[s] = dp[s] or dp[s - x]
    return dp[k]
''',
            "complexity": "Time O(n·k), space O(k).",
        },
        "deep_concept": "The iterate-down trick prevents counting an item twice (0/1 vs unbounded).",
        "confusion_notes": [],
        "summary": "0/1 knapsack template. Iterate down to avoid reuse.",
    },
    {
        "id": "partition-equal-subset-sum",
        "title": "Partition Equal Subset Sum",
        "step_id": 16,
        "lecture_id": 4,
        "difficulty": "medium",
        "tags": ["dp", "subset"],
        "what_this_teaches": "Reduces to subset sum with target = total / 2.",
        "pattern": "Subset sum.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["subset-sum-target"],
        "next_problems": ["partition-min-diff"],
        "resources": [
            _lc(416, "partition-equal-subset-sum"),
            _SHEET,
        ],
        "understanding": "Decide if a positive integer array can be split into two subsets of equal sum.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "If total is odd, return False. Else check if any subset sums to total // 2.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def can_partition(nums):
    s = sum(nums)
    if s % 2: return False
    target = s // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for x in nums:
        for t in range(target, x - 1, -1):
            dp[t] = dp[t] or dp[t - x]
    return dp[target]
''',
            "complexity": "Time O(n·S/2), space O(S/2).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Subset sum with target = total / 2.",
    },
    {
        "id": "partition-min-diff",
        "title": "Partition Array Minimum Difference",
        "step_id": 16,
        "lecture_id": 4,
        "difficulty": "medium",
        "tags": ["dp", "subset"],
        "what_this_teaches": "Knapsack to determine reachable subset sums; min difference = min |S - 2·sub|.",
        "pattern": "Knapsack + min computation.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["partition-equal-subset-sum"],
        "next_problems": ["count-subsets-sum-k"],
        "resources": [
            {"label": "Striver — Min Subset Diff", "url": "https://takeuforward.org/data-structure/partition-set-into-2-subsets-with-min-absolute-sum-difference-dp-16/"},
            _SHEET,
        ],
        "understanding": "Partition into two subsets minimizing |sum(A) - sum(B)|.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Enumerate which subset sums are achievable. For each achievable s ≤ S/2, |S - 2s| is a candidate.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def min_subset_diff(nums):
    S = sum(nums)
    dp = [False] * (S + 1)
    dp[0] = True
    for x in nums:
        for t in range(S, x - 1, -1):
            dp[t] = dp[t] or dp[t - x]
    best = float('inf')
    for s in range(S // 2 + 1):
        if dp[s]:
            best = min(best, S - 2 * s)
    return best
''',
            "complexity": "Time O(n·S), space O(S).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Compute reachable sums; min diff = min |S - 2s|.",
    },
    {
        "id": "count-subsets-sum-k",
        "title": "Count Subsets with Sum K",
        "step_id": 16,
        "lecture_id": 4,
        "difficulty": "medium",
        "tags": ["dp", "subset", "counting"],
        "what_this_teaches": "Switch from 'exists' to 'count' by changing OR → addition.",
        "pattern": "Subset sum counting.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["subset-sum-target"],
        "next_problems": ["count-partitions-given-diff", "target-sum"],
        "resources": [
            {"label": "Striver — Count Subsets with Sum K", "url": "https://takeuforward.org/data-structure/count-subsets-with-sum-k-dp-17/"},
            _SHEET,
        ],
        "understanding": "Count subsets summing to exactly K.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "dp[s] = number of subsets summing to s. Add nums[i] to all reachable s.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def count_subsets_sum_k(nums, k):
    dp = [0] * (k + 1)
    dp[0] = 1
    for x in nums:
        for s in range(k, x - 1, -1):
            dp[s] += dp[s - x]
    return dp[k]
''',
            "complexity": "Time O(n·k), space O(k).",
        },
        "deep_concept": "—",
        "confusion_notes": [
            {
                "question": "Handle zeros in the array?",
                "answer": "Zeros are tricky — each zero doubles the count (it can be included or not without changing the sum). Some implementations explicitly multiply by 2^(zero_count). Standard problems assume positives.",
            },
        ],
        "summary": "Subset-sum DP with += instead of OR.",
    },
    {
        "id": "count-partitions-given-diff",
        "title": "Count Partitions with Given Difference",
        "step_id": 16,
        "lecture_id": 4,
        "difficulty": "medium",
        "tags": ["dp", "subset"],
        "what_this_teaches": "Reduces to count-subsets-sum-k via algebra.",
        "pattern": "Algebraic reduction.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["count-subsets-sum-k"],
        "next_problems": ["target-sum"],
        "resources": [_SHEET],
        "understanding": "Count ways to partition into two subsets S1, S2 such that S1 − S2 = D and S1 ≥ S2.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Let T = sum. S1 - S2 = D and S1 + S2 = T, so S2 = (T - D) / 2. Count subsets summing to S2.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def count_partitions(nums, d):
    s = sum(nums)
    if (s - d) % 2 or s < d:
        return 0
    target = (s - d) // 2
    dp = [0] * (target + 1)
    dp[0] = 1
    for x in nums:
        for t in range(target, x - 1, -1):
            dp[t] += dp[t - x]
    return dp[target]
''',
            "complexity": "Time O(n·S), space O(S).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Reduce to count-subsets-sum-k with k = (T - D) / 2.",
    },
    {
        "id": "knapsack-01",
        "title": "0/1 Knapsack",
        "step_id": 16,
        "lecture_id": 4,
        "difficulty": "medium",
        "tags": ["dp", "knapsack"],
        "what_this_teaches": "Classic 0/1 knapsack: maximize value subject to weight capacity.",
        "pattern": "0/1 knapsack.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["subset-sum-target"],
        "next_problems": ["unbounded-knapsack"],
        "resources": [
            {"label": "GFG — 0/1 Knapsack", "url": "https://www.geeksforgeeks.org/0-1-knapsack-problem-dp-10/"},
            _SHEET,
        ],
        "understanding": "Given values, weights, and capacity W, maximize total value.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "dp[w] = max value at capacity w. Iterate items; iterate w from W down to weight[i].",
        "optimized": {
            "explanation": "—",
            "code": r'''
def knapsack01(values, weights, W):
    dp = [0] * (W + 1)
    for v, w in zip(values, weights):
        for cap in range(W, w - 1, -1):
            dp[cap] = max(dp[cap], dp[cap - w] + v)
    return dp[W]
''',
            "walkthrough": r'''
The 0/1 Knapsack DP, space-optimized to one dimension. *O(n·W)*
time, *O(W)* memory. Each item can be taken at most once
(hence "0/1": include or exclude).

**`def knapsack01(values, weights, W):`** — Takes lists of
item values and weights (same length), plus the knapsack
capacity `W`. Returns the maximum total value achievable.

**`dp = [0] * (W + 1)`** — 1D DP array. `dp[c]` will hold the
best total value achievable with capacity `c`, considering
the items we've processed so far.

We allocate size `W + 1` because we want indices `0` to `W`
inclusive. `dp[0]` represents capacity-zero (nothing can fit);
`dp[W]` represents the full capacity (our final answer).

All entries start at 0 because with zero items processed,
the max value is 0 regardless of capacity.

**`for v, w in zip(values, weights):`** — Process one item at
a time. `v` is its value, `w` is its weight.

**`for cap in range(W, w - 1, -1):`** — **Iterate capacity
DOWNWARD** from `W` to `w` (inclusive on both ends — the `w
- 1` is exclusive in `range`).

**Why downward?** This is the **most subtle line** in 0/1
knapsack. Iterating in reverse ensures that when we use
`dp[cap - w]`, that value comes from the **previous item's**
DP — not the current item's.

If we iterated upward (`for cap in range(w, W + 1)`), then
when computing `dp[cap]` we'd use a `dp[cap - w]` that was
**already updated in this iteration** — meaning we'd be
including the current item twice. That's **unbounded
knapsack**, not 0/1.

The downward iteration writes to higher indices first, so
lower indices remain at their previous-item values when read.

**`dp[cap] = max(dp[cap], dp[cap - w] + v)`** — The choice:
- Don't take this item: `dp[cap]` stays the same (the
  "previous-item" value).
- Take this item: gain value `v`, use weight `w`. The best we
  could do with the remaining `cap - w` capacity (using
  previous items) is `dp[cap - w]`. Add `v`.

Take the better of the two.

**`return dp[W]`** — After processing all items, `dp[W]` is
the optimal answer for the full capacity.

**Trace on values=[60, 100, 120], weights=[10, 20, 30], W=50:**
```
Init: dp = [0]*51.

Item 1: (v=60, w=10).
  Iterate cap from 50 down to 10:
    cap=50: dp[50] = max(0, dp[40]+60) = 60.
    cap=49: dp[49] = max(0, dp[39]+60) = 60.
    ...
    cap=10: dp[10] = max(0, dp[0]+60) = 60.
  After item 1: dp[0..9]=0, dp[10..50]=60.

Item 2: (v=100, w=20).
  Iterate cap from 50 down to 20:
    cap=50: dp[50] = max(60, dp[30]+100) = max(60, 60+100) = 160.
    cap=49: dp[49] = max(60, dp[29]+100) = max(60, 60+100) = 160.
    ...
    cap=30: dp[30] = max(60, dp[10]+100) = max(60, 60+100) = 160.
    cap=29: dp[29] = max(60, dp[9]+100) = max(60, 0+100) = 100.
    ...
    cap=20: dp[20] = max(60, dp[0]+100) = 100.
  After item 2: various values.

Item 3: (v=120, w=30).
  cap=50: dp[50] = max(160, dp[20]+120) = max(160, 100+120) = 220.
  ...
  cap=30: dp[30] = max(160, dp[0]+120) = max(160, 120) = 160.
  ...

Final: dp[50] = 220. Optimal!
(Take items 1 and 2: weight 30, value 160. Or items 2 and 3:
 weight 50, value 220. Yes — 220 is the answer.)
```

**Why is this optimal?**

The DP encodes the decision tree of "for each item, take or
skip." The number of states is `n × (W + 1)`. Each transition
is *O(1)*. Total time *O(n·W)*.

The 1D space optimization works because we only ever read
`dp[cap]` and `dp[cap - w]` — both from the **previous
item's** DP. The downward iteration preserves those values.

**Properties:**
- **Time**: *O(n·W)* — pseudo-polynomial. Fast when W is
  small (which it usually is in practice).
- **Space**: *O(W)*.

**Why "pseudo-polynomial"?**

Because the complexity depends on the **value** of W, not its
**bit-length**. For W = 10⁹, the algorithm is impractical
even though `n` is small. For NP-hardness purposes, 0/1
knapsack is hard.

**Variations**:
- **Unbounded knapsack** (item reusable): iterate cap upward.
- **Bounded knapsack** (each item has a count limit): more
  complex.
- **Fractional knapsack**: O(n log n) greedy, not DP.
- **Subset sum**: knapsack with weights = values.

Knapsack DP is the prototypical "include or exclude" problem.
Master this template and many subset/partition problems
become straightforward.
''',
            "complexity": "Time O(n·W), space O(W).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "1-D DP iterating cap downward; standard 0/1 knapsack.",
    },
    {
        "id": "min-coins",
        "title": "Minimum Coins (Coin Change)",
        "step_id": 16,
        "lecture_id": 4,
        "difficulty": "medium",
        "tags": ["dp", "knapsack"],
        "what_this_teaches": "Unbounded knapsack minimizing count.",
        "pattern": "Unbounded knapsack min.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["knapsack-01"],
        "next_problems": ["coin-change-2"],
        "resources": [
            _lc(322, "coin-change"),
            _SHEET,
        ],
        "understanding": "Minimum coins to make amount; coins can be reused.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "dp[a] = min coins for amount a. dp[a] = min(dp[a - c] + 1) for each coin c.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def coin_change(coins, amount):
    INF = amount + 1
    dp = [INF] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] != INF else -1
''',
            "complexity": "Time O(amount · |coins|).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Unbounded knapsack min; iterate amount up.",
    },
    {
        "id": "target-sum",
        "title": "Target Sum (Assign + / -)",
        "step_id": 16,
        "lecture_id": 4,
        "difficulty": "medium",
        "tags": ["dp", "subset"],
        "what_this_teaches": "Reduces to count-partitions-given-diff.",
        "pattern": "Algebraic reduction.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["count-partitions-given-diff"],
        "next_problems": [],
        "resources": [
            _lc(494, "target-sum"),
            _SHEET,
        ],
        "understanding": "Assign + or - to each element so total sum = target. Count ways.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Split into P (positives) and N (negatives). P - N = target, P + N = sum. So P = (sum + target) / 2. Count subsets summing to P.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def find_target_sum_ways(nums, target):
    s = sum(nums)
    if abs(target) > s or (s + target) % 2:
        return 0
    p = (s + target) // 2
    dp = [0] * (p + 1)
    dp[0] = 1
    for x in nums:
        for t in range(p, x - 1, -1):
            dp[t] += dp[t - x]
    return dp[p]
''',
            "complexity": "Time O(n·S).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Reduces to count-subsets-sum-k via algebra.",
    },
    {
        "id": "coin-change-2",
        "title": "Coin Change II (Count Ways)",
        "step_id": 16,
        "lecture_id": 4,
        "difficulty": "medium",
        "tags": ["dp", "knapsack", "counting"],
        "what_this_teaches": "Unbounded knapsack counting.",
        "pattern": "Unbounded knapsack count.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["min-coins"],
        "next_problems": ["unbounded-knapsack"],
        "resources": [
            _lc(518, "coin-change-2"),
            _SHEET,
        ],
        "understanding": "Count number of ways to make amount with given coins (each may be used unlimited times).",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Iterate coins as the outer loop (to avoid counting different orderings as distinct).",
        "optimized": {
            "explanation": "—",
            "code": r'''
def change(amount, coins):
    dp = [0] * (amount + 1)
    dp[0] = 1
    for c in coins:
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]
    return dp[amount]
''',
            "complexity": "Time O(amount · |coins|).",
        },
        "deep_concept": "Coin loop outer = combinations; amount loop outer = permutations. Different problems!",
        "confusion_notes": [],
        "summary": "Coin loop outer to count combinations.",
    },
    {
        "id": "unbounded-knapsack",
        "title": "Unbounded Knapsack",
        "step_id": 16,
        "lecture_id": 4,
        "difficulty": "medium",
        "tags": ["dp", "knapsack"],
        "what_this_teaches": "Like 0/1 knapsack but each item can be used unlimited times.",
        "pattern": "Unbounded knapsack max.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["knapsack-01"],
        "next_problems": ["rod-cutting"],
        "resources": [
            {"label": "GFG — Unbounded Knapsack", "url": "https://www.geeksforgeeks.org/unbounded-knapsack-repetition-items-allowed/"},
            _SHEET,
        ],
        "understanding": "Maximize value with unlimited copies per item.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Iterate cap from low to high (allow reuse).",
        "optimized": {
            "explanation": "—",
            "code": r'''
def unbounded_knapsack(values, weights, W):
    dp = [0] * (W + 1)
    for v, w in zip(values, weights):
        for cap in range(w, W + 1):
            dp[cap] = max(dp[cap], dp[cap - w] + v)
    return dp[W]
''',
            "complexity": "Time O(n·W).",
        },
        "deep_concept": "Iterate cap ascending = reuse allowed (item can be re-counted in the same iteration); descending = 0/1.",
        "confusion_notes": [],
        "summary": "Iterate cap ascending for unbounded.",
    },
    {
        "id": "rod-cutting",
        "title": "Rod Cutting",
        "step_id": 16,
        "lecture_id": 4,
        "difficulty": "medium",
        "tags": ["dp", "knapsack"],
        "what_this_teaches": "Unbounded knapsack with 'weights = lengths 1..n'.",
        "pattern": "Unbounded knapsack.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["unbounded-knapsack"],
        "next_problems": [],
        "resources": [
            {"label": "GFG — Rod Cutting", "url": "https://www.geeksforgeeks.org/cutting-a-rod-dp-13/"},
            _SHEET,
        ],
        "understanding": "Cut a rod of length n into pieces; piece of length i is worth price[i]. Maximize revenue.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Unbounded knapsack with weight i and value price[i].",
        "optimized": {
            "explanation": "—",
            "code": r'''
def rod_cutting(prices, n):
    dp = [0] * (n + 1)
    for L in range(1, n + 1):
        for i in range(1, L + 1):
            dp[L] = max(dp[L], prices[i - 1] + dp[L - i])
    return dp[n]
''',
            "complexity": "Time O(n²).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Unbounded knapsack with lengths 1..n.",
    },

    # ==================================================================
    # DP on Strings
    # ==================================================================
    {
        "id": "print-lcs",
        "title": "Print Longest Common Subsequence",
        "step_id": 16,
        "lecture_id": 5,
        "difficulty": "medium",
        "tags": ["dp", "strings", "lcs"],
        "what_this_teaches": "After building the LCS table, reconstruct the subsequence by walking back through the choices.",
        "pattern": "DP traceback.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["lcs"],
        "next_problems": ["longest-common-substring", "edit-distance"],
        "resources": [
            {"label": "Striver — Print LCS", "url": "https://takeuforward.org/data-structure/print-longest-common-subsequence-dp-26/"},
            _SHEET,
        ],
        "understanding": "Same as LCS but return the actual subsequence string.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Build the 2-D DP, then walk back from (n, m): if chars match, prepend and go diagonal; else go to the larger of (i-1, j) or (i, j-1).",
        "optimized": {
            "explanation": "DP + traceback.",
            "code": r'''
def print_lcs(s1, s2):
    n, m = len(s1), len(s2)
    dp = [[0]*(m+1) for _ in range(n+1)]
    for i in range(1, n+1):
        for j in range(1, m+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    # traceback
    res = []
    i, j = n, m
    while i > 0 and j > 0:
        if s1[i-1] == s2[j-1]:
            res.append(s1[i-1])
            i -= 1; j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    return ''.join(reversed(res))
''',
            "complexity": "Time O(n·m), space O(n·m).",
        },
        "deep_concept": "DP traceback is the standard way to recover an *optimal sequence*, not just its score.",
        "confusion_notes": [],
        "summary": "Build LCS DP; trace back from (n, m) emitting matched chars.",
    },
    {
        "id": "longest-common-substring",
        "title": "Longest Common Substring",
        "step_id": 16,
        "lecture_id": 5,
        "difficulty": "medium",
        "tags": ["dp", "strings"],
        "what_this_teaches": "Substring (contiguous!) DP; reset to 0 on mismatch.",
        "pattern": "2-D DP with reset on mismatch.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["lcs"],
        "next_problems": ["longest-palindromic-subseq"],
        "resources": [
            {"label": "GFG — Longest Common Substring", "url": "https://www.geeksforgeeks.org/longest-common-substring-dp-29/"},
            _SHEET,
        ],
        "understanding": "Longest *contiguous* substring common to two strings.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "dp[i][j] = length of LCS ending at i, j. If match, dp[i-1][j-1] + 1; else 0.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def longest_common_substring(s1, s2):
    n, m = len(s1), len(s2)
    prev = [0]*(m+1)
    best = 0
    for i in range(1, n+1):
        cur = [0]*(m+1)
        for j in range(1, m+1):
            if s1[i-1] == s2[j-1]:
                cur[j] = prev[j-1] + 1
                best = max(best, cur[j])
        prev = cur
    return best
''',
            "complexity": "Time O(n·m), space O(m).",
        },
        "deep_concept": "Substring vs subsequence: substring DP resets on mismatch, subsequence DP carries the max.",
        "confusion_notes": [],
        "summary": "DP with mismatch → 0; track global max.",
    },
    {
        "id": "longest-palindromic-subseq",
        "title": "Longest Palindromic Subsequence",
        "step_id": 16,
        "lecture_id": 5,
        "difficulty": "medium",
        "tags": ["dp", "strings", "lcs"],
        "what_this_teaches": "Reduces to LCS(s, reverse(s)).",
        "pattern": "LCS reduction.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["lcs"],
        "next_problems": ["min-insertions-palindrome"],
        "resources": [
            _lc(516, "longest-palindromic-subsequence"),
            _SHEET,
        ],
        "understanding": "Length of the longest palindrome that is a subsequence of s.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "LCS(s, reversed(s)).",
        "optimized": {
            "explanation": "—",
            "code": r'''
def longest_palindrome_subseq(s):
    t = s[::-1]
    n = len(s)
    dp = [[0]*(n+1) for _ in range(n+1)]
    for i in range(1, n+1):
        for j in range(1, n+1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[n][n]
''',
            "complexity": "Time O(n²).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "LCS with the reversed string.",
    },
    {
        "id": "min-insertions-palindrome",
        "title": "Minimum Insertions to Make a Palindrome",
        "step_id": 16,
        "lecture_id": 5,
        "difficulty": "medium",
        "tags": ["dp", "strings"],
        "what_this_teaches": "len(s) - longest palindromic subsequence.",
        "pattern": "Reduce to LPS.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["longest-palindromic-subseq"],
        "next_problems": ["min-ops-convert-a-to-b"],
        "resources": [
            _lc(1312, "minimum-insertion-steps-to-make-a-string-palindrome"),
            _SHEET,
        ],
        "understanding": "Minimum insertions to make s a palindrome.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Answer = len(s) - LPS(s).",
        "optimized": {
            "explanation": "—",
            "code": r'''
def min_insertions(s):
    return len(s) - longest_palindrome_subseq(s)   # see prev problem
''',
            "complexity": "Time O(n²).",
        },
        "deep_concept": "Symmetric leftovers: chars not in LPS each need one mirror inserted.",
        "confusion_notes": [],
        "summary": "len - LPS.",
    },
    {
        "id": "min-ops-convert-a-to-b",
        "title": "Minimum Operations to Convert String A to B (Delete + Insert)",
        "step_id": 16,
        "lecture_id": 5,
        "difficulty": "medium",
        "tags": ["dp", "strings"],
        "what_this_teaches": "Operations needed = len(A) + len(B) - 2 · LCS(A, B).",
        "pattern": "LCS reduction.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["lcs"],
        "next_problems": ["shortest-common-supersequence", "edit-distance"],
        "resources": [_SHEET],
        "understanding": "Convert A to B using only insertions and deletions; minimize ops.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "LCS(A, B) chars stay; delete len(A) - LCS and insert len(B) - LCS.",
        "optimized": {"explanation": "—", "code": "# return len(a) + len(b) - 2 * lcs(a, b)", "complexity": "Time O(n·m)."},
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Operations = |A| + |B| - 2·LCS.",
    },
    {
        "id": "shortest-common-supersequence",
        "title": "Shortest Common Supersequence",
        "step_id": 16,
        "lecture_id": 5,
        "difficulty": "hard",
        "tags": ["dp", "strings", "lcs"],
        "what_this_teaches": "SCS length = |A| + |B| - LCS(A, B). Reconstruct by merging.",
        "pattern": "LCS + traceback.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["print-lcs"],
        "next_problems": ["edit-distance"],
        "resources": [
            _lc(1092, "shortest-common-supersequence"),
            _SHEET,
        ],
        "understanding": "Shortest string containing both A and B as subsequences. Return the string itself.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Build LCS table; walk back: if chars match, take once; else take the char from the side with larger DP value, decrementing that index.",
        "optimized": {
            "explanation": "LCS + merge traceback.",
            "code": r'''
def shortest_common_supersequence(s1, s2):
    n, m = len(s1), len(s2)
    dp = [[0]*(m+1) for _ in range(n+1)]
    for i in range(1, n+1):
        for j in range(1, m+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    i, j = n, m
    res = []
    while i > 0 and j > 0:
        if s1[i-1] == s2[j-1]:
            res.append(s1[i-1]); i -= 1; j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            res.append(s1[i-1]); i -= 1
        else:
            res.append(s2[j-1]); j -= 1
    while i > 0: res.append(s1[i-1]); i -= 1
    while j > 0: res.append(s2[j-1]); j -= 1
    return ''.join(reversed(res))
''',
            "complexity": "Time O(n·m).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "LCS traceback; emit non-match chars from one side too.",
    },
    {
        "id": "distinct-subsequences",
        "title": "Distinct Subsequences",
        "step_id": 16,
        "lecture_id": 5,
        "difficulty": "hard",
        "tags": ["dp", "strings", "counting"],
        "what_this_teaches": "Counting variant: how many ways s contains t as subsequence.",
        "pattern": "Take-or-skip DP with counting.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["lcs"],
        "next_problems": ["edit-distance"],
        "resources": [
            _lc(115, "distinct-subsequences"),
            _SHEET,
        ],
        "understanding": "Count distinct ways to form t as a subsequence of s.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "dp[i][j] = ways s[0..i] contains t[0..j]. If s[i-1] == t[j-1]: dp[i][j] = dp[i-1][j-1] + dp[i-1][j]. Else dp[i][j] = dp[i-1][j].",
        "optimized": {
            "explanation": "—",
            "code": r'''
def num_distinct(s, t):
    n, m = len(s), len(t)
    dp = [[0]*(m+1) for _ in range(n+1)]
    for i in range(n+1): dp[i][0] = 1
    for i in range(1, n+1):
        for j in range(1, m+1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + dp[i-1][j]
            else:
                dp[i][j] = dp[i-1][j]
    return dp[n][m]
''',
            "complexity": "Time O(n·m).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "DP counting; match adds dp[i-1][j-1] + dp[i-1][j], mismatch carries dp[i-1][j].",
    },
    {
        "id": "edit-distance",
        "title": "Edit Distance (Levenshtein)",
        "step_id": 16,
        "lecture_id": 5,
        "difficulty": "medium",
        "tags": ["dp", "strings"],
        "what_this_teaches": "DP with insert/delete/replace transitions.",
        "pattern": "3-transition 2-D DP.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["lcs"],
        "next_problems": ["wildcard-matching"],
        "resources": [
            _lc(72, "edit-distance"),
            _SHEET,
        ],
        "understanding": "Minimum edits (insert / delete / replace) to convert word1 to word2.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "If chars match, no cost: dp[i-1][j-1]. Else: 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]).",
        "optimized": {
            "explanation": "—",
            "code": r'''
def min_distance(w1, w2):
    n, m = len(w1), len(w2)
    dp = [[0]*(m+1) for _ in range(n+1)]
    for i in range(n+1): dp[i][0] = i
    for j in range(m+1): dp[0][j] = j
    for i in range(1, n+1):
        for j in range(1, m+1):
            if w1[i-1] == w2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[n][m]
''',
            "walkthrough": r'''
**Edit distance** (Levenshtein distance) — the canonical
"three operations" 2D string DP. *O(n·m)* time and memory.

The problem: minimum number of single-character edits
(**insert**, **delete**, or **replace**) needed to convert
`w1` into `w2`.

**`def min_distance(w1, w2):`** — Takes two strings. Returns
the minimum number of edits.

**`n, m = len(w1), len(w2)`** — Cache lengths.

**`dp = [[0]*(m+1) for _ in range(n+1)]`** — 2D table of size
`(n+1) × (m+1)`. The extra row and column handle the empty-
prefix base cases. `dp[i][j]` will be the edit distance
between `w1[..i-1]` (first `i` chars of `w1`) and `w2[..j-1]`
(first `j` chars of `w2`).

**Base cases:**

**`for i in range(n+1): dp[i][0] = i`** — Converting `w1[..i-1]`
to the empty string requires **deleting all i characters**.
So `dp[i][0] = i`.

**`for j in range(m+1): dp[0][j] = j`** — Converting the
empty string to `w2[..j-1]` requires **inserting all j
characters**. So `dp[0][j] = j`.

**The double loop:**

**`for i in range(1, n+1): for j in range(1, m+1):`** — Fill
the table row-by-row, left to right. By the time we compute
`dp[i][j]`, all three dependent cells are already filled.

**`if w1[i-1] == w2[j-1]:`** — Compare the **last characters**
of the two current prefixes. (Index `i-1` because `dp[i]` is
for prefix length `i`.)

**`dp[i][j] = dp[i-1][j-1]`** — **Match case.** If the last
characters are already the same, no edit is needed for them.
The cost is whatever it takes to convert the shorter prefixes
`w1[..i-2]` and `w2[..j-2]`, which is `dp[i-1][j-1]`.

**`else:`** — Last characters differ. We need exactly **one
edit** to deal with this position. Three options:

**`dp[i-1][j]`** — **Delete** `w1[i-1]`. Now `w1` has length
`i-1`. The remaining problem is converting `w1[..i-2]` to
`w2[..j-1]`, costing `dp[i-1][j]`. Plus 1 for the delete.

**`dp[i][j-1]`** — **Insert** `w2[j-1]` into `w1`. Now both
"end" with `w2[j-1]`, which we conceptually consume. The
remaining problem is `w1[..i-1]` to `w2[..j-2]`, costing
`dp[i][j-1]`. Plus 1 for the insert.

**`dp[i-1][j-1]`** — **Replace** `w1[i-1]` with `w2[j-1]`.
Both ends now match (after the replace), so we consume both.
Remaining: `dp[i-1][j-1]`. Plus 1 for the replace.

**`dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`** —
Take the best of the three.

**`return dp[n][m]`** — Edit distance between the full
strings.

**Trace on w1 = "horse", w2 = "ros":**

```
          ""  r   o   s
   ""      0  1   2   3
   h       1  1   2   3
   o       2  2   1   2
   r       3  2   2   2
   s       4  3   3   2
   e       5  4   4   3
```

Reading: edit_distance("horse", "ros") = 3. Verify:
1. Replace 'h' with 'r': "rorse"
2. Delete 'r' (the 4th char): "rose"... hmm, let me redo:
1. Replace 'h' with 'r': "horse" → "rorse"
2. Delete 'r' (2nd r): "rorse" → "rose"? No.

Let me re-derive: the standard 3-edit transformation:
1. horse → rorse (replace h→r)
2. rorse → rose (delete r at position 2)
3. rose → ros (delete e)
Three edits. ✓

**Why does this work?**

The DP encodes the decision tree of "for each ending pair of
characters, what's the cheapest way to align them?" The
recurrence covers all possibilities:
- Match → no edit needed; both ends consumed.
- Replace → fix the mismatch with one edit; both consumed.
- Delete from `w1` → `w1` is shortened; only `w1`'s end
  consumed.
- Insert into `w1` → `w1` is lengthened to match `w2`'s end;
  only `w2`'s end consumed.

Every transformation of `w1` into `w2` is a sequence of these
operations. The DP finds the cheapest sequence.

**Properties:**
- **Time**: *O(n·m)*.
- **Space**: *O(n·m)* (can be reduced to *O(min(n, m))*
  using rolling rows).

**Applications:**
- Spell checkers (find closest dictionary word).
- DNA sequence alignment (similar problem, different scoring).
- File diff tools.
- Plagiarism detection.
- Fuzzy text matching.

Edit distance is the gateway to a huge family of "alignment"
problems in bioinformatics, NLP, and information retrieval.
''',
            "complexity": "Time O(n·m).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "3-transition DP: insert/delete/replace.",
    },
    {
        "id": "wildcard-matching",
        "title": "Wildcard Matching",
        "step_id": 16,
        "lecture_id": 5,
        "difficulty": "hard",
        "tags": ["dp", "strings"],
        "what_this_teaches": "Pattern matching with '?' (any char) and '*' (any sequence).",
        "pattern": "String DP.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["edit-distance"],
        "next_problems": ["stock-i"],
        "resources": [
            _lc(44, "wildcard-matching"),
            _SHEET,
        ],
        "understanding": "Does pattern p match string s? '?' matches one char; '*' matches zero or more chars.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": r'''
dp[i][j] = does s[0..i-1] match p[0..j-1]?
- If p[j-1] == s[i-1] or p[j-1] == '?': dp[i][j] = dp[i-1][j-1]
- If p[j-1] == '*': dp[i][j] = dp[i-1][j] (consume a char) or dp[i][j-1] (consume the star).
''',
        "optimized": {
            "explanation": "—",
            "code": r'''
def is_match_wildcard(s, p):
    n, m = len(s), len(p)
    dp = [[False]*(m+1) for _ in range(n+1)]
    dp[0][0] = True
    for j in range(1, m+1):
        if p[j-1] == '*': dp[0][j] = dp[0][j-1]
    for i in range(1, n+1):
        for j in range(1, m+1):
            if p[j-1] == s[i-1] or p[j-1] == '?':
                dp[i][j] = dp[i-1][j-1]
            elif p[j-1] == '*':
                dp[i][j] = dp[i-1][j] or dp[i][j-1]
    return dp[n][m]
''',
            "complexity": "Time O(n·m).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "DP with cases for matching char/'?' and '*'.",
    },

    # ==================================================================
    # DP on Stocks
    # ==================================================================
    {
        "id": "stock-i",
        "title": "Best Time to Buy and Sell Stock I",
        "step_id": 16,
        "lecture_id": 6,
        "difficulty": "easy",
        "tags": ["dp", "stocks"],
        "what_this_teaches": "Track running minimum + maximize profit.",
        "pattern": "Single pass.",
        "prerequisite_lessons": [],
        "prerequisite_problems": [],
        "next_problems": ["stock-ii"],
        "resources": [
            _lc(121, "best-time-to-buy-and-sell-stock"),
            _SHEET,
        ],
        "understanding": "Pick one buy day and one later sell day; maximize profit.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Track running min price; for each day, candidate profit = price - min.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def max_profit_i(prices):
    lo = float('inf'); best = 0
    for p in prices:
        lo = min(lo, p)
        best = max(best, p - lo)
    return best
''',
            "complexity": "Time O(n).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Track min so far; profit = price - min.",
    },
    {
        "id": "stock-ii",
        "title": "Best Time to Buy and Sell Stock II",
        "step_id": 16,
        "lecture_id": 6,
        "difficulty": "medium",
        "tags": ["dp", "stocks"],
        "what_this_teaches": "Unlimited transactions: sum every positive difference.",
        "pattern": "Greedy or DP with hold/cash states.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["stock-i"],
        "next_problems": ["stock-iii"],
        "resources": [
            _lc(122, "best-time-to-buy-and-sell-stock-ii"),
            _SHEET,
        ],
        "understanding": "Unlimited buy-and-sell allowed; one share at a time.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Greedy: sum all positive price[i] - price[i-1].",
        "optimized": {
            "explanation": "—",
            "code": r'''
def max_profit_ii(prices):
    return sum(max(0, prices[i] - prices[i-1]) for i in range(1, len(prices)))
''',
            "complexity": "Time O(n).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Greedy sum of positive deltas.",
    },
    {
        "id": "stock-iii",
        "title": "Best Time to Buy and Sell Stock III (At Most 2 Transactions)",
        "step_id": 16,
        "lecture_id": 6,
        "difficulty": "hard",
        "tags": ["dp", "stocks"],
        "what_this_teaches": "DP with (day, transactions_used, holding) state.",
        "pattern": "Multi-dim DP.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["stock-ii"],
        "next_problems": ["stock-iv"],
        "resources": [
            _lc(123, "best-time-to-buy-and-sell-stock-iii"),
            _SHEET,
        ],
        "understanding": "At most 2 buy-sell pairs.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "DP: (day, transactions_left, holding). Same template as Stock IV with k=2.",
        "optimized": {
            "explanation": "Stock IV with k=2.",
            "code": "# see Stock IV",
            "complexity": "Time O(n).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Stock IV with k=2.",
    },
    {
        "id": "stock-iv",
        "title": "Best Time to Buy and Sell Stock IV (At Most K Transactions)",
        "step_id": 16,
        "lecture_id": 6,
        "difficulty": "hard",
        "tags": ["dp", "stocks"],
        "what_this_teaches": "General-K version with 3-D state.",
        "pattern": "Multi-dim DP.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["stock-iii"],
        "next_problems": ["stock-cooldown"],
        "resources": [
            _lc(188, "best-time-to-buy-and-sell-stock-iv"),
            _SHEET,
        ],
        "understanding": "At most k transactions.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "dp[i][t][hold]. Fold day and tx dimensions.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def max_profit_iv(k, prices):
    n = len(prices)
    if n == 0 or k == 0: return 0
    if k >= n // 2:
        return sum(max(0, prices[i] - prices[i-1]) for i in range(1, n))
    buy = [-float('inf')] * (k + 1)
    sell = [0] * (k + 1)
    for p in prices:
        for j in range(1, k + 1):
            buy[j]  = max(buy[j], sell[j-1] - p)
            sell[j] = max(sell[j], buy[j] + p)
    return sell[k]
''',
            "complexity": "Time O(n·k).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "buy[j]/sell[j] arrays; iterate prices.",
    },
    {
        "id": "stock-cooldown",
        "title": "Stock with Cooldown",
        "step_id": 16,
        "lecture_id": 6,
        "difficulty": "medium",
        "tags": ["dp", "stocks"],
        "what_this_teaches": "DP with a cooldown state: must skip a day after selling.",
        "pattern": "State machine DP.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["stock-ii"],
        "next_problems": ["stock-fee"],
        "resources": [
            _lc(309, "best-time-to-buy-and-sell-stock-with-cooldown"),
            _SHEET,
        ],
        "understanding": "Unlimited transactions, but after selling you cannot buy the next day.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Three states: hold, sold, rest.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def max_profit_cooldown(prices):
    hold = -float('inf')
    sold = 0
    rest = 0
    for p in prices:
        prev_sold = sold
        sold = hold + p
        hold = max(hold, rest - p)
        rest = max(rest, prev_sold)
    return max(sold, rest)
''',
            "complexity": "Time O(n).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "3-state DP (hold/sold/rest).",
    },
    {
        "id": "stock-fee",
        "title": "Stock with Transaction Fee",
        "step_id": 16,
        "lecture_id": 6,
        "difficulty": "medium",
        "tags": ["dp", "stocks"],
        "what_this_teaches": "Same DP but each sale subtracts a fee.",
        "pattern": "Two-state DP.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["stock-cooldown"],
        "next_problems": [],
        "resources": [
            _lc(714, "best-time-to-buy-and-sell-stock-with-transaction-fee"),
            _SHEET,
        ],
        "understanding": "Each transaction (buy-sell pair) charges `fee`.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "hold/cash states; subtract fee on sell.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def max_profit_fee(prices, fee):
    hold = -float('inf'); cash = 0
    for p in prices:
        cash = max(cash, hold + p - fee)
        hold = max(hold, cash - p)
    return cash
''',
            "complexity": "Time O(n).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "2-state DP (hold/cash); subtract fee on sell.",
    },

    # ==================================================================
    # DP on LIS
    # ==================================================================
    {
        "id": "lis",
        "title": "Longest Increasing Subsequence (LIS) — O(n²) DP",
        "step_id": 16,
        "lecture_id": 7,
        "difficulty": "medium",
        "tags": ["dp", "lis"],
        "what_this_teaches": "Classic n² DP: dp[i] = length of LIS ending at i.",
        "pattern": "1-D DP.",
        "prerequisite_lessons": [],
        "prerequisite_problems": [],
        "next_problems": ["print-lis", "lis-binary-search"],
        "resources": [
            _lc(300, "longest-increasing-subsequence"),
            _SHEET,
        ],
        "understanding": "Length of the longest strictly increasing subsequence.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "For each i, scan all j < i and update dp[i].",
        "optimized": {
            "explanation": "—",
            "code": r'''
def lis_n2(nums):
    n = len(nums)
    dp = [1]*n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
''',
            "complexity": "Time O(n²).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "n² DP; dp[i] = LIS ending at i.",
    },
    {
        "id": "print-lis",
        "title": "Print LIS",
        "step_id": 16,
        "lecture_id": 7,
        "difficulty": "medium",
        "tags": ["dp", "lis"],
        "what_this_teaches": "Traceback using a `prev` index array.",
        "pattern": "DP traceback.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["lis"],
        "next_problems": ["lis-binary-search"],
        "resources": [_SHEET],
        "understanding": "Return the actual LIS, not just its length.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Maintain a `prev[i]` array recording the previous index in the LIS ending at i. Walk back from the argmax of dp.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def print_lis(nums):
    n = len(nums)
    dp = [1]*n; prev = [-1]*n
    end = 0
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j
        if dp[i] > dp[end]:
            end = i
    out = []
    while end != -1:
        out.append(nums[end]); end = prev[end]
    return out[::-1]
''',
            "complexity": "Time O(n²).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "LIS DP + prev array; walk back from argmax(dp).",
    },
    {
        "id": "lis-binary-search",
        "title": "LIS in O(n log n) — Binary Search",
        "step_id": 16,
        "lecture_id": 7,
        "difficulty": "medium",
        "tags": ["dp", "lis", "binary-search"],
        "what_this_teaches": "Maintain `tails[i]` = smallest tail of any increasing subsequence of length i+1.",
        "pattern": "Greedy + binary search.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["lis"],
        "next_problems": ["largest-divisible-subset"],
        "resources": [_lc(300, "longest-increasing-subsequence"), _SHEET],
        "understanding": "Same LIS but in O(n log n).",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Walk nums; for each x, binary-search the leftmost tail ≥ x and replace it. Final tails length = LIS length.",
        "optimized": {
            "explanation": "—",
            "code": r'''
from bisect import bisect_left
def lis_log(nums):
    tails = []
    for x in nums:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)
''',
            "complexity": "Time O(n log n).",
        },
        "deep_concept": "Note: `tails` is *not* the LIS itself — just a structure tracking the best tails. To reconstruct LIS in O(n log n), additional bookkeeping is needed.",
        "confusion_notes": [],
        "summary": "tails[] + bisect_left; length = LIS length.",
    },
    {
        "id": "largest-divisible-subset",
        "title": "Largest Divisible Subset",
        "step_id": 16,
        "lecture_id": 7,
        "difficulty": "medium",
        "tags": ["dp", "lis-variant"],
        "what_this_teaches": "LIS variant where the order is by divisibility, not ≤.",
        "pattern": "LIS DP.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["lis"],
        "next_problems": ["longest-string-chain"],
        "resources": [
            _lc(368, "largest-divisible-subset"),
            _SHEET,
        ],
        "understanding": "Subset where every pair (a, b) satisfies a % b == 0 or b % a == 0. Find the largest.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Sort; LIS-style DP with divisibility as the comparison.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def largest_divisible_subset(nums):
    nums.sort()
    n = len(nums)
    dp = [1]*n; prev = [-1]*n; best_end = 0
    for i in range(n):
        for j in range(i):
            if nums[i] % nums[j] == 0 and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j
        if dp[i] > dp[best_end]:
            best_end = i
    out = []
    i = best_end
    while i != -1:
        out.append(nums[i]); i = prev[i]
    return out[::-1]
''',
            "complexity": "Time O(n²).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Sort + LIS DP with divisibility.",
    },
    {
        "id": "longest-string-chain",
        "title": "Longest String Chain",
        "step_id": 16,
        "lecture_id": 7,
        "difficulty": "medium",
        "tags": ["dp", "lis-variant", "strings"],
        "what_this_teaches": "LIS variant on strings; predecessor = remove one char.",
        "pattern": "DP indexed by string.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["lis"],
        "next_problems": ["longest-bitonic-subseq"],
        "resources": [
            _lc(1048, "longest-string-chain"),
            _SHEET,
        ],
        "understanding": "Chain: w1 is a predecessor of w2 if removing one char from w2 gives w1. Find the longest chain.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Sort by length; for each word, try removing each char and look up the longest chain ending at that predecessor.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def longest_str_chain(words):
    words.sort(key=len)
    dp = {}
    best = 0
    for w in words:
        cur = 1
        for i in range(len(w)):
            pred = w[:i] + w[i+1:]
            if pred in dp:
                cur = max(cur, dp[pred] + 1)
        dp[w] = cur
        best = max(best, cur)
    return best
''',
            "complexity": "Time O(N · L²).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Sort by length; for each word try removing each char to find longest predecessor chain.",
    },
    {
        "id": "longest-bitonic-subseq",
        "title": "Longest Bitonic Subsequence",
        "step_id": 16,
        "lecture_id": 7,
        "difficulty": "medium",
        "tags": ["dp", "lis-variant"],
        "what_this_teaches": "Combine forward LIS and backward LIS.",
        "pattern": "Two-direction LIS.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["lis"],
        "next_problems": ["number-of-lis"],
        "resources": [
            {"label": "GFG — Longest Bitonic Subsequence", "url": "https://www.geeksforgeeks.org/longest-bitonic-subsequence-dp-15/"},
            _SHEET,
        ],
        "understanding": "Longest subsequence that first increases then decreases.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "forward[i] = LIS ending at i; backward[i] = LIS starting at i (computed on reversed array). Max over i of forward[i] + backward[i] - 1.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def longest_bitonic(nums):
    n = len(nums)
    inc = [1]*n; dec = [1]*n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                inc[i] = max(inc[i], inc[j] + 1)
    for i in range(n-1, -1, -1):
        for j in range(i+1, n):
            if nums[j] < nums[i]:
                dec[i] = max(dec[i], dec[j] + 1)
    return max(inc[i] + dec[i] - 1 for i in range(n))
''',
            "complexity": "Time O(n²).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Two LIS arrays (forward / backward); sum at peak.",
    },
    {
        "id": "number-of-lis",
        "title": "Number of Longest Increasing Subsequences",
        "step_id": 16,
        "lecture_id": 7,
        "difficulty": "medium",
        "tags": ["dp", "lis", "counting"],
        "what_this_teaches": "LIS DP carrying a count.",
        "pattern": "LIS + count array.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["lis"],
        "next_problems": ["matrix-chain-multiplication"],
        "resources": [
            _lc(673, "number-of-longest-increasing-subsequence"),
            _SHEET,
        ],
        "understanding": "Count the number of LISs.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Maintain dp[i] = LIS length ending at i, count[i] = number of LISs ending at i. Update both when finding longer/equal chains.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def find_number_of_lis(nums):
    n = len(nums)
    dp = [1]*n; cnt = [1]*n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    cnt[i] = cnt[j]
                elif dp[j] + 1 == dp[i]:
                    cnt[i] += cnt[j]
    longest = max(dp)
    return sum(c for d, c in zip(dp, cnt) if d == longest)
''',
            "complexity": "Time O(n²).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "LIS DP with cnt[i] tracking number of LISs ending at i.",
    },

    # ==================================================================
    # MCM / Partition DP
    # ==================================================================
    {
        "id": "matrix-chain-multiplication",
        "title": "Matrix Chain Multiplication",
        "step_id": 16,
        "lecture_id": 8,
        "difficulty": "medium",
        "tags": ["dp", "mcm", "partition"],
        "what_this_teaches": "Interval DP where the answer at (i, j) depends on all split points k in (i, j).",
        "pattern": "Interval DP.",
        "prerequisite_lessons": [],
        "prerequisite_problems": [],
        "next_problems": ["min-cost-cut-stick", "burst-balloons"],
        "resources": [
            {"label": "GFG — MCM", "url": "https://www.geeksforgeeks.org/matrix-chain-multiplication-dp-8/"},
            _SHEET,
        ],
        "understanding": "Given matrix dimensions arr (with matrix i having dimensions arr[i] × arr[i+1]), find min scalar multiplications to compute the product.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "dp[i][j] = min over k in [i, j) of dp[i][k] + dp[k+1][j] + arr[i] * arr[k+1] * arr[j+1].",
        "optimized": {
            "explanation": "Bottom-up interval DP.",
            "code": r'''
def matrix_chain_order(arr):
    n = len(arr) - 1
    dp = [[0]*n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k+1][j] + arr[i] * arr[k+1] * arr[j+1]
                dp[i][j] = min(dp[i][j], cost)
    return dp[0][n-1]
''',
            "complexity": "Time O(n³).",
        },
        "deep_concept": "Interval DP iterates by *length*, smallest first, so all subintervals are ready when needed.",
        "confusion_notes": [],
        "summary": "Interval DP. dp[i][j] = min over k of dp[i][k] + dp[k+1][j] + chain cost.",
    },
    {
        "id": "min-cost-cut-stick",
        "title": "Minimum Cost to Cut a Stick",
        "step_id": 16,
        "lecture_id": 8,
        "difficulty": "hard",
        "tags": ["dp", "mcm", "partition"],
        "what_this_teaches": "Add 0 and n to the cut list, sort, then MCM-style DP.",
        "pattern": "Interval DP.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["matrix-chain-multiplication"],
        "next_problems": ["burst-balloons"],
        "resources": [
            _lc(1547, "minimum-cost-to-cut-a-stick"),
            _SHEET,
        ],
        "understanding": "Stick of length n with required cut positions. Each cut costs the stick's current length. Minimize total cost.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Add sentinel 0 and n. Sort cuts. dp[i][j] = min cost to make all cuts in (cuts[i], cuts[j]). Try each cut k strictly between i and j.",
        "optimized": {
            "explanation": "Interval DP.",
            "code": r'''
def min_cost_cut(n, cuts):
    cuts = sorted([0] + cuts + [n])
    m = len(cuts)
    dp = [[0]*m for _ in range(m)]
    for length in range(2, m):
        for i in range(m - length):
            j = i + length
            dp[i][j] = float('inf')
            for k in range(i + 1, j):
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + cuts[j] - cuts[i])
    return dp[0][m-1]
''',
            "complexity": "Time O(m³).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Add sentinels; interval DP min cost.",
    },
    {
        "id": "burst-balloons",
        "title": "Burst Balloons",
        "step_id": 16,
        "lecture_id": 8,
        "difficulty": "hard",
        "tags": ["dp", "mcm", "partition"],
        "what_this_teaches": "Interval DP where the cost depends on the *last* element to be removed in the interval, not the first.",
        "pattern": "Interval DP (last-burst).",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["min-cost-cut-stick"],
        "next_problems": ["boolean-parenthesization"],
        "resources": [
            _lc(312, "burst-balloons"),
            _SHEET,
        ],
        "understanding": "Maximize coins from bursting balloons; bursting balloon i gives coins[left] * coins[i] * coins[right].",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Add 1 sentinels. dp[i][j] = best coins for bursting *all* balloons in (i, j). Try each k as the *last* burst: dp[i][k] + dp[k][j] + nums[i] * nums[k] * nums[j].",
        "optimized": {
            "explanation": "Interval DP, k as last burst.",
            "code": r'''
def max_coins(nums):
    arr = [1] + nums + [1]
    n = len(arr)
    dp = [[0]*n for _ in range(n)]
    for length in range(2, n):
        for i in range(n - length):
            j = i + length
            for k in range(i + 1, j):
                dp[i][j] = max(dp[i][j], dp[i][k] + dp[k][j] + arr[i] * arr[k] * arr[j])
    return dp[0][n-1]
''',
            "complexity": "Time O(n³).",
        },
        "deep_concept": "The key insight: choose k as the *last* burst, not the first. This decouples the subintervals (their neighbors are i and j, sentinels).",
        "confusion_notes": [
            {
                "question": "Why choose k as the *last* burst?",
                "answer": "If k is the last burst, then by the time we burst k, the balloons in (i, k) and (k, j) are already gone, so k's neighbors are exactly i and j — fixed and known. Choosing k as the first burst would make its neighbors depend on what's bursted later, which is hard to track.",
            },
        ],
        "summary": "Interval DP with k as the *last* burst; sentinel 1 padding.",
    },
    {
        "id": "boolean-parenthesization",
        "title": "Boolean Parenthesization",
        "step_id": 16,
        "lecture_id": 8,
        "difficulty": "hard",
        "tags": ["dp", "partition"],
        "what_this_teaches": "Counting variant of interval DP, with two states (True / False).",
        "pattern": "Interval DP with two states.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["matrix-chain-multiplication"],
        "next_problems": ["palindrome-partitioning-ii"],
        "resources": [
            {"label": "GFG — Boolean Parenthesization", "url": "https://www.geeksforgeeks.org/boolean-parenthesization-problem-dp-37/"},
            _SHEET,
        ],
        "understanding": "Given a boolean expression like 'T|F&T', count parenthesizations evaluating to True.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "dp[i][j][t] = number of ways for substring i..j to evaluate to t (True/False). For each operator at position k, combine left and right counts.",
        "optimized": {
            "explanation": "Interval DP carrying (T, F) counts.",
            "code": r'''
def count_ways(expr):
    n = len(expr)
    dp = [[[0, 0] for _ in range(n)] for _ in range(n)]
    for i in range(0, n, 2):
        dp[i][i] = [int(expr[i] == 'T'), int(expr[i] == 'F')]
    for length in range(3, n + 1, 2):
        for i in range(0, n - length + 1, 2):
            j = i + length - 1
            for k in range(i + 1, j, 2):
                op = expr[k]
                lt, lf = dp[i][k-1]
                rt, rf = dp[k+1][j]
                if op == '&':
                    dp[i][j][0] += lt * rt
                    dp[i][j][1] += lt * rf + lf * rt + lf * rf
                elif op == '|':
                    dp[i][j][0] += lt * rt + lt * rf + lf * rt
                    dp[i][j][1] += lf * rf
                else:  # ^
                    dp[i][j][0] += lt * rf + lf * rt
                    dp[i][j][1] += lt * rt + lf * rf
    return dp[0][n-1][0]
''',
            "complexity": "Time O(n³).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Interval DP; carry (Trues, Falses) at each (i, j).",
    },
    {
        "id": "palindrome-partitioning-ii",
        "title": "Palindrome Partitioning II",
        "step_id": 16,
        "lecture_id": 8,
        "difficulty": "hard",
        "tags": ["dp", "partition", "palindrome"],
        "what_this_teaches": "Front-partition DP with palindrome lookup.",
        "pattern": "Partition DP.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["boolean-parenthesization"],
        "next_problems": ["partition-max-sum"],
        "resources": [
            _lc(132, "palindrome-partitioning-ii"),
            _SHEET,
        ],
        "understanding": "Min cuts to partition s into palindromes.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Pre-compute is_pal[i][j]. Then dp[i] = min cuts for s[0..i]. dp[i] = 0 if s[0..i] is palindrome; else min(dp[j] + 1) for j < i where s[j+1..i] is palindrome.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def min_cut(s):
    n = len(s)
    is_pal = [[False]*n for _ in range(n)]
    for i in range(n):
        for j in range(i, -1, -1):
            if s[i] == s[j] and (i - j < 2 or is_pal[j+1][i-1]):
                is_pal[j][i] = True
    dp = [0]*n
    for i in range(n):
        if is_pal[0][i]:
            dp[i] = 0
        else:
            dp[i] = float('inf')
            for j in range(1, i + 1):
                if is_pal[j][i]:
                    dp[i] = min(dp[i], dp[j-1] + 1)
    return dp[n-1]
''',
            "complexity": "Time O(n²).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Precompute is_pal; partition DP min cuts.",
    },
    {
        "id": "partition-max-sum",
        "title": "Partition Array for Maximum Sum",
        "step_id": 16,
        "lecture_id": 8,
        "difficulty": "medium",
        "tags": ["dp", "partition"],
        "what_this_teaches": "Front-partition DP: try every back-segment of length 1..k.",
        "pattern": "Partition DP.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["palindrome-partitioning-ii"],
        "next_problems": ["maximal-square"],
        "resources": [
            _lc(1043, "partition-array-for-maximum-sum"),
            _SHEET,
        ],
        "understanding": "Partition into contiguous subarrays of size ≤ k; each subarray becomes its max value. Maximize total.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "dp[i] = max sum considering arr[0..i]. dp[i] = max over j in [1, k] of dp[i-j] + j * max(arr[i-j+1..i]).",
        "optimized": {
            "explanation": "—",
            "code": r'''
def max_sum_after_partitioning(arr, k):
    n = len(arr)
    dp = [0]*(n+1)
    for i in range(1, n+1):
        mx = 0
        for j in range(1, k+1):
            if i - j >= 0:
                mx = max(mx, arr[i-j])
                dp[i] = max(dp[i], dp[i-j] + mx * j)
    return dp[n]
''',
            "complexity": "Time O(n·k).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "1-D partition DP; try every tail length 1..k.",
    },

    # ==================================================================
    # DP on Squares
    # ==================================================================
    {
        "id": "maximal-square",
        "title": "Maximal Square",
        "step_id": 16,
        "lecture_id": 9,
        "difficulty": "medium",
        "tags": ["dp", "grid"],
        "what_this_teaches": "dp[i][j] = size of largest square ending at (i, j) = 1 + min(top, left, top-left) when grid[i][j] = 1.",
        "pattern": "Grid DP.",
        "prerequisite_lessons": [],
        "prerequisite_problems": [],
        "next_problems": ["count-square-submatrices"],
        "resources": [
            _lc(221, "maximal-square"),
            _SHEET,
        ],
        "understanding": "Find the largest square submatrix of all 1s.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "—",
        "optimized": {
            "explanation": "—",
            "code": r'''
def maximal_square(matrix):
    if not matrix: return 0
    m, n = len(matrix), len(matrix[0])
    dp = [0]*n
    best = 0
    prev = 0
    for i in range(m):
        for j in range(n):
            temp = dp[j]
            if int(matrix[i][j]) == 1:
                dp[j] = 1 + min(dp[j-1], prev, dp[j]) if j > 0 else 1
                best = max(best, dp[j])
            else:
                dp[j] = 0
            prev = temp
    return best * best
''',
            "complexity": "Time O(m·n), space O(n).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "dp = 1 + min(top, left, top-left). O(n) space.",
    },
    {
        "id": "count-square-submatrices",
        "title": "Count Square Submatrices with All Ones",
        "step_id": 16,
        "lecture_id": 9,
        "difficulty": "medium",
        "tags": ["dp", "grid"],
        "what_this_teaches": "Same DP as maximal square; sum dp[i][j] gives the count.",
        "pattern": "Grid DP.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["maximal-square"],
        "next_problems": [],
        "resources": [
            _lc(1277, "count-square-submatrices-with-all-ones"),
            _SHEET,
        ],
        "understanding": "Count number of all-1 square submatrices.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Same DP, but sum all dp[i][j].",
        "optimized": {
            "explanation": "—",
            "code": r'''
def count_squares(matrix):
    m, n = len(matrix), len(matrix[0])
    dp = [[0]*n for _ in range(m)]
    total = 0
    for i in range(m):
        for j in range(n):
            if matrix[i][j]:
                if i == 0 or j == 0:
                    dp[i][j] = 1
                else:
                    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
                total += dp[i][j]
    return total
''',
            "complexity": "Time O(m·n).",
        },
        "deep_concept": "Each dp[i][j] counts how many squares end at (i, j); sum gives total.",
        "confusion_notes": [],
        "summary": "Sum the maximal-square DP table.",
    },
]
