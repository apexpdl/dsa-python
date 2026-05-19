"""Step 7 extras — remaining recursion + backtracking problems."""
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
    # ============ Lecture 1 — Get a Strong Hold ============
    {
        "id": "atoi-recursive",
        "title": "Recursive Implementation of atoi",
        "step_id": 7,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["recursion", "strings", "parsing"],
        "what_this_teaches": "How to express the iterative state-machine parser recursively. The recursion builds the integer one digit at a time from the right.",
        "pattern": "Recurse to the right, building the number as you unwind.",
        "prerequisite_lessons": ["recursion", "strings"],
        "prerequisite_problems": ["atoi"],
        "next_problems": ["pow-x-n"],
        "resources": [_SHEET, _lc(8, "string-to-integer-atoi")],
        "understanding": r'''
The iterative `atoi` walks the string left-to-right, accumulating
the integer with `result = result * 10 + digit`. The recursive
version expresses the same idea with recursion: at each call,
parse one character and recurse on the rest.

```python
def atoi_rec(s, i, current):
    if i == len(s) or not s[i].isdigit():
        return current
    return atoi_rec(s, i + 1, current * 10 + int(s[i]))
```

Tail-style recursion (the "carry the accumulator" pattern). Same
algorithm, recursive form.
''',
        "optimized": {
            "explanation": "Recursive accumulator.",
            "code": r'''def my_atoi_rec(s: str) -> int:
    INT_MAX, INT_MIN = 2**31 - 1, -2**31
    s = s.lstrip()
    if not s:
        return 0
    sign = 1
    start = 0
    if s[0] == '-':
        sign = -1
        start = 1
    elif s[0] == '+':
        start = 1

    def helper(i, current):
        if i >= len(s) or not s[i].isdigit():
            return current
        new_val = current * 10 + int(s[i])
        # Clamp eagerly.
        if sign * new_val > INT_MAX:
            return INT_MAX // sign  # will be clamped below
        if sign * new_val < INT_MIN:
            return INT_MIN // sign
        return helper(i + 1, new_val)

    result = helper(start, 0) * sign
    return max(INT_MIN, min(INT_MAX, result))
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(n)* recursion stack.",
        },
        "summary": "**Pattern**: tail-recursive accumulator; one digit per call.",
    },
    {
        "id": "pow-x-n",
        "title": "Pow(x, n) — Fast Exponentiation",
        "step_id": 7,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["recursion", "math", "binary-exponentiation"],
        "what_this_teaches": "Fast exponentiation: x^n = (x^(n/2))^2 for even n; x * x^(n-1) for odd n. Reduces O(n) to O(log n).",
        "pattern": "Recursive halving on the exponent; square the result.",
        "prerequisite_lessons": ["recursion", "dp"],
        "prerequisite_problems": ["fibonacci-number"],
        "next_problems": ["count-good-numbers"],
        "resources": [_SHEET, _lc(50, "powx-n")],
        "understanding": r'''
Compute `x^n` efficiently. Naive: multiply `n` times — *O(n)*.

Fast exponentiation uses the identity `x^n = (x^(n/2))^2` for
even n, and `x * x^(n-1)` for odd n. Halving the exponent each
step gives *O(log n)*.

Handle negative n by computing `1 / x^(-n)`.
''',
        "optimized": {
            "explanation": "Recursive fast exponentiation.",
            "code": r'''def my_pow(x: float, n: int) -> float:
    # Handle negative exponent by inverting the base.
    if n < 0:
        x = 1 / x
        n = -n

    def helper(base, exp):
        if exp == 0:
            return 1.0
        half = helper(base, exp // 2)
        # Square the half-result.
        if exp % 2 == 0:
            return half * half
        else:
            return half * half * base

    return helper(x, n)
''',
            "complexity": "**Time**: *O(log n)*. **Space**: *O(log n)* recursion.",
        },
        "summary": "**Pattern**: halve exponent; square the recursive result.",
    },
    {
        "id": "count-good-numbers",
        "title": "Count Good Numbers",
        "step_id": 7,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["recursion", "math", "binary-exponentiation"],
        "what_this_teaches": "Combinatorial counting with modular fast exponentiation.",
        "pattern": "Compute 5^evens * 4^odds mod p using binary exponentiation.",
        "prerequisite_lessons": ["recursion"],
        "prerequisite_problems": ["pow-x-n"],
        "next_problems": [],
        "resources": [_SHEET, _lc(1922, "count-good-numbers")],
        "understanding": r'''
A "good number" of length n has even digits at even indices and
prime digits at odd indices. There are 5 even digits (0, 2, 4,
6, 8) and 4 single-digit primes (2, 3, 5, 7).

If n digits total, there are `(n + 1) // 2` even-index positions
and `n // 2` odd-index positions. Total count = `5^evens *
4^odds mod (10^9 + 7)`.

Compute each power with modular fast exponentiation.
''',
        "optimized": {
            "explanation": "Modular fast exponentiation.",
            "code": r'''MOD = 10**9 + 7

def count_good_numbers(n: int) -> int:
    def pow_mod(base, exp, mod):
        if exp == 0:
            return 1
        half = pow_mod(base, exp // 2, mod)
        result = (half * half) % mod
        if exp % 2 == 1:
            result = (result * base) % mod
        return result

    evens = (n + 1) // 2
    odds = n // 2
    return (pow_mod(5, evens, MOD) * pow_mod(4, odds, MOD)) % MOD
''',
            "complexity": "**Time**: *O(log n)*. **Space**: *O(log n)*.",
        },
        "summary": "**Pattern**: combinatorial count + modular fast exponentiation.",
    },
    {
        "id": "sort-stack-recursion",
        "title": "Sort a Stack Using Recursion",
        "step_id": 7,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["recursion", "stack"],
        "what_this_teaches": "Recursive helpers that work on the call stack instead of an auxiliary stack. The pattern: pop, recurse, insert-in-sorted-position.",
        "pattern": "Two recursions: outer 'pop, sort rest, insert'; inner 'insert in sorted'.",
        "prerequisite_lessons": ["recursion", "stacks"],
        "prerequisite_problems": ["reverse-stack-recursion"],
        "next_problems": [],
        "resources": [_SHEET],
        "understanding": r'''
Sort a stack with only push/pop/peek and **no extra container**.
Use recursion to hold elements on the call stack.

Algorithm:
1. Pop the top.
2. Recursively sort the remaining stack.
3. Insert the popped element in its sorted position by recursively
   popping until the right spot is found.

Both recursions use the call stack as auxiliary storage. *O(n²)*
time, *O(n)* recursion depth.
''',
        "optimized": {
            "explanation": "Two recursive helpers.",
            "code": r'''def sort_stack(stack: list) -> None:
    def insert_sorted(val):
        if not stack or stack[-1] <= val:
            stack.append(val)
            return
        top = stack.pop()
        insert_sorted(val)
        stack.append(top)

    def sort_rec():
        if not stack:
            return
        top = stack.pop()
        sort_rec()
        insert_sorted(top)

    sort_rec()
''',
            "complexity": "**Time**: *O(n²)*. **Space**: *O(n)* recursion.",
        },
        "summary": "**Pattern**: pop-sort-insert recursion; the call stack acts as auxiliary storage.",
    },
    {
        "id": "reverse-stack-recursion",
        "title": "Reverse a Stack Using Recursion",
        "step_id": 7,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["recursion", "stack"],
        "what_this_teaches": "Same 'use call stack as storage' idea: pop, reverse rest, insert at bottom.",
        "pattern": "Two recursions: outer 'pop, reverse rest, insert at bottom'; inner 'insert at bottom'.",
        "prerequisite_lessons": ["recursion", "stacks"],
        "prerequisite_problems": [],
        "next_problems": ["sort-stack-recursion"],
        "resources": [_SHEET],
        "understanding": r'''
Reverse a stack with only push/pop, no extra container.

Algorithm:
1. Pop the top.
2. Recursively reverse the remaining stack.
3. Insert the popped element **at the bottom** (recursively pop
   everything, push the value, push everything back).
''',
        "optimized": {
            "explanation": "Two recursive helpers.",
            "code": r'''def reverse_stack(stack: list) -> None:
    def insert_bottom(val):
        if not stack:
            stack.append(val)
            return
        top = stack.pop()
        insert_bottom(val)
        stack.append(top)

    def reverse_rec():
        if not stack:
            return
        top = stack.pop()
        reverse_rec()
        insert_bottom(top)

    reverse_rec()
''',
            "complexity": "**Time**: *O(n²)*. **Space**: *O(n)* recursion.",
        },
        "summary": "**Pattern**: pop-reverse-insert-at-bottom recursion.",
    },
    # ============ Lecture 2 — Subsequence Pattern ============
    {
        "id": "binary-strings-no-consecutive-ones",
        "title": "Generate Binary Strings Without Consecutive 1s",
        "step_id": 7,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["recursion", "backtracking"],
        "what_this_teaches": "Backtracking with a state constraint. At each position, only certain choices are valid based on the previous choice.",
        "pattern": "At each index, try '0' (always); try '1' only if last char wasn't '1'.",
        "prerequisite_lessons": ["recursion", "backtracking"],
        "prerequisite_problems": ["print-all-subsequences"],
        "next_problems": ["generate-parentheses"],
        "resources": [_SHEET],
        "understanding": r'''
Generate all binary strings of length n with no two consecutive
1s.

For n = 3: `000, 001, 010, 100, 101`. Five strings.

Backtracking: at each position, try '0' (always valid); try '1'
only if the previous character was not '1'.
''',
        "optimized": {
            "explanation": "Backtracking with last-char constraint.",
            "code": r'''def generate_binary_no_consecutive_ones(n: int) -> list[str]:
    result = []
    def helper(pos, current, last):
        if pos == n:
            result.append(''.join(current))
            return
        # Always try 0.
        current.append('0')
        helper(pos + 1, current, '0')
        current.pop()
        # Try 1 only if last wasn't 1.
        if last != '1':
            current.append('1')
            helper(pos + 1, current, '1')
            current.pop()
    helper(0, [], '')
    return result
''',
            "complexity": "**Time**: *O(Fib(n))* output count, each O(n). **Space**: *O(n)* recursion.",
        },
        "summary": "**Pattern**: backtracking with constraint on consecutive choices.",
    },
    {
        "id": "generate-parentheses",
        "title": "Generate All Valid Parentheses",
        "step_id": 7,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["recursion", "backtracking"],
        "what_this_teaches": "Backtracking with two state counters (open and close). Constraint: never close more than you've opened.",
        "pattern": "Try '(' if opens < n; try ')' if closes < opens.",
        "prerequisite_lessons": ["recursion", "backtracking"],
        "prerequisite_problems": ["print-all-subsequences"],
        "next_problems": ["combination-sum", "letter-combinations-phone"],
        "resources": [_SHEET, _lc(22, "generate-parentheses")],
        "understanding": r'''
Generate all valid parenthesis combinations of length 2n.

For n = 3: `((())), (()()), (())(), ()(()), ()()()`. Five.

Backtracking with two counters: `opens` (count of '(' so far)
and `closes` (count of ')'). Valid moves:

- Add '(' if opens < n.
- Add ')' if closes < opens (so we never have more closes than opens).

Stop when both counts equal n.
''',
        "optimized": {
            "explanation": "Backtracking with two counters.",
            "code": r'''def generate_parentheses(n: int) -> list[str]:
    result = []
    def helper(current, opens, closes):
        if len(current) == 2 * n:
            result.append(''.join(current))
            return
        if opens < n:
            current.append('(')
            helper(current, opens + 1, closes)
            current.pop()
        if closes < opens:
            current.append(')')
            helper(current, opens, closes + 1)
            current.pop()
    helper([], 0, 0)
    return result
''',
            "complexity": "**Time**: *O(Catalan(n) * n)*. **Space**: *O(n)* recursion.",
        },
        "summary": "**Pattern**: backtracking with open/close counters; never close more than opened.",
    },
    {
        "id": "subsequence-sum-k",
        "title": "Subsequences with Sum K",
        "step_id": 7,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["recursion", "subsequences"],
        "what_this_teaches": "Take-or-skip recursion with a running sum; check at the leaves.",
        "pattern": "At each index, recurse twice (take/skip); check sum at base case.",
        "prerequisite_lessons": ["recursion"],
        "prerequisite_problems": ["print-all-subsequences"],
        "next_problems": ["combination-sum", "subset-sum-i"],
        "resources": [_SHEET],
        "understanding": r'''
Three variants:
1. **Check existence** of any subsequence summing to k.
2. **Print one** such subsequence.
3. **Count** all such subsequences.

All use the take-or-skip recursion with a running sum.
''',
        "optimized": {
            "explanation": "Take-or-skip recursion; collect subsequences with sum K.",
            "code": r'''def subsequences_sum_k(arr: list[int], k: int) -> list[list[int]]:
    result = []
    def helper(i, current, current_sum):
        if i == len(arr):
            if current_sum == k:
                result.append(current[:])
            return
        # Take arr[i].
        current.append(arr[i])
        helper(i + 1, current, current_sum + arr[i])
        current.pop()
        # Skip arr[i].
        helper(i + 1, current, current_sum)
    helper(0, [], 0)
    return result
''',
            "complexity": "**Time**: *O(2^n * n)*. **Space**: *O(n)*.",
        },
        "summary": "**Pattern**: take-or-skip + running sum; check at leaves.",
    },
    {
        "id": "combination-sum",
        "title": "Combination Sum",
        "step_id": 7,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["recursion", "backtracking"],
        "what_this_teaches": "Like take-or-skip, but 'take' can be repeated (unlimited reuse of the current element).",
        "pattern": "Take (stay at index i, allowing reuse) or skip (move to i+1).",
        "prerequisite_lessons": ["recursion", "backtracking"],
        "prerequisite_problems": ["subsequence-sum-k"],
        "next_problems": ["combination-sum-ii", "combination-sum-iii"],
        "resources": [_SHEET, _lc(39, "combination-sum")],
        "understanding": r'''
Given distinct positive integers and a target, return all unique
combinations that sum to target. **Each number can be reused
unlimited times**.

Backtracking: take-or-skip, but when "taking" stay at the same
index (allowing reuse).
''',
        "optimized": {
            "explanation": "Take-with-reuse or skip recursion.",
            "code": r'''def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    result = []
    def helper(i, current, remaining):
        if remaining == 0:
            result.append(current[:])
            return
        if i == len(candidates) or remaining < 0:
            return
        # Take candidates[i] (stay at i for reuse).
        current.append(candidates[i])
        helper(i, current, remaining - candidates[i])
        current.pop()
        # Skip.
        helper(i + 1, current, remaining)
    helper(0, [], target)
    return result
''',
            "complexity": "**Time**: exponential. **Space**: *O(target / min_candidate)* recursion.",
        },
        "summary": "**Pattern**: take-with-reuse or skip; the take branch stays at same index.",
    },
    {
        "id": "combination-sum-ii",
        "title": "Combination Sum II",
        "step_id": 7,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["recursion", "backtracking"],
        "what_this_teaches": "Sort + skip-duplicates: prevent duplicate combinations by skipping equal candidates after the first usage.",
        "pattern": "Sort, then at each position try each distinct value once.",
        "prerequisite_lessons": ["recursion", "backtracking"],
        "prerequisite_problems": ["combination-sum"],
        "next_problems": ["combination-sum-iii", "subset-sum-ii"],
        "resources": [_SHEET, _lc(40, "combination-sum-ii")],
        "understanding": r'''
Like combination-sum but **each number can be used at most
once**, and the input may have duplicates. Return unique
combinations summing to target.

Trick: sort first; in the recursion, skip duplicate candidates
at the same recursion level (using `if i > start and
candidates[i] == candidates[i - 1]: continue`).
''',
        "optimized": {
            "explanation": "Sort + skip duplicates at same level.",
            "code": r'''def combination_sum_ii(candidates: list[int], target: int) -> list[list[int]]:
    candidates.sort()
    result = []
    def helper(start, current, remaining):
        if remaining == 0:
            result.append(current[:])
            return
        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i - 1]:
                continue
            if candidates[i] > remaining:
                break
            current.append(candidates[i])
            helper(i + 1, current, remaining - candidates[i])
            current.pop()
    helper(0, [], target)
    return result
''',
            "complexity": "**Time**: exponential. **Space**: *O(target)*.",
        },
        "summary": "**Pattern**: sort + skip duplicates at same recursion level.",
    },
    {
        "id": "subset-sum-i",
        "title": "Subset Sum I (All Subset Sums)",
        "step_id": 7,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["recursion", "subsequences"],
        "what_this_teaches": "Generate all possible subset sums via take-or-skip.",
        "pattern": "At each index, recurse twice (take/skip); collect the sum at base.",
        "prerequisite_lessons": ["recursion"],
        "prerequisite_problems": ["print-all-subsequences"],
        "next_problems": ["subset-sum-ii"],
        "resources": [_SHEET],
        "understanding": "Generate all 2^n subset sums. Take-or-skip recursion.",
        "optimized": {
            "explanation": "Take-or-skip; collect each subset's sum.",
            "code": r'''def subset_sums(arr: list[int]) -> list[int]:
    result = []
    def helper(i, current_sum):
        if i == len(arr):
            result.append(current_sum)
            return
        helper(i + 1, current_sum + arr[i])  # take
        helper(i + 1, current_sum)            # skip
    helper(0, 0)
    return result
''',
            "complexity": "**Time**: *O(2^n)*. **Space**: *O(n)*.",
        },
        "summary": "**Pattern**: take-or-skip + collect sum at leaves.",
    },
    {
        "id": "subset-sum-ii",
        "title": "Subset Sum II (Subsets with Duplicates)",
        "step_id": 7,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["recursion", "backtracking"],
        "what_this_teaches": "Generate unique subsets from an array with duplicates.",
        "pattern": "Sort + skip duplicates at same level (same as combination-sum-ii).",
        "prerequisite_lessons": ["recursion", "backtracking"],
        "prerequisite_problems": ["subset-sum-i", "combination-sum-ii"],
        "next_problems": [],
        "resources": [_SHEET, _lc(90, "subsets-ii")],
        "understanding": "Generate all unique subsets when the input has duplicates. Sort and skip duplicates.",
        "optimized": {
            "explanation": "Sort + take/skip with duplicate skipping.",
            "code": r'''def subsets_with_dup(arr: list[int]) -> list[list[int]]:
    arr.sort()
    result = []
    def helper(start, current):
        result.append(current[:])
        for i in range(start, len(arr)):
            if i > start and arr[i] == arr[i - 1]:
                continue
            current.append(arr[i])
            helper(i + 1, current)
            current.pop()
    helper(0, [])
    return result
''',
            "complexity": "**Time**: *O(2^n)*. **Space**: *O(n)*.",
        },
        "summary": "**Pattern**: sort + iterate from start; skip duplicates at same level.",
    },
    {
        "id": "combination-sum-iii",
        "title": "Combination Sum III",
        "step_id": 7,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["recursion", "backtracking"],
        "what_this_teaches": "Constrained backtracking: pick exactly k numbers from 1-9 summing to n.",
        "pattern": "Backtrack over choices 1-9; constraints on count and sum.",
        "prerequisite_lessons": ["recursion", "backtracking"],
        "prerequisite_problems": ["combination-sum-ii"],
        "next_problems": ["letter-combinations-phone"],
        "resources": [_SHEET, _lc(216, "combination-sum-iii")],
        "understanding": "Find all combinations of k distinct numbers from 1-9 summing to n.",
        "optimized": {
            "explanation": "Backtracking with count and sum constraints.",
            "code": r'''def combination_sum_iii(k: int, n: int) -> list[list[int]]:
    result = []
    def helper(start, current, remaining):
        if len(current) == k:
            if remaining == 0:
                result.append(current[:])
            return
        for i in range(start, 10):
            if i > remaining:
                break
            current.append(i)
            helper(i + 1, current, remaining - i)
            current.pop()
    helper(1, [], n)
    return result
''',
            "complexity": "**Time**: *O(C(9, k))*. **Space**: *O(k)*.",
        },
        "summary": "**Pattern**: backtracking on a small fixed range with count + sum constraints.",
    },
    {
        "id": "letter-combinations-phone",
        "title": "Letter Combinations of a Phone Number",
        "step_id": 7,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["recursion", "backtracking"],
        "what_this_teaches": "Backtracking over a tree of choices, one digit at a time.",
        "pattern": "For each digit, recursively choose one of its letters.",
        "prerequisite_lessons": ["recursion", "backtracking"],
        "prerequisite_problems": ["generate-parentheses"],
        "next_problems": [],
        "resources": [_SHEET, _lc(17, "letter-combinations-of-a-phone-number")],
        "understanding": "Classic phone keypad combinations. For digits like '23', generate 'ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf'.",
        "optimized": {
            "explanation": "Backtracking through digit positions.",
            "code": r'''def letter_combinations(digits: str) -> list[str]:
    if not digits:
        return []
    mapping = {'2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
               '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'}
    result = []
    def helper(i, current):
        if i == len(digits):
            result.append(''.join(current))
            return
        for ch in mapping[digits[i]]:
            current.append(ch)
            helper(i + 1, current)
            current.pop()
    helper(0, [])
    return result
''',
            "complexity": "**Time**: *O(4^n * n)*. **Space**: *O(n)*.",
        },
        "summary": "**Pattern**: backtracking with one position per digit; branch over each digit's letters.",
    },
    # ============ Lecture 3 — Hard ============
    {
        "id": "palindrome-partitioning",
        "title": "Palindrome Partitioning",
        "step_id": 7,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["recursion", "backtracking", "palindrome"],
        "what_this_teaches": "Recursive partitioning of a string into palindromic substrings.",
        "pattern": "For each starting position, try every prefix; recurse on the rest if the prefix is palindromic.",
        "prerequisite_lessons": ["recursion", "backtracking", "strings"],
        "prerequisite_problems": ["generate-parentheses", "check-string-palindrome-recursion"],
        "next_problems": ["word-break", "palindrome-partitioning-ii"],
        "resources": [_SHEET, _lc(131, "palindrome-partitioning")],
        "understanding": r'''
Partition the string into substrings, each of which is a
palindrome. Return all such partitionings.

`"aab"` → `[["a","a","b"], ["aa","b"]]`.

Backtracking: try each prefix; if palindromic, recurse on the
suffix.
''',
        "optimized": {
            "explanation": "Try every palindromic prefix; recurse.",
            "code": r'''def partition_palindromes(s: str) -> list[list[str]]:
    result = []
    def is_palindrome(t):
        return t == t[::-1]
    def helper(start, current):
        if start == len(s):
            result.append(current[:])
            return
        for end in range(start + 1, len(s) + 1):
            piece = s[start:end]
            if is_palindrome(piece):
                current.append(piece)
                helper(end, current)
                current.pop()
    helper(0, [])
    return result
''',
            "complexity": "**Time**: *O(2^n * n)*. **Space**: *O(n)*.",
        },
        "summary": "**Pattern**: try every palindromic prefix at each position; recurse on the suffix.",
    },
    {
        "id": "word-search",
        "title": "Word Search in a Grid",
        "step_id": 7,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["recursion", "backtracking", "grid"],
        "what_this_teaches": "Grid DFS with visited-marking and backtracking.",
        "pattern": "For each cell, DFS into 4 neighbors; mark visited; unmark on return.",
        "prerequisite_lessons": ["recursion", "backtracking"],
        "prerequisite_problems": ["n-queens"],
        "next_problems": ["rat-in-a-maze", "sudoku-solver"],
        "resources": [_SHEET, _lc(79, "word-search")],
        "understanding": r'''
Given a 2D board of characters and a word, find if the word can
be constructed from sequentially adjacent (up/down/left/right)
cells, where each cell is used at most once.

DFS from each cell; mark visited; recurse into 4 neighbors;
backtrack.
''',
        "optimized": {
            "explanation": "DFS with backtracking; mark/unmark each cell.",
            "code": r'''def word_search(board: list[list[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])
    def dfs(r, c, i):
        if i == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[i]:
            return False
        # Mark visited by overwriting; unmark on return.
        tmp = board[r][c]
        board[r][c] = '#'
        found = (dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1) or
                 dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1))
        board[r][c] = tmp
        return found
    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
''',
            "complexity": "**Time**: *O(m * n * 4^L)* where L is word length. **Space**: *O(L)* recursion.",
        },
        "summary": "**Pattern**: 4-direction DFS with mark/unmark backtracking.",
    },
    {
        "id": "sudoku-solver",
        "title": "Sudoku Solver",
        "step_id": 7,
        "lecture_id": 3,
        "difficulty": "hard",
        "tags": ["recursion", "backtracking", "constraints"],
        "what_this_teaches": "Backtracking with three constraint sets (row, column, 3x3 box).",
        "pattern": "For each empty cell, try each digit 1-9; check row/col/box validity; recurse; backtrack.",
        "prerequisite_lessons": ["recursion", "backtracking"],
        "prerequisite_problems": ["n-queens"],
        "next_problems": ["m-coloring"],
        "resources": [_SHEET, _lc(37, "sudoku-solver")],
        "understanding": r'''
Solve a partially-filled 9x9 Sudoku in place.

For each empty cell, try each digit 1-9. Check that the digit
doesn't already appear in the row, column, or 3x3 box. If
valid, place and recurse. On dead end, backtrack.

The three constraint sets (row, col, box) enable *O(1)*
validity checks. With careful pruning, the algorithm solves
typical Sudoku in milliseconds.
''',
        "optimized": {
            "explanation": "Backtracking with 27 constraint sets.",
            "code": r'''def solve_sudoku(board: list[list[str]]) -> None:
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    empties = []
    for r in range(9):
        for c in range(9):
            if board[r][c] == '.':
                empties.append((r, c))
            else:
                d = board[r][c]
                rows[r].add(d); cols[c].add(d); boxes[(r // 3) * 3 + c // 3].add(d)

    def backtrack(idx):
        if idx == len(empties):
            return True
        r, c = empties[idx]
        b = (r // 3) * 3 + c // 3
        for d in '123456789':
            if d not in rows[r] and d not in cols[c] and d not in boxes[b]:
                board[r][c] = d
                rows[r].add(d); cols[c].add(d); boxes[b].add(d)
                if backtrack(idx + 1):
                    return True
                board[r][c] = '.'
                rows[r].remove(d); cols[c].remove(d); boxes[b].remove(d)
        return False

    backtrack(0)
''',
            "complexity": "**Time**: exponential worst-case but very fast in practice. **Space**: *O(81)*.",
        },
        "summary": "**Pattern**: backtracking with row/column/box constraint sets.",
    },
    {
        "id": "m-coloring",
        "title": "M-Coloring Problem",
        "step_id": 7,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["recursion", "backtracking", "graph"],
        "what_this_teaches": "Constraint-satisfaction backtracking on a graph.",
        "pattern": "For each vertex, try each color; check no adjacent has the same; recurse; backtrack.",
        "prerequisite_lessons": ["recursion", "backtracking"],
        "prerequisite_problems": ["n-queens", "sudoku-solver"],
        "next_problems": ["rat-in-a-maze"],
        "resources": [
            _SHEET,
            {"label": "GFG — m Coloring Problem",
             "url": "https://www.geeksforgeeks.org/m-coloring-problem-backtracking-5/"},
        ],
        "understanding": "Can we color a graph with m colors so that no two adjacent vertices share a color?",
        "optimized": {
            "explanation": "Backtracking with adjacency-check.",
            "code": r'''def graph_coloring(graph: dict, m: int) -> bool:
    nodes = list(graph)
    color = {}
    def is_safe(v, c):
        return all(color.get(u) != c for u in graph[v])
    def helper(i):
        if i == len(nodes):
            return True
        v = nodes[i]
        for c in range(m):
            if is_safe(v, c):
                color[v] = c
                if helper(i + 1):
                    return True
                del color[v]
        return False
    return helper(0)
''',
            "complexity": "**Time**: *O(m^V)* worst case. **Space**: *O(V)*.",
        },
        "summary": "**Pattern**: backtracking; check adjacency constraints; assign color or fail.",
    },
    {
        "id": "rat-in-a-maze",
        "title": "Rat in a Maze",
        "step_id": 7,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["recursion", "backtracking", "grid"],
        "what_this_teaches": "Path-finding via backtracking on a 2D grid with blocked cells.",
        "pattern": "DFS with direction priority + visited marking + unmark on backtrack.",
        "prerequisite_lessons": ["recursion", "backtracking"],
        "prerequisite_problems": ["word-search"],
        "next_problems": [],
        "resources": [
            _SHEET,
            {"label": "GFG — Rat in a Maze",
             "url": "https://www.geeksforgeeks.org/rat-in-a-maze-backtracking-2/"},
        ],
        "understanding": "Find all paths a rat can take from (0,0) to (n-1,n-1) in a grid with blocked cells. Moves: D, L, R, U.",
        "optimized": {
            "explanation": "DFS with mark/unmark; ordered direction tries.",
            "code": r'''def rat_in_maze(maze: list[list[int]]) -> list[str]:
    n = len(maze)
    if maze[0][0] == 0 or maze[n - 1][n - 1] == 0:
        return []
    result = []
    visited = [[False] * n for _ in range(n)]
    dirs = [('D', 1, 0), ('L', 0, -1), ('R', 0, 1), ('U', -1, 0)]
    def dfs(r, c, path):
        if r == n - 1 and c == n - 1:
            result.append(''.join(path))
            return
        visited[r][c] = True
        for d, dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and maze[nr][nc] == 1:
                path.append(d)
                dfs(nr, nc, path)
                path.pop()
        visited[r][c] = False
    dfs(0, 0, [])
    return result
''',
            "complexity": "**Time**: *O(4^(n²))* worst case. **Space**: *O(n²)*.",
        },
        "summary": "**Pattern**: DFS with mark/unmark on grid; ordered direction tries.",
    },
    {
        "id": "word-break",
        "title": "Word Break I",
        "step_id": 7,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["recursion", "dp", "memoization"],
        "what_this_teaches": "Recursive decomposition: can the string be split into dictionary words? Memoize to avoid redoing.",
        "pattern": "Try every prefix that's a word; recurse on the suffix. Memoize by start index.",
        "prerequisite_lessons": ["recursion", "dp"],
        "prerequisite_problems": ["palindrome-partitioning"],
        "next_problems": [],
        "resources": [_SHEET, _lc(139, "word-break")],
        "understanding": "Can the string be segmented into a sequence of dictionary words? Recursion + memo.",
        "optimized": {
            "explanation": "Memoized recursion.",
            "code": r'''from functools import lru_cache

def word_break(s: str, words: list[str]) -> bool:
    word_set = set(words)

    @lru_cache(maxsize=None)
    def helper(start):
        if start == len(s):
            return True
        for end in range(start + 1, len(s) + 1):
            if s[start:end] in word_set and helper(end):
                return True
        return False
    return helper(0)
''',
            "complexity": "**Time**: *O(n²)* (with memo, n start positions × n end positions). **Space**: *O(n)*.",
        },
        "summary": "**Pattern**: memoized recursion; try every word-prefix; recurse on suffix.",
    },
    {
        "id": "expression-add-operators",
        "title": "Expression Add Operators",
        "step_id": 7,
        "lecture_id": 3,
        "difficulty": "hard",
        "tags": ["recursion", "backtracking", "math"],
        "what_this_teaches": "Backtracking with operator precedence tracking. The 'multiply' case requires remembering the last operand to undo and re-add with the product.",
        "pattern": "Try every prefix as the next operand; try +, -, * after; track previous operand for multiplication adjustment.",
        "prerequisite_lessons": ["recursion", "backtracking"],
        "prerequisite_problems": ["combination-sum"],
        "next_problems": [],
        "resources": [_SHEET, _lc(282, "expression-add-operators")],
        "understanding": r'''
Given a digit string and a target, return all ways to insert
`+`, `-`, `*` operators so the expression evaluates to target.

The tricky part: multiplication has higher precedence. When the
operator is `*`, we have to "undo" the previous addition and
re-add with the product.

Track `prev_operand` to handle this.
''',
        "optimized": {
            "explanation": "Backtrack over each split point; handle precedence.",
            "code": r'''def add_operators(num: str, target: int) -> list[str]:
    result = []
    def helper(start, path, value, prev):
        if start == len(num):
            if value == target:
                result.append(path)
            return
        for end in range(start + 1, len(num) + 1):
            piece = num[start:end]
            if len(piece) > 1 and piece[0] == '0':
                break   # no leading zeros
            n = int(piece)
            if start == 0:
                helper(end, piece, n, n)
            else:
                helper(end, path + '+' + piece, value + n, n)
                helper(end, path + '-' + piece, value - n, -n)
                # Multiplication: undo prev addition, multiply.
                helper(end, path + '*' + piece, value - prev + prev * n, prev * n)
    helper(0, '', 0, 0)
    return result
''',
            "complexity": "**Time**: exponential. **Space**: *O(n)* recursion.",
        },
        "summary": "**Pattern**: backtracking with prev-operand bookkeeping for multiplication precedence.",
    },
]
