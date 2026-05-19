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
        "what_this_teaches": (
            "How to decompose a non-trivial string transformation into "
            "**reversals**. The 'reverse all, then reverse each part' "
            "trick is the same algebra used to rotate arrays in O(1) "
            "extra memory."
        ),
        "pattern": "Tokenize and reverse, or reverse-all-then-reverse-parts.",
        "prerequisite_lessons": ["strings", "arrays"],
        "prerequisite_problems": [],
        "next_problems": [
            "largest-odd-number",
            "longest-common-prefix",
            "rotation-of-string",
            "left-rotate-by-d",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 5 (Easy Strings)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 151 — Reverse Words in a String",
                "url": "https://leetcode.com/problems/reverse-words-in-a-string/",
            },
        ],
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
        "confusion_notes": [
            {
                "question": "Why does `.split()` with no argument behave differently from `.split(' ')`?",
                "answer": r'''
This is a small but important Python detail.

`s.split()` with **no argument** does two helpful things at
once: it splits on **runs of whitespace** (any whitespace, of
any length), and it **drops leading and trailing whitespace**.
So `"  the  sky  ".split()` returns `["the", "sky"]` — a clean
two-element list with no empty strings.

`s.split(' ')` with an **explicit space** treats every single
space as a separator, including consecutive spaces. So `"  the
sky  ".split(' ')` returns `["", "", "the", "", "sky", "", ""]`
— a much messier list full of empty strings from the duplicate
delimiters.

For "reverse words" problems with sloppy input (extra spaces),
the no-argument form is what you want. The explicit-delimiter
form would force you to filter out empty strings afterward,
which is awkward and bug-prone.

This is one of those Pythonisms that comes up in interview code
all the time. Use `.split()` for whitespace tokenization;
reserve `.split(delim)` for cases where the delimiter is
specific and exactly counted (like CSV parsing).
''',
            },
            {
                "question": "Why is the in-place two-reversal trick `O(1)` extra memory?",
                "answer": r'''
Because all the reversals happen *inside* the existing array.
No new array is allocated; only a constant number of index
variables (`left`, `right`) are created. That gives `O(1)`
auxiliary space.

In Python, strings are immutable, so you cannot literally do
the trick on a `str` — you would first convert to a list of
characters (`list(s)`), do the reversals on the list, then join
back. The list conversion is technically `O(n)` extra space.

In C++ or Java with a `char[]`, the trick is truly in-place.
The two-reversal idea was originally developed in those
languages, where in-place is the natural target.

For Python interviews on this specific problem, the
`.split()/reversed()/' '.join()` approach is acceptable and
cleaner. Mention the two-reversal trick as the "in-place" answer
the interviewer might be hoping for in a typed language.

The reason the trick is in-place at all is that **two reversals
in the right places cancel out the local order changes from the
first one**. Reversing the whole array flips the global order,
but each word's characters end up in *reverse order* within
their new positions. Reversing each word again undoes the local
flip, leaving the global flip intact. Net: the words are in the
reversed order but each word reads correctly.
''',
            },
            {
                "question": "How do I handle multiple spaces and trailing whitespace?",
                "answer": r'''
The Pythonic approach (`.split()` with no argument) handles them
for free — runs of whitespace collapse to single separators,
and leading/trailing whitespace is silently dropped.

```python
" ".join(reversed(s.split()))
```

For `"  the  sky   is   blue  "`, this returns `"blue is sky
the"`. Clean and correct, no manual whitespace handling.

If you write the in-place two-reversal version, you have to do
the whitespace cleanup yourself, usually with a two-pointer
compaction pass:

1. Reverse the entire array.
2. Walk through with a fast pointer (read) and slow pointer
   (write). Copy non-space characters and exactly one space
   between words. Skip leading whitespace.
3. Reverse each word in place using the cleaned-up array.

It is mechanical but tedious. The Python version dodges all of
that by leaning on `.split()` and `' '.join()`. Choose the
right tool for the language.

A subtle interview tip: always check whether the problem treats
"the input might have weird whitespace" as part of the spec or
not. If the input is guaranteed to be cleanly tokenized, you can
skip the whitespace gymnastics entirely.
''',
            },
            {
                "question": "What is the time complexity of the simple version?",
                "answer": r'''
*O(n)* time, *O(n)* extra space.

`s.split()` walks the string once: *O(n)*. The resulting list
has at most *O(n)* total characters. `reversed(...)` is *O(1)*
to create — it returns an iterator, not a new list. The
`" ".join(...)` walks the reversed iterator and builds the
output, which is another *O(n)* pass.

The extra space comes from two places: the list of word strings
returned by `.split()`, and the new output string built by
`.join()`. Both are *O(n)* in the worst case.

The two-reversal in-place version is *O(n)* time and *O(1)*
extra space (after converting the string to a list, which is
itself *O(n)* in Python). In a language with mutable strings,
truly *O(1)*.

For interview problems, *O(n)* time is the optimum (you have to
look at every character at least once). The memory difference
between the two approaches is usually only relevant if the
interviewer specifically asks "can you do it in-place?".
''',
            },
        ],
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
        "what_this_teaches": (
            "**Bidirectional mapping** as a correctness tool. A "
            "consistent one-to-one mapping requires checks in *both* "
            "directions; one-way checks are a classic source of "
            "silent bugs in problems like word pattern matching."
        ),
        "pattern": "Two hash maps enforcing a bijection between character sets.",
        "prerequisite_lessons": ["strings", "hashing"],
        "prerequisite_problems": ["count-frequencies", "two-sum"],
        "next_problems": [
            "longest-common-prefix",
            "rotation-of-string",
            "sort-characters-by-frequency",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 5 (Easy Strings)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 205 — Isomorphic Strings",
                "url": "https://leetcode.com/problems/isomorphic-strings/",
            },
        ],
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
        "confusion_notes": [
            {
                "question": "Why do I need *two* maps? Isn't one enough?",
                "answer": r'''
A single map covers one direction of the bijection but misses
the other. A bijection is **one-to-one AND onto**, and you have
to check both.

Walk through `s = "foo"`, `t = "boa"`. With only an `s -> t`
map:
- `f -> b`: store `{f: b}`.
- `o -> o`: store `{f: b, o: o}`.
- `o -> a`: `o` already maps to `o`, but now we want it to map
  to `a`. Conflict — return `False`.

This catches the bug, so the one-map version *seems* to work.

Now try `s = "ab"`, `t = "aa"`. With only `s -> t`:
- `a -> a`: store `{a: a}`.
- `b -> a`: `b` is new — store `{a: a, b: a}`. No conflict.
- Return `True`.

But this is **wrong**. Both `a` and `b` from `s` map to the same
character `a` in `t`. That is not a bijection; it is a function
that collapses two distinct inputs to one output. With the
**second** map `t -> s`:
- `a -> a`: store `{a: a}`.
- `a -> b`: `a` in `t` already comes from `a` in `s`, but now
  we want it to come from `b`. Conflict — return `False`.

The reverse map catches the collapse. That is why you need both
directions.

The general lesson: whenever a problem says "one-to-one
correspondence" or "consistent bijection," ask yourself, *"can
two distinct inputs map to the same output, and is that
allowed?"* If not, you need the reverse check too.
''',
            },
            {
                "question": "Could I use a single dict whose keys are pairs?",
                "answer": r'''
Yes. A clever single-structure alternative tracks the *pair*
that has been seen. For each character pair `(s[i], t[i])`, you
need to ensure:

1. Every time `s[i]` has appeared, it was paired with the same
   `t[i]`.
2. Every time `t[i]` has appeared, it came from the same `s[i]`.

You can encode both with one dict from each character to its
partner *position* — usually the index of first occurrence. Two
strings are isomorphic iff their "indices of first occurrence"
patterns are identical:

```python
def is_isomorphic(s, t):
    if len(s) != len(t):
        return False
    return [s.index(c) for c in s] == [t.index(c) for c in t]
```

`s.index(c)` returns the **first** index where `c` appears, so
each character collapses to a number representing "which
position did this character first appear at?". Two strings with
the same "first-occurrence-index" pattern are isomorphic.

This is short but slow (`s.index` is `O(n)` per call, making it
`O(n²)` overall). The two-map version is `O(n)` and clearer.
But the index-pattern formulation is a beautiful demonstration
of "canonicalize, then compare."

In interviews, mention both. The interviewer may want the
optimal solution (`O(n)` two maps) or the clever one-liner
(`O(n²)` index pattern). Knowing both shows depth.
''',
            },
            {
                "question": "Why does the length check come first?",
                "answer": r'''
Because strings of different lengths cannot be isomorphic, and
checking this upfront avoids running the loop on input that is
guaranteed to fail.

A bijection between two character sequences requires a
**one-to-one pairing** of positions. If the strings have
different lengths, you cannot pair every position from one with
a position from the other. So the answer is immediately `False`.

```python
if len(s) != len(t):
    return False
```

Two lines. They guard against an obvious failure mode and let
the rest of the code assume `len(s) == len(t)`, which simplifies
the `zip(s, t)` loop.

Without the guard, `zip(s, t)` would silently stop at the
shorter string's end and produce a result based only on the
prefix that both share. For `s = "ab"` and `t = "abc"`, `zip`
would yield only `(a, a)` and `(b, b)` — concluding they are
isomorphic (which is wrong, because they have different
lengths).

The general lesson: **guard against pathological inputs at the
top** of your function, so the main logic can assume cleaner
preconditions. This is the same discipline as the `if n == 0:
return 1` guard in count-digits and the `if not arr: return 0`
guard in array problems.
''',
            },
            {
                "question": "What's the relationship between this and 'anagrams'?",
                "answer": r'''
They are cousins in the same family of "canonicalize, then
compare" problems, but the canonical forms differ.

**Anagrams**: two strings are anagrams if they have the same
multiset of characters. Canonical form: sorted character tuple,
or character-count map.

```python
def is_anagram(a, b):
    return sorted(a) == sorted(b)   # or Counter(a) == Counter(b)
```

**Isomorphic**: two strings are isomorphic if there is a
one-to-one mapping between their character sets that
respects position. Canonical form: tuple of first-occurrence
indices.

```python
def canon(s):
    return tuple(s.index(c) for c in s)

def is_isomorphic(a, b):
    return canon(a) == canon(b)
```

So both reduce to "compute a canonical signature, compare
signatures for equality" — but the signatures are different
because the equivalence relations are different.

**Group anagrams** uses anagram canonicalization plus a
dictionary keyed by canonical form. **Group isomorphic words**
would use isomorphic canonicalization plus the same
dictionary trick.

The mental move: whenever a problem says "find all things
equivalent under property X," pick a canonical form for X,
group by canonical form, done. This pattern shows up in many
shapes: anagrams, isomorphic words, equivalent subtree
detection, etc.
''',
            },
        ],
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
