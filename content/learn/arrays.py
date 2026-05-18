"""Arrays — the first data structure every learner must own."""

LESSON = {
    "id": "arrays",
    "title": "Arrays — Your First Real Data Structure",
    "tags": ["arrays", "beginner", "fundamentals"],
    "summary": (
        "What an array really is, why Python lists pretend to be arrays, "
        "how indexing actually works, and the mental model you must "
        "carry forward forever."
    ),
    "body": r'''
## What is an array, really?

Before we talk about code, let's talk about real life. Imagine you walk
into a long, narrow parking lot. The lot has numbered parking spots:
spot 0, spot 1, spot 2, and so on. Each spot can hold exactly one car.
If you want to find the car in spot 5, you do not start at the gate and
walk past every car. You walk directly to spot 5, because every spot is
the same size and they are laid out one after the other in a perfectly
predictable way. That is exactly what an array is. It is a row of
equal-sized "spots" in memory, numbered starting from 0, where each
spot holds one value.

Now read the previous paragraph one more time and notice something
important: the magic of arrays comes from the fact that **the spots are
the same size, and they sit next to each other in memory**. Because of
that, the computer can do simple arithmetic — start address plus index
times spot size — to jump straight to any spot. That is why accessing
an array by index is constant time, often written as *O(1)*. The
computer is not searching. It is jumping.

If you understand this single idea, you have understood the soul of an
array. Everything else — searches, sums, rotations, two-pointer tricks
— is built on top of that one fact.

## What about Python lists?

Here is a sentence that will save you a lot of pain later: **a Python
`list` is not exactly the same as a classical array, but for our
purposes it behaves like one.** Under the hood, CPython implements
`list` as a dynamic array of pointers. We do not need to worry about
that yet. What you should remember is:

- `nums[i]` jumps straight to the i-th item. Constant time.
- `len(nums)` is instant. The list knows its own length.
- `nums.append(x)` is *amortized* constant time. Most of the time it is
  instant; once in a while it has to copy everything to a bigger block.
- `nums.insert(0, x)` and `nums.pop(0)` are slow — *O(n)* — because
  every other element has to shuffle to make room or close the gap. We
  will see later that this is the whole reason `collections.deque`
  exists.

For now, when this site says "array", read it as "a Python list that
behaves like a row of numbered spots".

## How indexing really works (and the off-by-one trap)

This is where almost every beginner trips. The spots are numbered
starting from **zero**, not one. So in a list of length 5, the valid
indices are 0, 1, 2, 3, 4. There is no index 5. If you try `nums[5]`
you get an `IndexError`. That zero-vs-one confusion is the single most
common source of bugs for new programmers, and the only cure is to
practice until it feels natural.

Here is the mental model that finally made it click for me. Imagine the
indices as fence posts placed *between* the elements:

```
posts:   0   1   2   3   4   5
items:     A   B   C   D   E
```

Now `nums[0]` is "the item to the right of post 0", which is A. And
`nums[4]` is "the item to the right of post 4", which is E. Slicing
uses the posts directly: `nums[1:4]` means "everything between post 1
and post 4", which is `[B, C, D]`. Notice how the start is inclusive,
the end is exclusive, and the length of the slice is exactly
`end - start`. This is not random API design. It is the only way to
make slices add up cleanly.

## What can you actually do with an array?

These are the moves you must internalize so completely that you can do
them in your sleep. Every harder array problem is a recombination of
these moves.

### 1. Walk left to right

```python
# We want to visit every element exactly once, in order. This is the
# most basic loop you will ever write, and you will write it hundreds
# of times. Memorize it physically.
nums = [3, 1, 4, 1, 5, 9, 2, 6]

for i in range(len(nums)):
    # i takes the values 0, 1, 2, ... up to len(nums) - 1.
    # nums[i] is the current element. We can read it or change it.
    print(i, nums[i])
```

### 2. Walk left to right, but remember the best so far

```python
# Find the largest number. The trick: pretend the first element is the
# best, then walk forward and update the answer whenever we see better.
nums = [3, 1, 4, 1, 5, 9, 2, 6]

best = nums[0]            # our current champion
for i in range(1, len(nums)):
    if nums[i] > best:    # found a stronger challenger
        best = nums[i]    # crown it the new champion
print(best)               # 9
```

This pattern — "carry the best so far and update it as you scan" — is
the kernel of an enormous number of array problems. Maximum subarray
sum, stock buy/sell, longest run of ones, leaders in an array: they
are all variations of this one tune.

### 3. Two indices walking together

```python
# Reverse an array in place using two pointers, one at each end.
nums = [1, 2, 3, 4, 5]
left, right = 0, len(nums) - 1
while left < right:
    # Swap the two endpoints and then take a step inward from each side.
    nums[left], nums[right] = nums[right], nums[left]
    left += 1
    right -= 1
print(nums)  # [5, 4, 3, 2, 1]
```

The two-pointer pattern is its own world. We will give it a dedicated
lesson. For now just note that two indices marching toward each other,
or both marching in the same direction at different speeds, is a
recurring shape you will see everywhere.

## Common beginner mistakes (read this twice)

**Mistake 1: thinking arrays are linked lists.** They are not. Inserting
in the middle is expensive. If a problem asks for many middle
insertions, an array is probably the wrong tool.

**Mistake 2: forgetting that `for x in nums` gives you values, not
indices.** If you need the index, use `for i, x in enumerate(nums)` or
`for i in range(len(nums))`.

**Mistake 3: modifying a list while iterating over it.** Adding or
removing items mid-loop changes the indices under your feet. It is a
classic source of off-by-one bugs. The fix is usually to build a new
list, or to iterate over a copy.

**Mistake 4: confusing `nums[-1]` with an error.** In Python, negative
indices count from the right. `nums[-1]` is the last element. This is a
feature, not a bug. Use it.

**Mistake 5: assuming slices are free.** `nums[1:]` creates a brand new
list and copies the elements. In a tight loop, that copy can quietly
make your *O(n)* solution into *O(n²)*. Prefer index variables to
slices inside hot loops.

## The mental model you carry forward

When you see "array" anywhere on this site, picture a row of numbered
boxes that you can read instantly by index, walk linearly through, and
modify in place. That picture is enough to reason about almost every
problem in Step 3 of the curriculum. The harder array problems are
just clever combinations of "walk through, remember something, decide
something, walk through again".

The very last thing to internalize: the array does not know what its
values mean. It does not know if the numbers are scores, ages, or
indices into another array. Half of the cleverness in interview
problems comes from using array values as indices into themselves —
"the first array is the value, the second usage is the address". Once
you start seeing that double-meaning of numbers, hard problems start
to look easy.
''',
}
