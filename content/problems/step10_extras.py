"""Step 10 extras — Sliding Window & Two Pointer (10 problems).

Each problem is taught both as a *concept* and as a *solution*. We always
include: brute force narrative, transition to optimal, line-by-line code,
worked example, complexity, deep-concept section, beginner confusion
notes, summary, and embedded LeetCode + Striver sheet links.
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
    # 1) Max Consecutive Ones III
    # ------------------------------------------------------------------
    {
        "id": "max-consecutive-ones-iii",
        "title": "Max Consecutive Ones III",
        "step_id": 10,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["sliding-window", "binary-array"],
        "what_this_teaches": "The 'at most K' template — a window that may contain a bounded number of an 'unwanted' element. Slide right, shrink left only when the unwanted count exceeds K.",
        "pattern": "Variable-size sliding window with a constraint on number of zeros.",
        "prerequisite_lessons": ["sliding-window"],
        "prerequisite_problems": ["longest-substring-no-repeat"],
        "next_problems": ["fruit-into-baskets", "longest-repeating-replacement"],
        "resources": [
            _lc(1004, "max-consecutive-ones-iii"),
            _SHEET,
        ],
        "understanding": r'''
You are given a binary array `nums` (only 0s and 1s) and an integer `k`.
You are allowed to flip **at most** `k` zeros to ones. Return the length
of the longest contiguous subarray of `1`s you can obtain after the flips.

**What changes vs. counting consecutive ones?** Here you are *allowed*
to absorb up to `k` zeros into a streak of ones. So the question becomes:
*what is the longest window that contains at most `k` zeros?* Every such
window can be turned into all-ones by flipping the zeros it contains.

**Why is this a sliding window problem?** Because the answer is an
interval `[L, R]` and as `R` grows the count of zeros grows monotonically;
when the window has too many zeros, you push `L` rightward to shed zeros
until it fits the budget again. Once an `L` is ruled out for a given `R`,
it is ruled out for every larger `R` — so each index enters and leaves
the window at most once → O(n).

**Example:** `nums = [1,1,1,0,0,0,1,1,1,1,0]`, `k = 2`.
- Best window is `[1,1,1,0,0,1,1,1,1]` from index 5..9? Let's count it
  carefully: indices 2..9 give `[1,0,0,0,1,1,1,1]` which contains three
  zeros → too many. Indices 5..10 give `[0,1,1,1,1,0]` which has two
  zeros → length 6. Indices 3..9 = `[0,0,0,1,1,1,1]` has three zeros →
  too many. So answer = 6.
''',
        "brute_force": {
            "explanation": r'''
Try every subarray `(i, j)` and count zeros. If zeros ≤ k, update the
best length with `j - i + 1`. There are O(n²) subarrays and each count
is O(1) if you precompute prefix sums of zeros. So O(n²) overall — fine
on paper, but we want O(n).
''',
            "code": r'''
def longest_ones_brute(nums, k):
    n = len(nums)
    # prefix[i] = number of zeros in nums[0..i-1]
    prefix = [0] * (n + 1)
    for i, v in enumerate(nums):
        prefix[i + 1] = prefix[i] + (1 if v == 0 else 0)
    best = 0
    for i in range(n):
        for j in range(i, n):
            zeros = prefix[j + 1] - prefix[i]
            if zeros <= k:
                best = max(best, j - i + 1)
    return best
''',
            "complexity": "Time O(n²), space O(n) for the prefix array.",
        },
        "thought_process": r'''
The brute force counts zeros for *every* `(i, j)` even though increasing
`j` only adds to the zero count and increasing `i` only removes from it.
That is the signature of a sliding window: monotonic add/remove.

We will keep a window `[L, R]` and a single counter `zeros`. Push `R`
forward one step at a time. If `nums[R] == 0`, increment `zeros`. While
`zeros > k`, advance `L` (and decrement `zeros` when we leave a zero
behind). After fixing the window for `R`, the window length `R - L + 1`
is a valid candidate for the answer.
''',
        "optimized": {
            "explanation": r'''
Single linear scan. `L` only moves forward; `R` walks the array. The
invariant is: the window `[L, R]` always contains ≤ k zeros after the
inner `while`. We record the maximum window length seen.
''',
            "code": r'''
def longest_ones(nums, k):
    L = 0           # left edge of the window
    zeros = 0       # number of zeros currently inside [L, R]
    best = 0        # best length seen so far

    for R in range(len(nums)):
        if nums[R] == 0:
            zeros += 1                # absorbing one more zero

        # shrink until the budget is respected
        while zeros > k:
            if nums[L] == 0:
                zeros -= 1            # dropping a zero we previously absorbed
            L += 1                    # slide left edge inward

        # window [L, R] is now valid → its length is a candidate
        best = max(best, R - L + 1)

    return best
''',
            "complexity": "Time O(n) — each index enters the window once and leaves at most once. Space O(1).",
        },
        "deep_concept": r'''
This is the canonical **'at most K' window**. Memorize the four lines:
*expand R, update counter, while invariant broken shrink L, record
answer.* You will use it for "at most K distinct" (Fruit Into Baskets,
K Distinct), "longest substring with K replacements", and many more.

A useful variant trick: *exactly K = atMost(K) - atMost(K - 1)*. Many
problems on this page (binary subarrays with sum, nice subarrays, K
different integers) hinge on that identity.
''',
        "confusion_notes": [
            {
                "question": "Why don't we ever move L backward?",
                "answer": "Because once `[L, R]` is too zero-heavy, no smaller L would help — the window would only become more zero-heavy. Moving L forward is the *only* way to reduce zeros without dropping R. Once L has passed an index, that index is permanently outside the current window and we never revisit it.",
            },
            {
                "question": "What if `k = 0`?",
                "answer": "Then `zeros > 0` triggers shrinking immediately, and we end up measuring runs of consecutive ones — exactly the simpler 'Max Consecutive Ones' problem. The same code handles it.",
            },
            {
                "question": "Could we instead try every left endpoint and binary search the right one?",
                "answer": "Yes, that gives O(n log n) and is a fine alternative pattern (binary-search-the-answer-on-window). But the two-pointer/sliding-window achieves O(n) with simpler code, which is why interviewers expect it.",
            },
        ],
        "summary": "Sliding window with a budget. Expand right, count violations, shrink left while violations exceed the budget, take the max length.",
    },

    # ------------------------------------------------------------------
    # 2) Fruit Into Baskets
    # ------------------------------------------------------------------
    {
        "id": "fruit-into-baskets",
        "title": "Fruit Into Baskets",
        "step_id": 10,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["sliding-window", "hash-map"],
        "what_this_teaches": "Window with at most 2 distinct elements — a specialization of the 'at most K distinct' template.",
        "pattern": "At most K distinct (K = 2) using a frequency map.",
        "prerequisite_lessons": ["sliding-window", "hashing"],
        "prerequisite_problems": ["max-consecutive-ones-iii"],
        "next_problems": ["longest-substring-k-distinct"],
        "resources": [
            _lc(904, "fruit-into-baskets"),
            _SHEET,
        ],
        "understanding": r'''
You are given an array `fruits` representing fruit types in a row of
trees. You have two baskets, each can hold one fruit *type* but
unlimited quantity. Starting from any tree you pick *exactly one* fruit
per tree and move right; you must stop when you encounter a third type
you cannot fit. Find the maximum total fruits you can pick.

Reframed: find the longest contiguous subarray that contains **at most
2 distinct values**. That length is the answer.

**Example:** `fruits = [1, 2, 3, 2, 2]` → best subarray is `[3, 2, 2]`
of length 3 (types {3, 2}).
''',
        "brute_force": {
            "explanation": r'''
For every starting index `i`, walk forward and keep a set of distinct
types. As soon as the set has 3 types, stop. Track the longest run.
O(n²) and quite intuitive — but unnecessary.
''',
            "code": r'''
def total_fruits_brute(fruits):
    n = len(fruits)
    best = 0
    for i in range(n):
        s = set()
        for j in range(i, n):
            s.add(fruits[j])
            if len(s) > 2:
                break
            best = max(best, j - i + 1)
    return best
''',
            "complexity": "Time O(n²), space O(1) (at most 3 elements in the set).",
        },
        "thought_process": r'''
The same monotonic property applies: extending the window can only add
types, never remove them. Once the window has 3 types we must shed
elements from the left until we are back to 2.

We keep a frequency map `count[fruit] = how many of this type are
currently in the window`. When `len(count) > 2`, we shrink from the left,
decrementing counts and *removing keys when their count hits zero*. The
moment `len(count)` is ≤ 2 again, we record the window length.
''',
        "optimized": {
            "explanation": r'''
Standard 'at most 2 distinct' template using a frequency dict. Each
index enters and leaves the window once.
''',
            "code": r'''
def total_fruits(fruits):
    from collections import defaultdict
    count = defaultdict(int)    # type -> frequency inside window
    L = 0
    best = 0

    for R, f in enumerate(fruits):
        count[f] += 1           # add fruits[R] to the window

        # shrink while we have more than 2 distinct types
        while len(count) > 2:
            count[fruits[L]] -= 1
            if count[fruits[L]] == 0:
                del count[fruits[L]]   # drop the key so len() is accurate
            L += 1

        best = max(best, R - L + 1)

    return best
''',
            "complexity": "Time O(n), space O(1) — the map holds at most 3 keys at the moment of violation.",
        },
        "deep_concept": r'''
A frequency map plus a `len(map)` check is the standard tool for the
"at most K distinct" family. Important detail: **delete keys when count
hits 0**, otherwise `len(map)` overcounts and the algorithm breaks.
''',
        "confusion_notes": [
            {
                "question": "Why use a `defaultdict(int)` and not a regular dict?",
                "answer": "It saves `count[f] = count.get(f, 0) + 1`. Same semantics, less code. A regular dict works fine too — just remember to initialize.",
            },
            {
                "question": "Could we do this with two variables tracking the two latest types?",
                "answer": "Yes, there is a clever O(n) version that maintains the two last seen types and the length of the current 'last type run'. It avoids a hash map entirely. But the dict version generalizes to K, so it is more useful to internalize.",
            },
        ],
        "summary": "Longest subarray with ≤ 2 distinct values. Frequency-map window: expand right, shrink left when types > 2, track length.",
    },

    # ------------------------------------------------------------------
    # 3) Longest Substring with K Distinct Characters
    # ------------------------------------------------------------------
    {
        "id": "longest-substring-k-distinct",
        "title": "Longest Substring with At Most K Distinct Characters",
        "step_id": 10,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["sliding-window", "hash-map", "strings"],
        "what_this_teaches": "Generalizes 'fruit into baskets' to any K. The exact same window template, parameterized.",
        "pattern": "At most K distinct with a frequency map.",
        "prerequisite_lessons": ["sliding-window", "hashing"],
        "prerequisite_problems": ["fruit-into-baskets"],
        "next_problems": ["subarrays-k-different-integers"],
        "resources": [
            {"label": "LeetCode 340 — Longest Substring with At Most K Distinct Characters", "url": "https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/"},
            _SHEET,
        ],
        "understanding": r'''
Given a string `s` and integer `k`, return the length of the longest
substring containing at most `k` distinct characters.

This is the *generalization* of Fruit Into Baskets. Replace "2" with
"k" in the template and we are done.

**Example:** `s = "eceba"`, `k = 2` → longest is `"ece"` of length 3.
''',
        "brute_force": {
            "explanation": r'''
Enumerate every substring with two indices and count distinct chars
using a set. O(n³) naive, O(n² · α) with a running set. We skip directly
to the optimal because the structure is identical to the previous
problem.
''',
            "code": r'''
def longest_k_distinct_brute(s, k):
    best = 0
    for i in range(len(s)):
        seen = set()
        for j in range(i, len(s)):
            seen.add(s[j])
            if len(seen) > k:
                break
            best = max(best, j - i + 1)
    return best
''',
            "complexity": "Time O(n²), space O(min(n, alphabet)).",
        },
        "thought_process": r'''
A sliding window with a frequency dict. Expand right, when the dict has
more than `k` keys shrink left and delete keys that hit zero.
''',
        "optimized": {
            "explanation": r'''
Frequency-map window. Identical shape to Fruit Into Baskets, with K
parameterized.
''',
            "code": r'''
def longest_k_distinct(s, k):
    if k == 0:
        return 0
    from collections import defaultdict
    count = defaultdict(int)
    L = 0
    best = 0

    for R, ch in enumerate(s):
        count[ch] += 1

        while len(count) > k:
            count[s[L]] -= 1
            if count[s[L]] == 0:
                del count[s[L]]
            L += 1

        best = max(best, R - L + 1)

    return best
''',
            "complexity": "Time O(n), space O(k).",
        },
        "deep_concept": r'''
Once you have a 'window with ≤ K of something' counter, half a dozen
problems collapse to the same pattern. Always two things to manage:
the *quantity that triggers shrinking* and the *quantity you maximize/
minimize*.
''',
        "confusion_notes": [
            {
                "question": "What if k is larger than the number of distinct chars in s?",
                "answer": "Then the window can hold the whole string and the answer is `len(s)`. The code handles this naturally — the while-loop never triggers.",
            },
            {
                "question": "Why must we delete keys when count drops to 0?",
                "answer": "Because `len(count)` is our distinct-count proxy. If we leave dead entries with value 0 in the dict, `len(count)` overestimates and we wrongly shrink. Always delete keys when their frequency falls to zero in this family of problems.",
            },
        ],
        "summary": "Generalized Fruit Into Baskets. Use a frequency map and shrink the window while the number of keys exceeds k.",
    },

    # ------------------------------------------------------------------
    # 4) Number of Substrings Containing All Three Characters
    # ------------------------------------------------------------------
    {
        "id": "substrings-containing-three",
        "title": "Number of Substrings Containing All Three Characters",
        "step_id": 10,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["sliding-window", "counting", "strings"],
        "what_this_teaches": "Counting valid windows. Once `[L, R]` is valid, every extension `[L, R'], R' ≥ R` is *also* valid — so we can multiply.",
        "pattern": "Two-pointer with counting of extensions.",
        "prerequisite_lessons": ["sliding-window"],
        "prerequisite_problems": ["longest-substring-k-distinct"],
        "next_problems": ["binary-subarrays-with-sum"],
        "resources": [
            _lc(1358, "number-of-substrings-containing-all-three-characters"),
            _SHEET,
        ],
        "understanding": r'''
Given a string `s` containing only `'a'`, `'b'`, `'c'`, return the number
of substrings that contain at least one of each character.

**Example:** `s = "abcabc"`. Every substring of length 3 starting at
some index that contains all three counts. Plus longer ones. The answer
is 10.

The clean observation is: for each left endpoint `L`, find the smallest
right endpoint `R` such that `s[L..R]` contains all three. Then *every*
right endpoint from `R` to `n-1` extends to a valid substring. That
contributes `n - R` substrings.
''',
        "brute_force": {
            "explanation": r'''
Enumerate all O(n²) substrings, check if each contains all three
characters using a set. O(n² · n) = O(n³) naive, O(n²) with running
counts.
''',
            "code": r'''
def count_substrings_brute(s):
    n = len(s)
    res = 0
    for i in range(n):
        seen = set()
        for j in range(i, n):
            seen.add(s[j])
            if len(seen) == 3:
                res += n - j     # every extension is valid
                break
    return res
''',
            "complexity": "Time O(n²) using the early break, O(1) extra.",
        },
        "thought_process": r'''
The trick: when `[L..R]` first contains all three characters, *every*
larger right endpoint `R, R+1, ..., n-1` still contains all three
(adding more chars can never remove a type). That's `n - R`
contributions for this L.

Now move `L` right by one, dropping `s[L]`'s count. We don't restart the
search from scratch — `R` is monotonic too. Both pointers walk forward,
each at most n times: O(n).
''',
        "optimized": {
            "explanation": r'''
Maintain counts of `'a'`, `'b'`, `'c'` in the current window `[L, R]`.
Expand `R` until all three counts are ≥ 1. Then *for this L*, every
right endpoint from `R` to `n-1` is valid → add `n - R` to the answer.
Then shrink `L` by one and repeat.

There is an even slicker formulation: for each position `i` of `s`, count
the number of substrings *ending at i* that contain all three. Track
`last_seen['a'], last_seen['b'], last_seen['c']`; the number of valid
left endpoints is `1 + min(last_seen[a], last_seen[b], last_seen[c])`.
''',
            "code": r'''
def count_substrings(s):
    last = {'a': -1, 'b': -1, 'c': -1}
    res = 0
    for i, ch in enumerate(s):
        last[ch] = i                                  # record latest position
        res += 1 + min(last['a'], last['b'], last['c'])
        # the +1 turns min == -1 into 0 (i.e., zero substrings until we've
        # seen all three for the first time)
    return res
''',
            "complexity": "Time O(n), space O(1).",
        },
        "deep_concept": r'''
The key insight — **once valid, all longer windows are valid** — recurs
in many counting-of-subarrays problems. Whenever the property is
"contains at least one of each X", containment is monotone: a superset
window is always still 'at least' as good.
''',
        "confusion_notes": [
            {
                "question": "Why `1 + min(...)`? Where does the +1 come from?",
                "answer": "We want the count of left endpoints L in [0, i] such that `s[L..i]` contains all three. The smallest left endpoint that works is `min(last['a'], last['b'], last['c'])`. The number of valid L from 0 to that smallest position (inclusive) is `min(...) + 1`. If any letter hasn't appeared yet, `min` is -1 and we add 0.",
            },
        ],
        "summary": "For each right endpoint, count valid left endpoints using the latest occurrences of a/b/c. Linear time.",
    },

    # ------------------------------------------------------------------
    # 5) Longest Repeating Character Replacement
    # ------------------------------------------------------------------
    {
        "id": "longest-repeating-replacement",
        "title": "Longest Repeating Character Replacement",
        "step_id": 10,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["sliding-window", "strings", "counting"],
        "what_this_teaches": "Sliding window with a clever invariant: track the *most-frequent* character. We can keep the window if (window_size - max_freq) ≤ K.",
        "pattern": "Window with a dominant-character invariant.",
        "prerequisite_lessons": ["sliding-window"],
        "prerequisite_problems": ["max-consecutive-ones-iii"],
        "next_problems": ["min-window-substring"],
        "resources": [
            _lc(424, "longest-repeating-character-replacement"),
            _SHEET,
        ],
        "understanding": r'''
You are given a string `s` and integer `k`. In one move you can change
any character of `s` to any other character. After at most `k` changes,
return the length of the longest substring containing the same letter.

**Reframed:** find the longest window such that we only need to change
`window_size − max_letter_frequency_in_window` characters. If that
value is ≤ k, the window is feasible.

**Example:** `s = "AABABBA"`, `k = 1`. Window `"ABAB"` has size 4 with
max freq 2 → need 2 changes, too many. Window `"AABA"` size 4 max freq
3 → need 1 change, feasible. Answer = 4.
''',
        "brute_force": {
            "explanation": r'''
For every substring, compute its character frequencies and check if
`length - max(freq) ≤ k`. O(n² · 26).
''',
            "code": r'''
def char_replacement_brute(s, k):
    best = 0
    for i in range(len(s)):
        freq = [0] * 26
        for j in range(i, len(s)):
            freq[ord(s[j]) - ord('A')] += 1
            if (j - i + 1) - max(freq) <= k:
                best = max(best, j - i + 1)
    return best
''',
            "complexity": "Time O(n² · 26), space O(26).",
        },
        "thought_process": r'''
The invariant we want is `window_size - max_freq ≤ k`. Track the window
with a frequency array `freq[26]` and a running `max_freq`.

Two subtle questions:
1. Do we need to *recompute* `max_freq` when we shrink from the left?
   No! And here's why: even if `max_freq` is now slightly stale (too
   high), our answer can only *grow*, not shrink. The reason is that the
   answer is monotone in `max_freq`: a window is feasible iff
   `R - L + 1 - max_freq ≤ k`. If we keep an outdated (larger) `max_freq`
   we may sometimes accept a window that has slightly lower actual
   `max_freq`, but the *length* of that window won't exceed the true
   answer because the real `max_freq` for the *current* window is at
   least as large only when it equals the recorded value. The proof is
   classic: lazy `max_freq` is enough because the *answer* we report is
   `R - L + 1` at the largest valid window, and that largest valid
   window has the correct `max_freq` recorded.
2. When does L move? Only when `R - L + 1 - max_freq > k`. Then we shed
   `s[L]` and advance L by one.
''',
        "optimized": {
            "explanation": r'''
One pass, frequency array of size 26, lazy `max_freq` updates.
''',
            "code": r'''
def character_replacement(s, k):
    freq = [0] * 26
    L = 0
    max_freq = 0
    best = 0

    for R in range(len(s)):
        idx = ord(s[R]) - ord('A')
        freq[idx] += 1
        max_freq = max(max_freq, freq[idx])

        # if more than k replacements are needed, shrink from the left
        if (R - L + 1) - max_freq > k:
            freq[ord(s[L]) - ord('A')] -= 1
            L += 1
            # NOTE: we deliberately don't recompute max_freq here

        best = max(best, R - L + 1)

    return best
''',
            "complexity": "Time O(n) — both L and R advance monotonically. Space O(26) = O(1).",
        },
        "deep_concept": r'''
**Lazy max-frequency:** a beautiful example of trading exactness for
speed. The "real" `max_freq` for the window may be lower after a left
shrink, but it can only mean the window we keep is *also* valid by a
stricter bound. The window *length* tracked is always ≤ the true answer,
and the moment a genuinely larger window appears, the lazy `max_freq`
catches up.
''',
        "confusion_notes": [
            {
                "question": "Wait, why is it correct to never recompute `max_freq` even when it should drop?",
                "answer": "Because the answer is `best = max(best, R - L + 1)`. Whenever `best` is updated with a strictly larger value, the *current* `max_freq` value must equal the real max_freq of the current window (we just incremented it from the latest character). So overestimates of `max_freq` never inflate `best`. The pointer L might lag a little, but the *length we record* is always feasible. Formal argument: the optimal window has a true `max_freq`; when the right end of that window passes through our scan, the recorded `max_freq` is ≥ the true value and L has advanced enough to make the window valid by that bound. So we record at least that length.",
            },
            {
                "question": "Why use `if` instead of `while` on the shrink?",
                "answer": "Because in one step we add exactly one character, so the window can become infeasible by at most one. A single left shrink restores feasibility (or keeps the window the same length, which is fine because we only need `best` to be a valid lower bound). It works to use `while` too, but `if` is enough and more idiomatic for this problem.",
            },
        ],
        "summary": "Window invariant: `length - max_freq ≤ k`. Maintain a 26-element count and a lazy max_freq; shrink from the left when the invariant breaks.",
    },

    # ------------------------------------------------------------------
    # 6) Binary Subarrays With Sum
    # ------------------------------------------------------------------
    {
        "id": "binary-subarrays-with-sum",
        "title": "Binary Subarrays With Sum",
        "step_id": 10,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["sliding-window", "prefix-sum", "counting"],
        "what_this_teaches": "The exactly-K = atMost(K) - atMost(K-1) trick.",
        "pattern": "Counting subarrays via two sliding-window queries.",
        "prerequisite_lessons": ["sliding-window", "prefix-sum"],
        "prerequisite_problems": ["max-consecutive-ones-iii"],
        "next_problems": ["nice-subarrays", "subarrays-k-different-integers"],
        "resources": [
            _lc(930, "binary-subarrays-with-sum"),
            _SHEET,
        ],
        "understanding": r'''
Given a binary array `nums` and integer `goal`, return the number of
subarrays whose sum equals exactly `goal`.

A direct sliding window for *exact* sum doesn't quite work because the
sum is not monotone when you shrink (e.g., zeros don't help). The clean
trick is:

> count(sum == goal) = count(sum ≤ goal) − count(sum ≤ goal − 1)

Each `atMost(target)` count is straightforward via sliding window: the
window's sum never exceeds `target`, and for each `R` the number of
subarrays ending at `R` with sum ≤ target is `R − L + 1` where `L` is
the leftmost valid left endpoint.

**Example:** `nums = [1, 0, 1, 0, 1]`, `goal = 2` → 4 subarrays.
''',
        "brute_force": {
            "explanation": r'''
Prefix sums + hash map: for each `i`, the number of `j` with
`prefix[i] − prefix[j] == goal` is `freq[prefix[i] − goal]`. O(n) time
with O(n) space.
''',
            "code": r'''
def num_subarrays_sum_brute(nums, goal):
    from collections import defaultdict
    freq = defaultdict(int)
    freq[0] = 1
    s = 0
    res = 0
    for v in nums:
        s += v
        res += freq[s - goal]
        freq[s] += 1
    return res
''',
            "complexity": "Time O(n), space O(n). Already optimal in time, but uses a hash map.",
        },
        "thought_process": r'''
The educational point here is the *atMost trick*. Build a helper
`atMost(target)` that returns the number of subarrays with sum ≤ target,
using a sliding window. Then exact answer = `atMost(goal) − atMost(goal − 1)`.
''',
        "optimized": {
            "explanation": r'''
Two sliding-window passes, both O(n). No hash map.
''',
            "code": r'''
def num_subarrays_with_sum(nums, goal):
    def at_most(t):
        if t < 0:
            return 0
        L = 0
        s = 0
        res = 0
        for R in range(len(nums)):
            s += nums[R]
            while s > t:
                s -= nums[L]
                L += 1
            # subarrays ending at R with sum ≤ t: (R - L + 1)
            res += R - L + 1
        return res

    return at_most(goal) - at_most(goal - 1)
''',
            "complexity": "Time O(n), space O(1).",
        },
        "deep_concept": r'''
Three counting problems on this page (binary subarrays with sum, nice
subarrays, K different integers) use the **same identity**:
`exactly K = atMost(K) − atMost(K − 1)`. Internalize it once, apply it
everywhere.
''',
        "confusion_notes": [
            {
                "question": "Why does the sliding window work for `atMost`?",
                "answer": "Because sum is monotone non-decreasing as we extend R (only adding non-negative values), so there's a unique leftmost L for each R such that the window sum is ≤ t. All shorter suffixes ending at R also have sum ≤ t, giving `R - L + 1` valid subarrays for that R.",
            },
            {
                "question": "Could we apply the atMost trick to negative numbers?",
                "answer": "Not directly — the monotonicity argument requires non-negative values. For arrays with negatives, use a prefix-sum + hash-map approach instead.",
            },
        ],
        "summary": "exact = atMost(K) − atMost(K−1). The atMost is a vanilla sliding window in O(n).",
    },

    # ------------------------------------------------------------------
    # 7) Count Number of Nice Subarrays
    # ------------------------------------------------------------------
    {
        "id": "nice-subarrays",
        "title": "Count Number of Nice Subarrays",
        "step_id": 10,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["sliding-window", "counting", "parity"],
        "what_this_teaches": "Same atMost(K) − atMost(K−1) trick on a parity binarization.",
        "pattern": "Binarize first, then exactly-K reduction.",
        "prerequisite_lessons": ["sliding-window"],
        "prerequisite_problems": ["binary-subarrays-with-sum"],
        "next_problems": ["subarrays-k-different-integers"],
        "resources": [
            _lc(1248, "count-number-of-nice-subarrays"),
            _SHEET,
        ],
        "understanding": r'''
Given an integer array `nums` and integer `k`, return the number of
subarrays containing **exactly** `k` odd numbers.

The trick: replace each odd by 1 and each even by 0. Then a "nice
subarray" is a subarray with sum equal to k. This is the *same* problem
as "Binary Subarrays With Sum"!
''',
        "brute_force": {
            "explanation": r'''
For every (i, j) count odds. O(n²). Or prefix-sum-of-odds + hashmap in
O(n) (same as before).
''',
            "code": r'''
def number_of_subarrays_brute(nums, k):
    n = len(nums)
    res = 0
    for i in range(n):
        odds = 0
        for j in range(i, n):
            if nums[j] % 2 == 1:
                odds += 1
            if odds == k:
                res += 1
            elif odds > k:
                break
    return res
''',
            "complexity": "Time O(n²), space O(1).",
        },
        "thought_process": r'''
Binarize then apply atMost trick: count of subarrays with exactly k odds
= atMost(k) − atMost(k − 1) on the odd-count.
''',
        "optimized": {
            "explanation": r'''
Two sliding-window passes counting subarrays with ≤ k odd numbers.
''',
            "code": r'''
def number_of_subarrays(nums, k):
    def at_most(t):
        if t < 0:
            return 0
        L = 0
        odd_count = 0
        res = 0
        for R, v in enumerate(nums):
            if v % 2 == 1:
                odd_count += 1
            while odd_count > t:
                if nums[L] % 2 == 1:
                    odd_count -= 1
                L += 1
            res += R - L + 1
        return res

    return at_most(k) - at_most(k - 1)
''',
            "complexity": "Time O(n), space O(1).",
        },
        "deep_concept": r'''
Pattern: when a problem says "exactly K of property P", binarize on P
and apply the atMost identity.
''',
        "confusion_notes": [
            {
                "question": "Why subtract atMost(k - 1)?",
                "answer": "Because atMost(k) counts subarrays with up to k odds, including those with 0..k-1 odds. Subtracting atMost(k-1) removes those, leaving exactly k.",
            },
        ],
        "summary": "Binarize odds to 1, evens to 0; then count exact-k subarrays via atMost(k) − atMost(k−1).",
    },

    # ------------------------------------------------------------------
    # 8) Subarrays with K Different Integers
    # ------------------------------------------------------------------
    {
        "id": "subarrays-k-different-integers",
        "title": "Subarrays with K Different Integers",
        "step_id": 10,
        "lecture_id": 1,
        "difficulty": "hard",
        "tags": ["sliding-window", "counting", "hashing"],
        "what_this_teaches": "Combines atMost trick with at-most-K-distinct window. The same template, twice.",
        "pattern": "atMost(K) − atMost(K − 1) where atMost uses a frequency-map window.",
        "prerequisite_lessons": ["sliding-window", "hashing"],
        "prerequisite_problems": ["longest-substring-k-distinct", "binary-subarrays-with-sum"],
        "next_problems": ["min-window-substring"],
        "resources": [
            _lc(992, "subarrays-with-k-different-integers"),
            _SHEET,
        ],
        "understanding": r'''
Given an integer array `nums` and integer `k`, return the number of
**good subarrays** — those with exactly `k` distinct integers.

By now this is mechanical: atMost(k) − atMost(k − 1), where atMost(t)
counts subarrays with at most t distinct integers using the frequency-
map sliding window from "longest substring with k distinct".
''',
        "brute_force": {
            "explanation": r'''
For every left endpoint, walk right with a set. O(n²) overall. Easy to
write but rejected on n = 20,000+.
''',
            "code": r'''
def subarrays_with_k_distinct_brute(nums, k):
    n = len(nums)
    res = 0
    for i in range(n):
        s = set()
        for j in range(i, n):
            s.add(nums[j])
            if len(s) == k:
                res += 1
            elif len(s) > k:
                break
    return res
''',
            "complexity": "Time O(n²), space O(k).",
        },
        "thought_process": r'''
We can't directly slide for "exactly k distinct" because shrinking L
might drop the distinct count past k for some valid right ends and we
end up tangled. The atMost identity rescues us: define a window that
respects ≤ k distinct, count subarrays-ending-at-R, sum up.
''',
        "optimized": {
            "explanation": r'''
Two sliding-window passes. Per pass: a frequency dict, expand R, shrink
L while `len(count) > t`, add `R − L + 1` to the count.
''',
            "code": r'''
def subarrays_with_k_distinct(nums, k):
    from collections import defaultdict
    def at_most(t):
        count = defaultdict(int)
        L = 0
        res = 0
        for R, v in enumerate(nums):
            count[v] += 1
            while len(count) > t:
                count[nums[L]] -= 1
                if count[nums[L]] == 0:
                    del count[nums[L]]
                L += 1
            res += R - L + 1
        return res

    return at_most(k) - at_most(k - 1)
''',
            "complexity": "Time O(n), space O(k).",
        },
        "deep_concept": r'''
This problem is the strongest case for the atMost trick. Three
templates fuse: at-most-K-distinct window + counting subarrays ending
at R + the exactly = atMost(K) − atMost(K−1) identity. Recognizing this
combo earns the points.
''',
        "confusion_notes": [
            {
                "question": "Why can't we just count subarrays where the distinct count first becomes k and stop?",
                "answer": "Because the distinct count is not monotone with respect to L for fixed R — shrinking from the left can drop the distinct count below k and then maybe never get back. Subtracting two atMosts avoids reasoning about this.",
            },
        ],
        "summary": "Two-pass atMost trick over the at-most-K-distinct template.",
    },

    # ------------------------------------------------------------------
    # 9) Minimum Window Substring
    # ------------------------------------------------------------------
    {
        "id": "min-window-substring",
        "title": "Minimum Window Substring",
        "step_id": 10,
        "lecture_id": 2,
        "difficulty": "hard",
        "tags": ["sliding-window", "strings", "hash-map"],
        "what_this_teaches": "Variable-size window that *contains a required multiset*. Track how many distinct required chars are currently satisfied.",
        "pattern": "Shrinking window with a 'have / need' counter.",
        "prerequisite_lessons": ["sliding-window", "hashing"],
        "prerequisite_problems": ["longest-substring-k-distinct"],
        "next_problems": ["min-window-subsequence"],
        "resources": [
            _lc(76, "minimum-window-substring"),
            _SHEET,
        ],
        "understanding": r'''
Given strings `s` and `t`, return the *smallest* substring of `s`
containing every character of `t` (counting multiplicities). If none
exists, return `""`.

**Example:** `s = "ADOBECODEBANC"`, `t = "ABC"` → answer `"BANC"`.

The intuition: expand R until the window contains every required char,
then try to shrink L (sliding right) while it still contains everything.
Record the smallest valid window seen.
''',
        "brute_force": {
            "explanation": r'''
Enumerate every substring of `s`, check if it contains `t` as a
multiset. Even with optimized checks this is O(n² · |t|). Slow.
''',
            "code": r'''
def min_window_brute(s, t):
    from collections import Counter
    need = Counter(t)
    best = ""
    for i in range(len(s)):
        have = Counter()
        for j in range(i, len(s)):
            have[s[j]] += 1
            if all(have[c] >= need[c] for c in need):
                cand = s[i:j+1]
                if best == "" or len(cand) < len(best):
                    best = cand
                break
    return best
''',
            "complexity": "Time O(n² · alphabet), space O(alphabet).",
        },
        "thought_process": r'''
We need a way to know in O(1) whether the window currently *covers* t.
The classic approach:
- Count `need[c]` for each char of `t`. Let `required = len(need)` —
  the number of distinct chars that must be matched.
- Walk R across s, maintain `have[c]` for the window. When `have[c]`
  first reaches `need[c]`, increment `formed`. When `formed == required`,
  the window covers t.
- While the window covers t, record the length and try to shrink L; if
  `have[s[L]]` drops below `need[s[L]]`, decrement `formed`.
''',
        "optimized": {
            "explanation": r'''
Linear-time sliding window with two counters and a `formed` integer.
''',
            "code": r'''
def min_window(s, t):
    if not t or not s:
        return ""
    from collections import Counter, defaultdict
    need = Counter(t)
    required = len(need)            # # of distinct chars to satisfy

    have = defaultdict(int)
    formed = 0                      # # of chars whose need is met

    best = (float('inf'), 0, 0)     # (length, L, R)
    L = 0
    for R, ch in enumerate(s):
        have[ch] += 1
        if ch in need and have[ch] == need[ch]:
            formed += 1             # this distinct char is now satisfied

        # try to shrink while the window is still valid
        while L <= R and formed == required:
            if R - L + 1 < best[0]:
                best = (R - L + 1, L, R)

            have[s[L]] -= 1
            if s[L] in need and have[s[L]] < need[s[L]]:
                formed -= 1         # we just lost a previously-satisfied char
            L += 1

    return "" if best[0] == float('inf') else s[best[1]:best[2] + 1]
''',
            "complexity": "Time O(|s| + |t|), space O(|alphabet|).",
        },
        "deep_concept": r'''
The `formed / required` trick is the standard way to test "window
satisfies multiset" in O(1) on each shrink/expand. Without it, the naive
`all(have[c] >= need[c])` check is O(alphabet) per step, multiplying the
total work.
''',
        "confusion_notes": [
            {
                "question": "Why use `==` when incrementing `formed`?",
                "answer": "Because `formed` should count *distinct* required chars whose count target is *exactly met*. Each char crosses the threshold from below to above exactly once during expansion (when have[c] hits need[c]) and from above to below exactly once during shrink (when have[c] drops to need[c] - 1). Use `==` on increment and `<` on decrement.",
            },
            {
                "question": "What if t has repeated chars like t = 'AABC'?",
                "answer": "Then need['A'] = 2 and the window must contain two A's before that letter counts as satisfied. The == check handles this naturally — formed increments only when have['A'] reaches 2 exactly.",
            },
        ],
        "summary": "Window with multiset coverage. Track `formed` distinct chars whose required count is met; shrink whenever the window is valid; record the shortest.",
    },

    # ------------------------------------------------------------------
    # 10) Minimum Window Subsequence
    # ------------------------------------------------------------------
    {
        "id": "min-window-subsequence",
        "title": "Minimum Window Subsequence",
        "step_id": 10,
        "lecture_id": 2,
        "difficulty": "hard",
        "tags": ["two-pointer", "strings", "dynamic-programming"],
        "what_this_teaches": "Two-pointer walk that finds the earliest *subsequence* match for `t` in `s`, then tightens from the right.",
        "pattern": "Two-pointer forward+backward to minimize a subsequence window.",
        "prerequisite_lessons": ["two-pointer"],
        "prerequisite_problems": ["min-window-substring"],
        "next_problems": [],
        "resources": [
            {"label": "LeetCode 727 — Minimum Window Subsequence", "url": "https://leetcode.com/problems/minimum-window-subsequence/"},
            _SHEET,
        ],
        "understanding": r'''
Given strings `s` and `t`, return the *smallest* substring `W` of `s`
such that `t` is a *subsequence* of `W`. If multiple are tied, return
the leftmost.

This differs from Minimum Window Substring: here the chars of t must
appear *in order* (subsequence), not as a multiset.

**Example:** `s = "abcdebdde"`, `t = "bde"` → answer `"bcde"` (length 4).
Note `"bdde"` also contains `bde` as a subsequence but is longer.
''',
        "brute_force": {
            "explanation": r'''
For each starting index `i` of `s`, walk both pointers and check whether
t is a subsequence starting from `s[i:]`. O(n · m). For `n = m = 20000`,
that's 4·10⁸ ops — too slow in tight limits but conceptually simple.
''',
            "code": r'''
def min_window_subseq_brute(s, t):
    n, m = len(s), len(t)
    best = ""
    for i in range(n):
        j = 0
        k = i
        while k < n and j < m:
            if s[k] == t[j]:
                j += 1
            k += 1
        if j == m:
            cand = s[i:k]
            if not best or len(cand) < len(best):
                best = cand
    return best
''',
            "complexity": "Time O(n · m), space O(1).",
        },
        "thought_process": r'''
The clever observation: when a window `[i, k]` contains t as a
subsequence (forward scan succeeds at index k), we can shrink it on the
*left* by scanning backward — start with `j = m − 1` and walk left,
matching characters of t in reverse. The new `i'` is the smallest
starting index such that `s[i'..k]` still contains t.

So the algorithm walks two pointers forward to find a match endpoint `k`,
then walks backward to find the *tightest* starting index `i'` for that
k. Then we jump i one past i' and restart from there.
''',
        "optimized": {
            "explanation": r'''
Forward + backward two-pointer. Total work is O(n · m) in the worst
case but typically much faster because backward scans are short.
There is also an O(n · m) DP solution; we present the two-pointer one
because the educational value is higher.
''',
            "code": r'''
def min_window_subsequence(s, t):
    n, m = len(s), len(t)
    i = 0
    best_len = float('inf')
    best_start = -1

    while i < n:
        # forward scan: try to consume all of t
        j = 0
        k = i
        while k < n and j < m:
            if s[k] == t[j]:
                j += 1
            k += 1

        if j < m:
            break       # no further match possible

        # backward scan: tighten the left edge
        end = k - 1     # position where we matched the last char of t
        j = m - 1
        L = end
        while j >= 0:
            if s[L] == t[j]:
                j -= 1
            L -= 1
        L += 1          # restore to the actual leftmost match index

        if end - L + 1 < best_len:
            best_len = end - L + 1
            best_start = L

        i = L + 1       # next forward scan starts past the tight L

    return "" if best_start == -1 else s[best_start:best_start + best_len]
''',
            "complexity": "Time O(n · m) worst case; often much faster. Space O(1).",
        },
        "deep_concept": r'''
Forward-find-end then backward-tighten-start is a recurring pattern
whenever you need the *smallest* substring containing a target as a
subsequence. The two scans don't double the work in practice — they
only re-scan within the matched region, which is bounded by the size of
the best window found.

An alternative O(n · m) DP keeps `dp[i][j]` = the largest starting
index in `s[0..i]` such that `t[0..j]` is a subsequence ending at i.
The two-pointer version is shorter and uses no extra memory.
''',
        "confusion_notes": [
            {
                "question": "Why does the backward scan find the *tightest* L?",
                "answer": "Because we walk leftward from `end` and consume t in reverse. The very first time we have consumed all of t is the rightmost L where `s[L..end]` still contains t as a subsequence — any smaller L is unnecessary (gives a longer window).",
            },
            {
                "question": "Why `i = L + 1` and not `i = L`?",
                "answer": "Because reusing i = L would just rediscover the same tight match. Jumping to L + 1 guarantees forward progress and avoids infinite loops.",
            },
        ],
        "summary": "Forward two-pointer to find a match endpoint, then backward two-pointer to tighten the start. Track the minimal window across all matches.",
    },
]
