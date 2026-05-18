"""Strings — arrays of characters, with twists."""

LESSON = {
    "id": "strings",
    "title": "Strings — Arrays With Extra Rules",
    "tags": ["strings", "beginner", "fundamentals"],
    "summary": (
        "Strings feel different from arrays, but they're just arrays of "
        "characters that you cannot edit in place. Once you accept that, "
        "all the string tricks fall into place."
    ),
    "body": r'''
## A string is an array of characters

If arrays are rows of numbered parking spots, a string is the same
parking lot — except each spot holds a single character instead of a
number, and you have to promise not to repaint the spots after the lot
opens. That promise is what "immutable" means in Python.

```python
s = "hello"
print(s[0])   # 'h' — same indexing as a list.
print(s[-1])  # 'o' — negative indices count from the end.
print(s[1:4]) # 'ell' — same slicing rules as lists.
```

So far, strings look exactly like lists. And in fact, you can almost
always pretend they are.

## The catch: you cannot change a character in place

```python
s = "hello"
s[0] = "H"   # TypeError: 'str' object does not support item assignment
```

This is not a flaw. It is the rule. In Python, once you make a string,
that exact string can never change. If you want a different string,
you have to **build a new one**. Beginners feel this as friction, but
it leads to two huge benefits:

1. Strings are safe to share. Two variables pointing at the same string
   can never be surprised by an edit from far away.
2. Strings can be used as dictionary keys, because their identity is
   stable.

The mental model: think of a string as a **photo**. You cannot change
the photo. You can crop it, glue it next to another photo, or describe
it. But every operation produces a new photo.

## How do you "edit" a string then?

You build a list of characters, edit the list, and `"".join()` it
back. This is the canonical Python pattern.

```python
s = "hello"
chars = list(s)   # ['h', 'e', 'l', 'l', 'o'] — now we have a mutable copy.
chars[0] = "H"    # change the first character
s_new = "".join(chars)  # 'Hello' — a brand new string built from the list.
```

If you remember exactly one trick from this lesson, remember this one.
"Convert to list, edit, join back" is a string-builder's bread and
butter.

## The bread-and-butter operations

```python
s = "racecar"

# Length
len(s)             # 7

# Reverse
s[::-1]            # 'racecar' — slice with step -1 walks the string backwards.

# Lowercase / uppercase
s.lower()          # 'racecar'
s.upper()          # 'RACECAR'

# Check what kind of character we have
"a".isalpha()      # True — a letter
"7".isdigit()      # True — a digit
" ".isspace()      # True — whitespace

# Concatenation
"foo" + "bar"      # 'foobar' — but be careful inside loops; see below.

# Membership
"ace" in s         # True — substring search, runs left to right.
```

## The "+=" inside a loop trap

```python
# Slow: builds a brand new string every iteration. O(n^2) overall.
result = ""
for ch in big_string:
    result += ch
```

Because strings are immutable, `result += ch` cannot extend the old
string. It has to allocate a new string, copy every character that was
already there, and add the new character. If you do this `n` times,
that is `1 + 2 + 3 + ... + n` ≈ `n²/2` character copies. For
`n = 10,000` that is fifty million tiny copies, when the answer should
have been ten thousand.

The fix:

```python
# Fast: append into a list of pieces, then join once at the end.
pieces = []
for ch in big_string:
    pieces.append(ch)
result = "".join(pieces)
```

The list lets us append in constant time, and `join` walks the list
exactly once. The total work is *O(n)* instead of *O(n²)*.

## Characters are tiny integers (and we can do math on them)

Python does not have a "char" type; every character is a one-letter
string. But we have two functions that link characters to numbers:

```python
ord('a')   # 97 — the Unicode code point of 'a'
chr(97)    # 'a' — the character whose code point is 97
ord('A')   # 65 — uppercase letters are 32 below their lowercase twins
ord('z') - ord('a')   # 25 — there are 26 letters in the English alphabet
```

This unlocks a huge family of tricks. If you have a string of
lowercase letters and you want to count them, you do not need a
dictionary; a 26-length array indexed by `ord(c) - ord('a')` does the
job. Anagrams, character frequencies, and isomorphic-string problems
all use this idea.

```python
def char_counts(s: str) -> list[int]:
    """Count occurrences of each lowercase letter in s."""
    counts = [0] * 26                  # 26 buckets, one per letter
    for ch in s:                       # walk every character
        counts[ord(ch) - ord('a')] += 1
    return counts
```

## Common beginner mistakes

**Mistake 1: comparing characters with the wrong function.** Use `==`
to compare characters, not `is`. `s[0] is 'a'` happens to work
sometimes because of interning, but it is the wrong tool — comparing
identity, not value.

**Mistake 2: assuming `.find()` returns a boolean.** It returns the
index, or **-1** if the substring is missing. So `if s.find("x"):` is
buggy: it is true even when `find` returns 0 (a real match at the
start). Use `if "x" in s` for presence, and reserve `.find` for when
you need the position.

**Mistake 3: forgetting that slicing copies.** Just like with lists,
`s[1:]` builds a new string. Inside a tight loop, prefer carrying an
index variable.

**Mistake 4: confusing characters and integers in input.** When you
read a line of digits with `input()`, you get a string. If you want
the digits as integers, you have to convert: `[int(c) for c in s]`.

## The mental model you carry forward

When a problem says "string", picture a list of characters that you
cannot rewrite in place. To "edit", make a list, change it, and join
back. To count letters, use a 26-length array (or a `Counter`). To
compare strings character by character, use two indices and walk them
together. To search for a substring, in real life you call `in` or
`.find`; in interviews you may need to implement KMP or Rabin–Karp,
but those come later (Step 18).

Strings will haunt you in linked lists, in tries, in DP — get
comfortable with them now and the rest of the journey gets noticeably
easier.
''',
}
