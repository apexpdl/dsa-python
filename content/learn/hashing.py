"""Hashing — turning lookups from a search into a teleport."""

LESSON = {
    "id": "hashing",
    "title": "Hashing — The Power of Instant Lookup",
    "tags": ["hashing", "dict", "set", "fundamentals"],
    "summary": (
        "A full beginner chapter. Why dictionaries and sets feel like "
        "magic, where the magic comes from, the small handful of "
        "patterns that turn most 'find / count / pair' problems into "
        "one-pass solutions, and the discipline of choosing between "
        "set, dict, and Counter."
    ),
    "body": r'''
## 0. The promise of this chapter

Hashing is the single most useful idea in interview-level DSA. If
you learn nothing else about data structures, learn how to use a
hash map well. The number of problems that collapse from `O(n²)`
to `O(n)` purely by "use a dict" is staggering.

The good news: in Python, hashing is built into the language. You
already know `dict` and `set`. The challenge is not the syntax —
it is recognizing **when** to reach for them, and **how** to
structure the keys.

This chapter walks slowly through the why and the when. By the end
you should be reflexively asking "could a dict turn this nested
loop into a single pass?" whenever you face a new problem.

## 1. The problem hashing solves

Suppose I hand you a list of one million numbers and ask: *"Is 42
in this list?"* If you have no preparation, you have no choice —
you walk through the list one number at a time until you find 42
or run out. That is *O(n)* work for a single question.

Now I ask the same question for 17. You walk through again. And
again for 99. Every question costs another full pass. We are
asking the same kind of question over and over but learning
nothing between questions.

Hashing is the trick that lets us **prepare the data once** so
that every "is X in here?" question afterward becomes
**instant** — *O(1)* on average.

That is the basic value proposition. Pay an *O(n)* up-front cost
to build the structure; reap *O(1)* per query for every query
afterward. If you have many queries, the up-front cost pays for
itself many times over.

## 2. The library shelf analogy

Pictures help. Imagine a library where each book gets a card on
which the librarian writes a number — between, say, 0 and 999.
The number is computed from the book's title via some fixed
formula (long titles still produce one number; common letters
still produce one number; you get the idea). Then the book goes
on shelf number "that."

When you want *Moby-Dick*, you do not walk the entire library.
You compute the same number for "Moby-Dick," walk straight to
that shelf, and look at the (usually small) number of books
sitting there.

That formula — title → number — is a **hash function**. The
shelves are **buckets**. The whole arrangement is a **hash
table**. Looking up a book by title takes constant time on
average: compute the hash, jump to the shelf, scan a tiny number
of books.

In Python, `dict` and `set` are hash tables. The librarian works
behind the scenes; you just say `d[key]` and she walks to the
right shelf.

When the hash function is well-designed and the data is spread
out, almost every shelf has only one or two books. Lookups are
*O(1)* on average. The worst case is *O(n)* (every key hashes to
the same shelf), but in practice this almost never happens with
the high-quality hash functions Python uses.

## 3. When to reach for hashing

There are four unmistakable signals. When you see any of them, the
first instinct should be "use a hash."

**Signal 1: "Have I seen this before?"** — A `set` is the answer.
The classic example is detecting duplicates in a stream of values.

**Signal 2: "How many of each?"** — A `dict` (or `Counter`) is
the answer. Whenever a problem asks for frequencies, hashing is
almost always the right hammer.

**Signal 3: "For each X, does the partner Y exist?"** — Build a
set once, then ask one question per element. Two Sum is the
canonical example.

**Signal 4: "Group these things by some key."** — A `dict`
mapping key to a list of items collects groups in one pass.
Group anagrams is the canonical example.

If a problem fits one of those four shapes, hashing is the first
tool to try. Even if hashing is not the final answer, framing the
problem this way often suggests a better one.

## 4. Set: a bag with no duplicates and instant `in`

```python
seen = set()                # empty set
seen.add(7)                 # add element
seen.add(7)                 # duplicate — set stays {7}
print(7 in seen)            # True (O(1) average)
print(8 in seen)            # False (O(1) average)
seen.discard(7)             # remove if present; no error if absent
```

Use a set when you only care about **presence**, not **counts**.

Common patterns:

- **Detect duplicates**: walk the array; for each element check
  `if x in seen: return True; seen.add(x)`.
- **Set intersection**: `seen.intersection(other)` (or `&`)
  returns the common elements of two sets.
- **Deduplicate**: `list(set(items))` gives a list of unique
  values (order may not be preserved in older Python; from 3.7+
  insertion order is preserved through dict, but not through
  set).

Sets cannot store mutable objects (like lists). Their elements
must be hashable. If you need to use a list as a set member,
convert it to a tuple first.

## 5. Dict: a labelled set, where every label maps to a value

```python
counts = {}                 # empty dict
counts["apple"] = 1
counts["banana"] = counts.get("banana", 0) + 1
# {'apple': 1, 'banana': 1}

for key, value in counts.items():
    print(key, value)
```

The single most useful method on `dict` for beginners is
`.get(key, default)`. It returns the value if the key exists, the
default otherwise. This lets you write `counts[k] = counts.get(k,
0) + 1` to increment a count without first checking whether the
key exists.

You will write that exact pattern hundreds of times. Get it into
your fingers.

A close cousin is `dict.setdefault(key, default)`. It returns the
value if the key exists, otherwise sets it to `default` and
returns `default`. Useful for building dicts of lists:

```python
groups = {}
for item in items:
    groups.setdefault(group_of(item), []).append(item)
```

A cleaner version uses `collections.defaultdict(list)`:

```python
from collections import defaultdict
groups = defaultdict(list)
for item in items:
    groups[group_of(item)].append(item)
```

`defaultdict` auto-creates the default value the first time a key
is accessed. No more `.get(...)` boilerplate.

## 6. The frequency-counting pattern

```python
from collections import Counter

nums = [1, 2, 2, 3, 3, 3, 4]
freq = Counter(nums)
# Counter({3: 3, 2: 2, 1: 1, 4: 1})

freq[3]                    # 3 (how many times 3 appeared)
freq.most_common(2)        # [(3, 3), (2, 2)] — top-2 by count
```

`Counter` is a `dict` subclass purpose-built for counting. Prefer
it over hand-rolled count loops when you only need frequencies. It
runs in optimized C, so it is faster than a manual `for` loop.

Counter also supports:
- **Arithmetic**: `Counter(a) - Counter(b)` returns counts that
  remain after subtraction. Useful for "are these two multisets
  equal?" or "what is the difference?"
- **`update`**: add counts from another iterable.
- **`elements`**: iterate over each key as many times as its
  count.

For "anagram detection" the canonical line is:

```python
def are_anagrams(a, b):
    return Counter(a) == Counter(b)
```

One line. Cleaner than sorting both strings and comparing.

## 7. A worked example: Two Sum

> Given a list of numbers and a target, return any pair of indices
> whose values sum to the target.

Brute force: try every pair. Two nested loops. *O(n²)*.

The hash insight: for each element `x`, we already know what its
partner must be — `target - x`. If we have already seen that
partner, we are done. Otherwise we remember `x` for the future.

```python
def two_sum(nums, target):
    seen = {}                    # value -> index
    for i, x in enumerate(nums):
        partner = target - x
        if partner in seen:
            return (seen[partner], i)
        seen[x] = i
    return None
```

A single pass. We use a dict (not a set) because we want to
return the **indices**, not just confirm the pair's existence.

This is the **meet-the-other-half** pattern. Once you spot it,
you start seeing it everywhere:

- 3-Sum: fix one number, use Two Sum on the rest.
- Subarray sum equals K: prefix sums + meet-the-other-half.
- Longest substring without repeating: hash of "last index of
  each character."
- First non-repeating character: hash of counts + a second
  pass.

The pattern is "for each new element, ask one question of the
past — and the dict makes asking that question free."

## 8. What can hashing not do?

Two real limitations.

**1. Hashes are unordered.** If a problem cares about *order* or
*range* ("how many elements are between 5 and 10?", "what is the
k-th smallest?"), a hash is the wrong tool. You want a sorted
structure (balanced BST, sorted list with binary search) or a
specialized structure (Fenwick tree, segment tree).

**2. Hashes have amortized guarantees, not worst-case.** An
adversarial input can in theory make every key collide,
degrading lookups to *O(n)*. In practice this requires a
deliberate attacker who knows the hash function (which is why web
servers use randomized hash seeds). For interview purposes,
hashes are *O(1)* on average and you can quote that with
confidence.

Other minor caveats:

- Keys must be **hashable**. Lists and dicts are not hashable;
  tuples and frozensets are. If you want to key on a "list of
  things," convert it to a tuple first.
- Floats are hashable but their equality is fragile. Avoid float
  keys unless you really need them.
- Custom objects need to implement `__hash__` and `__eq__`
  consistently. The default for objects is identity-based, which
  is rarely what you want.

## 9. Worked example: group anagrams

> Given a list of strings, group them by anagram class.

The canonical form of an anagram is its sorted-character tuple.
"eat", "tea", "ate" all have canonical form `('a', 'e', 't')`.

Group by canonical form using a dict:

```python
from collections import defaultdict

def group_anagrams(words):
    groups = defaultdict(list)
    for w in words:
        key = tuple(sorted(w))
        groups[key].append(w)
    return list(groups.values())
```

*O(N × K log K)* where N is the number of strings and K is the
average length. Each string is sorted once, hashed once, and
appended to its group.

This "canonicalize, then group" pattern recurs constantly:

- Group anagrams → sort characters.
- Group isomorphic strings → first-occurrence-index pattern.
- Group equivalent subtrees → serialized subtree string.

The mental motion: pick a canonical representative for each
equivalence class, then group by canonical form.

## 10. Common beginner mistakes

**Mistake 1: hashing mutable objects.** You cannot use a list as
a dict key, because lists are mutable. Use a tuple instead.

**Mistake 2: hashing floats.** Floating-point equality is
unreliable. `0.1 + 0.2 != 0.3` in Python. Avoid float keys;
convert to rounded int or string first.

**Mistake 3: using a dict when a Counter would be cleaner.** If
you find yourself writing `d[k] = d.get(k, 0) + 1` everywhere,
switch to `Counter`. Beginners think `Counter` is "advanced," but
it is just a friendlier dict.

**Mistake 4: assuming dict iteration is random.** Since Python
3.7, dict iteration is in **insertion order**. This is a real,
guaranteed contract. Many problems exploit it (LRU cache, for
instance). But the elements are not **sorted** by key — they are
in the order you inserted them.

**Mistake 5: forgetting to handle the case where the key is
absent.** `d[k]` raises `KeyError` if `k` is missing. Use
`d.get(k)` (returns `None`), `d.get(k, default)`, or `if k in d`
to check first.

**Mistake 6: using `dict[]` access in a hot loop where `.get(...)`
would be cleaner.** Both are *O(1)* average, but `.get()` avoids
the exception-handling overhead when keys are sometimes missing.

## 11. The hash function (a brief glimpse)

You do not need to know how Python computes hashes to use them.
You should know it exists.

A hash function takes any input (string, number, tuple) and
returns an integer. The function is **deterministic** (same input
always produces the same hash) but designed so that small
differences in input cause large differences in hash — a property
called "avalanche."

The hash modulo the table size determines which bucket the entry
goes into. When two keys hash to the same bucket, the dict stores
both in the bucket and disambiguates via equality check. This is
called a **collision**, and a well-designed hash function makes
collisions rare.

Python's `hash()` function works on any hashable object:

```python
hash("hello")          # some integer
hash(42)               # 42 (small ints hash to themselves)
hash((1, 2, 3))        # works on tuples
hash([1, 2, 3])        # TypeError — lists are not hashable
```

For interview purposes you do not need to worry about hash
functions. The abstraction "dict and set are *O(1)* average" is
all you need.

## 12. Decision flowchart

When a problem walks in the door, ask these questions in order:

1. *"Do I need to know whether something is present?"* → set.
2. *"Do I need to know how many times something appeared?"* →
   Counter (or dict if you want to do something custom per
   element).
3. *"Do I need to look up something by key and get a value?"* →
   dict.
4. *"Do I need to group things by some key?"* → defaultdict(list)
   or `itertools.groupby` (after sorting).
5. *"Do I need order, range queries, or k-th smallest?"* → not
   hashing; reach for sorting, heaps, or sorted containers.

Internalize the flowchart. Run through it on the next ten
problems you see. You will find that maybe half of them have a
clean hash-based answer.

## 13. End-of-chapter exercise

Solve these five problems with hashing as your primary tool.
Before coding, name which signal applies (presence, count,
partner, group).

1. **First non-repeating character.** Given a string, return the
   first character that appears exactly once. LeetCode 387.
2. **Two Sum.** Already covered above; re-implement from scratch
   without looking. LeetCode 1.
3. **Group anagrams.** Already covered above; re-implement.
   LeetCode 49.
4. **Subarray sum equals K.** Count contiguous subarrays summing
   to K. Prefix sum + hash. LeetCode 560.
5. **Top K frequent elements.** Return the K most frequent
   values. Counter + sort (or Counter + heap). LeetCode 347.

These five exercises hit the four signals and the bonus "count
of patterns" extension. After all five, hashing should feel like
a reflex.

## 14. Where to go next

Hashing is the foundation for many later topics:

- **Step 3 (arrays)** — many medium array problems use hashing
  for `O(n)` solutions.
- **Step 10 (sliding window)** — the inside-window state is
  almost always a dict or Counter.
- **Step 14 (BST)** — for ordered queries, you graduate from
  hash sets to balanced BSTs.
- **Step 17 (Tries)** — for prefix queries, you graduate from
  dicts to trees of characters.

Hashing is also a baseline: if a problem has *any* "find /
count / pair" flavor, the hash solution is the first thing to
sketch. Even if you ultimately use a fancier structure, the hash
version usually gives you a correct baseline to compare against.

Take a breath. Reread anything that felt fast. Then go do the
five exercises. Hashing rewards practice — more than recursion,
more than DP. The reflex of "could a dict do this?" comes only
from solving twenty or thirty hash problems in a row.
''',
}
