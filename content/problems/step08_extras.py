"""Step 8 — Bit Manipulation + Advanced Maths."""
from __future__ import annotations

_SHEET = {
    "label": "Striver's A2Z DSA Course Sheet",
    "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
}


def _lc(num: int, slug: str) -> dict:
    return {
        "label": f"LeetCode {num} — {slug.replace('-', ' ').title()}",
        "url": f"https://leetcode.com/problems/{slug}/",
    }


PROBLEMS: list[dict] = [
    {
        "id": "bit-introduction",
        "title": "Introduction to Bit Manipulation (Get / Set / Clear)",
        "step_id": 8,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["bit-manipulation", "fundamentals"],
        "what_this_teaches": "The three atomic bit operations: get bit, set bit, clear bit. Every bit-manipulation algorithm is built from these.",
        "pattern": "Bit at position i is `(n >> i) & 1`. Set: `n | (1 << i)`. Clear: `n & ~(1 << i)`. Toggle: `n ^ (1 << i)`.",
        "prerequisite_lessons": [],
        "prerequisite_problems": [],
        "next_problems": ["check-odd-even-bits", "check-power-of-two", "count-set-bits"],
        "resources": [_SHEET],
        "understanding": r'''
Bits are the digits of binary. An integer in binary has bits at
positions 0 (least significant), 1, 2, ... To work with
individual bits, we use four atomic operations.

**Get the i-th bit**: `(n >> i) & 1` — shift right by i, then mask the last bit.

**Set the i-th bit** (to 1): `n | (1 << i)` — OR with a 1 at position i.

**Clear the i-th bit** (to 0): `n & ~(1 << i)` — AND with a mask that has 0 at position i and 1 elsewhere.

**Toggle the i-th bit**: `n ^ (1 << i)` — XOR with a 1 at position i.

These four are the alphabet of bit manipulation. Everything else
builds on them.
''',
        "optimized": {
            "explanation": "Implement get/set/clear/toggle.",
            "code": r'''def get_bit(n: int, i: int) -> int:
    return (n >> i) & 1

def set_bit(n: int, i: int) -> int:
    return n | (1 << i)

def clear_bit(n: int, i: int) -> int:
    return n & ~(1 << i)

def toggle_bit(n: int, i: int) -> int:
    return n ^ (1 << i)
''',
            "complexity": "**Time**: *O(1)* per operation.",
        },
        "summary": "**Pattern**: master get/set/clear/toggle — the alphabet of bit manipulation.",
    },
    {
        "id": "check-odd-even-bits",
        "title": "Check if a Number is Odd or Even Using Bits",
        "step_id": 8,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["bit-manipulation"],
        "what_this_teaches": "The last bit (bit 0) determines parity: 0 → even, 1 → odd. So `n & 1` gives parity.",
        "pattern": "`n & 1` returns 1 for odd, 0 for even.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["bit-introduction"],
        "next_problems": ["check-power-of-two"],
        "resources": [_SHEET],
        "understanding": r'''
In binary, the least significant bit (bit 0) represents 1 if
set, 0 if not. So a number's parity is determined entirely by
bit 0.

```python
def is_odd(n):
    return (n & 1) == 1
```

`n & 1` extracts bit 0. Faster than `n % 2` in many languages
(in Python the difference is negligible).
''',
        "optimized": {
            "explanation": "Mask the last bit.",
            "code": r'''def is_odd(n: int) -> bool:
    return (n & 1) == 1

def is_even(n: int) -> bool:
    return (n & 1) == 0
''',
            "complexity": "**Time**: *O(1)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: `n & 1` reads bit 0 = parity.",
    },
    {
        "id": "check-power-of-two",
        "title": "Check if a Number is a Power of Two",
        "step_id": 8,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["bit-manipulation"],
        "what_this_teaches": "Powers of two have exactly one bit set. The trick: `n & (n - 1) == 0` iff exactly one bit is set.",
        "pattern": "`n > 0 and (n & (n - 1)) == 0`.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["bit-introduction"],
        "next_problems": ["count-set-bits"],
        "resources": [_SHEET, _lc(231, "power-of-two")],
        "understanding": r'''
A power of two in binary is `100...0` — a single 1 followed by
zeros. Subtracting 1 gives `011...1` — a 0 followed by all 1s.
ANDing them gives 0.

For non-powers (more than one bit set), `n & (n - 1)` always
has at least one bit set, so it's nonzero.

So `n > 0 and (n & (n - 1)) == 0` checks power-of-two in O(1).
''',
        "optimized": {
            "explanation": "Bit trick.",
            "code": r'''def is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0
''',
            "walkthrough": r'''
The single most beautiful bit trick in CS. **One line.**
*O(1)*.

**`def is_power_of_two(n: int) -> bool:`** — Takes an integer,
returns True iff n is a power of 2 (1, 2, 4, 8, 16, ...).

**`return n > 0 and (n & (n - 1)) == 0`** — The whole
algorithm. Let me unpack the magic.

**The trick: `n & (n - 1)` clears the rightmost set bit.**

In binary:
- `n = 8 = 1000`
- `n - 1 = 7 = 0111`
- `n & (n - 1) = 1000 & 0111 = 0000 = 0`

The "1000" has exactly one set bit. Subtracting 1 turned that
bit off and turned all bits to its right ON. The AND keeps
only bits set in **both**, which is none.

Now consider a non-power:
- `n = 12 = 1100`
- `n - 1 = 11 = 1011`
- `n & (n - 1) = 1100 & 1011 = 1000 = 8`

The result is nonzero. So `n & (n - 1) == 0` exactly when `n`
has only one set bit — which is exactly when `n` is a power
of 2.

**`n > 0 and ...`** — Guards against the edge case
`n = 0`. We have `0 & -1` which in Python (with unbounded
integers) is `0`, technically satisfying the second condition.
But `0` is **not** a power of 2. So we explicitly exclude it.

(In C/Java with signed integers, `0 - 1 = -1` is all-ones,
so `0 & (-1) = 0` and the bit check passes — wrong result
without the `n > 0` guard.)

**Why does subtracting 1 do this?**

In binary subtraction, going from `...1000...0` to
`...1000...0 - 1`:
- The rightmost `0`s borrow from the rightmost `1`.
- The `1` becomes `0`.
- All the borrowed `0`s become `1`s.

So `1000 → 0111`. The rightmost set bit was "swallowed" and
all bits to its right turned on.

When we then AND `n` with `n - 1`:
- Bits **left of** the rightmost set bit: same in both (the
  borrow didn't reach them). AND keeps them.
- Rightmost set bit of n: it's 0 in `n - 1`. AND gives 0.
- Bits **right of** the rightmost set bit: they were 0 in n.
  AND gives 0 regardless.

Net effect: the rightmost set bit (and only that bit) is
cleared.

For a power of 2, there's only one set bit. Clearing it gives
0. For anything else (other than 0), there are other set bits
that survive, so the result is nonzero.

**This trick generalizes** to count set bits (Brian
Kernighan's algorithm): repeatedly do `n &= n - 1` until n
becomes 0; the number of iterations is the count of set bits.

Faster than naive bit-by-bit counting because we only iterate
once per **set** bit, not once per **possible** bit position.

**Properties:**
- **Time**: *O(1)*. One subtraction, one AND, two comparisons.
- **Space**: *O(1)*.
- **Edge cases**: 0 → False (handled by `n > 0`). 1 → True
  (one set bit, `1 & 0 = 0`). Negatives → False.

This trick is the foundation of many bit-manipulation
algorithms: counting set bits, finding the lowest set bit,
power-of-two checks, and more.
''',
            "complexity": "**Time**: *O(1)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: `n & (n - 1)` clears the rightmost set bit; equals 0 iff exactly one bit was set.",
    },
    {
        "id": "count-set-bits",
        "title": "Count the Number of Set Bits (Hamming Weight)",
        "step_id": 8,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["bit-manipulation"],
        "what_this_teaches": "Brian Kernighan's trick: `n & (n - 1)` removes the rightmost set bit; loop and count.",
        "pattern": "While n: n &= n - 1; count += 1.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["check-power-of-two"],
        "next_problems": ["set-unset-rightmost", "min-bit-flips"],
        "resources": [_SHEET, _lc(191, "number-of-1-bits")],
        "understanding": r'''
Count how many bits are set (= 1) in n's binary representation.

**Brute force**: shift and count. `O(bits)`.

**Brian Kernighan's algorithm**: `n & (n - 1)` clears the
rightmost set bit. So each iteration of the loop removes exactly
one set bit. *O(popcount)* — faster when few bits are set.

In Python, `bin(n).count('1')` is also one-liner.
''',
        "optimized": {
            "explanation": "Brian Kernighan's trick.",
            "code": r'''def count_set_bits(n: int) -> int:
    count = 0
    while n > 0:
        n &= n - 1   # clears the rightmost set bit
        count += 1
    return count

# Pythonic alternative:
def count_set_bits_py(n: int) -> int:
    return bin(n).count('1')

# Even better in Python 3.10+:
def count_set_bits_py310(n: int) -> int:
    return n.bit_count()
''',
            "walkthrough": r'''
Three versions of "count set bits." The first is the
algorithmic gold standard; the latter two are Python
shortcuts.

**Version 1: Brian Kernighan's trick**

**`def count_set_bits(n: int) -> int:`** — Takes an integer,
returns the number of `1` bits in its binary representation.

**`count = 0`** — Running counter.

**`while n > 0:`** — Loop until all bits have been processed.

**`n &= n - 1`** — Clear the **rightmost set bit**. Same
trick as power-of-two. Each iteration removes exactly one set
bit.

**`count += 1`** — One bit cleared = one bit was set.

**`return count`** — Total bits set.

**Why is this faster than the naive `for each of 32 bits` approach?**

The naive method checks each bit position (32 or 64
iterations regardless of n). Kernighan's algorithm runs once
per **set** bit. For sparse numbers (few bits set), it's much
faster. For dense numbers, it's the same order.

**Trace on `n = 12 = 1100`:**
```
n=12 (1100), count=0.
n &= n-1: n=12 & 11 = 1100 & 1011 = 1000 = 8. count=1.
n=8 (1000), still > 0.
n &= n-1: n=8 & 7 = 1000 & 0111 = 0000 = 0. count=2.
n=0, exit loop.
Return 2.
```

Two set bits in `1100`. ✓

**Version 2: `bin(n).count('1')`**

A Pythonic one-liner. `bin(n)` returns a string like
`"0b1100"`. Count the `'1'` chars: 2.

This is *O(log n)* time (string construction) but uses string
operations, so it's slower in practice than Kernighan for
large n.

**Version 3: `n.bit_count()` (Python 3.10+)**

The cleanest. Uses CPU-native popcount instruction internally
(on x86, the `POPCNT` instruction does it in one cycle).
Fastest of all three.

If you're on Python 3.10+, prefer this. Otherwise use
Kernighan.

**Why is this trick called "Brian Kernighan's"?**

Kernighan (co-author of *The C Programming Language*) wrote
it up in a 1988 paper. The trick predates him in folklore —
it's an old chestnut — but his exposition popularized it.

**Properties:**
- **Time**: *O(popcount)* — proportional to the number of set
  bits.
- **Space**: *O(1)*.

**Applications:**
- Counting "balanced" numbers.
- Hamming distance: count bits where two numbers differ
  (XOR them, then count set bits).
- Bitmask DP: count items in a subset.
- Network protocols: counting flags.

This pattern — "process one set bit at a time" — appears
throughout bit-manipulation problems.
''',
            "complexity": "**Time**: *O(popcount)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: Brian Kernighan — `n & (n-1)` removes the rightmost set bit; count iterations.",
    },
    {
        "id": "set-unset-rightmost",
        "title": "Set / Unset the Rightmost Unset Bit",
        "step_id": 8,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["bit-manipulation"],
        "what_this_teaches": "Bit tricks for locating and operating on the rightmost unset bit.",
        "pattern": "`n | (n + 1)` sets the rightmost unset bit. `n & (n - 1)` unsets the rightmost set bit.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["count-set-bits"],
        "next_problems": ["swap-using-xor"],
        "resources": [_SHEET],
        "understanding": r'''
**Set the rightmost unset bit**: `n | (n + 1)`.

Why? `n + 1` flips all trailing 1s to 0 and sets the next bit
(the rightmost 0 in n). OR-ing keeps everything from n plus
that new bit.

**Unset the rightmost set bit**: `n & (n - 1)` (the same trick
as in count-set-bits).
''',
        "optimized": {
            "explanation": "Two complementary one-liners.",
            "code": r'''def set_rightmost_unset(n: int) -> int:
    return n | (n + 1)

def unset_rightmost_set(n: int) -> int:
    return n & (n - 1)
''',
            "complexity": "**Time**: *O(1)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: `n | (n+1)` sets rightmost 0; `n & (n-1)` clears rightmost 1.",
    },
    {
        "id": "swap-using-xor",
        "title": "Swap Two Numbers Using XOR",
        "step_id": 8,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["bit-manipulation", "xor"],
        "what_this_teaches": "XOR's self-inverse property: a ^ a == 0 and a ^ 0 == a. Three XORs swap two variables without a temp.",
        "pattern": "a ^= b; b ^= a; a ^= b.",
        "prerequisite_lessons": [],
        "prerequisite_problems": [],
        "next_problems": ["single-number-i"],
        "resources": [_SHEET],
        "understanding": r'''
Classic trick: swap two integers without a temporary variable
using XOR.

```python
a ^= b   # a = a^b
b ^= a   # b = b ^ (a^b) = a
a ^= b   # a = (a^b) ^ a = b
```

Three XOR operations. In modern Python, `a, b = b, a` is
cleaner and just as fast. The XOR swap is a curiosity that shows
the algebra of XOR; not used in real code anymore.
''',
        "optimized": {
            "explanation": "XOR swap.",
            "code": r'''def xor_swap(a: int, b: int) -> tuple[int, int]:
    a ^= b
    b ^= a
    a ^= b
    return a, b
''',
            "complexity": "**Time**: *O(1)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: three XORs swap without a temporary; demonstrates XOR's self-inverse.",
    },
    {
        "id": "divide-without-mul-div",
        "title": "Divide Two Integers Without Multiplication or Division",
        "step_id": 8,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["bit-manipulation", "binary-exponentiation"],
        "what_this_teaches": "Use repeated doubling (left shift) to implement division. Subtract the largest doubled divisor that fits; track the quotient bit.",
        "pattern": "While dividend >= divisor: double divisor while it still fits; subtract; add the doubled bit to the quotient.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["pow-x-n"],
        "next_problems": [],
        "resources": [_SHEET, _lc(29, "divide-two-integers")],
        "understanding": r'''
Implement integer division without using `*`, `/`, or `%`.

**Brute force**: subtract divisor from dividend repeatedly,
counting subtractions. *O(quotient)* — slow for large dividends.

**Bit-shifting approach**: repeatedly **double** the divisor
(left shift) until doubling would exceed the dividend. Subtract
this large multiple and add the corresponding power of 2 to the
quotient. Repeat.

Time: *O(log²(dividend))*.
''',
        "optimized": {
            "explanation": "Repeated doubling.",
            "code": r'''def divide(dividend: int, divisor: int) -> int:
    INT_MAX, INT_MIN = 2**31 - 1, -2**31
    # Handle sign.
    sign = -1 if (dividend < 0) ^ (divisor < 0) else 1
    a, b = abs(dividend), abs(divisor)
    quotient = 0
    while a >= b:
        # Double the divisor until it would exceed a.
        temp, count = b, 1
        while a >= (temp << 1):
            temp <<= 1
            count <<= 1
        a -= temp
        quotient += count
    quotient *= sign
    # Clamp to 32-bit.
    return max(INT_MIN, min(INT_MAX, quotient))
''',
            "complexity": "**Time**: *O(log²(a))*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: repeated doubling of the divisor; subtract; accumulate the power-of-2 quotient.",
    },
    # ============ Lecture 2 — Interview Problems ============
    {
        "id": "min-bit-flips",
        "title": "Minimum Bit Flips to Convert One Number to Another",
        "step_id": 8,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["bit-manipulation"],
        "what_this_teaches": "XOR isolates the bits where two numbers differ. Count set bits in the XOR to get the flip count.",
        "pattern": "popcount(a ^ b).",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["count-set-bits"],
        "next_problems": ["single-number-i"],
        "resources": [_SHEET, _lc(2220, "minimum-bit-flips-to-convert-number")],
        "understanding": r'''
The minimum bit flips to convert `a` to `b` is the number of
bit positions where they differ. XOR gives a number with 1s
exactly at those positions. Count the 1s.

```python
def min_bit_flips(a, b):
    return bin(a ^ b).count('1')
```

*O(bits)* time.
''',
        "optimized": {
            "explanation": "popcount(a ^ b).",
            "code": r'''def min_bit_flips(a: int, b: int) -> int:
    return bin(a ^ b).count('1')
''',
            "complexity": "**Time**: *O(bits)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: XOR + popcount.",
    },
    {
        "id": "single-number-i",
        "title": "Single Number (All Others Twice)",
        "step_id": 8,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["bit-manipulation", "xor"],
        "what_this_teaches": "XOR all numbers; pairs cancel; the loner remains.",
        "pattern": "Fold the array with XOR.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["single-number"],
        "next_problems": ["single-number-ii", "single-number-iii"],
        "resources": [_SHEET, _lc(136, "single-number")],
        "understanding": "Same as Step 3's single-number problem. XOR all elements; duplicates cancel; only the loner survives.",
        "optimized": {
            "explanation": "Fold with XOR.",
            "code": r'''def single_number(arr: list[int]) -> int:
    result = 0
    for x in arr:
        result ^= x
    return result
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: XOR cancellation; loner survives.",
    },
    {
        "id": "single-number-ii",
        "title": "Single Number II (All Others Three Times)",
        "step_id": 8,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["bit-manipulation"],
        "what_this_teaches": "Bit-by-bit counting modulo 3. For each bit position, sum bits across the array; the loner's bit is `sum % 3`.",
        "pattern": "For each bit position, count and reduce mod 3.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["single-number-i"],
        "next_problems": ["single-number-iii"],
        "resources": [_SHEET, _lc(137, "single-number-ii")],
        "understanding": r'''
Every element appears 3 times except one which appears once.
Find the loner.

XOR doesn't work directly because `x ^ x ^ x = x`, not 0.

**Approach**: bit-by-bit. For each of the 32 bit positions,
sum the bits across all elements. Triplets contribute 0 mod 3
(they contribute 3); the loner contributes its own bit.

```python
for bit in range(32):
    s = sum((x >> bit) & 1 for x in arr)
    if s % 3 != 0:
        result |= (1 << bit)
```

*O(32n)* time, *O(1)* space.

There's also a clever *O(n)* time, *O(1)* space approach with
two running variables (`ones`, `twos`) tracking the state, but
it's harder to derive on the fly.
''',
        "optimized": {
            "explanation": "Bit-by-bit count mod 3.",
            "code": r'''def single_number_ii(arr: list[int]) -> int:
    result = 0
    for bit in range(32):
        s = sum((x >> bit) & 1 for x in arr)
        if s % 3 != 0:
            result |= (1 << bit)
    # Handle negatives (Python ints are arbitrary precision).
    if result >= 2**31:
        result -= 2**32
    return result
''',
            "complexity": "**Time**: *O(32n)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: bit-by-bit counting mod 3; recover loner's bits.",
    },
    {
        "id": "single-number-iii",
        "title": "Single Number III (Two Loners)",
        "step_id": 8,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["bit-manipulation", "xor"],
        "what_this_teaches": "XOR all → get xor of the two loners. Pick any differing bit; split by that bit; XOR each partition separately.",
        "pattern": "XOR all; pick a differing bit; partition.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["single-number-ii"],
        "next_problems": ["repeating-and-missing"],
        "resources": [_SHEET, _lc(260, "single-number-iii")],
        "understanding": r'''
Two numbers appear once; all others appear twice. Find the two
loners.

**Step 1**: XOR all elements. Result = `a ^ b` where a, b are
the two loners.

**Step 2**: pick any bit set in `a ^ b`. This is a bit where
a and b differ. Partition the array by this bit. Each
partition contains exactly one loner.

**Step 3**: XOR each partition separately. Each XOR gives one
loner.

`O(n)` time, `O(1)` space.
''',
        "optimized": {
            "explanation": "XOR + bit partition.",
            "code": r'''def single_number_iii(arr: list[int]) -> list[int]:
    # Step 1: XOR all → xor of the two loners.
    xor_all = 0
    for x in arr:
        xor_all ^= x
    # Step 2: find a differing bit (rightmost set bit of xor_all).
    diff_bit = xor_all & -xor_all
    # Step 3: partition and XOR each side.
    a = b = 0
    for x in arr:
        if x & diff_bit:
            a ^= x
        else:
            b ^= x
    return [a, b]
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: XOR-all + bit-partition; each partition's XOR is one loner.",
    },
    {
        "id": "power-set-bitwise",
        "title": "Power Set Using Bitwise Operators",
        "step_id": 8,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["bit-manipulation", "subsets"],
        "what_this_teaches": "Every subset of an n-element set corresponds to an integer in [0, 2^n). Bit i of the integer indicates whether element i is included.",
        "pattern": "For mask in 0 to 2^n - 1, include element i if mask has bit i set.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["print-all-subsequences"],
        "next_problems": [],
        "resources": [_SHEET, _lc(78, "subsets")],
        "understanding": r'''
Generate all 2^n subsets using bitmasks. For each integer
`mask` from 0 to `2^n - 1`, include element `i` iff `mask`
has bit `i` set.

This bypasses recursion entirely — pure iteration over integers.
''',
        "optimized": {
            "explanation": "Iterate masks; bit-check.",
            "code": r'''def power_set_bitwise(arr: list[int]) -> list[list[int]]:
    n = len(arr)
    result = []
    for mask in range(1 << n):
        subset = [arr[i] for i in range(n) if mask & (1 << i)]
        result.append(subset)
    return result
''',
            "complexity": "**Time**: *O(2^n * n)*. **Space**: *O(2^n * n)* for output.",
        },
        "summary": "**Pattern**: bitmask iteration; bit i selects element i.",
    },
    {
        "id": "xor-product-subarray",
        "title": "XOR Product of Subarrays",
        "step_id": 8,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["bit-manipulation", "math"],
        "what_this_teaches": "Combinatorial XOR: each element of nums contributes to many subarrays; count how many and use the parity.",
        "pattern": "An element at index i is in `(i+1) * (n-i)` subarrays. If that count is odd, the element XORs into the result.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["single-number-iii"],
        "next_problems": [],
        "resources": [_SHEET],
        "understanding": r'''
Given an array of n elements, compute the XOR of all subarrays'
XOR values.

Direct: enumerate all O(n²) subarrays. Too slow for large n.

Insight: element at index i appears in exactly `(i + 1) * (n -
i)` subarrays (i + 1 choices for left endpoint, n - i choices
for right). If that count is odd, the element XORs into the
total result; if even, it cancels out.

So we XOR the elements at indices where `(i + 1) * (n - i)` is
odd. That happens iff both factors are odd, which requires
n to be odd and i to be even.

If n is even, the result is 0. If n is odd, the result is XOR
of elements at even indices.
''',
        "optimized": {
            "explanation": "Parity-of-count trick.",
            "code": r'''def xor_subarrays(nums: list[int]) -> int:
    n = len(nums)
    if n % 2 == 0:
        return 0
    result = 0
    for i in range(0, n, 2):
        result ^= nums[i]
    return result
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: count parity of element occurrences; XOR only the odd-count contributors.",
    },
    # ============ Lecture 3 — Advanced Maths ============
    {
        "id": "prime-factors",
        "title": "Print Prime Factors of a Number",
        "step_id": 8,
        "lecture_id": 3,
        "difficulty": "easy",
        "tags": ["math", "primes"],
        "what_this_teaches": "Trial division: factor out the smallest prime repeatedly until 1.",
        "pattern": "Trial divide by 2, then odd numbers up to sqrt(n); whatever's left > 1 is the last prime.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["check-for-prime"],
        "next_problems": ["sieve-of-eratosthenes", "all-divisors"],
        "resources": [
            _SHEET,
            {"label": "GFG — Print prime factors",
             "url": "https://www.geeksforgeeks.org/print-all-prime-factors-of-a-given-number/"},
        ],
        "understanding": r'''
Print all prime factors of n.

Trial division: try 2 first (factor out all 2s). Then try odd
numbers 3, 5, 7, ... up to sqrt(remaining). Any leftover > 1 is
itself prime (the last factor).
''',
        "optimized": {
            "explanation": "Trial division up to sqrt.",
            "code": r'''def prime_factors(n: int) -> list[int]:
    factors = []
    # Factor out 2s.
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    # Factor out odd numbers up to sqrt(n).
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 2
    # If anything's left, it's prime.
    if n > 1:
        factors.append(n)
    return factors
''',
            "complexity": "**Time**: *O(sqrt(n))*. **Space**: *O(log n)* for factors.",
        },
        "summary": "**Pattern**: trial division up to sqrt(n); handle the 2-case separately.",
    },
    {
        "id": "sieve-of-eratosthenes",
        "title": "Sieve of Eratosthenes",
        "step_id": 8,
        "lecture_id": 3,
        "difficulty": "medium",
        "tags": ["math", "primes"],
        "what_this_teaches": "Classical sieve algorithm for finding all primes up to n in O(n log log n).",
        "pattern": "Bool array; for each prime p, mark multiples starting from p² as composite.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["prime-factors", "check-for-prime"],
        "next_problems": ["segmented-sieve"],
        "resources": [
            _SHEET,
            {"label": "Wikipedia — Sieve of Eratosthenes",
             "url": "https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes"},
        ],
        "understanding": r'''
Find all primes up to n.

Maintain a boolean array `is_prime[0..n]`, initially all True
(except indices 0 and 1). For each i from 2 up to sqrt(n):

- If `is_prime[i]` is True, i is prime.
- Mark all multiples of i (starting from i²) as composite.

After the loop, the True indices are exactly the primes.

*O(n log log n)* time, *O(n)* space.
''',
        "optimized": {
            "explanation": "Sieve.",
            "code": r'''def sieve(n: int) -> list[int]:
    if n < 2:
        return []
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            # Mark multiples starting from i*i (smaller multiples already marked).
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(n + 1) if is_prime[i]]
''',
            "complexity": "**Time**: *O(n log log n)*. **Space**: *O(n)*.",
        },
        "summary": "**Pattern**: sieve — mark multiples of each prime as composite.",
    },
    {
        "id": "segmented-sieve",
        "title": "Segmented Sieve",
        "step_id": 8,
        "lecture_id": 3,
        "difficulty": "hard",
        "tags": ["math", "primes"],
        "what_this_teaches": "Find primes in a range [L, R] using small primes computed up to sqrt(R), without a full sieve to R.",
        "pattern": "Sieve up to sqrt(R); use those primes to sieve the [L, R] segment.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["sieve-of-eratosthenes"],
        "next_problems": [],
        "resources": [
            _SHEET,
            {"label": "GFG — Segmented Sieve",
             "url": "https://www.geeksforgeeks.org/segmented-sieve/"},
        ],
        "understanding": r'''
Find all primes in `[L, R]` where R could be up to 10^12 but
R - L is small (say 10^6).

A full sieve up to R is infeasible. Instead:

1. Sieve primes up to sqrt(R) using normal Sieve of Eratosthenes.
2. For each such prime p, mark its multiples in [L, R] as
   composite.

Time: *O(sqrt(R) log log sqrt(R) + (R - L) log log sqrt(R))*.
''',
        "optimized": {
            "explanation": "Sieve sqrt(R), then segment.",
            "code": r'''def segmented_sieve(L: int, R: int) -> list[int]:
    # Step 1: sieve up to sqrt(R).
    limit = int(R**0.5) + 1
    is_prime_small = [True] * (limit + 1)
    is_prime_small[0] = is_prime_small[1] = False
    for i in range(2, limit + 1):
        if is_prime_small[i]:
            for j in range(i * i, limit + 1, i):
                is_prime_small[j] = False
    small_primes = [i for i in range(2, limit + 1) if is_prime_small[i]]

    # Step 2: sieve the segment [L, R].
    is_prime_seg = [True] * (R - L + 1)
    if L < 2:
        for i in range(2 - L):
            is_prime_seg[i] = False  # 0 and 1 not prime
    for p in small_primes:
        # First multiple of p in [L, R].
        start = max(p * p, ((L + p - 1) // p) * p)
        for j in range(start, R + 1, p):
            is_prime_seg[j - L] = False
    return [L + i for i, x in enumerate(is_prime_seg) if x]
''',
            "complexity": "**Time**: *O((R - L + sqrt(R)) log log sqrt(R))*. **Space**: *O(R - L + sqrt(R))*.",
        },
        "summary": "**Pattern**: sieve small primes; use them to sieve the [L, R] segment.",
    },
    {
        "id": "gcd-euclidean",
        "title": "GCD via Euclidean Algorithm",
        "step_id": 8,
        "lecture_id": 3,
        "difficulty": "easy",
        "tags": ["math", "gcd"],
        "what_this_teaches": "Euclid's algorithm: gcd(a, b) = gcd(b, a mod b). Reduces large numbers fast.",
        "pattern": "while b: a, b = b, a % b.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["gcd-lcm"],
        "next_problems": [],
        "resources": [
            _SHEET,
            {"label": "Wikipedia — Euclidean algorithm",
             "url": "https://en.wikipedia.org/wiki/Euclidean_algorithm"},
        ],
        "understanding": "Classic O(log(min(a, b))) GCD. Already covered in Step 1 gcd-lcm — this is a brief recap with the same algorithm.",
        "optimized": {
            "explanation": "Iterative Euclid.",
            "code": r'''def gcd(a: int, b: int) -> int:
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a
''',
            "complexity": "**Time**: *O(log(min(a, b)))*. **Space**: *O(1)*.",
        },
        "summary": "**Pattern**: gcd(a, b) = gcd(b, a mod b).",
    },
    {
        "id": "all-divisors",
        "title": "Print All Divisors of a Number",
        "step_id": 8,
        "lecture_id": 3,
        "difficulty": "easy",
        "tags": ["math", "divisors"],
        "what_this_teaches": "Divisor-pairing trick. Same as Step 1 print-all-divisors.",
        "pattern": "Scan i from 1 to sqrt(n); record both i and n//i.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["print-all-divisors", "check-for-prime"],
        "next_problems": ["prime-factors"],
        "resources": [_SHEET],
        "understanding": "Find all divisors in O(sqrt(n)) using the divisor-pairing trick. Same algorithm as Step 1 print-all-divisors.",
        "optimized": {
            "explanation": "Trial up to sqrt; pair (i, n // i).",
            "code": r'''def all_divisors(n: int) -> list[int]:
    result = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            result.append(i)
            if i != n // i:
                result.append(n // i)
        i += 1
    return sorted(result)
''',
            "complexity": "**Time**: *O(sqrt(n))*. **Space**: *O(sqrt(n))*.",
        },
        "summary": "**Pattern**: divisor pairing around sqrt(n); record both halves of each pair.",
    },
]
