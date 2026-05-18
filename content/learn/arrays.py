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

## 10. The promise, kept

If you read this chapter carefully, you now have:

- A mental picture of an array as a row of numbered, fixed-size
  slots in memory.
- An understanding of why indexing is *O(1)* and why front
  insertion is *O(n)*.
- A clean way to think about zero-indexing using the fence-post
  model.
- The four basic moves: walk forward, walk and carry the best,
  two pointers from the ends, and two pointers in the same
  direction.
- A checklist of questions to ask of every array problem.
- An awareness of the five most common beginner bugs and how to
  prevent them.

That is a real foundation. Almost every problem in Step 3 of the
curriculum is a recombination of these moves with a clever twist.
When you sit down to solve "Maximum Subarray Sum" or "Move Zeros"
or "Longest Subarray with Sum K," your job is no longer to invent
a brand-new algorithm — it is to recognize which of the moves
above apply, and to add the small problem-specific decoration on
top.

Take a breath. Read the chapter again if anything felt fast. Then
move on to the practice problems in Step 3, Lecture 1. They are
designed to give your new array intuition somewhere to land.
''',
}
