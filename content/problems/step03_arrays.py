"""Step 3 — Arrays.

The biggest single lecture in this curriculum. Almost every array
problem boils down to a combination of: walk once, remember
something, use a hash, or sort first.
"""
from __future__ import annotations

PROBLEMS: list[dict] = [
    {
        "id": "largest-element",
        "title": "Largest Element in an Array",
        "step_id": 3,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["arrays", "linear-scan"],
        "what_this_teaches": (
            "The single most reused move in array DSA: walk once, "
            "carry a 'best so far' scalar, return it. Master this and "
            "you have ninety percent of easy array problems already "
            "in your fingers."
        ),
        "pattern": "Single-pass linear scan with a running scalar.",
        "prerequisite_lessons": ["arrays"],
        "prerequisite_problems": [],
        "next_problems": [
            "second-largest-element",
            "check-array-sorted",
            "max-consecutive-ones",
            "kadane-algorithm",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 3 (Easy Arrays)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "Python docs — built-in max()",
                "url": "https://docs.python.org/3/library/functions.html#max",
            },
        ],
        "understanding": r'''
We have an array of numbers like `[3, 8, 1, 9, 2, 4]`. We want to
return the largest one — in this example, `9`. That is the entire
problem.

It is the first array problem in the sheet for a reason. It teaches
the single most reused pattern in all of array work:

> *Walk through the array once, carrying along "the best so far",
> and update it whenever you see something better.*

Once that move is in your fingers, you have it forever.
''',
        "brute_force": {
            "explanation": r'''
For each element, ask: "is this the largest?". To answer, walk the
entire array and compare. *O(n²)* if you take the question literally.

```python
for i in range(n):
    if all(arr[i] >= arr[j] for j in range(n)):
        return arr[i]
```

Nobody writes this seriously, but it is a useful "wrong" baseline to
contrast with the correct one-pass solution.
''',
            "code": r'''def largest_brute(arr: list[int]) -> int:
    # For each candidate index i, verify it is at least as big as
    # every other element. The first one that passes is the max.
    n = len(arr)
    for i in range(n):
        ok = True
        for j in range(n):
            if arr[j] > arr[i]:
                ok = False
                break
        if ok:
            return arr[i]
    # Defensive return; should not reach here for non-empty arrays.
    raise ValueError("empty array")
''',
            "walkthrough": r'''
This is the "test every candidate against every other element"
approach. Inefficient but very explicit.

**`def largest_brute(arr: list[int]) -> int:`** — Takes a list
of integers, returns the largest one.

**`n = len(arr)`** — Cache the length. We'll reference it
twice inside loops, and reading `len(arr)` every time has a
tiny but real cost.

**`for i in range(n):`** — Outer loop: pick each index `i` in
turn as our candidate for "the largest."

**`ok = True`** — Optimistically assume the current candidate
is the largest. We'll set this to False if we find evidence
otherwise.

**`for j in range(n):`** — Inner loop: scan every other index
`j`. We're checking: is there any element that's bigger than
`arr[i]`? If yes, `arr[i]` is not the max.

**`if arr[j] > arr[i]:`** — Found an element bigger than the
candidate. The candidate is not the max.

**`ok = False; break`** — Mark the candidate as failed and
break out of the inner loop. No point checking the rest of
`j` once we've found a counter-example.

**`if ok: return arr[i]`** — If the inner loop completed
without finding anything bigger, then `arr[i]` *is* the max.
Return it.

**`raise ValueError("empty array")`** — Defensive code in case
the array is empty. The outer loop wouldn't run, and we'd fall
through without returning.

The total work: for each of `n` candidates, we scan up to `n`
elements. That's `n × n = n²` operations in the worst case.
For `n = 1000`, that's a million operations — still fast. For
`n = 1,000,000`, that's a trillion — way too slow. The
optimized version below uses a single scan.

This is the kind of brute force we write *first* — easy to
understand, easy to verify, but not what we ship.
''',
            "complexity": (
                "**Time**: *O(n²)* — we re-scan for each candidate.\n\n"
                "**Space**: *O(1)*."
            ),
        },
        "thought_process": r'''
After writing the brute force you immediately notice the wasted
work. We do not need to know "is `arr[i]` the largest?" for every
`i`. We only need the largest overall. So we walk once, carrying
"best so far", and update it whenever we see a bigger value.

The mental model is "tournament": every new element challenges the
current champion. If the challenger is bigger, it becomes the new
champion. After we have walked through everyone, the champion is
the winner.

A subtle detail: we should initialize the champion to something
sensible. Two choices:

1. **Start with `arr[0]`** and loop from index 1. Clean and
   intention-revealing.
2. **Start with `float('-inf')`** and loop from index 0. Also fine,
   handles empty arrays gracefully (returns `-inf`).

Both work. Choice (1) is more common in interviews and more honest
about the precondition that the array is non-empty.
''',
        "optimized": {
            "explanation": r'''
Single pass with a running maximum. *O(n)* time, *O(1)* extra space.
''',
            "code": r'''def largest(arr: list[int]) -> int:
    # Treat the first element as the initial champion.
    best = arr[0]
    # Walk through the rest and replace the champion when challenged.
    for i in range(1, len(arr)):
        if arr[i] > best:
            best = arr[i]
    return best
''',
            "walkthrough": r'''
This is one of the most important "small patterns" in all of
DSA. Memorize it. Variants of this loop appear in dozens of
problems.

**`def largest(arr: list[int]) -> int:`** — Same signature.

**`best = arr[0]`** — Initialize our running maximum to the
first element. We pick `arr[0]` because we have no other
information yet — the first element is the best we've seen so
far (the only one we've seen, in fact). Some people use
`float('-inf')` here for safety, but `arr[0]` works as long
as the array is non-empty.

**`for i in range(1, len(arr)):`** — Loop from index 1 to the
end. Why start at 1 and not 0? Because we already used
`arr[0]` as our initial `best`. Comparing it against itself
would be wasted work.

You might also write this as:
```python
for x in arr[1:]:
    if x > best: best = x
```
Both are correct. The index version is slightly more
efficient (no slice copy), but for normal-sized inputs the
difference is negligible.

**`if arr[i] > best:`** — The challenger comparison. Is this
new element bigger than our current champion?

**`best = arr[i]`** — Crown the new champion. If `arr[i]` is
bigger than the previous best, it becomes the new best. We
keep this updated as we walk.

**`return best`** — After the loop completes, `best` holds
the maximum value seen anywhere in the array. Return it.

The mental model: imagine a tournament where each new array
element challenges the reigning champion. If the challenger
is stronger (bigger), they take the crown. After everyone has
challenged once, whoever is wearing the crown is the overall
winner.

Total work: we look at each element exactly once (after the
initial `arr[0]`). That's *O(n)*. The brute force did *O(n²)*
by comparing every element against every other; the optimized
version compares each element only against the running best.
The insight that turned `n²` into `n` is just **one extra
variable** — `best` — carried across iterations.
''',
            "complexity": (
                "**Time**: *O(n)*. **Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
"Walk once and track the best so far" is the kernel of an immense
family of array problems. Some examples on this very sheet:

- **Second largest** — track two best-so-far values.
- **Max consecutive ones** — track the current run and the best run.
- **Stock buy/sell** — track the minimum price so far and the max
  profit so far.
- **Maximum subarray sum (Kadane)** — track the best subarray
  ending here and the best overall.

The common structure: as you walk, you carry one or two scalars that
summarize "everything seen so far". The output is one of those
scalars at the end.

When you start solving harder problems, you will find that the
biggest difficulty is **choosing what to carry**. "What single
number captures everything I need to know about the prefix I have
seen so far?" — that is the central question. For "largest", the
answer is obvious: the largest value seen. For Kadane, the answer
takes some thought. For longest-consecutive-sequence, the answer
involves a hash. But the shape is the same.
''',
        "confusion_notes": [
            {
                "question": "Why initialize `best = arr[0]` instead of `0` or `float('-inf')`?",
                "answer": r'''
Because the array might contain only **negative** numbers, in
which case starting at `0` would give the wrong answer.

If `arr = [-3, -7, -2, -9]`, the true largest is `-2`. If we
initialize `best = 0`, the comparison `arr[i] > best` is false
for every element (since every element is less than 0), and we
return `0` — a value that does not even appear in the array.
Wrong.

Initializing `best = arr[0]` sidesteps this entirely. By the
**first** iteration, `best` is already a real element of the
array, so we cannot return a phantom value. From there, every
update only moves `best` toward a larger real element.

The other safe initialization is `float('-inf')`, which is
guaranteed to be smaller than any real number. Both styles work.
The `arr[0]` style is preferred when you can assume the array
has at least one element (which you can, in this problem). It
also tells the reader of your code "I know the array is
non-empty, and I am starting from a real element of it."

Lesson: the initial value of a running scalar matters, especially
when the input has signs you might not have considered. Always
ask: *"could the input be all-negative, all-zero, or empty? Does
my initialization handle those?"*
''',
            },
            {
                "question": "Could I just use Python's built-in `max(arr)`?",
                "answer": r'''
Yes, and in production code, that is the right answer. `max(arr)`
is exactly equivalent to our single-pass loop, but implemented in
optimized C, so it runs faster than the hand-written Python loop.

The reason we write the explicit loop in DSA practice is to
**make the algorithm visible**. The point of the exercise is to
internalize the pattern "walk once, carry the best so far, update
on improvement." Once that pattern is in your fingers, you can
recognize it in much harder problems (Kadane, max consecutive
ones, stock buy-sell), where there is no built-in shortcut.

Treat `max(arr)` as the cheat code for this specific problem —
fast, correct, idiomatic. Treat the loop version as the **tool**
you carry to every harder problem in the lecture.

In interviews, write the loop unless the interviewer explicitly
allows the built-in. The point of the question is rarely "do you
know about `max`" — it is "can you express this scan yourself?"
''',
            },
            {
                "question": "Why does the loop start at index 1?",
                "answer": r'''
Because we already used `arr[0]` to initialize `best`, so there
is no need to compare it against itself. Starting the loop at
index 1 saves one iteration and makes the intent clearer:
*"`arr[0]` is the initial champion; compare it against every
later element."*

If we started at index 0, the very first iteration would compare
`arr[0]` with `best` (which equals `arr[0]`). The condition
`arr[0] > best` is false, so nothing happens. Correct but wasted
work.

`range(1, len(arr))` produces indices `1, 2, ..., len(arr) - 1`.
The `1` is the inclusive start, the `len(arr)` is the exclusive
stop. Together they cover every index that has not been
"consumed" by the initialization.

This pattern — "use index 0 as initialization, loop from index 1
to the end" — is one of the standard idioms for running-scalar
algorithms. You will write it many times in this lecture.
''',
            },
            {
                "question": "What if the array is empty?",
                "answer": r'''
Then this algorithm crashes, because `arr[0]` on an empty list
raises `IndexError`. The function does not handle the empty case.

Should it? That depends on the problem. Most curriculum versions
of "largest element" promise that the array has at least one
element, so a crash is acceptable. If you want to be defensive,
add a guard:

```python
if not arr:
    return None  # or raise ValueError, depending on convention
```

This is the same kind of edge-case discipline we discussed for
`count-digits` (special-case `n == 0`). When you sit down to
solve a new problem, pause and ask:
- What if the array is empty?
- What if it has one element?
- What if all elements are equal?
- What if the array is sorted? Reverse-sorted?

For "largest," each of these is fine with the algorithm above
*except* the empty case. Either guard against it or document the
precondition.

In interview practice, mention the empty case out loud. "I am
assuming the array is non-empty; if it can be empty I would add
a guard and return [None / raise / ...]." This shows that you
think about edge cases, even when you do not handle them.
''',
            },
        ],
        "summary": r'''
**Pattern**: linear scan with a running scalar.

**Lesson**: the simplest array problem teaches the most reused
move. Walk once, carry a summary, return it.

**Recognize next time**: anywhere "find the maximum / minimum /
longest / smallest" applies. Always reach for the single-pass
running-scalar pattern first.
''',
    },
    {
        "id": "second-largest-element",
        "title": "Second Largest Element (No Sorting)",
        "step_id": 3,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["arrays", "linear-scan"],
        "what_this_teaches": (
            "The 'top K' pattern in miniature: maintain K best-so-far "
            "scalars and update them carefully when a new champion "
            "arrives. The careful update order — *demote the old "
            "champion before crowning the new one* — is the part "
            "beginners miss."
        ),
        "pattern": "Maintain the top two scalars; demote-then-crown on each new candidate.",
        "prerequisite_lessons": ["arrays"],
        "prerequisite_problems": ["largest-element"],
        "next_problems": [
            "check-array-sorted",
            "kth-largest",
            "top-k-frequent",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 3 (Easy Arrays)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "GeeksforGeeks — Second largest element in an array",
                "url": "https://www.geeksforgeeks.org/find-second-largest-element-array/",
            },
        ],
        "understanding": r'''
Find the second-largest distinct value in the array. For
`[3, 8, 1, 9, 2, 4]` the answer is `8`. For `[5, 5, 5]` there is no
second-largest (only one distinct value); we typically return `-1`
or `None`.

The "no sorting" constraint is the whole point. Sorting would solve
the problem in *O(n log n)* trivially. The challenge is to do it in
**one pass**, *O(n)*, with a few constant slots of memory.
''',
        "brute_force": {
            "explanation": r'''
**Two passes**: first pass finds the largest. Second pass finds the
largest among elements not equal to the global largest. Correct and
*O(n)*, but requires two scans. We can do better with one.

```python
biggest = max(arr)
second = -1
for x in arr:
    if x != biggest and x > second:
        second = x
```
''',
            "code": r'''def second_largest_two_pass(arr: list[int]) -> int:
    # First pass: find the actual largest.
    biggest = arr[0]
    for x in arr:
        if x > biggest:
            biggest = x
    # Second pass: find the largest value strictly less than biggest.
    second = -1
    for x in arr:
        if x < biggest and x > second:
            second = x
    return second
''',
            "walkthrough": r'''
The two-pass approach is straightforward — find the biggest,
then find the biggest of "everything that's not the biggest."

**`def second_largest_two_pass(arr: list[int]) -> int:`** —
Takes the array, returns the second-largest value, or -1 if
none exists (e.g., all elements are equal).

**`biggest = arr[0]`** — Start the running max as `arr[0]`.

**`for x in arr: if x > biggest: biggest = x`** — Standard
max-of-array loop from the previous problem. By the end,
`biggest` holds the global maximum.

**`second = -1`** — Initialize `second` to -1 as a sentinel
meaning "no second largest found yet." If the array has only
one distinct value (like `[5, 5, 5]`), this will remain -1
and we'll return it.

**`for x in arr:`** — Second pass over the array.

**`if x < biggest and x > second:`** — Two conditions joined
by `and`. (a) `x < biggest`: strictly less than the global
max, so we exclude duplicates of the biggest. (b) `x > second`:
better than our current second-best candidate. If both hold,
this is a new second-best.

**`second = x`** — Update.

**`return second`** — Hand back the answer.

This is simple but requires two full passes through the array.
For huge arrays we'd prefer a single pass — and that's exactly
what the optimized version does (see below). The single-pass
version is trickier because it has to maintain *two* running
quantities simultaneously, with a careful update order: when
a new biggest arrives, the *old biggest* becomes the new
second-largest. Mess up the order and you lose information.
''',
            "complexity": (
                "**Time**: *O(n)* but two passes. **Space**: *O(1)*."
            ),
        },
        "thought_process": r'''
The single-pass version asks: can we maintain "largest" and "second
largest" *simultaneously* as we walk?

Yes. We hold two variables. When a new element arrives, three cases:

1. It is larger than `largest`. The current `largest` is dethroned
   — it now becomes the new `second`. The newcomer becomes
   `largest`.
2. It is between `largest` and `second`. It dethrones `second` only.
3. It is no bigger than `second`. We ignore it.

Read those three cases slowly. Many beginners forget case 1 — they
update `largest` without saving the old `largest` into `second`,
and the algorithm silently produces wrong answers. The trap is so
common it is worth practicing on paper once.

Edge cases to think about: duplicates of the largest value should
not count as a "second largest". If the array is all equal, there
is no second largest and we return `-1`. Our implementation handles
both correctly because we use strict `>` for the "dethrone largest"
case and exclude equality in the "dethrone second" case.
''',
        "optimized": {
            "explanation": r'''
A single pass maintaining both `largest` and `second`.
''',
            "code": r'''def second_largest(arr: list[int]) -> int:
    # Sentinels: a value lower than any expected input. -inf works
    # universally but for typical int arrays a large negative is fine.
    largest = float("-inf")
    second = float("-inf")
    for x in arr:
        if x > largest:
            # x is the new champion; demote the old champion.
            second = largest
            largest = x
        elif x < largest and x > second:
            # x slots between the two; replace second.
            second = x
    # If second never moved, the array had no second-largest value.
    if second == float("-inf"):
        return -1
    return int(second)
''',
            "walkthrough": r'''
Now the elegant single-pass version. The clever part is the
update order — get it wrong and you lose data.

**`largest = float("-inf")`** — Sentinel value meaning "no
candidate seen yet." Anything we encounter will be larger.
Using `-inf` (negative infinity) ensures the very first
comparison always wins. Some implementations use `arr[0]`
instead; either works.

**`second = float("-inf")`** — Same sentinel for the
second-largest tracker.

**`for x in arr:`** — Walk through every element.

**`if x > largest:`** — `x` beats the current champion. Three
things follow.

**`second = largest`** — **Here is the critical step.** Before
we crown `x` as the new largest, we **demote the old
largest** to second place. Why? Because if `x` is bigger than
the old largest, the old largest is automatically the
second-best thing we've seen. We must capture it before
overwriting.

If we swapped these two lines (`largest = x` first, then
`second = largest`), we'd assign `x` to `second` — wrong! The
*old* largest would have been overwritten and lost. This is
the kind of order-sensitive bug that beginners hit and
struggle to debug.

**`largest = x`** — Now safe to crown `x`.

**`elif x < largest and x > second:`** — `x` is not bigger
than `largest`, but it might be bigger than `second`. Two
conditions:
- `x < largest`: strict less-than, to exclude duplicates of
  the largest. If `arr = [5, 5, 3]`, we want `second = 3`,
  not `5`.
- `x > second`: better than our current second-place
  candidate.

**`second = x`** — `x` slots into second place.

**`if second == float("-inf"): return -1`** — If we never
updated `second` (array was all equal, or only one element),
return -1 to signal "no second-largest exists."

**`return int(second)`** — Otherwise return the answer. The
`int()` conversion is just to clean up the float representation
back to a regular integer.

The mental model: imagine an Olympic podium with gold and
silver positions. When a new athlete arrives with a faster
time than gold, gold moves to silver and the new one takes
gold. If the new athlete is between gold and silver, they
take silver. If slower than silver, ignore. Same algorithm.

This pattern generalizes to top-K with a min-heap of size K.
We'll meet it again in many later problems.
''',
            "complexity": (
                "**Time**: *O(n)* single pass. **Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
The deep idea: when you need the **top K** of something, you
maintain a structure of size K and update it as you scan. For
K = 2, two variables suffice. For larger K, you typically use a
**min-heap of size K**: when you see a new element, push it; if the
heap is larger than K, pop the smallest. That keeps the heap as the
"best K so far". This generalizes to "top K largest", "top K most
frequent", and other heap problems in Step 11.

The single-pass habit also matters operationally. In a streaming
setting (data arrives one item at a time and you cannot rewind), a
two-pass algorithm is impossible. The "carry top-K so far" pattern
is the only viable approach.
''',
        "confusion_notes": [
            {
                "question": "Why is the order of the two assignments inside the `>` branch so important?",
                "answer": r'''
Because if you swap their order, you lose the old champion
before you save it.

Look at the correct order:

```python
if x > largest:
    second = largest    # save the old champion FIRST
    largest = x         # then crown the new one
```

Now consider what would happen if we flipped them:

```python
if x > largest:
    largest = x         # crown the new one
    second = largest    # but now largest IS x, so second becomes x too!
```

The second version sets `second` equal to `x`, which is wrong —
we wanted `second` to be the *previous* `largest`, not the new
one. After a single iteration like this, both variables hold the
same value, and the algorithm is broken forever.

This is the same "save before you mutate" discipline as
`current = arr[i]` in insertion sort and `original = n` in
palindrome-number. Whenever an assignment will destroy
information you still need, save the old value first.

A defensive trick: write the swap as a tuple assignment, which
evaluates the right side first:

```python
second, largest = largest, x
```

The right side computes `(largest, x)` using the old values,
then assigns them to the left. Order-independent and impossible
to get backward. Pythonic and bug-resistant.
''',
            },
            {
                "question": "Why use `x > largest` AND `x < largest` for the two branches?",
                "answer": r'''
Because we want to handle the **strict** inequality cases
separately, and the case `x == largest` should be ignored
entirely.

If `x` is strictly greater than `largest`, it dethrones the
current champion (and the old champion becomes the second). If
`x` is strictly less than `largest` but greater than `second`,
it dethrones only the second. If `x` equals `largest`, we do
nothing — duplicates of the largest value should not bump
`second` up to match.

To see why the `x == largest` case must be excluded, consider
`arr = [5, 5, 3]`. The largest is 5; the second-largest
(distinct) is 3. If our code updated `second` on `x == largest`,
the second 5 would push `second` up to 5, giving the wrong
answer (5 instead of 3).

The two strict inequalities (`x > largest` and `x < largest`)
naturally skip the equality case. The `elif x < largest and x >
second` branch fires only when `x` slots strictly between the
two scalars.

If the problem definition allowed "second largest" to mean "the
second element in sorted order, possibly equal to the largest,"
we would use `<=` and the algorithm would handle it. Read the
problem statement carefully — "second largest" usually means
strictly less than the largest.
''',
            },
            {
                "question": "What if the array has all equal elements?",
                "answer": r'''
Then there is no second-largest, and we should return a sentinel
value (typically `-1` or `None`).

For `arr = [5, 5, 5, 5]`, the largest is 5 and the second
largest (distinct) does not exist. Our algorithm uses sentinels
initialized to `float('-inf')`:

```python
largest = float('-inf')
second = float('-inf')
```

If `second` is still `float('-inf')` at the end of the loop, no
candidate ever satisfied `x < largest`, which means every
element was equal to `largest`. We return `-1` to indicate "no
second-largest exists."

This idiom — "initialize a scalar to a sentinel value, check if
it changed at the end" — is a common way to detect "did we ever
find anything?" without an explicit boolean flag.

Other common sentinels: `-1` for indices (since 0 is a valid
index), `None` for objects, `float('inf')` and `float('-inf')`
for numbers. Pick a sentinel that cannot collide with a real
answer.
''',
            },
            {
                "question": "Why does this generalize to a heap for larger K?",
                "answer": r'''
For two scalars, two variables work fine. For three, four, or
five, you could keep three, four, or five variables — but the
code gets ugly fast. The branching for "where does this new
element slot in?" becomes a tangle of nested `if`s.

A **min-heap of size K** packages this logic neatly. The heap
always holds the K largest elements seen so far. When a new
element arrives, you check whether it beats the smallest one in
the heap (which sits at `heap[0]`, by the min-heap property). If
yes, replace; if no, ignore.

```python
import heapq
heap = []
for x in arr:
    if len(heap) < k:
        heapq.heappush(heap, x)
    elif x > heap[0]:
        heapq.heapreplace(heap, x)
```

After processing all elements, the heap contains the K largest
values. The smallest of them (at `heap[0]`) is the K-th largest.

This is *O(n log K)*, which is great when K is small.

The takeaway: two-variable "second largest" is just the K = 2
specialization of a general top-K pattern. As K grows, switch to
a heap. The mental model — "maintain the best-K-so-far structure
and update it on each new element" — is the same.
''',
            },
        ],
        "summary": r'''
**Pattern**: maintain top-K best-so-far as you scan.

**Lesson**: when promoting a new champion, demote the old champion
carefully. Missing the demote step is the classic bug.

**Recognize next time**: "top K largest/smallest/most frequent" of
a stream — two variables for K = 2, a heap for general K.
''',
    },
    {
        "id": "remove-duplicates-sorted",
        "title": "Remove Duplicates from a Sorted Array",
        "step_id": 3,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["arrays", "two-pointers", "in-place"],
        "what_this_teaches": (
            "The 'slow / fast' two-pointer pattern for in-place "
            "compaction: one pointer **writes**, the other **reads**, "
            "both move forward. The same skeleton handles 'remove "
            "element', 'move zeros to end', and many other 'filter "
            "in place' problems."
        ),
        "pattern": "Slow pointer writes uniques, fast pointer scans for new values.",
        "prerequisite_lessons": ["arrays", "two-pointers"],
        "prerequisite_problems": ["largest-element"],
        "next_problems": [
            "move-zeros-to-end",
            "left-rotate-by-one",
            "remove-outermost-parentheses",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 3 (Easy Arrays)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 26 — Remove Duplicates from Sorted Array",
                "url": "https://leetcode.com/problems/remove-duplicates-from-sorted-array/",
            },
        ],
        "understanding": r'''
We have a **sorted** array like `[1, 1, 2, 2, 3, 4, 4]` and we need
to remove duplicates **in place**. The output array should contain
each distinct value exactly once, kept in sorted order:
`[1, 2, 3, 4, _, _, _]`. We return the new length `k = 4`; the tail
of the array can hold anything (the problem usually does not care).

Two things to pay attention to:

1. **The input is sorted.** That single fact unlocks a slick
   *O(n)* in-place solution. Duplicates of any value must sit next
   to each other.
2. **In place.** No allocating a brand new array. We modify the
   given one and return the new length.
''',
        "brute_force": {
            "explanation": r'''
A simple non-in-place approach uses a set:

```python
return sorted(set(arr))
```

It is correct, but it loses the in-place property and is *O(n log n)*
or *O(n)* depending on details. For interview purposes the in-place
version is the canonical answer.
''',
            "code": r'''def remove_dups_set(arr: list[int]) -> int:
    # Build a sorted list of unique values, then write them back
    # into the front of arr in place.
    uniques = sorted(set(arr))
    for i, v in enumerate(uniques):
        arr[i] = v
    return len(uniques)
''',
            "walkthrough": r'''
The brute-ish approach uses a set to deduplicate and a sort to
re-order, then writes back into the input array.

**`def remove_dups_set(arr: list[int]) -> int:`** — Takes the
array (which we're allowed to modify), returns the count of
unique elements.

**`uniques = sorted(set(arr))`** — Two operations packed in
one line.

`set(arr)` walks through the array once and builds a set —
which by definition contains no duplicates. For
`arr = [1, 1, 2, 2, 3]`, `set(arr)` is `{1, 2, 3}`.

`sorted(...)` then takes that set and returns a new list with
its elements sorted ascending. For `{1, 2, 3}` (which is
already in sorted order conceptually but sets are unordered),
we get `[1, 2, 3]`.

This costs *O(n)* to build the set plus *O(k log k)* to sort
where `k` is the number of unique values. Both are bounded by
*O(n log n)* total.

**`for i, v in enumerate(uniques):`** — Walk the unique values
with their positions. `enumerate` gives us both the index
(`i`) and the value (`v`).

**`arr[i] = v`** — Overwrite the front of `arr` with the
unique values, in order. We're modifying the input array
in place, replacing its first `len(uniques)` slots with the
deduplicated sorted values.

**`return len(uniques)`** — Hand back the count.

This works, but it's wasteful for a problem where the input is
already sorted. The set throws away ordering information we
already had, and the sort puts it back. The optimized version
exploits the sortedness directly via the two-pointer
slow-and-fast pattern — *O(n)* with no extra memory.
''',
            "complexity": (
                "**Time**: *O(n log n)* due to sorting the set. "
                "**Space**: *O(n)* for the set."
            ),
        },
        "thought_process": r'''
Because the input is **sorted**, duplicates are guaranteed to be
adjacent. That means we can detect a duplicate by comparing each
element with its immediate predecessor. If they differ, we have a
new unique value.

This is the **slow-and-fast pointer** pattern. `slow` is the index
where the next unique value should be written; `fast` is the index
we are currently reading from. When the value at `fast` is new (i.e.
different from the value at `slow`), we advance `slow` and copy it
in. Otherwise we ignore `fast` and keep moving.

Read the pattern once more:

- `slow` points to the last unique value we kept.
- `fast` walks through everything.
- When `arr[fast] != arr[slow]`, we have a fresh unique value;
  promote `slow` by one and overwrite.

By the end, `slow + 1` is the count of unique values, and the front
of the array `arr[0..slow]` is the deduplicated content.

This pattern — slow pointer for "where to write", fast pointer for
"where to read" — is one of the most reused moves in array
problems. It shows up in "move zeroes to end", "remove element", and
"sort 0s/1s/2s".
''',
        "optimized": {
            "explanation": r'''
Two pointers walking the array once. *O(n)* time, *O(1)* extra
space.
''',
            "code": r'''def remove_duplicates(arr: list[int]) -> int:
    # An empty array trivially has zero unique elements.
    if not arr:
        return 0
    # slow points to the last index that holds a confirmed unique value.
    slow = 0
    # fast walks through the rest of the array.
    for fast in range(1, len(arr)):
        # If arr[fast] differs from the most-recent unique, it is a
        # new unique value.
        if arr[fast] != arr[slow]:
            slow += 1                 # reserve the next slot
            arr[slow] = arr[fast]     # write the new unique there
    # Number of unique elements = slow + 1 (because we are 0-indexed).
    return slow + 1
''',
            "walkthrough": r'''
The two-pointer slow-and-fast technique. This is one of the
most reusable patterns in array problems — memorize the shape.

**`def remove_duplicates(arr: list[int]) -> int:`** — Same
signature. We mutate the input array in place.

**`if not arr: return 0`** — Edge case. An empty array has
zero unique elements. The Python idiom `if not arr` is shorter
than `if len(arr) == 0` and means the same thing for lists
(empty lists are falsy).

**`slow = 0`** — `slow` is our "write head." It points to the
last position in the array where we've written a confirmed
unique value. Initially it points to index 0 — we trust that
the first element is unique (it has no predecessor to compare
against, so we keep it by default).

**`for fast in range(1, len(arr)):`** — `fast` is the "read
head." It walks through every position starting at index 1
(because index 0 is already trusted). Why start at 1 and not
0? Because the comparison `arr[fast] != arr[slow]` needs
something to compare against, and the slow pointer starts at 0.

**`if arr[fast] != arr[slow]:`** — The key test: is the value
at the read head different from the most-recently-kept value?
Because the array is sorted, equal values cluster together,
so the only way to find a new unique is to see a different
value than the last one we kept.

**`slow += 1`** — A new unique was found. Advance the write
head by one to reserve the next slot. After this line, the
write head points to a slot we're about to fill (it was
previously a duplicate of the value at `slow - 1`, or it was
the same as `arr[fast]` from a previous iteration).

**`arr[slow] = arr[fast]`** — Write the new unique value into
the reserved slot. This overwrites whatever was there
(possibly a duplicate, possibly nothing important).

**`return slow + 1`** — After the loop, `slow` is the index
of the last unique value. The *count* of unique values is one
more than the index (because indices start at 0). So we return
`slow + 1`.

The invariant the algorithm maintains: positions `[0, slow]`
contain the unique values seen so far, in sorted order.
Positions `[slow+1, fast]` are "garbage" — we've already
processed them but they might be duplicates or stale data.
Positions `[fast, end]` are yet to be examined.

The "write head + read head" pattern works whenever you want
to filter or compact an array in place. The read head never
falls behind the write head, so we never overwrite data we
still need.

Total work: one pass with `fast`, *O(n)*. No extra memory
beyond the two indices. The set-based approach used *O(n)*
memory and *O(n log n)* time; this version is strictly
better on both axes — when the input is sorted.
''',
            "complexity": (
                "**Time**: *O(n)*. **Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
The deep idea is **the slow pointer is a write head**. We use it to
compact the array in place by overwriting the duplicates. Because
the input is sorted, the front of the array stays valid the entire
time — we never overwrite something we still need to read, because
slow ≤ fast always.

The general pattern: any time the problem says "remove all X from
the array in place" or "compact the array", reach for slow/fast. The
question becomes: "what is the condition under which I keep an
element?". Here it is "different from the previous kept value".
Elsewhere it might be "nonzero" (move zeroes), "doesn't equal val"
(remove element), or "satisfies predicate".

A nice variation: **at most twice** instead of "at most once". We
keep a count of how many times the current value has been kept, and
allow up to two. The slow/fast structure is identical; only the
"keep?" condition changes.
''',
        "confusion_notes": [
            {
                "question": "Why does this only work on a *sorted* array?",
                "answer": r'''
Because the algorithm detects a duplicate by comparing the
current element with the **most recent unique element kept** —
not with every earlier element. That shortcut only works when
duplicates are guaranteed to be adjacent.

On a sorted array, all copies of any value sit next to each other.
So if `arr[fast] != arr[slow]`, we know `arr[fast]` is a brand
new value that has not appeared before. One comparison is enough.

On an *unsorted* array, the same comparison would let copies
through. For `arr = [1, 3, 1, 3]`, the slow pointer might be at
the second `1` while fast looks at the second `3`. They differ,
so the algorithm "keeps" the `3` — even though `3` already
appeared earlier. The result has duplicates.

The fix for unsorted input is to either sort first (`O(n log n)`)
or use a hash set to track all previously seen values (`O(n)`
time, `O(n)` extra memory). Either approach works; the slow/fast
trick is specifically the *O(n)* time / *O(1)* memory solution
**that requires sortedness**.

The general principle: the data structure's invariants (here,
sortedness) determine which shortcuts are legal. Always state the
invariant out loud before reaching for an algorithm.
''',
            },
            {
                "question": "Why does the function return `slow + 1`?",
                "answer": r'''
Because indices are zero-based, but counts are one-based.

The slow pointer marks the **index** of the last unique element
we kept. If slow ended at index 3, that means slots 0, 1, 2, and
3 hold the four unique elements. The *count* is 4, which is
`slow + 1`.

This is the same fence-post counting we covered in the Arrays
lesson. An array of length 4 has its last valid index at 3 — the
length is always one more than the last index.

The function returns the count (often called `k` in LeetCode
problems) because the problem asks "how many unique elements?".
The caller can then look at `arr[:k]` to read those unique
elements, ignoring the garbage that may remain beyond index `k`.

If the function instead returned `slow`, the caller would lose
the last unique element. Always double-check the off-by-one when
returning index-related counts.
''',
            },
            {
                "question": "Why advance `slow` *before* writing, not after?",
                "answer": r'''
Because `slow` already points to a finalized value (the last
unique we kept). The next *empty* slot is `slow + 1`. We have to
reserve that empty slot first, then write into it.

Walk through:

```python
if arr[fast] != arr[slow]:
    slow += 1                # reserve the next slot
    arr[slow] = arr[fast]    # fill it
```

If we wrote first and incremented after:

```python
arr[slow] = arr[fast]        # OVERWRITES the most recent kept value!
slow += 1
```

The second version overwrites `arr[slow]`, destroying the unique
value we just kept. Wrong.

The "advance first, then write" order is a small but crucial
piece of the algorithm. Whenever a pointer points at the *last
written* slot, the next write goes to position pointer + 1. Bump
first, write second.

In some variants you maintain a `write` pointer that points at
the *next empty* slot instead. Then the order flips: write, then
bump. Both styles work; pick one and be consistent.
''',
            },
            {
                "question": "Why is the time `O(n)` if there's a swap-like operation?",
                "answer": r'''
Because the inner work is **one comparison and at most one
assignment** per iteration, both of which are constant time.

The `fast` pointer walks every index from 1 to `n - 1`. That is
exactly `n - 1` iterations of the loop. At each iteration we do
a few constant-time operations: an `if` check, possibly an
increment, possibly an assignment. No nested loop, no shifting
of many elements. Total: `O(n)` work.

Note that the assignment `arr[slow] = arr[fast]` is **not** a
swap. We do not save `arr[slow]` first because the value at
`arr[slow]` is a duplicate that we are intentionally overwriting.
The slow pointer is always at or behind the fast pointer, so
`arr[slow]`'s old value has already been "kept" earlier and is
safe to overwrite.

Contrast with insertion sort, where shifting `k` elements
rightward inside the inner loop costs `O(k)`. That is why
insertion sort is `O(n²)` and this algorithm is `O(n)`. The
difference: insertion sort has to make room; here, we are just
overwriting trash.
''',
            },
        ],
        "summary": r'''
**Pattern**: slow/fast pointer for in-place compaction on a sorted
array.

**Lesson**: sortedness puts duplicates next to each other, so a
single comparison detects them. The slow pointer marks where to
write; the fast pointer marks where to read.

**Recognize next time**: any in-place array compaction. The general
pattern is `for fast: if keep(arr[fast]): slow += 1; arr[slow] = arr[fast]`.
''',
    },
    {
        "id": "max-consecutive-ones",
        "title": "Maximum Consecutive Ones",
        "step_id": 3,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["arrays", "linear-scan"],
        "what_this_teaches": (
            "The 'current streak vs all-time record' pattern. Two "
            "scalars, one pass — extend on a positive signal, reset on "
            "a negative one, always update the record. Reused in "
            "Kadane, stock buy/sell, longest run problems, and more."
        ),
        "pattern": "Walk once with `current` (live streak) and `best` (record).",
        "prerequisite_lessons": ["arrays"],
        "prerequisite_problems": ["largest-element"],
        "next_problems": [
            "kadane-algorithm",
            "max-consecutive-ones-iii",
            "longest-subarray-with-sum-k",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 3 (Easy Arrays)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 485 — Max Consecutive Ones",
                "url": "https://leetcode.com/problems/max-consecutive-ones/",
            },
        ],
        "understanding": r'''
Given a binary array (only 0s and 1s) like `[1, 1, 0, 1, 1, 1, 0, 1]`,
find the length of the longest run of consecutive 1s. The answer for
that example is `3` (the run `1, 1, 1` in the middle).

This is one of the cleanest examples of the running-scalar pattern,
with a small twist: we maintain *two* running scalars — the current
run length and the best run length seen so far.
''',
        "brute_force": {
            "explanation": r'''
For each starting index, scan forward as long as we see 1s and count
the run. Record the longest. This is *O(n²)* worst case (mostly 1s)
and we can do better with one pass.
''',
            "code": r'''def max_ones_brute(arr: list[int]) -> int:
    n = len(arr)
    best = 0
    # For each start, count the run of 1s.
    for i in range(n):
        run = 0
        j = i
        while j < n and arr[j] == 1:
            run += 1
            j += 1
        if run > best:
            best = run
    return best
''',
            "walkthrough": r'''
The brute force tries every possible starting position and
walks forward counting consecutive 1s. Simple, but does
redundant work.

**`def max_ones_brute(arr: list[int]) -> int:`** — Takes an
array of 0s and 1s, returns the length of the longest run of
consecutive 1s.

**`n = len(arr)`** — Cache the length for the loop bounds.

**`best = 0`** — Track the longest run found so far. Starts at
0 because an all-zeros array has no run of 1s.

**`for i in range(n):`** — Outer loop: try each index `i` as a
potential starting position for a run.

**`run = 0`** — Reset the run counter for this new starting
position. We're about to count how many consecutive 1s
**start** at index `i`.

**`j = i`** — `j` is the index we're currently examining,
starting from `i`. We use a separate variable so the outer
`i` can keep its position for the next iteration.

**`while j < n and arr[j] == 1:`** — Walk forward as long as
two things hold: we haven't run off the end of the array, and
the current value is 1. The instant we see a 0 (or run off
the end), the run ends.

The order matters here: `j < n` comes first because of Python's
short-circuit evaluation. If `j == n`, we should stop and not
evaluate `arr[j]` (which would be out of bounds). Python only
evaluates the second condition if the first is True. So this
order keeps us safe from index errors.

**`run += 1; j += 1`** — Found a 1; bump both counters.

**`if run > best: best = run`** — After the inner while ends,
check if this run beats our current best. If yes, update.

**`return best`** — Hand back the answer.

The cost: outer loop runs `n` times. Inner while can run up to
`n` times for each. Worst case (all 1s): the inner loop runs
roughly `n`, `n-1`, `n-2`, ..., 1 times for each outer
iteration — total *O(n²)*. Wasteful, because we're re-counting
sub-runs many times.

The optimized version does it in a single pass with constant
memory — see below.
''',
            "complexity": (
                "**Time**: *O(n²)* worst case. **Space**: *O(1)*."
            ),
        },
        "thought_process": r'''
The brute force wastes time by restarting the run count for each
starting index. But there is no need to restart. We can maintain
a single running count as we walk:

- When we see a 1, increment the current run.
- When we see a 0, reset the current run to 0.
- At every step, update the best with the current run.

That is it. One pass, two scalars.

The mental model is "current streak vs all-time record". The
algorithm is exactly how a sports broadcaster would narrate: the
current streak goes up while the team wins, resets on a loss, and
the record updates whenever the current streak exceeds it.
''',
        "optimized": {
            "explanation": r'''
Single pass with two scalars: current run and best run.
''',
            "code": r'''def max_consecutive_ones(arr: list[int]) -> int:
    best = 0          # longest run seen so far
    current = 0       # length of the run we are currently inside
    for x in arr:
        if x == 1:
            # Extend the current run by one.
            current += 1
            # Update the all-time record if we just broke it.
            if current > best:
                best = current
        else:
            # The run ends here; reset the counter.
            current = 0
    return best
''',
            "walkthrough": r'''
The single-pass version. Two scalars, one walk. This is the
"current streak vs all-time record" pattern that appears in
many problems.

**`def max_consecutive_ones(arr: list[int]) -> int:`** — Same
signature.

**`best = 0`** — The longest run we've seen *anywhere* in the
array so far. Our final answer.

**`current = 0`** — The length of the run we're currently
inside. Resets every time we see a 0.

**`for x in arr:`** — Walk through every element. We don't
even need the index — we just need the value at each position.
This is the cleanest form of an array walk in Python.

**`if x == 1:`** — Hit a 1. We're inside (or starting) a run
of 1s.

**`current += 1`** — Extend the current run by one. If we just
came from a stretch of 0s, `current` was 0 before this and is
now 1 — the start of a new run.

**`if current > best: best = current`** — Update the all-time
record if our current run has surpassed it. This check is
done **every time** we extend a run, not just at the end of
the run. Why? Because the current run might be ongoing when
the array ends; we'd miss the answer if we only checked at
the next 0.

You could also write `best = max(best, current)`, which is
more Pythonic. The `if` version avoids the `max` function
call, marginally faster in a tight loop.

**`else: current = 0`** — Hit a 0. The current run ends. Reset
`current` to start fresh next time we see a 1.

**`return best`** — Hand back the all-time longest run.

The mental model: imagine watching a streak of dominoes
falling. As long as 1s keep arriving, the streak grows; the
moment a 0 arrives, the streak resets. Throughout the whole
process, we're keeping a running record of "longest streak
ever seen."

Total work: one pass, *O(n)*. Two scalars, *O(1)* extra
memory. This is the asymptotic floor for this problem —
there's no way to do less work because we must at least look
at every element once.

The "carry current streak, update record" pattern generalizes
to: longest run of any condition, longest non-decreasing
subarray, longest substring without repeating characters
(with a twist), max stock profit with one buy-sell, and many
others.
''',
            "complexity": (
                "**Time**: *O(n)*. **Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
The "current streak vs record" pattern is one of the cheapest and
most reused tricks in array work. A surprising number of problems
are this same shape with a slightly different reset condition:

- **Max consecutive ones** — reset on 0.
- **Longest substring with at most K zeroes** — reset is more
  subtle and uses sliding window.
- **Maximum subarray sum** (Kadane) — reset is "if current sum
  drops below zero, reset to 0".
- **Longest increasing run** — reset is "if `arr[i] <= arr[i-1]`,
  reset to 1".

You will see the same `current` / `best` pair across many array
problems. Get to know the rhythm: extend on a positive signal,
reset on a negative signal, always update the best.
''',
        "confusion_notes": [
            {
                "question": "Why reset to `0` and not to `1` after a zero appears?",
                "answer": r'''
Because the zero itself is **not** part of any run of ones. When
we see a zero, the current streak of ones ends; the next "ones
streak" has not yet started.

Walk through `arr = [1, 1, 0, 1, 1, 1]`. At index 2 (the zero),
the streak that was building (`1, 1`, length 2) is broken. The
next element is at index 3. If we reset `current = 1` at the
zero, we would be claiming that the *zero itself* contributed to
a streak of length 1 — which is nonsense.

The correct flow: hit zero → `current = 0`. Then on the next 1
(at index 3), `current` increments to 1, marking the start of a
new streak. From there it keeps extending.

You will see the same "reset to neutral on bad signal, extend on
good signal" pattern in Kadane (reset to 0 when running sum
drops below 0, extend when it stays positive), in longest
increasing run (reset to 1 when monotonicity breaks), and in
many sliding window problems.

The rule of thumb: **what does the current variable count *when
the new element is bad*?** For "consecutive 1s," the answer is
"the bad element itself contributes nothing, so the count is
zero." So we reset to 0.
''',
            },
            {
                "question": "Why update `best` inside the `if x == 1` branch instead of at the end of the loop?",
                "answer": r'''
You can do either; both produce the right answer. But updating
inside the branch is more efficient because we only need to
check when `current` could have grown — and that is only when we
just saw a 1.

Compare the two styles:

Style A (update on every iteration):

```python
for x in arr:
    if x == 1:
        current += 1
    else:
        current = 0
    if current > best:
        best = current
```

Style B (update only on extends):

```python
for x in arr:
    if x == 1:
        current += 1
        if current > best:
            best = current
    else:
        current = 0
```

Style B avoids one comparison per zero. Tiny saving, but it also
makes the code's *intent* clearer: "the best can only change
when the streak grows."

Either style is fine. For interview practice, prefer Style B
because it shows you are thinking about *when* the answer
changes — a small marker of algorithmic maturity.
''',
            },
            {
                "question": "What if the array has no `1`s at all? Or no `0`s?",
                "answer": r'''
**No 1s** (e.g., `[0, 0, 0]`): `current` never increases past 0,
and `best` stays at its initial value of 0. The function
correctly returns 0 — there are no consecutive ones at all.

**No 0s** (e.g., `[1, 1, 1, 1]`): `current` increments to 4 over
four iterations, and `best` tracks it, ending at 4. The function
returns 4 — the entire array is one streak.

Both edge cases work naturally thanks to the initialization
`current = 0, best = 0`. The algorithm does not need special
cases; the math is symmetric.

This is the mark of a well-designed algorithm: it handles the
extremes (all-good, all-bad) without extra code. When you write
your own running-scalar algorithms, run through these mental
test cases:
- Empty array
- All elements satisfy the condition
- No elements satisfy the condition
- Exactly one element satisfies the condition

If any of those breaks, your initialization or reset condition
is wrong.
''',
            },
            {
                "question": "How does this generalize to 'at most K zeros allowed'?",
                "answer": r'''
The generalization is the **sliding window** technique, and it
unlocks a family of problems (Max Consecutive Ones III, Longest
Substring with K Replacements, etc.).

The idea: maintain a window `[left, right]` and a count of zeros
inside it. Expand `right` greedily. When the zero count exceeds
K, shrink `left` until it falls back to K. The maximum window
length is the answer.

```python
def longest_ones(arr, k):
    left = 0
    zeros = 0
    best = 0
    for right in range(len(arr)):
        if arr[right] == 0:
            zeros += 1
        while zeros > k:
            if arr[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
```

For `k = 0` (no zeros allowed), this reduces to the original
problem. For `k > 0`, we tolerate up to `k` "bad" elements inside
the window.

The same skeleton handles "longest substring with at most K
distinct characters," "longest substring with K replacements,"
"fruit into baskets," and many more. Recognizing that the
running-scalar pattern generalizes to a sliding-window pattern
is one of the bigger leaps in array DSA.

We cover sliding window in detail in its own lesson and in Step
10 of the curriculum.
''',
            },
        ],
        "summary": r'''
**Pattern**: current streak + all-time record.

**Lesson**: don't restart counts when you can extend them. Two
scalars, one pass, *O(n)*.

**Recognize next time**: any "longest run / streak / consecutive"
problem. The reset condition is the only thing that changes.
''',
    },
    {
        "id": "single-number",
        "title": "Find the Number That Appears Once (Others Twice)",
        "step_id": 3,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["arrays", "xor", "bit-manipulation"],
        "what_this_teaches": (
            "XOR as a cancellation tool. The three magic properties — "
            "`x ^ x == 0`, `x ^ 0 == x`, commutativity — make XOR the "
            "right tool for any 'pairs cancel, surplus survives' "
            "problem."
        ),
        "pattern": "Fold the entire array with XOR; pairs cancel, the loner remains.",
        "prerequisite_lessons": ["arrays", "hashing"],
        "prerequisite_problems": ["count-frequencies"],
        "next_problems": [
            "single-number-ii",
            "single-number-iii",
            "missing-number",
            "min-bit-flips",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 3 (Easy Arrays)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 136 — Single Number",
                "url": "https://leetcode.com/problems/single-number/",
            },
        ],
        "understanding": r'''
We have an array where every integer appears **exactly twice**,
except one integer that appears exactly **once**. Find the loner.

Example: `[2, 3, 5, 4, 5, 3, 4]` — the loner is `2`.

The hashing solution is obvious. The optimized solution is one of
the prettiest tricks in all of beginner DSA: **XOR everything
together, and the answer drops out**.
''',
        "brute_force": {
            "explanation": r'''
Count frequencies with a hash map; return the value whose count is
1. *O(n)* time, *O(n)* space.

```python
from collections import Counter
[k for k, v in Counter(arr).items() if v == 1][0]
```

Correct and simple. The XOR solution improves the **space** to
*O(1)*, which is the real prize.
''',
            "code": r'''def single_number_hash(arr: list[int]) -> int:
    from collections import Counter
    counts = Counter(arr)
    for k, v in counts.items():
        if v == 1:
            return k
    raise ValueError("no unique element found")
''',
            "walkthrough": r'''
The hash-table approach. Straightforward and works for any
problem with "find element with frequency 1."

**`def single_number_hash(arr: list[int]) -> int:`** — Takes
the array, returns the unique element.

**`from collections import Counter`** — Import Counter, a dict
subclass specialized for counting. It turns any iterable into
a `value -> count` mapping in one line.

**`counts = Counter(arr)`** — Build the count map. For
`arr = [4, 1, 2, 1, 2]`, this produces `{4: 1, 1: 2, 2: 2}`.
Counter walks the array once internally — *O(n)* time, *O(n)*
extra memory.

**`for k, v in counts.items():`** — Loop through each
`(value, count)` pair. The `.items()` method gives us both
the key (the value from the array) and the value (its count).

**`if v == 1: return k`** — Found the lone element — its count
is 1. Return its value.

**`raise ValueError("no unique element found")`** — Defensive
code. The problem guarantees a unique element exists, but if
the caller passed bad input, we raise a clear error instead
of silently returning None.

This approach is *O(n)* time but uses *O(n)* memory for the
counter. The optimized version below uses *O(1)* memory via
the XOR trick — a beautiful application of bitwise arithmetic.
''',
            "complexity": (
                "**Time**: *O(n)*. **Space**: *O(n)* for the counter."
            ),
        },
        "thought_process": r'''
The leap to the XOR solution requires knowing **three properties of
XOR**:

1. **XOR is commutative and associative.** `a ^ b == b ^ a` and
   `(a ^ b) ^ c == a ^ (b ^ c)`. So the order in which you XOR a
   list of numbers does not matter.
2. **`x ^ x == 0`.** XOR-ing a number with itself produces zero.
3. **`x ^ 0 == x`.** XOR-ing a number with zero leaves it unchanged.

Now imagine XOR-ing every element of the array together. Because
order does not matter, we can mentally pair up the duplicates.
Every pair contributes `x ^ x == 0` to the final result. The loner
has no partner, so it contributes itself. The final XOR is
`0 ^ 0 ^ ... ^ loner == loner`.

That is the entire algorithm. One pass, one variable.

When does this work? Whenever the "duplicates" are exact pairs.
There are gorgeous variations:

- **Every value appears three times except one** — needs a
  different trick (counting bits modulo 3).
- **Two unique values, others appear twice** — XOR everything, then
  split by a bit position where the two unique values differ.

Step 8 covers these. For now, the basic XOR trick is the headliner.
''',
        "optimized": {
            "explanation": r'''
XOR all elements together. The duplicates cancel out; only the
loner survives.
''',
            "code": r'''def single_number(arr: list[int]) -> int:
    # Start with 0 because x ^ 0 == x.
    result = 0
    # XOR every element. Duplicates cancel to zero in pairs; the loner
    # has no partner and stays.
    for x in arr:
        result ^= x
    return result
''',
            "walkthrough": r'''
The XOR trick. Three short lines, but one of the most elegant
algorithms in all of competitive programming. Let me explain
the magic.

**`def single_number(arr: list[int]) -> int:`** — Takes the
array, returns the unique element.

**`result = 0`** — Start the running XOR with 0. We use 0
because of the identity `x ^ 0 == x` (XOR-ing anything with
zero gives that thing unchanged). So starting at 0 means our
first iteration effectively initializes `result` to the first
element.

**`for x in arr:`** — Walk every element.

**`result ^= x`** — XOR `x` into `result`. The `^=` is
shorthand for `result = result ^ x`.

**`return result`** — Hand back the answer.

The reason this works is one of the most beautiful facts in
discrete math. XOR has three crucial properties:

1. **Commutative and associative:** `a ^ b ^ c == c ^ a ^ b`.
   The order doesn't matter. This means we can imagine
   rearranging the array into pairs before XOR-ing.

2. **Self-cancellation:** `x ^ x = 0`. Any number XOR-ed with
   itself is zero. So `5 ^ 5 = 0`, regardless of what `5` is.

3. **Identity with zero:** `x ^ 0 = x`. XOR-ing with zero
   leaves a value unchanged.

Now imagine `arr = [4, 1, 2, 1, 2]`. Rearrange (allowed by
property 1): `[1, 1, 2, 2, 4]`. XOR them in this order:
`1 ^ 1 = 0`, then `0 ^ 2 = 2`, then `2 ^ 2 = 0`, then
`0 ^ 4 = 4`. The pairs cancel themselves, the unique element
survives. Property 2 + property 3 handle the rest.

The implementation walks the array in its given order, not in
the rearranged order. But because of commutativity, it doesn't
matter — the algebraic result is the same.

This is *O(n)* time, *O(1)* extra memory. No hash table, no
sorting. Just one running integer and one bitwise operation
per element. Beautiful.

This XOR trick generalizes: "find the *one* number that
appears odd times when all others appear even times" — same
algorithm. The hash version handles arbitrary frequency
patterns; the XOR version handles only the "all-but-one
appear an even number of times" specialization, but in
constant memory.
''',
            "complexity": (
                "**Time**: *O(n)*. **Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
XOR is *bit-by-bit* "are these two bits different?". The
self-cancellation property comes from the fact that any bit XORed
with itself is 0. So XOR-ing a list of values is, at each bit
position, asking "did this bit appear an odd number of times?". For
pairs the answer is always "even, so 0". For the loner the answer is
whatever its own bit is.

This is the foundation for several beautiful algorithms:

- **Detecting differences** between two arrays. XOR them together;
  the result is the XOR of the differing elements.
- **Finding the missing number 1..n**. XOR `1..n` and the array
  together; everything cancels except the missing number.
- **Encoding pair sums** in O(1) — useful in tricky bit-trick problems.

XOR feels like magic the first time you see it, then like a tool the
tenth time you see it. Get comfortable.
''',
        "confusion_notes": [
            {
                "question": "Why does `x ^ x` equal zero? And `x ^ 0` equal `x`?",
                "answer": r'''
Look at XOR bit by bit. For each bit position, XOR asks the
question *"are the two bits different?"*. If they are different,
the result bit is 1; if they are the same, the result bit is 0.

When you XOR `x` with itself, every bit position has identical
bits (each bit of `x` matches itself). So every result bit is
0. Therefore `x ^ x == 0`.

When you XOR `x` with `0`, every bit position pairs a bit of `x`
with `0`. The "different?" question reduces to "is this bit 1?".
Where `x` has a 1, the result has a 1. Where `x` has a 0, the
result has a 0. So the result is just `x`. Therefore `x ^ 0 == x`.

These two facts together — self-cancellation and identity — are
why XOR is the algebraic structure of *symmetric difference*.
Think of XOR-ing a value into a running total as "toggling" that
value's contribution: the first toggle adds, the second cancels,
the third adds again, and so on.

For pairs of duplicates, two toggles cancel out, leaving the
running total untouched. For the loner, one toggle remains. So
the final XOR is the loner's value.

This is the same reason XOR is used in cryptography (the Vernam
cipher), error-detecting checksums, and reversible operations:
applying XOR twice with the same key undoes itself.
''',
            },
            {
                "question": "Why is the order of the XORs not important?",
                "answer": r'''
Because XOR is **commutative** (`a ^ b == b ^ a`) and
**associative** (`(a ^ b) ^ c == a ^ (b ^ c)`).

Both properties follow from the bit-by-bit definition. At each
bit position, XOR is the "is the count of 1s odd?" function.
This function does not care which order you fed it the inputs;
it only cares about the parity of the count.

The practical upshot: you can XOR an array's elements in any
order and get the same result. The traditional left-to-right
fold is what we use, but middle-out or right-to-left would
produce the same final value.

This is what lets us think of XOR as a "set operation" on
multisets. The XOR of a list is determined entirely by which
values appear an odd number of times — not by their positions.

The same property is what makes hashing-with-XOR work for
multiset equality: two arrays have the same XOR iff their
symmetric difference is the empty multiset.
''',
            },
            {
                "question": "What if elements appear three times instead of twice (except one)?",
                "answer": r'''
The XOR trick **does not work directly** because three XORs of
the same value yield the value itself (not zero):

```
x ^ x ^ x = (x ^ x) ^ x = 0 ^ x = x
```

So XOR-ing the whole array would give you "the lone element XOR
all the triplets," and the triplets would not cancel.

The fix is a different cancellation arithmetic. Instead of XOR
(which cancels pairs), use **bit-by-bit modulo-3 counting**. For
each bit position, count how many elements have that bit set. If
the count is a multiple of 3, the triplets contributed; the
remainder (0, 1, or 2 mod 3) tells you what the lone element's
bit must be.

```python
def single_number_3(arr):
    result = 0
    for bit in range(32):
        count = sum((x >> bit) & 1 for x in arr)
        if count % 3 != 0:
            result |= (1 << bit)
    return result
```

There is also a clever *O(1)* extra space variant using two
running variables to maintain "seen once" and "seen twice"
states. That is what Step 8's Single Number II problem covers.

The takeaway: cancellation arithmetic is **base-dependent**. XOR
is the right tool for "even count cancels," not for "count
divisible by 3." Match the operator to the duplicity pattern.
''',
            },
            {
                "question": "Could I just use a hash set and `add/remove`?",
                "answer": r'''
Yes, and it is a common simpler-to-explain alternative. Walk the
array; for each element, if it is already in the set, remove
it; otherwise, add it. At the end, the set contains exactly the
loner.

```python
def single_number_set(arr):
    seen = set()
    for x in arr:
        if x in seen:
            seen.remove(x)
        else:
            seen.add(x)
    return next(iter(seen))
```

This is *O(n)* time but uses *O(n)* extra memory. The XOR
version uses *O(1)* memory.

For interview answers, mention the set version first (easier to
explain) and then the XOR version (better memory). The
interviewer usually wants you to know **both** — the set version
to show you can think clearly, the XOR version to show you know
the bit trick.

A third alternative uses the formula `2 * sum(unique) - sum(arr)
= loner`, where `unique` is the deduplicated array. *O(n)* time
and memory but no XOR knowledge required. Less elegant; rarely
used.
''',
            },
        ],
        "summary": r'''
**Pattern**: XOR as "cancel out the pairs".

**Lesson**: when duplicates appear in pairs and you want O(1)
space, XOR is the answer. The three core properties are
commutativity, `x ^ x == 0`, and `x ^ 0 == x`.

**Recognize next time**: "every element appears N times except one"
problems. Pairs → XOR. Triples → bit-counting mod 3. Two singles
in pairs → XOR + split by bit.
''',
    },
    {
        "id": "missing-number",
        "title": "Find the Missing Number",
        "step_id": 3,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["arrays", "math", "xor"],
        "what_this_teaches": (
            "**O(1)-memory invariants** — sum, XOR, or product — that "
            "encode the expected state of a set and let you recover "
            "the missing element by subtraction. A small but powerful "
            "trick that shows up in many 'find the odd one out' "
            "problems."
        ),
        "pattern": "Encode the expected total; subtract the actual; recover the difference.",
        "prerequisite_lessons": ["arrays", "hashing"],
        "prerequisite_problems": ["single-number"],
        "next_problems": [
            "single-number-iii",
            "repeating-and-missing",
            "first-missing-positive",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 3 (Easy Arrays)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 268 — Missing Number",
                "url": "https://leetcode.com/problems/missing-number/",
            },
        ],
        "understanding": r'''
We are given an array of size `n` that contains `n` distinct numbers
from the range `[0, n]`. Exactly one number from that range is
missing. Find it.

Example: for `n = 4` and array `[3, 0, 1]`, the missing number is
`2` (because we expected `0, 1, 2, 3` but only saw `0, 1, 3`).

Three solutions of increasing cleverness solve this:

1. **Hashing** — store the seen set, then walk `0..n` looking for
   the absentee.
2. **Sum formula** — the sum of `0..n` is `n(n+1)/2`. Subtract the
   sum of the array. The difference is the missing number.
3. **XOR** — XOR `0..n` together, then XOR every element of the
   array; everything cancels except the missing one.

All three are *O(n)*. The sum and XOR approaches are *O(1)* space.
''',
        "brute_force": {
            "explanation": r'''
Hash-set approach: put every element in a set, then scan 0..n.

```python
seen = set(arr)
for i in range(n + 1):
    if i not in seen:
        return i
```

Correct and intuitive but uses *O(n)* extra memory.
''',
            "code": r'''def missing_set(arr: list[int]) -> int:
    seen = set(arr)
    n = len(arr)
    # The expected values are 0..n (inclusive), and exactly one is missing.
    for i in range(n + 1):
        if i not in seen:
            return i
    # Should not get here if the problem's promise holds.
    raise ValueError("no missing number found")
''',
            "complexity": (
                "**Time**: *O(n)*. **Space**: *O(n)*."
            ),
        },
        "thought_process": r'''
The sum trick comes from a tiny piece of math: the sum
`0 + 1 + 2 + ... + n` equals `n(n + 1) / 2`. That formula was first
written down (according to legend) by a very young Carl Gauss. We
do not need to know its history; we just need to know it.

So **expected_sum** = `n(n + 1) / 2`, where `n` is the largest
possible value. **actual_sum** = `sum(arr)`. The missing number is
`expected_sum - actual_sum`. One line of arithmetic.

There is one trap to avoid: **integer overflow**. In Python this is
a non-issue, but in C++/Java with 32-bit ints, `n(n + 1) / 2` can
overflow for large `n`. The XOR version sidesteps that completely
because XOR does not grow the bit width.

The XOR version uses the same idea as "single number": pair the
array's values with the indices 0..n. Each pair (value, same value
in the index range) cancels. The missing index has no partner and
survives.
''',
        "optimized": {
            "explanation": r'''
Both the sum and XOR approaches work in *O(n)* time and *O(1)*
space. The sum approach is the most beginner-friendly. The XOR
approach is overflow-proof.
''',
            "code": r'''def missing_number_sum(arr: list[int]) -> int:
    n = len(arr)
    # Gauss formula: expected sum of 0..n inclusive.
    expected = n * (n + 1) // 2
    # Subtract what we actually saw; the difference is what's missing.
    return expected - sum(arr)


def missing_number_xor(arr: list[int]) -> int:
    n = len(arr)
    result = 0
    # XOR all integers 0..n (the expected set).
    for i in range(n + 1):
        result ^= i
    # XOR all elements of arr (the actually-present set).
    for x in arr:
        result ^= x
    # Everything present in both cancels; what remains is the missing one.
    return result
''',
            "walkthrough": r'''
Two beautiful constant-memory algorithms for the same problem.
Both run in *O(n)* with *O(1)* memory. The choice between
them depends on whether you're worried about integer overflow.

**Version 1: The Gauss sum trick**

**`def missing_number_sum(arr: list[int]) -> int:`** — Takes
an array containing all integers from 0 to n except one, and
returns the missing one. The array length is `n`.

**`n = len(arr)`** — The array has length `n`. The complete
set `0, 1, ..., n` has `n + 1` elements; the array is missing
one of them.

**`expected = n * (n + 1) // 2`** — Gauss's formula for the
sum of integers from 0 to n inclusive. The math: pair the
numbers `(0, n), (1, n-1), (2, n-2), ...` — each pair sums to
`n`. There are `(n + 1) / 2` such pairs, giving total sum
`n × (n + 1) / 2`. We use integer division `//` to keep the
result as an integer (one of `n` and `n+1` is always even, so
the division is always exact).

This formula computes the expected sum in **constant time** —
no loop required.

**`return expected - sum(arr)`** — The actual sum of the
array is missing exactly one value. The difference between
expected and actual is that missing value. Return it.

`sum(arr)` walks the array once, *O(n)*. So this whole
function is *O(n)* time, *O(1)* extra memory.

**Version 2: The XOR trick**

Same idea but using XOR instead of addition. The reason: in
languages with 32-bit integers, the sum could overflow. XOR
can never overflow because each bit operates independently.

**`def missing_number_xor(arr: list[int]) -> int:`** — Same
signature.

**`n = len(arr)`** — Same setup.

**`result = 0`** — Start the running XOR at 0. Recall `x ^ 0 = x`,
so 0 is the identity for XOR.

**`for i in range(n + 1):`** — Loop from 0 to n inclusive.

**`result ^= i`** — XOR each value of the complete set into
the running total.

**`for x in arr:`** — Now XOR every element of the actual array.

**`result ^= x`** — XOR each one in.

After both loops, every value that appears in **both** the
complete set and the array has been XORed twice, so it
cancels itself out (`x ^ x = 0`). The only value that has
been XORed an odd number of times is the one in the complete
set but missing from the array — exactly what we want.

**`return result`** — Hand back the missing value.

This is *O(n)* time, *O(1)* memory, and is safe from integer
overflow. The sum version is one line shorter but can overflow
on 32-bit integers; the XOR version is two passes and never
overflows. Pick based on your constraints.

The XOR trick is one of the most elegant uses of bitwise math
in DSA. Once you internalize "XOR cancels pairs," dozens of
problems become approachable in *O(1)* memory.
''',
            "complexity": (
                "**Time**: *O(n)*. **Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
Both clever solutions use the same principle: **encode the expected
state in O(1), then "remove" the actual state, and what is left is
the difference**. The sum approach uses arithmetic (subtract). The
XOR approach uses XOR (which is its own inverse). Both are clean
ways to compute "set difference" without storing the set.

This trick generalizes powerfully. Need to find **two** missing
numbers from a range? XOR everything; the result is the XOR of the
two missing numbers. Then split by a differing bit to recover them
individually. That is one of the hidden gems of Step 8.

Need to find a **repeating** number in a 1..n array where exactly
one repeats? Use a Floyd cycle on the array-as-pointer interpretation,
or use sum/XOR with adjustments. There is a whole family.
''',
        "confusion_notes": [
            {
                "question": "Why does `n * (n + 1) // 2` give the sum of `0..n`?",
                "answer": r'''
This is Gauss's famous formula, often called the **triangular
number** formula. The intuition: pair up the numbers from the
two ends.

Write out the sum `0 + 1 + 2 + ... + n`. Now pair the first
with the last: `0 + n = n`. Pair the second with the
second-to-last: `1 + (n - 1) = n`. Pair the third with the
third-to-last: `2 + (n - 2) = n`. Every pair sums to exactly
`n`.

How many pairs? Half of `(n + 1)` numbers, which is `(n + 1) /
2` pairs. Each pair sums to `n`. So the total sum is
`n * (n + 1) / 2`.

This pairing trick is attributed (probably apocryphally) to a
young Gauss, who supposedly solved a "sum 1 to 100" busywork
problem in seconds by writing `100 * 101 / 2 = 5050`.

We use integer division `//` because the product `n * (n + 1)`
is always even (one of two consecutive integers must be), so the
division gives an exact integer result.

Memorize this formula. It comes up in many problems: counting
pairs, sum of subarrays of fixed length, arithmetic progression
sums. It is one of the most reused identities in DSA.
''',
            },
            {
                "question": "Why prefer XOR over the sum approach?",
                "answer": r'''
Two reasons: **overflow safety** and **conceptual elegance**.

In Python, neither version overflows because integers are
arbitrary precision. But in C++, Java, or any language with
fixed-width integers, the sum `n * (n + 1) / 2` can overflow
when `n` is large. For `n = 10⁵`, the product is about `5 × 10⁹`,
which already exceeds a 32-bit signed integer. The XOR version
never overflows because XOR does not increase the bit width.

Conceptually, the XOR version is also more **uniform**. The sum
trick relies on a specific arithmetic identity (Gauss's
formula). The XOR trick relies only on the cancellation property
(`x ^ x = 0`) and works for **any** set, not just `0..n`. If
the problem changed to "find the missing element from a known
set," the XOR approach generalizes immediately; the sum
approach does not (unless you also precompute the expected sum).

For Python interviews, either is fine. For typed languages,
prefer XOR. The general lesson: prefer **range-safe**
operations when porting between languages.
''',
            },
            {
                "question": "What if the array is missing more than one number?",
                "answer": r'''
Then a single sum or XOR is not enough — you cannot recover two
unknowns from one equation.

For **two missing numbers**, you need two equations. The classic
trick: use both `sum` and `sum_of_squares`. The two equations
let you solve for the two unknowns (it is a 2-variable system).

Alternatively, the XOR approach generalizes: XOR everything;
the result is `missing_a ^ missing_b`. To recover `a` and `b`
individually, find any bit where the XOR result is 1 (that bit
must differ between `a` and `b`). Partition all numbers (input
and expected) by that bit. XOR each partition separately;
each partition contains exactly one of the two missing
numbers.

This split-by-bit trick is Step 8 territory (Single Number III).
It is a beautiful application of XOR.

For **K missing numbers**, the techniques get more sophisticated
(typically, hashing or sorting). The "encode the total, subtract"
trick works only for very small K.

Bottom line: the sum/XOR trick has a constant equation count, so
it can recover only a constant number of missing values. For
larger K, switch to hashing or sorting.
''',
            },
            {
                "question": "Why is the range `0..n` and not `1..n`?",
                "answer": r'''
Different versions of the problem use different conventions. The
LeetCode version uses `0..n` (the array of length `n` contains
numbers from 0 to n with exactly one missing). Other versions
say `1..n` (array of length `n - 1` containing values from 1 to
n with one missing).

For LeetCode's `0..n` version: array has `n` elements, expected
sum is `0 + 1 + ... + n = n(n+1)/2`.

For the `1..n` version: array has `n - 1` elements, expected
sum is `1 + 2 + ... + n = n(n+1)/2` (the formula happens to be
the same since `0` does not contribute).

The algorithm is essentially identical; only the array length
and the loop bounds change. Always read the problem statement
carefully to determine which convention is in use.

This is a small but real source of off-by-one bugs. When you sit
down with a "missing number" problem, pause and ask: *"What is
the expected range? What is the array length? Does the range
include 0?"*. Two minutes of thinking saves twenty minutes of
debugging.
''',
            },
        ],
        "summary": r'''
**Pattern**: encode the expected total (sum or XOR), subtract the
actual, recover the difference.

**Lesson**: O(1) memory + arithmetic invariants can replace a hash
set in many "find the missing / extra / odd-one-out" problems.

**Recognize next time**: any "exactly one is different from the
expected set" question. Sum, XOR, or product invariants are usually
the path.
''',
    },
    {
        "id": "longest-subarray-with-sum-k",
        "title": "Longest Subarray with Sum K",
        "step_id": 3,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["arrays", "prefix-sum", "hashing", "sliding-window"],
        "what_this_teaches": (
            "**Prefix sums + hash map** — the workhorse pattern for "
            "subarray-sum questions. Once you see how range sums "
            "factor into point differences of prefix sums, an enormous "
            "family of problems unlocks."
        ),
        "pattern": "Running prefix sum, hashed by value, queried for `prefix - K`.",
        "prerequisite_lessons": ["arrays", "hashing"],
        "prerequisite_problems": ["two-sum", "count-frequencies"],
        "next_problems": [
            "subarrays-with-sum-k",
            "longest-subarray-zero-sum",
            "subarrays-with-xor-k",
            "binary-subarrays-with-sum",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 3 (Easy Arrays)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 325 — Maximum Size Subarray Sum Equals k",
                "url": "https://leetcode.com/problems/maximum-size-subarray-sum-equals-k/",
            },
        ],
        "understanding": r'''
Find the length of the **longest contiguous subarray** whose sum
equals a target `K`. The array may contain positives, negatives, and
zeros.

Example: `[1, -1, 5, -2, 3]`, `K = 3` → the longest subarray summing
to 3 is `[1, -1, 5, -2]`, of length 4.

A "subarray" must be contiguous — no skipping. That contiguity is
the whole game. It rules out greedy "skip the bad ones" tricks and
points us at two beautiful patterns: **sliding window** (for
non-negative arrays) and **prefix sums with hashing** (the general
case).

We will discuss both.
''',
        "brute_force": {
            "explanation": r'''
Try every subarray, sum it, track the longest matching length. Two
nested loops: outer for the start, inner for the end.

A small optimization: keep a running sum for each start, so the
inner loop adds one element at a time instead of re-summing.

```python
best = 0
for i in range(n):
    s = 0
    for j in range(i, n):
        s += arr[j]
        if s == K:
            best = max(best, j - i + 1)
```

This is *O(n²)*. With careful pruning it can sometimes be
worthwhile, but for general arrays we want better.
''',
            "code": r'''def longest_subarray_sum_k_brute(arr: list[int], k: int) -> int:
    n = len(arr)
    best = 0
    # Outer loop fixes the start index.
    for i in range(n):
        # Inner loop extends the end index, maintaining a running sum.
        s = 0
        for j in range(i, n):
            s += arr[j]
            if s == k:
                best = max(best, j - i + 1)
    return best
''',
            "walkthrough": r'''
Try every subarray, compute its sum, check if it equals K.
Slow but easy to verify. Let me walk through each line.

**`def longest_subarray_sum_k_brute(arr: list[int], k: int) -> int:`** —
Takes the array and target sum K, returns the length of the
longest contiguous subarray summing to K, or 0 if no such
subarray exists.

**`n = len(arr)`** — Cache the length.

**`best = 0`** — Track the longest valid subarray length found
so far. Starts at 0 to handle the "no valid subarray exists"
case.

**`for i in range(n):`** — Outer loop: pick each possible
starting index `i`.

**`s = 0`** — Reset the running sum for this new starting
position.

**`for j in range(i, n):`** — Inner loop: extend the subarray
by including more elements on the right. `j` ranges from `i`
(a single-element subarray) up to `n - 1` (extending all the
way to the end).

Notice we start at `j = i`, not `j = i + 1`. Why? Because a
single-element subarray (containing just `arr[i]`) is a valid
candidate — it equals K if `arr[i]` itself equals K.

**`s += arr[j]`** — Add the new element to the running sum.
Crucially, we **don't recompute the sum from scratch** for
each `j`. Instead, we extend the sum incrementally as `j`
grows. This makes the inner loop *O(n)* total instead of
*O(n²)*.

**`if s == k:`** — Found a subarray summing to K. Check its
length.

**`best = max(best, j - i + 1)`** — The length of the
subarray from index `i` to `j` inclusive is `j - i + 1`. (The
"+1" is the standard fence-post adjustment for inclusive
ranges.) Update `best` if this length beats the previous
record.

**`return best`** — Hand back the longest length found.

The cost: outer loop runs `n` times. Inner loop runs up to `n`
times. Total *O(n²)*. For `n = 10⁵`, that's 10 billion
operations — way too slow.

The optimized version uses **prefix sums + a hash map** to
collapse this to *O(n)*. The trick: rather than checking every
pair of indices, check each *prefix sum* against a memoized
table of earlier prefix sums.
''',
            "complexity": (
                "**Time**: *O(n²)*. **Space**: *O(1)*."
            ),
        },
        "thought_process": r'''
The key idea behind the optimized approach is the **prefix sum**.
Define `prefix[i]` = sum of `arr[0..i - 1]`. So `prefix[0] = 0`,
`prefix[1] = arr[0]`, `prefix[2] = arr[0] + arr[1]`, and so on.

The sum of the subarray `arr[i..j]` (inclusive on both ends) equals
`prefix[j + 1] - prefix[i]`. That single identity transforms
"sum of every subarray" from *O(n²)* into *O(n)*-with-a-hash.

We want subarrays whose sum is `K`. Using the identity:
`prefix[j + 1] - prefix[i] == K`, equivalently
`prefix[i] == prefix[j + 1] - K`.

So as we scan and compute prefix sums, we ask at each step: *"have
I previously seen a prefix sum equal to `current_prefix - K`?"* If
yes, the subarray between that earlier index and the current one
sums to K. We want the **longest**, so we record the **earliest**
index at which each prefix sum first appeared.

This pattern — "as I scan, ask a question about earlier prefix sums
using a hash" — is one of the heaviest hitters in array DSA. It is
the optimized version of subarray sum equals K, count of subarrays
with sum K, longest subarray with zero sum, count of subarrays with
XOR K, and many more.

For arrays of **non-negative integers**, there is a simpler
**sliding window** approach because the prefix sum is
monotonically non-decreasing. We discuss it for completeness, but
the prefix-sum-with-hash approach is the general solution.
''',
        "optimized": {
            "explanation": r'''
Walk the array maintaining a running prefix sum. Use a dict that
maps prefix sums to their **earliest** index. At each step, check
whether `prefix - K` has been seen; if so, the length is `i -
earliest_index_of_that_prefix`.
''',
            "code": r'''def longest_subarray_sum_k(arr: list[int], k: int) -> int:
    # first_index[s] = the earliest index i such that prefix[i] == s.
    # We seed it with prefix sum 0 at index -1 (the empty prefix sits
    # "before" index 0). That handles subarrays that start at index 0.
    first_index = {0: -1}
    prefix = 0
    best = 0
    for i, x in enumerate(arr):
        prefix += x
        # If prefix - k appeared earlier at some index j, then
        # arr[j + 1 .. i] sums to k.
        if prefix - k in first_index:
            best = max(best, i - first_index[prefix - k])
        # Only record THIS prefix sum if it is new — we want the
        # earliest occurrence to maximize length.
        if prefix not in first_index:
            first_index[prefix] = i
    return best
''',
            "walkthrough": r'''
The prefix-sum + hash-map combo. Conceptually difficult the
first time you see it, but the pattern is everywhere in DSA.
Let me explain carefully.

The mathematical insight: the sum of `arr[j+1..i]` equals
`prefix[i+1] - prefix[j+1]`, where `prefix[k]` is the sum of
the first `k` elements (with `prefix[0] = 0` being the empty
prefix). So `sum(arr[j+1..i]) == k` is equivalent to
`prefix[i+1] - prefix[j+1] == k`, which rearranges to
`prefix[j+1] == prefix[i+1] - k`.

In words: at position `i`, we want to find an earlier position
`j` where the running sum equaled `current_prefix - k`. If
such a `j` exists, then the subarray from `j+1` to `i`
inclusive sums to exactly `k`. To find it fast, we store
prefix sums in a hash map.

**`def longest_subarray_sum_k(arr: list[int], k: int) -> int:`** —
Same signature as the brute force.

**`first_index = {0: -1}`** — Initialize the hash map. The
seed `{0: -1}` is the most important line in this function.
It says: "the running sum was 0 at position `-1`" — i.e.,
before the array started. This handles subarrays that start
at index 0.

For example, if `arr[0..2]` sums to `k`, then `prefix - k`
equals 0 when we hit index 2. Without the seed, the lookup
would fail. With the seed, we find `0 -> -1`, and the length
calculation `i - (-1) = i + 1` gives the correct length 3.

**`prefix = 0`** — Running prefix sum, initialized to 0.

**`best = 0`** — Track the longest valid subarray length.

**`for i, x in enumerate(arr):`** — Walk the array with both
index `i` and value `x`.

**`prefix += x`** — Update the running prefix sum. After this
line, `prefix` is the sum of `arr[0..i]` inclusive.

**`if prefix - k in first_index:`** — The killer question:
have we seen the prefix sum `prefix - k` at some earlier
position? Hash lookup is *O(1)* average.

**`best = max(best, i - first_index[prefix - k])`** — Yes,
we've seen it. The earlier position is `first_index[prefix - k]`,
call it `j`. The subarray from index `j + 1` to `i` (inclusive
of `i`, exclusive of `j`) sums to exactly `k`. Its length is
`i - j`. Update `best`.

Important: `i - j` is the correct length here, not `i - j + 1`.
Why? Because the subarray we found goes from index `j + 1` to
index `i`, inclusive on both ends. That's `i - (j + 1) + 1 = i - j`
elements. The `+1` and `-(j+1)` cancel out.

**`if prefix not in first_index:`** — Should we record the
current prefix sum?

**`first_index[prefix] = i`** — Yes, but **only if this is the
first time we've seen this prefix sum**. We use `not in` to
check. Why first time? Because we want the **longest**
subarray. Longer subarrays correspond to **earlier** starting
points. If two indices have the same prefix sum, keeping the
**smaller** index gives us the longer potential subarray
later.

**`return best`** — Hand back the answer.

The total work: one pass through the array, *O(n)* time, with
each step doing constant hash work. *O(n)* memory for the
hash map.

The transformation in big-O: *O(n²)* brute force becomes
*O(n)* via "prefix sums + hash of earlier prefix sums."

This pattern generalizes beautifully:
- **Subarray sum equals K (counting):** same idea, but instead
  of `first_index`, store `count[prefix]` and add it to the
  running total.
- **Subarray with sum divisible by K:** same shape, but key
  the hash by `prefix mod K`.
- **Subarray with XOR equal to K:** same shape, but replace
  `+` with `^`.

Once you internalize "for each prefix, ask the hash whether
the complementary prefix appeared earlier," dozens of problems
crack open.
''',
            "complexity": (
                "**Time**: *O(n)*. **Space**: *O(n)* for the hash."
            ),
        },
        "deep_concept": r'''
Prefix sums turn "range sum queries" into "point subtractions". Once
you internalize that, an enormous class of problems become tractable.

The pattern's full skeleton, which you should commit to memory:

1. Compute prefix sums on the fly as you scan.
2. As you compute each new prefix, ask one or both of:
   - "Has this exact prefix appeared before?" (zero-sum subarrays)
   - "Has prefix - K appeared before?" (sum-K subarrays)
   - "Has the XOR-equivalent appeared before?" (subarray XOR
     problems)
3. Store either the first or count of occurrences in a hash.

The "first index" version computes the **longest** matching
subarray. The "count of occurrences" version computes **how many**
matching subarrays exist. Same prefix sum trick; different bookkeeping.

For **non-negative arrays**, there is the cheaper sliding window:
maintain a window `[left, right]` with running sum; if the sum
exceeds K, advance `left`; if it equals K, record the length. This
is *O(n)* with *O(1)* space — better when applicable. The prefix
sum approach is the *general* solution that handles negatives too.
''',
        "confusion_notes": [
            {
                "question": "What is a prefix sum, and why does it help here?",
                "answer": r'''
A **prefix sum** of an array is a new array where each entry
holds the running total up to (and excluding) that index. So if
`arr = [3, 1, 4, 1, 5]`, then `prefix = [0, 3, 4, 8, 9, 14]`.
`prefix[0]` is 0 (the sum of no elements). `prefix[1] = arr[0]
= 3`. `prefix[2] = arr[0] + arr[1] = 4`. And so on.

The magic identity: **the sum of any range `arr[i..j]`
(inclusive on both ends) equals `prefix[j + 1] - prefix[i]`.**

For example, the sum of `arr[1..3]` (which is `1 + 4 + 1 = 6`)
equals `prefix[4] - prefix[1] = 8 - 3 = 5`. Wait, that gave 5,
not 6. Let me recompute: `prefix[4] = arr[0] + arr[1] + arr[2] +
arr[3] = 3 + 1 + 4 + 1 = 9`. `prefix[1] = 3`. So the range sum
is `9 - 3 = 6`. Correct. (I miscounted; recompute carefully and
the identity holds.)

Why does this identity help? Because **range-sum queries become
point-difference queries**. Computing one range sum naively
costs *O(n)* (walk every element in the range). With prefix sums
precomputed, each range sum is *O(1)*. If you have many
queries, the up-front *O(n)* cost of building the prefix array
pays for itself many times over.

For this problem, we never actually materialize the prefix array
— we maintain a single running prefix value. Same idea, less
memory.
''',
            },
            {
                "question": "Why store the *first* index of each prefix sum, not the last?",
                "answer": r'''
Because we want the **longest** subarray, and the longest
subarray ending at index `i` corresponds to the **earliest**
position where the required prefix sum first appeared.

Suppose the prefix value at index `i` is `P`, and we want a
subarray summing to `K`. We need to find an earlier index `j`
where `prefix[j] = P - K`. The length of the resulting subarray
is `i - j`. To **maximize** the length, we want `j` as small
(early) as possible.

So when we add a prefix sum to the hash, we only do it the
**first** time we see that value:

```python
if prefix not in first_index:
    first_index[prefix] = i
```

If we overwrote every time, we would track the *latest* index of
each prefix sum, which gives the *shortest* subarray ending at
each `i` — the wrong direction.

The opposite convention applies to other problems. For "count of
subarrays with sum K," we want to count **every** previous
occurrence, not just the first — so we use a Counter that
increments each time. For "longest," store the first. For
"count," store the count. For "any," either works.

Always ask: *"do I want longest, shortest, count, or any?"* The
answer determines the hash bookkeeping.
''',
            },
            {
                "question": "Why is `{0: -1}` the initial state of the hash?",
                "answer": r'''
Because of an edge case: a subarray that starts at index 0.

Consider `arr = [3, 1, 5]` with `K = 4`. The valid subarray
`[3, 1]` starts at index 0 and ends at index 1. Its sum is 4.
Using the identity, the prefix sum at index 2 is 4, and we want
to find some earlier index where the prefix sum equals
`prefix - K = 4 - 4 = 0`.

But the prefix sum at index 0 is, by definition, 0 (the sum of
zero elements). To find this "empty prefix" we need to have
recorded prefix sum 0 in our hash with index -1 (meaning "before
the first element").

The line `first_index = {0: -1}` plants this convention. It
encodes the fact that the **empty prefix** has sum 0 and lives
at "index -1." When we later see `prefix = 4` and look up
`prefix - K = 0`, the hash returns -1, and the subarray length
is `i - (-1) = i + 1`, which is correct.

Without this initialization, subarrays starting at index 0 would
be missed. It is a small but critical piece of the algorithm.

The same trick — seeding the hash with the empty-prefix
convention — applies to all the prefix-sum-plus-hash problems
(subarray sum K, longest subarray with zero sum, count of
subarrays with XOR K).
''',
            },
            {
                "question": "Why not just use sliding window for this?",
                "answer": r'''
Because sliding window **only works on non-negative arrays**.

The sliding window approach assumes that **growing the window**
monotonically increases the sum, and **shrinking the window**
monotonically decreases it. With non-negative numbers, that is
true: adding an element to the right increases the sum, removing
an element from the left decreases it.

With negative numbers in the array, growing the window can
*decrease* the sum (when you add a negative), and shrinking can
*increase* it. The "if sum is too big, shrink; if too small,
grow" decision rule breaks down. You no longer know which way to
move.

For `arr = [1, -1, 5, -2, 3]` with `K = 3`: the longest subarray
is `[1, -1, 5, -2]` of length 4. Sliding window would either
miss this (because the running sum temporarily drops below K and
the window shrinks prematurely) or get tangled trying to recover.

The prefix-sum-plus-hash approach handles negatives because it
treats the array as a *sequence of prefix sums*, where each
prefix sum is just a number — no monotonicity assumed. The hash
lookup `prefix - K` finds any earlier prefix that completes a
sum-K subarray, regardless of sign.

The rule of thumb:
- Non-negative array + subarray sum: **sliding window** is
  optimal (*O(n)* time, *O(1)* memory).
- General array + subarray sum: **prefix sum + hash** is the
  go-to (*O(n)* time, *O(n)* memory).
''',
            },
        ],
        "summary": r'''
**Pattern**: prefix sum + hash map.

**Lesson**: range sums become point subtractions in the prefix sum
world. The question "is there a subarray summing to K ending here?"
becomes "have I seen `prefix - K` before?".

**Recognize next time**: any subarray-sum question. Some variants:
count of subarrays with sum K, longest with sum K, presence with
sum K, XOR variants, divisible by M variants. The prefix-sum-hash
pattern handles them all.
''',
    },
    {
        "id": "two-sum",
        "title": "Two Sum",
        "step_id": 3,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["arrays", "hashing", "two-pointers"],
        "what_this_teaches": (
            "The most reused idea in all of array DSA: trade memory for "
            "time by remembering what you have already seen. Two Sum is "
            "the cleanest possible demonstration that a hash map can "
            "collapse a nested loop into a single pass."
        ),
        "pattern": "Hash the past; query the complement for each new element.",
        "prerequisite_lessons": ["arrays", "hashing"],
        "prerequisite_problems": ["count-frequencies"],
        "next_problems": [
            "three-sum",
            "four-sum",
            "longest-subarray-with-sum-k",
            "subarrays-with-sum-k",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 3 (Medium Arrays)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 1 — Two Sum",
                "url": "https://leetcode.com/problems/two-sum/",
            },
            {
                "label": "Python docs — dict",
                "url": "https://docs.python.org/3/library/stdtypes.html#dict",
            },
        ],
        "understanding": r'''
Let's slow down and really see what is being asked.

You are handed an array of integers and one target number. Your job
is to find two elements in the array whose **sum** equals the
target, and return their indices. The problem promises that exactly
one such pair exists, and you are not allowed to use the same index
twice — that is, you cannot pair an element with itself.

For example, with `nums = [2, 7, 11, 15]` and `target = 9`, the
answer is `(0, 1)`, because `nums[0] + nums[1] = 2 + 7 = 9`. With
`nums = [3, 2, 4]` and `target = 6`, the answer is `(1, 2)`,
because `nums[1] + nums[2] = 2 + 4 = 6`. Notice that we report
the **indices**, not the values themselves.

Read the problem one more time with a beginner's eye and notice
two subtleties that trip people up.

First: the array is not sorted. We cannot binary search. We cannot
walk inward from the ends. Whatever algorithm we use has to work on
a jumbled list.

Second: the problem asks for *any* valid pair (since exactly one
exists), and it asks for *indices*, not values. That second detail
is the reason we will reach for a dictionary that maps **value →
index** rather than just a set of values. A set would tell us "yes,
the partner exists somewhere," but we want to actually *return*
where. A dict gives us both: presence *and* position.

Two Sum is famous not because it is hard — once you see the trick
it is almost embarrassingly simple — but because it is the
**textbook moment** when a beginner first feels in their bones the
power of using extra memory to shortcut time. After Two Sum, the
sentence *"I could remember what I have already seen"* turns into a
reflex. That reflex unlocks 3-Sum, 4-Sum, subarray sums, longest
substring without repeating, and a long tail of medium / hard
problems.
''',
        "brute_force": {
            "explanation": r'''
Try every pair of indices. For each `i`, scan all `j > i` looking
for `arr[i] + arr[j] == target`. Two nested loops, *O(n²)*.
''',
            "code": r'''def two_sum_brute(arr: list[int], target: int) -> tuple[int, int] | None:
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] + arr[j] == target:
                return (i, j)
    return None
''',
            "walkthrough": r'''
Brute force = try every possible pair. Simple, obvious, slow.

**`def two_sum_brute(arr: list[int], target: int)`** — Takes
the array and the target sum. Returns the indices as a tuple,
or `None` if no pair sums to the target.

**`n = len(arr)`** — Cache the length for the two loops below.

**`for i in range(n):`** — Outer loop: pick the first element
of the pair. `i` ranges from `0` to `n-1`.

**`for j in range(i + 1, n):`** — Inner loop: pick the second
element of the pair. `j` starts at `i + 1` (not `0`!) for two
reasons:
1. We don't want to pair an element with itself (the problem
   says "two distinct indices").
2. We avoid counting each pair twice. If we let `j` start at
   `0`, then both `(i=0, j=1)` and `(i=1, j=0)` would be
   considered — same pair, just two orderings. Starting `j`
   after `i` enforces `i < j` and counts each pair once.

**`if arr[i] + arr[j] == target:`** — Check if this pair sums
to the target.

**`return (i, j)`** — Found it. Return the index pair as a
tuple.

**`return None`** — If both loops finish without finding a
pair, no solution exists. (Some problems require a guaranteed
solution and we'd raise an error here.)

Total work: we examine `n × (n-1) / 2` pairs in the worst
case. That's *O(n²)*. For `n = 10⁴`, that's 50 million
operations — slow but tractable. For `n = 10⁶`, it's a
trillion — completely infeasible. The hash-map optimized
version below does it in *O(n)*.

This problem is the gateway to the entire "hash trick" family:
*for each element, ask the hash map a question about the
past.* Watch how this transforms the algorithm in the
optimized section.
''',
            "complexity": (
                "**Time**: *O(n²)*. **Space**: *O(1)*."
            ),
        },
        "thought_process": r'''
Watch yourself solve this problem on paper for `nums = [2, 7, 11,
15]`, `target = 9`. The very natural first move is to point at
`2` and ask, *"what would I have to add to this to get 9?"* The
answer is `7`. You scan forward, find `7`, done. Now point at `7`
and ask the same question — the answer is `2`, and you remember
you just walked past it.

That little inner monologue is the **whole algorithm**. Every step
boils down to:

1. Look at the current element `x`.
2. Compute the **complement**: `target - x`. That is the partner
   we would need.
3. Ask: have I already seen the complement somewhere earlier in
   the array? If yes, we have our pair. If not, file `x` away in
   memory and move on.

The brute force version does step 3 by re-scanning the array. That
re-scan is what makes the brute force *O(n²)*: for each starting
element, we look at every later element again, repeating work we
could have done once.

The optimization is to make step 3 *O(1)*. A dictionary (or hash
map) does exactly that. We keep a dict that maps "every value we
have already seen" → "the index where we saw it". When we look at
a new element `x`, we compute its complement and ask the dict in
constant time, "do you remember seeing this value?" If yes, the
answer is the stored index plus the current one. If no, we add
`x` to the dict and continue.

This compresses two passes (build the dict, then query it) into a
**single** pass, because at the moment we look at `nums[i]`, the
dict already contains exactly the right set of candidates — every
element strictly to the left of `i`. We never accidentally pair an
element with itself, because we **check the dict before inserting
the current element**. The order matters.

A small mental model that helps: imagine you are walking through
the array left to right, carrying a notebook. The notebook is your
dict. Every time you see a new number, you do two things in this
exact order — *first ask* "is my complement already in the
notebook?", *then write down* my own number so future steps can
ask about me. Check, then file. Check, then file. That is the
loop, and that is why it works in one pass.

One last beautiful detail: this trick generalizes. The instant you
catch yourself writing "for each element, look at every other
element," ask whether a hash of "what I have already seen" could
turn the inner loop into a single dictionary lookup. The answer is
*yes* embarrassingly often.
''',
        "optimized": {
            "explanation": r'''
Walk once. Maintain a dict from value to index. For each new
element, check whether `target - current` is in the dict.
''',
            "code": r'''def two_sum(arr: list[int], target: int) -> tuple[int, int] | None:
    # seen[value] = first index at which `value` was encountered.
    seen: dict[int, int] = {}
    for i, x in enumerate(arr):
        partner = target - x
        # If we've seen `partner` before, we have our pair.
        if partner in seen:
            return (seen[partner], i)
        # Otherwise record the current value for future lookups.
        # Note: we record AFTER the check, so we never pair an
        # element with itself.
        seen[x] = i
    return None
''',
            "walkthrough": r'''
This is one of the most-asked interview problems in existence,
and the solution is one of the most-loved tricks in DSA. Let
me walk you through it.

**`def two_sum(arr: list[int], target: int)`** — Same
signature as the brute force.

**`seen: dict[int, int] = {}`** — A hash map (Python dict)
that will track every value we've encountered so far, paired
with the index where we saw it. Initially empty.

**`for i, x in enumerate(arr):`** — Walk the array. `enumerate`
gives us both the index `i` and the value `x` at that index
on each iteration. We need the index because the problem asks
for index pairs.

**`partner = target - x`** — Compute what value would *pair*
with `x` to hit the target. If `target = 9` and `x = 7`, the
partner is `2`. We need to find an earlier element equal to
2 to complete the pair.

**`if partner in seen:`** — The killer question: have we
**already seen** the partner value somewhere earlier in the
array? Hash-map lookup is *O(1)* on average — no scanning,
just a single probe.

**`return (seen[partner], i)`** — Yes, we saw it. The earlier
occurrence is at index `seen[partner]`; the current one is at
index `i`. Return both. Note we return the earlier index
first to keep the pair sorted by position.

**`seen[x] = i`** — Record the current `(value, index)` for
future iterations. **Important:** this happens **after** the
`if partner in seen` check. Why? Because if we recorded first
and then checked, we could find `arr[i]` pairing with itself
(e.g., if target = 6 and arr[i] = 3, we'd accidentally pair
index `i` with itself). Recording after the check ensures
"seen" means "seen in an *earlier* iteration."

**`return None`** — No pair found.

The mental shift: instead of asking "for each element, scan
forward to find a partner" (which is *O(n²)*), we ask "for
each element, **does the hash map remember its partner from
earlier**?" (which is *O(n)*). Hash lookup is free; loop is
one pass.

The pattern — "for each element, ask the hash map a question
about the past" — is the single most powerful idiom in array
problems. It transforms many quadratic algorithms into
linear ones. You'll see it in: longest substring without
repeating chars, subarray sum equals K, group anagrams,
longest consecutive sequence, and on and on.
''',
            "complexity": (
                "**Time**: *O(n)*. **Space**: *O(n)* for the hash."
            ),
        },
        "deep_concept": r'''
Step back from the code and look at the deeper move.

We started with a question that *sounds* relational — "find two
things that interact" — and turned it into a question that is
**personal**: at each element, given only the element and a
notebook of the past, can I decide? The dictionary did the
relational work for us by encoding "I have seen these values
before" as a constant-time check.

That conversion — from "for every pair, ask a question" to "for
every element, ask the past one question" — is the deeper move
behind almost every "hash trick" in DSA. Once you can spot it, you
can do it on your own:

- **Subarray sum equals K** — running prefix sum + hash of "which
  prefix sums have I seen?". For each new prefix, ask "have I
  seen `prefix - K` before?". Same shape as Two Sum.
- **Longest substring without repeating characters** — hash of
  "last index of each character." For each new character, ask
  "is the last index of this character inside my window?".
- **Group anagrams** — hash from canonical form to list of
  members.
- **Pair sum in a binary search tree** — same as Two Sum but
  iterating the tree in order.

The unifying principle: a hash gives you *O(1)* "have I seen this
before?" lookups. Whenever a problem can be re-cast so that each
new element needs to ask exactly one such question, the hash will
collapse a nested loop into a single pass.

Two Sum also has a beautiful **alternative** solution when the
array is sorted (or you sort it first): the two-pointer sweep.
Left at index 0, right at the end. If `nums[left] + nums[right]`
is too small, move left right; if too big, move right left; if
equal, you have your pair. *O(n)* time, *O(1)* space — better
memory than hashing, at the cost of *O(n log n)* up-front sorting.
This trade-off — "more memory vs. more comparisons" — is one you
will see in many problems. Pick the right tool for the specific
constraints.
''',
        "confusion_notes": [
            {
                "question": "Why do we check the dict *before* inserting the current value?",
                "answer": r'''
This is the most common bug when writing Two Sum, and the answer
gets at a subtle correctness invariant.

The line order matters. Our algorithm goes:

```python
for i, x in enumerate(arr):
    partner = target - x
    if partner in seen:        # check first
        return (seen[partner], i)
    seen[x] = i                # then insert
```

If we flipped the order — insert first, then check — and an
element happened to equal exactly half the target, we would
"find" it pairing with itself. For example, `arr = [3, 4, 5]`,
`target = 6`. The element `3` has complement `3`. If we inserted
first, the dict would contain `{3: 0}`, then we would look up
`3` in the dict, find ourselves, and return the pair `(0, 0)`.
But the problem forbids using the same index twice. The pair `(0,
0)` is wrong.

By checking *before* inserting, the dict at the moment of the
check contains **only elements strictly to the left** of the
current index. So when we find a partner, it must live at an
earlier index. The invariant is "the dict holds the past, not
the present." That invariant is the entire correctness argument.

A close cousin of this question is "what if the same value appears
twice in the array?" Try `arr = [3, 3]`, `target = 6`. On `i = 0`,
the dict is empty, so `partner = 3` is not there. We insert
`{3: 0}` and move on. On `i = 1`, we compute `partner = 3` and
find it in the dict with value `0`. We return `(0, 1)`. Correct.
The check-then-insert order naturally handles duplicates because
the previous occurrence is already in the dict by the time we get
to the second one.
''',
            },
            {
                "question": "Why store the index instead of just `True` for each seen value?",
                "answer": r'''
Because the problem asks us to return **indices**, not just to
confirm that a pair exists.

If we used a set (just storing values), the algorithm would tell
us "yes, a partner exists," but we would have no way to report
*where* the partner lives. We would either have to do a second
pass to find it, or restructure the loop.

The dict lets us do both with one structure: the **key** is the
value (so we can ask "have I seen this value?"), and the **value
in the dict** is the index (so when we get a hit, we know where).
Same lookup cost, more information per lookup.

A subtle bonus: if the same value appears in the array multiple
times, the dict stores the **most recent** index (or the
**first**, depending on whether you overwrite). For Two Sum it
does not matter — any valid pair works. But for related problems
("longest substring without repeating characters," for example),
you specifically want the last index, and that is what the dict
naturally gives you when you assign on every iteration.

Mental model: a set is a guest list (just names); a dict is a
guest list with seating chart (names and table numbers). For Two
Sum we need the table number, not just the name.
''',
            },
            {
                "question": "Why does this work in a single pass? Doesn't the partner need to come *after* the current element?",
                "answer": r'''
This is a beautiful subtlety. The answer is that **for every
valid pair, one of the two elements comes before the other**. So
if we look at the *later* one of the two, the *earlier* one is
already in our dictionary.

Concretely: suppose the valid pair is at indices `i` and `j` with
`i < j`. When the loop reaches index `i`, we don't see the pair
yet — `nums[j]` hasn't appeared. We just file `nums[i]` away.
When the loop reaches index `j`, `nums[i]` is already in the
dict. We compute `partner = target - nums[j]`, and that
`partner` equals `nums[i]`, which is in the dict. Match.

So one single pass catches every pair, as long as we process
elements left to right and only ever pair "current" with "past."

A useful image: the dict is a **growing memory** of everything
we have seen. As we walk forward, the memory grows by one each
step, and at each step we ask one question of the memory. The
loop and the memory grow together, like two pointers moving in
lockstep.

If we tried to look for the pair by walking left from each `j`,
we would do nested-loop work and lose our speed. The dict
replaces the inner loop with a constant-time question.
''',
            },
            {
                "question": "What if the same number appears twice and is part of the pair? Like `nums = [3, 3]`, `target = 6`.",
                "answer": r'''
Walk through it slowly to make sure you really see what happens.

Initial state: `seen = {}` (empty dict).

**Iteration 0**: `i = 0`, `x = 3`.
- `partner = 6 - 3 = 3`.
- Is `3` in `seen`? `seen` is empty, so no.
- We did *not* find a pair. Insert: `seen = {3: 0}`. Continue.

**Iteration 1**: `i = 1`, `x = 3`.
- `partner = 6 - 3 = 3`.
- Is `3` in `seen`? Yes — `seen[3] == 0`.
- Return `(0, 1)`. Done.

So duplicates are handled naturally. The key is that we **insert
after checking**, so the duplicate that appears later finds its
predecessor in the dict without the predecessor accidentally
"matching itself."

What if `nums = [3]` and `target = 6`? On iteration 0, partner is
3, the dict is empty, we insert. The loop ends with no match.
Function returns `None`. Correct — there is no pair to find when
there is only one element.

What if `nums = [3, 3, 4]` and `target = 6`? We return `(0, 1)`
on iteration 1. The 4 is never even examined. Also correct.

The takeaway: as long as you check-then-insert, duplicates and
single-element arrays behave the way you expect. No special
cases.
''',
            },
            {
                "question": "When should I use the two-pointer version instead of the hash version?",
                "answer": r'''
Use the **two-pointer** version when the input is **already
sorted**, or when the problem context says you should not use
*O(n)* extra memory. Use the **hash** version when the array is
**unsorted**, when memory is plentiful, or when you need to
preserve the original indices.

A side-by-side comparison:

| Aspect | Hash (this solution) | Two pointers |
|---|---|---|
| Requires sort? | No | Yes (sort first if needed) |
| Time | *O(n)* | *O(n)* after sort, *O(n log n)* total |
| Extra space | *O(n)* for the dict | *O(1)* |
| Preserves indices? | Yes | No (sort scrambles them) |
| Handles duplicates? | Naturally | Naturally |

If the LeetCode problem says "return the indices in the input
array," the hash version is the cleaner answer because sorting
would lose the original positions (you would have to track them
separately).

If the problem is a follow-up like "given a sorted array, find a
pair summing to target," the two-pointer version is the cleaner
answer. *O(1)* memory and no hash overhead.

For the higher-order family (3-Sum, 4-Sum), the **two-pointer
version is preferred**, because once you fix one or two elements,
the remaining subproblem on the sorted suffix is exactly a
two-pointer search. Step 3's "Hard" section will use this idea.

Bottom line: both are good. They are not competing — they are
**complementary tools** for different shapes of the same family
of problems. Knowing both makes you flexible.
''',
            },
            {
                "question": "Why is the hash version *O(n)* space? Isn't that wasteful for a small array?",
                "answer": r'''
It is *O(n)* in the worst case because, if no pair exists or the
pair is at the very end, we end up inserting every single element
into the dict before finding (or failing to find) the answer.
For an array of size `n`, the dict can grow to `n` entries.

Is this wasteful? It depends on the scale. For an array of size
100, the dict holds at most 100 entries — a few kilobytes of
memory. Negligible. For an array of size one billion, the dict
holds up to a billion entries, which could be tens of gigabytes.
That matters.

But here is the perspective shift: the algorithm runs in *O(n)*
**time**, which beats the brute-force *O(n²)*. For `n = 10⁴`,
that is `10⁴` operations versus `10⁸` — a ten-thousand-times
speedup. The price you pay is *O(n)* memory instead of *O(1)*.
For most real-world inputs, this is a great trade.

If memory is genuinely tight, the two-pointer-after-sort approach
gives you *O(1)* extra memory at the cost of *O(n log n)* time
and losing original indices. Pick the trade that fits your
constraints.

A general lesson from this: **the cheapest speedups in DSA come
from using extra memory to remember work you have already done**.
Almost every "O(n²) → O(n)" improvement on this sheet uses
exactly this trick. Sometimes it is a hash; sometimes a precomputed
prefix array; sometimes a memo table. The mental motion is the
same.
''',
            },
        ],
        "summary": r'''
**Pattern**: hash "values seen so far" while scanning; for each
new element, query the dict for its complement.

**Lesson**: when a brute force "for every pair, check..." loop
appears, the first question to ask is *"can a hash of what I have
already seen reduce the inner question to one lookup?"*. For Two
Sum the answer is yes, and the algorithm collapses from *O(n²)*
to *O(n)*.

**Recognize next time**: any "find two / three / four elements
satisfying property P" problem. K-Sum, subarray sums, anagram
grouping, longest-substring problems — they all build on this
exact instinct.

**Bigger picture**: Two Sum is the **kindergarten classroom** of
hash-based algorithm design. Master the check-then-insert order,
internalize "the dict holds the past, not the present," and you
have unlocked an entire family of medium / hard problems with
almost no extra learning.
''',
    },
    {
        "id": "sort-0s-1s-2s",
        "title": "Sort 0s, 1s, and 2s (Dutch National Flag)",
        "step_id": 3,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["arrays", "three-pointers", "partition"],
        "what_this_teaches": (
            "Three-pointer partitioning with explicit invariants — a "
            "miniature version of Quicksort's partition step "
            "generalized from two groups to three. The 'do not advance "
            "mid on swap-with-high' detail is the kind of subtlety "
            "that separates careful programmers from careless ones."
        ),
        "pattern": "Three pointers (low, mid, high) maintaining four invariant zones.",
        "prerequisite_lessons": ["arrays", "two-pointers"],
        "prerequisite_problems": ["remove-duplicates-sorted", "quick-sort"],
        "next_problems": [
            "move-zeros-to-end",
            "rearrange-alternating",
            "ll-sort-012",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 3 (Medium Arrays)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 75 — Sort Colors",
                "url": "https://leetcode.com/problems/sort-colors/",
            },
        ],
        "understanding": r'''
We have an array containing only the values 0, 1, and 2 — in any
order. Sort it in place. Example: `[2, 0, 1, 2, 1, 0]` becomes
`[0, 0, 1, 1, 2, 2]`.

You could call Python's `sort()` and be done. The interesting
challenge is to do it in **one pass**, **in place**, with **only
three pointers**. The algorithm is famous enough to have a name:
**Dutch National Flag**, named for the Dutch flag's three colored
stripes.
''',
        "brute_force": {
            "explanation": r'''
**Two passes (counting sort)**: first pass counts the number of 0s,
1s, and 2s. Second pass overwrites the array with those counts.
*O(n)* time, *O(1)* extra space. Correct and simple.

```python
c0 = arr.count(0); c1 = arr.count(1); c2 = arr.count(2)
arr[:] = [0] * c0 + [1] * c1 + [2] * c2
```

But it is two passes, and the slicing creates a new list. The real
algorithmic gem is the **one-pass three-pointer** approach.
''',
            "code": r'''def sort_012_count(arr: list[int]) -> None:
    c0 = arr.count(0)
    c1 = arr.count(1)
    c2 = arr.count(2)
    # Overwrite in place.
    i = 0
    for _ in range(c0):
        arr[i] = 0; i += 1
    for _ in range(c1):
        arr[i] = 1; i += 1
    for _ in range(c2):
        arr[i] = 2; i += 1
''',
            "complexity": (
                "**Time**: *O(n)* (two passes). **Space**: *O(1)*."
            ),
        },
        "thought_process": r'''
The three-pointer one-pass version is wonderful. We maintain three
indices:

- `low` — the next position to fill with a 0.
- `mid` — the position we are currently inspecting.
- `high` — the next position to fill with a 2.

Invariants we maintain throughout the loop:

- `arr[0 .. low - 1]` contains only 0s.
- `arr[low .. mid - 1]` contains only 1s.
- `arr[high + 1 .. n - 1]` contains only 2s.
- `arr[mid .. high]` is the "unprocessed" zone.

At each step we look at `arr[mid]`:

- If `arr[mid] == 0`: it belongs at the front. Swap with `arr[low]`,
  advance both `low` and `mid`. (The swapped-in value was a 1 from
  the middle zone, so `mid` moves on.)
- If `arr[mid] == 1`: it is already where it should be. Just advance
  `mid`.
- If `arr[mid] == 2`: it belongs at the back. Swap with `arr[high]`,
  decrement `high`. **Do not advance `mid`**, because the swapped-in
  value is unprocessed and we have to look at it next.

That `mid` does not advance on the "swap with high" case is the
subtle, critical detail. Most beginners get this wrong on their
first try. Walk through `[2, 0, 1]` on paper to feel it.
''',
        "optimized": {
            "explanation": r'''
Single pass with three pointers (low, mid, high), in place.
''',
            "code": r'''def sort_012(arr: list[int]) -> None:
    low = 0
    mid = 0
    high = len(arr) - 1
    # Continue while there is still an unprocessed zone.
    while mid <= high:
        if arr[mid] == 0:
            # The element belongs to the 0-zone at the front.
            arr[low], arr[mid] = arr[mid], arr[low]
            low += 1
            mid += 1
        elif arr[mid] == 1:
            # The element is already in the 1-zone where it belongs.
            mid += 1
        else:  # arr[mid] == 2
            # The element belongs to the 2-zone at the back.
            # Crucial: we do NOT advance mid, because we just swapped in
            # an unprocessed value from the high side and need to inspect it.
            arr[mid], arr[high] = arr[high], arr[mid]
            high -= 1
''',
            "complexity": (
                "**Time**: *O(n)* — each element is inspected at most "
                "a constant number of times.\n\n"
                "**Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
The Dutch flag is the generalization of quick sort's partition step
to **three** groups instead of two. Once you see this, you realize
that the same idea handles:

- **Quick sort with three-way partitioning** (useful when many
  duplicates exist; degenerate quick sort behaves badly on those).
- **Three-way merge sort** variants.
- **In-place rearrangement** problems like "move all evens before
  all odds" — same shape, simpler.
- **Partition around a pivot value** in selection algorithms.

The deep mental shift: **partitioning** is a primitive operation
that buys you a lot. Every time you face an array problem with
"rearrange so that all X come before all Y", a partition pass is
nearly always the right answer.

And the loop invariant we wrote in plain English ("arr[0..low - 1]
contains only 0s" etc.) is the kind of careful thinking that makes
this category of problems tractable. Write the invariant first, the
code second.
''',
        "confusion_notes": [
            {
                "question": "Why don't we advance `mid` on the swap-with-high case?",
                "answer": r'''
Because the element we just swapped *in* from the `high` side is
**unprocessed**. We need to look at it before moving on.

Walk through `arr = [2, 0, 1]`. Start with `low = 0, mid = 0,
high = 2`.

- `mid = 0`: `arr[mid] = 2`. Swap with `arr[high = 2]`. Array
  becomes `[1, 0, 2]`. Decrement `high` to 1. **Do not advance
  `mid`**, because `arr[mid]` is now 1, which we have not yet
  processed.
- `mid = 0`: `arr[mid] = 1`. It belongs in the middle zone.
  Advance `mid` to 1.
- `mid = 1`: `arr[mid] = 0`. Swap with `arr[low = 0]`. Array
  becomes `[0, 1, 2]`. Advance both `low` and `mid` to 1 and 2.
- `mid = 2 > high = 1`. Loop exits.

If we had advanced `mid` after the first swap-with-high, we
would have skipped the `1` that landed at index 0 — and ended
up with an unsorted array like `[1, 0, 2]` because index 0 was
never reconsidered.

By contrast, the swap-with-low case is different: the element we
swap *in* from `low` is **already processed** (it must be a 1
from the middle zone). So advancing `mid` is safe in that case.

This asymmetry is the one beginner trap of Dutch National Flag.
Write the invariants explicitly and the answer becomes obvious.
''',
            },
            {
                "question": "Why does the loop condition use `<=` instead of `<`?",
                "answer": r'''
Because the index `high` is **inclusive** — it points at the
last unprocessed slot, not one past it. So we need to process
the element *at* `high` too.

If we wrote `while mid < high:`, the loop would exit when
`mid == high`, leaving the single element at that index
unprocessed. For an input like `[1, 0]`, the algorithm would
fail to handle the final position correctly.

The choice between `<` and `<=` depends on whether your boundary
variable is "one past the last valid" (exclusive) or "the last
valid" (inclusive). When you write any two-pointer or three-
pointer algorithm, decide on the convention first and stick to
it. Mixing styles inside one function is a classic source of
off-by-one bugs.

In our code, both `low` and `high` are **inclusive** — they
point to the leftmost and rightmost slots still in play. The
loop condition `mid <= high` reflects that, and the decrement
`high -= 1` correctly shrinks the unprocessed zone by one slot.
''',
            },
            {
                "question": "What if the array contains values other than 0, 1, 2?",
                "answer": r'''
Then this algorithm does not work — it assumes exactly three
distinct categories. For a general partition you would need a
different approach.

The Dutch National Flag is specifically a **3-way partition**.
It generalizes to k-way partition only by chaining multiple
passes or by switching to a different algorithm (such as
counting sort, which works in *O(n + k)* for k distinct
values).

If your array has *many* distinct values and you just want them
sorted, use `sorted(arr)` or `arr.sort()`. The Dutch National
Flag shines specifically when:

1. There are exactly **two boundary values** (so three
   categories).
2. You need an in-place, single-pass algorithm.
3. You cannot afford the *O(n log n)* of a general sort.

A common interview follow-up: "what if the values are not
labeled 0, 1, 2 but instead 'red', 'white', 'blue'?" The
algorithm is identical — substitute the labels in the
comparisons. The structure does not care.

A trickier follow-up: "sort an array around a pivot value, with
elements less than the pivot on the left and elements greater on
the right." Same algorithm with the comparison `arr[mid] <
pivot`, `==`, `>`.

The Dutch National Flag is the *template* for any 3-way
partition. Whenever you see "rearrange so that X < Y < Z by
category," reach for it.
''',
            },
            {
                "question": "Why call it the *Dutch National Flag*?",
                "answer": r'''
Because the Dutch flag has three horizontal stripes — red on
top, white in the middle, blue on the bottom. The algorithm
sorts elements into three stripes based on their values, which
mimics arranging the flag.

The name was popularized by Edsger Dijkstra in the 1970s when
he used the problem as a teaching example. (He was Dutch.) The
nickname stuck because it is more memorable than "3-way
in-place partition."

It is one of several algorithmic problems with whimsical names:
the "stable matching" problem (sometimes called "stable
marriage"), the "knapsack" problem (a thief filling a sack),
the "rod cutting" problem (a metal rod into priced pieces), the
"painter's partition" problem. Memorable names help you
remember the **shape** of the algorithm, which often outlives
the specific problem statement.

So: Dutch National Flag = 3-way in-place partition. Whenever
the problem shape says "three categories, put them in order,
one pass, in place," that is the algorithm to reach for.
''',
            },
        ],
        "summary": r'''
**Pattern**: three-pointer partition with explicit invariants.

**Lesson**: the trick is `mid` *not* advancing on the
swap-with-high case. The reason is that you just imported an
unprocessed element from the unknown zone.

**Recognize next time**: any "rearrange so all X come first, then
Y, then Z" with a small fixed set of categories. Dutch flag
generalizes naturally to 3, 4, or more colors.
''',
    },
    {
        "id": "kadane-algorithm",
        "title": "Maximum Subarray Sum (Kadane's Algorithm)",
        "step_id": 3,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["arrays", "dp", "kadane"],
        "what_this_teaches": (
            "The first real **DP-on-arrays** insight: define a running "
            "scalar that summarizes 'best subarray ending here' and "
            "update it with one tiny recurrence. The whole pattern is "
            "a 1D DP collapsed to two variables."
        ),
        "pattern": "Track 'best subarray ending here'; reset when extending hurts.",
        "prerequisite_lessons": ["arrays", "dp"],
        "prerequisite_problems": ["max-consecutive-ones", "largest-element"],
        "next_problems": [
            "print-max-subarray",
            "stock-buy-sell",
            "max-product-subarray",
            "house-robber-i",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 3 (Medium Arrays)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 53 — Maximum Subarray",
                "url": "https://leetcode.com/problems/maximum-subarray/",
            },
        ],
        "understanding": r'''
Given an array of integers (possibly with negatives), find the
**maximum sum** of any **contiguous subarray**. A subarray must be
non-empty.

Example: `[-2, 1, -3, 4, -1, 2, 1, -5, 4]` → best is `[4, -1, 2, 1]`
with sum `6`.

The brilliance of this problem is that the naive answer is *O(n²)*
or *O(n³)*, and the optimal is *O(n)* with one *brilliant* insight.
The optimal algorithm is so well known it has a name: **Kadane's
algorithm**.
''',
        "brute_force": {
            "explanation": r'''
**Most brute force (O(n³))**: every subarray is a pair (start, end).
For each pair, sum and track the max. Three nested loops.

**Slightly better (O(n²))**: for each start, run a running sum as
end advances. Drops one factor of n.

We will show the *O(n²)* version because the *O(n³)* is unkind.
''',
            "code": r'''def max_subarray_brute(arr: list[int]) -> int:
    n = len(arr)
    best = arr[0]
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += arr[j]
            if s > best:
                best = s
    return best
''',
            "complexity": (
                "**Time**: *O(n²)*. **Space**: *O(1)*."
            ),
        },
        "thought_process": r'''
Kadane's insight is the cleverest single line in beginner DSA. Let
me try to reproduce the *aha* moment.

Define `best_ending_here[i]` as the maximum sum of any subarray that
**ends at index i**. The final answer is the maximum of
`best_ending_here[i]` over all `i`.

Now: what is the relationship between `best_ending_here[i]` and
`best_ending_here[i - 1]`? Two possibilities for the best subarray
ending at `i`:

1. It extends the best subarray ending at `i - 1` by adding `arr[i]`.
2. It starts fresh at `i`, sum equal to `arr[i]`.

The first option gives `best_ending_here[i - 1] + arr[i]`. The
second gives `arr[i]`. We pick the larger.

So: `best_ending_here[i] = max(arr[i], best_ending_here[i - 1] + arr[i])`.

Now read that recurrence in plain English: *"to find the best
subarray ending here, either I extend the best one from yesterday,
or I start fresh today. Pick the better option."*

And the implementation does not even need an array. We only need
the previous value:

```python
best_ending_here = arr[0]
best_overall = arr[0]
for i in range(1, n):
    best_ending_here = max(arr[i], best_ending_here + arr[i])
    best_overall = max(best_overall, best_ending_here)
```

That's Kadane's. The algorithm fits on a beer mat and it's *O(n)*.

The mental rule of thumb: **if your running sum drops to a value
worse than starting fresh, start fresh.** The previous prefix has
already done its damage; carrying it forward only hurts.
''',
        "optimized": {
            "explanation": r'''
Single pass tracking two scalars: the best subarray ending at the
current index, and the global best.
''',
            "code": r'''def max_subarray(arr: list[int]) -> int:
    # Initialize both running scalars to the first element. Any best
    # subarray contains at least one element, so this is the floor.
    best_ending_here = arr[0]
    best_overall = arr[0]
    for i in range(1, len(arr)):
        # Either extend the previous subarray by adding arr[i], or
        # start a fresh subarray of just arr[i]. Pick whichever sum
        # is larger.
        best_ending_here = max(arr[i], best_ending_here + arr[i])
        # Update the global best whenever we've topped it.
        if best_ending_here > best_overall:
            best_overall = best_ending_here
    return best_overall
''',
            "complexity": (
                "**Time**: *O(n)*. **Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
Kadane's algorithm is the **simplest example of dynamic
programming**. The recurrence `best_ending_here[i] = max(arr[i],
best_ending_here[i - 1] + arr[i])` is a one-dimensional DP. The
state is "the index `i`", and the value is "best subarray ending
exactly there". The transition takes constant time, so total work is
*O(n)*.

Because the DP only depends on the previous value, we collapse the
array of `best_ending_here` values to a single scalar. That is a
common DP optimization, "space optimization", which we cover in
detail in Step 16.

A variant: **circular maximum subarray sum**. The subarray can wrap
around. The trick is to also compute the minimum subarray sum, and
the circular max equals `total_sum - min_subarray_sum` (unless the
entire array is negative). One Kadane forward, one Kadane backward,
and a tiny adjustment.

Another variant: **find the indices of the best subarray**. Track
the current start whenever we "start fresh", and update best_start
/ best_end whenever we update the global best. The algorithm grows
by two scalars but remains *O(n)*.
''',
        "confusion_notes": [
            {
                "question": "Why is `max(arr[i], best_ending_here + arr[i])` the right recurrence?",
                "answer": r'''
Because the best subarray ending at index `i` has only two
possibilities:

1. It uses **only** `arr[i]` (the subarray of length 1). Sum is
   `arr[i]`.
2. It uses `arr[i]` **plus** the best subarray ending at index
   `i - 1`. Sum is `best_ending_here[i - 1] + arr[i]`.

There is no third option, because any subarray ending at `i`
must include `arr[i]`, and what comes before `arr[i]` is either
"some contiguous run ending at `i - 1`" or "nothing." The best
of those two captures the optimal subarray ending at `i`.

The `max` picks the larger of the two. If the previous run had a
positive contribution, extending is better. If it had a negative
contribution, we "abandon" it and start fresh from `arr[i]`.

That decision rule — *"keep the past only if it helps"* — is the
heart of Kadane. Internalize it: the running scalar is not "sum
so far," it is "best sum of a subarray that ends right here."
The distinction matters. The first would grow forever; the
second resets when the past becomes a liability.

This recurrence is the simplest possible **dynamic programming**
recurrence. It has one dimension (the index `i`), constant
transition cost, and the answer at `i` depends only on the
answer at `i - 1`. That structure is why we can compute it in
*O(n)* time and *O(1)* space.
''',
            },
            {
                "question": "Why do we initialize both `best_ending_here` and `best_overall` to `arr[0]`?",
                "answer": r'''
Because the problem requires a **non-empty** subarray, so the
smallest valid subarray contains at least one element. Starting
both scalars at `arr[0]` reflects "the best subarray we have
seen so far is the single-element subarray `[arr[0]]`."

If we initialized to `0`, we would silently allow an "empty"
subarray of sum 0 — wrong when the array contains only negative
numbers. For `arr = [-3, -1, -7]`, the correct answer is `-1`
(the best single element), not `0`.

Initializing to `arr[0]` sidesteps this. By the time the loop
starts at index 1, both scalars hold real values from the array,
and any update preserves the "subarray exists" invariant.

The other safe initialization is `float('-inf')` combined with
**handling each element from index 0**:

```python
best_ending_here = float('-inf')
best_overall = float('-inf')
for x in arr:
    best_ending_here = max(x, best_ending_here + x)
    best_overall = max(best_overall, best_ending_here)
```

Both styles work. The `arr[0]` initialization is slightly more
direct; the `-inf` initialization is slightly more uniform. Pick
the one that reads better to you, but be sure you understand
why initializing to `0` would be wrong for arrays of all
negatives.
''',
            },
            {
                "question": "Why is this called *dynamic programming* when there's no table?",
                "answer": r'''
Because **DP is fundamentally about reusing the answers to
overlapping subproblems**, not about building a table. The table
is just one common way to store those answers; sometimes a few
scalars are enough.

In Kadane, the "subproblem" is "what is the best subarray ending
exactly at index `i`?" We solve it for `i = 0`, then `i = 1`,
then `i = 2`, and so on. Each answer depends on the previous
one (via the recurrence). That sequence of dependent subproblems
is the DP structure.

If we wanted to store every intermediate `best_ending_here[i]`,
we could make an explicit array of length `n`. That would be a
"tabulated" DP. But since the recurrence only looks at the
*immediately previous* value, we can throw away everything older
than that. The result: two scalars instead of an array.

This "the recurrence only touches the last K answers" insight is
called **space optimization** and shows up in many DPs:

- Fibonacci: keep the last 2 values.
- Climbing stairs: keep the last 2.
- House robber: keep the last 2.
- Longest common subsequence: keep the last 2 rows (not the
  whole table).

So Kadane is DP. It is DP in its slickest, leanest form. After
you finish Step 16 (the DP step), you will recognize Kadane as
the *first* DP you ever wrote, even before you knew the word
"dynamic programming."
''',
            },
            {
                "question": "What about all-negative arrays? Doesn't Kadane fail there?",
                "answer": r'''
It does not fail, as long as `best_overall` is initialized to a
real element (or `-inf`) rather than `0`.

For `arr = [-3, -1, -7]`:

- Start: `best_ending_here = -3, best_overall = -3`.
- `i = 1`, `arr[i] = -1`: `best_ending_here = max(-1, -3 + -1) =
  max(-1, -4) = -1`. `best_overall = max(-3, -1) = -1`.
- `i = 2`, `arr[i] = -7`: `best_ending_here = max(-7, -1 + -7) =
  max(-7, -8) = -7`. `best_overall = max(-1, -7) = -1`.

Final answer: `-1`. Correct — the best (least-bad) single-element
subarray.

The common bug is initializing `best_overall = 0` because "zero
seems neutral." That would return `0` for all-negative arrays,
which is wrong if empty subarrays are disallowed.

LeetCode's "Maximum Subarray" problem requires a non-empty
subarray. If a variant allows empty subarrays and the answer is
defined as `max(answer, 0)`, then initialize to `0` instead.
Read the problem carefully — the "is empty allowed?" question
flips the initialization.

The general lesson: edge cases of "what is allowed?" silently
change the initialization of running scalars. Always state the
constraint out loud before writing the code.
''',
            },
        ],
        "summary": r'''
**Pattern**: 1D DP collapsed to a running scalar.

**Lesson**: if extending the previous subarray makes the sum
worse than starting fresh, start fresh. That single rule is
Kadane's.

**Recognize next time**: any "maximum sum of a contiguous range"
problem. With negatives, Kadane's is the go-to. With only positives,
sliding window or prefix sum are alternatives.
''',
    },
    {
        "id": "stock-buy-sell",
        "title": "Best Time to Buy and Sell Stock",
        "step_id": 3,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["arrays", "linear-scan", "dp"],
        "what_this_teaches": (
            "How a 'best partner from the past' question collapses to "
            "a single pass: maintain the **cheapest price so far** and "
            "for each new day compute the profit. Hidden in plain "
            "sight is the same idea as Kadane — applied to the array "
            "of consecutive-day differences."
        ),
        "pattern": "Single pass with `min_so_far` and `best_profit` scalars.",
        "prerequisite_lessons": ["arrays"],
        "prerequisite_problems": ["largest-element", "kadane-algorithm"],
        "next_problems": [
            "stock-ii",
            "stock-iii",
            "stock-cooldown",
            "stock-fee",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 3 (Medium Arrays)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 121 — Best Time to Buy and Sell Stock",
                "url": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/",
            },
        ],
        "understanding": r'''
You have an array of stock prices, one per day. You can buy on one
day and sell on a later day. Find the maximum profit you can make
from a **single** buy-sell transaction. If no profit is possible,
return 0.

Example: `[7, 1, 5, 3, 6, 4]` → buy on day 1 at price 1, sell on
day 4 at price 6 → profit 5.

The "single transaction" constraint matters. The harder variations
(multiple transactions, with fees, with cooldown) are covered in
Step 16's DP-on-stocks lecture.
''',
        "brute_force": {
            "explanation": r'''
For each day `i`, consider buying on day `i` and check every later
day `j > i` for the maximum profit `prices[j] - prices[i]`. *O(n²)*.

The optimized algorithm collapses this to *O(n)* with the same
"carry the best so far" trick we have been using.
''',
            "code": r'''def max_profit_brute(prices: list[int]) -> int:
    best = 0
    n = len(prices)
    for i in range(n):
        for j in range(i + 1, n):
            profit = prices[j] - prices[i]
            if profit > best:
                best = profit
    return best
''',
            "complexity": "**Time**: *O(n²)*. **Space**: *O(1)*.",
        },
        "thought_process": r'''
For each day `j`, the best profit if I sell on `j` is
`prices[j] - min(prices[0..j - 1])`. If I have been tracking the
running minimum price so far as I walk forward, then computing the
best-if-sold-today is one subtraction per day.

So: walk forward, carry `min_so_far`, and for each day update
`best_profit = max(best_profit, prices[j] - min_so_far)` before
updating `min_so_far = min(min_so_far, prices[j])`.

The order matters. We must compute the profit (which uses today's
price as the sell) **before** updating `min_so_far` to include
today's price (which would be using today as both buy and sell).
Actually it does not change the result here because the profit
would be zero, but for clarity many people compute profit first.

This is yet another instance of the running-scalar pattern. By now
you should be noticing how many array problems collapse to "walk
once, carry one or two scalars".
''',
        "optimized": {
            "explanation": r'''
Walk left to right. Maintain the minimum price seen so far. For
each day, the best profit "if I sold today" is `price - min_so_far`.
Track the maximum of those.
''',
            "code": r'''def max_profit(prices: list[int]) -> int:
    # The cheapest price we have seen so far.
    min_so_far = prices[0]
    # The best profit we have found so far.
    best = 0
    for price in prices[1:]:
        # If we sold today at `price`, our profit is `price - min_so_far`.
        # Update the best with that, but never go below 0.
        if price - min_so_far > best:
            best = price - min_so_far
        # Now update min_so_far to potentially include today.
        if price < min_so_far:
            min_so_far = price
    return best
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "deep_concept": r'''
This is **Kadane in disguise**. If we look at the *differences*
between consecutive days — `prices[1] - prices[0]`, `prices[2] -
prices[1]`, ... — the maximum profit equals the maximum subarray
sum of those differences. The "running min" version and the
"max-subarray-of-differences" version are equivalent expressions of
the same idea.

This connection between a stock problem and Kadane is one of the
prettiest little jokes in interview DSA. Once you see it, you know
that "max profit (1 transaction)" is just a renamed array problem.

The more advanced stock problems (multiple transactions, cooldowns,
fees) are DP. They each maintain state for "do I currently hold
stock?" and possibly "how many transactions left?". The single-pass
trick generalizes via DP recurrences. We tackle those in Step 16.
''',
        "confusion_notes": [
            {
                "question": "Why do we update `best` *before* updating `min_so_far`?",
                "answer": r'''
Because the trade we are scoring is "buy at some earlier day,
sell today." For today's profit calculation, the buy day must be
**strictly before** today, not today itself.

If we updated `min_so_far` first, then computed profit, we might
end up "buying" and "selling" on the same day — which is not
allowed (and would always yield a profit of zero anyway). So we
compute `price - min_so_far` first, using the minimum from
*previous* days, and only then fold today's price into
`min_so_far` for tomorrow's calculation.

Walk through `prices = [3, 1, 4]`:

- Start: `min_so_far = 3, best = 0`.
- Day 1 (`price = 1`): profit if sold today = `1 - 3 = -2`. Not
  better than 0, so `best` stays 0. Update `min_so_far = 1`.
- Day 2 (`price = 4`): profit if sold today = `4 - 1 = 3`. New
  best! `best = 3`. Update `min_so_far` stays at 1.

Final: `best = 3`. Correct.

If we flipped the order, on day 1 we would first set
`min_so_far = 1`, then compute profit `1 - 1 = 0` — same answer
in this case but a coincidence. For sneakier inputs it matters.

In Kadane and other "buy-now sell-later" problems, the rule of
thumb is: **decide what you can do today using only past
information; *then* update the past with today's information**.
This is the discrete version of "you can only act on what you
already know."
''',
            },
            {
                "question": "Why initialize `best = 0` instead of `min_so_far - some_price`?",
                "answer": r'''
Because the problem allows you to **not trade at all**, and the
profit of doing nothing is exactly 0.

If no buy-sell pair produces a positive profit (for example, a
monotonically decreasing price array), the answer is 0 — we
simply choose not to trade. Initializing `best = 0` reflects
this floor.

For `prices = [5, 4, 3, 2, 1]`, every day is worse than the
previous, so no trade is profitable. Our algorithm tracks
`min_so_far` going down each day, and the profit each day is
either 0 or negative. Since the `if` guard `if price - min_so_far
> best` never fires, `best` remains 0. Correct.

If the problem instead said "you must execute exactly one buy
and one sell," the initialization would be different —
`float('-inf')` or some other sentinel — and we would need to
handle the "always loses money" case explicitly.

The general lesson: the initial value of a running scalar
encodes a baseline assumption about what "no work has been done"
should return. Choose it based on the problem's allowed actions.
''',
            },
            {
                "question": "How is this 'Kadane in disguise'?",
                "answer": r'''
Because the max profit equals the **maximum subarray sum of the
consecutive-day differences**.

Let `diffs[i] = prices[i] - prices[i - 1]`. Then the profit from
buying on day `i` and selling on day `j` equals the sum of
`diffs[i + 1]` through `diffs[j]` — a contiguous range of the
diffs array. So "find the best buy-sell profit" is exactly
"find the maximum subarray sum of diffs," which is Kadane's
problem.

To see this, walk through `prices = [7, 1, 5, 3, 6, 4]`:

- Diffs: `[1 - 7, 5 - 1, 3 - 5, 6 - 3, 4 - 6] = [-6, 4, -2, 3,
  -2]`.
- Maximum subarray sum of `[-6, 4, -2, 3, -2]` is `4 + (-2) + 3
  = 5`. (Kadane.)
- Buy on day 1 (price 1), sell on day 4 (price 6), profit `6 -
  1 = 5`. Same answer.

The running-min version (`min_so_far`) and the Kadane-on-diffs
version are equivalent expressions of the same observation. The
running-min is just easier to write directly because it avoids
computing the diffs array.

This is one of those little discoveries that makes you smile.
The same algorithm wearing different costumes.
''',
            },
            {
                "question": "What if I want the actual buy day and sell day?",
                "answer": r'''
Track two extra scalars: `min_day` (the index where `min_so_far`
was achieved) and `best_pair` (a tuple of buy and sell indices).

```python
def max_profit_with_days(prices):
    min_so_far = prices[0]
    min_day = 0
    best = 0
    best_pair = (0, 0)
    for i in range(1, len(prices)):
        if prices[i] - min_so_far > best:
            best = prices[i] - min_so_far
            best_pair = (min_day, i)
        if prices[i] < min_so_far:
            min_so_far = prices[i]
            min_day = i
    return best, best_pair
```

Two new scalars, same *O(n)* time. We update `min_day` only when
`min_so_far` itself changes, and we update `best_pair` only when
we improve the best profit. The buy day is the `min_day` at the
moment of the improvement, the sell day is the current `i`.

This is a common interview follow-up: "great, now also return
the days." If you have written the basic algorithm cleanly, the
extension is mechanical.

A subtle point: when there are ties (multiple days achieve the
same min), our algorithm keeps the **earliest** of them as
`min_day` (because we use strict `<` for the update). If the
problem instead asked for the *latest* min day, switch to `<=`.
Read the problem carefully.
''',
            },
        ],
        "summary": r'''
**Pattern**: walk once carrying min-so-far and best-so-far.

**Lesson**: every "buy low, sell high" problem reduces to "at each
point, what is the best partner from the past?". A scan with a
running scalar gives the answer.

**Recognize next time**: any optimization problem where you need
"the best earlier value" as you walk forward.
''',
    },
    {
        "id": "longest-consecutive-sequence",
        "title": "Longest Consecutive Sequence",
        "step_id": 3,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["arrays", "hashing", "sets"],
        "what_this_teaches": (
            "How an amortized argument turns a *nested* loop into an "
            "*O(n)* algorithm. The 'extend only from run-starters' "
            "trick is one of the prettiest amortization arguments in "
            "beginner DSA."
        ),
        "pattern": "Hash all values; only extend forward from elements that have no predecessor.",
        "prerequisite_lessons": ["arrays", "hashing"],
        "prerequisite_problems": ["two-sum"],
        "next_problems": [
            "longest-subarray-zero-sum",
            "longest-subarray-with-sum-k",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 3 (Medium Arrays)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 128 — Longest Consecutive Sequence",
                "url": "https://leetcode.com/problems/longest-consecutive-sequence/",
            },
        ],
        "understanding": r'''
Given an unsorted array of integers, return the length of the
longest **consecutive** sequence of values present in the array. The
values do not need to be in order in the array — they just need to
exist.

Example: `[100, 4, 200, 1, 3, 2]` → consecutive sequence is
`[1, 2, 3, 4]`, length 4. (The array also contains 100 and 200 but
those don't extend any run.)

The problem looks like a sorting problem (sort and walk), but the
real prize is doing it in *O(n)* without sorting.
''',
        "brute_force": {
            "explanation": r'''
**Sort then walk**: sort the array, then walk linearly counting runs
of consecutive integers. *O(n log n)* time due to sort. Simple and
arguably the right answer when the array is small.

```python
arr = sorted(set(arr))
best = current = 1
for i in range(1, len(arr)):
    if arr[i] == arr[i - 1] + 1:
        current += 1
        best = max(best, current)
    else:
        current = 1
```

We can do better. *O(n)* with a hash set.
''',
            "code": r'''def longest_consec_sort(arr: list[int]) -> int:
    if not arr:
        return 0
    arr = sorted(set(arr))
    best = current = 1
    for i in range(1, len(arr)):
        if arr[i] == arr[i - 1] + 1:
            current += 1
            best = max(best, current)
        else:
            current = 1
    return best
''',
            "complexity": "**Time**: *O(n log n)*. **Space**: *O(n)*.",
        },
        "thought_process": r'''
The clever *O(n)* algorithm uses a set and a single observation:
**every consecutive sequence has a unique starting point**, which is
the smallest number in it. A number `x` is a starting point if and
only if `x - 1` is **not** in the set.

So we walk through every element. For each element that is a
starting point (i.e., `x - 1` is missing), we extend forward by
checking `x + 1`, `x + 2`, ... in the set until we run out. We
record the length.

The trick is that we only spend time extending when we are at a
starting point. Every consecutive run is extended exactly once. So
the total work is *O(n)*, not *O(n²)* — even though there is a
nested `while` loop.

Read the previous paragraph again. It is subtle. The total work
inside the inner `while` loop is bounded by the total length of all
consecutive runs, which is at most `n`. So the inner loop adds *O(n)*
across the whole algorithm, not *O(n)* per outer iteration.

This is one of those clever amortized arguments that interviewers
love to see explained out loud.
''',
        "optimized": {
            "explanation": r'''
Put all elements in a set. For each element that starts a run
(no `x - 1` in the set), extend the run forward and track the
longest.
''',
            "code": r'''def longest_consecutive(arr: list[int]) -> int:
    s = set(arr)
    best = 0
    for x in s:
        # Only START extending from values that are run-starters.
        # A run-starter has no predecessor x - 1 in the set.
        if x - 1 not in s:
            length = 1
            current = x
            # Extend forward as long as the next value exists.
            while (current + 1) in s:
                current += 1
                length += 1
            if length > best:
                best = length
    return best
''',
            "complexity": (
                "**Time**: *O(n)* amortized. **Space**: *O(n)* for "
                "the set."
            ),
        },
        "deep_concept": r'''
The "skip non-starting values" optimization is a beautiful instance
of an **amortization argument**. We have a nested loop that *looks*
quadratic but is actually linear because each consecutive run is
extended exactly once.

This pattern recurs:

- **Number of distinct islands** in a 2D grid — flood-fill starts
  only at "fresh" cells, so the total work is bounded by grid size.
- **Visiting nodes in a graph** during BFS/DFS — each node is
  visited once, even though we have an outer "for each node" loop.
- **Sliding window** — each element enters and exits the window
  exactly once.

Whenever you see a nested loop that you think might secretly be
linear, ask: "is there an invariant that bounds the inner work
globally?". If yes, you have a smart algorithm masquerading as a
slow one.

A variation: instead of "longest consecutive run", count "how many
consecutive runs of length ≥ k". Same set scaffolding, different
bookkeeping.
''',
        "confusion_notes": [
            {
                "question": "Why is the algorithm `O(n)` even though there's a `while` inside the `for`?",
                "answer": r'''
Because the inner `while` loop is bounded **globally**, not
per-iteration.

The `for x in s` loop iterates `n` times. Inside, we only enter
the `while` extension when `x - 1` is **not** in the set — i.e.,
when `x` is the start of a consecutive run. The `while` then
walks every element of that run, stopping at the end.

Crucially, each value in the set belongs to **exactly one**
consecutive run, and we only extend from each run's starter. So
across the entire outer loop, the total work inside `while` is
bounded by the total length of all consecutive runs, which is at
most `n`. The outer loop adds another `n` constant-time
membership checks. Total: `O(n)`.

This is called an **amortized analysis** — the worst case of any
single inner iteration could be `n`, but the *average* (amortized
across the outer loop) is constant. The argument relies on the
fact that we never extend the same run twice.

If we removed the `if x - 1 not in s` guard and extended from
every element, the algorithm would be `O(n²)` because each
run of length `k` would be extended `k` times. The guard is what
turns the algorithm linear.

This style of argument — "nested loop, but the inner work is
globally bounded" — shows up in many places: sliding window
(each element enters and leaves the window once), graph
traversal (each vertex visited once), monotonic stack (each
element pushed and popped once). Once you can spot it, you stop
being scared of nested loops in linear algorithms.
''',
            },
            {
                "question": "Why does sorting also work, and when should I prefer it?",
                "answer": r'''
Sorting works because, after sorting, consecutive values land
adjacent. Then a single linear scan counts run lengths:

```python
def longest_sort(arr):
    if not arr:
        return 0
    arr = sorted(set(arr))
    best = current = 1
    for i in range(1, len(arr)):
        if arr[i] == arr[i - 1] + 1:
            current += 1
            best = max(best, current)
        else:
            current = 1
    return best
```

This is *O(n log n)* due to the sort, *O(n)* for the scan, and
*O(n)* extra memory for the set + sorted list. Compare with the
hash-set version: *O(n)* time, *O(n)* memory.

When to prefer sorting:

- When `n` is small and constants matter more than asymptotics.
- When you do not have a hash set available (rare in modern
  languages).
- When you also need other order-dependent queries on the data
  (e.g., quantiles).

When to prefer hashing:

- When `n` is large and you want `O(n)`.
- When sorting would destroy a useful order in the original
  array.
- When the values do not have a natural total order (rare for
  integers, but matters for custom objects).

For LeetCode 128 specifically, the problem explicitly requires
`O(n)`, so hashing is the canonical answer. For curriculum
practice, knowing both is useful.
''',
            },
            {
                "question": "Why use a set and not the original array directly?",
                "answer": r'''
For two reasons: **O(1) membership tests** and **automatic
deduplication**.

If we kept the original list, the test `x - 1 in arr` would be
`O(n)` — Python has to scan the entire list to check. Doing that
inside a loop would push the algorithm back to `O(n²)`. A set
gives us `O(1)` lookups, restoring the linear total time.

The set also collapses duplicates. If the input is `[1, 2, 2, 3,
4]`, the set is `{1, 2, 3, 4}` and the algorithm sees only one
copy of each value. Duplicates in the input do not extend a run
(`2, 2` is not a "consecutive sequence of length 2" by the
problem's definition; `2, 3` is). The set removes them
automatically, so we never accidentally count `2` twice.

The set is also a **constant-cost** data structure to build (`O(n)`)
and a tiny amount of memory (`O(n)` words). The trade is well
worth the speedup.

In general, whenever you want fast "have I seen this value?"
queries and the values do not need to be ordered, reach for a
set. The Two Sum problem uses the same instinct.
''',
            },
            {
                "question": "What if the array can have duplicates that should count?",
                "answer": r'''
Then the problem statement changes, and the algorithm changes
slightly too.

The standard "Longest Consecutive Sequence" problem treats
duplicates as the same value. `[1, 2, 2, 3]` has the consecutive
sequence `1, 2, 3` of length 3.

If a variant said "the **count** of values forming the
consecutive run, with duplicates allowed," the answer for `[1,
2, 2, 3]` would still be 4 — the sequence `1, 2, 2, 3` is
"consecutive with duplicates." But this is unusual phrasing.

The way to handle a variant: read the problem carefully and ask
yourself, *"does duplicates count as extending the run, or not?"*

If duplicates do **not** count (standard LC 128), use a set.
That's our algorithm.

If duplicates **do** count, sort the array (keeping duplicates),
walk it, and count "consecutive or equal." That is a slightly
different problem.

The general lesson: never write code until you have nailed down
the edge-case rules. Two minutes of "what about duplicates? what
about negatives? what about empty?" up front saves twenty
minutes of debugging.
''',
            },
        ],
        "summary": r'''
**Pattern**: hash set + only-extend-from-starting-points.

**Lesson**: a nested loop is not always quadratic. Find the global
invariant that bounds inner work.

**Recognize next time**: "longest sequence of consecutive things"
without the array being sorted. The set lookup is the magic
ingredient.
''',
    },
    {
        "id": "majority-element",
        "title": "Majority Element (> N/2 times) — Boyer-Moore",
        "step_id": 3,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["arrays", "boyer-moore", "voting"],
        "what_this_teaches": (
            "**Cancellation arguments** as an algorithmic technique. "
            "Boyer-Moore vote pairs off non-matching elements; the "
            "majority's surplus survives because no other group can "
            "out-vote it. A beautiful *O(1)* memory trick that "
            "generalizes to 'more than N/K' problems."
        ),
        "pattern": "Maintain a candidate and a vote count; cancellations preserve the true majority.",
        "prerequisite_lessons": ["arrays", "hashing"],
        "prerequisite_problems": ["count-frequencies", "single-number"],
        "next_problems": [
            "majority-element-n3",
            "single-number-iii",
            "kth-largest",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 3 (Medium Arrays)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 169 — Majority Element",
                "url": "https://leetcode.com/problems/majority-element/",
            },
        ],
        "understanding": r'''
Given an array of integers, return the **majority element** — the
one that appears **more than N/2 times**. The problem guarantees one
exists.

Example: `[3, 2, 3]` → majority is 3 (appears twice in a length-3
array, which is more than 3/2).

The hashing solution is trivial. The optimized solution is one of
the most elegant tricks in algorithms: **Boyer-Moore voting**. It
finds the majority element in *O(n)* time and *O(1)* space — no
sorting, no hashing.
''',
        "brute_force": {
            "explanation": r'''
**Count with a hash**: walk once, increment a counter for each
value, then return the key with count > N/2. *O(n)* time, *O(n)*
space.

The Boyer-Moore version achieves *O(1)* space. That is the
distinguishing trick.
''',
            "code": r'''def majority_hash(arr: list[int]) -> int:
    from collections import Counter
    counts = Counter(arr)
    n = len(arr)
    for k, v in counts.items():
        if v > n // 2:
            return k
    raise ValueError("no majority element")
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(n)*.",
        },
        "thought_process": r'''
Boyer-Moore voting is the kind of algorithm that feels like a magic
trick. Imagine a knockout tournament where each element of the
array "votes" — but every time two different values appear together,
they cancel each other out. The majority element survives the
cancellations because it has more votes than everyone else
combined.

Concretely we maintain a **candidate** and a **vote count**. We
walk through the array:

- If `count == 0`, we adopt the current element as our new
  candidate and set count to 1.
- If the current element matches the candidate, increment count.
- If it does not match, decrement count.

At the end, the candidate is the majority element (assuming one
exists). If you are not sure a majority exists, do a second pass to
verify.

**Why does this work?** Picture the votes as a battle: matching
votes increase the candidate's lead, non-matching votes decrease
it. Since the majority appears more than `N/2` times and everyone
else combined appears less than `N/2` times, the majority's lead
cannot be wiped out by the combined opposition. The candidate at
the end is guaranteed to be the majority.

This argument is one of those *aha* moments. Don't be surprised if
it takes a few rereads. The leap of faith — that the running
candidate, despite being overwritten multiple times, lands on the
right answer — is part of the algorithm's charm.
''',
        "optimized": {
            "explanation": r'''
Boyer-Moore Majority Vote. One pass, two scalars.
''',
            "code": r'''def majority_element(arr: list[int]) -> int:
    candidate = None
    count = 0
    # First pass: identify the candidate.
    for x in arr:
        if count == 0:
            candidate = x
            count = 1
        elif x == candidate:
            count += 1
        else:
            count -= 1
    # If a majority is guaranteed to exist, candidate IS the answer.
    # Otherwise verify with a second pass:
    # if arr.count(candidate) > len(arr) // 2: return candidate else None
    return candidate  # type: ignore[return-value]
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "deep_concept": r'''
The Boyer-Moore voting algorithm generalizes to **finding the K
elements that appear more than N/(K+1) times**. The classic case
is `K = 2` ("more than N/3 times"), which is in this curriculum's
hard section: there can be at most two such elements. We maintain
two candidates and two counters instead of one. The generalization
to general `K` is called the **Boyer-Moore generalized vote**.

The underlying principle — "pair up opposing votes and let the
majority survive" — is a beautiful instance of cancellation
arguments. We saw similar cancellation in the XOR-based "single
number" problem. Cancellation is a recurring algorithmic idea: if
two things "destroy" each other when paired, the surplus survives.
''',
        "confusion_notes": [
            {
                "question": "How can we possibly find the majority by only remembering one candidate at a time?",
                "answer": r'''
This is the part that feels like magic. Let me try to make it
intuitive.

Imagine the majority element as a team with a numerical
*advantage*: it has more than `N/2` votes, while every other
element combined has fewer than `N/2` votes. Now imagine every
"non-majority" vote and every "majority" vote pairing off and
canceling each other.

Because the majority has the surplus, after every possible
pairing, the surplus remaining is still majority votes. The
"count" can drop to 0 only after a non-majority value paired
with a majority value — and at that point, all the non-majority
votes have been exhausted (since the non-majority side started
smaller). Every later majority vote can no longer be canceled,
so eventually the algorithm settles on the majority candidate.

A second framing: think of `count` as the **net lead** that the
current `candidate` has against the rest of the array seen so
far. When a vote matches, lead increases. When it does not,
lead decreases. When lead reaches 0, the candidate is "deposed"
and the next element becomes the new tentative leader.

Because the majority outnumbers everyone combined, even in the
worst possible interleaving the final candidate will be the
true majority. The proof is a careful induction; the intuition is
"surplus survives cancellation."

If you are still uneasy, run the algorithm by hand on `[3, 3, 4,
2, 4, 4, 2, 4, 4]` and watch `count` rise and fall. The candidate
flips around a few times, but ends on 4 — the true majority.
''',
            },
            {
                "question": "What if no majority element actually exists?",
                "answer": r'''
The algorithm still returns *some* candidate, but it is **not
guaranteed to be the majority**. You need a second pass to
verify.

If no element appears more than `N/2` times, the cancellations
do not have a clear winner. The candidate at the end of the loop
could be any element. To handle this, we run a verification
pass:

```python
def majority(arr):
    candidate, count = None, 0
    for x in arr:
        if count == 0:
            candidate = x
        if x == candidate:
            count += 1
        else:
            count -= 1
    # Verify (only needed if majority is not guaranteed).
    if arr.count(candidate) > len(arr) // 2:
        return candidate
    return None
```

The verification is *O(n)* and uses *O(1)* extra space, so the
total is still *O(n)* time and *O(1)* memory. If the problem
*guarantees* a majority exists (as LeetCode 169 does), the
verification can be skipped.

In interview settings, always state your assumption out loud:
"Assuming a majority exists, the candidate from the first pass
is the answer. If not, I would add a verification pass."
''',
            },
            {
                "question": "Why is `count == 0` the trigger to switch candidates?",
                "answer": r'''
Because `count == 0` means *"the current candidate's lead has
been completely canceled — they are no longer a contender."*
When the lead is zero, we have no reason to keep tracking the
current candidate, so we let the next element take over.

Walk through `[1, 2, 1, 2, 1, 3, 1]`:

- `i = 0, x = 1`: `count = 0`, so `candidate = 1`. `x ==
  candidate`, so `count = 1`.
- `i = 1, x = 2`: `x != candidate`, so `count = 0`. After:
  `count = 0` triggers the "switch on the *next* iteration"
  state, but actually we wait until the next element to
  re-anoint.
- `i = 2, x = 1`: `count = 0`, so `candidate = 1`. `x ==
  candidate`, so `count = 1`.
- ... and so on.

The order inside the loop matters: check `count == 0` and
re-anoint *before* the match check. Otherwise on the iteration
that makes `count` drop to 0, we would also try to re-anoint with
the wrong element.

This dance — "if lead is exhausted, accept the new arrival as
the next contender" — is the heart of the algorithm. It works
because the *true* majority's surplus cannot be canceled out;
the algorithm will eventually pivot back to it as the cancelled
pairs exhaust the non-majority votes.
''',
            },
            {
                "question": "How does this generalize to 'more than N/3 times'?",
                "answer": r'''
At most **two** elements can appear more than `N/3` times. So
we maintain **two candidates and two counters**, and pair off
non-matching votes against *both* candidates simultaneously.

```python
def majority_n3(arr):
    c1 = c2 = None
    count1 = count2 = 0
    for x in arr:
        if c1 == x:
            count1 += 1
        elif c2 == x:
            count2 += 1
        elif count1 == 0:
            c1, count1 = x, 1
        elif count2 == 0:
            c2, count2 = x, 1
        else:
            count1 -= 1
            count2 -= 1
    # Verify both candidates (two-thirds majority is not guaranteed
    # in general).
    return [c for c in (c1, c2) if c is not None and arr.count(c) > len(arr) // 3]
```

This is the **generalized Boyer-Moore vote**. It generalizes
further: to find elements appearing more than `N/(K+1)` times,
maintain `K` candidates and counters. The first pass identifies
the candidates; a second verification pass filters out anything
that does not actually meet the threshold.

The reason at most two elements can appear more than `N/3` times:
three such elements would each contribute more than `N/3`,
summing to more than `N`. Contradiction.

The general principle, again: cancellation arguments preserve
the surplus. The trick is to pair the right number of opposing
votes at a time.
''',
            },
        ],
        "summary": r'''
**Pattern**: Boyer-Moore vote — pair off non-matching elements;
the majority survives.

**Lesson**: certain problems that *look* like they need a hash can
actually be solved in *O(1)* space via cancellation arguments.

**Recognize next time**: any "appears more than N/K times" problem.
Boyer-Moore voting generalizes to K candidates.
''',
    },
    {
        "id": "merge-overlapping-intervals",
        "title": "Merge Overlapping Intervals",
        "step_id": 3,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["arrays", "intervals", "sorting", "greedy"],
        "what_this_teaches": (
            "The 'sort by start, sweep once' pattern that unlocks the "
            "entire interval-problem family. Merging, insertion, "
            "counting overlaps, finding meeting rooms — all are "
            "variations on this same sort-and-sweep skeleton."
        ),
        "pattern": "Sort intervals by start time; sweep once, extending the last merged interval when overlap.",
        "prerequisite_lessons": ["arrays", "sorting"],
        "prerequisite_problems": ["merge-sort"],
        "next_problems": [
            "insert-intervals",
            "non-overlapping-intervals",
            "n-meetings",
            "min-platforms",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 3 (Hard Arrays)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 56 — Merge Intervals",
                "url": "https://leetcode.com/problems/merge-intervals/",
            },
        ],
        "understanding": r'''
Given a list of intervals `[start, end]`, merge any that overlap.
Two intervals `[a, b]` and `[c, d]` overlap if `c <= b` (assuming
`a <= c`). Output the list of merged intervals.

Example: `[[1, 3], [2, 6], [8, 10], [15, 18]]` → `[[1, 6], [8, 10],
[15, 18]]`. The first two overlap and merge into `[1, 6]`.

This is the canonical "sort first" problem. Sorting the intervals
by start time is the unlock.
''',
        "brute_force": {
            "explanation": r'''
You can repeatedly look for any pair of overlapping intervals, merge
them, and repeat until no overlaps remain. That is *O(n² log n)* or
worse. Painful and unnecessary.

The "sort by start time, walk once" approach is the textbook answer
and is fast and clean.
''',
            "code": r'''def merge_intervals_brute(intervals: list[list[int]]) -> list[list[int]]:
    # Naive: keep merging the first overlapping pair until stable.
    out = [list(iv) for iv in intervals]
    changed = True
    while changed:
        changed = False
        for i in range(len(out)):
            for j in range(i + 1, len(out)):
                a, b = out[i]
                c, d = out[j]
                # Overlap test that does not assume ordering.
                if a <= d and c <= b:
                    out[i] = [min(a, c), max(b, d)]
                    out.pop(j)
                    changed = True
                    break
            if changed:
                break
    return sorted(out)
''',
            "complexity": (
                "**Time**: poor — *O(n³)* or worse in pathological "
                "cases. **Space**: *O(n)*."
            ),
        },
        "thought_process": r'''
The key insight: **if we sort intervals by start time**, then for
any pair of overlapping intervals, the one with the smaller start
comes first. So we can walk through the sorted list and, for each
new interval, only need to compare it with the **most recent
merged interval** in our output. If it overlaps, we extend the
merged interval's end. If it does not, we append it as a new
interval.

That observation reduces the problem to a single pass after sorting.

Why? Because once intervals are sorted by start, an interval cannot
overlap with anyone that comes after the next one without also
overlapping the next one. Overlaps are "transitive forward" — if
A overlaps B and B overlaps C, then the merge so far includes a
single chunk containing all three.

The runtime is dominated by the sort: *O(n log n)*. The walk is
*O(n)*. The space is *O(n)* for the output.
''',
        "optimized": {
            "explanation": r'''
Sort by start. Walk through; either extend the last output interval
or append a new one.
''',
            "code": r'''def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    # Sort by start time. If starts are equal, sort by end (does not
    # affect correctness here, but tidier).
    intervals = sorted(intervals, key=lambda iv: (iv[0], iv[1]))
    merged: list[list[int]] = [list(intervals[0])]
    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            # The new interval overlaps with the last merged one.
            # Extend the last one's end (keep the maximum).
            merged[-1][1] = max(last_end, end)
        else:
            # No overlap; this interval starts after the last one ends.
            merged.append([start, end])
    return merged
''',
            "complexity": (
                "**Time**: *O(n log n)* due to sorting. **Space**: "
                "*O(n)* for the output."
            ),
        },
        "deep_concept": r'''
The "sort by start time, then walk" approach is the **interval
processing pattern**. It shows up in many shapes:

- **Insert interval** — given sorted non-overlapping intervals,
  insert a new one and re-merge. The single new interval keeps the
  algorithm *O(n)*.
- **Meeting rooms / number of platforms** — count concurrent
  intervals. Sort start times and end times separately, then sweep.
- **Skyline problem** — events at each interval's start and end,
  sorted, then swept with a priority queue.
- **Non-overlapping intervals** — sort by end time and greedily
  keep intervals that fit. (The greedy choice "earliest end first"
  is what unlocks the problem.)

The unifying idea: **time is one-dimensional and orderable**. Any
problem about ranges, durations, or schedules tends to benefit from
sorting along the time axis and sweeping forward.

A second deep idea is the **sort key choice**. For merging, we sort
by **start**. For non-overlapping, we sort by **end**. Why? Because
the optimal greedy choice depends on what you want to keep. The
start-sort lets us decide "does this overlap the previous?" without
backtracking; the end-sort lets us decide "what is the latest
interval I can finish to leave room for the most future ones?".
''',
        "confusion_notes": [
            {
                "question": "Why is `start <= last_end` the right overlap test?",
                "answer": r'''
Because two intervals overlap (or just touch) exactly when one
starts at or before the other ends.

For two intervals `[a, b]` and `[c, d]` with `a <= c` (which is
true after sorting by start time), they overlap if and only if
`c <= b`. If `c > b`, the second interval starts strictly after
the first ends, so they are disjoint.

Whether `c == b` should count as "overlapping" depends on
problem conventions. Most problems treat touching as merging
(`[1, 4]` and `[4, 6]` merge into `[1, 6]`). A few problems
distinguish "touching" from "overlapping" — read the statement.

Our condition `start <= last_end` covers both true overlaps and
touching. If the problem instead used strict overlap, change to
`start < last_end`.

After sorting by start, the overlap question becomes a single
constant-time check against the last merged interval's end. No
need to check against all earlier intervals — because they are
already merged into the last one, the last one's end is the
"deadline" for any new interval.
''',
            },
            {
                "question": "Why use `max(last_end, end)` when extending? Couldn't I just take `end`?",
                "answer": r'''
Because the new interval might be **entirely contained** within
the last merged interval, in which case its end is *smaller*
than the existing end.

Consider `[1, 10]` followed by `[2, 5]`. Both start within `[1,
10]`, and the second is fully contained. After merging, the
result should still be `[1, 10]`, not `[1, 5]`. If we wrote
`merged[-1][1] = end`, we would shrink the merged interval —
wrong.

`max(last_end, end)` takes the larger of the two ends, which
correctly handles both cases:

- New interval extends beyond last: pick the new end.
- New interval is contained within last: pick the old end.

This is a small but important detail. The naive write
`merged[-1][1] = end` works on most test cases but quietly
breaks on contained intervals. The `max` makes the algorithm
robust to any overlap configuration.

The general principle: when you "merge" or "extend" a range,
always think *"what is the maximum of the old and new
boundary?"* rather than blindly overwriting.
''',
            },
            {
                "question": "Why sort by start time, not by end time?",
                "answer": r'''
Because sorting by start time makes the "is this the next
interval I should merge with?" decision trivial: it is always
the most recently merged interval. Sorting by end would require
more bookkeeping.

After sorting by start, every new interval `(start, end)` has a
`start` value at or after every previous start. So if its
`start` is at or before `merged[-1][1]`, it overlaps with the
last merged interval. If not, it cannot overlap with any earlier
interval either (those have even smaller ends already swallowed
by the last merged one).

This monotonicity argument is what gives the algorithm its
one-pass simplicity. With unsorted intervals, you would need to
check overlap against every previous merged result, which
could be *O(n)* per new interval and *O(n²)* total.

A separate problem — "the maximum number of non-overlapping
intervals you can keep" — is best solved by sorting by **end
time** instead. Why? Because the greedy choice "pick the
earliest-finishing interval that does not overlap your last
pick" lets you maximize remaining room for future picks.
Different question, different sort key.

The lesson: always ask, *"what comparison drives my greedy
choice, and what sort key makes that comparison cheap?"*. Then
sort by that key.
''',
            },
            {
                "question": "What's the time and space complexity?",
                "answer": r'''
**Time**: *O(n log n)* — dominated by the sort. The sweep itself
is *O(n)*, but it sits below the sort cost in the big-O.

**Space**: *O(n)* for the output list of merged intervals. If
the problem allows you to mutate the input in place, the
auxiliary space can shrink to *O(1)* extra (beyond the input
storage), but the typical implementation allocates a new list.

Python's `sorted` is Timsort, which is `O(n log n)` worst case
and stable. The merge sweep needs only a single pass, with one
comparison and one constant-time mutation per element. Together
that gives *O(n log n)* time and *O(n)* output memory — which
is the optimal for this problem, since you cannot decide overlaps
without examining each interval at least once and sorting them.

If you somehow had the intervals pre-sorted by start (or your
input format guaranteed it), you could skip the sort entirely
and run the sweep in *O(n)*. That is a real consideration for
streaming algorithms or when the data source already provides
sorted ordering.

Practical tip: if your interval data structure is a list of
lists `[[a, b], ...]`, Python's default sort sorts
lexicographically — first by `a`, then by `b`. That happens to
be exactly the sort we want, so `sorted(intervals)` works.
Explicit `sorted(intervals, key=lambda x: x[0])` is clearer if
you only want to sort by start.
''',
            },
        ],
        "summary": r'''
**Pattern**: sort by start, sweep once, merge or append.

**Lesson**: interval problems are sort-and-sweep problems in
disguise. The sort key matters — pick it for the question you are
asking.

**Recognize next time**: any problem about merging, scheduling, or
counting overlapping intervals. Always start by sorting.
''',
    },
]
