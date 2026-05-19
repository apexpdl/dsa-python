"""Step 1 extras — Python basics, patterns, collections, and a few more.

These fill in the stub problems from Step 1 lectures 1, 2, 3, 4, 5,
and 6. The "Lecture 1" items are mostly syntax tours rather than
algorithmic puzzles, so they get a friendlier "what you need to
know" treatment than the standard six-section template.
"""
from __future__ import annotations

_STRIVER_SHEET = {
    "label": "Striver's A2Z DSA Course Sheet",
    "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
}


PROBLEMS: list[dict] = [
    # =================================================================
    # Lecture 1 — Things to Know in Python (8 problems, syntax tours)
    # =================================================================
    {
        "id": "user-input-output",
        "title": "User Input and Output in Python",
        "step_id": 1,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["python-basics", "io"],
        "what_this_teaches": (
            "How to read input from the user and print output. These "
            "are the two ends of every console program; you will use "
            "them in every single problem in this curriculum."
        ),
        "pattern": "input() reads strings; print() writes them.",
        "prerequisite_lessons": [],
        "prerequisite_problems": [],
        "next_problems": ["data-types", "if-else-statements"],
        "resources": [
            _STRIVER_SHEET,
            {
                "label": "Python docs — built-in input()",
                "url": "https://docs.python.org/3/library/functions.html#input",
            },
            {
                "label": "Python docs — built-in print()",
                "url": "https://docs.python.org/3/library/functions.html#print",
            },
        ],
        "understanding": r'''
Programs are conversations between you and the user. They have two
fundamental moves: **read what the user typed** and **print
something for the user to see**. Python provides these as two
built-in functions: `input()` for reading and `print()` for
writing.

Reading a line of input:

```python
name = input()              # waits for the user to type and press Enter
greeting = input("Name? ")  # the argument is shown as a prompt
```

`input()` always returns a **string**, even if the user types
something that looks like a number. If you want the number, you
have to convert:

```python
n = int(input())           # parse the line as an integer
x = float(input())         # parse as a floating-point number
```

If the user types something that is not a valid integer, `int()`
raises `ValueError`. Beginners often forget to convert and end up
treating numbers as strings — and `"5" + "3"` is `"53"`, not `8`.

Writing output:

```python
print("Hello, world!")
print(7)                   # numbers print fine; print() converts automatically
print("a", "b", "c")       # multiple args separated by spaces
print("a", "b", sep="-")   # custom separator
print("no newline", end="")  # suppress the trailing newline
```

`print()` ends with a newline by default. If you want to print
several things on the same line, either pass them all as one
`print` call (with `sep=`), or use `end=""`.

For reading **many numbers on one line** (a common
competitive-programming pattern):

```python
nums = list(map(int, input().split()))
# Input like "1 2 3 4 5" becomes nums = [1, 2, 3, 4, 5].
```

`input().split()` returns a list of whitespace-separated tokens.
`map(int, ...)` applies `int` to each. `list(...)` materializes the
result.

For reading **many lines**:

```python
n = int(input())
data = [int(input()) for _ in range(n)]
```

That covers 95% of input parsing you will ever do in this
curriculum.
''',
        "summary": r'''
**Pattern**: `input()` to read a string, convert with `int()` /
`float()` if you need a number; `print()` to write.

**Lesson**: input is always a string. Convert explicitly. Output
gets a newline by default; customize with `end=` or `sep=`.

**Recognize next time**: every problem on this site starts with
reading some input and ends with printing the answer. Burn the
parsing idioms above into your fingers.
''',
    },
    {
        "id": "data-types",
        "title": "Data Types in Python",
        "step_id": 1,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["python-basics", "types"],
        "what_this_teaches": (
            "The seven data types you will use constantly in this "
            "curriculum: int, float, bool, str, list, tuple, dict. "
            "Knowing what each one can and cannot do prevents whole "
            "classes of beginner bugs."
        ),
        "pattern": "Pick the right container for the job; check type() when confused.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["user-input-output"],
        "next_problems": ["if-else-statements", "for-while-loops"],
        "resources": [
            _STRIVER_SHEET,
            {
                "label": "Python docs — built-in types",
                "url": "https://docs.python.org/3/library/stdtypes.html",
            },
        ],
        "understanding": r'''
Python has many built-in types, but for DSA you really only need
a small handful. Here are the seven that come up in almost every
problem.

**Integer (`int`)** — whole numbers. Arbitrary precision, so they
never overflow. `7`, `-3`, `0`, `10**100` are all valid.

**Float (`float`)** — fractional numbers using IEEE 754 double
precision. About 15-17 significant digits of precision. `3.14`,
`1e-9`, `float('inf')`. Beware: floats are inexact. `0.1 + 0.2 !=
0.3` in Python (try it).

**Boolean (`bool`)** — `True` or `False`. Booleans are a subclass
of integers, so `True == 1` and `False == 0`. Useful for flags
and conditions.

**String (`str`)** — immutable sequence of characters. `"hello"`,
`'world'`. Strings cannot be modified in place; use the list-
edit-join trick from the Strings lesson.

**List (`list`)** — ordered, mutable sequence of any values.
`[1, 2, 3]`, `["a", "b"]`. The most-used container in DSA.
Indexable, sliceable, appendable.

**Tuple (`tuple`)** — ordered, immutable sequence. `(1, 2, 3)`.
Use tuples for fixed-size records (e.g., a 2D point) or as dict
keys (lists cannot be keys because they are mutable).

**Dictionary (`dict`)** — key-value mapping with *O(1)* average
lookup. `{"a": 1, "b": 2}`. The workhorse of hashing.

Two friends that show up often:

**Set (`set`)** — unordered collection of unique hashable values.
`{1, 2, 3}`. *O(1)* membership.

**Counter (`collections.Counter`)** — a dict subclass for
counting. `Counter("hello")` gives `{'l': 2, 'h': 1, 'e': 1, 'o':
1}`.

**Type checking** when confused:

```python
type(x)                     # returns the type object
isinstance(x, int)          # True if x is an int (or bool, which is a subclass)
```

**Type conversion** is explicit in Python:

```python
int("42")        # 42 (string to int)
str(42)          # '42' (int to string)
float("3.14")    # 3.14
list("abc")      # ['a', 'b', 'c']
tuple([1, 2])    # (1, 2)
```

There is no implicit conversion. `"5" + 3` raises `TypeError`.
You must convert one to match the other.
''',
        "summary": r'''
**Pattern**: pick the right built-in type for the job. Use `int`
for whole numbers, `float` only when you need fractions, `str`
for text, `list` for variable-length sequences, `tuple` for
fixed records, `dict` for key-value lookups, `set` for unique
membership.

**Lesson**: Python is strongly typed at runtime. You cannot mix
types in arithmetic or comparison without explicit conversion.

**Recognize next time**: every algorithm starts with a choice of
data type. The wrong choice usually leads to verbose or wrong
code. Pause to pick consciously.
''',
    },
    {
        "id": "if-else-statements",
        "title": "If / Else Statements",
        "step_id": 1,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["python-basics", "control-flow"],
        "what_this_teaches": (
            "Branching — the simplest control structure. Every "
            "decision in an algorithm is some flavor of `if`."
        ),
        "pattern": "if condition: ... elif other: ... else: ...",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["data-types"],
        "next_problems": ["match-case-statement", "for-while-loops"],
        "resources": [
            _STRIVER_SHEET,
            {
                "label": "Python docs — Control flow",
                "url": "https://docs.python.org/3/tutorial/controlflow.html",
            },
        ],
        "understanding": r'''
Branching lets a program take different actions depending on a
condition. Python's syntax is gentle:

```python
if x > 0:
    print("positive")
elif x < 0:
    print("negative")
else:
    print("zero")
```

Three keywords: `if`, `elif`, `else`. `elif` is "else if." `else`
is the catch-all.

**Boolean expressions** combine with `and`, `or`, `not`:

```python
if 0 < x < 100 and x % 2 == 0:
    print("even and in range")
```

Python supports chained comparisons (`0 < x < 100` is one
expression, not two). This is unusual among languages and
delightful.

**Truthiness** — Python lets you use any value where a boolean
is expected. The "falsy" values are: `False`, `0`, `0.0`, `""`,
`[]`, `{}`, `set()`, `None`. Everything else is "truthy."

```python
if some_list:       # True if non-empty
    process(some_list)
```

Use truthiness for cleaner checks: `if not arr:` reads better
than `if len(arr) == 0:`.

**Ternary expression** for short conditional values:

```python
sign = "positive" if x > 0 else "negative"
```

Use sparingly — nested ternaries are hard to read.

**Common gotcha**: indentation matters! Python uses indentation
to determine which lines belong to the `if`. Mixing tabs and
spaces causes `IndentationError`. Use four spaces consistently.

**Another gotcha**: `if a = 5` is a syntax error in Python (unlike
C). You meant `if a == 5`. Assignment is `=`, comparison is `==`.
''',
        "summary": r'''
**Pattern**: `if / elif / else` with Boolean expressions and
truthiness shortcuts.

**Lesson**: chained comparisons (`0 < x < 100`) and truthy
shortcuts (`if not arr:`) make Python conditions noticeably
cleaner than the C-style equivalent.

**Recognize next time**: every algorithm decision is an `if`.
Master the syntax now so it stops being noise.
''',
    },
    {
        "id": "match-case-statement",
        "title": "Match / Case Statement (Python 3.10+)",
        "step_id": 1,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["python-basics", "control-flow"],
        "what_this_teaches": (
            "Python's pattern-matching statement — a cleaner "
            "alternative to chains of `if/elif` when matching on "
            "structure or value."
        ),
        "pattern": "match value: case pattern: action",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["if-else-statements"],
        "next_problems": ["for-while-loops"],
        "resources": [
            _STRIVER_SHEET,
            {
                "label": "Python docs — match statement",
                "url": "https://docs.python.org/3/tutorial/controlflow.html#match-statements",
            },
        ],
        "understanding": r'''
Python 3.10 introduced `match` / `case` — a pattern-matching
construct similar to `switch` in C/Java but more powerful.

Basic value matching:

```python
def describe(x):
    match x:
        case 0:
            return "zero"
        case 1 | 2 | 3:
            return "small"
        case n if n > 100:
            return "huge"
        case _:
            return "other"
```

Notes:

- `case _:` is the catch-all (like `default:` in C).
- `case 1 | 2 | 3:` matches any of the three values.
- `case n if n > 100:` binds `n` and adds a guard condition.

**Structural matching** is where `match` really shines. You can
match on the shape of tuples, lists, and even classes:

```python
def head_and_tail(items):
    match items:
        case []:
            return None, []
        case [head, *tail]:
            return head, tail
```

For DSA practice, `match` is a nice-to-know but not essential.
You can do everything with `if/elif`. Use `match` when matching
on structure makes the code cleaner; stick to `if/elif` for
simple value tests.

**Caveat**: `match` was introduced in Python 3.10. If your
LeetCode / Codeforces judge runs an older Python, it won't work
and you'll need `if/elif`.
''',
        "summary": r'''
**Pattern**: `match / case` for value matching, guarded matching,
and structural decomposition.

**Lesson**: a nice alternative to long `if/elif` chains; not
essential but worth knowing.

**Recognize next time**: when a chain of `if/elif` has more than
4-5 branches and is matching on a single value or structure,
consider `match`.
''',
    },
    {
        "id": "arrays-and-strings",
        "title": "What Are Arrays and Strings?",
        "step_id": 1,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["arrays", "strings", "python-basics"],
        "what_this_teaches": (
            "A first introduction to the two most-used containers: "
            "lists (arrays) and strings. The full chapters on each "
            "live in the Learn section."
        ),
        "pattern": "Indexable, iterable, sliceable sequences.",
        "prerequisite_lessons": ["arrays", "strings"],
        "prerequisite_problems": ["data-types"],
        "next_problems": ["for-while-loops", "largest-element"],
        "resources": [_STRIVER_SHEET],
        "understanding": r'''
This problem is really a pointer to two full chapters in the
Learn section. Please open them now:

- **Arrays** — the Learn lesson on lists, indexing, fence posts,
  and the four basic moves.
- **Strings** — the Learn lesson on immutability, the
  list-edit-join pattern, character arithmetic, and
  canonicalization.

A quick recap of what you should know:

**Lists** (arrays in DSA-speak) are ordered, mutable sequences:

```python
nums = [3, 1, 4, 1, 5, 9, 2, 6]
nums[0]            # 3 (first element)
nums[-1]           # 6 (last element)
nums[1:4]          # [1, 4, 1] (slice; end is exclusive)
nums.append(10)    # add to end (O(1) amortized)
nums.pop()         # remove from end (O(1))
len(nums)          # 8
```

**Strings** are immutable sequences of characters:

```python
s = "racecar"
s[0]               # 'r'
s[-1]              # 'r'
s[::-1]            # 'racecar' (reverse via slice with step -1)
len(s)             # 7
"ace" in s         # True (substring check)
```

The key difference: **lists are mutable**, **strings are
immutable**. You can change `nums[0] = 99`. You cannot change
`s[0] = 'X'` — Python raises `TypeError`. To modify a string,
convert to a list, edit, and join back.

Both support **iteration**:

```python
for x in nums:
    print(x)
for ch in s:
    print(ch)
```

Both support **negative indexing**, **slicing**, and **`in`**
membership tests.

For full depth on each, please read the Arrays and Strings
lessons in the Learn section before tackling the practice
problems.
''',
        "summary": r'''
**Pattern**: lists are mutable indexed sequences; strings are
immutable indexed sequences. Both support iteration, slicing,
and `in`.

**Lesson**: the array/list and the string are the two most-used
containers in DSA. Master their syntax cold.

**Recognize next time**: every easy problem in this curriculum
uses one of these. Familiarity here makes the rest easier.
''',
    },
    {
        "id": "for-while-loops",
        "title": "For and While Loops",
        "step_id": 1,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["python-basics", "loops"],
        "what_this_teaches": (
            "The two looping constructs: `for` for iterating over "
            "a known sequence, `while` for iterating until a "
            "condition becomes false."
        ),
        "pattern": "for x in iterable: ... and while condition: ...",
        "prerequisite_lessons": ["arrays"],
        "prerequisite_problems": ["data-types"],
        "next_problems": ["functions", "largest-element"],
        "resources": [_STRIVER_SHEET],
        "understanding": r'''
Python has two looping constructs. Pick based on what you know
about the iteration count.

**`for` loop** — when you know what you're iterating over.

```python
for x in [1, 2, 3, 4, 5]:
    print(x)

for i in range(10):              # 0, 1, 2, ..., 9
    print(i)

for i in range(2, 10):           # 2, 3, ..., 9
    print(i)

for i in range(0, 10, 2):        # 0, 2, 4, 6, 8 (step of 2)
    print(i)

for i in range(10, 0, -1):       # 10, 9, 8, ..., 1 (countdown)
    print(i)

for i, x in enumerate(nums):     # both index and value
    print(i, x)

for a, b in zip(list1, list2):   # pair up two lists
    print(a, b)
```

`range(n)` produces `0, 1, ..., n - 1`. `range(start, stop)` is
half-open (start inclusive, stop exclusive). `range(start, stop,
step)` adds a step.

`enumerate(iterable)` yields `(index, value)` pairs.

`zip(a, b)` pairs corresponding elements; stops at the shorter.

**`while` loop** — when you iterate until a condition is no
longer true.

```python
i = 0
while i < 10:
    print(i)
    i += 1                       # don't forget to update the condition variable!

while True:
    line = input()
    if line == "stop":
        break                    # exit the loop
```

`break` exits the loop early. `continue` skips to the next
iteration.

**Common gotchas**:

- Off-by-one in `range`. `range(10)` does NOT include 10.
- Forgetting to update the loop variable in `while`, causing an
  infinite loop.
- Using `for` when you should use `while`. If you don't know the
  iteration count in advance (e.g., reading until EOF), use
  `while`.

A few Python loop idioms worth knowing:

```python
# Loop over a list in reverse
for x in reversed(nums):
    ...

# Loop with both index and value
for i, x in enumerate(nums):
    ...

# Iterate two lists simultaneously
for a, b in zip(list1, list2):
    ...

# Build a list with a single line
squares = [x * x for x in range(10)]
```

The last one is a **list comprehension** — Python's most loved
syntactic shortcut. It is equivalent to a `for` loop that
appends, but shorter and faster.
''',
        "summary": r'''
**Pattern**: `for x in iterable` for known iteration counts,
`while condition` for unknown counts.

**Lesson**: `range`, `enumerate`, `zip`, and list comprehensions
are the four most-used loop helpers in Python. Get them in your
fingers.

**Recognize next time**: every loop you ever write will be one
of these shapes.
''',
    },
    {
        "id": "functions",
        "title": "Functions (Pass by Reference vs Value)",
        "step_id": 1,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["python-basics", "functions"],
        "what_this_teaches": (
            "How to define and call functions, and the subtle but "
            "critical distinction between mutable and immutable "
            "arguments that confuses many beginners."
        ),
        "pattern": "def name(args): ... ; return value",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["for-while-loops"],
        "next_problems": ["time-space-complexity", "factorial-of-n"],
        "resources": [
            _STRIVER_SHEET,
            {
                "label": "Python docs — Defining functions",
                "url": "https://docs.python.org/3/tutorial/controlflow.html#defining-functions",
            },
        ],
        "understanding": r'''
A function is a named block of code that takes inputs (arguments)
and returns an output.

```python
def add(a, b):
    return a + b

result = add(3, 5)    # 8
```

Functions can have **default arguments**:

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Alice")             # 'Hello, Alice!'
greet("Bob", "Hi")         # 'Hi, Bob!'
```

**Keyword arguments** let you specify by name:

```python
greet(name="Alice", greeting="Hi")
```

**Variable-length arguments**:

```python
def sum_all(*nums):
    return sum(nums)

sum_all(1, 2, 3, 4)        # 10

def with_options(**kwargs):
    return kwargs.get('color', 'red')

with_options(color='blue', size=12)
```

`*args` collects positional arguments into a tuple. `**kwargs`
collects keyword arguments into a dict.

## Pass by reference vs pass by value

This is the part that confuses beginners.

Python uses what some call "pass by object reference." The
behavior depends on whether the argument is **mutable** or
**immutable**.

**Immutable arguments** (int, float, str, tuple, bool) — the
function gets a reference to the same object, but since the
object cannot change, reassigning inside the function does not
affect the caller:

```python
def reset(x):
    x = 0           # rebinds the local name; original is untouched

a = 5
reset(a)
print(a)            # still 5
```

**Mutable arguments** (list, dict, set, custom objects) — the
function gets a reference to the same object, and mutating the
object **does** affect the caller:

```python
def append_one(lst):
    lst.append(1)

a = [10, 20]
append_one(a)
print(a)            # [10, 20, 1] — modified!
```

But reassigning a mutable argument inside the function does NOT
affect the caller (because the rebinding is local):

```python
def replace(lst):
    lst = [99]       # rebinds local name only

a = [10, 20]
replace(a)
print(a)            # [10, 20] — unchanged
```

The rule of thumb:

- **Mutating an object** (calling its methods, indexing assignment)
  is visible outside the function.
- **Rebinding the parameter name** (with `=`) is local only.

This subtle distinction comes up constantly. When you pass a
list to a function and the function modifies it, the caller
sees the modification. When the function reassigns the parameter
to a new list, the caller does not.

## Default argument pitfall

Default values are evaluated **once**, at function definition
time. So a mutable default value is shared across all calls:

```python
def bad(items=[]):
    items.append(1)
    return items

bad()    # [1]
bad()    # [1, 1] — surprise!
bad()    # [1, 1, 1]
```

Fix: use `None` as the default and create the mutable inside:

```python
def good(items=None):
    if items is None:
        items = []
    items.append(1)
    return items
```

This is the **#1 Python gotcha** in functions. Always use `None`
for mutable defaults.
''',
        "summary": r'''
**Pattern**: `def name(args): ... return value`. Use `*args` and
`**kwargs` for flexibility. Use `None` for mutable default
values.

**Lesson**: Python passes references. Mutating a mutable
argument is visible outside; reassigning the parameter name is
not.

**Recognize next time**: every problem on this curriculum will
have you writing functions. The mutable/immutable distinction
will bite you eventually — be ready.
''',
    },
    {
        "id": "time-space-complexity",
        "title": "Time and Space Complexity",
        "step_id": 1,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["complexity", "analysis"],
        "what_this_teaches": (
            "How to talk about algorithm efficiency. Big-O notation, "
            "the common complexity classes, and how to estimate "
            "runtime from your code's structure."
        ),
        "pattern": "Count loops and recursive calls; identify the dominant term.",
        "prerequisite_lessons": [],
        "prerequisite_problems": [],
        "next_problems": ["largest-element", "binary-search"],
        "resources": [
            _STRIVER_SHEET,
            {
                "label": "Wikipedia — Big O notation",
                "url": "https://en.wikipedia.org/wiki/Big_O_notation",
            },
        ],
        "understanding": r'''
Big-O notation describes how an algorithm's runtime grows as the
input size grows. It is the language we use to compare
algorithms.

The basic idea: as input size `n` grows, how does the number of
operations grow?

Common complexity classes from fastest to slowest:

| Notation | Name | Example |
|---|---|---|
| *O(1)* | Constant | Indexing into an array; dict lookup |
| *O(log n)* | Logarithmic | Binary search |
| *O(n)* | Linear | Walking through an array once |
| *O(n log n)* | Linearithmic | Merge sort, quicksort average |
| *O(n²)* | Quadratic | Nested loop over the array |
| *O(n³)* | Cubic | Triple-nested loop |
| *O(2ⁿ)* | Exponential | Naive Fibonacci; subset enumeration |
| *O(n!)* | Factorial | Permutation enumeration |

Rough operation counts at `n = 10⁶`:

- *O(n)*: 1 million — fine.
- *O(n log n)*: 20 million — fine.
- *O(n²)*: 10¹² — too slow.
- *O(2ⁿ)*: astronomical — too slow even at `n = 50`.

## How to estimate the complexity of your code

Walk through the structure mechanically:

1. **A single loop** over the array → *O(n)*.
2. **A nested loop** → *O(n²)*. Two loops, each from 0 to n.
3. **A loop that halves** → *O(log n)*. Like binary search.
4. **A recursive call** that halves the input → *O(log n)*
   depth, *O(n log n)* total work if each level does *O(n)*.
5. **Two recursive calls**, each on a half → *O(n log n)*
   (master theorem, like merge sort).
6. **Two recursive calls**, each on the full size minus 1 →
   *O(2ⁿ)* (naive Fibonacci).
7. **Built-in `sorted()`** → *O(n log n)*.
8. **Dictionary lookup / set membership** → *O(1)* average.
9. **`list.pop(0)`** → *O(n)*! Often forgotten.

## Space complexity

Same notation, applied to memory:

- *O(1)* — a constant number of variables.
- *O(n)* — an array or hash of size `n`.
- *O(n²)* — a 2D table.
- *O(log n)* — recursion depth (for divide-and-conquer).

Important: recursion uses *O(depth)* stack memory, even if the
algorithm "feels" iterative.

## A worked example

```python
def has_duplicate(arr):
    for i in range(len(arr)):           # O(n)
        for j in range(i + 1, len(arr)):   # O(n)
            if arr[i] == arr[j]:
                return True
    return False
```

Two nested loops, each *O(n)*. Total: *O(n²)* time, *O(1)*
space.

Compare with the hash-based version:

```python
def has_duplicate(arr):
    seen = set()                         # O(n) space
    for x in arr:                        # O(n) loop
        if x in seen:                    # O(1) lookup
            return True
        seen.add(x)
    return False
```

*O(n)* time, *O(n)* space. We trade memory for time.

## Why this matters

When you face a problem with `n = 10⁵`, an *O(n²)* solution will
take 10¹⁰ operations — about a minute or more in Python. An
*O(n log n)* solution finishes in a fraction of a second.

So the rule of thumb: **always state the complexity of your
solution out loud before writing code**. If the complexity is
worse than the constraints allow, you know to find a better
algorithm before wasting time on implementation.
''',
        "summary": r'''
**Pattern**: count nested loops and recursive depth; identify
the dominant term.

**Lesson**: big-O is the language of algorithm analysis. Know
the common classes, know which Python operations are O(1) vs
O(n), and quote your solution's complexity before coding.

**Recognize next time**: every interview problem starts with
"what is your time and space complexity?". Be ready.
''',
    },
    # =================================================================
    # Lecture 2 — Patterns (5 problems)
    # =================================================================
    {
        "id": "pattern-square",
        "title": "Pattern — Square of Stars",
        "step_id": 1,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["patterns", "loops"],
        "what_this_teaches": (
            "The basic nested-loop pattern. Outer loop = rows, "
            "inner loop = columns. Every pattern problem in this "
            "lecture is a variation of this skeleton."
        ),
        "pattern": "Two nested loops: outer for rows, inner for columns.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["for-while-loops"],
        "next_problems": [
            "pattern-right-triangle",
            "pattern-inverted-triangle",
            "pattern-number-pyramid",
            "pattern-diamond",
        ],
        "resources": [_STRIVER_SHEET],
        "understanding": r'''
Print a square of stars of size `n × n`:

```
* * * * *
* * * * *
* * * * *
* * * * *
* * * * *
```

The skeleton: two nested loops. Outer for each row, inner for
each column in that row. Print a space after each star and a
newline at the end of each row.

```python
def square(n):
    for i in range(n):
        for j in range(n):
            print("*", end=" ")
        print()
```

For an `n × n` pattern, both loops run from `0` to `n - 1`, so
the total work is *O(n²)*. That is the cost of printing every
cell.

The Pythonic shortcut:

```python
def square(n):
    for _ in range(n):
        print("* " * n)
```

`"* " * n` builds a string by repetition. Cleaner but functionally
identical.

For a square of digits:

```python
def square_digits(n):
    for i in range(n):
        for j in range(n):
            print(j + 1, end=" ")
        print()
```

For a square of "0"s and "1"s:

```python
def square_binary(n):
    for i in range(n):
        for j in range(n):
            print((i + j) % 2, end=" ")
        print()
```

All variations follow the same skeleton: nested loops, with a
formula that decides what to print at `(i, j)`.

This is foundational for the rest of the pattern problems —
every other shape is just a different formula or loop range.
''',
        "summary": r'''
**Pattern**: nested loops; outer for rows, inner for columns.

**Lesson**: every pattern problem boils down to this skeleton.
The "shape" of the pattern is encoded in the inner loop's range
and the formula for what to print.

**Recognize next time**: any "print this shape" problem. Start
with the skeleton, then customize.
''',
    },
    {
        "id": "pattern-right-triangle",
        "title": "Pattern — Right Triangle of Stars",
        "step_id": 1,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["patterns", "loops"],
        "what_this_teaches": (
            "How varying the inner loop's range produces different "
            "shapes. The right triangle is the simplest such variation."
        ),
        "pattern": "Inner loop range depends on the outer index.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["pattern-square"],
        "next_problems": [
            "pattern-inverted-triangle",
            "pattern-number-pyramid",
            "pattern-diamond",
        ],
        "resources": [_STRIVER_SHEET],
        "understanding": r'''
Print a right triangle of stars:

```
*
* *
* * *
* * * *
* * * * *
```

The change from the square: each row has a different number of
stars. Row `i` (0-indexed) has `i + 1` stars.

So the inner loop's range is no longer fixed at `n` — it depends
on the outer index.

```python
def right_triangle(n):
    for i in range(n):
        for j in range(i + 1):       # i + 1 stars on row i
            print("*", end=" ")
        print()
```

For row 0, the inner loop runs 1 time. For row 1, twice. And so
on. Total stars printed: `1 + 2 + ... + n = n(n+1)/2`, which is
*O(n²)*.

The shortcut:

```python
def right_triangle(n):
    for i in range(1, n + 1):
        print("* " * i)
```

Variations:

**Number triangle**: print `j + 1` instead of `*`.

**Letter triangle**: print `chr(ord('A') + j)`.

**Reverse right triangle** (right-aligned):

```python
def right_aligned(n):
    for i in range(n):
        print(" " * (n - i - 1) + "* " * (i + 1))
```

For each row, print leading spaces to push the stars right.

The key insight: **the inner loop's range parameterizes the
shape**. By choosing the right formula for the row, you can
print any shape that has row-wise variation.
''',
        "summary": r'''
**Pattern**: inner loop range depends on the outer index.

**Lesson**: the formula `inner range = f(outer index)` controls
the shape. Right triangle uses `f(i) = i + 1`.

**Recognize next time**: any "triangle" or "ladder" pattern. The
inner loop's range is the variable.
''',
    },
    {
        "id": "pattern-inverted-triangle",
        "title": "Pattern — Inverted Triangle",
        "step_id": 1,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["patterns", "loops"],
        "what_this_teaches": (
            "The reverse of the right triangle — rows shrink instead "
            "of grow. Same skeleton, opposite range."
        ),
        "pattern": "Inner range decreases with outer index.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["pattern-right-triangle"],
        "next_problems": ["pattern-number-pyramid", "pattern-diamond"],
        "resources": [_STRIVER_SHEET],
        "understanding": r'''
Print an inverted triangle:

```
* * * * *
* * * *
* * *
* *
*
```

Row `i` (0-indexed) has `n - i` stars. So the inner loop range
shrinks as `i` grows.

```python
def inverted_triangle(n):
    for i in range(n):
        for j in range(n - i):
            print("*", end=" ")
        print()
```

The shortcut:

```python
def inverted_triangle(n):
    for i in range(n, 0, -1):
        print("* " * i)
```

For a **centered** inverted triangle (sometimes asked):

```
* * * * *
 * * * *
  * * *
   * *
    *
```

Add leading spaces that grow with `i`:

```python
def centered_inverted(n):
    for i in range(n):
        print(" " * i + "* " * (n - i))
```

Again, the skeleton is the same as the right triangle. Only the
inner loop's range and the leading-space formula change.

By now you should be seeing the pattern: every pattern problem
is some combination of "how many stars on row `i`" and "how many
leading spaces on row `i`." Pick the two formulas; the rest is
mechanical.
''',
        "summary": r'''
**Pattern**: inner range = `n - i` (shrinks with row).

**Lesson**: inverted is just the right triangle's range reversed.

**Recognize next time**: any "decreasing rows" pattern. Flip the
range direction.
''',
    },
    {
        "id": "pattern-number-pyramid",
        "title": "Pattern — Number Pyramid",
        "step_id": 1,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["patterns", "loops"],
        "what_this_teaches": (
            "Centering — adding leading spaces that shrink with each "
            "row to push the content rightward into a pyramid shape."
        ),
        "pattern": "Leading spaces + content, both functions of the row.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["pattern-right-triangle"],
        "next_problems": ["pattern-diamond"],
        "resources": [_STRIVER_SHEET],
        "understanding": r'''
Print a centered number pyramid:

```
    1
   2 3
  4 5 6
 7 8 9 10
```

Row `i` (0-indexed) has `i + 1` numbers and `n - i - 1` leading
spaces (where `n` is the total number of rows).

```python
def number_pyramid(n):
    current = 1
    for i in range(n):
        print(" " * (n - i - 1), end="")
        for j in range(i + 1):
            print(current, end=" ")
            current += 1
        print()
```

The trick: a running counter `current` increments after each
number is printed, so we get the sequence 1, 2, 3, ... across
the entire pyramid.

For a **symmetric number pyramid**:

```
    1
   1 2 1
  1 2 3 2 1
 1 2 3 4 3 2 1
```

Each row reads up to `i + 1`, then back down to 1:

```python
def symmetric_pyramid(n):
    for i in range(n):
        print(" " * (n - i - 1), end="")
        for j in range(1, i + 2):
            print(j, end=" ")
        for j in range(i, 0, -1):
            print(j, end=" ")
        print()
```

Two inner loops — one for the ascent, one for the descent.

The deeper principle: every pattern is some combination of
**leading spaces** and **content**. Pick the formula for each
row, and the pattern emerges.
''',
        "summary": r'''
**Pattern**: leading spaces shrink, content grows; combine for a
pyramid.

**Lesson**: pyramids are centered triangles. The leading-space
formula is what does the centering.

**Recognize next time**: any centered or symmetric pattern. Two
formulas: spaces, then content.
''',
    },
    {
        "id": "pattern-diamond",
        "title": "Pattern — Diamond",
        "step_id": 1,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["patterns", "loops"],
        "what_this_teaches": (
            "Combining two triangles — an upper pyramid and a lower "
            "inverted pyramid — to form a diamond shape."
        ),
        "pattern": "Two phases: ascent and descent.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["pattern-number-pyramid", "pattern-inverted-triangle"],
        "next_problems": [],
        "resources": [_STRIVER_SHEET],
        "understanding": r'''
Print a diamond:

```
    *
   * *
  * * *
 * * * *
* * * * *
 * * * *
  * * *
   * *
    *
```

A diamond is just an upper pyramid followed by a lower inverted
pyramid. Write both phases:

```python
def diamond(n):
    # Upper half — pyramid
    for i in range(n):
        print(" " * (n - i - 1) + "* " * (i + 1))
    # Lower half — inverted pyramid
    for i in range(n - 1):
        print(" " * (i + 1) + "* " * (n - i - 1))
```

Two separate loops, each printing one half. The bottom row of
the upper half is the widest; the top row of the lower half
starts the descent.

For a **hollow diamond** (just the outline), only the leftmost
and rightmost stars per row are printed:

```python
def hollow_diamond(n):
    for i in range(n):
        line = list(" " * (2 * n - 1))
        line[n - i - 1] = "*"
        line[n + i - 1] = "*"
        print("".join(line))
    for i in range(n - 1, 0, -1):
        line = list(" " * (2 * n - 1))
        line[n - i] = "*"
        line[n + i - 2] = "*"
        print("".join(line))
```

For a **number diamond**, replace the star content with the row
index formula from the number pyramid.

The principle, repeated for the final time: every pattern is
loops + formulas. Master the basic shapes (square, triangle,
inverted triangle, pyramid, diamond) and you can compose any
other shape from them.

Pattern problems test only one thing: comfort with nested loops
and index formulas. Once that comfort is real, every variation
takes 30 seconds.
''',
        "summary": r'''
**Pattern**: upper pyramid loop + lower inverted pyramid loop.

**Lesson**: complex patterns are compositions of simpler ones.
Recognize the components, write each phase, concatenate.

**Recognize next time**: any "symmetric vertical" pattern is a
diamond. Two halves, mirror images.
''',
    },
    # =================================================================
    # Lecture 3 — Python collections (7 problems)
    # =================================================================
    {
        "id": "python-list-collection",
        "title": "Python List — the Workhorse",
        "step_id": 1,
        "lecture_id": 3,
        "difficulty": "easy",
        "tags": ["python", "collections", "list"],
        "what_this_teaches": (
            "Everything you need to know about Python's `list`: "
            "the most-used container in DSA practice."
        ),
        "pattern": "Indexable, mutable, dynamic array of any objects.",
        "prerequisite_lessons": ["arrays"],
        "prerequisite_problems": ["arrays-and-strings"],
        "next_problems": ["python-deque", "python-set"],
        "resources": [
            _STRIVER_SHEET,
            {
                "label": "Python docs — Lists",
                "url": "https://docs.python.org/3/tutorial/datastructures.html#more-on-lists",
            },
        ],
        "understanding": r'''
Python's `list` is a dynamic array — under the hood it is a
contiguous block of pointers, resized automatically as you add
or remove elements. It is the most-used container in DSA
practice and you should know its operations cold.

**Creation:**

```python
empty = []
nums = [1, 2, 3, 4, 5]
zeros = [0] * 10                       # ten zeros
squares = [x * x for x in range(5)]    # list comprehension
```

**Access and modification:**

```python
nums[0]              # first element (O(1))
nums[-1]             # last element (O(1))
nums[0] = 99         # update (O(1))
nums[1:4]            # slice from 1 to 4 (exclusive end)
len(nums)            # length (O(1))
```

**Adding elements:**

```python
nums.append(6)       # add to end (O(1) amortized)
nums.insert(0, 0)    # insert at index 0 (O(n) — shifts everyone right)
nums.extend([7, 8])  # extend with another iterable (O(k))
nums + [9]           # creates a new list (O(n + k))
```

**Removing elements:**

```python
nums.pop()           # remove and return last (O(1))
nums.pop(0)          # remove and return first (O(n) — shifts everyone left!)
nums.remove(5)       # remove first occurrence of value 5 (O(n))
del nums[0]          # delete at index 0 (O(n))
```

**Searching:**

```python
5 in nums            # True/False (O(n))
nums.index(5)        # index of first 5 (raises ValueError if absent)
nums.count(5)        # how many 5s (O(n))
```

**Sorting:**

```python
nums.sort()          # in-place sort (O(n log n))
nums.sort(reverse=True)
nums.sort(key=lambda x: -x)    # custom key
sorted_copy = sorted(nums)     # new sorted list, original untouched
```

**Reversing:**

```python
nums.reverse()       # in-place
reversed_copy = nums[::-1]     # new reversed list
```

**Common idioms:**

```python
# List comprehension
squares = [x * x for x in range(10)]
evens = [x for x in nums if x % 2 == 0]

# Iterate with index
for i, x in enumerate(nums):
    ...

# Zip two lists
for a, b in zip(list1, list2):
    ...

# Flatten a list of lists
flat = [x for sublist in nested for x in sublist]
```

**Big-O cheat sheet:**

| Operation | Complexity |
|---|---|
| `nums[i]`, `nums[i] = ...` | O(1) |
| `nums.append(x)`, `nums.pop()` | O(1) amortized |
| `nums.pop(0)`, `nums.insert(0, x)` | **O(n)** — avoid! |
| `x in nums` | O(n) |
| `nums.sort()` | O(n log n) |
| `nums[a:b]` | O(b - a) (slicing copies) |
| `len(nums)` | O(1) |

The single most important takeaway: **operations at the front of
the list are O(n)**. If you need fast front operations, use
`collections.deque` instead.
''',
        "summary": r'''
**Pattern**: Python's list is a dynamic array. O(1) at end, O(n)
at front.

**Lesson**: know which operations are O(1) and which are O(n).
Avoid `pop(0)` and `insert(0, x)` in hot loops.

**Recognize next time**: every problem uses lists. Mastery here
is non-negotiable.
''',
    },
    {
        "id": "python-deque",
        "title": "Python `collections.deque` — O(1) Both Ends",
        "step_id": 1,
        "lecture_id": 3,
        "difficulty": "easy",
        "tags": ["python", "collections", "deque"],
        "what_this_teaches": (
            "When list.pop(0) is too slow, deque is the answer. "
            "It's the right tool for queues, BFS, and "
            "monotonic-deque tricks."
        ),
        "pattern": "O(1) append and pop at both ends.",
        "prerequisite_lessons": ["queues"],
        "prerequisite_problems": ["python-list-collection"],
        "next_problems": ["python-stack-queue", "graph-bfs"],
        "resources": [
            _STRIVER_SHEET,
            {
                "label": "Python docs — collections.deque",
                "url": "https://docs.python.org/3/library/collections.html#collections.deque",
            },
        ],
        "understanding": r'''
`collections.deque` ("double-ended queue") is the right tool
whenever you need fast operations at **both ends** of a sequence.

```python
from collections import deque

d = deque()
d.append(1)              # add to right (O(1))
d.appendleft(0)          # add to left (O(1))
d.pop()                  # remove from right (O(1))
d.popleft()              # remove from left (O(1))
d[0]                     # peek front (O(1))
d[-1]                    # peek back (O(1))
len(d)                   # length (O(1))
```

All four ends-operations are *O(1)*. Compare with list:

| Operation | list | deque |
|---|---|---|
| append right | O(1) | O(1) |
| append left | **O(n)** | O(1) |
| pop right | O(1) | O(1) |
| pop left | **O(n)** | O(1) |
| index by middle | O(1) | O(n) |

So:
- Use **list** when you mostly add/remove at the end and need
  fast random indexing.
- Use **deque** when you add/remove at both ends or implement a
  queue/BFS.

## Implementation: queue (FIFO)

```python
from collections import deque

q = deque()
q.append("first")
q.append("second")
q.append("third")
while q:
    print(q.popleft())
# first
# second
# third
```

## Implementation: stack (LIFO)

Either list or deque works for a stack; both are *O(1)* at the
end.

```python
stack = deque()
stack.append(1)
stack.append(2)
stack.pop()              # 2
```

## Sliding window with deque

The classic use: maintaining a window of recent elements with
fast add/remove at both ends.

```python
from collections import deque

def first_negative_in_windows(arr, k):
    dq = deque()
    out = []
    for i, x in enumerate(arr):
        if x < 0:
            dq.append(i)
        if dq and dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(arr[dq[0]] if dq else 0)
    return out
```

## Bounded deque (fixed maxlen)

`deque(maxlen=n)` automatically drops the oldest when full —
useful for "last n items" buffers.

```python
recent = deque(maxlen=3)
recent.extend([1, 2, 3, 4, 5])
# deque([3, 4, 5], maxlen=3)
```

The takeaway: **whenever a problem involves a FIFO queue, BFS,
or a sliding-window summary that needs both-ends speed, reach
for `deque`**.
''',
        "summary": r'''
**Pattern**: `deque` for O(1) at both ends; the right tool for
queues, BFS, and sliding-window deque tricks.

**Lesson**: never use `list.pop(0)` for a queue. The hidden
*O(n)* will silently destroy your algorithm's runtime.

**Recognize next time**: BFS, level-order traversal, sliding
window maximum, "last n items" buffers — all `deque` problems.
''',
    },
    {
        "id": "python-stack-queue",
        "title": "Python Stack and Queue Implementations",
        "step_id": 1,
        "lecture_id": 3,
        "difficulty": "easy",
        "tags": ["python", "stack", "queue"],
        "what_this_teaches": (
            "How to implement stacks and queues using built-in "
            "Python containers, and which built-in is right for "
            "each."
        ),
        "pattern": "list for stack; deque for queue.",
        "prerequisite_lessons": ["stacks", "queues"],
        "prerequisite_problems": ["python-list-collection", "python-deque"],
        "next_problems": ["balanced-parentheses", "graph-bfs"],
        "resources": [_STRIVER_SHEET],
        "understanding": r'''
Python doesn't have a dedicated `Stack` or `Queue` class for
basic use. Instead, you reach for the right built-in.

## Stack (LIFO)

Use `list` with `.append()` and `.pop()`:

```python
stack = []
stack.append(1)          # push
stack.append(2)
stack.append(3)
top = stack[-1]          # peek (3)
v = stack.pop()          # pop (returns 3)
# stack is now [1, 2]
```

`list.append` and `list.pop` (without index) are both *O(1)*
amortized.

## Queue (FIFO)

Use `collections.deque`:

```python
from collections import deque

q = deque()
q.append(1)              # enqueue (add to back)
q.append(2)
q.append(3)
front = q[0]             # peek (1)
v = q.popleft()          # dequeue (returns 1, removes it)
# q is now deque([2, 3])
```

Both `append` and `popleft` are *O(1)*.

## What about `queue.Queue`?

Python has a `queue.Queue` class in the standard library, but it
is designed for **thread-safe** producer-consumer scenarios. It
has locking overhead and is unnecessarily slow for single-
threaded DSA use. **Use `collections.deque` instead.**

## What about `queue.LifoQueue`?

Same situation — designed for threading. For DSA, use a list as
a stack.

## What about `queue.PriorityQueue`?

For priority queues, use **`heapq`** (also in the standard
library), which is lighter and faster than `queue.PriorityQueue`.

## Quick comparison

| Need | Use |
|---|---|
| Stack | `list` |
| Queue | `collections.deque` |
| Priority queue | `heapq` |
| Threading-safe queue | `queue.Queue` (rare in DSA) |

The lesson: there is no single "Stack" or "Queue" class in
Python's idiomatic DSA usage. The right answer depends on what
you need.

## A common bug

The mistake almost every beginner makes:

```python
# WRONG: O(n) per dequeue
queue = []
queue.append(1)
queue.append(2)
queue.pop(0)             # SLOW — shifts everyone left
```

`list.pop(0)` is *O(n)*. Using it in a BFS turns the algorithm
from *O(V + E)* into *O(V × (V + E))*. The bug is silent — the
algorithm still produces correct answers, just absurdly slowly.

Always use `deque.popleft()` for the front of a queue.
''',
        "summary": r'''
**Pattern**: list for stack, deque for queue. Avoid
`queue.Queue` unless you specifically need thread safety.

**Lesson**: there's no separate Stack or Queue class in DSA
Python. Pick the right built-in based on operation costs.

**Recognize next time**: any LIFO/FIFO data structure choice.
Match the structure to the operation profile.
''',
    },
    {
        "id": "python-heapq",
        "title": "Python `heapq` — Min-Heap Done Right",
        "step_id": 1,
        "lecture_id": 3,
        "difficulty": "easy",
        "tags": ["python", "heap", "priority-queue"],
        "what_this_teaches": (
            "How to use Python's heapq module for priority queues, "
            "top-K problems, and merge-K-sorted-lists style "
            "algorithms."
        ),
        "pattern": "heapq operates on a list interpreted as a binary min-heap.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["python-list-collection"],
        "next_problems": ["kth-largest", "merge-k-sorted-lists"],
        "resources": [
            _STRIVER_SHEET,
            {
                "label": "Python docs — heapq",
                "url": "https://docs.python.org/3/library/heapq.html",
            },
        ],
        "understanding": r'''
Python's `heapq` module provides heap operations on a regular
list. It is the standard library's **min-heap** (smallest at the
top).

## Basic operations

```python
import heapq

heap = []
heapq.heappush(heap, 5)       # add (O(log n))
heapq.heappush(heap, 2)
heapq.heappush(heap, 8)
heap[0]                        # peek smallest (O(1)) — returns 2
heapq.heappop(heap)            # remove smallest (O(log n)) — returns 2
```

The heap is just a list; `heap[0]` is always the smallest.

## Building a heap from a list

```python
arr = [5, 2, 8, 1, 9]
heapq.heapify(arr)             # O(n)
# arr is now a valid heap
```

`heapify` is *O(n)*, much faster than pushing all elements one
by one (*O(n log n)*).

## Max-heap trick

`heapq` is min-only. For a max-heap, **negate the values**:

```python
import heapq

max_heap = []
heapq.heappush(max_heap, -5)   # push the negative
heapq.heappush(max_heap, -2)
heapq.heappush(max_heap, -8)
-max_heap[0]                    # peek largest (8)
-heapq.heappop(max_heap)        # pop largest (8)
```

For tuples (e.g., `(priority, value)`), negate only the priority:

```python
heapq.heappush(heap, (-priority, value))
```

## Top-K pattern

To find the **K largest** elements, maintain a min-heap of size
K:

```python
def k_largest(arr, k):
    heap = []
    for x in arr:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap   # contains the K largest, smallest at top
```

`O(n log k)` time, `O(k)` space.

There's also a built-in for this:

```python
heapq.nlargest(k, arr)         # K largest, sorted descending
heapq.nsmallest(k, arr)        # K smallest, sorted ascending
```

Both are *O(n log k)*.

## Merge K sorted lists

```python
import heapq

def merge_sorted(*lists):
    return list(heapq.merge(*lists))
```

`heapq.merge` is a generator that walks all input iterables in
sorted order. *O(N log K)* where N is total elements and K is
number of lists.

## Tuple comparison

When two items have equal priority, heapq compares the rest of
the tuple. If your values are not comparable (e.g., custom
objects), break ties with a unique counter:

```python
import itertools
import heapq

counter = itertools.count()
heap = []
heapq.heappush(heap, (priority, next(counter), my_object))
```

This is a common pattern for priority queues with custom
objects.

## When to reach for heapq

- **Top-K** problems.
- **Median from data stream** (two heaps).
- **Merge K sorted lists / streams**.
- **Dijkstra's algorithm**.
- **Scheduling** (always pick the next-priority task).

If a problem says "always pick the smallest/largest available
right now," that is a heap.
''',
        "summary": r'''
**Pattern**: `heappush` / `heappop` for *O(log n)* priority
queue operations. Negate values for a max-heap.

**Lesson**: heapq is the standard library's priority queue. Use
it whenever you need "give me the next smallest/largest"
repeatedly.

**Recognize next time**: top-K, Dijkstra, median from stream,
scheduling. All heaps.
''',
    },
    {
        "id": "python-set",
        "title": "Python `set` — Unique, Unordered, O(1) Membership",
        "step_id": 1,
        "lecture_id": 3,
        "difficulty": "easy",
        "tags": ["python", "set", "hashing"],
        "what_this_teaches": (
            "When you need 'is this present?' in O(1), reach for "
            "set. The simplest hash-based container in Python."
        ),
        "pattern": "Unordered collection of unique hashable values.",
        "prerequisite_lessons": ["hashing"],
        "prerequisite_problems": [],
        "next_problems": ["python-dict", "two-sum"],
        "resources": [
            _STRIVER_SHEET,
            {
                "label": "Python docs — Set types",
                "url": "https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset",
            },
        ],
        "understanding": r'''
A `set` stores unique values without preserving order. Membership
tests, additions, and removals are all *O(1)* on average.

## Basic operations

```python
s = set()
s = {1, 2, 3}                  # set literal (note: braces)
s = set([1, 2, 2, 3])          # {1, 2, 3} — duplicates collapse

s.add(4)                        # O(1)
s.discard(2)                    # O(1), no error if absent
s.remove(2)                     # O(1), KeyError if absent
3 in s                          # O(1) membership
len(s)                          # O(1)

# Iteration (order not guaranteed)
for x in s:
    print(x)
```

`{}` is an empty **dict**, not an empty set! Use `set()` for an
empty set.

## Set operations

```python
a = {1, 2, 3}
b = {2, 3, 4}

a | b           # union: {1, 2, 3, 4}
a & b           # intersection: {2, 3}
a - b           # difference: {1}
a ^ b           # symmetric difference: {1, 4}

a.issubset(b)   # False
a.issuperset({1})  # True
```

These set-algebra operations are extremely useful in DSA. For
example, "elements in A but not in B" is `a - b`.

## When to use a set

- **Deduplication**: `unique = list(set(arr))`.
- **Presence test**: `if x in seen:`.
- **Detecting duplicates**: walk the array, return True on
  second seeing.
- **Set difference / intersection**: as above.

## When NOT to use a set

- **You need order**: sets don't preserve insertion order. Use a
  list, or a dict (which does, since 3.7), or `dict.fromkeys()`.
- **You need to count occurrences**: sets discard counts. Use
  `Counter`.
- **You need to look up by key and get a value**: that's a dict.

## frozenset

`frozenset` is the immutable version of `set`. Useful when you
need a hashable set (e.g., as a dict key or as an element of
another set).

```python
fs = frozenset([1, 2, 3])
{fs: "hello"}           # frozenset can be a dict key
```

## A common pattern

Deduplicating while preserving order:

```python
# Wrong: set drops order
unique = list(set(arr))    # order is not preserved

# Right: dict.fromkeys preserves order (since 3.7)
unique = list(dict.fromkeys(arr))
```

For DSA practice, when "order doesn't matter" and "I just want
unique values," set is the answer.
''',
        "summary": r'''
**Pattern**: `set` for *O(1)* unique membership and presence
tests. Don't preserve order; don't store counts.

**Lesson**: pick set for the "is this present?" question; pick
dict for "what's the value for this key?"; pick Counter for "how
many of each?".

**Recognize next time**: detect duplicates, deduplicate, set
algebra, presence checks — all sets.
''',
    },
    {
        "id": "python-dict",
        "title": "Python `dict` — Key-Value at the Speed of Light",
        "step_id": 1,
        "lecture_id": 3,
        "difficulty": "easy",
        "tags": ["python", "dict", "hashing"],
        "what_this_teaches": (
            "The workhorse of hashing. Everything about Python's "
            "dict: creation, access, idioms, gotchas."
        ),
        "pattern": "Key-value mapping with *O(1)* average access.",
        "prerequisite_lessons": ["hashing"],
        "prerequisite_problems": ["python-set"],
        "next_problems": ["count-frequencies", "two-sum"],
        "resources": [
            _STRIVER_SHEET,
            {
                "label": "Python docs — Mapping types",
                "url": "https://docs.python.org/3/library/stdtypes.html#mapping-types-dict",
            },
        ],
        "understanding": r'''
A `dict` is a hash-based key-value mapping. Lookups, insertions,
and deletions are all *O(1)* on average.

## Creation and access

```python
d = {}
d = {"a": 1, "b": 2}
d = dict(a=1, b=2)              # keyword form
d = dict([("a", 1), ("b", 2)])  # from list of pairs

d["a"]                          # 1 (KeyError if missing)
d.get("c")                      # None (no error)
d.get("c", 0)                   # 0 (custom default)
d["c"] = 3                      # add or update
del d["a"]                      # remove (KeyError if missing)
"a" in d                        # True/False
len(d)                          # number of keys
```

## Iteration

```python
for key in d:                   # iterate keys
    ...
for key, value in d.items():    # iterate key-value pairs
    ...
for value in d.values():        # iterate values
    ...
```

Iteration order is **insertion order** (since Python 3.7). This
is a real guarantee, not an implementation detail.

## The .get(key, default) idiom

The single most useful method on dict:

```python
d.get(key, default)
```

Returns `d[key]` if `key` is present, otherwise `default`. The
canonical use:

```python
counts = {}
for x in items:
    counts[x] = counts.get(x, 0) + 1
```

You will write this exact pattern hundreds of times.

## setdefault

`dict.setdefault(key, default)` returns the existing value if the
key is present, otherwise inserts `default` and returns it.

```python
groups = {}
for item in items:
    groups.setdefault(group_of(item), []).append(item)
```

This handles "build a dict of lists" in one line.

## defaultdict

`collections.defaultdict(factory)` auto-creates a default value
the first time a key is accessed.

```python
from collections import defaultdict

counts = defaultdict(int)       # missing keys default to 0
for x in items:
    counts[x] += 1

groups = defaultdict(list)      # missing keys default to []
for item in items:
    groups[group_of(item)].append(item)
```

Cleaner than `setdefault` for repeated use.

## Counter

`collections.Counter` is a dict subclass purpose-built for
counting:

```python
from collections import Counter
freq = Counter("hello")
# Counter({'l': 2, 'h': 1, 'e': 1, 'o': 1})

freq.most_common(2)             # [('l', 2), ('h', 1)]
freq + Counter("world")         # element-wise addition
```

## Dict comprehension

```python
squares = {x: x * x for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

flipped = {v: k for k, v in d.items()}
```

## Common gotchas

**Gotcha 1: mutable values.** If you store lists as values,
mutating one mutates the entry. Usually what you want, sometimes
not.

**Gotcha 2: keys must be hashable.** Lists are not hashable; use
tuples.

**Gotcha 3: KeyError vs .get.** Use `.get()` when missing keys
are expected. Use direct indexing when missing keys are bugs.

**Gotcha 4: dict() vs {}.** Both create an empty dict. `{}` is
slightly faster.

## When dict, when not

Use **dict** for:
- Key-value lookups.
- Counting (or use Counter).
- Grouping (or use defaultdict).
- Memoization (the cache in DP).
- Hashing-based algorithms (two-sum, anagrams, etc.).

Use **set** when you only care about presence, not values.

Use **Counter** when you specifically need frequencies.

Use **defaultdict** when you want missing keys to auto-create.

These four (dict, set, Counter, defaultdict) cover 99% of hash-
based DSA work.
''',
        "summary": r'''
**Pattern**: dict for *O(1)* key-value mapping. Iteration is
insertion order. Use `.get()` for missing-key safety.

**Lesson**: dict, defaultdict, and Counter are the three core
hash containers. Pick based on what your missing-key semantics
need to be.

**Recognize next time**: every hashing problem uses one of
these.
''',
    },
    {
        "id": "python-sorting",
        "title": "Python's `sorted()` and `list.sort()`",
        "step_id": 1,
        "lecture_id": 3,
        "difficulty": "easy",
        "tags": ["python", "sorting"],
        "what_this_teaches": (
            "How to use Python's built-in sort, the `key=` "
            "parameter, custom orderings, and the stability "
            "guarantee."
        ),
        "pattern": "sorted(iterable, key=..., reverse=...).",
        "prerequisite_lessons": ["sorting"],
        "prerequisite_problems": [],
        "next_problems": ["merge-overlapping-intervals", "kth-largest"],
        "resources": [
            _STRIVER_SHEET,
            {
                "label": "Python docs — sorted()",
                "url": "https://docs.python.org/3/library/functions.html#sorted",
            },
        ],
        "understanding": r'''
Python's built-in sort is **Timsort**: *O(n log n)* worst-case,
stable, and highly optimized for partially-sorted real-world
data.

## Two flavors

```python
sorted(iterable)          # returns a new sorted list, original untouched
list.sort()               # sorts in place, returns None
```

Use `sorted()` when you want a new list. Use `list.sort()` when
you want to modify the list in place (slightly faster, no extra
memory).

**Common bug**: don't write `new = list.sort()`. `list.sort()`
returns `None`. You meant `list.sort()` (modifying) followed by
`new = list`, or `new = sorted(list)`.

## The `key=` parameter

The `key=` parameter takes a function that extracts the
comparison key from each element:

```python
words = ["banana", "apple", "cherry"]
sorted(words)                              # alphabetic
sorted(words, key=len)                     # by length
sorted(words, key=lambda w: w[-1])         # by last letter
sorted(words, key=str.lower)               # case-insensitive

items = [(1, "b"), (3, "a"), (2, "c")]
sorted(items, key=lambda x: x[1])          # by second element
```

`key=` is much faster than `cmp=` (which Python removed in 3.0).
You almost never need `functools.cmp_to_key`; learn the `key=`
approach.

## Reverse order

```python
sorted(nums, reverse=True)
```

For numerical reverse, you can also use `key=lambda x: -x`. For
arbitrary types, prefer `reverse=True`.

## Multi-field sort

Use a tuple as the key — Python's tuple comparison is
lexicographic:

```python
people = [("Alice", 30), ("Bob", 25), ("Alice", 25)]
sorted(people, key=lambda p: (p[0], p[1]))
# Sort by name ascending, then age ascending
```

For mixed orderings (one field ascending, another descending),
negate the descending field:

```python
sorted(people, key=lambda p: (p[0], -p[1]))
# Name ascending, age descending
```

For non-numeric descending, use the stability trick — sort
twice:

```python
people.sort(key=lambda p: p[1])           # secondary first
people.sort(key=lambda p: p[0])           # primary last (stable)
```

Because Timsort is **stable**, equal primary keys keep their
secondary-sorted order.

## Stability

Stability means: elements that compare equal keep their original
relative order. Python's `sorted` is stable. This is a real
guarantee, not just an implementation detail.

When stability matters: sorting records by one field while
preserving order on another (as above).

## Performance

Timsort is *O(n log n)* worst case. On real-world "mostly
sorted" data it can be *O(n)*. Highly optimized in C. For 99%
of use cases, `sorted()` is the right answer.

For top-K or bottom-K problems, `heapq.nlargest(k, arr)` is
*O(n log k)*, faster than sorting when k is small.

## Sorting custom objects

Define `__lt__` on your class, then `sorted()` works:

```python
class Item:
    def __init__(self, priority, value):
        self.priority = priority
        self.value = value
    def __lt__(self, other):
        return self.priority < other.priority
```

Or use `key=`:

```python
sorted(items, key=lambda i: i.priority)
```

## Common idioms

```python
# Sort dict by value
sorted(d.items(), key=lambda kv: kv[1])

# Sort dict by key
sorted(d.items())                          # tuples compare lexicographically

# Sort and take top K
sorted(arr)[:k]                            # O(n log n) — slower
import heapq
heapq.nsmallest(k, arr)                    # O(n log k) — faster
```
''',
        "summary": r'''
**Pattern**: `sorted(iterable, key=..., reverse=...)`. Use
`list.sort()` for in-place, `sorted()` for a new list.

**Lesson**: Timsort is stable, *O(n log n)*, optimized.
Almost always the right choice over a custom sort.

**Recognize next time**: every problem that involves ordering.
Reach for `sorted()` first; specialize only when needed.
''',
    },
    # =================================================================
    # Lecture 4 — remaining basic math (2 problems)
    # =================================================================
    {
        "id": "armstrong-number",
        "title": "Armstrong Number",
        "step_id": 1,
        "lecture_id": 4,
        "difficulty": "easy",
        "tags": ["math", "digits"],
        "what_this_teaches": (
            "Combines digit extraction (count-digits) with digit "
            "iteration (sum of digits). A two-pass digit problem."
        ),
        "pattern": "Count digits, then sum each digit raised to that power.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["count-digits", "reverse-number"],
        "next_problems": ["print-all-divisors", "check-for-prime"],
        "resources": [_STRIVER_SHEET],
        "understanding": r'''
An **Armstrong number** (also called a narcissistic number) is a
positive integer that equals the sum of its digits each raised
to the power of the number of digits.

Examples:

- `153 = 1³ + 5³ + 3³ = 1 + 125 + 27 = 153`. Yes — Armstrong.
- `9474 = 9⁴ + 4⁴ + 7⁴ + 4⁴ = 6561 + 256 + 2401 + 256 = 9474`. Yes.
- `123 = 1³ + 2³ + 3³ = 1 + 8 + 27 = 36`. No.

So the algorithm:

1. Count the digits of `n` — call it `d`.
2. Sum `digit^d` for each digit of `n`.
3. If the sum equals `n`, it's Armstrong.

```python
def is_armstrong(n):
    # Step 1: count digits
    temp = n
    d = 0
    while temp > 0:
        d += 1
        temp //= 10

    # Step 2: sum each digit to the d-th power
    temp = n
    total = 0
    while temp > 0:
        digit = temp % 10
        total += digit ** d
        temp //= 10

    return total == n
```

Two passes over the digits: one to count, one to sum. *O(d)*
where `d` is the number of digits.

A Pythonic shortcut using string conversion:

```python
def is_armstrong(n):
    s = str(n)
    d = len(s)
    return n == sum(int(c) ** d for c in s)
```

Same algorithm, more compact.

This problem combines two patterns you already know — counting
digits and summing digits — into a single check. The composition
is the lesson: many "harder" digit problems are just
combinations of simpler ones.
''',
        "summary": r'''
**Pattern**: count digits + sum digit-powers + compare.

**Lesson**: composition of simpler digit-extraction patterns. No
new technique, just a combination.

**Recognize next time**: any "is this number special?" digit
question. Count, sum (with some operation), compare.
''',
    },
    {
        "id": "print-all-divisors",
        "title": "Print All Divisors of a Number",
        "step_id": 1,
        "lecture_id": 4,
        "difficulty": "easy",
        "tags": ["math", "divisors"],
        "what_this_teaches": (
            "The divisor-pairing trick — divisors come in pairs that "
            "multiply to n, mirrored around sqrt(n). The same idea "
            "behind the O(sqrt(n)) primality check."
        ),
        "pattern": "Scan up to sqrt(n); for each divisor i, record both i and n//i.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["check-for-prime"],
        "next_problems": ["prime-factors", "sieve-of-eratosthenes"],
        "resources": [_STRIVER_SHEET],
        "understanding": r'''
Print all positive divisors of a positive integer `n`.

For `n = 12`, the divisors are 1, 2, 3, 4, 6, 12. Six divisors.

## Brute force

Walk from 1 to `n`, check each:

```python
def divisors_brute(n):
    out = []
    for i in range(1, n + 1):
        if n % i == 0:
            out.append(i)
    return out
```

*O(n)*. Works but slow for large `n`.

## Optimized: divisor pairing

Divisors come in **pairs** that multiply to `n`. For `n = 36`:

```
1 × 36
2 × 18
3 × 12
4 × 9
6 × 6
```

Every pair has one member at or below `sqrt(n)` and one at or
above. So if we scan from 1 to `sqrt(n)`, for each divisor `i`
we find, we automatically also know `n // i` is a divisor.

```python
def divisors(n):
    result = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            result.append(i)
            if i != n // i:
                result.append(n // i)
        i += 1
    return sorted(result)
```

*O(sqrt(n))* time. The `if i != n // i` check avoids
double-counting when `n` is a perfect square (e.g., for `n =
36`, we don't add both 6 and 6).

For `n = 10⁹`, this is ~31,623 iterations instead of a billion.
Massive speedup.

## A note about sorting

Our optimized version collects divisors in a mixed order (small
ones first, then large), so we `sorted()` at the end. If you
need them in sorted order during collection, you can split the
loop into two passes:

```python
def divisors_sorted(n):
    smalls = []
    larges = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            smalls.append(i)
            if i != n // i:
                larges.append(n // i)
        i += 1
    return smalls + larges[::-1]
```

Same complexity, no final sort needed.

## Why this pattern matters

The divisor-pairing trick is the same idea behind the
*O(sqrt(n))* primality check. Any time you need to enumerate
divisors, factor pairs, or test for divisibility, the
`i * i <= n` upper bound is your friend.

This is one of those small algorithmic techniques that recurs
constantly in number-theory problems.
''',
        "summary": r'''
**Pattern**: scan `i` from 1 to `sqrt(n)`; for each divisor,
record both `i` and `n // i`.

**Lesson**: divisors pair around `sqrt(n)`. The same trick
powers the primality check.

**Recognize next time**: any divisor-enumeration or factor-
finding problem.
''',
    },
    # =================================================================
    # Lecture 5 — remaining basic recursion (5 problems)
    # =================================================================
    {
        "id": "print-n-times",
        "title": "Print Something N Times using Recursion",
        "step_id": 1,
        "lecture_id": 5,
        "difficulty": "easy",
        "tags": ["recursion", "fundamentals"],
        "what_this_teaches": (
            "The simplest possible recursive function — just to "
            "feel the call stack in your hands."
        ),
        "pattern": "Base case + one recursive call.",
        "prerequisite_lessons": ["recursion"],
        "prerequisite_problems": [],
        "next_problems": ["print-1-to-n", "print-n-to-1", "sum-first-n"],
        "resources": [_STRIVER_SHEET],
        "understanding": r'''
The classroom-level recursion warmup: print "Hello" `n` times,
without a loop.

```python
def print_hello(n):
    if n == 0:
        return                # base case
    print("Hello")
    print_hello(n - 1)        # recurse with smaller n
```

For `n = 3`, the output is:

```
Hello
Hello
Hello
```

Walk through it:

- `print_hello(3)` prints "Hello", calls `print_hello(2)`.
- `print_hello(2)` prints "Hello", calls `print_hello(1)`.
- `print_hello(1)` prints "Hello", calls `print_hello(0)`.
- `print_hello(0)` returns immediately (base case).
- The stack unwinds.

The two pillars of recursion are on display:

1. **Base case**: `if n == 0: return`. Without it, the recursion
   never stops.
2. **Smaller subproblem**: `print_hello(n - 1)`. The argument
   strictly shrinks each call.

This is the simplest non-trivial recursion. If it feels obvious,
great — the rest of recursion is variations on this pattern.

A common variant: take a second argument for the message.

```python
def print_n(message, n):
    if n == 0:
        return
    print(message)
    print_n(message, n - 1)
```

Both versions are *O(n)* time and *O(n)* stack space (one frame
per recursive call).
''',
        "summary": r'''
**Pattern**: base case + one recursive call with smaller input.

**Lesson**: the simplest recursion. Two pillars: base case,
shrinking subproblem. Print is the "work" each frame does.

**Recognize next time**: every recursion has this shape; the
"work" varies.
''',
    },
    {
        "id": "print-n-to-1",
        "title": "Print N to 1 using Recursion",
        "step_id": 1,
        "lecture_id": 5,
        "difficulty": "easy",
        "tags": ["recursion", "fundamentals"],
        "what_this_teaches": (
            "The mirror of print-1-to-n. Print first, then recurse "
            "→ output is top-down (N to 1)."
        ),
        "pattern": "Act before recursing → output in arrival order.",
        "prerequisite_lessons": ["recursion"],
        "prerequisite_problems": ["print-n-times", "print-1-to-n"],
        "next_problems": ["sum-first-n", "factorial-of-n"],
        "resources": [_STRIVER_SHEET],
        "understanding": r'''
Print `n, n-1, n-2, ..., 2, 1` using recursion (no loops).

```python
def print_n_to_1(n):
    if n <= 0:
        return
    print(n)                  # act first
    print_n_to_1(n - 1)       # then recurse
```

For `n = 5`:

```
5
4
3
2
1
```

Compare with `print-1-to-n`:

```python
def print_1_to_n(n):
    if n <= 0:
        return
    print_1_to_n(n - 1)       # recurse first
    print(n)                  # then act
```

That version prints `1, 2, 3, 4, 5` — opposite order, same
recursion structure.

The deep observation: **the order in which the function does its
own work versus calling itself determines the output order**.

- **Act before recursing** → top-down. Output goes from the
  current value downward as the recursion descends.
- **Recurse before acting** → bottom-up. Output emerges as the
  recursion unwinds, from the deepest frame upward.

This same dichotomy controls:

- **Preorder vs postorder** traversal of a tree.
- **Build forward vs build backward** in DP.
- **Process before children vs after children** in any
  hierarchical structure.

It is the same idea wearing different costumes. Internalize the
swap and you have a tool that reappears everywhere.

## Iterative equivalent

```python
def print_n_to_1_iter(n):
    while n > 0:
        print(n)
        n -= 1
```

Identical output, no recursion. The iterative version uses no
stack frames; the recursive version uses `n`. For very large
`n`, prefer iteration in Python (recursion limit).

But for learning recursion, the recursive version is the point.
The order-of-operations decision is what we are practicing.
''',
        "summary": r'''
**Pattern**: act before recursing → output in input order
(top-down).

**Lesson**: swapping `act()` and `recurse()` flips the output
order. The same swap controls preorder vs postorder.

**Recognize next time**: any "do this in a specific order"
recursive problem. The order is decided by when you act.
''',
    },
    {
        "id": "sum-first-n",
        "title": "Sum of First N Natural Numbers (Recursion)",
        "step_id": 1,
        "lecture_id": 5,
        "difficulty": "easy",
        "tags": ["recursion", "math"],
        "what_this_teaches": (
            "The simplest accumulator recursion — base case 0, "
            "combine step add n. Every aggregation recursion has "
            "this shape."
        ),
        "pattern": "Base 0; combine = n + recurse(n - 1).",
        "prerequisite_lessons": ["recursion"],
        "prerequisite_problems": ["print-1-to-n", "factorial-of-n"],
        "next_problems": ["fibonacci-number", "climbing-stairs"],
        "resources": [_STRIVER_SHEET],
        "understanding": r'''
Compute `1 + 2 + 3 + ... + n` using recursion.

```python
def total(n):
    if n == 0:
        return 0              # base: sum of zero numbers
    return n + total(n - 1)   # combine: add n to the sum of 1..n-1
```

Read it as a sentence: *"the sum up to n is the sum up to n - 1
plus n; the sum up to zero is zero."* That sentence is the
algorithm.

Walk through it for `n = 4`:

```
total(4) = 4 + total(3)
         = 4 + (3 + total(2))
         = 4 + (3 + (2 + total(1)))
         = 4 + (3 + (2 + (1 + total(0))))
         = 4 + (3 + (2 + (1 + 0)))
         = 10
```

The recursion unwinds from the deepest frame outward, adding
each value as it returns.

## Alternative: pass a running total

You can also pass an accumulator as an argument — sometimes
called "tail recursion" style:

```python
def total(n, acc=0):
    if n == 0:
        return acc
    return total(n - 1, acc + n)
```

This style avoids the unwinding "add at the end" step. In
languages with tail-call optimization, the compiler converts this
into a loop. Python does **not** do TCO, so this style is no
more efficient — but it can be clearer for some problems.

## The closed-form alternative

For this specific problem, there's a famous closed-form
solution:

```python
def total(n):
    return n * (n + 1) // 2
```

*O(1)*. This is the **Gauss formula** — the same one we used in
the `missing-number` problem.

So for production code, use the formula. For learning recursion,
write the recursive version. The two together make a nice
demonstration that some problems have closed-forms that recursion
doesn't need to discover.

## Time and space complexity

Both recursive versions: *O(n)* time, *O(n)* stack space.
Closed-form: *O(1)* time and space.

For `n` up to ~1000 the recursion is fine in Python. Beyond
that, hit Python's recursion limit. Use the formula or convert
to a loop.
''',
        "summary": r'''
**Pattern**: base 0, combine = n + recurse(n - 1).

**Lesson**: the simplest aggregation recursion. Every "sum /
product / count" recursion looks like this.

**Recognize next time**: any "accumulate over 1..n" problem.
Recursive shape is fixed; only the operation differs.
''',
    },
    {
        "id": "reverse-an-array-recursion",
        "title": "Reverse an Array using Recursion",
        "step_id": 1,
        "lecture_id": 5,
        "difficulty": "easy",
        "tags": ["recursion", "arrays", "two-pointers"],
        "what_this_teaches": (
            "Recursion on two indices walking toward each other. "
            "Same shape as the iterative two-pointer reverse."
        ),
        "pattern": "Swap arr[left] and arr[right]; recurse with left+1, right-1.",
        "prerequisite_lessons": ["recursion", "arrays"],
        "prerequisite_problems": ["sum-first-n"],
        "next_problems": ["check-string-palindrome-recursion", "ll-reverse"],
        "resources": [_STRIVER_SHEET],
        "understanding": r'''
Reverse an array in place using recursion.

```python
def reverse(arr, left=0, right=None):
    if right is None:
        right = len(arr) - 1
    if left >= right:
        return                      # base case: pointers met or crossed
    arr[left], arr[right] = arr[right], arr[left]
    reverse(arr, left + 1, right - 1)
```

For `arr = [1, 2, 3, 4, 5]`:

- Call `reverse([1,2,3,4,5], 0, 4)`. Swap. Array becomes
  `[5,2,3,4,1]`. Recurse with `(1, 3)`.
- Swap. Array becomes `[5,4,3,2,1]`. Recurse with `(2, 2)`.
- `left >= right`. Return.

Three recursive calls, two swaps. *O(n/2)* time = *O(n)*.
*O(n/2)* stack = *O(n)*.

## The iterative two-pointer version

```python
def reverse_iter(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
```

Same algorithm, no stack frames. The iterative version is
preferable in production — equal speed, less memory.

## Why use recursion here?

To practice. The recursive form makes you think in pairs of
indices walking toward each other, which is the **two-pointer
mental model**. That model recurs constantly in DSA — pair
sum, palindrome, container with most water, 3-Sum, and more.

Writing reverse-array recursively forces you to:

1. Identify the base case (`left >= right`).
2. Pick the smaller subproblem (pointers moved inward).
3. Combine — here, just do the swap and recurse.

These three steps are the universal recursion recipe.

## Pythonic alternatives

```python
arr.reverse()           # in-place, O(n)
arr[::-1]               # new reversed list, O(n)
```

For production code, use these. For practice, write the
recursive version.
''',
        "summary": r'''
**Pattern**: two pointers from the ends, recursing inward with
left+1, right-1.

**Lesson**: recursion can encode two-pointer algorithms just as
well as iteration. Practice expressing both ways.

**Recognize next time**: any "operate on two ends" problem.
Reverse, palindrome check, pair sum on sorted array — all this
shape.
''',
    },
    {
        "id": "check-string-palindrome-recursion",
        "title": "Check String Palindrome using Recursion",
        "step_id": 1,
        "lecture_id": 5,
        "difficulty": "easy",
        "tags": ["recursion", "strings", "two-pointers"],
        "what_this_teaches": (
            "Recursive two-pointer palindrome check. Same shape as "
            "reverse-array, with a comparison instead of a swap."
        ),
        "pattern": "Compare s[left] and s[right]; recurse with left+1, right-1.",
        "prerequisite_lessons": ["recursion", "strings"],
        "prerequisite_problems": ["reverse-an-array-recursion"],
        "next_problems": ["ll-palindrome", "longest-palindromic-substring"],
        "resources": [_STRIVER_SHEET],
        "understanding": r'''
Check whether a string is a palindrome using recursion.

```python
def is_palindrome(s, left=0, right=None):
    if right is None:
        right = len(s) - 1
    if left >= right:
        return True              # base: empty or single character
    if s[left] != s[right]:
        return False             # mismatch — short-circuit
    return is_palindrome(s, left + 1, right - 1)
```

For `s = "racecar"`:

- `(0, 6)`: 'r' == 'r'. Recurse with `(1, 5)`.
- `(1, 5)`: 'a' == 'a'. Recurse with `(2, 4)`.
- `(2, 4)`: 'c' == 'c'. Recurse with `(3, 3)`.
- `(3, 3)`: `left >= right`. Return True.

For `s = "hello"`:

- `(0, 4)`: 'h' != 'o'. Return False.

The pattern is identical to reverse-array: two pointers walking
inward, base case when they meet. The "work" is comparison
instead of swap.

## Iterative equivalent

```python
def is_palindrome_iter(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True
```

Same algorithm without recursion.

## The Pythonic shortcut

```python
def is_palindrome(s):
    return s == s[::-1]
```

`s[::-1]` reverses the string. Compare with original — one line.

This is the right production answer. The recursive version is
for learning the two-pointer mental model.

## Variations

**Case-insensitive palindrome**:

```python
s = s.lower()
return s == s[::-1]
```

**Alphanumeric-only palindrome** (LeetCode 125):

```python
s = "".join(c.lower() for c in s if c.isalnum())
return s == s[::-1]
```

Filter first, then check.

All variations use the same core idea: reduce to a pure
palindrome check by canonicalizing the input.

## Time and space

- **Recursive**: *O(n)* time, *O(n)* stack space.
- **Iterative**: *O(n)* time, *O(1)* extra space.
- **Slice reverse**: *O(n)* time, *O(n)* space (the reversed
  copy).

For very long strings, the iterative version uses the least
memory.
''',
        "summary": r'''
**Pattern**: two pointers, compare, recurse inward, short-
circuit on mismatch.

**Lesson**: palindrome detection is the comparison version of
reverse. Same shape, different work.

**Recognize next time**: any "two ends agree?" problem.
Palindrome, valid mountain array, anagram check on aligned
strings.
''',
    },
    # =================================================================
    # Lecture 6 — remaining hashing (1 problem)
    # =================================================================
    {
        "id": "highest-lowest-frequency",
        "title": "Highest / Lowest Frequency Element",
        "step_id": 1,
        "lecture_id": 6,
        "difficulty": "easy",
        "tags": ["hashing", "counter"],
        "what_this_teaches": (
            "Build a frequency map, then walk it to find the "
            "extreme. Two passes; same shape as 'count + find max'."
        ),
        "pattern": "Counter for frequencies + max-by-value.",
        "prerequisite_lessons": ["hashing"],
        "prerequisite_problems": ["count-frequencies"],
        "next_problems": ["top-k-frequent", "majority-element"],
        "resources": [_STRIVER_SHEET],
        "understanding": r'''
Given an array, return the element with the **highest** and
**lowest** frequencies.

For `[10, 5, 10, 15, 10, 5]`:
- Frequencies: `{10: 3, 5: 2, 15: 1}`.
- Highest: 10 (appears 3 times).
- Lowest: 15 (appears 1 time).

## The algorithm

1. Build the frequency map (one pass).
2. Walk the map to find max-count and min-count entries.

```python
from collections import Counter

def highest_lowest(arr):
    freq = Counter(arr)
    highest = max(freq, key=freq.get)
    lowest = min(freq, key=freq.get)
    return highest, lowest
```

Three lines. Both `max` and `min` accept a `key=` function, so
we use `freq.get` to compare by frequency.

*O(n)* time, *O(k)* space where `k` is the number of distinct
values.

## Tiebreaking

The problem might specify what to do on ties (multiple values
share the same frequency). Default Python behavior:
- `max` returns the **first** one encountered with the maximum.
- `min` returns the **first** one encountered with the minimum.

For "any one with max frequency" the default is fine. For "the
smallest among ties," use a multi-key sort:

```python
highest = max(freq, key=lambda k: (freq[k], -k))
# Sort by frequency descending, then by value ascending (-k flips it)
```

The tuple trick generalizes to any tiebreak rule. Just build a
tuple key that captures the priority.

## When the array is huge but values are bounded

If the array's values are bounded small integers (say, 0–25 for
lowercase letters), replace the `Counter` with a fixed-size list
for slightly faster access:

```python
def highest_lowest_letters(s):
    counts = [0] * 26
    for ch in s:
        counts[ord(ch) - ord('a')] += 1
    highest_idx = max(range(26), key=lambda i: counts[i])
    lowest_idx = min((i for i in range(26) if counts[i] > 0),
                     key=lambda i: counts[i])
    return chr(highest_idx + ord('a')), chr(lowest_idx + ord('a'))
```

Note the `if counts[i] > 0` filter for lowest — we don't want
to report letters that never appeared.

## Related problems

- **Top K frequent**: heap-based version. *O(n log k)*.
- **First non-repeating character**: walk the array twice — once
  to count, once to find the first with count 1.
- **Majority element**: find the value appearing > N/2 times.
  Boyer-Moore vote does it in *O(1)* extra space.

All of them start with the same "build the frequency map" move
you've practiced here.
''',
        "summary": r'''
**Pattern**: `Counter` to build frequencies, then `max` / `min`
with `key=freq.get`.

**Lesson**: a frequency map is the bridge between "values" and
"counts." Once built, many extremes and queries are one-liners.

**Recognize next time**: any "most/least frequent X" problem.
First reach: Counter.
''',
    },
]
