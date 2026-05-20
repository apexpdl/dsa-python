"""Strings — arrays of characters, with twists."""

LESSON = {
    "id": "strings",
    "title": "Strings — Arrays With Extra Rules",
    "tags": ["strings", "beginner", "fundamentals"],
    "summary": (
        "A full beginner chapter. Strings as immutable arrays, the "
        "string-builder pattern, character arithmetic, the canonical "
        "form trick, slicing pitfalls, and the family of pattern-"
        "matching ideas that grow out of basic string work."
    ),
    "body": r'''
## 0. The promise of this chapter

Strings show up in roughly half of all interview problems. You
might think they would be easy — just arrays of characters,
right? Mostly, yes. But Python's strings have a few quirks
(immutability, slicing copies, indexing surprises) that catch
beginners constantly.

This chapter is the friendly tour of those quirks, plus the small
handful of patterns that solve the lion's share of string DSA. By
the end you should be able to look at any string problem and ask
"is this index-walking, two-pointers, sliding window, or hash-
based grouping?"

Read slowly. Strings reward muscle memory.

## 1. A string is an array of characters (mostly)

If arrays are rows of numbered parking spots, a string is the
same parking lot — except each spot holds a single character and
you have to promise not to repaint the spots after the lot opens.

```python
s = "hello"
print(s[0])    # 'h' — same indexing as a list
print(s[-1])   # 'o' — negative indices count from the end
print(s[1:4])  # 'ell' — same slicing as lists
print(len(s))  # 5
```

So far, strings look identical to lists. And for most read-only
purposes, you can pretend they are.

The deviation begins with mutation.

## 2. The catch: you cannot change a character in place

```python
s = "hello"
s[0] = "H"     # TypeError: 'str' object does not support item assignment
```

Strings in Python are **immutable**. Once you make a string, it
can never change. If you want a different string, you have to
**build a new one**.

This is not a flaw — it is a deliberate design choice with two
big benefits:

1. **Safe sharing.** Two variables pointing at the same string
   can never be surprised by an edit from elsewhere.
2. **Usable as dict keys.** Mutable objects cannot be hashed (or
   their hash would change beneath you). Immutable strings make
   excellent keys.

Mental model: think of a string as a **photo**. You cannot change
the photo. You can crop it, glue it next to another, or describe
it. Every operation produces a new photo.

## 3. How do you "edit" a string then?

The canonical Python pattern: convert to a list of characters,
edit the list, join back.

```python
s = "hello"
chars = list(s)         # ['h', 'e', 'l', 'l', 'o']
chars[0] = "H"          # mutable list, edit in place
s_new = "".join(chars)  # 'Hello'
```

If you remember exactly one trick from this chapter, remember
this one. "Convert to list, edit, join back" is the string-
builder's bread-and-butter.

The implicit cost: the conversion `list(s)` is *O(n)*, and the
final `"".join(chars)` is also *O(n)*. So an edit-via-list takes
*O(n)* per edit. That is fine for one edit but expensive for many.

## 4. The "+=" inside a loop trap

```python
# Slow: O(n²) overall because of immutability.
result = ""
for ch in big_string:
    result += ch
```

Each `result += ch` cannot extend the old string (because the old
string is immutable). It must allocate a new string, copy every
character that was already in `result`, and add the new
character. If you do this `n` times, the total work is `1 + 2 +
... + n ≈ n²/2`. For `n = 10,000` that is 50 million tiny copies
when the answer should be 10,000.

The fix:

```python
# Fast: append into a list (O(1) per append), then join once (O(n)).
pieces = []
for ch in big_string:
    pieces.append(ch)
result = "".join(pieces)
```

The list appends in amortized constant time. The `join` walks the
list exactly once. Total work is `O(n)` instead of `O(n²)`.

This is a small habit but a critical one. Whenever you find
yourself accumulating characters in a loop, build a list and join
at the end. Never `+=` strings in tight loops.

## 5. Characters are tiny integers in disguise

Python does not have a separate "char" type — every character is
a one-letter string. But there are two functions that link
characters to numbers, and they unlock huge possibilities:

```python
ord('a')   # 97 — the Unicode code point of 'a'
chr(97)    # 'a' — the character with code point 97
ord('A')   # 65 — uppercase letters are 32 below their lowercase twins
ord('z') - ord('a')   # 25 — 26 lowercase letters total
```

This unlocks the **26-bucket trick**. If your input is a string
of lowercase English letters, you can use a 26-length list
indexed by `ord(c) - ord('a')` instead of a dict. Faster, smaller,
and more cache-friendly.

```python
def char_counts(s):
    counts = [0] * 26
    for ch in s:
        counts[ord(ch) - ord('a')] += 1
    return counts
```

Anagram problems, character-frequency problems, and many DP-on-
strings problems use this trick. When the alphabet is small and
known, the fixed-size array beats the dict for both speed and
clarity.

## 6. The string-as-array operations

```python
s = "racecar"

len(s)                  # 7
s[::-1]                  # 'racecar' — reverse via slicing
s.lower()                # lowercase
s.upper()                # uppercase
"a".isalpha()            # True
"7".isdigit()            # True
" ".isspace()            # True
"foo" + "bar"            # 'foobar' — concatenation
"ace" in s               # True — substring check (O(n × m) worst case)
```

A few things to internalize:

- **Slicing creates a copy.** `s[1:]` is *O(n)*, not free. Inside
  tight loops, prefer index variables to slices.
- **`in` is substring search**, not character check. For a single
  character, `"a" in s` is *O(n)*. For "is this letter present?"
  on lots of strings, a set is faster.
- **`.split()` with no argument** splits on whitespace runs and
  drops leading/trailing. `.split(' ')` splits on every space
  including consecutive ones. They are different!
- **`.find(sub)` returns -1 on miss**, not None. `if s.find("x")`
  is a bug — it's True for index 0. Use `if "x" in s` for
  presence.

## 7. The canonical-form trick (group by signature)

A surprising number of string problems reduce to "group by a
canonical signature." The signature is a string or tuple that is
the same for every member of an equivalence class.

**Anagrams**: canonical form = `tuple(sorted(s))`. Two strings
are anagrams iff their canonical forms are equal.

```python
def group_anagrams(words):
    from collections import defaultdict
    groups = defaultdict(list)
    for w in words:
        groups[tuple(sorted(w))].append(w)
    return list(groups.values())
```

**Isomorphic strings**: canonical form = tuple of first-
occurrence indices. Two strings are isomorphic iff their tuples
match.

**Equivalent words under some relation**: pick a canonical
representative, use it as the dict key.

The pattern: **canonicalize, then equate**. When the problem
defines equivalence in a way you can compute, choose a canonical
form and reduce equality to dict-key equality.

## 8. Common slicing and indexing gotchas

**Gotcha 1: negative indices.** `s[-1]` is the last character.
`s[-2]` is the second-last. Use these — they make code more
readable than `s[len(s) - 1]`.

**Gotcha 2: slicing is forgiving.** `s[100:200]` on a length-5
string returns an empty string, not an error. This can hide bugs:
if your slice computation produces wrong bounds, you may get an
empty result without any signal that something is wrong.

**Gotcha 3: `s[::-1]` reverses but allocates.** It is the idiomatic
way to reverse, but it creates a new string of size `n`. For
very long strings inside tight loops, consider whether you really
need the reverse or whether a backward iteration would do.

**Gotcha 4: comparing characters with the wrong operator.** Use
`==`, not `is`. `s[0] is 'a'` might work in your tests because of
interning, but it is comparing identity rather than value. Use
`==` for character comparison.

**Gotcha 5: confusing single character with single-character
string.** Python has no separate char type. `s[0]` is a string
of length 1, not a character. This rarely causes problems but
can confuse beginners coming from C/Java.

## 9. The two-pointer family on strings

Many medium string problems are two-pointer or sliding-window.
The two flavours:

**Opposite ends**: typically for palindrome check, reverse, or
"check that two ends agree."

```python
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True
```

**Same direction (fast / slow)**: typically for compaction or
window-based summaries.

```python
def remove_char(s, c):
    write = 0
    chars = list(s)
    for read in range(len(chars)):
        if chars[read] != c:
            chars[write] = chars[read]
            write += 1
    return "".join(chars[:write])
```

If you have read the two-pointer chapter, all of this should feel
familiar. The pattern is the same; the elements are characters
instead of numbers.

## 10. The sliding-window family on strings

Sliding window with strings is so common it has its own chapter.
The signature template:

```python
left = 0
state = {}  # something that summarizes the current window
for right, ch in enumerate(s):
    # add ch to state
    while state_is_invalid():
        # remove s[left] from state
        left += 1
    # window [left, right] is valid; record answer
```

This skeleton solves longest substring without repeating
characters, longest substring with at most K distinct, minimum
window substring, longest substring of replaceable characters,
and so on. The "state" varies; the skeleton stays the same.

## 11. The pattern-matching family (advanced glimpse)

Once you go beyond beginner string DSA, you meet algorithms like
KMP, Z-algorithm, and Rabin-Karp. These are *O(n + m)*
substring-search algorithms that beat the naive *O(n × m)*. They
appear in this curriculum's Step 18 (Advanced Strings).

You do not need them for most interview problems — `"sub" in s`
is fine. But knowing they exist is useful for problems involving
periodicity, longest proper prefix that is also a suffix, and
similar.

For now, treat them as the dragons-be-here corner of strings.
Come back to them after you have mastered the basics.

## 12. Common beginner mistakes (and fixes)

**Mistake 1: comparing characters with `is` instead of `==`.**
`is` checks identity, `==` checks value. Always use `==` for
characters (and strings in general).

**Mistake 2: assuming `.find()` returns boolean.** It returns the
index, or -1 if missing. `if s.find("x"):` is buggy because 0 is
falsy. Use `if "x" in s` for presence.

**Mistake 3: forgetting that slicing copies.** `s[1:]` builds a
new string. Inside a hot loop, prefer to carry an index variable
and avoid slicing.

**Mistake 4: confusing characters and digits in input.** When you
read digits with `input()`, you get a string. If you want them
as integers: `[int(c) for c in s]` or `int(s)` for the whole
thing.

**Mistake 5: `s += "x"` inside a loop.** As covered above, this
is *O(n²)*. Build a list, then join.

**Mistake 6: `s.split(' ')` when you wanted `.split()`.** With
extra spaces in the input, the argumentless form is almost always
what you want.

## 13. End-of-chapter exercise

Solve these five problems with strings as your primary topic.
Before coding, ask yourself: "is this index-walking, two-pointer,
sliding window, or canonical-form grouping?"

1. **Valid palindrome (alphanumeric only).** Ignore non-letters
   and case. LeetCode 125.
2. **Longest common prefix of an array of strings.** LeetCode 14.
3. **Group anagrams.** Already covered above; reimplement.
   LeetCode 49.
4. **Longest substring without repeating characters.** Sliding
   window. LeetCode 3.
5. **Roman to integer.** Parse a Roman numeral string into its
   value. LeetCode 13.

These five hit four different patterns. After all five, string
DSA should feel mechanical.

## 14. The Unicode story — and why it sometimes bites

Most beginners never think about Unicode. Then one day they
process a username that contains an emoji, and `len()` returns
something they didn't expect. Let me sketch the story.

A **character** is what you see on the screen — the letter `A`,
the digit `7`, the punctuation `?`, the emoji 😀. A **code point**
is the numeric ID that Unicode assigns to a character — `A` is
65, `?` is 63, 😀 is 128512. Python strings are sequences of
**code points** (in CPython, abstractly). `ord(c)` gives you the
code point of a one-character string; `chr(n)` gives you the
character for a code point.

For ASCII characters (codes 0–127), one character = one code
point = one byte when encoded as UTF-8. For accented Latin
characters, Greek, Cyrillic, etc., one character = one code point
= 2 bytes in UTF-8. For Chinese, Japanese, Korean, most code
points take 3 bytes in UTF-8. Emojis often take 4 bytes.

When you call `len("hello")` in Python 3, you get `5`. When you
call `len("😀")` you get `1` — because Python counts code points,
not bytes. The byte length is recoverable via `len("😀".encode())`,
which returns `4`. The encoded bytes-string and the original
string are two different views of the same characters.

For DSA problems you can usually pretend strings are ASCII and
not worry about Unicode at all. Striver's A-Z sheet does this.
But know that the story is real, and that one day you will read
a username or file name that breaks your assumptions, and now
you'll know where to look.

## 15. Hashing strings — looking ahead

Strings can be **hashed** for fast comparison. The simplest hash
is the built-in `hash(s)` in Python, which assigns a (probably
unique) integer to each string. Equality on strings is *O(n)* in
the worst case — Python has to compare every character. But
checking if a string is in a `set` or used as a `dict` key is
*O(1) average* — because Python hashes the string once and uses
that hash to jump to the right bucket. (The hash itself takes
*O(n)* on the first computation; CPython caches it on the string
object, so subsequent operations on the same string are *O(1)*.)

For polynomial **rolling hashes** — used in Rabin-Karp,
duplicate-substring detection, and many other algorithms — we
compute the hash of a substring `s[i..j]` as a polynomial in
some base, modulo some large prime. As the window slides, we can
update the hash in *O(1)* by subtracting the old front character's
contribution and adding the new back character's contribution.
The full story is in Step 18 (Advanced Strings), but file the
preview away — rolling hashes are one of the most beautiful
techniques in DSA.

## 16. String-DP intuition — looking ahead

A whole family of DP problems lives on pairs of strings: longest
common subsequence (LCS), edit distance, shortest common
supersequence, distinct subsequences, regex/wildcard matching.
The common pattern: `dp[i][j]` summarizes some answer for the
prefix `s1[0..i-1]` paired against the prefix `s2[0..j-1]`, and
the transition is "if `s1[i-1] == s2[j-1]`, do X; else do Y."

You will meet these problems in Step 16 (Dynamic Programming).
The reason I mention them here is to plant a seed: when you see
a string-pair problem and the answer involves "matching letters
in order," reach for 2D string DP. The Cartesian grid `(i, j)`
of prefix-pair states is the canonical state space for these
problems.

Another string-DP family is **palindromic** — longest palindromic
substring, longest palindromic subsequence, minimum cuts to
partition into palindromes. These can usually be solved by
either (a) the LCS-of-string-and-its-reverse trick, or (b)
expanding around each center, or (c) Manacher's algorithm
(advanced).

## 17. Tries — looking further ahead

When you have **many** strings and want to ask prefix-related
questions ("which words start with `app`?", "is `apple` stored?",
"what is the longest stored prefix of `applejuice`?"), the right
data structure is a **trie**. A trie is a tree where each path
from the root spells a string and shared prefixes share branches.
It is the natural structure behind autocomplete, spell-checkers,
IP routing tables, and the longest-common-prefix family of
problems.

We will spend a whole chapter on tries in Step 17. Until then,
keep this in mind: any time a problem talks about prefixes,
shared starts, or "many strings, look up fast," the trie is
likely your friend.

## 18. The full string toolbox — reference card

A reference card of the string idioms you will use most. Tape
this somewhere you can see it.

**Building a string fast** — never use `+=` in a loop. Use
`''.join(parts)`.

**Reversing** — `s[::-1]`.

**Lowercasing for case-insensitive compare** — `s.lower()`. Or
`s.casefold()` for locale-aware comparison.

**Checking character classes** — `c.isdigit()`, `c.isalpha()`,
`c.isalnum()`, `c.isspace()`. All return booleans.

**Numeric conversion of a digit char** — `ord(c) - ord('0')`.
Returns 0..9 for chars '0'..'9'.

**Lowercase letter as index 0..25** — `ord(c) - ord('a')`. Useful
for fixed-size frequency arrays.

**Counting characters** — `Counter(s)` from `collections`. Or
`s.count(ch)` for a single character.

**Two strings are anagrams** — `Counter(s1) == Counter(s2)` (or
`sorted(s1) == sorted(s2)`, which is *O(n log n)*).

**Splitting a sentence into words** — `s.split()` (with no
argument splits on any whitespace; preferred for free-form text).

**Joining words back** — `' '.join(words)`. The separator can
be any string.

**Stripping whitespace** — `s.strip()`, `s.lstrip()`, `s.rstrip()`.
Pass an argument to strip specific characters: `s.strip(',.?!')`.

**Substring search** — `s.find(sub)` returns the index or `-1`.
`s.index(sub)` raises if missing. `sub in s` returns boolean.

**Substring count (non-overlapping)** — `s.count(sub)`.

**Replace** — `s.replace(a, b)`. Pass a count to limit replacements.

**Check prefix/suffix** — `s.startswith(p)`, `s.endswith(p)`.
Both can take tuples: `s.startswith(('a', 'b'))`.

**Padding** — `s.zfill(5)` pads with leading zeros to length 5.
`s.ljust(10)`, `s.rjust(10)`, `s.center(10)` pad with spaces.

**Format numbers** — `f"{value:.2f}"`, `f"{value:,}"`,
`f"{value:>10}"`. f-strings are powerful, learn them.

If you don't know one of these by heart, look it up *once* and
then drill it into reflex. Idioms speed up both writing and
reading.

## 19. Common bugs — extended catalog

I gave you confusion notes earlier. Here is the longer catalog of
string-specific bugs.

**Mutating attempts.** `s[0] = 'H'` raises `TypeError`. Strings
are immutable. Build a new string or use a list of characters.

**The `is` vs `==` trap.** `s1 == s2` checks equality. `s1 is s2`
checks identity (same object in memory). Python interns short
strings, so sometimes `is` accidentally works — but it is not
reliable. Always use `==` for value comparison.

**Forgetting that string slices copy.** `s[a:b]` builds a new
string of length `b - a`. Inside a loop this becomes *O(n²)*
total. For tight loops, use indices directly.

**Using `+=` for string building.** In Python this is *O(n²)*
total in a loop. Use a list and `join` at the end:

```python
# bad
result = ""
for x in things:
    result += str(x)
# good
parts = []
for x in things:
    parts.append(str(x))
result = "".join(parts)
```

**Index out of range on empty strings.** `s[0]` on `""` raises
`IndexError`. Always check `if not s:` first if your algorithm
might see empty input.

**Locale-dependent case folding.** `'I'.lower()` returns `'i'`
in most locales, but Turkish `'I'.lower()` is `'ı'` (dotless i).
For pure-ASCII problems this doesn't matter; for international
text, use `casefold()` rather than `lower()`.

**Splitting on whitespace vs a single space.** `'a  b'.split(' ')`
gives `['a', '', 'b']` (note the empty string between two
spaces). `'a  b'.split()` (no argument) gives `['a', 'b']`
(splits on any run of whitespace). Different behaviors;
choose deliberately.

**The "stripchars are a set" surprise.** `s.strip("abc")` strips
*any* of `a`, `b`, or `c` from each end — not the literal
substring `"abc"`. People misread this constantly.

**Off-by-one in palindrome bounds.** Two-pointer palindrome
checks: the loop condition is `while left < right`. Stop when
they meet or cross; do not double-check the middle element.

**Forgetting that `replace` does *all* occurrences.** Pass a
count if you only want to replace the first few.

**Mixing bytes and strings.** In Python 3, `b'hello'` and
`'hello'` are different types. Concatenating them raises a
`TypeError`. Encode/decode explicitly when crossing the boundary.

## 20. Mental practice exercises (no code)

Before you close this chapter, work these in your head.

1. *Take `s = "racecar"`. Walk the two-pointer palindrome check.
   What positions do `left` and `right` visit, and when does the
   loop end?*

2. *Why is `"aab" == "aab"` always `True` in Python, even though
   they are technically two different string objects? (Hint:
   interning.)*

3. *On `s = "abcabcbb"`, walk the sliding-window "longest
   substring without repeating characters" algorithm in your
   head. When does the left pointer move? What is the answer?*

4. *Given `words = ["bat", "tab", "cat", "atc"]`, what is the
   canonical form for grouping anagrams? Which words end up in
   which groups?*

5. *Why does `"".join(["a", "b", "c"])` cost *O(n)* total, but
   `result = ""; for x in ["a", "b", "c"]: result += x` cost
   *O(n²)* total? Where does the difference come from?*

6. *Construct two strings of length 10⁶ that differ only at the
   last character. Comparing them with `==` is *O(n)*. Hashing
   them is also *O(n)*. So when does hashing help? (Hint: think
   about doing many comparisons against the same target.)*

If all six feel comfortable, you have absorbed this chapter. If
not, scroll back to the matching section.

## 21. Where to go next

- **Step 5 (strings)** — easy and medium string problems.
- **Step 7 (recursion)** — recursive parsing, palindrome
  partitioning.
- **Step 10 (sliding window)** — many string problems live here.
- **Step 17 (tries)** — prefix-based string structures.
- **Step 18 (advanced strings)** — KMP, Z, Rabin-Karp.

Strings are the lingua franca of programming interviews. Spend
the practice time — the muscle pays off everywhere else.

## 22. The closing pep talk

You have just absorbed more about strings than most working
programmers ever think about. The reward is that *all* your
future string work — interview problems, log parsers, ORMs,
templating engines, JSON handling, search indexes — will feel
less mysterious. Strings are not "just text." They are arrays of
code points with immutable storage and rich library support. Now
you know what's under the hood, and you can reach for the right
tool by reflex.

Take a break. When you come back, work through the practice
problems in Step 5. Your string intuition has somewhere to land
now.
''',
}
