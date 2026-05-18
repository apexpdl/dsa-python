"""Hashing — turning lookups from a search into a teleport."""

LESSON = {
    "id": "hashing",
    "title": "Hashing — The Power of Instant Lookup",
    "tags": ["hashing", "dict", "set", "fundamentals"],
    "summary": (
        "Why dictionaries and sets feel like magic, where the magic "
        "comes from, and the small handful of patterns that turn most "
        "'find / count / pair' problems into one-pass solutions."
    ),
    "body": r'''
## The problem hashing solves

Suppose I give you a list of one million numbers and ask: *"Is 42 in
this list?"* If you have no preparation, you have no choice — you walk
through the list one number at a time, top to bottom, until you find
42 or run out. That is *O(n)* work. Now I ask the same question again,
for 17. You walk through again. And again for 99. Every question costs
another full pass.

This feels wasteful, and it is. We are not learning anything between
questions. Hashing is the trick that lets us prepare the data once so
that every "is X in here?" question afterward becomes instant.

## The intuition: a bookshelf with labelled shelves

Imagine a library, except the librarian has a special rule: she takes
the title of every book and reduces it to a number between 0 and 999,
using some clever formula. Then she puts the book on shelf number
"that". To find *Moby-Dick*, you do not search every shelf. You
compute the same number for "Moby-Dick", walk straight to that shelf,
and look at the (usually very small) number of books sitting there.

That formula is a **hash function**. The shelves are **buckets**. The
whole arrangement is a **hash table**. In Python, `dict` and `set` are
hash tables. The librarian works behind the scenes; you just say
`d[key]` and she walks to the right shelf for you.

When the hash function is well-designed and the shelves are spread
out, almost every shelf has only one or two books on it, so lookups
take constant time on average. That is the whole reason we say a dict
lookup is *O(1)*.

## When to reach for hashing

A few unmistakable signals:

1. **"Have I seen this before?"** A `set` is the answer. The classic
   example is detecting duplicates in a stream of values.
2. **"How many of each?"** A `dict` (or `collections.Counter`) is the
   answer. Whenever a problem asks for frequencies, hashing is almost
   always the right hammer.
3. **"For each value, does another specific value also exist?"**
   Build a set once, then ask one question per element. Two-Sum is the
   poster child.
4. **"Group these things by some key."** A `dict` mapping key to a
   list of items collects groups in one pass.

If a problem fits one of those four shapes, your first instinct should
be hashing.

## Set: a bag with no duplicates and instant `in`

```python
seen = set()                 # empty set
seen.add(7)                  # add element
seen.add(7)                  # still just {7} — duplicates collapse
print(7 in seen)             # True  — average O(1)
print(8 in seen)             # False — average O(1)
seen.discard(7)              # remove without erroring if missing
```

Use a set when you only care about *presence*, not *counts*.

## Dict: a labelled set, where every label points to a value

```python
counts = {}                  # empty dict
counts["apple"] = 1
counts["banana"] = counts.get("banana", 0) + 1  # the "get with default" trick
print(counts)                # {'apple': 1, 'banana': 1}

# Iterating
for key, value in counts.items():
    print(key, value)
```

The single most useful method on `dict` for beginners is `.get(key,
default)`. It lets you say "give me the value, or this default if it
is missing" without writing an `if`. You will write that pattern a
thousand times.

## The frequency-counting pattern

```python
from collections import Counter

nums = [1, 2, 2, 3, 3, 3, 4]
freq = Counter(nums)
# Counter({3: 3, 2: 2, 1: 1, 4: 1})

freq[3]               # 3 — how many times 3 appeared
freq.most_common(2)   # [(3, 3), (2, 2)] — top-2 most frequent
```

`Counter` is a `dict` subclass that knows about counting. It is the
right tool for "highest frequency", "lowest frequency", "first
non-repeating character", "majority element", and similar.

## A worked example: two-sum

> Given a list of numbers and a target, return any pair of indices
> whose values sum to the target.

Brute force is obvious: try every pair. That is *O(n²)*. Hashing
collapses it to one pass. The insight is "for each number `x`, I
already know what its partner would be: `target - x`. If I've already
seen that partner, I'm done. Otherwise I remember `x` for the future."

```python
def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    seen = {}                     # value -> index
    for i, x in enumerate(nums):
        partner = target - x
        if partner in seen:       # we met partner earlier; pair found
            return (seen[partner], i)
        seen[x] = i               # remember current value for the future
    return None
```

Notice how the two-pass scan ("for each pair") collapses into a single
pass because the hash remembers everything we have seen. This is the
**meet-the-other-half** pattern, and it is one of the most reused
ideas in this whole sheet.

## What can hashing not do?

Hashes are unordered. If a problem cares about *order* or *range*
("how many elements between 5 and 10?"), a hash is not your tool —
you want a sorted structure or a BIT/segment tree. Hashes also have
*amortized* constant-time guarantees, which means an adversarial
worst case can be slow. For interviews this rarely matters, but
remember it exists.

## Common beginner mistakes

**Mistake 1: hashing mutable objects.** You cannot use a `list` as a
dict key, because it can change underneath you. Use a `tuple` instead.
This is why "key by sorted characters" usually means
`key = tuple(sorted(s))`, not `key = sorted(s)`.

**Mistake 2: hashing floats.** Floating-point equality is unreliable.
Avoid using floats as keys; convert to a rounded int or a string
representation first.

**Mistake 3: using a dict where a `Counter` would have been clearer.**
If you find yourself writing `d[k] = d.get(k, 0) + 1` everywhere,
switch to `Counter`. Beginners think `Counter` is fancy, but it is
just a friendlier dict.

**Mistake 4: assuming dict iteration is random.** Since Python 3.7, dict
iteration is in *insertion order*. This is a real guarantee. Many
problems exploit it (LRU cache, for instance). But the elements are
still not *sorted* by key — order is insertion, not value.

## The mental model

Whenever you find yourself about to write a nested loop because you
need to "find" or "count" or "pair", pause for a moment and ask:
*could a dict or a set let me do this in one pass?* If yes, you have
just turned an *O(n²)* solution into *O(n)*. That single instinct
makes a stunning fraction of Step 3, Step 5, and Step 10 problems
collapse into easy wins.
''',
}
