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
