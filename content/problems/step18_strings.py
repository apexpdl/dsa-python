"""Step 18 — Advanced String Algorithms (4 problems).

Z algorithm, KMP, Rabin-Karp, and shortest palindrome (KMP application).
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
        "id": "z-algorithm",
        "title": "Z Algorithm — Pattern Matching",
        "step_id": 18,
        "lecture_id": 1,
        "difficulty": "hard",
        "tags": ["strings", "z-algorithm"],
        "what_this_teaches": "Compute z[i] = length of the longest substring starting at i that matches a prefix of s. Linear time.",
        "pattern": "Z-array construction.",
        "prerequisite_lessons": [],
        "prerequisite_problems": [],
        "next_problems": ["kmp-algorithm", "rabin-karp"],
        "resources": [
            {"label": "CP-Algorithms — Z function", "url": "https://cp-algorithms.com/string/z-function.html"},
            _SHEET,
        ],
        "understanding": r'''
The **Z-array** of a string s satisfies: `z[i]` = length of the longest
substring starting at i that matches a prefix of s. By convention,
z[0] = len(s) (or sometimes 0).

**Use:** to find pattern p in text t, concatenate `p + '$' + t` (with
some separator) and compute Z. Wherever z[i] = len(p), there's a match
starting at i - len(p) - 1.
''',
        "brute_force": {
            "explanation": "Naive matching is O(n·m). Z is O(n + m).",
            "code": "",
            "complexity": "—",
        },
        "thought_process": r'''
Maintain a 'z-box' [L, R] = the rightmost prefix-match found so far.
For each i:
- If i > R, compute z[i] from scratch.
- Else, copy z[i - L] but bounded by R - i + 1.
- Then extend if possible.
- Update L, R if the match extended past R.
''',
        "optimized": {
            "explanation": "Z function implementation.",
            "code": r'''
def z_function(s):
    n = len(s)
    z = [0] * n
    z[0] = n
    L = R = 0
    for i in range(1, n):
        if i < R:
            z[i] = min(R - i, z[i - L])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > R:
            L, R = i, i + z[i]
    return z
''',
            "complexity": "Time O(n).",
        },
        "deep_concept": "The amortized argument: R only moves forward, so the total work of inner while-loops is bounded by O(n).",
        "confusion_notes": [],
        "summary": "Maintain a z-box [L, R]; copy from a smaller already-computed prefix-match, then extend.",
    },
    {
        "id": "kmp-algorithm",
        "title": "KMP — Knuth-Morris-Pratt",
        "step_id": 18,
        "lecture_id": 1,
        "difficulty": "hard",
        "tags": ["strings", "kmp"],
        "what_this_teaches": "Build the LPS (longest proper prefix that is also a suffix) array; use it to skip without re-checking.",
        "pattern": "KMP failure function.",
        "prerequisite_lessons": [],
        "prerequisite_problems": [],
        "next_problems": ["shortest-palindrome"],
        "resources": [
            {"label": "Wikipedia — KMP algorithm", "url": "https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm"},
            _SHEET,
        ],
        "understanding": r'''
KMP finds all occurrences of pattern P in text T in O(n + m).

**Step 1: build the LPS (longest proper prefix-suffix) array.** For
pattern P, lps[i] = the longest *proper* prefix of P[0..i] that is also
a suffix of P[0..i].

**Step 2: scan T with two pointers.** When chars match, advance both.
On mismatch, fall back using lps; never re-check chars already matched.
''',
        "brute_force": {
            "explanation": "Naive O(n·m).",
            "code": "",
            "complexity": "—",
        },
        "thought_process": "—",
        "optimized": {
            "explanation": "LPS + match scan.",
            "code": r'''
def kmp_search(text, pattern):
    if not pattern: return []
    m = len(pattern)
    lps = [0] * m
    k = 0
    for i in range(1, m):
        while k > 0 and pattern[i] != pattern[k]:
            k = lps[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
        lps[i] = k
    out = []
    j = 0
    for i, c in enumerate(text):
        while j > 0 and c != pattern[j]:
            j = lps[j - 1]
        if c == pattern[j]:
            j += 1
        if j == m:
            out.append(i - m + 1)
            j = lps[j - 1]
    return out
''',
            "complexity": "Time O(n + m).",
        },
        "deep_concept": "The LPS array captures the *self-similarity* of the pattern. When matching fails at pattern[j], we know that the last lps[j-1] chars of what we've matched in text *already* match a prefix of pattern — so we can skip ahead without re-checking.",
        "confusion_notes": [],
        "summary": "Build LPS; scan with fallback via LPS on mismatch. O(n + m).",
    },
    {
        "id": "rabin-karp",
        "title": "Rabin-Karp — Rolling Hash Pattern Matching",
        "step_id": 18,
        "lecture_id": 1,
        "difficulty": "hard",
        "tags": ["strings", "hashing", "rolling-hash"],
        "what_this_teaches": "Rolling hash compares strings in O(1) per shift, finding matches in average O(n + m).",
        "pattern": "Rolling hash.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["kmp-algorithm"],
        "next_problems": ["shortest-palindrome"],
        "resources": [
            {"label": "Wikipedia — Rabin-Karp", "url": "https://en.wikipedia.org/wiki/Rabin%E2%80%93Karp_algorithm"},
            _SHEET,
        ],
        "understanding": r'''
Hash the pattern in O(m). Compute a rolling hash of the text and
compare to the pattern's hash. If they match, verify char-by-char to
avoid hash collisions.

Average O(n + m); worst case O(n · m) if many collisions.
''',
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Use a polynomial hash. Choose base = 256 (or 31), modulus = large prime.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def rabin_karp(text, pattern):
    n, m = len(text), len(pattern)
    if m > n: return []
    base = 256
    mod = (1 << 61) - 1
    high = pow(base, m - 1, mod)
    h_pat = 0
    h_txt = 0
    for i in range(m):
        h_pat = (h_pat * base + ord(pattern[i])) % mod
        h_txt = (h_txt * base + ord(text[i])) % mod
    out = []
    for i in range(n - m + 1):
        if h_pat == h_txt and text[i:i+m] == pattern:
            out.append(i)
        if i + m < n:
            h_txt = ((h_txt - ord(text[i]) * high) * base + ord(text[i + m])) % mod
            h_txt %= mod
    return out
''',
            "complexity": "Average O(n + m); worst O(n · m).",
        },
        "deep_concept": "Rolling hashes shine in multi-pattern matching: hash each candidate once, compare to a set of pattern hashes.",
        "confusion_notes": [],
        "summary": "Polynomial rolling hash; compare to pattern's hash; verify on match.",
    },
    {
        "id": "shortest-palindrome",
        "title": "Shortest Palindrome",
        "step_id": 18,
        "lecture_id": 1,
        "difficulty": "hard",
        "tags": ["strings", "kmp", "palindrome"],
        "what_this_teaches": "Use KMP on `s + '#' + reverse(s)` to find the longest palindromic prefix.",
        "pattern": "KMP application.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["kmp-algorithm"],
        "next_problems": [],
        "resources": [
            _lc(214, "shortest-palindrome"),
            _SHEET,
        ],
        "understanding": "Convert s to a palindrome by prepending characters. Return the shortest palindrome.",
        "brute_force": {"explanation": "—", "code": "", "complexity": "—"},
        "thought_process": "Let rev = reverse(s). The shortest palindrome = (rev's chars not in longest palindromic prefix of s) + s. To find that prefix length, compute LPS of `s + '#' + rev` — the final LPS value gives the answer.",
        "optimized": {
            "explanation": "—",
            "code": r'''
def shortest_palindrome(s):
    rev = s[::-1]
    combined = s + '#' + rev
    m = len(combined)
    lps = [0] * m
    k = 0
    for i in range(1, m):
        while k > 0 and combined[i] != combined[k]:
            k = lps[k - 1]
        if combined[i] == combined[k]:
            k += 1
        lps[i] = k
    L = lps[-1]              # longest palindromic prefix of s
    return rev[:len(s) - L] + s
''',
            "complexity": "Time O(n).",
        },
        "deep_concept": "KMP isn't just for matching — its LPS array has many other uses (period finding, palindromes, longest common prefix-suffix).",
        "confusion_notes": [],
        "summary": "Combine s + '#' + reverse(s); KMP's final LPS = longest palindromic prefix; prepend the missing chars.",
    },
]
