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
