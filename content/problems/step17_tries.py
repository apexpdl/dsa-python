"""Step 17 — Tries (6 problems).

Trie data structure, two implementation styles, and four classic
applications (longest word with all prefixes, distinct substring count,
maximum XOR via bitwise trie, max-XOR with element-queries).
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
    {
        "id": "trie-impl-i",
        "title": "Implement Trie (Insert, Search, StartsWith)",
        "step_id": 17,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["trie", "design"],
        "what_this_teaches": "Trie node = dict of children + end-of-word flag. Insert/Search/StartsWith are O(L).",
        "pattern": "Trie basic implementation.",
        "prerequisite_lessons": [],
        "prerequisite_problems": [],
        "next_problems": ["trie-impl-ii", "longest-word-all-prefixes"],
        "resources": [
            _lc(208, "implement-trie-prefix-tree"),
            _SHEET,
        ],
        "understanding": r'''
A **Trie** (also called *prefix tree*) is a tree where each path from
the root spells a string. Each node has a set of children (one per
possible next character) and a flag marking 'end of a stored word'.

**Why trie?** Searching a hash table for a word is O(L) where L is the
word length. But hash tables can't efficiently answer 'does any stored
word start with this prefix?' — for that, a trie is the natural choice.

Real uses: autocomplete, spell checkers, IP routing, longest-prefix
matching, dictionary problems.
''',
        "brute_force": {
            "explanation": "Store all words in a list; linear scan on every query. O(N · L) per query.",
            "code": "",
            "complexity": "—",
        },
        "thought_process": "Each node has a children dict (or array of 26 for lowercase letters) and an `is_end` flag.",
        "optimized": {
            "explanation": "Classic trie node + class.",
            "code": r'''
class Trie:
    def __init__(self):
        self.children = {}
        self.is_end = False

    def insert(self, word):
        node = self
        for c in word:
            if c not in node.children:
                node.children[c] = Trie()
            node = node.children[c]
        node.is_end = True

    def search(self, word):
        node = self._find(word)
        return node is not None and node.is_end

    def starts_with(self, prefix):
        return self._find(prefix) is not None

    def _find(self, s):
        node = self
        for c in s:
            if c not in node.children:
                return None
            node = node.children[c]
        return node
''',
            "complexity": "Time O(L) per operation. Space O(N · L).",
        },
        "deep_concept": r'''
The trade-off: tries use more memory than hash tables (each node is a
small object) but support prefix-related queries that hashes can't.
''',
        "confusion_notes": [
            {
                "question": "Dict of children or array[26]?",
                "answer": "Array[26] is faster when the alphabet is small and fixed (lowercase letters). Dict is more flexible (Unicode, sparse charsets). Pick based on input domain.",
            },
        ],
        "summary": "Trie: tree where each node has children-by-char and an end-of-word flag. O(L) per op.",
    },
    {
        "id": "trie-impl-ii",
        "title": "Trie II — Count Words and Count Prefixes",
        "step_id": 17,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["trie", "design"],
        "what_this_teaches": "Store `count_end` and `count_prefix` at each node to support frequency queries.",
        "pattern": "Trie with counters.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["trie-impl-i"],
        "next_problems": ["longest-word-all-prefixes"],
        "resources": [
            {"label": "Striver — Implement Trie II", "url": "https://takeuforward.org/data-structure/implement-trie-ii/"},
            _SHEET,
        ],
        "understanding": "Support: `insert`, `count_words_equal_to(w)`, `count_words_starting_with(p)`, and `erase(w)`.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Each node maintains `count_end` (how many words end here) and `count_prefix` (how many words go through here). Increment on insert, decrement on erase.",
        "optimized": {
            "explanation": "Trie with two counters.",
            "code": r'''
class TrieII:
    def __init__(self):
        self.children = {}
        self.count_end = 0
        self.count_prefix = 0

    def insert(self, word):
        node = self
        for c in word:
            if c not in node.children:
                node.children[c] = TrieII()
            node = node.children[c]
            node.count_prefix += 1
        node.count_end += 1

    def count_words_equal_to(self, word):
        node = self._find(word)
        return node.count_end if node else 0

    def count_words_starting_with(self, prefix):
        node = self._find(prefix)
        return node.count_prefix if node else 0

    def erase(self, word):
        node = self
        path = []
        for c in word:
            path.append((node, c))
            node = node.children.get(c)
            if node is None:
                return
            node.count_prefix -= 1
        node.count_end -= 1

    def _find(self, s):
        node = self
        for c in s:
            if c not in node.children:
                return None
            node = node.children[c]
        return node
''',
            "complexity": "Time O(L) per op.",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Trie with count_end and count_prefix per node.",
    },
    {
        "id": "longest-word-all-prefixes",
        "title": "Longest Word with All Prefixes Present",
        "step_id": 17,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["trie", "strings"],
        "what_this_teaches": "Trie traversal verifying that every prefix of a candidate word is also a stored word.",
        "pattern": "Trie + DFS / scan.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["trie-impl-i"],
        "next_problems": ["distinct-substrings-count"],
        "resources": [
            {"label": "GFG — Word with all prefixes", "url": "https://www.geeksforgeeks.org/find-the-longest-string-that-can-be-made-up-of-other-strings-from-the-array/"},
            _SHEET,
        ],
        "understanding": "From a list of words, find the longest one such that *every* prefix of it (of length 1, 2, ..., L-1) is also in the list.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Insert all words. For each word, walk char-by-char and at every step check `is_end` — every prefix must be a stored word.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def longest_word_all_prefixes(words):
    root = {}
    END = '$'
    for w in words:
        node = root
        for c in w:
            node = node.setdefault(c, {})
        node[END] = True
    best = ""
    for w in sorted(words, key=lambda x: (-len(x), x)):
        node = root
        ok = True
        for c in w:
            node = node[c]
            if END not in node:
                ok = False; break
        if ok:
            return w
    return ""
''',
            "complexity": "Time O(total chars).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Walk each word in the trie; every node along the way must mark end-of-word.",
    },
    {
        "id": "distinct-substrings-count",
        "title": "Count Distinct Substrings",
        "step_id": 17,
        "lecture_id": 2,
        "difficulty": "hard",
        "tags": ["trie", "strings"],
        "what_this_teaches": "Insert every suffix into a trie; count distinct nodes (excluding the root) = distinct substrings.",
        "pattern": "Suffix trie.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["trie-impl-i"],
        "next_problems": ["max-xor-two-numbers"],
        "resources": [
            {"label": "Striver — Distinct Substrings", "url": "https://takeuforward.org/data-structure/count-distinct-substrings-of-a-string-using-trie/"},
            _SHEET,
        ],
        "understanding": "Count the number of distinct non-empty substrings of s.",
        "brute_force": {"explanation": "Generate all O(n²) substrings, put in a set. O(n³) total.", "code": "", "complexity": "—"},
        "thought_process": "Insert every suffix into a trie. Each distinct substring corresponds to a distinct path from the root. Count the number of nodes added (excluding root).",
        "optimized": {
            "explanation": "Build a suffix trie; count nodes.",
            "code": r'''
def count_distinct_substrings(s):
    root = {}
    count = 0
    for i in range(len(s)):
        node = root
        for c in s[i:]:
            if c not in node:
                node[c] = {}
                count += 1
            node = node[c]
    return count
''',
            "complexity": "Time O(n²), space O(n²) in the worst case.",
        },
        "deep_concept": "Suffix trees (a compressed version of suffix tries) achieve O(n) space and time. The suffix-trie version is the conceptual baseline.",
        "confusion_notes": [],
        "summary": "Insert every suffix into a trie; count nodes added.",
    },
    {
        "id": "max-xor-two-numbers",
        "title": "Maximum XOR of Two Numbers in an Array",
        "step_id": 17,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["trie", "bit-manipulation"],
        "what_this_teaches": "Bitwise trie — store each number's bits from MSB to LSB; for each number, greedily walk the trie choosing the opposite bit when possible.",
        "pattern": "Binary trie.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["trie-impl-i"],
        "next_problems": ["max-xor-with-element-queries"],
        "resources": [
            _lc(421, "maximum-xor-of-two-numbers-in-an-array"),
            _SHEET,
        ],
        "understanding": "Find max(a XOR b) over all pairs.",
        "brute_force": {"explanation": "All pairs O(n²).", "code": "", "complexity": "—"},
        "thought_process": "Build a bitwise trie of all numbers (MSB first, 31 bits for ints). For each number, walk the trie taking the *opposite* bit at each step when available — that maximizes XOR.",
        "optimized": {
            "explanation": "Bitwise trie.",
            "code": r'''
def find_maximum_xor(nums):
    root = {}
    for x in nums:
        node = root
        for i in range(31, -1, -1):
            b = (x >> i) & 1
            if b not in node:
                node[b] = {}
            node = node[b]
    best = 0
    for x in nums:
        node = root
        xor = 0
        for i in range(31, -1, -1):
            b = (x >> i) & 1
            want = 1 - b
            if want in node:
                xor |= (1 << i)
                node = node[want]
            else:
                node = node[b]
        best = max(best, xor)
    return best
''',
            "complexity": "Time O(n · 32).",
        },
        "deep_concept": "—",
        "confusion_notes": [],
        "summary": "Bitwise trie; walk greedily to maximize XOR per number.",
    },
    {
        "id": "max-xor-with-element-queries",
        "title": "Maximum XOR with Element Constraints (Queries)",
        "step_id": 17,
        "lecture_id": 2,
        "difficulty": "hard",
        "tags": ["trie", "bit-manipulation", "offline"],
        "what_this_teaches": "Offline query processing: sort queries and array together; insert into trie up to each query's threshold.",
        "pattern": "Offline + bitwise trie.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["max-xor-two-numbers"],
        "next_problems": [],
        "resources": [
            _lc(1707, "maximum-xor-with-an-element-from-array"),
            _SHEET,
        ],
        "understanding": "For each query (x, m), return the maximum x XOR a over elements a ≤ m in the array (or -1 if none).",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Sort the array and queries by their threshold m. Walk through queries in order; insert array elements ≤ m into the trie; then answer the query using the bitwise-trie greedy.",
        "optimized": {
            "explanation": "Offline sweep + bitwise trie.",
            "code": r'''
def maximize_xor(nums, queries):
    nums.sort()
    indexed = sorted(((m, x, i) for i, (x, m) in enumerate(queries)), key=lambda q: q[0])
    root = {}
    def insert(v):
        node = root
        for i in range(31, -1, -1):
            b = (v >> i) & 1
            node = node.setdefault(b, {})
    def query(v):
        node = root
        if not node: return -1
        x = 0
        for i in range(31, -1, -1):
            b = (v >> i) & 1
            want = 1 - b
            if want in node:
                x |= (1 << i)
                node = node[want]
            else:
                node = node[b]
        return x
    ans = [0] * len(queries)
    j = 0
    for m, x, idx in indexed:
        while j < len(nums) and nums[j] <= m:
            insert(nums[j]); j += 1
        ans[idx] = query(x) if j > 0 else -1
    return ans
''',
            "complexity": "Time O((n + q) log + (n + q) · 32).",
        },
        "deep_concept": "Offline query processing is a powerful pattern when queries can be reordered.",
        "confusion_notes": [],
        "summary": "Sort queries by m; sweep array into trie up to m; greedy XOR query.",
    },
]
