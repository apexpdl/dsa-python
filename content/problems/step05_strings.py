"""Step 5 — Strings."""
from __future__ import annotations

PROBLEMS: list[dict] = [
    {
        "id": "reverse-words",
        "title": "Reverse Words in a String",
        "step_id": 5,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["strings", "split", "two-pointers"],
        "understanding": r'''
We have a string like `"  the sky   is blue  "` and we need to
return `"blue is sky the"`. Words are sequences of non-space
characters separated by spaces. Leading, trailing, and multiple
in-between spaces should collapse to a single space between words
in the output.

The challenge is more about **edge cases** (extra spaces) than
about cleverness.
''',
        "brute_force": {
            "explanation": r'''
Python makes this almost too easy:

```python
return " ".join(reversed(s.split()))
```

`split()` with no arguments splits on runs of whitespace and skips
leading/trailing whitespace. `reversed()` reverses the list.
`" ".join(...)` glues them with a single space. Three operations,
one line.

For interview / educational purposes, doing it in-place with two
pointers (treating the string as a list of characters) teaches a
useful pattern.
''',
            "code": r'''def reverse_words_pythonic(s: str) -> str:
    # split() with no argument splits on whitespace runs and drops
    # leading/trailing whitespace. join with single space gives the
    # clean output.
    return " ".join(reversed(s.split()))
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(n)*.",
        },
        "thought_process": r'''
The interview-flavored version goes like this. **Step 1**: reverse
the entire string. **Step 2**: reverse each word in place. The
result is the original words in reverse order.

For input `"the sky"` (no extra spaces): reverse the whole string
to `"yks eht"`. Then reverse each word: `"sky the"`.

The two-reversal trick is famous and reused in **array rotation**
(rotate by k means: reverse all, reverse first k, reverse rest). It
is one of the prettiest constant-space tricks.

For Python where strings are immutable, you implement this on a
list of characters, then join. For C++/Java with `char[]` it is
truly in-place.

The handling of multiple spaces is the only fiddly part. The
`split()` approach finesses it. The two-reversal approach requires
an explicit "skip extra spaces" pass.
''',
        "deep_concept": r'''
The reverse-all-then-reverse-parts trick is the "rotation
identity". If you ever face "rotate array by k positions in O(1)
extra space", the answer is:

1. Reverse the entire array.
2. Reverse the first k elements.
3. Reverse the rest.

Total *O(n)* time, *O(1)* space. The proof is by direct
verification: the algebra works out, even if the *aha* takes a
moment.

For strings specifically, the lesson is to recognize when the
problem reduces to a sequence of reversals on a list of characters.
That mental model handles "reverse words", "reverse only letters",
and several others.
''',
        "summary": r'''
**Pattern**: split / reverse list / join, OR the in-place
"reverse all, then reverse each part" trick.

**Lesson**: many string rearrangements decompose into reversals.

**Recognize next time**: array rotation, "reverse words", string
permutations involving block flips.
''',
    },
    {
        "id": "isomorphic-strings",
        "title": "Isomorphic Strings",
        "step_id": 5,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["strings", "hashing"],
        "understanding": r'''
Two strings `s` and `t` are **isomorphic** if you can replace
characters in `s` to get `t` using a **consistent one-to-one
mapping**. So `"egg"` and `"add"` are isomorphic (`e -> a`,
`g -> d`). But `"foo"` and `"bar"` are not, because mapping `f -> b`
and then `o -> a` is fine, but then the second `o` would also map
to `r`, which contradicts our earlier `o -> a` rule.

The one-to-one constraint is crucial: each character in `s` maps to
a unique character in `t`, **and** each character in `t` is the
image of a unique character in `s`. Both directions.
''',
        "brute_force": {
            "explanation": r'''
There is no real "brute force" here. The natural algorithm is to
walk both strings together, maintaining two maps: `s[i] -> t[i]`
and `t[i] -> s[i]`. At each step we check consistency.

The reason for **two** maps: the mapping must be a **bijection**.
If we only check `s -> t`, we miss cases like `s = "foo"`,
`t = "boa"` (which fails because both `o` characters map to `o`
and `a`).
''',
            "code": r'''def is_isomorphic(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    s_to_t: dict[str, str] = {}
    t_to_s: dict[str, str] = {}
    for a, b in zip(s, t):
        # Direction 1: a must map to the same b each time.
        if a in s_to_t and s_to_t[a] != b:
            return False
        # Direction 2: b must come from the same a each time.
        if b in t_to_s and t_to_s[b] != a:
            return False
        s_to_t[a] = b
        t_to_s[b] = a
    return True
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(k)* where k is the alphabet size.",
        },
        "thought_process": r'''
The interview test is to remember the **two-direction** check. Many
candidates write only one map and miss the case where two distinct
source characters collapse into the same target. Always think:
"does the constraint go both ways? If yes, I need two maps".

A more compact technique: instead of two maps, encode each string
by the index of first occurrence of each character. Two strings are
isomorphic iff their first-occurrence-index encodings match.
''',
        "deep_concept": r'''
The "bijection" pattern shows up in many problems:

- **Word pattern** — same idea but at word granularity.
- **Group anagrams** — group by sorted-character-tuple (a canonical
  form).
- **Find duplicate subtrees** — group by serialized subtree string.

The unifying idea: **canonicalize each item into a comparable form,
then group/compare**. For isomorphism the canonical form is "indices
of first occurrence". For anagrams it is "sorted characters". For
trees it is "serialized structure".

Whenever you need to compare items by some equivalence relation,
the move is to choose a canonical representative and reduce to
equality.
''',
        "summary": r'''
**Pattern**: maintain bidirectional maps to enforce a bijection.

**Lesson**: "consistent one-to-one mapping" needs checks in both
directions.

**Recognize next time**: any problem about renaming, character
substitution, or pattern matching where the mapping must be unique
both ways.
''',
    },
]
