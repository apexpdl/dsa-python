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
        "tags": ["math", "loops", "digits"],
        "what_this_teaches": (
            "How to **discover** information about a number that the "
            "number does not carry explicitly. The pattern that emerges "
            "— peel one digit, count, repeat — is the foundation for "
            "every digit-manipulation problem in this lecture."
        ),
        "pattern": "Digit extraction loop: `% 10` peels, `// 10` shrinks.",
        "prerequisite_lessons": ["arrays"],
        "prerequisite_problems": [],
        "next_problems": [
            "reverse-number",
            "check-palindrome-number",
            "armstrong-number",
            "count-frequencies",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 1 (Basic Maths)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "GeeksforGeeks — Program to count digits in an integer",
                "url": "https://www.geeksforgeeks.org/program-count-digits-integer-3-different-methods/",
            },
        ],
        "understanding": r'''
Let's slow down and really see this problem. We are handed a positive
integer. Something like `7894`, or `5`, or `100000`. Our job is to
report how many digits it has. For `7894` the answer is `4`. For
`5` the answer is `1`. For `100000` the answer is `6`.

When you read this for the first time, it can feel embarrassingly
simple. You look at the number, you count the digits with your eyes,
done. *"Why are we even being asked this?"* That feeling is honest,
and it deserves an honest answer.

The catch is that you are not looking at a *string* of digits. You
are looking at **a number**. A number, deep down inside the computer,
is a quantity. It is just *value*. The number 7894 does not store the
character `7`, then the character `8`, then `9`, then `4`. It stores
a single binary representation of the quantity seven thousand eight
hundred and ninety-four. There is no list of digits sitting in
memory waiting for us to count.

So the real question hiding inside this innocent problem is: **given
only the value, how do we recover its digits?** And answering that
question is what teaches us a tiny but absolutely fundamental skill.
That skill, "peel the last digit off a number using arithmetic," is
the same skill we will use to reverse a number, check if a number
is a palindrome, compute its digit sum, check whether it is an
Armstrong number, and so on. So even though this looks like a
toy problem, please treat it seriously. The muscle you build here
gets reused for the next six problems in this lecture.

The two pieces of mathematical machinery we need are this pair:

1. **Mod 10** (`n % 10`) asks the number: *"what is your rightmost
   digit?"* For `n = 7894`, `n % 10` is `4`. That is because dividing
   7894 by 10 leaves a remainder of 4. The remainder is, by the very
   definition of base 10, the last digit.
2. **Integer division by 10** (`n // 10`) asks the number to *"throw
   away your rightmost digit, please."* For `n = 7894`, `n // 10` is
   `789`. The 4 is gone. The remaining digits stay.

Now combine those two operations into a loop. Peel the last digit
off, throw it away, peel the next last digit off, throw it away, and
keep going. Every time you peel, the number gets shorter by one
digit. So if you count how many times you can peel before the
number runs out, you have just counted the number's digits — *without
ever needing to know what those digits actually were*.

That last sentence is the **soul** of this problem. The question is
about *how many*, not about *which*. We never even look at the
digits themselves. We only count how many times we managed to peel.
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
            "walkthrough": r'''
Let's read this code as a story, line by line, the way a senior
engineer might explain it to you sitting beside them.

**`def count_digits_brute(n: int) -> int:`** — We're defining a
function. It takes an integer (we said so with the `: int` type
hint, which Python doesn't enforce but it documents the intent),
and it returns an integer (the `-> int`). The name `brute` is
our hint to ourselves that this is the straightforward version,
not the clever one.

**`count = 0`** — We make a counter and set it to zero. This
will be our tally. Every time we successfully remove a digit
from `n`, we'll add one to `count`.

**`if n == 0: return 1`** — A small but important edge case.
The number zero, written down on paper, has one digit: the
digit `0`. But the loop we're about to write needs `n > 0` to
do any work. If we let `n = 0` fall through to the loop, the
loop would run zero times and we'd return `0` — wrong! So we
catch this special case first and return `1`. This is the kind
of edge case that bites beginners constantly; train yourself to
ask "what about zero?" and "what about negatives?" before every
loop.

**`while n > 0:`** — The main loop. We're going to keep chipping
away at `n` until there's nothing left. As long as `n` has at
least one digit (which in math-speak means `n` is positive), we
have work to do.

**`n = n // 10`** — This is the surgery. The double slash `//`
is Python's *integer division*. Dividing by 10 and throwing
away the remainder is exactly the operation "remove the
rightmost digit." For instance, `7894 // 10` gives `789`, not
`789.4` and not `790`. We assign the result back to `n`, so
`n` shrinks by one digit each iteration.

**`count += 1`** — We just removed a digit, so the original
number had at least one more digit than we'd previously
counted. Bump the counter by one. This is the actual "counting
work" — everything else is just bookkeeping.

**`return count`** — After the loop exits (when `n` finally
reaches `0`), `count` holds the total number of times we were
able to do the surgery. That's the digit count. Return it.

That's the whole function — five real lines of logic and a
single edge case. The mental dance is "while there's still a
digit, take one off and bump the counter." Memorize that
phrase; the same dance shows up in reversing a number, summing
digits, checking Armstrong numbers, and many more digit
manipulation problems coming up.
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
Okay, let's slow down and really walk through what is happening inside
the loop, the way you would explain it to yourself out loud while
debugging.

Imagine you are sitting at a desk with the number `7894` written on a
slip of paper. Your job is to count how many digits are on the slip,
but **you are only allowed to use two tools**: a tool that tells you
the last digit of the number, and a tool that hands you back the
number with its last digit removed. You may use those tools as many
times as you like.

You look at `7894`. You hit the "remove last digit" tool. The paper
now says `789`. You make a tally mark — *one*. You hit the tool
again. The paper says `78`. Another tally mark — *two*. Again. The
paper says `7`. *Three*. Again. The paper says `0`. *Four*. The
number ran out. You stop. You look at your tallies: four. That is
your answer.

That tiny play-by-play *is* the loop. Each pass through the loop
does the same thing your hand did: divide once, tally once. The loop
keeps going as long as the paper still has digits on it — which, in
arithmetic terms, means as long as `n > 0`. When `n` finally reaches
zero, the paper is blank, the work is done, the tally is the answer.

Now, the interview-friendly framing of this thinking. *"I need to
count digits, but the number does not store its digits. It only
stores a value. So I need an operation that lets me **discover** one
digit at a time. `% 10` gives me the rightmost digit; `// 10`
discards it. If I keep applying `// 10`, the number will shrink
exactly one digit per step. The number of steps before the number
becomes zero is the digit count. I do not even need to look at the
digit each time — I just need to count how many times I shrank."*

This little dance — "I do not need to look at the value, only count
how many times I could act on it" — is a surprisingly powerful
mental move. We will reuse it when checking primality (count how many
divisors you find, not what they are), counting trailing zeros, and
in many problems about *quantity of operations* rather than *content
of operations*.

There is a second, more "Pythonic" approach worth comparing:
`len(str(n))`. It works perfectly and is one line. The reason we
**still** write the arithmetic loop is that the arithmetic version
generalizes. As soon as the next problem asks us to **reverse** the
number, or to **sum its digits**, or to **check whether it is an
Armstrong number**, the `len(str(n))` trick is useless — we need
actual access to the digits one at a time. The arithmetic skeleton
`while n: digit = n % 10; n //= 10` gives us that access. Burn it
into your fingers now and it pays off for the next six problems.
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
            "walkthrough": r'''
This version is a one-liner, but it deserves an explanation
because the math behind it is the kind of thing that delights
people the first time they see it.

**`import math`** — We need `math.log10`, which Python doesn't
include by default. The `math` module provides scientific
functions like logarithms, trigonometry, and constants. We
import it at the top so we can use `math.log10` later.

**`def count_digits_log(n: int) -> int:`** — Same signature as
before. Just a different way to compute the same thing.

**`if n == 0: return 1`** — Same edge case as the brute force.
The math version actually *requires* this guard because
`math.log10(0)` is undefined (logarithm of zero is negative
infinity, mathematically). Without this guard, the function
would raise a `ValueError`. Always handle zero first when
working with logs.

**`return int(math.log10(n)) + 1`** — Here is the magic. Let me
unpack it slowly.

`math.log10(n)` computes the logarithm base 10 of `n`. For
example, `math.log10(7894)` is approximately `3.897`. That
fractional part `0.897` is the "how close to the next power of
10" measurement, and we don't need it. The integer part `3`
tells us the *exponent* of the largest power of 10 that fits
inside `n` — that is, `n` is at least `10³ = 1000` but less
than `10⁴ = 10000`.

`int(...)` chops off the fractional part. Note that `int()`
truncates toward zero for positive floats, which for positive
results is the same as the "floor" function. So
`int(math.log10(7894))` is `3`.

`+ 1` because the *number of digits* in a 4-digit number is one
more than the exponent. Think of it this way: numbers from `1`
to `9` have 1 digit and their log10 floor is `0`; from `10` to
`99` have 2 digits and floor log10 is `1`; from `100` to `999`
have 3 digits and floor log10 is `2`. Pattern: digits = floor
log10 + 1.

So `int(math.log10(7894)) + 1` = `3 + 1` = `4`. Four digits.
Correct!

The whole expression runs in constant time — `log10` is one
fast hardware operation. No loop, no iteration. But there's a
catch I want you to remember: floating-point arithmetic is not
exact. For very large numbers near a power of 10 (like
`10**16` or `10**17`), the floating-point `log10` can be very
slightly off, and the `int()` truncation can give a wrong
answer by one. This is rare but real. The brute-force loop is
boring but always correct; the log version is elegant but has
a numerical pothole at extreme scale.
''',
            "complexity": (
                "**Time**: *O(1)* — constant time arithmetic.\n\n"
                "**Space**: *O(1)*."
            ),
        },
        "deep_concept": r'''
Let's zoom out from the loop and ask why this all works in the first
place. The whole trick lives in one observation about **base 10**.

Pick any positive integer, say `7894`. You can always write it as

```
7894 = 7 × 1000 + 8 × 100 + 9 × 10 + 4 × 1
     = 7 × 10³ + 8 × 10² + 9 × 10¹ + 4 × 10⁰
```

Look at the last digit, `4`. Notice that every other term in the sum
is a multiple of 10 — `7 × 1000`, `8 × 100`, `9 × 10` are all
divisible by 10. So when you take `7894 % 10`, all those terms
vanish and only the last term, `4 × 1 = 4`, survives. That is why
**mod 10 gives you the last digit, exactly, every time**. It is not
a coincidence and it is not magic; it falls directly out of the
definition of base 10.

Now look at `7894 // 10`. The integer division throws away the
remainder. So you get `7 × 100 + 8 × 10 + 9 × 1 = 789`. The number
has lost its `1`s place and slid the rest of the digits down by one
position. That is the second half of the magic: integer division by
the base **shifts** the number rightward by one digit.

Together, `% 10` and `// 10` form a tiny but complete toolkit for
walking a number's digits from right to left, *without ever
converting it to a string*. Every digit-manipulation problem in this
lecture — reverse a number, check palindrome, sum of digits,
Armstrong, count of digits — uses exactly these two operations.

The same idea generalizes to other bases. To peel a binary digit,
use `% 2` and `// 2`. To peel a hex digit, use `% 16` and `// 16`.
The algorithm is identical; only the base plugs in. That observation
becomes especially valuable in bit-manipulation problems in Step 8,
where `% 2` and `// 2` reappear under the names "bit at position 0"
and "shift right by one".

One last beautiful detail: the formula version, `int(math.log10(n))
+ 1`, comes from the same place. Because `n` has `d` digits exactly
when `10^(d-1) ≤ n < 10^d`, you can take `log10` and read the
exponent. It is the same fact, expressed in continuous-math
language instead of arithmetic-loop language. Two perspectives, one
underlying truth.
''',
        "confusion_notes": [
            {
                "question": "Why do we use `//` (floor division) instead of `/` (regular division)?",
                "answer": r'''
Because `/` in Python gives you a *floating-point* result, and
floats will quietly ruin this algorithm.

Try it. `7894 / 10` is `789.4`. That is not what we want. We want
the **integer** `789`, with the `.4` chopped off. We want to throw
the last digit away cleanly, not turn it into a fraction.

`//` is "floor division" — it divides and then rounds **down** to
the nearest integer. So `7894 // 10` is `789`, exactly. No
decimals, no floats, no fractions. It is the operation that
genuinely models "throw the last digit away."

There is a second reason to insist on `//`: floats lose precision
on big numbers. If `n` is huge (say, 20 digits long), `n / 10`
might not even be exact anymore — floats only have about 15–17
significant digits. Your loop would silently produce the wrong
count for large inputs. With `//` you stay in integer-land where
everything is exact, no matter how large.

So the rule is simple: whenever you want to throw away a digit (or
any integer remainder), use `//`. Whenever you actually want a
fractional result, use `/`. In digit problems, the answer is
always `//`.
''',
            },
            {
                "question": "Why do we need a special case for `n == 0`?",
                "answer": r'''
Read the loop carefully. It says `while n > 0: ...`. That means
**the loop body never runs if `n` starts at zero**. The counter
stays at 0. The function returns 0.

But that is wrong! The number `0`, written down, has *one* digit
— the digit `0`. We would expect `count_digits(0)` to return 1,
not 0.

So we plant a tiny check at the top:

```python
if n == 0:
    return 1
```

This is what programmers call "handling the edge case." The main
loop assumes the number has at least one nonzero digit somewhere;
zero is special because it has *no* nonzero digits at all, yet it
still counts as a one-digit number.

There is a deeper lesson hiding in this two-line fix. Almost every
algorithm in DSA has at least one **edge case** — an input that
the main logic does not handle correctly. Empty arrays. Strings of
length one. Numbers that are zero or negative. The discipline of
the experienced programmer is to **ask, at the start of every
problem, "what are the weird inputs my loop will mishandle?"** and
then guard against them explicitly.

If you forget the check, the algorithm will appear to work for
every positive number you test, and only fail when someone passes
in zero. That is exactly the kind of bug that survives months of
casual testing before suddenly biting in production. Pay the
two-line tax up front.
''',
            },
            {
                "question": "How does the loop know when to stop?",
                "answer": r'''
The loop stops when `n` becomes zero. Look at the condition:
`while n > 0:`. As long as `n` is strictly greater than zero, the
body runs. The moment `n` hits zero, the condition fails and the
loop exits.

So the real question is: *will `n` always reach zero?* And the
answer is yes, every time, because of how `//` shrinks the
number.

Take any positive integer, say 7894. After one round, `n` is 789.
After two rounds, `n` is 78. Then 7. Then 0. Notice how each round
makes `n` strictly smaller — it cannot ever grow or stay the same.
Since `n` is an integer and it cannot go below zero (because
`789 // 10` is 78, `7 // 10` is 0, `0 // 10` is 0), it has to
reach zero in a finite number of steps.

In computer-science vocabulary, this is called a **decreasing
variant** — a quantity that strictly shrinks each iteration and is
bounded below by zero. Whenever you can identify a decreasing
variant for your loop, you have **proven** that it terminates.
This is a habit worth picking up early. Every loop you write
should have an answer to the question "what gets smaller, and what
is the floor?" — otherwise you might be writing an infinite loop
without realizing it.

A common mistake: writing `while n != 0:` instead of `while n > 0:`
when the input could be negative. If `n` is `-7`, `n // 10` in
Python is `-1` (not `0`!), because Python's floor division rounds
toward negative infinity. So your loop never terminates on
negative input. The cure: either work on `abs(n)` at the top, or
use `while n > 0:` and document that the function expects a
non-negative input. Both are reasonable. Choose consciously.
''',
            },
            {
                "question": "Why does the code never actually look at the digits? Don't we need them?",
                "answer": r'''
Great instinct to spot this. You are right: the code never stores
or uses the individual digits. The line `n = n // 10` discards
the last digit; we never assign it to a variable. And that is on
purpose.

The question we are answering is *"how many digits are there?"*
That is a question about **quantity**, not about **identity**. We
care about *how many*, not *which*. So we count the number of
times we successfully shrank `n`, and that count is our answer.

It is a bit like asking how many pages a book has. To answer, you
do not need to read any of the pages. You can flip from page 1 to
page 2, then to page 3, and so on, and just count how many flips
you did before the book ended. That is what our loop is doing —
flipping pages without reading them.

This separation between "process the structure" and "process the
content" comes back in many problems. For example, finding the
height of a binary tree does not require reading the values in
the nodes — only walking the structure. Counting the number of
items in a linked list does not require looking at the values.
Whenever you find yourself about to store something inside a loop
"just in case I need it later," ask whether the problem actually
asks for that information. Often it does not.

That said: the same loop skeleton, with one extra line, *does*
give you the digits when you need them. For sum-of-digits:

```python
total = 0
while n > 0:
    total += n % 10        # use the digit here
    n = n // 10
```

So when the problem changes from "how many digits" to "what is
the sum of the digits," the only change is that you read
`n % 10` and do something with it. The loop itself is the same.
''',
            },
            {
                "question": "What does `n = n // 10` actually do to `n` in memory?",
                "answer": r'''
Beautiful question, and the answer touches on something many
beginners feel uneasy about: *"am I changing the original number,
or making a new one?"*

When you write `n = n // 10`, Python evaluates the right side
first. It computes `n // 10`, which is a brand-new integer object
in memory — say, 789. Then it reassigns the *name* `n` so that it
points at this new integer. The old integer (7894) is no longer
reachable from `n` and Python will garbage-collect it eventually.

So `n` is not "mutated." Integers in Python are **immutable** —
they cannot be changed in place. What changes is which integer
the *variable name* `n` refers to. After the line runs, the name
`n` points at a different integer than it did before. From your
perspective inside the loop, that distinction does not matter —
`n` got smaller — but it is a useful mental model for later
problems where mutation versus rebinding actually does matter
(like lists, dictionaries, and objects).

If you wanted to keep the original number intact for use after
the loop, you would copy it first:

```python
def count_digits(n):
    original = n          # keep a copy
    if n == 0:
        return 1
    count = 0
    while n > 0:
        n = n // 10
        count += 1
    # original still equals the input; n is now 0
    return count
```

In this function we did not actually need `original`, but in
problems like "reverse a number," we use both the original (to
compare for palindrome) and the shrinking copy (to extract
digits). Getting comfortable with "keep a copy when you might
need it" is a small but real piece of programmer discipline.
''',
            },
        ],
        "summary": r'''
**Pattern**: digit extraction with `% 10` (peel) and `// 10` (shrink).

**Lesson**: every digit-manipulation loop in DSA wears the same
skeleton — `while n > 0: digit = n % 10; n //= 10`. Memorize the
shape and you have ninety percent of Step 1's basic-maths lecture
in your fingers.

**Recognize next time**: any problem about a number's digits — sum
of digits, reverse a number, palindrome number, Armstrong number,
happy number, count of even digits. They are all the same loop
with a different one-line body in the middle.

**Bigger picture**: when a problem asks "how many," count
iterations. When it asks "which," store or test the value of
`n % 10`. The skeleton is the same; only what happens inside the
loop changes.
''',
    },
    {
        "id": "reverse-number",
        "title": "Reverse a Number",
        "step_id": 1,
        "lecture_id": 4,
        "difficulty": "easy",
        "tags": ["math", "loops", "digits"],
        "what_this_teaches": (
            "The dual of digit extraction: how to **build** a number "
            "from its rightmost digit using `new = new * 10 + digit`. "
            "This pairs perfectly with the extraction loop and is the "
            "core move behind atoi-style parsing too."
        ),
        "pattern": "Shift-and-add: extract a digit, append it to a growing reversed number.",
        "prerequisite_lessons": ["arrays"],
        "prerequisite_problems": ["count-digits"],
        "next_problems": [
            "check-palindrome-number",
            "armstrong-number",
            "atoi",
            "atoi-recursive",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 1 (Basic Maths)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 7 — Reverse Integer",
                "url": "https://leetcode.com/problems/reverse-integer/",
            },
        ],
        "understanding": r'''
Let's read the problem carefully and feel what is really being
asked.

You are handed a positive integer like `7894`. You have to produce
a brand-new integer whose digits appear in the **reverse order**:
`4987`. For `1200` the reverse is `21` — the zero that was at the
end of `1200` would have become a leading zero on the front of
`0021`, but integers do not store leading zeros, so it silently
becomes the two-digit number `21`. For `5` (a one-digit input), the
reverse is also `5`, because flipping a one-digit number does
nothing.

The catch — and this is the whole point of the problem — is that
the input is a **number**, not a string. Inside the computer,
`7894` is one quantity stored in a few bytes; it is not the
sequence of characters `'7', '8', '9', '4'`. So we cannot just
"reverse the characters" the way we would reverse a Python string
with `s[::-1]`. We have to actually build up the reversed number
using arithmetic.

That makes this problem a perfect partner for the previous one.
*Count Digits* taught us how to **peel** digits off a number using
`% 10` and `// 10`. Now we will learn the mirror skill: how to
**build** a number by tacking digits onto a growing total. Once
you have both moves in your hands, you can do nearly anything with
the digits of a number.
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
            "walkthrough": r'''
Walk through the function with me, line by line. This is one of
the most important little loops in basic-maths programming —
once you internalize it, six or seven later problems become
trivial.

**`def reverse_number(n: int) -> int:`** — Function signature.
Takes an integer, returns an integer.

**`reversed_value = 0`** — We are going to *build* the reversed
number digit-by-digit, starting from zero. Think of
`reversed_value` as a small piece of paper where we'll write
each new digit on the right as it arrives. Right now the paper
is empty (zero).

**`sign = -1 if n < 0 else 1`** — A small but important detail.
Negative numbers complicate the digit-stripping loop (which
expects `n > 0`), so we capture the sign first. The expression
is a Python conditional: "set sign to -1 if n is negative,
otherwise to 1." This pattern (`x if cond else y`) is Python's
ternary; it returns one of two values.

**`n = abs(n)`** — We strip the sign and work with the
absolute value. We saved the sign in the previous line; we'll
re-apply it at the end. This trick — strip a difficult thing,
deal with the easier core, re-apply at the end — is a
recurring pattern in programming.

**`while n > 0:`** — The main loop. Keep going until we've
peeled off every digit. When `n` finally reaches `0`, all the
digits have been transferred to `reversed_value`.

**`last_digit = n % 10`** — Extract the rightmost digit. As we
saw in count-digits, `%` is the modulo operator: it returns
the remainder after division. `7894 % 10` returns `4`, the
last digit. We give it the name `last_digit` for clarity.

**`reversed_value = reversed_value * 10 + last_digit`** — Here
is the magic line, the heart of the algorithm. Let me unpack it.

Suppose `reversed_value` currently holds `49` (we've already
extracted the `4` then the `9` from `7894`). We just extracted
`8`. We want `reversed_value` to become `498`. How?

`reversed_value * 10` shifts the existing digits left by one
position, turning `49` into `490`. Now there's a `0` in the
ones place, ready to be replaced. We add `last_digit` (`8`) to
get `498`. The `0` is gone, replaced by our new digit.

This shift-and-add trick is the *opposite* of the `// 10`
strip-and-shrink trick. Strip-and-shrink removes the rightmost
digit; shift-and-add appends a new rightmost digit. They are
mirror operations, and you'll use them together constantly.

**`n = n // 10`** — Drop the digit we just consumed. This is
the now-familiar shrink operation. Next iteration's `last_digit`
will be a fresh digit one position to the left of the previous
one.

**`return sign * reversed_value`** — Re-apply the original
sign and return. If we started with `-7894`, sign was `-1` and
this gives us `-4987`. If we started with `7894`, sign was `1`
and this gives us `4987`.

That's the whole algorithm. Five real lines of work. The key
mental images: digits coming off the right end of `n` and
landing on the right end of `reversed_value`. Like passing
beads off one string and onto another.
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
        "confusion_notes": [
            {
                "question": "Why does `reversed_value * 10 + last_digit` actually shift things left?",
                "answer": r'''
Multiplying any integer by 10 moves every one of its digits one
position to the left in base 10, and writes a fresh `0` in the
new rightmost position. That `0` is the slot we are about to fill
with our new digit.

Walk through it slowly. Suppose `reversed_value` is `49`. Now do
`49 * 10`. The result is `490`. Notice what happened: the `4` slid
from the tens column into the hundreds column, the `9` slid from
the ones column into the tens column, and a fresh `0` appeared in
the ones column. That zero is the empty parking spot.

Now add `last_digit`, say `8`. `490 + 8 = 498`. The `8` slipped
into the empty ones slot. No digits were disturbed; we simply
filled a hole.

This is exactly how humans build numbers from left to right when
writing them out — you write the most significant digit first, and
each new digit you add gets a fresh place value of `× 10⁰`. The
formula `new = new * 10 + digit` is the mechanical version of that
intuition.

You can change the base if you ever need to. In binary, "shift
left by one bit" is `* 2`, and you add a new bit using `* 2 + bit`.
In hex, it is `* 16 + hex_digit`. The structure is the same, only
the base plugs in.
''',
            },
            {
                "question": "Why do we need a separate `sign` variable?",
                "answer": r'''
Because Python's floor division and modulo behave **unintuitively**
on negative numbers, and we want a clean loop.

Try `(-7) % 10` in Python and you might be surprised: the result
is `3`, not `-7` or `-3`. That is because Python defines `%` so
the result has the same sign as the **divisor** (which is `+10`
here). And `(-7) // 10` is `-1`, not `0`.

If we let our loop run on a negative number, those quirks make the
digit-extraction logic ugly. The cleanest workaround is the one
you see in the code: pull off the sign at the top, work on the
absolute value, then re-apply the sign at the end.

```python
sign = -1 if n < 0 else 1
n = abs(n)
# ... loop on the non-negative n ...
return sign * reversed_value
```

This pattern — "remember the sign, work on the absolute value,
re-apply at the end" — comes up again in any digit-manipulation
problem that has to support negatives: atoi, sum of digits,
Armstrong on signed input, and so on. Worth memorizing as a small
boilerplate.

(If your input is guaranteed non-negative, like in most of the
beginner problems, you can skip the sign machinery entirely.)
''',
            },
            {
                "question": "What happens with trailing zeros like `1200`?",
                "answer": r'''
They silently disappear, and that is the correct behavior for
integer reversal.

Walk through `n = 1200`:

- Iteration 1: `last_digit = 0`, `reversed_value = 0 * 10 + 0 = 0`,
  `n = 120`.
- Iteration 2: `last_digit = 0`, `reversed_value = 0 * 10 + 0 = 0`,
  `n = 12`.
- Iteration 3: `last_digit = 2`, `reversed_value = 0 * 10 + 2 = 2`,
  `n = 1`.
- Iteration 4: `last_digit = 1`, `reversed_value = 2 * 10 + 1 = 21`,
  `n = 0`.

Loop ends, return `21`.

The two leading zeros never appear in the output because integers
do not store leading zeros. `0021` and `21` are the same integer;
the way you wrote it on paper is just a notational choice. Our
function returns the *integer* `21`, which is mathematically
correct.

If a problem specifically asks for "the reversed digits as a
string of exactly the same length as the input," you should
convert to a string and reverse the characters instead. That
preserves the leading zeros because they are characters, not
quantities. The two operations are different — choose based on
what the problem actually wants.
''',
            },
            {
                "question": "What about integer overflow in 32-bit languages?",
                "answer": r'''
In Python, this is a non-issue because Python integers are
**arbitrary precision** — they can grow to any size that fits in
memory. So reversing a huge integer like `9876543210123456789`
just works.

But many interview platforms (and the original LeetCode problem)
require you to **return 0 if the reversed value overflows a
32-bit signed integer**. The 32-bit range is `[-2³¹, 2³¹ - 1] =
[-2147483648, 2147483647]`. Reversing `1534236469` gives
`9646324351`, which is bigger than `2147483647`. So you must
return 0 instead.

The check is one line at the end:

```python
INT_MIN, INT_MAX = -(2**31), 2**31 - 1
if not (INT_MIN <= reversed_value * sign <= INT_MAX):
    return 0
return reversed_value * sign
```

In C++ / Java you have to check **inside** the loop, *before*
each `* 10 + digit`, because the multiplication itself can
overflow. The Python version dodges that pain because the
arithmetic never fails — only the final range check matters.

The general lesson: when porting a Python solution to a typed
language, every `* 10 + digit` step is a potential overflow site.
Add a defensive check.
''',
            },
            {
                "question": "Could I just do `int(str(n)[::-1])` instead?",
                "answer": r'''
Yes! And in production code, that is often the cleanest answer.

```python
def reverse_number(n: int) -> int:
    sign = -1 if n < 0 else 1
    return sign * int(str(abs(n))[::-1])
```

`str(abs(n))` turns `1200` into the string `"1200"`. The slice
`[::-1]` reverses the string to `"0021"`. `int(...)` parses it
back into the integer `21`, which automatically drops the leading
zeros. Then we re-apply the sign.

It is short, correct, and trivially fast.

So why do we even write the arithmetic version? Two reasons.

First, **it is the version interviewers want to see**. The point
of the question is usually to verify that you can manipulate
digits with arithmetic, not to verify that you know Python's
slice syntax. The string version dodges the algorithm and shows
the interviewer the convenience method instead of the underlying
idea.

Second, **the arithmetic version is the foundation of harder
problems**. Once you know how to do `new = new * 10 + digit`, you
can solve "atoi" (parse a string of digits into an integer),
"palindrome number without converting to string," "Armstrong
number," and many others. The string trick is a one-shot answer
to one specific question. The arithmetic loop is a tool.

So in real code: use the string version if you do not care about
the journey. In learning code: write the arithmetic version, then
treat the string version as the "Pythonic shortcut" you reach for
once you have proven you understand the underlying machinery.
''',
            },
        ],
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
        "what_this_teaches": (
            "How a previously-solved sub-problem becomes a building "
            "block for the next one. *Reverse the number* is the verb; "
            "*compare against the original* is the question. Once you "
            "have the verb, the question is one line."
        ),
        "pattern": "Reverse and compare; reuse the previous routine as a subroutine.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["count-digits", "reverse-number"],
        "next_problems": [
            "armstrong-number",
            "ll-palindrome",
            "longest-palindromic-substring",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 1 (Basic Maths)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 9 — Palindrome Number",
                "url": "https://leetcode.com/problems/palindrome-number/",
            },
        ],
        "understanding": r'''
Let's slow down and think about what *palindrome* means before we
write any code.

A palindrome is anything that reads the same in both directions —
the word `level`, the sentence "Madam, I'm Adam," or the number
`121`. For numbers, palindrome means: if you read the digits left
to right and then right to left, you see the same sequence. So
`121` is a palindrome (reading both ways gives `1, 2, 1`). `1221`
is a palindrome (`1, 2, 2, 1`). `123` is not (`1, 2, 3` versus
`3, 2, 1`).

Most versions of this problem declare that **negative numbers are
not palindromes**, by convention. The reasoning: the minus sign is
part of the number in some sense, but it does not have a partner
on the other end. So `-121` reads as `-, 1, 2, 1` forwards and
`1, 2, 1, -` backwards — and the minus would have to magically
appear on the right, which we do not allow. Different problems
disagree on this rule, but for this problem we follow the
standard LeetCode convention: negatives return `False`.

Now the beautiful part. The question *"is this number a
palindrome?"* is mathematically identical to *"is this number
equal to its own reverse?"*. And we already solved the
sub-problem of reversing a number in the previous problem! So we
can write the palindrome check as a tiny, one-line composition on
top of the reversal routine.

This is one of the smallest but most important moves in algorithm
design: **reuse what you already built**. Whenever you face a new
problem, ask if part of it is something you have already solved.
Often you can write the new function as one line of glue on top
of the old one.
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
            "walkthrough": r'''
Let's read this line by line. Most of the heavy lifting was
done in the previous problem (Reverse a Number) — this one
just adds a comparison at the end.

**`def is_palindrome_number(n: int) -> bool:`** — Takes an
integer, returns a boolean (True or False). The `bool` return
type is your signal that this is a yes/no question.

**`if n < 0: return False`** — Negative numbers can't be
palindromes by the typical convention. Why? Because the minus
sign would have to match the rightmost digit when "reversed,"
and digits don't equal minus signs. `-121` reversed conceptually
would be `121-` which isn't a valid number representation. We
declare them non-palindromes and move on.

**`original = n`** — Stash the original value. We're about to
mutate `n` inside the loop (dividing by 10 each iteration), so
we save a copy first. This is the **most-forgotten line** in
this algorithm; beginners often compare against `n` at the end
and wonder why every input returns True or False incorrectly.
The bug: `n` is zero by then.

**`reversed_value = 0`** — Starting paper for the reversed
number, just like the previous problem.

**`while n > 0:`** — Same loop as Reverse a Number. Walks every
digit of `n`.

**`reversed_value = reversed_value * 10 + n % 10`** — The
shift-and-add we learned in the previous problem. Extracts the
rightmost digit of the current `n` and appends it to the
right of `reversed_value`.

**`n = n // 10`** — Shrink `n` for the next iteration.

**`return reversed_value == original`** — The whole point of
this problem in one line. If reversing the digits gives the
same number we started with, the digits read identically in
both directions, which is the definition of a palindrome. We
return that boolean directly.

Notice how this function is *almost identical* to Reverse a
Number, just with the comparison appended. That's the lesson:
once you have a primitive (`reverse_number`), problems that
depend on it become one line. Senior developers think in
primitives, not in monolithic procedures.
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
        "confusion_notes": [
            {
                "question": "Why do we stash `original = n` before the loop?",
                "answer": r'''
Because the loop **destroys `n`**. Each iteration does
`n = n // 10`, which makes `n` smaller and smaller until it
reaches zero. By the time the loop finishes, `n` is `0` and the
original value is gone.

But the whole point of the algorithm is to compare the reversed
value with the *original* number. If we forget to save the
original first, we end up comparing the reversed value to `0`,
which gives the wrong answer for almost every input.

So we plant `original = n` at the top:

```python
original = n
reversed_value = 0
while n > 0:
    reversed_value = reversed_value * 10 + n % 10
    n = n // 10
return reversed_value == original
```

Now `original` is frozen — Python integers are immutable, so once
we assign `original = n`, the variable `original` will never
change just because we reassign `n` later. We can do whatever we
want to `n` inside the loop, and `original` stays put.

This is a very common pattern: **two variables for two roles**.
One is the *constant* (`original`, never mutated), the other is
the *scratchpad* (`n`, shrinks each iteration). Whenever you
catch yourself wanting to compare the final state against the
initial state, plant a copy of the initial state at the top.
''',
            },
            {
                "question": "Why are negative numbers automatically not palindromes?",
                "answer": r'''
By convention. The standard LeetCode rule is that any negative
number — like `-121` — returns `False`. The reasoning is intuitive
if a little arbitrary: a palindrome should read the same forward
and backward, and the minus sign appears only at the front, never
at the back. `-121` reads as `-, 1, 2, 1` forward and `1, 2, 1, -`
backward. The minus would have to teleport to the right side for
the reading to match, which feels wrong.

You could imagine a different convention where you simply ignore
the sign and check `abs(n)`. Then `-121` would be a palindrome
because `121` is. But that is not the standard rule, and most
interviewers expect you to return `False` for negatives.

Our code handles this with one line at the top:

```python
if n < 0:
    return False
```

Beginners sometimes forget this guard and the loop still
"works" — but the answer is incorrect for negatives because the
arithmetic gets weird (Python's `%` on negative numbers can
produce unexpected positive results, as discussed in the
*Reverse a Number* confusion notes).

The general lesson: read the problem statement for sign
conventions before you start coding. A two-line guard can save
you a wrong-answer submission.
''',
            },
            {
                "question": "Why not just do `str(n) == str(n)[::-1]`?",
                "answer": r'''
You absolutely can! It is correct, fast, and one of the most
Pythonic one-liners possible:

```python
def is_palindrome(n: int) -> bool:
    if n < 0:
        return False
    s = str(n)
    return s == s[::-1]
```

The arithmetic version exists because, in interview settings, the
question is often phrased as *"check if a number is a palindrome
**without converting it to a string**"*. The restriction is
artificial, but it forces you to demonstrate that you understand
digit manipulation with `% 10` and `// 10`. If you reach for
`str(n)` you skip the lesson the problem is trying to teach.

There is also a tiny memory argument: converting to a string
allocates a new string object of length `log₁₀(n)`. The
arithmetic version uses only a couple of integer variables.
*O(1)* extra memory versus *O(d)*. For most inputs the
difference is negligible, but in tightly constrained contexts
(embedded systems, very large numbers) it can matter.

In day-to-day code, prefer the string version for readability.
In interview practice, write the arithmetic version to prove you
understand the math.
''',
            },
            {
                "question": "Is there a way to check without reversing the *whole* number?",
                "answer": r'''
Yes — there is a beautiful "half-reverse" trick. The idea: build
up the reversed value only until it equals or exceeds the
remaining unreversed part. Then compare the two halves.

```python
def is_palindrome_half(n: int) -> bool:
    if n < 0 or (n != 0 and n % 10 == 0):
        return False
    reversed_half = 0
    while n > reversed_half:
        reversed_half = reversed_half * 10 + n % 10
        n = n // 10
    # For odd-length numbers, the middle digit lands in
    # reversed_half; drop it with another // 10.
    return n == reversed_half or n == reversed_half // 10
```

For `n = 12321`, the loop reverses the right half `321` while the
remaining `n` becomes `12`. The middle digit `3` ends up in
`reversed_half`. We then compare `n == reversed_half // 10` to
strip it.

Why bother? In languages with 32-bit integers, the full reversal
of `n` could overflow even though `n` itself fits. The
half-reverse avoids that risk because `reversed_half` never
exceeds the input size. In Python, where integers do not
overflow, this is mostly an academic curiosity.

Interview tip: the full reversal is what most candidates write
and is perfectly acceptable. The half-reversal is what
interviewers love to see *after* you have first explained the
full version. Build up to it.
''',
            },
        ],
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
        "what_this_teaches": (
            "The Euclidean trick — keep replacing a problem with a "
            "strictly smaller version of itself while preserving the "
            "answer. This single pattern collapses an *O(min(a,b))* "
            "brute force into *O(log(min(a,b)))*."
        ),
        "pattern": "Euclidean reduction: gcd(a, b) = gcd(b, a % b).",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["count-digits"],
        "next_problems": [
            "gcd-euclidean",
            "prime-factors",
            "sieve-of-eratosthenes",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 1 (Basic Maths)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "Python docs — math.gcd / math.lcm",
                "url": "https://docs.python.org/3/library/math.html#math.gcd",
            },
        ],
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
            "walkthrough": r'''
Let me walk you through this naive but easy-to-understand
solution.

**`def gcd_brute(a: int, b: int) -> int:`** — Takes two
integers and returns their greatest common divisor.

**`g = 1`** — We initialize our answer to `1`. Why `1`? Because
`1` divides every integer, so we know it's *always* a valid
candidate. By starting here we guarantee we have at least one
answer, even if no bigger common divisor exists.

**`for d in range(1, min(a, b) + 1):`** — The main loop. We
try every possible divisor from `1` up to and including
`min(a, b)`. Why stop at `min(a, b)`? Think about it: a divisor
of `a` cannot be larger than `a` itself. Similarly, a divisor
of `b` cannot be larger than `b`. So a *common* divisor cannot
exceed *either* — meaning it cannot exceed the smaller. That's
why `min(a, b)` is the ceiling.

Note the `+ 1` in `range(1, min(a, b) + 1)` — `range` is
exclusive of its upper bound, so we add 1 to include
`min(a, b)` in the iteration. This is the fence-post detail
we keep meeting.

**`if a % d == 0 and b % d == 0:`** — Test if `d` is a common
divisor of both `a` and `b`. The condition `a % d == 0` says
"the remainder when `a` is divided by `d` is zero," which is
the math definition of "`d` divides `a` evenly." We need this
to be true for both numbers — hence the `and`.

**`g = d`** — Whenever we find a common divisor, we record it.
We don't break out of the loop yet, because we want the
**greatest** common divisor — there might be an even bigger one
later. Since the loop goes upward (`d` increases each
iteration), the *last* common divisor we record is automatically
the largest.

**`return g`** — Hand back the final winner.

This algorithm is *correct* but *slow*. We're doing up to
`min(a, b)` iterations, each with two modulo operations. For
inputs like `a = b = 1_000_000_000`, that's about a billion
operations — way too slow for real use. Euclid's algorithm
(in the optimized section below) cuts this down to about 30
operations for the same input.

The lesson here: linear search through possible answers is a
fine first instinct, but always ask "could the answer space be
exponentially shrunk somehow?" In gcd, the answer is yes.
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
            "walkthrough": r'''
This is one of the most elegant algorithms in computing. Let's
unpack it line by line.

**`def gcd(a: int, b: int) -> int:`** — Same signature as the
brute force.

**`a, b = abs(a), abs(b)`** — Normalize to non-negative values.
The Euclidean algorithm is most cleanly defined on non-negative
integers; for negatives, the GCD is the same as for their
absolute values. The tuple assignment `a, b = ...` is Python's
parallel assignment — both names get their new values
simultaneously, no temporary variable needed.

**`while b != 0:`** — The loop continues as long as `b` is not
zero. When `b` becomes zero, we stop. Why? Because the
mathematical fact behind Euclid's algorithm: `gcd(a, 0) = a` for
any `a`. So once `b` hits zero, `a` holds the answer.

**`a, b = b, a % b`** — Here is the magic line of the entire
algorithm. We simultaneously do two things:

1. Replace `a` with the old `b`.
2. Replace `b` with `a % b` (the remainder of the old `a`
   divided by the old `b`).

This single statement uses Python's tuple-assignment trick:
the right side is evaluated *first* using the old values, then
both names are assigned. So there's no risk of overwriting `a`
before computing `a % b`.

**Why does this work?** Because of Euclid's theorem:
`gcd(a, b) = gcd(b, a mod b)`. Each iteration replaces `(a, b)`
with `(b, a % b)` — same GCD, smaller numbers. The numbers
shrink rapidly (you can prove they roughly halve every two
iterations), so the loop runs in *O(log(min(a, b)))* steps.

**`return a`** — When `b` is zero, `a` is the GCD.

Now the LCM helper.

**`def lcm(a: int, b: int) -> int:`** — Compute least common
multiple.

**`if a == 0 or b == 0: return 0`** — Edge case. LCM with zero
is zero by convention.

**`return abs(a // gcd(a, b) * b)`** — Compute LCM via the
identity `a * b = gcd(a, b) * lcm(a, b)`, rearranged to
`lcm = (a * b) / gcd(a, b)`. We use `//` for integer division.

Notice the order: `a // gcd(a, b) * b`, not `a * b // gcd(a, b)`.
Why? In Python it doesn't matter (integers are unbounded), but
in languages like C++ and Java with 32-bit or 64-bit integer
limits, `a * b` might overflow even though the final answer
fits. Dividing first by the GCD keeps the intermediate value
smaller. It's a habit worth keeping even in Python.

The `abs(...)` wrapper handles any lingering sign issues.

That's the whole algorithm: about three lines of real work,
yet it's one of the oldest algorithms in mathematics (Euclid
wrote it in his *Elements* around 300 BC). The shrink-by-
remainder pattern reappears in many later algorithms.
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
        "confusion_notes": [
            {
                "question": "Why does the algorithm terminate? It looks like it could loop forever.",
                "answer": r'''
Look at the loop carefully:

```python
while b != 0:
    a, b = b, a % b
```

Each iteration, `b` is replaced by `a % b`. The remainder
`a % b` is *strictly less than `b`*, always. (That is the
definition of remainder: it is the part left over after dividing,
so it must be smaller than the divisor.) Since `b` is a
non-negative integer and shrinks every step, it eventually
reaches `0` and the loop exits.

This is exactly the kind of **decreasing variant** we talked
about in `count-digits`: a quantity that strictly shrinks each
iteration and is bounded below by zero. Whenever you have one,
you have a proof that the loop terminates.

Actually, the convergence is much faster than it looks. There is
a classical theorem (Lamé's theorem) that the number of
Euclidean steps for inputs of size `n` is at most about
`5 * log₁₀(n)`. So even for `n` in the trillions, you finish in
about 60 steps. That is the *O(log n)* time complexity in
action.
''',
            },
            {
                "question": "Why does `gcd(a, b) = gcd(b, a % b)` actually preserve the GCD?",
                "answer": r'''
This is the heart of the algorithm, and it deserves a careful
walk-through.

Suppose `d` divides both `a` and `b`. We want to show that `d`
also divides `a % b`, and vice versa.

By the division algorithm, `a = q * b + r`, where `q` is the
quotient and `r` is the remainder (which is exactly `a % b`).
Rearranging: `r = a - q * b`.

Now, if `d` divides both `a` and `b`, then `d` divides `a` and
`d` divides `q * b` (since `q * b` is just `b` multiplied by an
integer). The difference of two multiples of `d` is also a
multiple of `d`. So `d` divides `a - q * b = r`. Therefore `d`
divides both `b` and `r`.

The reverse direction: if `d` divides both `b` and `r`, then `d`
divides `q * b + r = a`. So `d` divides `a` and `b`.

Conclusion: the set of common divisors of `(a, b)` is exactly
the set of common divisors of `(b, a % b)`. Since both sets are
the same, their largest element (the GCD) is the same. The
replacement preserves the answer.

This is a small but glorious example of the **invariant
argument** in mathematics: every transformation preserves the
quantity you care about, and the transformations also drive the
problem toward something trivial (here, `gcd(x, 0) = x`). The
algorithm is correct because of the invariant; it is fast
because of the shrinking.
''',
            },
            {
                "question": "Why divide before multiplying in the LCM formula?",
                "answer": r'''
The mathematical identity is `lcm(a, b) = (a * b) / gcd(a, b)`.
In Python you can write this either as

```python
return (a * b) // gcd(a, b)
```

or as

```python
return a // gcd(a, b) * b
```

Both are mathematically equivalent, but the second one avoids
computing the (potentially huge) product `a * b`. In Python it
does not matter because integers are arbitrary precision. But in
C++/Java/Go with fixed-width integers, `a * b` can overflow even
if the final `lcm` fits comfortably.

The habit `a // gcd(a, b) * b` says: first divide `a` by the GCD
(which definitely fits, since it is at most `a` itself), then
multiply by `b`. This keeps the intermediate value small.

It is a small habit but a worthwhile one. If you ever port your
Python solution to a typed language, this rewrite is the
difference between "works on the test cases" and "overflows on
edge cases."
''',
            },
            {
                "question": "What is `gcd(0, 0)`? And `gcd(0, n)`?",
                "answer": r'''
By convention:

- `gcd(0, n) = n` for any positive `n`. Because every positive
  integer divides `0` (`0 = 0 * n` for any `n`), so the set of
  common divisors of `0` and `n` is just the divisors of `n`,
  and the largest is `n` itself.
- `gcd(0, 0) = 0`. There is no greatest common divisor here in
  a strict sense — every integer divides zero — but `0` is the
  standard convention because it makes the algebra work out.

Our loop handles both correctly. If you call `gcd(0, 5)`:

- Iteration: `a, b = 5, 0 % 5 = 0`. Loop exits because `b == 0`.
- Return `a = 5`. Correct.

If you call `gcd(0, 0)`:

- Loop condition `b != 0` is false immediately.
- Return `a = 0`. Correct.

For LCM, the convention is `lcm(0, n) = 0` (because zero is a
multiple of everything). Our code returns `0` explicitly when
either argument is zero, dodging the divide-by-zero that
`lcm = (a*b) // gcd(a, b)` would produce when `gcd` is zero.
''',
            },
        ],
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
        "what_this_teaches": (
            "The divisor-pairing fact — divisors come in pairs that "
            "multiply to `n`, mirrored around `sqrt(n)` — which lets us "
            "test primality in `O(sqrt(n))` instead of `O(n)`. This is "
            "the seed for every divisor-enumeration optimization."
        ),
        "pattern": "Trial division up to `sqrt(n)`, using the pair `(i, n // i)`.",
        "prerequisite_lessons": [],
        "prerequisite_problems": ["count-digits"],
        "next_problems": [
            "print-all-divisors",
            "prime-factors",
            "sieve-of-eratosthenes",
            "segmented-sieve",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 1 (Basic Maths)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "GeeksforGeeks — Primality Test (Basic and School Methods)",
                "url": "https://www.geeksforgeeks.org/primality-test-set-1-introduction-and-school-method/",
            },
        ],
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
            "walkthrough": r'''
Let's walk through this slowly. This algorithm is direct
translation of the definition of "prime number" into code.

**`def is_prime_brute(n: int) -> bool:`** — Takes an integer,
returns True or False.

**`if n < 2: return False`** — The definition of prime requires
`n > 1`. By convention, 0, 1, and negative numbers are not
prime. We catch these cases first and return False, because
the loop below would either give a wrong answer or run zero
times.

**`for d in range(2, n):`** — Try every potential divisor from
`2` up to `n - 1`. Why start at `2`? Because `1` divides
everything; if we tested `d = 1`, the check `n % d == 0` would
always be true and we'd wrongly conclude every number is
composite. And why stop at `n - 1`? Because `n` itself divides
`n` evenly, so testing `d = n` would also be a false alarm.
The valid "non-trivial" divisors live in the range `(1, n)`
exclusive — exactly what `range(2, n)` gives us.

**`if n % d == 0:`** — Test whether `d` divides `n` evenly.
The modulo operator returns the remainder; if the remainder is
zero, division is exact.

**`return False`** — As soon as we find *any* non-trivial
divisor, we know `n` is composite. There's no need to keep
looking — return False immediately. This is called "early
exit" and it's a common pattern.

**`return True`** — If the loop completes without finding any
divisor, then `n` has no non-trivial divisors. Its only
divisors are 1 and itself. That's the definition of prime;
return True.

This is *O(n)* time. For small inputs it's fine. For
`n = 1,000,000,000`, this would require a billion iterations,
each doing a modulo. Way too slow. The optimized version
brings this down to about 30,000 iterations using a beautiful
mathematical insight (see below).
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
            "walkthrough": r'''
Let's read this optimized version. It has several small tricks
that compound into a dramatically faster algorithm.

**`def is_prime(n: int) -> bool:`** — Same signature.

**`if n < 2: return False`** — Same edge case as before. 0, 1,
and negatives are not prime.

**`if n < 4: return True`** — Handle the small primes 2 and 3
explicitly. Why a separate case? Because the upcoming
optimization tests *odd* numbers starting at 3 and the *even*
divisor 2 is handled separately. If we didn't special-case 2
and 3, the algorithm would skip them.

**`if n % 2 == 0: return False`** — Eliminate even numbers in
one shot. Every even number greater than 2 is composite (it
has 2 as a divisor besides 1 and itself). By removing all
evens here, we avoid wasting iterations on them later.

**`i = 3`** — We start testing divisors at 3. We've already
handled the case `d = 2` (by checking `n % 2`), so we start
at the next odd number.

**`while i * i <= n:`** — This is the killer optimization. The
condition says "while `i` squared is at most `n`," which is
equivalent to "while `i` is at most `sqrt(n)`." We avoid
calling `math.sqrt(n)` explicitly because:
1. It's slightly slower than multiplication.
2. It returns a float, introducing potential precision errors.
3. Squaring `i` is exact integer arithmetic.

But why is `sqrt(n)` the right stopping point? Here's the
beautiful argument: if `n` has any non-trivial divisor `d`,
then `n / d` is also a divisor. One of these two must be at
most `sqrt(n)`. (Because if both were greater than `sqrt(n)`,
their product would exceed `n`, contradiction.) So if no
divisor exists up to `sqrt(n)`, no divisor exists at all. We
only need to scan to `sqrt(n)`, not to `n`. This cuts the
work from *O(n)* to *O(sqrt(n))* — a billion becomes 30,000.

**`if n % i == 0: return False`** — Same check as before.
Found a divisor? Composite.

**`i += 2`** — Increment by 2 to skip the even numbers (which
can't be prime divisors of an odd `n` — if `n` is odd, no
even divides it). This roughly halves the inner-loop work.

**`return True`** — If we got here, no divisor was found.
Prime.

So the optimized version has three layers of speedup over the
brute force:
1. Stop at `sqrt(n)` instead of `n`. (Biggest win.)
2. Skip all even candidates. (Constant-factor 2x.)
3. Use `i * i <= n` instead of `math.sqrt`. (Tiny win, but
   safer numerically.)

Combined, this is the standard interview-grade primality test.
For inputs up to about 10^12 it runs in microseconds.
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
        "confusion_notes": [
            {
                "question": "Why is it enough to check divisors up to `sqrt(n)`? Don't we miss the big ones?",
                "answer": r'''
We do not miss them, because **divisors come in pairs**. Every
divisor `d` of `n` has a partner `n // d`, and their product is
exactly `n`.

Picture the divisors of 36: they are 1, 2, 3, 4, 6, 9, 12, 18,
36. Look at the pairs that multiply to 36:

```
1 × 36 = 36
2 × 18 = 36
3 × 12 = 36
4 ×  9 = 36
6 ×  6 = 36
```

Every pair has one member at or below `sqrt(36) = 6` and one
member at or above `sqrt(36) = 6`. They are mirror images of
each other around the square root.

So if we scan divisors `i` from 1 up to `sqrt(n)`, and we find
even one divisor in that range (other than 1), we have implicitly
also found its partner `n // i` on the other side. We do not
need to scan past `sqrt(n)` because anything we would find there
is the partner of something we already found.

For prime checking: if no divisor exists in `[2, sqrt(n)]`, then
no divisor exists in `(sqrt(n), n)` either, because any such
divisor would have its partner in `[2, sqrt(n)]` — which we just
checked. So `n` is prime.

The fence-post version: divisors of `n` are *symmetric around
`sqrt(n)`*. You only need to look on one side.
''',
            },
            {
                "question": "Why `i * i <= n` instead of `i <= math.sqrt(n)`?",
                "answer": r'''
Two reasons. One is correctness, one is style.

**Correctness**: `math.sqrt(n)` returns a floating-point number,
and floats are not exact. For huge `n` near a perfect square,
`math.sqrt(n)` can return a value that is just slightly off,
causing the loop to stop one iteration too soon (and miss a
divisor) or one too late. `i * i <= n` is pure integer
arithmetic, exact every time.

**Style / speed**: `i * i` avoids a call to `math.sqrt`. Function
calls in Python are slow compared to integer multiplication. For
a tight inner loop, this matters.

The two forms are mathematically equivalent (`i <= sqrt(n)`
exactly when `i * i <= n` for non-negative `i`), but the
integer-only version is universally preferred in DSA code. Burn
it into your fingers — it shows up in many problems.
''',
            },
            {
                "question": "Why do we handle 2 separately and then only test odd numbers?",
                "answer": r'''
Because once you have ruled out 2 as a factor, **no even number
can ever be a factor** of `n` either. Every even number is
divisible by 2; if 2 does not divide `n`, then 4, 6, 8, ...
cannot divide `n` either.

So testing every even number above 2 is wasted work. We test 2
explicitly, eliminate it (or accept it), then jump to 3 and
increment by 2 from there.

This roughly halves the number of trial divisions. The
asymptotic complexity stays *O(sqrt(n))*, but the **constant
factor** improves by 2×. Worth it for one extra line of code.

You can take this even further with a "wheel" — eliminate
multiples of 2, 3, 5, etc. — but each step has diminishing
returns. The 2-only optimization is the sweet spot for hand-written
primality tests.
''',
            },
            {
                "question": "What about 0, 1, and negatives? Are they prime?",
                "answer": r'''
**Negative numbers**: not prime, by definition. Primes are
positive integers.

**Zero**: not prime. Zero is divisible by every nonzero integer,
so it has infinitely many divisors — far more than the two that
primes are allowed.

**One**: not prime, despite many beginners thinking it is. The
definition of prime requires *exactly two* distinct positive
divisors: 1 and itself. The number 1 has only one positive
divisor — itself, which equals 1. So 1 fails the "exactly two"
clause.

The exclusion of 1 is not arbitrary mathematical pedantry. If
you allowed 1 to be prime, every integer would have infinitely
many "prime factorizations" (`12 = 2 × 2 × 3 = 1 × 2 × 2 × 3 = 1
× 1 × 2 × 2 × 3 = ...`), and the **fundamental theorem of
arithmetic** would lose its uniqueness statement. So we exclude
1 from primes to keep factorizations unique.

Our code handles all three cases with the same guard:

```python
if n < 2:
    return False
```

`n < 2` catches `n = 0`, `n = 1`, and every negative integer.
One line, all three edge cases. Clean.
''',
            },
        ],
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
        "what_this_teaches": (
            "The two flavours of basic recursion — *delegate then act* "
            "versus *act then delegate* — and how the relative order "
            "of the recursive call and the work decides whether the "
            "output comes out forward or backward."
        ),
        "pattern": "Recursive delegation: trust the smaller call, add one action around it.",
        "prerequisite_lessons": ["recursion"],
        "prerequisite_problems": [],
        "next_problems": [
            "print-n-to-1",
            "sum-first-n",
            "factorial-of-n",
            "fibonacci-number",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 1 (Basic Recursion)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
        ],
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
        "confusion_notes": [
            {
                "question": "How can the recursive call print 1, 2, 3, ..., N-1 *before* I have written the code to do that?",
                "answer": r'''
This is the single biggest mental hurdle in recursion, and the
answer is what experienced programmers call the **leap of
faith**.

Here is the trick: when you are writing a recursive function,
**you are allowed to assume that the function works correctly
for any smaller input, even before you finish writing it.** This
sounds like cheating. It is not. It is the deal that recursion
asks you to make.

Concretely: when you write `print_1_to_n(n - 1)` inside the body
of `print_1_to_n`, you are saying: *"I trust that, by the time
this call returns, it will have printed 1, 2, 3, ..., n - 1
correctly."* You do not look inside the call. You do not trace
through it. You just trust it.

The reason this trust is justified is **induction**. We prove
correctness for the smallest case (the base case) by hand. We
then assume correctness for `n - 1` and show that the body
correctly extends it to `n`. By the principle of mathematical
induction, the function is correct for all `n`.

In day-to-day coding, you do not write proofs. You just take the
leap. The mental motion is: *"Imagine someone hands me the
answer for `n - 1`. What do I do with it to get the answer for
`n`?"* That one extra step is what you write.

If this feels strange, that is normal. It feels strange to
everyone the first ten times. After the eleventh, it stops
feeling strange and starts feeling like the most natural way to
think about certain problems.
''',
            },
            {
                "question": "Why does the base case `if n <= 0: return` not break everything?",
                "answer": r'''
The base case is the floor. Without it, the recursion would
never stop — we would call `print_1_to_n(0)`, then
`print_1_to_n(-1)`, then `print_1_to_n(-2)`, forever. Python
would eventually crash with `RecursionError: maximum recursion
depth exceeded`.

The base case says: *"For inputs at or below this threshold,
the answer is trivial — just return without doing anything."*
For `n = 0`, the request "print numbers 1 to 0" is asking us to
print an empty sequence, which means do nothing. So returning
immediately is correct.

Notice that the base case is **not** about correctness of the
algorithm; it is about **termination**. The algorithm itself
would be correct in spirit even without a base case, but it
would loop forever. Every recursion needs a base case for the
same reason every loop needs a stopping condition.

A subtle issue: the base case must be reached *eventually*. The
recursive call `print_1_to_n(n - 1)` makes `n` strictly smaller
each step, and the base case fires when `n` drops to 0 or below.
So termination is guaranteed for any starting `n`. If you ever
write recursion where the argument might not shrink, or might
shrink in the wrong direction, you have a bug.
''',
            },
            {
                "question": "Why is the call stack `O(N)`? Doesn't recursion use no memory?",
                "answer": r'''
Each recursive call creates a new **stack frame** — a small
chunk of memory that holds the local variables of that call,
plus a return address pointing to where execution should resume
when the call finishes.

For `print_1_to_n(5)`, Python pushes a stack frame for `n = 5`.
That frame then calls `print_1_to_n(4)`, which pushes another
frame. And so on, until `print_1_to_n(0)` returns. At the moment
the base case fires, there are five frames stacked up. Only
then do they start unwinding, one by one.

So even though the algorithm "feels" linear and we are not
explicitly allocating any data structure, there is still *O(n)*
hidden memory cost in the call stack.

This matters for two practical reasons. First, Python has a
default recursion limit of around 1000. If `n` is 10,000, your
recursive function crashes with `RecursionError` before it gets
near the base case. Second, on memory-constrained devices, deep
recursion eats stack memory and can cause a stack overflow
crash.

Most curriculum problems use small `n` so this is fine. But
remember: recursion is not magically free. It pays in stack
depth what an iterative solution would have paid in extra
variables.
''',
            },
            {
                "question": "Why do `recurse-then-print` and `print-then-recurse` give different orders?",
                "answer": r'''
This is the most beautiful subtlety in basic recursion, and it
unlocks understanding of preorder vs postorder traversals later.

Look at `recurse-then-print` for `n = 3`:

```
print_1_to_n(3):
  print_1_to_n(2):
    print_1_to_n(1):
      print_1_to_n(0):    # base case, does nothing
      print(1)
    print(2)
  print(3)
```

The print statements happen as the recursion **unwinds** — that
is, as the calls return from deepest to shallowest. The deepest
call (`n = 1`) prints first because it returns first. Output:
`1, 2, 3`.

Now flip the order to `print-then-recurse`:

```
print_n_to_1(3):
  print(3)
  print_n_to_1(2):
    print(2)
    print_n_to_1(1):
      print(1)
      print_n_to_1(0):    # base case, does nothing
```

The prints happen as the recursion **dives down**, before the
recursive call. The shallowest call (`n = 3`) prints first.
Output: `3, 2, 1`.

The deep pattern hiding here: a recursive function has two
*moments* — the moment before the recursive call (the "way down")
and the moment after (the "way up"). Anything you put before the
call happens top-down; anything you put after happens bottom-up.

Trees have the same dichotomy under different names:
**preorder** is "do the work before recursing"; **postorder** is
"do the work after recursing." Same idea, same recursion
mechanism, different name. Once you see it here, you see it
everywhere.
''',
            },
        ],
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
        "what_this_teaches": (
            "How a recursive *mathematical definition* translates one "
            "line at a time into a recursive function. Factorial is "
            "the prototype: the math says `n! = n * (n-1)!`, and the "
            "code says `return n * factorial(n - 1)`."
        ),
        "pattern": "Translate a self-referential math definition into a recursive call.",
        "prerequisite_lessons": ["recursion"],
        "prerequisite_problems": ["print-1-to-n"],
        "next_problems": [
            "fibonacci-number",
            "pow-x-n",
            "count-good-numbers",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 1 (Basic Recursion)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "Python docs — sys.setrecursionlimit",
                "url": "https://docs.python.org/3/library/sys.html#sys.setrecursionlimit",
            },
        ],
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
        "confusion_notes": [
            {
                "question": "Why is `0! = 1`? Shouldn't it be 0 or undefined?",
                "answer": r'''
By convention, `0!` is defined to be `1`. The convention exists
because it makes a huge number of formulas work out cleanly. The
two best ways to understand it are:

**Combinatorial reason**: `n!` counts the number of ways to
arrange `n` distinct items in a row. How many ways are there to
arrange zero items? Exactly one — the empty arrangement. There
is one (and only one) way to "do nothing." So `0! = 1`.

**Recursive reason**: the recurrence `n! = n * (n - 1)!` works
for `n = 1` only if `0! = 1`, because `1! = 1 * 0! = 1 * 1 = 1`,
which matches the expected `1! = 1`. If we tried `0! = 0`, we
would get `1! = 0`, which contradicts the standard definition.
So `0! = 1` is what makes the recurrence consistent.

The same convention extends to combinatorics: `C(n, 0) = n! /
(0! * n!) = 1`, which says "there is exactly one way to choose
zero items," again matching intuition.

In code we usually combine the bases:

```python
if n <= 1:
    return 1
```

This handles both `0! = 1` and `1! = 1` in one line.
''',
            },
            {
                "question": "Why does Python crash on `factorial(2000)` even though the math is straightforward?",
                "answer": r'''
Because Python imposes a **recursion depth limit** to protect
itself from runaway recursion.

Every recursive call consumes one slot in Python's call stack.
By default, the stack can hold about 1000 frames. When
`factorial(2000)` makes the 1001st call, Python aborts with
`RecursionError: maximum recursion depth exceeded`.

This is a Python design choice, not a mathematical limitation.
The math for `factorial(2000)` works perfectly — it produces a
gigantic integer with thousands of digits. The problem is
mechanical: too many nested function calls.

Three ways to fix it:

1. **Raise the limit** with `sys.setrecursionlimit(10000)`. Works
   but risky — if you set it too high, you can crash the entire
   Python interpreter with a real stack overflow at the OS level.
2. **Switch to iteration**:
   ```python
   result = 1
   for k in range(2, n + 1):
       result *= k
   ```
   No call stack, no limit. This is what production code does.
3. **Convert recursion to a loop with an explicit stack**. Useful
   for tree / graph problems where the recursion structure is
   complex.

The general lesson: recursion is wonderful for *expressing*
algorithms, but if the depth might be huge, prefer iteration.
The same lesson applies to deep tree traversal, long linked
lists, and DP problems with large state spaces.
''',
            },
            {
                "question": "Why does the base case use `n <= 1` instead of `n == 0`?",
                "answer": r'''
Both work, but `n <= 1` is the more careful choice for two
reasons.

First, it handles `0! = 1` and `1! = 1` together. Mathematically,
`1! = 1 * 0! = 1 * 1 = 1`, so the recursion *would* terminate
correctly at `n == 0` anyway. But explicitly returning at `n =
1` saves one function call per invocation, which is a tiny
optimization.

Second and more importantly, it guards against accidentally
passing a negative input. If you write `if n == 0: return 1` and
someone calls `factorial(-3)`, the recursion will infinitely
loop downward (`factorial(-3)` → `factorial(-4)` → ...) and
crash with `RecursionError`. The condition `n <= 1` catches all
negatives too, returning `1` immediately. Whether `1` is the
"right" answer for negative input is debatable (it really should
raise an error), but at least the function does not crash.

If you want to be strict about input validation, add an explicit
guard:

```python
if n < 0:
    raise ValueError("factorial undefined for negative input")
if n <= 1:
    return 1
return n * factorial(n - 1)
```

For curriculum problems, the simpler `n <= 1` is usually
sufficient.
''',
            },
            {
                "question": "Could `n!` actually overflow in Python like in C++?",
                "answer": r'''
No — Python integers are **arbitrary precision**, so they can
grow to any size that fits in available memory. `factorial(100)`
in Python returns the exact 158-digit number with no problem.

In C++ or Java, factorial overflows quickly. A 32-bit signed
integer can hold values up to about `2.1 * 10^9`. `12!` is
about `4.8 * 10^8` (fits), `13!` is about `6.2 * 10^9` (does
not fit, overflows silently). So C++ programmers learn to be
paranoid about factorials early.

In Python you can compute `factorial(1000)` and get an exact
answer. The math just works. But beware: those huge numbers
consume real memory, and arithmetic on them is slower than on
machine-word integers. For numerical algorithms involving
factorials of large `n`, you often want to work in modular
arithmetic (`n! mod p`), use Stirling's approximation, or use
the `math.lgamma` log-gamma function — none of which suffer the
size explosion.

For interview problems, Python's arbitrary precision is a real
luxury. Use it without worry, but know that the C++/Java answer
to "compute factorial mod p" requires an explicit `% p` after
every multiplication.
''',
            },
        ],
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
        "what_this_teaches": (
            "The first real efficiency lesson in DSA: a perfectly "
            "correct recursive algorithm can be *catastrophically* "
            "slow if it solves the same subproblem more than once. "
            "Remembering each subproblem's answer (memoization) is "
            "the single most important idea behind dynamic programming."
        ),
        "pattern": "Overlapping subproblems → memoize or tabulate.",
        "prerequisite_lessons": ["recursion", "dp"],
        "prerequisite_problems": [
            "print-1-to-n",
            "factorial-of-n",
        ],
        "next_problems": [
            "climbing-stairs",
            "frog-jump",
            "house-robber-i",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 1 (Basic Recursion)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "LeetCode 509 — Fibonacci Number",
                "url": "https://leetcode.com/problems/fibonacci-number/",
            },
            {
                "label": "Python docs — functools.lru_cache",
                "url": "https://docs.python.org/3/library/functools.html#functools.lru_cache",
            },
        ],
        "understanding": r'''
The Fibonacci sequence is a small mathematical pattern with an
oversized reputation. Its definition is wonderfully self-referential:

> `F(0) = 0`, `F(1) = 1`, and for every `n ≥ 2`, `F(n) = F(n - 1) + F(n - 2)`.

In plain English: start with two seed values, `0` and `1`. Every
later number in the sequence is the **sum of the two numbers just
before it**. So the sequence unfolds as `0, 1, 1, 2, 3, 5, 8, 13,
21, 34, 55, 89, ...` — a slow walk where every step adds the
previous two footprints together.

The problem itself is simple. We are given an integer `n` and we
have to return `F(n)`. For `n = 0` we return `0`. For `n = 5` we
return `5`. For `n = 10` we return `55`. That is the entire
problem statement.

So why is this in the curriculum? Because Fibonacci is the
*single best* teaching example for the most important efficiency
idea in DSA. It is the place where every beginner first feels in
their bones that **correct does not always mean fast**, and that
the fix is not cleverness — it is *memory*.

You will write the most natural recursive solution, you will run
it for `n = 40` and watch it stall, and at that exact moment of
frustration the next idea — "wait, am I doing the same work over
and over?" — will arrive on its own. That moment is the doorway to
**dynamic programming**.

Treat this problem as a story in three acts:

1. **Act I**: the recursive definition is so direct that writing
   the code feels almost free.
2. **Act II**: you run that code for any moderately large `n` and
   watch it crawl. You realize the recursion tree is enormous
   because the same subproblems are being recomputed many times.
3. **Act III**: you add memory — a cache, an array, or two
   variables — and the algorithm becomes linear. Same idea, same
   recurrence, but now blindingly fast.

By the end you should understand why memoization is not a trick
but a *paradigm*, and you should never again write a naive
recursive Fibonacci.
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
Let's slow down and really see why the naive version is so slow,
because the *feeling* of the slowness is half the lesson.

Pick a small example, `n = 5`. Trace the recursion tree by hand:

```
                fib(5)
              /        \
          fib(4)       fib(3)
          /    \       /    \
       fib(3) fib(2) fib(2) fib(1)
       /   \   / \    /  \
     fib(2)fib(1)...
```

Look at the tree carefully. `fib(3)` shows up **twice**. `fib(2)`
shows up **three times**. `fib(1)` appears even more often. As `n`
grows, the number of times each small `fib(k)` gets recomputed
**explodes**. For `n = 30`, `fib(0)` and `fib(1)` are each
recomputed *over a million times*. Every single one of those calls
returns the same answer. We are burning the CPU on identical
questions.

The mathematician's way of saying this: the number of leaves in
the recursion tree is roughly `φ^n` where `φ ≈ 1.618` is the
golden ratio. For `n = 50` that is about 12 billion leaves. Even at
a billion operations per second, this is going to take seconds. For
`n = 100` it would take many lifetimes.

Now the *aha*. Every time we call `fib(3)`, we get back the same
number: 2. There is no randomness, no input that changes. So the
**second** call is pure waste — we already knew the answer from the
first call. The fix is the most natural thing imaginable: **the
first time we compute `fib(k)`, write it down. Every subsequent
time, just read it.**

This idea has a name: **memoization**. The word looks like
"memorization" with a missing `r`, and that is exactly what it is —
we are *memo*-izing the function, attaching a note to each input
that says "this is the answer; please do not recompute me." With
memoization, every distinct `fib(k)` is computed exactly once.
There are only `n + 1` distinct values to compute (`fib(0)`,
`fib(1)`, ..., `fib(n)`), so the total work drops from exponential
to **linear**.

That one realization — *"don't redo, remember"* — is the entire
soul of dynamic programming. Every DP problem you will ever solve
in Step 16 is, at its core, a recursion plus a sticky note. If you
get this lesson here, in the friendly company of Fibonacci, you
will have an enormous head start when DP arrives in earnest.

There are two flavors of "remember." Both compute the same numbers
and have the same complexity; they differ in style.

1. **Top-down memoization** — keep the recursion exactly as written,
   add a cache, and check the cache before recomputing. In Python
   this is `@lru_cache` applied to the naive function. Read it as
   "the same algorithm, but the function now remembers what it has
   already been asked."

2. **Bottom-up tabulation** — flip the recursion on its head. Start
   from the base cases (`F(0)`, `F(1)`) and build forward, storing
   each `F(k)` as you compute it. By the time you reach `F(n)`,
   everything it needs has already been computed. No recursion, no
   stack frames — just a single loop.

Both are linear. The bottom-up version uses less memory (especially
once you notice you only need the last two values, not the whole
table) and avoids Python's recursion limit. The top-down version
is closer to the recursive definition and easier to write when the
recurrence is complicated. In real interview practice, learn both.
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
Step back from the code and look at the real lesson. Fibonacci is
not the point. The point is the **mental model**: a recursive
algorithm is a tree of subproblems, and whenever that tree has
*repeated* subproblems, the algorithm is silently doing exponential
work where linear would do.

Visually: imagine the recursion tree as a real, physical tree
drawn on a wall. The naive Fibonacci tree is **enormous and
bushy**, with the same small subtree (`fib(2)`, `fib(3)`, ...)
appearing in many different places. Memoization is the act of
**pruning** all those duplicate subtrees down to a single shared
node. The bushy tree collapses into a thin chain of `n` distinct
nodes, each computed once.

That collapse is the entire idea of dynamic programming. Every DP
problem in Step 16 will turn out to be "a recursion whose tree has
overlapping subproblems, with the duplicates pruned by a cache."
The cache might be a dict, an array, a 2D table, a tuple of
booleans — the shape varies. But the underlying move is always
"remember what you have computed; never recompute."

A second deep observation: the bottom-up version uses only two
variables (`prev2` and `prev1`). Why? Because the recurrence
`F(n) = F(n-1) + F(n-2)` looks at only the last two values. We
never need `F(n-3)` again once we have computed `F(n-1)`. So even
though the full table of `n + 1` numbers exists *conceptually*,
the algorithm only ever needs a tiny window of it at any moment.

This shrinking-the-table trick is called **space optimization**
and it shows up everywhere in DP. Many beautiful DP solutions
that look like they need a 2D table actually need only two rows,
or even one row, once you notice which cells the recurrence
touches.

There are even more beautiful facts about Fibonacci that we will
mostly skip — the golden ratio limit `F(n+1)/F(n) → φ ≈ 1.618`,
Binet's closed-form formula, the *O(log n)* matrix-exponentiation
algorithm — but for now the lesson worth carrying forward is:

> *A recursion with overlapping subproblems plus a cache equals
> dynamic programming.*

If that sentence makes sense after Fibonacci, you have done the
work this problem was supposed to teach.
''',
        "confusion_notes": [
            {
                "question": "Why does my naive recursion freeze on fib(50) when the math is so simple?",
                "answer": r'''
Because the recursion tree is exponential in `n`. Even though each
**call** does almost no work, the **number of calls** explodes.

Concretely, the number of leaves in the recursion tree of `fib(n)`
is roughly `F(n + 1)`, which grows like `φ^n` where
`φ ≈ 1.618` is the golden ratio. For `n = 50`, that is about 20
billion. At a billion function calls per second (which is wildly
optimistic for Python), that is *20 seconds of pure call overhead*
— and Python is much slower than that. In practice `fib(40)`
already takes several seconds, and every increase of `n` by 5
multiplies the time by about 10.

The shocking part is that *the math itself is trivial*. There are
only `n + 1` distinct subproblems to compute (`fib(0)`, `fib(1)`,
..., `fib(n)`). If we computed each once and reused the answer,
the whole job would be 50 additions — done in microseconds. The
naive recursion is slow not because Fibonacci is hard but because
**we are computing the same easy answers billions of times**.

This is the gut-punch moment that the problem is designed to
deliver. Once you have felt the slowness, you will never write
unmemoized exponential recursion again without at least asking
"are subproblems overlapping?"
''',
            },
            {
                "question": "What does `@lru_cache` actually do? It feels like magic.",
                "answer": r'''
It is magic, but the magic is small and worth understanding.

`@lru_cache` is a **decorator** from Python's standard
`functools` module. When you put it above a function, Python
wraps your function inside a tiny invisible helper. That helper
keeps a hidden **dictionary** mapping inputs to outputs.

Every time the wrapped function is called, the helper does this:

1. Look at the arguments. Is this input already in the
   dictionary?
2. If yes, return the saved answer immediately — your function
   body never runs.
3. If no, run the original function body, save its return value
   in the dictionary, and then return it.

That is the whole mechanism. There is no AI, no parallelism, no
clever rewriting of your code. It is literally a dictionary look-up
sitting in front of your function.

The "LRU" stands for "least-recently-used" — by default, if you
configure a maximum size, the cache forgets the least-recently-used
entries when it overflows. With `maxsize=None`, the cache grows
without bound (which is what we want for Fibonacci, since there
are only `n + 1` distinct keys).

A quick mental model: think of `@lru_cache` as a personal
assistant who stands beside your function. Every time someone
calls the function, the assistant first checks their notepad. If
the answer is on the notepad, they hand it over immediately and
don't even disturb the function. If not, they let the function
work, then write the new answer on the notepad.

The constraints for `@lru_cache` to work: your function's
arguments must be **hashable** (numbers, tuples, strings — yes;
lists and dicts — no), and your function must be **pure** (same
input always returns same output, no side effects). Fibonacci
meets both of these trivially.

You can absolutely write the same thing by hand if you want to
demystify it:

```python
cache = {}
def fib(n):
    if n in cache:
        return cache[n]
    if n < 2:
        result = n
    else:
        result = fib(n - 1) + fib(n - 2)
    cache[n] = result
    return result
```

That code does **exactly** what `@lru_cache` does, just with the
plumbing exposed. Once you have written it once, the decorator
stops feeling like magic and starts feeling like a convenience.
''',
            },
            {
                "question": "Why do we only need to keep the last two values? Don't we need the whole table?",
                "answer": r'''
Look at the recurrence carefully: `F(n) = F(n - 1) + F(n - 2)`.

The right-hand side mentions only the *previous two* terms. It
does not mention `F(n - 3)`, `F(n - 4)`, or `F(0)`. So once we
have advanced past those values, we never need to read them again.

It is a bit like climbing a staircase by always looking at only
the two steps just behind you. The step you took three moves ago
is no longer useful — you can forget about it without losing any
information.

In the bottom-up loop, this is exactly what we do:

```python
prev2, prev1 = 0, 1
for _ in range(2, n + 1):
    prev2, prev1 = prev1, prev1 + prev2
```

At every iteration, `prev2` holds what was `F(i - 2)` and `prev1`
holds what was `F(i - 1)`. We compute `F(i) = prev1 + prev2`,
then **shift the window**: the new `prev2` becomes the old
`prev1`, and the new `prev1` becomes the value we just computed.
The number two steps back drops off the bottom and is gone
forever.

This is the simplest example of **space optimization** in DP. The
full conceptual table has `n + 1` cells, but at any moment we
only need the most recent two. So the *O(n)* space requirement
collapses to *O(1)*.

The same trick reappears later in Step 16 — climbing stairs uses
two variables, frog jump uses three, house robber uses two. Any
time a recurrence depends on a fixed number of previous values,
you can collapse the table to that many scalars.
''',
            },
            {
                "question": "How does `prev2, prev1 = prev1, prev1 + prev2` work? It looks like it should break.",
                "answer": r'''
This is one of Python's loveliest features, and it is worth
understanding precisely because it surprises everyone the first
time.

The line is a **simultaneous (tuple) assignment**. Python
evaluates the *entire right-hand side first*, then assigns the
results to the variables on the left.

So when Python sees `prev2, prev1 = prev1, prev1 + prev2`, it
does this:

1. **First**, compute the right side as if you were just
   evaluating an expression. The right side is the pair
   `(prev1, prev1 + prev2)`. Both pieces are read using the
   *old* values of `prev1` and `prev2`.
2. **Then**, assign that pair to the left side: the new `prev2`
   gets the first element (the old `prev1`), and the new `prev1`
   gets the second (the old `prev1 + prev2`).

To make this concrete: suppose `prev2 = 0` and `prev1 = 1`. The
right side evaluates to `(1, 0 + 1)`, which is `(1, 1)`. Then
the assignment makes `prev2 = 1` and `prev1 = 1`. Next iteration,
the right side is `(1, 1 + 1) = (1, 2)`, so `prev2 = 1` and
`prev1 = 2`. And so on.

If you tried to write this *without* the simultaneous assignment,
you would need a temporary variable, because the line `prev2 =
prev1` would clobber the old `prev2` before you could read it:

```python
# Without simultaneous assignment — need a temp.
temp = prev1
prev1 = prev1 + prev2
prev2 = temp
```

The simultaneous version is shorter and harder to get wrong. It
appears constantly in Python: swapping two variables (`a, b = b,
a`), maintaining sliding windows, walking two pointers. Internalize
the rule "right side first, then assign," and tuple assignment
becomes a friend instead of a puzzle.
''',
            },
            {
                "question": "Is recursion always slower than iteration?",
                "answer": r'''
No, but there is a kernel of truth to the worry, and it is worth
unpacking.

A recursive function call has more overhead than a loop iteration
in Python. Every call creates a new **stack frame** — a small
package of memory that holds the local variables and the place to
return to when the call finishes. Allocating and freeing that
frame takes time. So function calls are not free.

But that is a *constant-factor* difference, usually tiny. The
**massive** difference between fast and slow Fibonacci is not
"recursion versus iteration" — it is **with-memoization versus
without**. The memoized recursive version is *O(n)*, basically as
fast as the iterative version. The unmemoized recursive version
is *O(φ^n)*, billions of times slower. Both look almost the same
on the page; the cache is the difference.

So the more accurate rule is: **redundant work is what makes you
slow, not the syntax**. A recursion that does no redundant work
is fine. An iteration that recomputes the same thing in every
loop iteration is just as bad as exponential recursion.

A second issue with deep recursion in Python is the **recursion
limit**. Python defaults to a maximum recursion depth of around
1000. If your problem has `n = 10000` and you recurse, you will
crash with `RecursionError`. Iterative solutions avoid this
ceiling. So for problems where `n` can be huge, prefer iteration
or convert recursion to iteration with an explicit stack.

Bottom line: write recursion when it matches the structure of
the problem (trees, divide-and-conquer, "try every option"
search). Write iteration when state evolves left-to-right or
right-to-left along an array. Apply memoization whenever
subproblems repeat. None of these is inherently faster or
slower — they are different tools for different shapes.
''',
            },
            {
                "question": "Why does the base case use `if n < 2: return n`?",
                "answer": r'''
The base case has to cover **both** seed values of the sequence
without falling into infinite recursion.

By definition, `F(0) = 0` and `F(1) = 1`. So when the input is 0,
we should return 0; when it is 1, we should return 1. Conveniently,
both of those facts are summarized by `return n` (since `F(0) = 0`
and `F(1) = 1` both happen to equal their index).

If we wrote only `if n == 0: return 0`, then calling `fib(1)`
would recurse into `fib(0) + fib(-1)`, and `fib(-1)` makes no
sense and would recurse forever. So we need to cover index 1 as
well, otherwise the recursion stumbles.

`if n < 2: return n` is a compact way to write both base cases at
once. You could equivalently write:

```python
if n == 0:
    return 0
if n == 1:
    return 1
```

It is two lines instead of one, but it is just as correct and
sometimes easier to read for beginners. Pick whichever feels
clearer to you. The interview-favorite is the one-liner because
it is shorter and signals that you understand both seeds.

A small subtlety: this base case **assumes `n` is non-negative**.
The function will behave strangely on negative inputs because
`n < 2` is true for `n = -1`, and we will return `-1` — which is
not a Fibonacci number. If your problem allows negative inputs,
you should add a guard at the top:

```python
if n < 0:
    raise ValueError("n must be non-negative")
```

Most curriculum problems assume non-negative `n`, so the guard is
usually omitted. But know it is there as an option.
''',
            },
        ],
        "summary": r'''
**Pattern**: overlapping subproblems → memoize (top-down) or
tabulate (bottom-up).

**Lesson**: a correct algorithm can be uselessly slow if it solves
the same subproblem many times. The cure is to remember each
subproblem's answer the first time you compute it.

**Recognize next time**: any recursion where the same arguments
appear in multiple branches of the recursion tree. The instant you
spot the repetition, reach for a cache.

**Bigger picture**: Fibonacci is the friendliest possible
introduction to dynamic programming. Every DP problem in Step 16
is, at its core, a recursion plus a sticky note. The sticky note
might be a dict, an array, or a 2D table — but the idea is
identical to what you just learned here.
''',
    },
    {
        "id": "count-frequencies",
        "title": "Count Frequencies of Array Elements",
        "step_id": 1,
        "lecture_id": 6,
        "difficulty": "easy",
        "tags": ["hashing", "dict", "counter"],
        "what_this_teaches": (
            "The one-pass frequency-map idiom. Once you reach for "
            "`Counter` instead of nested loops, an enormous family of "
            "problems collapses from *O(n²)* to *O(n)*."
        ),
        "pattern": "Walk once + dictionary = frequency map.",
        "prerequisite_lessons": ["arrays", "hashing"],
        "prerequisite_problems": [],
        "next_problems": [
            "highest-lowest-frequency",
            "two-sum",
            "majority-element",
            "top-k-frequent",
        ],
        "resources": [
            {
                "label": "Striver's A2Z DSA Course — Step 1 (Basic Hashing)",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
            },
            {
                "label": "Python docs — collections.Counter",
                "url": "https://docs.python.org/3/library/collections.html#collections.Counter",
            },
        ],
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
        "confusion_notes": [
            {
                "question": "What is `counts.get(x, 0) + 1` actually doing?",
                "answer": r'''
It is the single most useful idiom in beginner Python dict work,
and worth dissecting carefully.

`counts.get(x, 0)` says: *"give me `counts[x]` if `x` is in the
dict; otherwise give me `0`."* Notice that, unlike `counts[x]`,
this does **not** raise an error when `x` is missing. It returns
the default value (here, `0`) instead.

So `counts.get(x, 0) + 1` reads in English as: *"the previous
count for `x`, treating absent as zero, plus one."*

When we then assign `counts[x] = counts.get(x, 0) + 1`, we are
saying: *"set `counts[x]` to its previous value plus one, with
the convention that absent counts as zero."*

This idiom is what lets us write the frequency loop without a
manual "if `x` in counts" guard:

```python
counts = {}
for x in arr:
    counts[x] = counts.get(x, 0) + 1
```

Without `.get`, you would need an awkward conditional:

```python
counts = {}
for x in arr:
    if x in counts:
        counts[x] += 1
    else:
        counts[x] = 1
```

Both are correct, but the `.get` version is shorter and more
idiomatic. Internalize it; you will write this pattern hundreds
of times.

An even cleaner alternative is `collections.defaultdict(int)`,
which gives you a dict where every missing key defaults to `0`
automatically. Or just use `Counter`, which is purpose-built for
counting and does the whole loop in one line.
''',
            },
            {
                "question": "Why is `Counter` better than writing the loop by hand?",
                "answer": r'''
Three reasons. First, it is **shorter** — one line instead of
three. Second, it is **faster** — `Counter` is implemented in
optimized C inside the standard library, so the underlying loop
runs faster than a hand-written Python loop. Third, it carries
**extra useful methods** that the dict version does not.

The headline extras:

- `most_common(k)` — returns the top `k` most frequent items as
  a list of `(value, count)` pairs, sorted descending. This
  solves "top K frequent" in one method call.
- Arithmetic: `Counter(a) - Counter(b)` gives a Counter with the
  difference in counts. Useful for "are these two arrays
  anagrams?" or "what is the difference between two multisets?".
- `Counter.update(...)` adds counts from another iterable
  without losing existing counts.
- `Counter(...)` accepts any iterable, including generators,
  strings, and other Counters.

A concrete comparison. Frequency of characters in a string:

```python
# Hand-rolled.
counts = {}
for ch in s:
    counts[ch] = counts.get(ch, 0) + 1

# With Counter.
from collections import Counter
counts = Counter(s)
```

Both produce the same result. The Counter version reads like
prose.

When to NOT use Counter: when you need to support a custom
counting rule that is not just "add one per occurrence." For
example, if each element contributes a *weight* rather than 1,
you want the hand-rolled loop. But for plain frequency, always
reach for Counter.
''',
            },
            {
                "question": "What is the difference between a set and a Counter?",
                "answer": r'''
A **set** stores distinct values but discards counts. A
**Counter** stores distinct values *and* how many times each one
appeared. They answer different questions.

- Set: "did this value appear at all?" — yes / no.
- Counter: "how many times did this value appear?" — a number.

Concretely:

```python
arr = [1, 1, 2, 2, 2, 3]

s = set(arr)             # {1, 2, 3}
c = Counter(arr)         # Counter({2: 3, 1: 2, 3: 1})

print(2 in s)            # True
print(c[2])              # 3
print(c[99])             # 0  (Counter returns 0 for missing keys, unlike dict)
```

Use a **set** when the question is binary — "is this value
present?", "are these two collections equal as sets?", "remove
duplicates from this list." Use a **Counter** (or a `dict`)
when the question involves the *number* of occurrences.

For example, "do these two strings have the same letters,
ignoring order?" is asking whether the **multisets** match, which
means comparing **counts**. So `Counter(s1) == Counter(s2)`. A
set comparison would incorrectly say "aabb" and "abbb" are equal
(both have characters `{a, b}`), but their counters differ —
`Counter("aabb") = {a:2, b:2}` vs `Counter("abbb") = {a:1, b:3}`.

The general rule: pick the data structure whose question matches
yours. Sets for presence, Counters for frequency.
''',
            },
            {
                "question": "When should I use a list-indexed-by-value instead of a Counter?",
                "answer": r'''
When the values are bounded small integers, a list (or fixed-size
array) is faster and uses less memory than a dict.

The canonical case: counting lowercase English letters. The
values `'a'`–`'z'` map to indices 0–25 via `ord(ch) - ord('a')`.
A length-26 list of integers is a perfectly tight counting
structure:

```python
counts = [0] * 26
for ch in s:
    counts[ord(ch) - ord('a')] += 1
```

This is faster than a `Counter` for two reasons. First, list
indexing is a single pointer-arithmetic step, while dict access
requires hashing the key and probing the table. Second, the list
has no hash overhead and no dynamic resizing.

When does this matter? Mostly for **anagram problems** with
millions of comparisons, or for tight inner loops in
performance-sensitive code. For ordinary problems, the speedup
is negligible and the Counter version is clearer.

When values are NOT bounded small integers — arbitrary strings,
floats, large random integers — a list is impractical. A dict
or Counter is the right answer.

The general principle: if you know the value space is small and
dense, you can use the value itself as an array index. This is
the same trick that powers **counting sort**, **radix sort**,
and the **bucket** data structures used in advanced algorithms.
''',
            },
        ],
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
