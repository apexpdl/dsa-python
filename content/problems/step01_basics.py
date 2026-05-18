"""Step 1 — Learn the Basics.

Most of the items in Step 1 are syntax tours rather than algorithmic
challenges. We still treat them seriously, because beginners need a
gentle hand here.
"""
from __future__ import annotations

PROBLEMS: list[dict] = [
    {
        "id": "count-digits",
        "title": "Count Digits in a Number",
        "step_id": 1,
        "lecture_id": 4,
        "difficulty": "easy",
        "tags": ["math", "loops"],
        "understanding": r'''
We are given a positive integer like `7894`. We have to tell how many
digits it has. For `7894` the answer is `4` (the digits are 7, 8, 9,
and 4). For `5` the answer is `1`. For `100000` the answer is `6`.

It sounds trivial, but pause for a moment. The number is **a number**,
not a string. Numbers do not have "digits" the way strings do — they
are just a quantity. So the question is really: *"how many digits
would I need to write this number down in base 10?"*. That tiny
re-phrasing matters, because it points us at the math we will use.

Two pieces of mathematical machinery solve this:

1. **Integer division by 10** (`n // 10`) chops off the rightmost
   digit of `n`. For `n = 7894`, `n // 10 = 789`. The 4 is gone.
2. **Counting how many times we can chop** tells us how many digits
   there were to begin with.

Once we have that idea, the rest is just translating it into a loop.
''',
        "brute_force": {
            "explanation": r'''
The most natural beginner instinct is to **convert the number to a
string** and ask for its length. In Python that is one line:

```python
len(str(7894))   # 4
```

This works perfectly. It is *O(d)* where `d` is the number of digits,
because converting an integer to a string still walks through every
digit internally. Conceptually, however, it dodges the algorithm —
Python's `str` is doing the digit work for us, hidden away.

If we want to actually *do* the digit work ourselves, the most
honest "brute force" is to repeatedly chop and count.
''',
            "code": r'''def count_digits_brute(n: int) -> int:
    # We will count how many times we can divide n by 10 before
    # it becomes zero. Each division removes exactly one digit.
    count = 0
    # Special-case zero so that "0" is considered to have one digit.
    if n == 0:
        return 1
    # Standard digit-stripping loop.
    while n > 0:
        # n // 10 removes the rightmost digit. We do not care WHAT
        # the digit was; we only care that there was one to remove.
        n = n // 10
        # We just removed one digit, so bump the count.
        count += 1
    return count
''',
            "complexity": (
                "**Time**: *O(log₁₀ n)*. We chop off one digit per "
                "iteration, and a number `n` has about `log₁₀ n` "
                "digits.\n\n"
                "**Space**: *O(1)*. We only keep a counter and the "
                "shrinking copy of `n`."
            ),
        },
        "thought_process": r'''
The interview-style thinking goes like this. *"I need to count digits.
The number itself does not carry that information directly — I have
to discover it. What is the simplest operation that reveals one digit
at a time? `n % 10` gives me the rightmost digit. `n // 10` discards
it. If I keep dividing by 10 until nothing is left, I will have
walked through every digit. So the count of iterations is the count
of digits."*

Notice that we never even **looked** at the individual digits in our
final code. We just counted how many times we could safely divide.
That is a small but important realization: the question is about
**how many**, not about **which**. Counting how many divisions is
enough.

A second instinct worth comparing is the `len(str(n))` approach. It
is shorter and correct, but it hides the algorithm behind a Python
built-in. Both are *O(log n)* and in real code I would happily use
`len(str(n))`. The reason we even write the loop version is to build
the mental muscle for digit problems that you cannot solve with a
single built-in — like reversing a number, summing its digits, or
checking Armstrong numbers.
''',
        "optimized": {
            "explanation": r'''
There is a slightly cuter formula version. Since the number of digits
of a positive integer `n` in base 10 is `floor(log₁₀(n)) + 1`, we
can compute it directly without any loop.

```python
import math
digits = int(math.log10(n)) + 1
```

This is *O(1)* in terms of arithmetic operations (assuming `log10`
runs in constant time on machine-sized integers). It is the kind of
"clever one-liner" interviewers like to see, but it has a real-world
caveat: floating-point `log10` is not exact, so for very large `n`
near a power of 10 it can produce off-by-one errors. The loop is
boring but always correct.
''',
            "code": r'''import math

def count_digits_log(n: int) -> int:
    # Edge case: log10(0) is undefined. We declare zero has one digit.
    if n == 0:
        return 1
    # int() truncates toward zero, giving us floor(log10(n)).
    # Add 1 because, for example, 7894 has log10 ~= 3.9, floor = 3,
    # but we want 4.
    return int(math.log10(n)) + 1
''',
            "complexity": (
                "**Time**: *O(1)* — constant time arithmetic.\n\n"
                "**Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
The trick at the bottom of all of these solutions is the relationship
between integers, base 10, and `// 10` and `% 10`. **Mod 10** asks
"what is your last digit?" and **div 10** asks "throw your last digit
away". That single pair of operations powers every digit-twiddling
algorithm in Step 1.

If we changed the base, the operations change. To count binary
digits, you would `// 2` and `% 2`. To count digits in hex, you would
`// 16`. The algorithm is one and the same — the base just plugs in.
That insight saves you when an interviewer asks for digit
manipulation in a non-decimal base.
''',
        "summary": r'''
**Pattern**: digit extraction with `% 10` and `// 10`.

**Lesson**: every digit-extraction loop in DSA looks roughly like
`while n: extract = n % 10; n //= 10`. Memorize that skeleton — it
shows up over and over.

**Recognize next time**: any problem about digits of a number (sum
of digits, reverse a number, palindrome number, Armstrong, happy
number). They all share this same shape.
''',
    },
    {
        "id": "reverse-number",
        "title": "Reverse a Number",
        "step_id": 1,
        "lecture_id": 4,
        "difficulty": "easy",
        "tags": ["math", "loops", "digits"],
        "understanding": r'''
We get a number like `7894` and we want to produce the number whose
digits are in reverse order: `4987`. For `1200` the reverse is `21`
(the leading zeros that appear after reversal silently disappear
because we are working with integers, not strings).

The catch is that the input is a **number**, not a string. So we
cannot just "flip the characters". We need to actually build up the
reversed number using arithmetic. That makes this a perfect drill
for the digit-extraction pattern we built in the previous problem.
''',
        "brute_force": {
            "explanation": r'''
The "lazy" answer is to convert to a string, reverse the string, and
convert back: `int(str(n)[::-1])`. This is correct, *O(d)*, and what
you would write in production code.

But the educational version is the arithmetic one. We extract the
last digit, then "push it" onto a growing reversed number. The way
to push a digit onto the end of a number is to multiply the existing
number by 10 (moving everything left by one place) and add the new
digit.

Read that sentence again: **multiply by 10 to shift everything left,
add the new digit on the right**. That is the *only* trick we use.
''',
            "code": r'''def reverse_number(n: int) -> int:
    # We will build `reversed_value` one digit at a time.
    reversed_value = 0
    # Track sign separately so the loop can work on the absolute value.
    sign = -1 if n < 0 else 1
    n = abs(n)
    # Classic digit-extraction loop.
    while n > 0:
        # last_digit is the rightmost digit of n.
        last_digit = n % 10
        # Multiply the existing reversed value by 10 (shifting it left)
        # and add the new digit on the right.
        reversed_value = reversed_value * 10 + last_digit
        # Drop the digit we just consumed.
        n = n // 10
    return sign * reversed_value
''',
            "complexity": (
                "**Time**: *O(log₁₀ n)*. One iteration per digit.\n\n"
                "**Space**: *O(1)*."
            ),
        },
        "thought_process": r'''
The mental movie is this. Imagine reading the digits of `7894` from
right to left: 4, then 9, then 8, then 7. The first one you read is
4. You want it to end up as the *leftmost* digit of your answer.
The next one you read is 9 — that should sit just to the right of 4.
And so on.

Now ask: if I have built `4` so far, and I read `9`, how do I make
my running answer `49`? I shift the `4` left by one position and
add `9`. Numerically, that is `4 * 10 + 9 = 49`. Beautiful.

Repeat: I have `49`, I read `8`. I make `49 * 10 + 8 = 498`. I have
`498`, I read `7`. I make `498 * 10 + 7 = 4987`. Done.

The arithmetic is exactly the "shift left, add on the right" you
already use mentally when counting.

**Watch-out**: in languages like C++ or Java this is the typical
place where an integer **overflow** sneaks in — reversing a number
near the 32-bit limit can produce a result above `INT_MAX`. In
Python that does not bite, because Python integers are
arbitrary-precision. But the conceptual point matters: if asked to
"reverse a 32-bit int", check the result against the range and
return 0 (or whatever the problem says) on overflow.
''',
        "deep_concept": r'''
The pattern "multiply by 10, add new digit" is the inverse of "divide
by 10, mod 10". Together they form a tiny pair of operations that
encodes and decodes numbers in base 10. Every time you find yourself
working on the digits of a number, you will use one of these two
moves.

A nice generalization: this exact skeleton (`new = new * BASE +
digit`) is also how you parse a string of digits into an integer.
Build something up by multiplying the running total by the base and
adding the next character's value. If you have ever written your own
`atoi`, you have written this loop.
''',
        "summary": r'''
**Pattern**: build a number digit by digit from right to left using
`new = new * 10 + digit`.

**Lesson**: arithmetic reversal is just digit extraction plus
"shift-and-add". The same two-move dance shows up in palindrome
number, sum of digits, Armstrong, atoi, and many others.

**Recognize next time**: anything that reads a number digit by digit
and produces another number. Reach for the dual `% 10` / `// 10`
pattern.
''',
    },
    {
        "id": "check-palindrome-number",
        "title": "Check if a Number is a Palindrome",
        "step_id": 1,
        "lecture_id": 4,
        "difficulty": "easy",
        "tags": ["math", "digits", "palindrome"],
        "understanding": r'''
A palindrome reads the same forwards and backwards. `121` is a
palindrome. `1221` is. `123` is not. We are asked: given an integer
`n`, is it a palindrome?

There is a subtle convention question. Most versions of this problem
declare that **negative numbers are not palindromes** (because the
minus sign would mismatch on reversal). We'll follow that rule.

The trick is to recognize that "is this a palindrome?" is the same
question as "if I reverse this, do I get the same number?". And we
already know how to reverse a number. So the algorithm is just:
reverse, compare.
''',
        "brute_force": {
            "explanation": r'''
The string-based approach is trivial:

```python
s = str(n)
return s == s[::-1]
```

Correct, *O(d)* time, one line. In an interview the follow-up will
be "can you do it without converting to a string?". And the answer
is: yes, reverse the number with arithmetic and compare.

We are reusing the routine we built in the previous problem. That
is one of the joys of basic DSA — earlier work compounds.
''',
            "code": r'''def is_palindrome_number(n: int) -> bool:
    # By convention, negative numbers are not palindromes because
    # the leading minus would mismatch the reversed trailing digit.
    if n < 0:
        return False
    # Build the reversed value with the exact same loop as before.
    original = n
    reversed_value = 0
    while n > 0:
        reversed_value = reversed_value * 10 + n % 10
        n = n // 10
    # If the reversal equals the original number, it reads the same
    # forwards and backwards.
    return reversed_value == original
''',
            "complexity": (
                "**Time**: *O(log₁₀ n)*.\n\n"
                "**Space**: *O(1)*."
            ),
        },
        "thought_process": r'''
The natural sentence is: *"A number is a palindrome if and only if
reversing it gives back the same number."* That sentence is
literally the algorithm. We translate "reversing it" into the digit
loop and "gives back the same number" into a final equality check.

The only subtlety is that the loop **destroys** `n` (each step
divides it by 10). So we must stash the original first. This is a
common rookie bug: people compare against `n` at the end, forgetting
that `n` is now zero.

You may have seen a clever "half-reverse" trick that stops at the
midpoint and compares two halves. It avoids reversing the whole
number, which on overflow-sensitive platforms (C++/Java with
32-bit ints) matters. In Python it is unnecessary — the full reverse
is just as fast and simpler. We mention it for completeness.
''',
        "deep_concept": r'''
Notice the symmetry between this problem and "reverse a number". The
algorithms are identical; only the final step differs. Once you have
a procedure for reversal, palindrome detection is one comparison
away. That kind of compositional thinking — "if I had a reverse, I
could check palindrome easily" — is a huge part of how senior
programmers solve problems.

The same idea applies to strings: `s == s[::-1]` is the cleanest
check. And to linked lists, where palindrome detection becomes
"reverse the second half, then walk both halves and compare". The
problem changes shape; the strategy ("compare the original to a
reversed copy") stays the same.
''',
        "summary": r'''
**Pattern**: reverse and compare.

**Lesson**: complicated-sounding questions often reduce to a
sub-question you already solved. Reverse-a-number is the
sub-question here.

**Recognize next time**: any "palindrome" question — number, string,
linked list. The first question to ask is always *"how do I produce
the reversed version, and can I afford it?"*.
''',
    },
    {
        "id": "gcd-lcm",
        "title": "GCD and LCM of Two Numbers",
        "step_id": 1,
        "lecture_id": 4,
        "difficulty": "easy",
        "tags": ["math", "gcd", "euclidean"],
        "understanding": r'''
The **greatest common divisor (GCD)** of two positive integers `a`
and `b` is the largest integer that divides both of them without a
remainder. So `gcd(12, 18) = 6`, because 6 divides both 12 and 18,
and nothing larger does.

The **least common multiple (LCM)** of `a` and `b` is the smallest
positive integer that both `a` and `b` divide into. So
`lcm(4, 6) = 12`, because 12 is the smallest number divisible by
both 4 and 6.

A beautiful fact ties them together:

> **`a * b = gcd(a, b) * lcm(a, b)`**

So if you can compute one efficiently, you get the other for free.
That alone is a huge reason to fall in love with GCD.

We will focus on GCD first and use the identity to get LCM.
''',
        "brute_force": {
            "explanation": r'''
The blunt approach: try every candidate from `min(a, b)` down to 1.
The first candidate that divides both `a` and `b` is the GCD.

This is correct but slow. The work is *O(min(a, b))*, which is
disastrous for large numbers.
''',
            "code": r'''def gcd_brute(a: int, b: int) -> int:
    # Start with the larger possible divisor and walk down.
    # Anything larger than min(a, b) cannot divide both.
    g = 1
    for d in range(1, min(a, b) + 1):
        # If d divides both a and b, it's a common divisor.
        # We overwrite g, so the LAST one we record is the largest.
        if a % d == 0 and b % d == 0:
            g = d
    return g
''',
            "complexity": (
                "**Time**: *O(min(a, b))*. Linear in the smaller "
                "number, which is terrible for large inputs.\n\n"
                "**Space**: *O(1)*."
            ),
        },
        "thought_process": r'''
The brute force version comes naturally: "I want the biggest divisor
of both, so let me try every candidate". But it is painfully slow.
The leap to **Euclid's algorithm** is one of the most beautiful
moves in number theory.

Euclid noticed this: if `d` divides both `a` and `b`, then it also
divides `a - b`, `a - 2b`, and in particular `a mod b`. So the set of
common divisors of `(a, b)` is exactly the set of common divisors of
`(b, a mod b)`. That is, **the GCD does not change when we replace
the larger number by its remainder when divided by the smaller one**.

Since `a mod b < b`, this operation shrinks the numbers rapidly. We
keep applying it until one number is zero — and then the other
number *is* the GCD (because everything divides zero).

That insight turns *O(min(a, b))* into *O(log(min(a, b)))*. It is
arguably the oldest non-trivial algorithm in human history (around
300 BCE) and still the fastest way to compute GCD.
''',
        "optimized": {
            "explanation": r'''
Euclid's algorithm: repeatedly replace `(a, b)` with `(b, a % b)`
until `b` becomes zero. The remaining `a` is the GCD.

```python
def gcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a
```

For LCM we use the identity from the introduction:
''',
            "code": r'''def gcd(a: int, b: int) -> int:
    # Work with absolute values so the algorithm is sign-safe.
    a, b = abs(a), abs(b)
    # Loop until b is zero. The invariant: gcd(a, b) never changes
    # when we replace (a, b) with (b, a % b).
    while b != 0:
        # Simultaneously assign new values so we do not need a temp.
        a, b = b, a % b
    # When b is zero, a contains the answer.
    return a


def lcm(a: int, b: int) -> int:
    # Edge case: lcm involving zero is zero by convention.
    if a == 0 or b == 0:
        return 0
    # a * b = gcd(a, b) * lcm(a, b), so lcm = (a * b) // gcd(a, b).
    # We divide before multiplying to avoid huge intermediate values
    # in languages with integer limits. In Python it does not matter
    # but the habit is worth keeping.
    return abs(a // gcd(a, b) * b)
''',
            "complexity": (
                "**Time**: *O(log(min(a, b)))*. Each step at least "
                "halves the smaller number (in a precise sense).\n\n"
                "**Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
Euclid's algorithm is the prototype for what mathematicians call
"the Euclidean trick": use a property to keep replacing your problem
with a strictly smaller version of itself while preserving the
quantity you care about. We will see this exact rhythm again in
modular arithmetic, in extended GCD (which solves linear Diophantine
equations), and even — more loosely — in the way binary search
shrinks its window.

A second observation: Python's standard library exposes
`math.gcd(a, b)` and `math.lcm(a, b)` directly. Use them in real
code. The reason to know the algorithm is to be ready when you need
a custom variant — like *extended* Euclidean (which also returns the
coefficients of Bezout's identity), or GCD over arrays.

```python
import math

g = math.gcd(48, 36)            # 12
l = math.lcm(4, 6, 10)          # 60 (lcm accepts many arguments)
```
''',
        "summary": r'''
**Pattern**: replace `(a, b)` with `(b, a % b)` until `b == 0`.

**Lesson**: the right invariant ("GCD is preserved under
remainder") shrinks an *O(n)* search to an *O(log n)* algorithm.

**Recognize next time**: any question involving "common", "divides",
"reducing a fraction", or LCMs/GCDs across arrays. The Euclidean
trick is usually inside.
''',
    },
    {
        "id": "check-for-prime",
        "title": "Check if a Number is Prime",
        "step_id": 1,
        "lecture_id": 4,
        "difficulty": "easy",
        "tags": ["math", "primes"],
        "understanding": r'''
A **prime number** is a positive integer greater than 1 with exactly
two divisors: 1 and itself. So 2, 3, 5, 7, 11, 13 are prime. 4 is
not, because 4 = 2 × 2. 9 is not, because 9 = 3 × 3. 1 is not prime
by definition.

We are given a number `n` and we need to say whether it is prime.
The question sounds trivial, but it has a *very* satisfying
optimization that teaches a beautiful fact about divisors.
''',
        "brute_force": {
            "explanation": r'''
The simplest approach: check every integer from 2 to `n - 1`. If any
of them divides `n`, then `n` has more than two divisors — it is
composite. Otherwise it is prime.

This is *O(n)*. For `n = 10⁹` that is a billion divisions. Too slow.
''',
            "code": r'''def is_prime_brute(n: int) -> bool:
    # Primes are defined for n > 1, so 0, 1, and negatives are not prime.
    if n < 2:
        return False
    # Try every candidate divisor from 2 up to n - 1.
    for d in range(2, n):
        if n % d == 0:
            # Found a non-trivial divisor; n is composite.
            return False
    # No divisor found; n is prime.
    return True
''',
            "complexity": "**Time**: *O(n)*. **Space**: *O(1)*.",
        },
        "thought_process": r'''
The genius insight is this. **If `n` has a divisor `d` greater than
`sqrt(n)`, then `n` also has a divisor `n / d` less than `sqrt(n)`.**

Why? Because divisors come in pairs that multiply to `n`. If
`d * e = n` and `d > sqrt(n)`, then `e < sqrt(n)`. So divisors are
mirror-symmetric around `sqrt(n)`. To find any divisor, we only need
to check up to `sqrt(n)`. Anything above `sqrt(n)` we would have
found via its partner.

So instead of scanning to `n`, we scan only to `sqrt(n)`. For
`n = 10⁹` that is about 31,623 divisions instead of a billion.
Massive win.

You can squeeze more out by realizing that aside from 2, every prime
is odd. So we only need to check 2 first, then test odd numbers
3, 5, 7, ... up to `sqrt(n)`. This is small in big-O terms but
roughly halves the constant.
''',
        "optimized": {
            "explanation": r'''
We scan candidate divisors from 2 to `floor(sqrt(n))`. If any of
them divides `n`, it is composite. Otherwise it is prime.
''',
            "code": r'''def is_prime(n: int) -> bool:
    # Handle the small cases explicitly. Primes start at 2.
    if n < 2:
        return False
    if n < 4:                        # 2 and 3 are prime
        return True
    # Even numbers (other than 2) are composite, so eliminate them once.
    if n % 2 == 0:
        return False
    # Now we only need to test odd candidates 3, 5, 7, ...
    # We stop at sqrt(n) because of the divisor-pairing argument.
    # i * i <= n is equivalent to i <= sqrt(n) and avoids a sqrt() call.
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True
''',
            "complexity": (
                "**Time**: *O(sqrt(n))*. **Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
The divisor-pairing argument — "divisors of `n` come in symmetric
pairs around `sqrt(n)`" — is one of the most reused facts in
number-theoretic algorithms. We use it again to list all divisors of
a number in *O(sqrt(n))*: iterate `i` from 1 to `sqrt(n)`, and
whenever `i` divides `n`, record both `i` and `n // i`. Two divisors
for the price of one.

If you need to test many numbers for primality, you do **not** want
to run *O(sqrt(n))* per number. The right tool is the
**Sieve of Eratosthenes**, which precomputes all primes up to `n` in
*O(n log log n)* time. That is covered in Step 8's Advanced Maths
lecture.

There are also probabilistic primality tests (Miller-Rabin) for
truly enormous numbers. For interview purposes, `O(sqrt(n))` is the
gold standard and the one to know cold.
''',
        "summary": r'''
**Pattern**: trial division up to `sqrt(n)`.

**Lesson**: divisors are paired symmetrically around `sqrt(n)`, so
we only have to search half of the divisor space.

**Recognize next time**: anytime you scan divisors (count divisors,
sum of divisors, prime check) the `i * i <= n` upper bound is your
friend.
''',
    },
    {
        "id": "print-1-to-n",
        "title": "Print 1 to N using Recursion",
        "step_id": 1,
        "lecture_id": 5,
        "difficulty": "easy",
        "tags": ["recursion", "fundamentals"],
        "understanding": r'''
Print the numbers 1, 2, 3, ..., N — but without using a loop. We
have to use recursion. This is one of those problems where the
*answer* is trivial; the value lies in **forming the right mental
model** for recursion.
''',
        "brute_force": {
            "explanation": r'''
There is no real "brute force" vs "optimized" split here; both
approaches are recursion, but they differ in the *thinking style*.

The first style is **"think in terms of the smaller subproblem"**.
*"If I already had a function that prints 1 to N-1, what would I do
to extend it to print 1 to N?"* Answer: call that function first,
then print N. That gives us a tail-style printing — first we print
1, 2, ..., N-1; then we print N.
''',
            "code": r'''def print_1_to_n_v1(n: int) -> None:
    # Base case: nothing to print if n <= 0.
    if n <= 0:
        return
    # Trust that this call prints 1, 2, ..., n - 1 in order.
    print_1_to_n_v1(n - 1)
    # Now append n on the end.
    print(n)
''',
            "complexity": (
                "**Time**: *O(n)* — n recursive calls.\n\n"
                "**Space**: *O(n)* — the call stack is n deep."
            ),
        },
        "thought_process": r'''
There is an alternative style — **"pass a counter forward and grow
it"**. This one feels more like iteration disguised as recursion.

```python
def print_1_to_n_v2(i: int, n: int) -> None:
    if i > n:
        return
    print(i)
    print_1_to_n_v2(i + 1, n)
```

Both styles are correct. The first style is closer to **classical
recursion** — "express the solution in terms of a smaller
subproblem". The second style is **iteration with a stack** — "carry
a counter forward, advance it each step".

For absolute beginners I gently recommend the first style, because
it builds the leap-of-faith muscle. Once you have written half a
dozen recursive solutions thinking "what if I already had the answer
for n - 1?", recursion stops feeling magical.

The mind game is this: in the line `print_1_to_n_v1(n - 1); print(n)`,
do not look inside `print_1_to_n_v1`. Assume it already does its job
correctly for `n - 1`. Then ask: what one extra step do I add to
make it work for `n`? The answer is: print `n` at the end.

Now reverse the order:

```python
def print_n_to_1(n: int) -> None:
    if n <= 0:
        return
    print(n)
    print_n_to_1(n - 1)
```

By swapping the print and the recursive call, we print N first and
recurse second — giving N, N-1, N-2, ..., 1. Same skeleton, different
relative order of "act" and "delegate". That choice of order is one
of the most important little decisions in recursion.
''',
        "deep_concept": r'''
There is a profound point here that is worth highlighting. **The
order in which you do work versus call yourself controls whether you
process the data top-down or bottom-up.**

- *Recurse first, then act* → results come out in their natural
  forward order. We compute `print_1_to_N` and the "act" (printing
  N) happens after the recursive call returns.
- *Act first, then recurse* → results come out in reverse order, or
  we attack the problem top-down.

This same dichotomy controls preorder vs postorder traversals of a
tree. It controls "build forward" vs "build backward" in DP. It is
the *same* idea wearing different costumes. Internalize the swap and
you have a tool that re-appears everywhere.
''',
        "summary": r'''
**Pattern**: recursion as "delegate to a smaller version, then
combine".

**Lesson**: the order of `print(n)` and `recurse(n - 1)` controls
output order. Recurse first → forward; print first → backward.

**Recognize next time**: any "do this for n, n-1, n-2, ... down to a
base case" problem. The recursion shape is identical to this one.
''',
    },
    {
        "id": "factorial-of-n",
        "title": "Factorial of N",
        "step_id": 1,
        "lecture_id": 5,
        "difficulty": "easy",
        "tags": ["recursion", "math"],
        "understanding": r'''
The factorial of N, written `N!`, is defined as

> `N! = N × (N-1) × (N-2) × ... × 1`

with the special case `0! = 1`. So `5! = 5 × 4 × 3 × 2 × 1 = 120`.

It is famous because it is the simplest function whose textbook
definition is **already recursive**: `N! = N × (N-1)!`. The problem
is asking us to translate that line of math directly into code.
''',
        "brute_force": {
            "explanation": r'''
The iterative version multiplies in a loop:

```python
result = 1
for k in range(2, n + 1):
    result *= k
```

It is fine and *O(n)*. The recursive version reads the math directly.
''',
            "code": r'''def factorial(n: int) -> int:
    # Base case: 0! = 1 and 1! = 1.
    if n <= 1:
        return 1
    # Recursive case: n! = n * (n - 1)!
    return n * factorial(n - 1)
''',
            "complexity": (
                "**Time**: *O(n)*. One multiplication per recursive "
                "call.\n\n"
                "**Space**: *O(n)* call stack."
            ),
        },
        "thought_process": r'''
We do not need to invent anything new here. The recursive definition
*is* the algorithm. The interesting questions are different ones.

*What if `n` is huge?* In Python, integers can grow arbitrarily, so
the answer is mathematically correct but huge. The recursion depth
grows linearly with `n`, which collides with Python's default
recursion limit of 1000. For `n = 10000`, you would hit
`RecursionError`. The iterative version sidesteps that.

*What if you want it really fast?* For numbers that fit in machine
ints, this is already linear and you can't do meaningfully better.
For "factorial mod p" problems in number theory, you use modular
arithmetic and may use Wilson's theorem or precomputed factorial
tables. But these are higher-level concerns.

For a beginner, the lesson is: **a problem with a recursive
definition has a recursive solution that looks identical to the
definition**.
''',
        "deep_concept": r'''
Factorial is the gateway to combinatorics. The number of ways to
arrange `n` distinct items in a row is `n!`. The number of ways to
choose `k` items from `n` is `n! / (k! * (n - k)!)`. Permutations
and combinations come up constantly in counting problems.

It is also the gateway to **stack overflow appreciation**. If you
ask for `factorial(2000)` recursively, Python's default limit will
slap you. This is the right time to learn `sys.setrecursionlimit`
and, more importantly, to understand why deep recursion in Python is
not free. Trees, graphs, and DP problems with linear depth all share
this gotcha.
''',
        "summary": r'''
**Pattern**: a recursive math definition translates directly into
code.

**Lesson**: recursion shines when the problem has the same shape as
its smaller subproblem. `n! = n * (n-1)!` is the canonical example.

**Recognize next time**: anywhere the mathematical definition is
self-referential — Fibonacci, Catalan numbers, sums-of-sequences.
''',
    },
    {
        "id": "fibonacci-number",
        "title": "Fibonacci Number",
        "step_id": 1,
        "lecture_id": 5,
        "difficulty": "easy",
        "tags": ["recursion", "dp", "memoization"],
        "understanding": r'''
The Fibonacci sequence is defined like this:

> `F(0) = 0`, `F(1) = 1`, `F(n) = F(n - 1) + F(n - 2)` for `n >= 2`.

So the sequence starts 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, ... Each
number is the sum of the two before it.

We are asked: given `n`, compute `F(n)`. The recursive definition
practically writes the function for us. The interesting part is what
happens when you actually *run* that naive function. The lesson here
is the **first big efficiency lesson in DSA**.
''',
        "brute_force": {
            "explanation": r'''
The naive recursion translates the definition directly:

```python
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

It is correct. But **it is disastrously slow**. Run `fib(40)` and
your laptop will visibly think. Run `fib(50)` and you will be
waiting many seconds. Run `fib(60)` and you may as well make tea.

Why? Because the recursion tree branches. `fib(5)` calls `fib(4)`
and `fib(3)`. `fib(4)` calls `fib(3)` and `fib(2)`. Notice that
`fib(3)` was computed twice — once for `fib(5)` directly and once
via `fib(4)`. As `n` grows, the same subproblems get recomputed
exponentially many times. The time complexity is roughly
**O(φⁿ)** ≈ **O(1.618ⁿ)**.

This is the first time you really feel the cost of redundant work.
''',
            "code": r'''def fib_brute(n: int) -> int:
    # Base cases: F(0) = 0, F(1) = 1.
    if n < 2:
        return n
    # The recursive definition, translated literally. This is
    # CORRECT but slow because of overlapping subproblems.
    return fib_brute(n - 1) + fib_brute(n - 2)
''',
            "complexity": (
                "**Time**: *O(φⁿ)* — exponential. **Space**: *O(n)* "
                "call stack."
            ),
        },
        "thought_process": r'''
The first time a beginner writes this and runs it on n=50, the
penny drops: not all correct algorithms are fast. The key
observation is: *we are solving the same subproblems over and over
again*. If we only solved each once and remembered the result, we
would walk through `n + 1` subproblems total — a complete shift from
exponential to linear.

This is **memoization**. It is the simplest, most direct entry into
**dynamic programming**. And Fibonacci is the universal teaching
example for it.

The shift in thinking: *"Don't redo. Remember."*

Two ways to remember:

1. **Top-down** — keep the recursion, add a cache.
2. **Bottom-up** — compute F(0), F(1), F(2), ..., F(n) iteratively,
   storing each value as you go (or just the last two, since that
   is all you ever need).
''',
        "optimized": {
            "explanation": r'''
**Top-down with memoization** (closest to the recursive version):

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

**Bottom-up with constant extra memory** (the most memory-efficient
version, the one to ship):
''',
            "code": r'''def fib(n: int) -> int:
    # Edge cases.
    if n < 2:
        return n
    # We only ever need the last two values to compute the next one.
    # prev2 is F(i - 2), prev1 is F(i - 1).
    prev2, prev1 = 0, 1
    # Walk from i = 2 up to i = n, computing each value once.
    for _ in range(2, n + 1):
        # F(i) = F(i - 1) + F(i - 2). After computing it, shift the
        # window: new prev2 is the old prev1, new prev1 is the value
        # we just computed.
        prev2, prev1 = prev1, prev1 + prev2
    # After the loop, prev1 is F(n).
    return prev1
''',
            "complexity": (
                "**Time**: *O(n)*. **Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
Fibonacci is the smallest, friendliest example of the central DP
insight: **when subproblems overlap, cache them**. Once you have
felt the exponential pain of the naive solution and the relief of
the linear solution, you understand what DP is for.

Beyond the algorithm, there are gorgeous facts:

- The ratio `F(n + 1) / F(n)` converges to the golden ratio
  `φ ≈ 1.618`.
- There is a closed-form formula (Binet's formula) that computes
  `F(n)` from `n` using `φ`. It is *O(1)* arithmetic but uses
  floating-point and is inexact for large `n`.
- Fibonacci can be computed in *O(log n)* using matrix
  exponentiation. That is overkill for interview problems but
  beautiful.

For the curriculum's purposes: write the linear iterative version,
understand the recursion + memoization view, and you are in
excellent shape for the entire DP lecture in Step 16.
''',
        "summary": r'''
**Pattern**: overlapping subproblems → memoize or tabulate.

**Lesson**: an exponential-time recursion can usually be turned into
a linear-time algorithm just by remembering each subproblem's answer
once. This is the entire idea of dynamic programming.

**Recognize next time**: any recursion where the same arguments
appear in multiple branches. The cache transforms the runtime.
''',
    },
    {
        "id": "count-frequencies",
        "title": "Count Frequencies of Array Elements",
        "step_id": 1,
        "lecture_id": 6,
        "difficulty": "easy",
        "tags": ["hashing", "dict", "counter"],
        "understanding": r'''
Given an array of numbers (or any hashable values), we want to know
how many times each distinct value appears. For
`[1, 2, 2, 3, 3, 3, 4]` the answer is `{1: 1, 2: 2, 3: 3, 4: 1}`.

This sounds easy because it is — but the way we *think* about it
introduces the central idea of hashing as a tool. Frequency counting
is the bread-and-butter of many medium-hard problems (anagrams,
majority element, first non-repeating, top-K frequent).
''',
        "brute_force": {
            "explanation": r'''
For each distinct value, walk the array and count occurrences. We
need to do this for every distinct value, which is *O(n²)* in the
worst case (all distinct).

```python
def freq_brute(arr):
    seen = []
    result = {}
    for x in arr:
        if x not in seen:
            seen.append(x)
            count = 0
            for y in arr:
                if y == x:
                    count += 1
            result[x] = count
    return result
```

Correct, but quadratic. We re-scan the whole array for each new
value, and the `x not in seen` check on a list is also *O(n)*.

We will improve to a single pass using a dictionary.
''',
            "code": r'''def count_freq_brute(arr: list) -> dict:
    seen = []
    result = {}
    # Outer loop: pick a candidate value.
    for x in arr:
        # Skip if we've already counted this one.
        if x in seen:
            continue
        seen.append(x)
        # Inner loop: count occurrences of x in the whole array.
        count = 0
        for y in arr:
            if y == x:
                count += 1
        result[x] = count
    return result
''',
            "complexity": (
                "**Time**: *O(n²)* in the worst case.\n\n"
                "**Space**: *O(n)* for the result and the `seen` list."
            ),
        },
        "thought_process": r'''
The brute force does double work: it scans the whole array once for
each distinct value. But we could collect all counts in a **single
pass** by using a dictionary: walk through the array, and for each
element, add one to its dictionary entry. By the end of the pass,
the dict contains exactly the counts.

This is the central instinct of hashing — *whenever you find
yourself counting or matching, a dict lets you bind information to
keys and look it up in O(1)*.

```python
counts = {}
for x in arr:
    counts[x] = counts.get(x, 0) + 1
```

Two-line algorithm. *O(n)* time. Dramatic improvement.

Python's `collections.Counter` does exactly this and a bit more.
Senior Python: prefer `Counter`. Beginner Python: write the loop
version once to make sure you understand it, then switch to
`Counter`.
''',
        "optimized": {
            "explanation": r'''
Use a dictionary (or `Counter`) and walk the array once.
''',
            "code": r'''from collections import Counter

def count_freq(arr: list) -> dict:
    # Counter is a dict subclass that knows how to count. The single
    # line below walks `arr` once and produces the frequency map.
    return dict(Counter(arr))


def count_freq_manual(arr: list) -> dict:
    """Same idea, written without Counter for educational purposes."""
    counts: dict = {}
    for x in arr:
        # dict.get(key, default) returns the value if key is present,
        # otherwise the default. So if x has never been seen, we
        # start its count at 0 and immediately bump to 1.
        counts[x] = counts.get(x, 0) + 1
    return counts
''',
            "complexity": (
                "**Time**: *O(n)*. **Space**: *O(k)* where `k` is the "
                "number of distinct values."
            ),
        },
        "deep_concept": r'''
The deep idea here is **trading time for space**. We are asking the
computer to hold a dictionary in memory in exchange for skipping
repeated linear scans. That trade is one of the foundational
techniques of algorithmic optimization. It will reappear in two-sum,
in longest substring without repeating, in subarray sum equals K, in
group-anagrams, and in dozens of other problems.

A second deep idea is the **commutative property of counting**: we
can process elements in any order and get the same final dict. That
property is what lets us do this in one pass. Many algorithms that
look linear are linear because the operation we're applying is
commutative.

A small but important variant: when the array values are bounded
small integers (say 0 ≤ value < 26 for lowercase letters, or
0 ≤ value < 10⁵), you can replace the dict with a list indexed by
value. List lookups are slightly faster than dict lookups and use
less memory. Anagram-style problems use exactly this trick.
''',
        "summary": r'''
**Pattern**: walk once + a dictionary = frequency map.

**Lesson**: any "how many of each?" question becomes one pass once
you reach for a hash map.

**Recognize next time**: anagrams, top-K, first non-repeating,
majority element, "do these two arrays have the same multiset".
Always start with `Counter`.
''',
    },
]
