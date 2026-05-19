"""Step 2 extras — the two recursive sort exercises."""
from __future__ import annotations

_STRIVER_SHEET = {
    "label": "Striver's A2Z DSA Course Sheet",
    "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
}


PROBLEMS: list[dict] = [
    {
        "id": "recursive-bubble-sort",
        "title": "Recursive Bubble Sort",
        "step_id": 2,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["sorting", "recursion", "fundamentals"],
        "what_this_teaches": (
            "How to convert an iterative algorithm into recursion. "
            "The outer loop becomes 'recurse on a smaller suffix', "
            "the inner loop stays as is — a useful pattern when you "
            "want to think recursively about sorting."
        ),
        "pattern": "Recurse on smaller suffix; one pass per recursive call.",
        "prerequisite_lessons": ["recursion", "sorting"],
        "prerequisite_problems": ["bubble-sort", "factorial-of-n"],
        "next_problems": ["recursive-insertion-sort", "merge-sort"],
        "resources": [
            _STRIVER_SHEET,
            {
                "label": "GeeksforGeeks — Recursive Bubble Sort",
                "url": "https://www.geeksforgeeks.org/recursive-bubble-sort/",
            },
        ],
        "understanding": r'''
The iterative bubble sort runs `n - 1` passes, each bubbling the
largest unsorted element to its final position. Recursively, the
same algorithm reads:

> *"Do one pass to bubble the maximum to the end; then sort the
> array minus its last element."*

```python
def bubble_sort_rec(arr, n=None):
    if n is None:
        n = len(arr)
    if n <= 1:
        return                          # base case: 0 or 1 element is sorted
    for j in range(n - 1):
        if arr[j] > arr[j + 1]:
            arr[j], arr[j + 1] = arr[j + 1], arr[j]
    bubble_sort_rec(arr, n - 1)         # smaller subarray
```

After one pass, `arr[n - 1]` is correct. The recursion handles
`arr[0..n - 2]`.

This is a textbook example of "iterative → recursive conversion":
the outer `for end in range(n - 1, 0, -1)` becomes recursion on a
shrinking `n`. The inner adjacent-swap loop is unchanged.

Time *O(n²)* (same as iterative). Space *O(n)* for the call
stack (worse than iterative *O(1)*). Use this version for the
mental exercise, not because it is faster.
''',
        "summary": r'''
**Pattern**: convert outer loop into recursion on a smaller
subarray.

**Lesson**: every iterative algorithm has a recursive twin —
sometimes useful for clarity, but typically worse on stack space.

**Recognize next time**: "rewrite this as recursion" exercises.
The outer loop becomes the recursion driver.
''',
    },
    {
        "id": "recursive-insertion-sort",
        "title": "Recursive Insertion Sort",
        "step_id": 2,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["sorting", "recursion", "fundamentals"],
        "what_this_teaches": (
            "Same conversion pattern as recursive bubble sort, but "
            "with the insertion-sort inner logic. Practice flipping "
            "between iteration and recursion."
        ),
        "pattern": "Recurse on prefix of size i; insert arr[i] into sorted prefix.",
        "prerequisite_lessons": ["recursion", "sorting"],
        "prerequisite_problems": ["insertion-sort", "recursive-bubble-sort"],
        "next_problems": ["merge-sort", "quick-sort"],
        "resources": [
            _STRIVER_SHEET,
            {
                "label": "GeeksforGeeks — Recursive Insertion Sort",
                "url": "https://www.geeksforgeeks.org/recursive-insertion-sort/",
            },
        ],
        "understanding": r'''
The iterative insertion sort processes index `i` from 1 to `n -
1`, inserting `arr[i]` into the sorted prefix `arr[0..i - 1]`.
Recursively:

> *"Sort `arr[0..i - 1]` recursively, then insert `arr[i]` into
> place."*

```python
def insertion_sort_rec(arr, i=1):
    if i >= len(arr):
        return                          # base case
    insertion_sort_rec(arr, i + 1 if False else i)  # see below
    # The cleaner way:

def insertion_sort_rec(arr, n=None):
    if n is None:
        n = len(arr)
    if n <= 1:
        return
    insertion_sort_rec(arr, n - 1)      # sort arr[0..n-2] first
    # Now insert arr[n-1] into the sorted prefix.
    last = arr[n - 1]
    j = n - 2
    while j >= 0 and arr[j] > last:
        arr[j + 1] = arr[j]
        j -= 1
    arr[j + 1] = last
```

The recursive call sorts the prefix first; then the body inserts
the new element. The "insert" step is exactly the same shift-and-
drop pattern as iterative insertion sort.

Time *O(n²)*. Stack space *O(n)*.

Note the **recurse first, then act** ordering. The iterative
version walks left to right; the recursive version walks all the
way down, then builds up. The end result is identical, but the
order of operations is the reverse.

This dichotomy — "recurse first" vs "act first" — is the same one
we covered in the Recursion chapter. Internalize it; the same
swap powers preorder/postorder tree traversals.
''',
        "summary": r'''
**Pattern**: recurse on prefix, then insert the new element.

**Lesson**: recursive insertion sort uses the "recurse first,
then act" order. The act is the slide-and-insert that the
iterative version does in its inner loop.

**Recognize next time**: rewriting an iterative sort as
recursion is mostly about choosing where the recursive call goes.
''',
    },
]
