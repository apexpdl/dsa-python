"""Step 5 extras — remaining string problems.

Lecture 1 (Easy): remove-outer-parentheses, largest-odd-number,
longest-common-prefix, rotation-of-string.

Lecture 2 (Medium): sort-characters-by-frequency, max-nesting-depth,
roman-to-integer, integer-to-roman, atoi, substrings-k-distinct,
longest-palindromic-substring, beauty-of-substrings.
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
        "id": "remove-outer-parentheses",
        "title": "Remove Outermost Parentheses",
        "step_id": 5,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["strings", "stack"],
        "what_this_teaches": "Tracking nesting depth with a counter rather than a stack.",
        "pattern": "Counter-based depth; emit when depth > 0 (with timing).",
        "prerequisite_lessons": ["strings", "stacks"],
        "prerequisite_problems": ["balanced-parentheses"],
        "next_problems": ["max-nesting-depth"],
        "resources": [_SHEET, _lc(1021, "remove-outermost-parentheses")],
        "understanding": r'''
A valid parentheses string decomposes into "primitive" balanced
parts. For `(()())(())(()(()))` the primitives are `(()())`,
`(())`, and `(()(()))`. The problem asks: remove the outermost
pair of each primitive, then concatenate.

Result for the example: `()()()()(())`.

**Algorithm**: walk the string with a depth counter. The
outermost `(` is when depth is 0 before incrementing; the
outermost `)` is when depth is 0 after decrementing. Skip those;
keep everything else.
''',
        "brute_force": {
            "explanation": "Identify primitive boundaries and strip the outer pair.",
            "code": r'''def remove_outer_brute(s):
    result, depth, start = [], 0, 0
    for i, ch in enumerate(s):
        depth += 1 if ch == '(' else -1
        if depth == 0:
            result.append(s[start + 1:i])
            start = i + 1
    return ''.join(result)
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(n)*.",
        },
        "optimized": {
            "explanation": "Single pass with a depth counter; emit non-outermost characters.",
            "code": r'''def remove_outer_parens(s: str) -> str:
    result = []
    depth = 0
    for ch in s:
        if ch == '(':
            # Emit only if not at depth 0 (i.e., this is NOT an outermost opener).
            if depth > 0:
                result.append(ch)
            depth += 1
        else:
            depth -= 1
            # Emit only if depth is still > 0 (i.e., NOT an outermost closer).
            if depth > 0:
                result.append(ch)
    return ''.join(result)
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(n)* for output.",
        },
        "thought_process": "Outermost brackets are those at depth transition 0↔1. A counter is enough; no stack needed.",
        "deep_concept": "When only depth matters (not which kind of bracket), a counter is enough.",
        "confusion_notes": [
            {"question": "Why check depth > 0 before incrementing for '(' but after decrementing for ')'?",
             "answer": "Symmetry. The outermost `(` happens at the transition from 0 to 1 (depth=0 before increment). The outermost `)` happens at the transition from 1 to 0 (depth=0 after decrement). Both checks correctly skip the outermost brackets."},
        ],
        "summary": "**Pattern**: counter-based depth tracking; emit non-outermost characters.",
    },
    {
        "id": "largest-odd-number",
        "title": "Largest Odd Number in a String",
        "step_id": 5,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["strings"],
        "what_this_teaches": "A number is odd iff its last digit is odd. So the largest odd substring is the longest prefix ending in an odd digit.",
        "pattern": "Right-to-left scan for the first odd digit; truncate.",
        "prerequisite_lessons": ["strings"],
        "prerequisite_problems": [],
        "next_problems": ["roman-to-integer"],
        "resources": [_SHEET, _lc(1903, "largest-odd-number-in-string")],
        "understanding": r'''
Given a numeric string, return the largest substring representing
an odd integer. If none exists, return `""`.

Key insight: a number is odd iff its **last digit** is odd. So
the largest odd-valued substring is the longest prefix of the
input ending in an odd digit.

Walk right-to-left for the first odd digit and truncate.
''',
        "brute_force": {
            "explanation": "Try every substring.",
            "code": r'''def largest_odd_brute(num):
    best = ""
    for i in range(len(num)):
        for j in range(i + 1, len(num) + 1):
            sub = num[i:j]
            if int(sub) % 2 == 1 and (best == "" or int(sub) > int(best)):
                best = sub
    return best
''',
            "complexity": "**Time**: *O(n³)*. **Space**: *O(n)*.",
        },
        "optimized": {
            "explanation": "Right-to-left scan.",
            "code": r'''def largest_odd_number(num: str) -> str:
    # Walk right to left, looking for the first odd digit.
    for i in range(len(num) - 1, -1, -1):
        if int(num[i]) % 2 == 1:
            # The longest odd-valued substring ends here.
            return num[:i + 1]
    return ""
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "thought_process": "Odd-ness depends only on the last digit. The 'largest' is the longest prefix ending in an odd digit.",
        "deep_concept": "Exploit the structure of decimal representation to collapse a search.",
        "confusion_notes": [
            {"question": "Why is longest = largest?",
             "answer": "Without leading zeros, longer numeric strings always represent larger values. So among all odd substrings, the longest prefix is the largest."},
        ],
        "summary": "**Pattern**: scan right-to-left for the first satisfying digit; return the prefix.",
    },
    {
        "id": "longest-common-prefix",
        "title": "Longest Common Prefix",
        "step_id": 5,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["strings"],
        "what_this_teaches": "Vertical scanning across multiple strings.",
        "pattern": "Compare character-by-character across all strings.",
        "prerequisite_lessons": ["strings"],
        "prerequisite_problems": [],
        "next_problems": ["trie-impl-i"],
        "resources": [_SHEET, _lc(14, "longest-common-prefix")],
        "understanding": r'''
Find the longest common prefix shared by all strings. Return
`""` if no common prefix.

`["flower", "flow", "flight"]` → `"fl"`.

Vertical scanning: for each character position, compare across
all strings; stop on first mismatch.
''',
        "brute_force": {
            "explanation": "Horizontal scanning — shrink a candidate prefix.",
            "code": r'''def lcp_horizontal(strs):
    if not strs:
        return ""
    prefix = strs[0]
    for s in strs[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix
''',
            "complexity": "**Time**: *O(S)*. **Space**: *O(1)*.",
        },
        "optimized": {
            "explanation": "Vertical scan: for each position, compare across all strings.",
            "code": r'''def longest_common_prefix(strs: list[str]) -> str:
    if not strs:
        return ""
    # Iterate character positions of the first string.
    for i in range(len(strs[0])):
        ch = strs[0][i]
        # Compare with every other string at this position.
        for s in strs[1:]:
            # If s is too short or has a different character, we've found the boundary.
            if i >= len(s) or s[i] != ch:
                return strs[0][:i]
    return strs[0]
''',
            "complexity": "**Time**: *O(S)*. **Space**: *O(1)*.",
        },
        "thought_process": "Walk character positions across all strings; stop when any differs or runs out.",
        "deep_concept": "The vertical-scan pattern works whenever you compare aligned sequences.",
        "confusion_notes": [
            {"question": "Empty string in input?",
             "answer": "Vertical scan returns `\"\"` immediately because the empty string is too short — correct, an empty input forces the LCP to be empty."},
        ],
        "summary": "**Pattern**: vertical scan; stop on first mismatch.",
    },
    {
        "id": "rotation-of-string",
        "title": "Check if One String is a Rotation of Another",
        "step_id": 5,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["strings"],
        "what_this_teaches": "The 'concatenate with itself' trick: rotations of S are substrings of S+S.",
        "pattern": "`len(a) == len(b) and b in (a + a)`.",
        "prerequisite_lessons": ["strings"],
        "prerequisite_problems": [],
        "next_problems": ["isomorphic-strings"],
        "resources": [_SHEET, _lc(796, "rotate-string")],
        "understanding": r'''
Two strings are rotations iff one appears as a substring of the
other concatenated with itself.

`is_rotation("abcde", "cdeab")` = True. `"abcde" + "abcde" =
"abcdeabcde"` contains `"cdeab"` as a substring.
''',
        "brute_force": {
            "explanation": "Try every rotation.",
            "code": r'''def is_rotation_brute(a, b):
    if len(a) != len(b):
        return False
    return any(a[i:] + a[:i] == b for i in range(len(a)))
''',
            "complexity": "**Time**: *O(n²)*. **Space**: *O(n)*.",
        },
        "optimized": {
            "explanation": "Use the a+a trick.",
            "code": r'''def is_rotation(a: str, b: str) -> bool:
    # Same length is necessary.
    if len(a) != len(b):
        return False
    # Every rotation of a is a substring of a + a.
    return b in (a + a)
''',
            "complexity": "**Time**: *O(n * m)* with naive search; *O(n + m)* with KMP.",
        },
        "thought_process": "Recognize that all length-n rotations are slices of a+a.",
        "deep_concept": "The S+S trick generalizes to cyclic shift problems and circular arrays.",
        "confusion_notes": [
            {"question": "Why the length check?",
             "answer": "Without it, b could be a non-rotation substring of a+a. Length check rules this out."},
        ],
        "summary": "**Pattern**: rotations of S = substrings of S+S of length |S|.",
    },
    {
        "id": "sort-characters-by-frequency",
        "title": "Sort Characters by Frequency",
        "step_id": 5,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["strings", "hashing", "sorting"],
        "what_this_teaches": "Counter.most_common as a one-line solution.",
        "pattern": "Counter + sort by count descending + join.",
        "prerequisite_lessons": ["strings", "hashing"],
        "prerequisite_problems": ["count-frequencies"],
        "next_problems": ["top-k-frequent"],
        "resources": [_SHEET, _lc(451, "sort-characters-by-frequency")],
        "understanding": r'''
Sort the characters of a string by frequency descending. Ties
can be broken arbitrarily.

`"tree"` → `"eert"`.

Use `collections.Counter` and `.most_common()`.
''',
        "brute_force": {
            "explanation": "Manual counting and sort.",
            "code": r'''def freq_sort_manual(s):
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    pairs = sorted(counts.items(), key=lambda kv: -kv[1])
    return ''.join(ch * cnt for ch, cnt in pairs)
''',
            "complexity": "**Time**: *O(n log k)*. **Space**: *O(k + n)*.",
        },
        "optimized": {
            "explanation": "Counter.most_common.",
            "code": r'''from collections import Counter

def frequency_sort(s: str) -> str:
    # Counter builds the freq map; most_common sorts by count desc.
    # Emit each char count times.
    return ''.join(ch * cnt for ch, cnt in Counter(s).most_common())
''',
            "complexity": "**Time**: *O(n log k)*. **Space**: *O(k + n)*.",
        },
        "thought_process": "Counter handles counting and sorting in one call.",
        "deep_concept": "Knowing the stdlib saves hand-rolled sort.",
        "confusion_notes": [
            {"question": "Case-sensitive?",
             "answer": "Yes. Lowercase the input first if you want case-insensitive."},
        ],
        "summary": "**Pattern**: Counter.most_common + repeat-and-join.",
    },
    {
        "id": "max-nesting-depth",
        "title": "Maximum Nesting Depth of Parentheses",
        "step_id": 5,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["strings"],
        "what_this_teaches": "Depth-counter with running maximum.",
        "pattern": "Increment on '(', decrement on ')', track max.",
        "prerequisite_lessons": ["strings"],
        "prerequisite_problems": ["balanced-parentheses", "remove-outer-parentheses"],
        "next_problems": [],
        "resources": [_SHEET, _lc(1614, "maximum-nesting-depth-of-the-parentheses")],
        "understanding": r'''
Given a valid parenthesis string, return its maximum nesting
depth.

`"(1+(2*3)+((8)/4))+1"` → 3.
''',
        "brute_force": {"explanation": "Same as optimized.",
                        "code": "# Same as optimized.\n",
                        "complexity": "**Time**: *O(n)*. **Space**: *O(1)*."},
        "optimized": {
            "explanation": "Depth counter with running max.",
            "code": r'''def max_depth(s: str) -> int:
    depth = best = 0
    for ch in s:
        if ch == '(':
            depth += 1
            if depth > best:
                best = depth
        elif ch == ')':
            depth -= 1
    return best
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "thought_process": "Same depth-counter idea; track max instead of filtering.",
        "deep_concept": "Counters track depth; max-of-counter = deepest nesting.",
        "confusion_notes": [
            {"question": "What if unbalanced?",
             "answer": "Problem promises balanced input. For unbalanced, depth could go negative; add a guard if needed."},
        ],
        "summary": "**Pattern**: depth counter + running max.",
    },
    {
        "id": "roman-to-integer",
        "title": "Roman to Integer",
        "step_id": 5,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["strings", "math"],
        "what_this_teaches": "Subtractive notation: smaller digit before larger = subtraction.",
        "pattern": "Walk left-to-right with one-step look-ahead.",
        "prerequisite_lessons": ["strings"],
        "prerequisite_problems": [],
        "next_problems": ["integer-to-roman"],
        "resources": [_SHEET, _lc(13, "roman-to-integer")],
        "understanding": r'''
Convert a Roman numeral to an integer. Use subtractive notation:
`IV = 4, IX = 9, XL = 40, XC = 90, CD = 400, CM = 900`.

Walk left-to-right with look-ahead.
''',
        "brute_force": {"explanation": "Same as optimized.", "code": "# Same.\n", "complexity": "**Time**: *O(n)*."},
        "optimized": {
            "explanation": "Look-ahead to decide subtract or add.",
            "code": r'''def roman_to_int(s: str) -> int:
    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50,
              'C': 100, 'D': 500, 'M': 1000}
    total = 0
    for i in range(len(s)):
        # If current < next, this is a subtractive pair.
        if i + 1 < len(s) and values[s[i]] < values[s[i + 1]]:
            total -= values[s[i]]
        else:
            total += values[s[i]]
    return total
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "thought_process": "Subtractive only when smaller digit precedes larger. One look-ahead is enough.",
        "deep_concept": "Left-to-right parsing with one-step look-ahead handles context-sensitive notation.",
        "confusion_notes": [
            {"question": "Right-to-left works too?",
             "answer": "Yes — add values; subtract when current < previous. Same algorithm, mirrored direction."},
        ],
        "summary": "**Pattern**: walk + look-ahead for subtractive notation.",
    },
    {
        "id": "integer-to-roman",
        "title": "Integer to Roman",
        "step_id": 5,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["strings", "math"],
        "what_this_teaches": "Greedy with denomination list including subtractive forms.",
        "pattern": "Walk values largest-to-smallest; emit symbol while value fits.",
        "prerequisite_lessons": ["strings"],
        "prerequisite_problems": ["roman-to-integer"],
        "next_problems": [],
        "resources": [_SHEET, _lc(12, "integer-to-roman")],
        "understanding": r'''
Convert 1..3999 to Roman. Use the denomination list including
subtractive forms (CM, CD, XC, XL, IX, IV).

Example: 1994 → MCMXCIV.
''',
        "brute_force": {"explanation": "Same greedy.", "code": "# Same.\n", "complexity": "**Time**: *O(1)*."},
        "optimized": {
            "explanation": "Greedy with sorted denominations.",
            "code": r'''def int_to_roman(num: int) -> str:
    pairs = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
             (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
             (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
    result = []
    for value, symbol in pairs:
        while num >= value:
            result.append(symbol)
            num -= value
    return ''.join(result)
''',
            "complexity": "**Time**: *O(1)*. **Space**: *O(1)*.",
        },
        "thought_process": "Greedy works because the denomination list (including subtractive pairs) is designed for it.",
        "deep_concept": "The 'canonical greedy' pattern: when denominations are sufficient, greedy is optimal.",
        "confusion_notes": [
            {"question": "Why include CM, CD, etc. explicitly?",
             "answer": "Without them, greedy emits DCCCC instead of CM. Including subtractive forms gives canonical Roman."},
        ],
        "summary": "**Pattern**: greedy subtraction with denomination list.",
    },
    {
        "id": "atoi",
        "title": "String to Integer (atoi)",
        "step_id": 5,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["strings", "parsing"],
        "what_this_teaches": "State-machine parsing: whitespace, sign, digits, clamp.",
        "pattern": "Sequential phases: skip ws → read sign → accumulate digits → clamp.",
        "prerequisite_lessons": ["strings"],
        "prerequisite_problems": ["reverse-number"],
        "next_problems": ["atoi-recursive"],
        "resources": [_SHEET, _lc(8, "string-to-integer-atoi")],
        "understanding": r'''
Convert a string to a 32-bit signed integer with rules: skip
leading whitespace, optional sign, read digits, clamp to int32
range, return 0 on invalid/empty.
''',
        "brute_force": {"explanation": "Same.", "code": "# Same.\n", "complexity": "**Time**: *O(n)*."},
        "optimized": {
            "explanation": "State-machine.",
            "code": r'''def my_atoi(s: str) -> int:
    INT_MAX, INT_MIN = 2**31 - 1, -2**31
    i, n = 0, len(s)
    # Skip leading whitespace.
    while i < n and s[i] == ' ':
        i += 1
    if i == n:
        return 0
    # Optional sign.
    sign = 1
    if s[i] == '-':
        sign = -1
        i += 1
    elif s[i] == '+':
        i += 1
    # Accumulate digits.
    result = 0
    while i < n and s[i].isdigit():
        result = result * 10 + int(s[i])
        i += 1
        # Clamp early to avoid integer overflow in typed languages.
        if sign * result > INT_MAX:
            return INT_MAX
        if sign * result < INT_MIN:
            return INT_MIN
    return sign * result
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "thought_process": "Sequential phases handle each parsing concern. Clamp during accumulation for portability.",
        "deep_concept": "State-machine discipline matters for any parser.",
        "confusion_notes": [
            {"question": "Why clamp during accumulation?",
             "answer": "In C++/Java with 32-bit int, `result * 10` can overflow. Python doesn't overflow, but the discipline is good practice."},
        ],
        "summary": "**Pattern**: state-machine parsing for atoi.",
    },
    {
        "id": "substrings-k-distinct",
        "title": "Count Substrings with Exactly K Distinct Characters",
        "step_id": 5,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["strings", "sliding-window", "hashing"],
        "what_this_teaches": "The 'at most K minus at most K-1' subtraction trick.",
        "pattern": "Sliding window 'at most K distinct'; subtract.",
        "prerequisite_lessons": ["strings", "sliding-window", "hashing"],
        "prerequisite_problems": ["longest-substring-no-repeat"],
        "next_problems": ["subarrays-k-different-integers"],
        "resources": [_SHEET, _lc(992, "subarrays-with-k-different-integers")],
        "understanding": r'''
Count substrings with exactly k distinct characters.

Direct sliding window for 'exactly K' is awkward. The trick:
`count(exactly K) = count(at most K) - count(at most K-1)`.
''',
        "brute_force": {
            "explanation": "Try every substring.",
            "code": r'''def k_distinct_brute(s, k):
    count = 0
    for i in range(len(s)):
        chars = set()
        for j in range(i, len(s)):
            chars.add(s[j])
            if len(chars) == k:
                count += 1
            elif len(chars) > k:
                break
    return count
''',
            "complexity": "**Time**: *O(n²)*. **Space**: *O(k)*.",
        },
        "optimized": {
            "explanation": "at_most(K) - at_most(K-1).",
            "code": r'''from collections import defaultdict

def count_at_most_k(s: str, k: int) -> int:
    if k < 0:
        return 0
    count = defaultdict(int)
    left = total = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        while len(count) > k:
            count[s[left]] -= 1
            if count[s[left]] == 0:
                del count[s[left]]
            left += 1
        # Every substring ending at right with start in [left, right]
        # has at most k distinct chars; that's right - left + 1.
        total += right - left + 1
    return total


def substrings_with_k_distinct(s: str, k: int) -> int:
    return count_at_most_k(s, k) - count_at_most_k(s, k - 1)
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(k)*.",
        },
        "thought_process": "Two sliding windows; subtract. Each counts 'at most K' which is sliding-window-friendly.",
        "deep_concept": "The at-most-K trick is the canonical way to handle 'exactly K' with sliding window.",
        "confusion_notes": [
            {"question": "Why right - left + 1 instead of 1?",
             "answer": "Every substring ending at right with start in [left, right] satisfies the constraint. That's right - left + 1 substrings counted at this step."},
        ],
        "summary": "**Pattern**: 'exactly K' = 'at most K' minus 'at most K-1'.",
    },
    {
        "id": "longest-palindromic-substring",
        "title": "Longest Palindromic Substring",
        "step_id": 5,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["strings", "palindrome", "expand-around-center"],
        "what_this_teaches": "Expand around each of the 2n-1 centers.",
        "pattern": "For each center (single char or pair), expand outward while characters match.",
        "prerequisite_lessons": ["strings"],
        "prerequisite_problems": ["check-string-palindrome-recursion"],
        "next_problems": ["longest-palindromic-subseq", "shortest-palindrome"],
        "resources": [_SHEET, _lc(5, "longest-palindromic-substring")],
        "understanding": r'''
Find the longest palindromic substring.

`"babad"` → `"bab"` or `"aba"`.
`"cbbd"` → `"bb"`.

A palindrome has a center — either a single character (odd
length) or between two characters (even length). There are
`2n - 1` possible centers. For each, expand outward while
characters match. Track the longest.
''',
        "brute_force": {
            "explanation": "Try every substring; check palindrome.",
            "code": r'''def longest_palindrome_brute(s):
    n = len(s)
    best = ""
    for i in range(n):
        for j in range(i + 1, n + 1):
            sub = s[i:j]
            if sub == sub[::-1] and len(sub) > len(best):
                best = sub
    return best
''',
            "complexity": "**Time**: *O(n³)*. **Space**: *O(n)*.",
        },
        "optimized": {
            "explanation": "Expand around 2n-1 centers.",
            "code": r'''def longest_palindrome(s: str) -> str:
    def expand(left: int, right: int) -> tuple[int, int]:
        # Expand as long as both sides match.
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        # After loop, [left+1, right-1] is the palindrome.
        return left + 1, right - 1

    best_l = best_r = 0
    for i in range(len(s)):
        # Odd-length: center at i.
        l1, r1 = expand(i, i)
        # Even-length: center between i and i+1.
        l2, r2 = expand(i, i + 1)
        if r1 - l1 > best_r - best_l:
            best_l, best_r = l1, r1
        if r2 - l2 > best_r - best_l:
            best_l, best_r = l2, r2
    return s[best_l:best_r + 1]
''',
            "complexity": "**Time**: *O(n²)*. **Space**: *O(1)*.",
        },
        "thought_process": "Each potential center generates a palindrome. Expand and track the longest.",
        "deep_concept": "Manacher's algorithm achieves *O(n)* using more sophisticated bookkeeping; rarely worth in interviews.",
        "confusion_notes": [
            {"question": "Why 2n-1 centers?",
             "answer": "n centers at characters (odd-length) + n-1 centers between adjacent characters (even-length) = 2n - 1."},
        ],
        "summary": "**Pattern**: expand around each center; track the longest.",
    },
    {
        "id": "beauty-of-substrings",
        "title": "Sum of Beauty of All Substrings",
        "step_id": 5,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["strings", "hashing"],
        "what_this_teaches": "Incremental frequency tracking — extend a substring one character at a time, updating freqs in O(1).",
        "pattern": "Outer loop: start index. Inner loop: extend, update freq[26], compute max-min.",
        "prerequisite_lessons": ["strings", "hashing"],
        "prerequisite_problems": ["sort-characters-by-frequency"],
        "next_problems": [],
        "resources": [_SHEET, _lc(1781, "sum-of-beauty-of-all-substrings")],
        "understanding": r'''
The **beauty** of a string is `max_frequency - min_frequency`
considering only characters that appear.

Compute the sum of beauty across every substring.

For each starting index, walk the suffix, updating a fixed-size
freq[26] array. Compute max - min of nonzero counts each step.
''',
        "brute_force": {
            "explanation": "Build a Counter for each substring.",
            "code": r'''from collections import Counter

def beauty_brute(s):
    total = 0
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            c = Counter(s[i:j])
            total += max(c.values()) - min(c.values())
    return total
''',
            "complexity": "**Time**: *O(n³)*. **Space**: *O(n)*.",
        },
        "optimized": {
            "explanation": "Incremental freq[26] update.",
            "code": r'''def beauty_sum(s: str) -> int:
    total = 0
    for i in range(len(s)):
        # Reset freq array for this starting index.
        freq = [0] * 26
        for j in range(i, len(s)):
            freq[ord(s[j]) - ord('a')] += 1
            # max over all 26 counts; min over only the nonzero ones.
            mx = max(freq)
            mn = min(f for f in freq if f > 0)
            total += mx - mn
    return total
''',
            "complexity": "**Time**: *O(n² * 26)*. **Space**: *O(1)*.",
        },
        "thought_process": "Extending the substring by one char only changes one count. Maintain incrementally.",
        "deep_concept": "Substring problems benefit from extending an existing data structure rather than rebuilding.",
        "confusion_notes": [
            {"question": "Why filter nonzero in min?",
             "answer": "min over a 26-length array would always be 0 (most letters absent). We want the minimum freq among letters that actually appear."},
        ],
        "summary": "**Pattern**: incremental freq[26] + max - min of nonzero counts.",
    },
]
