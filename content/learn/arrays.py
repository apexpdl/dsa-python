"""Arrays — the first data structure every learner must own."""

LESSON = {
    "id": "arrays",
    "title": "Arrays — Your First Real Data Structure",
    "tags": ["arrays", "beginner", "fundamentals"],
    "summary": (
        "A full beginner chapter. What an array really is, how memory "
        "makes indexing instant, how to walk an array confidently, the "
        "off-by-one demons and how to tame them, and the patterns "
        "that every later array problem will reuse."
    ),
    "body": r'''
## 0. Before we begin — a promise to the reader

Most courses skim arrays. They show you a list, they show you a
loop, and they march on to "real" data structures. This chapter is
not going to do that. We are going to spend a lot of words on the
single boring topic of arrays — because **every harder data
structure is built on top of arrays**, and **every later DSA
problem starts with an array intuition**. If you understand arrays
deeply, the rest of the curriculum becomes noticeably easier. If
you skim arrays, every later topic feels like wading through
treacle.

So please slow down. Read paragraphs twice if you need to. Try
the small exercises in your head. By the time you finish this
chapter you should be able to picture an array, picture a loop
walking through it, picture two pointers crawling toward each
other, and not feel mystery about any of it.

## 1. What is an array, really?

Let's start with a real-world picture, not a code snippet.

Imagine you walk into a long, narrow parking lot. The lot has
numbered parking spots, painted clearly on the asphalt: spot 0,
spot 1, spot 2, spot 3, and so on. Each spot holds **exactly one
car**. Every spot is the **same size**. The spots are arranged in
a perfect straight line, in order, with no gaps.

Now suppose I phone you and say, "Please go to spot 5 and tell me
what color the car is." What do you do? You do *not* walk in at
the entrance, look at spot 0, then spot 1, then spot 2, slowly
making your way to spot 5. That would be silly — the spots are
numbered. You walk **straight to spot 5**, look, and report back.

That is exactly how an array works. An array is a row of
equal-sized "spots" in memory, numbered starting from zero, where
each spot holds one value. Because the spots are the same size and
they sit immediately next to each other in memory, the computer
can compute the address of spot `i` directly: "start of the array,
plus `i` times the spot size." No searching. Pure arithmetic.

This is the reason we say array indexing is **O(1)** — constant
time. It is not because the computer is clever. It is because the
**layout** of an array is so regular that no cleverness is needed.
A single multiplication and a single addition give the address of
any element, no matter how huge the array is.

> **The single most important fact about arrays: they live as a
> contiguous block of equal-sized slots in memory, so any slot can
> be reached by index in constant time. Everything else flows from
> this.**

If you take only one sentence from this chapter, take that one.

## 2. Why does this matter? (Or: arrays vs. everything else)

You might be thinking: *"Okay, arrays are fast at indexing. Why
should I care?"* Here is why.

Almost every fancier data structure trades away that fast
indexing for some other power. A **linked list** can grow in the
middle cheaply, but you lose constant-time access by index — to
get to the fifth node, you have to walk four hops. A **dictionary
(hash map)** lets you look up by key, but you do not have a
natural numerical order. A **tree** organizes things hierarchically,
but you cannot index it like an array.

Arrays are the **default** because their layout is the simplest
possible thing that a computer can have: a flat row of slots. Every
other data structure adds complication to gain a feature; every
other data structure also pays for that feature in some way.

So when a problem walks in the door, your first instinct should be
*"can I solve this with an array?"* If yes, the code will usually
be simple and the performance will usually be excellent. Reach for
something fancier only when the problem actively demands it.

## 3. Python lists are arrays (mostly)

A small technical aside that will save you confusion. In Python,
the type called `list` is what we will treat as our array. It is
not *exactly* a classical fixed-size array — under the hood,
CPython implements `list` as a **dynamic array of pointers**, which
means it can grow and shrink at runtime. But for our purposes, all
the array intuition transfers:

- `nums[i]` jumps directly to the `i`-th element. Constant time.
- `len(nums)` is instant. The list keeps track of its own length.
- `nums.append(x)` is *amortized* constant time. Most of the time
  it is instant; once in a while Python has to copy the whole list
  to a larger block of memory, but if you do many appends in a row,
  the average cost is still constant.
- `nums.insert(0, x)` and `nums.pop(0)` are **slow** — *O(n)* —
  because every other element has to shift to make room or close
  the gap. This is the same fundamental reason a parking lot row
  cannot easily get a new spot inserted at the entrance: you would
  have to slide every car backward by one space.

If you take away one practical rule: **inserting and removing at
the end of a list is fast; doing it at the front (or middle) is
slow.** If your algorithm needs lots of front insertions, you do
not want a list — you want a `collections.deque`, which we will
meet in the Queues chapter.

For now, when we say "array" in this curriculum, you can read it
as "a Python list that behaves like a row of numbered slots."

## 4. The zero-indexing trap (read this twice)

Now we have to talk about the single most frequent source of bugs
for beginners. Pay attention.

Arrays start at index **zero**, not one. So an array of length 5
has the valid indices `0, 1, 2, 3, 4`. There is no index `5`. If
you try to read `nums[5]`, Python raises `IndexError: list index
out of range`. That error is the universe telling you that you
have miscounted.

The very first thing your brain has to do, every time you write
array code, is **separate "length" from "last valid index"**. The
length of an array of 5 elements is `5`. The last valid index is
`4`. They are different numbers. They differ by 1, always.

Why does this matter so much? Because **almost every off-by-one
bug** comes from mixing them up. You write a loop that runs `for
i in range(len(nums) + 1):` and it crashes. You write `while i <=
len(nums):` and it crashes. You write `nums[len(nums)]` thinking
you are reading the last element, and it crashes. These mistakes
are extremely common, and the cure is to drill the distinction
into your head until it is automatic.

Here is the mental picture that finally made it click for me, and
that I recommend to every beginner. Imagine the indices as **fence
posts placed between the elements**, not as the elements themselves:

```
posts:   0   1   2   3   4   5
items:     A   B   C   D   E
```

Five items, six posts. The items live in the gaps between the
posts. Now:

- `nums[0]` means "the item just to the right of post 0," which
  is `A`.
- `nums[4]` means "the item just to the right of post 4," which
  is `E`.
- `len(nums)` is `5`, the number of items, which also happens to
  equal the *rightmost post number*.
- `nums[5]` would mean "the item to the right of post 5," but
  there is nothing there. That is the index error.

The slice notation uses the posts directly. `nums[1:4]` means
"everything between post 1 and post 4," which is `[B, C, D]`.
Notice that the start is **inclusive** (post 1 is included as the
left edge of the first item we want), the end is **exclusive** (post
4 is included as the right edge of the last item we want), and the
length of the slice is exactly `end - start = 3`. This is not
arbitrary API design — it is the only way to make slices add up
cleanly. Slicing notation is the fence-post model written down.

Negative indices count from the right, so `nums[-1]` is the last
element (`E`), `nums[-2]` is the second-last (`D`), and so on.
Python's negative indices are not a bug; they are a feature. Use
them when they make the code clearer.

## 5. The four basic moves on an array

You will use these four moves in nearly every array problem. You
should write them so often that your fingers know the shapes
without your brain getting involved. Let's go through them slowly.

### Move 1: walk left to right

The most basic loop in DSA. We visit every element exactly once,
in order.

```python
nums = [3, 1, 4, 1, 5, 9, 2, 6]
for i in range(len(nums)):
    # i takes the values 0, 1, 2, 3, 4, 5, 6, 7.
    # nums[i] is the current element.
    print(i, nums[i])
```

Read this code as a sentence: *"For each valid index `i` in the
array, do something with `nums[i]`."* The `range(len(nums))`
produces the indices `0, 1, 2, ..., len(nums) - 1`. Notice that
`range` is **exclusive** of its endpoint, which fits the fence-post
model perfectly.

If you do not actually need the index, you can write the cleaner
form:

```python
for x in nums:
    print(x)
```

This iterates over the **values**, not the indices. Beginners
sometimes mistakenly think `for x in nums` gives them the index;
it does not. If you need both at once, use `enumerate`:

```python
for i, x in enumerate(nums):
    # i is the index, x is nums[i].
    print(i, x)
```

`enumerate` is one of the most useful tiny tools in Python. Get
comfortable with it early.

### Move 2: walk and carry a "best so far"

This is the kernel of an enormous family of array problems. We
walk through the array once, keeping a single variable that
summarizes everything we have seen.

```python
# Find the largest number in the array.
nums = [3, 1, 4, 1, 5, 9, 2, 6]
best = nums[0]                       # start by assuming the first is best
for i in range(1, len(nums)):        # consider everyone else
    if nums[i] > best:
        best = nums[i]               # crown a new champion
print(best)                          # 9
```

The mental model is a tournament. Every new element challenges the
current champion. If the challenger is bigger, it takes the crown.
After we have walked through everyone, the current champion is the
overall winner.

This pattern — "scan once, carry the best so far, update on each
step" — is the heart of the easy array problems: largest, smallest,
maximum consecutive ones, stock buy/sell (carry the cheapest price
so far), and many more. It is also the seed of Kadane's algorithm
for maximum subarray sum, which we meet in a few problems.

Whenever you find yourself thinking "for each element, I want to
know..." pause and ask: *can I carry a single scalar that summarizes
the past, and update it as I scan?* If yes, you have a single-pass
*O(n)* solution.

### Move 3: two indices walking toward each other

The two-pointer pattern is its own world, and we will give it a
dedicated chapter. For now, here is the simplest example: reverse
an array in place.

```python
nums = [1, 2, 3, 4, 5]
left, right = 0, len(nums) - 1
while left < right:
    nums[left], nums[right] = nums[right], nums[left]  # swap
    left += 1
    right -= 1
print(nums)                                            # [5, 4, 3, 2, 1]
```

Picture two fingers on the page, one at the left end and one at
the right. They swap the values they are pointing at, then each
takes one step inward. They keep doing that until they meet (or
cross) in the middle. By the time they meet, the whole array is
reversed.

Notice the loop condition: `while left < right`. Why strict less
than? Because when `left == right`, both fingers are pointing at
the same element, and swapping it with itself is pointless. We
stop before that wastes an iteration. The fence-post intuition
here is "we have done all the work needed when the fingers meet
or cross."

### Move 4: two indices walking the same way

Two pointers can also both move in the same direction, at
different speeds or with different rules. The classic example:
move all zeros to the end of an array, in place, preserving the
order of the non-zeros.

```python
def move_zeros(nums):
    write = 0                        # where the next non-zero should go
    for read in range(len(nums)):    # walk every position
        if nums[read] != 0:
            nums[write], nums[read] = nums[read], nums[write]
            write += 1
```

Two pointers, both moving rightward. The **read** pointer walks
every position. The **write** pointer marks "where the next
non-zero should land." When we find a non-zero, we swap it forward
and advance the write pointer. Zeros get left behind, and at the
end of the walk, all of them are clustered at the right side.

This same shape — "fast pointer reads, slow pointer writes" —
shows up in remove-duplicates-from-sorted-array,
remove-element, and a bunch of others. The general pattern is
**in-place compaction**: filter an array down to the elements you
want, without allocating a new array.

## 6. The arithmetic of array indices

A small but important toolbox: the arithmetic identities you will
use over and over when working with array indices.

- **Last element**: `nums[len(nums) - 1]` or `nums[-1]`. Both are
  the same. Prefer `-1` when it is clearer.
- **Middle element** (of an array of length `n`): `nums[n // 2]`.
  Note the `//` (floor division). For even `n`, this is the
  *upper* middle (e.g., for `n = 4`, `n // 2 == 2`, the third
  element).
- **Wrap around to start**: `nums[i % len(nums)]` cycles through
  the array. Used in circular array problems.
- **Distance between two indices**: `j - i` is the number of
  *gaps* between them. If you want the number of *elements*
  between `i` and `j` inclusive, it is `j - i + 1`. The "plus
  one" comes from the fence-post model: 5 fence posts have 4
  gaps but enclose 4 spaces if both ends are included.

The off-by-one identities deserve a memorization session of their
own. When in doubt, draw the fence-post picture and count.

## 7. Common beginner mistakes (and how to fix each)

Let me list the bugs I have seen the most often when teaching
arrays, with the cure for each.

**Mistake 1 — Treating arrays like linked lists.** Inserting in
the middle of an array is *O(n)*, not *O(1)*. If your algorithm
does many middle insertions, you are using the wrong data
structure. Either use a linked list (next chapter) or rethink the
algorithm to append-only.

**Mistake 2 — Mixing up `for x in nums` and `for i in
range(len(nums))`.** The first gives you values, the second gives
you indices. If you need both, use `enumerate`. If you only need
values, do not invent indices you do not use.

**Mistake 3 — Modifying a list while iterating over it.** Adding
or removing items mid-loop shifts every later element, and the
loop counter no longer points where you think it does. The cure
is usually to **build a new list** and replace at the end, or to
iterate over a copy with `for x in nums[:]:`.

**Mistake 4 — `nums[len(nums)]`.** This is an out-of-bounds read.
The last valid index is `len(nums) - 1`. Use `nums[-1]` if you
want the last element.

**Mistake 5 — Forgetting that slices copy.** `nums[1:]` builds an
entirely new list and copies all but the first element. Inside a
tight loop, that copying turns an *O(n)* algorithm into *O(n²)*
without warning. The cure: use index variables (`for i in range(1,
len(nums)):` instead of `for x in nums[1:]:`) inside hot loops.

**Mistake 6 — Confusing `range(start, stop)` boundaries.** The
`stop` is exclusive. `range(0, 5)` gives `0, 1, 2, 3, 4`, not
`0, 1, 2, 3, 4, 5`. This matches the fence-post model and is the
same convention as Python slicing. Once you see all of Python's
boundary conventions as "the right edge is exclusive," it stops
being confusing.

## 8. A mental model for thinking about array algorithms

When you read a new array problem, here is a checklist of
questions to ask in your head before writing any code. It will
save you from a lot of brute-force flailing.

1. **Is the array sorted?** If yes, you have superpowers — binary
   search and two-pointer-from-ends become available, and many
   *O(n²)* problems collapse to *O(n log n)* or *O(n)*.
2. **Do I need to know each element exactly, or just an aggregate
   (max, min, sum, count, frequency)?** If aggregate, a single
   walk with a running scalar usually works.
3. **Could a hash map turn "for each pair, check..." into a
   single pass?** If yes, you just turned *O(n²)* into *O(n)*.
4. **Can I exploit prefix sums?** If the question is about sums of
   contiguous ranges, prefix sums make range-sum queries instant.
5. **Are there negative numbers, or only non-negatives?** This
   changes whether sliding window or prefix sum is the right tool
   for "subarray with sum X."

Ask these five questions every time. Soon they become reflex.

## 9. A small but mighty insight: values can be indices

This is the move that separates beginner array work from
intermediate array work. Sometimes the **values** stored in an
array can be used as **indices** into another array (or the same
array). When that double use is available, it often unlocks
beautiful *O(n)* algorithms with no extra memory.

For example, suppose you have an array `nums` of length `n`
containing values from `1` to `n`, possibly with duplicates and
missing values. If you walk through `nums` and for each value `v`
flip the sign of `nums[v - 1]`, you have just *marked* which
values appeared, **using the array itself as a side scratch pad**.
A second walk can then read off which values were missing and
which were duplicated. *O(n)* time, *O(1)* extra space.

This trick — "the values double as indices into the same array" —
shows up in find-the-duplicate, find-missing-and-duplicate,
first-missing-positive, and other clever array problems. It will
feel like a magic trick the first time you see it; after the
fifth time, it becomes part of your normal toolbox.

## 10. The price list of array operations

Before we move on, let me hand you a small price list. Print it,
tape it above your desk, look at it every time you write array
code. This is the **cost** of each thing you might want to do, in
big-O terms. If you internalize these numbers, you will stop
choosing bad data structures by accident.

| Operation | Cost | Why |
| --- | --- | --- |
| `nums[i]` | *O(1)* | Direct address arithmetic |
| `len(nums)` | *O(1)* | The list stores its own length |
| `nums.append(x)` | *O(1) amortized* | Mostly free; occasional resize |
| `nums.pop()` (from end) | *O(1)* | Just decrement length |
| `nums.insert(0, x)` | *O(n)* | Every element shifts right by one |
| `nums.pop(0)` | *O(n)* | Every element shifts left by one |
| `nums.insert(i, x)` | *O(n-i)* | Elements after `i` shift right |
| `nums.pop(i)` | *O(n-i)* | Elements after `i` shift left |
| `x in nums` | *O(n)* | Linear scan |
| `nums.index(x)` | *O(n)* | Linear scan |
| `nums.count(x)` | *O(n)* | Scan and count |
| `nums.sort()` | *O(n log n)* | Timsort |
| `sorted(nums)` | *O(n log n)* | Same but returns a new list |
| `nums.reverse()` | *O(n)* | Swap from both ends |
| `nums[a:b]` | *O(b-a)* | Slice **copies** |
| `nums + other` | *O(n+m)* | Concatenation copies both |
| `nums * k` | *O(n·k)* | Repetition copies n times |
| `nums == other` | *O(n)* | Element-by-element compare |
| `min(nums)` / `max(nums)` | *O(n)* | Linear scan |
| `sum(nums)` | *O(n)* | Linear scan |

A few of these deserve more conversation, because their costs
**surprise people**. The big surprise is that `nums[1:]` is *O(n)*,
not *O(1)*. Many beginners write code like this:

```python
def sum_recursive(nums):
    if not nums:
        return 0
    return nums[0] + sum_recursive(nums[1:])
```

This looks like it does *n* recursive calls, each doing constant
work — so *O(n)* total, right? Wrong. Each `nums[1:]` builds a
brand-new list of size `n-1`. The total work to build all those
slices is `n + (n-1) + (n-2) + ... + 1`, which is *O(n²)*. The
moral: when you are inside a loop or recursion, prefer **index
variables** over slicing. Slices are wonderful at the top level;
they are deadly in the inner loop.

The second surprise is `x in nums`. People who learned dicts
first sometimes assume `in` is fast on every Python container. It
is *O(1) average* on a `set` or `dict` key, but *O(n)* on a list,
because the list has to scan. If your algorithm does many `in`
checks, you almost certainly want to convert to a set first.

The third surprise is **list concatenation in a loop**. The classic
trap:

```python
result = []
for x in some_iter:
    result = result + [x]    # creates a brand-new list every time
```

That inner statement copies the whole current `result` plus one
new element, every loop iteration. The total work is *O(n²)*. The
fix is `result.append(x)`, which is amortized *O(1)*. Or use a
list comprehension. Anything except `result = result + [x]`.

## 11. Prefix sums — the calculator your array secretly contains

Now we enter the first "real" technique that goes beyond the
beginner basics. **Prefix sums** are the technique that turns
"sum of any range" from an *O(n)* operation into an *O(1)*
operation, at the cost of one extra *O(n)* pass to build them.
It is one of the highest-value tricks in the whole DSA toolbox.

Picture a long line of mailboxes, each containing some number of
letters. Suppose someone phones you and asks, "How many letters
total in mailboxes 5 through 8?" The naive answer: walk down the
line, open mailboxes 5, 6, 7, and 8, count their letters, sum
them up, report. That is fine for one question. But what if your
boss is going to ask you fifty range questions today? Now you are
walking the line fifty times. Each walk takes time.

The clever clerk takes a different approach. On day one, the
clerk walks down the line **once** and writes down, on a fresh
sheet of paper, a running total: "After mailbox 0, total letters
= 3. After mailbox 1, total = 7. After mailbox 2, total = 10. ..."
Now, for any range question, the clerk just subtracts two numbers
from that sheet. "Mailboxes 5 to 8 inclusive" becomes "total after
mailbox 8 minus total after mailbox 4." One subtraction. Constant
time. The walk down the line only happens once.

That sheet is the **prefix sum array**. In code:

```python
def build_prefix(nums):
    # prefix[i] = nums[0] + nums[1] + ... + nums[i-1].
    # Length is n+1 so that prefix[0] is the empty-sum (zero).
    prefix = [0] * (len(nums) + 1)
    for i, x in enumerate(nums):
        prefix[i + 1] = prefix[i] + x
    return prefix

def range_sum(prefix, lo, hi):
    # Sum of nums[lo..hi] inclusive.
    return prefix[hi + 1] - prefix[lo]
```

Trace it on `nums = [3, 1, 4, 1, 5, 9, 2, 6]`:

```
indices:  0  1  2  3  4  5  6  7
values:   3  1  4  1  5  9  2  6
prefix:  0  3  4  8  9 14 23 25 31    (length 9)
```

To get the sum of `nums[2..5]`, take `prefix[6] - prefix[2]` =
`23 - 4` = `19`. Verify: `4 + 1 + 5 + 9 = 19`. ✓

Notice the **+1 offset** in the prefix array — we make it length
`n + 1` and shift all indices up by one. Why? Because we need an
"empty sum at the left" so that `prefix[hi + 1] - prefix[lo]`
works for `lo = 0` without a special case. The empty sum is zero
and lives at `prefix[0]`. This is the fence-post model again, in
disguise.

**Where prefix sums show up.** Range-sum-query problems, "find
subarray with sum K" (combined with a hash map), "subarray sum
divisible by K," moving averages, problems with "how many ranges
satisfy ..." When you see *any* problem asking about sums (or
counts, products, XORs — same idea with different operator) over
arbitrary ranges, your first thought should be: *prefix sums*.

### Difference arrays — the dual of prefix sums

While we're here, let me show you the **difference array**, which
is prefix sums upside down. It is what you reach for when the
problem says "add `v` to every element in range `[lo, hi]`" and
asks the result *after many such updates*.

A difference array `diff` stores, at index `i`, the **change**
from `nums[i-1]` to `nums[i]`. To "add `v` to range `[lo, hi]`,"
you do `diff[lo] += v` and `diff[hi+1] -= v`. Both *O(1)*. After
all updates, you take the prefix sum of `diff` to recover the
final `nums`. That's *O(n)* once, no matter how many updates.

```python
def apply_updates(n, updates):
    diff = [0] * (n + 1)
    for lo, hi, v in updates:
        diff[lo] += v
        diff[hi + 1] -= v
    # prefix sum reconstructs the final array
    result = [0] * n
    running = 0
    for i in range(n):
        running += diff[i]
        result[i] = running
    return result
```

The difference array turns "k range updates, then read all" from
*O(k·n)* into *O(k + n)*. Magical when k is huge.

## 12. The "scan once, remember the best" pattern in depth

I want to dwell on this pattern more, because it is the soul of
many easy and medium array problems. The pattern is:

> Walk the array left to right. At each step, you can compute
> the answer-so-far using the new element and a small constant
> amount of remembered information. Update both the
> answer-so-far and the remembered information. At the end of
> the walk, the answer-so-far *is* the answer.

This is a state machine, even though it doesn't look like one.
The "state" is whatever you remember from the past. Different
problems need different remembered state:

- **Maximum element**: remember the best value seen so far.
- **Best stock profit (Buy/Sell I)**: remember the cheapest
  price seen so far.
- **Maximum subarray sum (Kadane)**: remember the best subarray
  *ending here*.
- **Longest streak of 1s**: remember the current streak length.
- **First missing positive (with caveats)**: remember which
  values have been "marked."

Let me show Kadane in detail because it is the most famous example.
The problem: given an array of integers (positive and negative),
find the maximum sum of any contiguous subarray.

The naive *O(n²)* approach tries every (left, right) pair. Kadane
realizes that as we walk left to right, the best subarray
**ending at position `i`** is one of two things: either it is
just `nums[i]` itself (starting fresh), or it is the best subarray
ending at `i - 1` plus `nums[i]` (extending). So we keep one
variable `cur` = best sum ending at the current index, and one
variable `best` = best sum seen anywhere yet.

```python
def kadane(nums):
    cur = best = nums[0]                 # best ending here, best ever
    for x in nums[1:]:
        cur = max(x, cur + x)            # extend or restart
        best = max(best, cur)
    return best
```

Trace on `[-2, 1, -3, 4, -1, 2, 1, -5, 4]`:

```
x:   -2   1   -3   4   -1   2   1   -5   4
cur: -2   1   -2   4    3   5   6    1   5
best:-2   1   -2   4    4   5   6    6   6
```

Answer: 6, from subarray `[4, -1, 2, 1]`. Verify by brute force if
you don't believe it.

The insight that turned *O(n²)* into *O(n)* was just **one extra
variable**. The whole "scan once, carry state" pattern is exactly
this: the right state turns an expensive nested loop into a single
linear walk. When you face an array problem, before writing the
double loop, ask yourself: *what could I remember from the past
that would let this be a single walk?*

## 13. Two-dimensional arrays (matrices)

Up to now we have talked about one-dimensional arrays. Many DSA
problems involve **2D arrays**, also called matrices: grids of
values arranged in rows and columns. In Python, these are usually
represented as a "list of lists":

```python
grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
```

`grid[r][c]` is the value at row `r`, column `c`. Convention: row
first, column second. The number of rows is `len(grid)`. The
number of columns is `len(grid[0])` (assuming all rows are the
same length, which they should be).

To walk every cell of a matrix, you nest two loops:

```python
m, n = len(grid), len(grid[0])           # m rows, n columns
for r in range(m):
    for c in range(n):
        # do something with grid[r][c]
        ...
```

The cost is *O(m·n)*. Notice that I named the dimensions `m` and
`n` — this is a near-universal convention in DSA. Stick to it.

**Moving in four directions.** For grid problems (flood fill,
islands, shortest path on a grid), you often need to look at the
four neighbors of a cell. The standard idiom uses **direction
vectors**:

```python
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # up, down, left, right

for dr, dc in DIRS:
    nr, nc = r + dr, c + dc
    if 0 <= nr < m and 0 <= nc < n:
        # nr, nc is a valid neighbor
        ...
```

The boundary check `0 <= nr < m` says "nr is a valid row index";
similarly for `nc`. Skip cells that fall off the grid.

**Walking diagonally.** Two diagonals: from top-left to
bottom-right, and from top-right to bottom-left. The diagonal
walking trick: cells `(r, c)` on the same top-left-to-bottom-right
diagonal share `r - c` (constant). Cells on the same
top-right-to-bottom-left diagonal share `r + c` (constant). This
fact powers many matrix problems (Pascal's triangle, anti-diagonal
sums, N-Queens conflict tests).

**Be careful constructing a matrix.** This snippet looks innocent
but is a famous bug:

```python
grid = [[0] * 3] * 3        # WRONG — all three rows are the SAME list
```

`[0] * 3` creates one list. `[...] * 3` creates a list of **three
references to the same inner list**. Mutating `grid[0][0]` also
mutates `grid[1][0]` and `grid[2][0]`, because they all point at
the same memory. The fix is a comprehension:

```python
grid = [[0] * 3 for _ in range(3)]   # three independent rows
```

This builds a fresh inner list each iteration. Memorize this idiom;
you will need it constantly in DP and grid problems.

## 14. The values-as-indices super-trick

I sketched this in section 9. Let me dwell on it because it is
the move that separates "I can do easy array problems" from "I can
do clever array problems."

The trick: when your array contains values from a known small range,
those values can be used as **indices** into the same array (or
a side array of the same size). This often lets you mark, count,
or transform without allocating any new memory.

**Example: find the first missing positive.** Given an unsorted
array of length `n`, find the smallest positive integer that does
not appear in it. The trick: the answer must be in the range
`[1, n + 1]`. (Why? Because if all of `1` through `n` appear, the
answer is `n + 1`; otherwise, some integer in `1..n` is missing.)

So we can do two passes:

```python
def first_missing_positive(nums):
    n = len(nums)
    # pass 1: put each value v at index v - 1 if 1 <= v <= n
    i = 0
    while i < n:
        v = nums[i]
        if 1 <= v <= n and nums[v - 1] != v:
            nums[v - 1], nums[i] = nums[i], nums[v - 1]
        else:
            i += 1
    # pass 2: scan for the first slot where the wrong value sits
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    return n + 1
```

After pass 1, position `i` holds value `i + 1` if and only if that
value appeared in the original array. Pass 2 finds the first
violation, which gives the missing value. *O(n)* time, *O(1)*
extra memory.

The mental key: *we cycled values into their "correct" slots, using
the array itself as the marking surface*. No extra hash set. No
extra count array. Just clever use of what we already had.

**Other classic uses:**
- **Find the duplicate number** (each value 1..n appears exactly
  once except one that appears twice) — same cycling trick.
- **Set matrix zeroes** — use the first row and first column as
  flags, then fix them up in a final pass.
- **Rotate array by k** — three reverses, no extra memory.

The reason these tricks feel like magic is that you are using
*one piece of memory in two different ways* — both as data and as
bookkeeping. They reward people who think structurally about what
the array could be made to do.

## 15. Common bugs (extended catalog)

I gave you five common mistakes in section 7. Here is the longer
catalog. Each one I have personally seen in interviews, in code
reviews, and (embarrassingly) in my own code at three in the
morning.

**Aliasing.** `b = a` does not copy. After `b.append(99)`, the
list `a` also has `99` at the end. `a` and `b` are two names for
the same list. To copy: `b = a.copy()` or `b = list(a)` or
`b = a[:]`. All three give you an independent copy. Beware
nested lists — those need `copy.deepcopy(a)` if the inner lists
should also be independent.

**Off-by-one in range.** `range(1, n)` runs from `1` to `n - 1`
inclusive. If you want to include `n`, write `range(1, n + 1)`.
The exclusive end is consistent with slicing; once you internalize
it, the "+1" inconsistencies vanish.

**Forgetting to bound-check a 2D access.** `grid[r][c]` will
crash with an `IndexError` if `r` or `c` is out of range. Either
guard with `0 <= r < m and 0 <= c < n`, or write a small helper:

```python
def in_bounds(r, c, m, n):
    return 0 <= r < m and 0 <= c < n
```

and use it.

**Comparing floats for equality.** `0.1 + 0.2 == 0.3` is False
in Python because floats are binary approximations. If you need
to check equality of floats, allow a small epsilon:
`abs(a - b) < 1e-9`. Or just avoid floats entirely; many DSA
problems are happier with integers.

**Misusing `list.index`.** `nums.index(x)` returns the index of
the *first* occurrence of `x`. Many algorithms that "find" a value
secretly do this in a loop, leading to *O(n²)* surprises. Prefer
explicit `for i, v in enumerate(nums):` when you need fine control.

**Empty arrays.** `nums[0]` on `[]` raises `IndexError`.
`max([])` raises `ValueError`. Many algorithms assume a
non-empty array; if the problem says "the array may be empty,"
handle that case first.

**Strides in slices.** `nums[::-1]` reverses. `nums[::2]` takes
every other element. `nums[1::2]` takes every other element
starting at index 1. These are powerful but easy to misread.
When in doubt, write a normal loop.

**Mutating inside a comprehension.** Comprehensions are for
*building* new lists, not for side effects. Don't do
`[print(x) for x in nums]`; just write `for x in nums: print(x)`.
The comprehension creates a useless list and obscures intent.

**Forgetting that `min` and `max` need a key sometimes.** To find
the longest string in a list, you want `max(strings, key=len)`,
not `max(strings)`. The default `max` compares values directly,
which on strings means lexicographic order.

**The "remove all occurrences" foot-gun.**

```python
for x in nums:
    if x == target:
        nums.remove(x)                  # BUG: skips elements
```

Removing during iteration is the classical bug. The cure is one
of:

```python
nums = [x for x in nums if x != target]      # build new
# or
nums[:] = [x for x in nums if x != target]   # in place
```

The `nums[:] = ...` form is sometimes wanted when other code holds
a reference to the same list. Otherwise, plain reassignment is
fine.

## 16. A practical reference card

Print this out. Tape it next to the price list from section 10.

**To do this . . .                                . . . reach for this.**
- Walk every element ...................... `for x in nums:`
- Walk with index ......................... `for i, x in enumerate(nums):`
- Walk in reverse ......................... `for x in reversed(nums):`
- Walk pairs (i, i+1) ..................... `for i in range(len(nums) - 1):`
- Walk pairs (i, j) where i < j ........... nested loops, *O(n²)*
- Build with arithmetic ................... list comprehension
- Filter ................................... `[x for x in nums if cond(x)]`
- Map ...................................... `[f(x) for x in nums]`
- Sum ...................................... `sum(nums)`
- Min / max ................................ `min(nums)` / `max(nums)`
- Count ................................... `nums.count(x)`
- Find index .............................. `nums.index(x)` (raises if missing)
- Membership .............................. `x in nums` (O(n) on list)
- Sort ascending .......................... `nums.sort()` (in place)
- Sort descending ......................... `nums.sort(reverse=True)`
- Sort by key .............................. `nums.sort(key=lambda x: ...)`
- Reverse in place ........................ `nums.reverse()`
- Reverse as a new list ................... `nums[::-1]`
- Copy list ................................ `nums.copy()` or `list(nums)`
- Concatenate .............................. `a + b` (creates new)
- Extend in place .......................... `a.extend(b)`
- Find max-by-key .......................... `max(nums, key=...)`
- Group by key ............................. dict from key to list
- Top-K elements ........................... `heapq.nlargest(k, nums)`
- Unique elements .......................... `set(nums)` or `list(dict.fromkeys(nums))`

If you don't know one of these by heart, that's fine — but try
to reach for the idiom rather than re-deriving it from scratch.
Idioms are fast both to write and to read.

## 17. Mental practice exercises (no code)

I want to leave you with a few mental exercises. Don't write code.
Just sit with each one for a minute and visualize.

1. *On the array `[5, 2, 8, 1, 9, 3]`, where do the left and
   right pointers point after the first iteration of the
   reverse-in-place algorithm? After the second? When does the
   loop end?*

2. *On the same array, walk Kadane's algorithm in your head. What
   are the values of `cur` and `best` after each element?*

3. *If `nums = [3, 1, 4, 1, 5]`, what is the prefix sum array?
   What does `prefix[4] - prefix[1]` equal, and which elements
   does it sum?*

4. *I want to add `5` to `nums[2..5]` and `-2` to `nums[1..3]` on
   an array of length 8. Using a difference array, what entries
   do I touch? What does the difference array look like before
   the final prefix-sum reconstruction?*

5. *Why is the "values as indices" trick possible only when the
   values are in a bounded range? What goes wrong if the array
   contains the number `10⁹`?*

If you can answer all five without writing code, you have
internalized this chapter. If any feel uncertain, scroll back to
the relevant section and re-read. There is no rush.

## 18. Looking ahead — where this lesson lands in the curriculum

Every problem in Step 1, Step 2, and Step 3 is some recombination
of the moves and patterns in this chapter. Let me name a few so
you know where you are headed.

- **Step 1 problems** (Largest Element, Second Largest, Sorted
  Check, Rotate Array, Move Zeros, Union of Sorted Arrays,
  Missing Number, Single Number) all use the basic walk + carry
  + two-pointer moves you just learned.
- **Step 3 Easy** (Largest, Second Largest, Sorted Check, Rotate,
  Move Zeros, Remove Duplicates, Find Missing, Maximum
  Consecutive Ones, Single Number, Longest Subarray Sum K) is
  the gym — these problems are designed to make the patterns
  reflexive.
- **Step 3 Medium** (Two Sum, Sort 0s 1s 2s, Majority Element,
  Maximum Subarray, Best Time to Buy and Sell Stock, Rearrange
  +/-, Next Permutation, Leaders, Longest Consecutive Sequence,
  Set Matrix Zeros, Rotate Image, Spiral Matrix, Pascal Triangle,
  Subarray with Sum K) brings in slightly more state. Kadane,
  prefix sum, two pointers, the values-as-indices trick — all
  applied to slightly twistier setups.
- **Step 3 Hard** (Pascal Triangle II, Majority N/3, 3-Sum,
  4-Sum, Largest Subarray Zero Sum, Subarray with XOR K, Merge
  Intervals, Merge Two Sorted Arrays In Place, Find Repeating
  and Missing, Reverse Pairs, Maximum Product Subarray, Count
  Inversions) extends prefix sum, sliding window, and merge
  sort into harder territory.

When you start a problem in any of these, your first instinct
should be: *which of the moves from this chapter applies here?*
Don't reinvent. Recognize.

## 19. The promise, kept (finally)

If you have read this far, you have done more thinking about
arrays than 90% of self-taught programmers ever do. That is not
hyperbole — most people skim the basics, hit a wall on a medium
problem, and never figure out that the wall was made of beginner
material they accidentally skipped.

You should now have:

- A picture in your head of how an array sits in memory — slots
  in a row, fixed size, no gaps.
- An understanding of **why** indexing is *O(1)* and front
  operations are *O(n)*. (It is purely about layout, not
  cleverness.)
- A confident handle on zero-indexing using the fence-post
  model, which generalizes to slicing, `range`, and every other
  half-open Python convention.
- The four basic moves — left-to-right, scan-and-carry,
  two-pointer-from-ends, two-pointer-same-direction — that
  underlie most array algorithms.
- The prefix-sum and difference-array techniques for fast range
  queries and bulk updates.
- A working knowledge of 2D arrays, direction vectors, and the
  classic mutable-default bug `[[0]*n]*m`.
- The "values as indices" super-trick for in-place algorithms.
- A long list of common bugs with concrete fixes.
- A checklist of questions to ask before writing any array code.
- A reference card of idioms to reach for.

That is a real foundation. Almost every problem in Step 3 of the
curriculum is a recombination of these moves with a clever twist.
When you sit down to solve "Maximum Subarray Sum" or "Move Zeros"
or "Longest Subarray with Sum K," your job is no longer to invent
a brand-new algorithm — it is to recognize which of the moves
above apply, and to add the small problem-specific decoration on
top.

Take a breath. Read the chapter again if anything felt fast. Re-do
the mental exercises in section 17. Then move on to the practice
problems in Step 3, Lecture 1. They are designed to give your new
array intuition somewhere to land.
''',
}
