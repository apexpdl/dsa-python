"""Step 10 — Sliding Window & Two Pointer."""
from __future__ import annotations

PROBLEMS: list[dict] = [
    {
        "id": "longest-substring-no-repeat",
        "title": "Longest Substring Without Repeating Characters",
        "step_id": 10,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["sliding-window", "hashing"],
        "what_this_teaches": (
            "The **variable-size sliding window** template — grow on "
            "the right, shrink on the left until valid, record the "
            "best. This single skeleton handles a huge family of "
            "'longest / shortest substring with property P' problems."
        ),
        "pattern": "Two pointers + a hash that summarizes the current window.",
        "prerequisite_lessons": ["strings", "hashing", "sliding-window"],
        "prerequisite_problems": ["two-sum", "count-frequencies"],
        "next_problems": [
            "longest-substring-k-distinct",
            "longest-repeating-replacement",
            "max-consecutive-ones-iii",
            "fruit-into-baskets",
            "min-window-substring",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 10 (Sliding Window)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 3 — Longest Substring Without Repeating Characters",
                "url": "https://leetcode.com/problems/longest-substring-without-repeating-characters/",
            },
        ],
        "understanding": r'''
Given a string `s`, return the length of the longest substring
containing **no repeated character**. A substring is contiguous.

Examples: `"abcabcbb"` → `3` (`"abc"`). `"bbbbb"` → `1` (`"b"`).
`"pwwkew"` → `3` (`"wke"`, not `"pwke"` because the latter is a
subsequence, not a substring).

This is the canonical variable-size sliding window problem. Master
it; many medium / hard problems are slight variations.
''',
        "brute_force": {
            "explanation": r'''
For each starting index, expand the window until a duplicate
appears; record the length. Two nested loops, *O(n²)*.

```python
best = 0
for i in range(n):
    seen = set()
    for j in range(i, n):
        if s[j] in seen:
            break
        seen.add(s[j])
        best = max(best, j - i + 1)
```
''',
            "code": r'''def longest_unique_brute(s: str) -> int:
    n = len(s)
    best = 0
    for i in range(n):
        seen = set()
        for j in range(i, n):
            if s[j] in seen:
                break
            seen.add(s[j])
            best = max(best, j - i + 1)
    return best
''',
            "complexity": "**Time**: *O(n²)*. **Space**: *O(k)*.",
        },
        "thought_process": r'''
The brute force restarts from scratch at each starting index. But
we can avoid this with a **moving window** `[left, right]`. We
extend `right` greedily; whenever the new character is already
inside the window, we shrink from the left until the duplicate is
gone. At every step the window is **a valid no-repeat substring**.

To track "is this character inside the window?", we use a hash map
from character to its last seen index. When we see a character that
is already in the map **and** its last index is `>= left`, that's
a duplicate inside the current window. We jump `left` to
`last_index + 1` to escape it.

Why is this *O(n)*? Because `left` and `right` each move only
forward, and each character is visited at most twice (once by
`right`, once by `left`).

This is the textbook variable-size sliding window. Internalize the
shape:

1. Move `right` forward, updating the data structure.
2. If a constraint is violated, move `left` forward and undo the
   update.
3. Record the answer.

Steps 1 and 3 are common. Step 2 is the constraint-specific
shrinking logic.
''',
        "optimized": {
            "explanation": r'''
Single-pass sliding window with a hash from character to last
index seen.
''',
            "code": r'''def longest_unique(s: str) -> int:
    last_index: dict[str, int] = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        # If ch is in the window, jump left past its previous
        # occurrence. The 'in window' test is `prev_index >= left`.
        if ch in last_index and last_index[ch] >= left:
            left = last_index[ch] + 1
        # Record / update ch's last seen index.
        last_index[ch] = right
        # The current window [left..right] is valid; update best.
        best = max(best, right - left + 1)
    return best
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(min(n, k))*.",
        },
        "deep_concept": r'''
The variable-size sliding window has one signature shape: **a
window that grows on the right and shrinks on the left until the
constraint is satisfied, then records the answer**.

Variations on this sheet:

- **Longest substring with at most K distinct characters** — shrink
  while the number of distinct keys exceeds K.
- **Max consecutive ones III** (with at most K zeros allowed) —
  shrink when the count of zeros in the window exceeds K.
- **Longest repeating character replacement** — shrink when the
  window length minus the max-frequency character count exceeds K.
- **Fruit into baskets** — exactly "at most 2 distinct".

For "exactly K" problems (e.g., subarrays with exactly K distinct):
solve "at most K" twice, subtract. That trick converts hard
"exactly" problems into easy "at most" sliding windows.

Sliding window is one of the cleanest examples of trading
*O(n²)* nested loops for *O(n)* incremental maintenance.
''',
        "confusion_notes": [
            {
                "question": "Why does the check `last_index[ch] >= left` use `>=` and not just `in`?",
                "answer": r'''
Because a character can be in the `last_index` dict from a
**previous** appearance that has already slid out of the
current window. Such a stale entry should be ignored — it does
not represent a current duplicate.

Walk through `s = "abba"`. After processing the first three
characters:
- `left = 0`, dict = `{a: 0, b: 2}`, current window is `"ab"`
  followed by `"bb"` which shrinks left to 2, so window is
  `"b"`.

Hmm, let me redo that more carefully. Step by step:

- `right = 0, ch = 'a'`: dict empty, `left = 0`. Record `{a:
  0}`. Window `[0, 0]` = `"a"`, length 1.
- `right = 1, ch = 'b'`: `'b'` not in dict. Record `{a: 0, b:
  1}`. Window `[0, 1]` = `"ab"`, length 2.
- `right = 2, ch = 'b'`: `'b'` is in dict at index 1, and `1 >=
  left (0)`. So we set `left = 1 + 1 = 2`. Record `{a: 0, b:
  2}`. Window `[2, 2]` = `"b"`, length 1.
- `right = 3, ch = 'a'`: `'a'` is in dict at index 0, but `0 <
  left (2)`. So the `'a'` we saw earlier is OUTSIDE the
  current window — ignore it. Set `left` stays at 2. Record
  `{a: 3, b: 2}`. Window `[2, 3]` = `"ba"`, length 2.

Final answer: 2 (longest is `"ab"` or `"ba"`).

If we had used just `if ch in last_index` (without the `>=
left` check), the last step would have jumped `left` to 1,
incorrectly treating the long-gone `'a'` as a duplicate inside
the window. The window would shrink unnecessarily and the
answer would be wrong.

The `>= left` check is the critical "is this duplicate actually
inside the current window?" filter.
''',
            },
            {
                "question": "Why do we write `last_index[ch] = right` even when ch is already in the dict?",
                "answer": r'''
Because we always want the dict to hold the **most recent**
index where each character appeared. The next time we encounter
that character, we want to jump `left` to just past its **most
recent** occurrence, not its earliest one.

If we only inserted on first encounter and never updated, the
stale earliest-index entries would mislead the algorithm. For
`s = "abcab"`:

- After processing the first `'a'`, dict = `{a: 0}`.
- After the second `'a'`, we should update dict to `{a: 3, ...}`
  so the next `'a'` jumps `left` past index 3, not index 0.

The pattern is "scan once, dict tracks the latest" for every
character. The assignment `last_index[ch] = right` happens
unconditionally on every iteration, with the value being the
current `right`.

This is the same pattern as **dictionary by overwriting** in
many problems — Counter doing the same thing for counts,
"last seen" maps for cycle detection, etc. The data structure
holds the most recent state; old state is implicitly forgotten
because it gets overwritten.

A small note: if you wanted "first occurrence" instead (for a
different problem), you would guard with `if ch not in
last_index:`. For longest-substring-no-repeat, we want "most
recent," so we just overwrite.
''',
            },
            {
                "question": "Why is the time complexity O(n) and not O(n²)?",
                "answer": r'''
Because **each character is processed at most twice** across the
entire algorithm: once when `right` reaches it, and at most once
when `left` slides past it.

The `right` pointer marches from 0 to `n - 1` exactly once. The
`left` pointer also only moves forward (it can jump, but never
backward). So `left` also moves at most `n` steps total.

Combined, the algorithm does at most `2n` pointer movements,
plus constant-time dict operations per movement. That gives
*O(n)* time.

Each iteration's inner work is bounded:
- One dict lookup: amortized *O(1)*.
- One comparison and at most one assignment: *O(1)*.
- One dict update: *O(1)*.
- One max comparison: *O(1)*.

So even though the inner branch updates `left`, the update is
bounded by the total budget for `left`'s forward motion. The
algorithm is genuinely linear.

Contrast with a naive O(n²) approach: for each starting
position, scan rightward until a duplicate is found, counting
the length. That algorithm re-scans the same characters many
times. The sliding-window version uses the dict to make those
re-scans unnecessary.
''',
            },
            {
                "question": "Why does `right - left + 1` correctly count window length?",
                "answer": r'''
Because the window is the **inclusive** range `[left, right]`,
and the number of integers in such a range is `right - left +
1`.

This is the fence-post counting rule from the Arrays lesson.
For `left = 2, right = 5`, the indices in the window are `{2, 3,
4, 5}` — four indices, which equals `5 - 2 + 1`.

The `+ 1` is the easiest off-by-one to get wrong. A common bug
is writing `right - left`, which gives **one less** than the
correct length. For `left = 2, right = 5`, that returns 3
instead of 4.

To verify your formula: pick the smallest case (`left ==
right`). The window contains just one element. Plug in:
`right - left + 1 = 0 + 1 = 1`. Correct.

If you instead used a half-open window `[left, right)`, the
length would be `right - left` (no `+ 1`). Both styles are
valid; pick one and be consistent throughout the function.

Our code uses inclusive boundaries (the canonical sliding
window style), so `right - left + 1` is the right formula.
''',
            },
        ],
        "summary": r'''
**Pattern**: variable-size window `[left, right]` with a hash
maintaining the inside-window state.

**Lesson**: the constraint that forbids duplicates drives the
shrinking rule. Every "longest substring with property X"
template is the same.

**Recognize next time**: any "longest / shortest / count of
substrings satisfying property P". The recipe is mechanical.
''',
    },
]
