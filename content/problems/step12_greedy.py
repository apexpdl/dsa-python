"""Step 12 — Greedy Algorithms (15 problems).

Covers the classic greedy patterns: exchange argument problems,
interval scheduling, the candy problem, fractional knapsack, the
N-meetings sort-by-finish-time idea, and so on.
"""
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
    # ------------------------------------------------------------------
    # 1) Assign Cookies
    # ------------------------------------------------------------------
    {
        "id": "assign-cookies",
        "title": "Assign Cookies",
        "step_id": 12,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["greedy", "two-pointer", "sorting"],
        "what_this_teaches": "First greedy exchange argument: give the smallest cookie that satisfies the smallest unsatisfied child.",
        "pattern": "Sort + two pointers.",
        "prerequisite_lessons": ["sorting", "greedy"],
        "prerequisite_problems": [],
        "next_problems": ["fractional-knapsack", "n-meetings"],
        "resources": [
            _lc(455, "assign-cookies"),
            _SHEET,
        ],
        "understanding": r'''
You are a parent. You have a list `g[i]` of children's greed factors
and a list `s[j]` of cookie sizes. You can give *one* cookie per child;
child i is content iff some cookie j with `s[j] >= g[i]` is given to
them. Maximize the number of content children.

**Example:** `g = [1, 2, 3], s = [1, 1]` → 1 child can be content (the
one with greed 1).
''',
        "brute_force": {
            "explanation": r'''
Try every assignment: for each permutation of cookies to children,
count content children. Exponential. Useless beyond n = 8.
''',
            "code": r'''
from itertools import permutations
def assign_brute(g, s):
    best = 0
    for perm in permutations(s, min(len(g), len(s))):
        c = sum(1 for child, cookie in zip(g, perm) if cookie >= child)
        best = max(best, c)
    return best
''',
            "complexity": "Time O(n!).",
        },
        "thought_process": r'''
**Exchange argument.** Sort both arrays ascending. Walk a pointer `i`
through children and a pointer `j` through cookies. If `s[j] >= g[i]`,
match them and advance both. Otherwise advance only j (this cookie is
too small for everyone left). When either array is exhausted, stop.

**Why is this optimal?** Suppose an optimal solution assigns a bigger
cookie B to child X and a smaller cookie A to child Y where A could
have satisfied X. Swap them — both children remain satisfied (or
better). This means we can always rearrange any optimum to be a
"smallest fitting cookie to smallest unmatched child" assignment.
That's exactly what the greedy produces.
''',
        "optimized": {
            "explanation": r'''
Two pointers after sorting. O(n log n).
''',
            "code": r'''
def find_content_children(g, s):
    g.sort()
    s.sort()
    i = j = 0
    while i < len(g) and j < len(s):
        if s[j] >= g[i]:
            i += 1                # child i is content
        j += 1                    # move past this cookie either way
    return i
''',
            "walkthrough": r'''
The optimal greedy. Sort both arrays, then walk with two
pointers. *O(n log n + m log m)* due to the sorts; the
two-pointer walk itself is *O(n + m)*.

**`def find_content_children(g, s):`** — Takes children's
greed factors `g` and cookie sizes `s`. Returns the maximum
number of children we can satisfy.

**`g.sort(); s.sort()`** — Sort both arrays in ascending
order. This is the **enabling step** for the greedy. After
sorting, smaller children come first (easier to satisfy) and
smaller cookies come first (use them up before reaching for
bigger ones).

**`i = j = 0`** — Two pointers. `i` walks through children;
`j` walks through cookies. We try to match them.

**`while i < len(g) and j < len(s):`** — Continue while we
have both children left to feed and cookies left to give.

**`if s[j] >= g[i]:`** — Is the current cookie big enough to
satisfy the current child? Since both arrays are sorted, we
just need to compare the fronts.

**`i += 1`** — Yes! Child `i` is content. Move to the next
child. We don't immediately also advance `j` here — that
happens unconditionally below.

**`j += 1`** — Move past this cookie either way:
- If we used it (matched a child), the cookie is consumed.
- If we couldn't use it (this cookie was too small even for
  the smallest unfed child), then this cookie is useless for
  every later child (who are at least as greedy) — discard it.

**`return i`** — `i` ends up equal to the number of satisfied
children. Return it.

**Why is this greedy correct?**

The **exchange argument**: suppose some optimal solution uses
cookie `B` for child `X`, but cookie `A` (smaller, still
satisfies `X`) is sitting unused. Then we can swap:
use `A` for `X` and free up `B`. Either `B` then satisfies
some other child (improving the solution) or it's wasted (no
change). Either way, the new solution is at least as good.

So we can always rearrange any optimal solution to use the
**smallest possible cookie** for each child. That's exactly
what our greedy does: smallest unfed child + smallest cookie
that fits + walk.

**Trace on `g = [1, 2, 3], s = [1, 1]`:**
```
After sort: g = [1, 2, 3], s = [1, 1]
i=0, j=0: s[0]=1 >= g[0]=1 → satisfy child 0. i=1.
         j=1 (advanced unconditionally).
i=1, j=1: s[1]=1 < g[1]=2 → cookie too small. j=2.
         (loop ends, j out of range)
Return i = 1. (Only 1 child satisfied.)
```

The unused cookie at index 0 (the other size-1) couldn't help
anyone after child 0 because all later children are greedier.

**Properties:**
- **Time**: *O(n log n + m log m)* dominated by sorting.
- **Space**: *O(1)* (sorting in place; just two pointers).

**The pattern**: sort + two pointers + greedy matching. The
same shape appears in many "match small to small" problems.
''',
            "complexity": "Time O(n log n + m log m), space O(1).",
        },
        "deep_concept": r'''
The exchange argument is the *bread and butter* of greedy proofs. To
show your greedy is optimal, take any optimal solution and demonstrate
that you can transform it step-by-step into the greedy solution
without decreasing its quality.
''',
        "confusion_notes": [
            {
                "question": "Could we instead give the *biggest* cookie to the greediest child?",
                "answer": "It's symmetric — sort both descending and walk. Same answer. But sorting ascending feels more natural for 'satisfy the easiest child first'.",
            },
        ],
        "summary": "Sort, two pointers, advance j always, advance i only on a match.",
    },

    # ------------------------------------------------------------------
    # 2) Fractional Knapsack
    # ------------------------------------------------------------------
    {
        "id": "fractional-knapsack",
        "title": "Fractional Knapsack",
        "step_id": 12,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["greedy", "sorting"],
        "what_this_teaches": "Maximizing value subject to a capacity constraint when *fractions are allowed*. Sort by value/weight density.",
        "pattern": "Greedy by ratio.",
        "prerequisite_lessons": ["greedy"],
        "prerequisite_problems": ["assign-cookies"],
        "next_problems": ["job-sequencing"],
        "resources": [
            {"label": "GFG — Fractional Knapsack", "url": "https://www.geeksforgeeks.org/fractional-knapsack-problem/"},
            _SHEET,
        ],
        "understanding": r'''
Given N items, each with `value[i]` and `weight[i]`, and a knapsack of
capacity W, return the maximum value you can carry. **You may take
fractional pieces** of any item (unlike 0/1 knapsack).

**Example:** items `[(60, 10), (100, 20), (120, 30)]`, W = 50 →
take all of item 1 and 2 (value 160), then 2/3 of item 3 (80) → total
240.
''',
        "brute_force": {
            "explanation": r'''
Try every subset and within each, take a fraction of the last item if
needed. Exponential. We jump to the proven greedy.
''',
            "code": r'''
# Skipped — exponential enumeration.
''',
            "complexity": "Time O(2^n).",
        },
        "thought_process": r'''
**Greedy by density.** Compute the value/weight ratio for each item;
sort items in descending order of this ratio. Walk through and take
items whole if they fit; for the first item that doesn't fit, take a
fraction equal to the remaining capacity / item weight.

**Why optimal?** Exchange argument: any optimal allocation that
includes some weight of a low-density item and skips weight of a
higher-density item can be improved by swapping a unit of low-density
for a unit of high-density. Iterating, the optimum collapses to the
density-greedy.
''',
        "optimized": {
            "explanation": r'''
Sort by ratio, walk, accumulate.
''',
            "code": r'''
def fractional_knapsack(W, items):
    # items: list of (value, weight)
    items_sorted = sorted(items, key=lambda x: x[0] / x[1], reverse=True)
    total = 0.0
    cap = W
    for v, w in items_sorted:
        if w <= cap:
            total += v
            cap -= w
        else:
            total += v * (cap / w)        # take fraction
            break
    return total
''',
            "complexity": "Time O(n log n), space O(1).",
        },
        "deep_concept": r'''
The fractional version is fundamentally easier than 0/1 knapsack
because the relaxation makes the problem **linear**. 0/1 knapsack
requires DP precisely because we can't 'partially' grab an item.
''',
        "confusion_notes": [
            {
                "question": "Why doesn't the same density-greedy work for 0/1 knapsack?",
                "answer": "Because in 0/1 you can't take half of the next item. If the highest-density item is huge, you may waste capacity by being unable to fit it whole. Counter-example: W=10, items [(11, 11), (10, 10)]. Density-greedy picks the first → can't fit, value 0. Optimum: skip the first, take the second, value 10.",
            },
        ],
        "summary": "Sort by value/weight descending, take whole items while they fit, then a fraction of the next.",
    },

    # ------------------------------------------------------------------
    # 3) Lemonade Change
    # ------------------------------------------------------------------
    {
        "id": "lemonade-change",
        "title": "Lemonade Change",
        "step_id": 12,
        "lecture_id": 1,
        "difficulty": "easy",
        "tags": ["greedy", "simulation"],
        "what_this_teaches": "Give the largest bill change first to preserve flexibility.",
        "pattern": "Greedy by denomination size.",
        "prerequisite_lessons": ["greedy"],
        "prerequisite_problems": [],
        "next_problems": ["valid-parenthesis-string"],
        "resources": [
            _lc(860, "lemonade-change"),
            _SHEET,
        ],
        "understanding": r'''
You sell lemonade for \$5. Customers pay with \$5, \$10, or \$20 bills
(in order). You start with no cash. Return True iff you can give every
customer correct change.
''',
        "brute_force": {
            "explanation": r'''
Brute force would try every way to make change. Tiny denomination set
makes this irrelevant; the greedy is obviously optimal.
''',
            "code": r'''
# n/a — greedy is the natural solution.
''',
            "complexity": "—",
        },
        "thought_process": r'''
We have only three denominations (5, 10, 20). When a \$10 customer
arrives, we must give one \$5 back. When a \$20 customer arrives, we
prefer one \$10 + one \$5 (using the less flexible \$10). Only if no \$10
is available do we give three \$5.

**Why prefer \$10 + \$5 over three \$5s?** Because \$5 bills can also
serve future \$10 customers, whereas \$10 bills can only serve \$20
customers. We hoard the flexible currency.
''',
        "optimized": {
            "explanation": r'''
Simulate with two counters for \$5 and \$10 bills (no need to track
\$20s).
''',
            "code": r'''
def lemonade_change(bills):
    fives = tens = 0
    for b in bills:
        if b == 5:
            fives += 1
        elif b == 10:
            if fives == 0:
                return False
            fives -= 1
            tens += 1
        else:                       # b == 20
            if tens > 0 and fives > 0:
                tens -= 1
                fives -= 1
            elif fives >= 3:
                fives -= 3
            else:
                return False
    return True
''',
            "complexity": "Time O(n), space O(1).",
        },
        "deep_concept": r'''
A toy demonstration of *flexibility preservation*: when multiple change
combinations work, prefer the one that keeps high-flexibility currency
(small bills) in reserve.
''',
        "confusion_notes": [
            {
                "question": "Why not track \$20 bills?",
                "answer": "Because we can never make change *with* a \$20 — no transaction gives less change than \$15. The \$20 we receive only ever ends up in our drawer doing nothing useful.",
            },
        ],
        "summary": "Track \$5 and \$10 counts; for \$20 prefer one \$10 + one \$5 to three \$5s.",
    },

    # ------------------------------------------------------------------
    # 4) Valid Parenthesis String
    # ------------------------------------------------------------------
    {
        "id": "valid-parenthesis-string",
        "title": "Valid Parenthesis String",
        "step_id": 12,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["greedy", "strings"],
        "what_this_teaches": "Track a *range* of possible open counts. Maintain `low` and `high`; reject when high goes negative or low ends positive.",
        "pattern": "Range tracking through a string.",
        "prerequisite_lessons": ["strings", "stacks"],
        "prerequisite_problems": [],
        "next_problems": ["job-sequencing"],
        "resources": [
            _lc(678, "valid-parenthesis-string"),
            _SHEET,
        ],
        "understanding": r'''
A string contains `'('`, `')'`, and `'*'`. The `'*'` can act as `'('`,
`')'`, or empty. Return True iff some interpretation makes the string a
valid parenthesis sequence.

**Example:** `"(*))"` → True (interpret `*` as `(` → `(())`).
''',
        "brute_force": {
            "explanation": r'''
Try every interpretation of every `'*'` (each has 3 choices) and check
each. O(3^k · n). Acceptable only on short strings.
''',
            "code": r'''
def check_valid_brute(s):
    def helper(i, bal):
        if bal < 0:
            return False
        if i == len(s):
            return bal == 0
        if s[i] == '(':
            return helper(i + 1, bal + 1)
        if s[i] == ')':
            return helper(i + 1, bal - 1)
        # '*'
        return helper(i + 1, bal + 1) or helper(i + 1, bal) or helper(i + 1, bal - 1)
    return helper(0, 0)
''',
            "complexity": "Time O(3^k · n).",
        },
        "thought_process": r'''
**Maintain a range.** Track the minimum (`low`) and maximum (`high`)
possible number of open parens after each char.
- `(` → both increase by 1.
- `)` → both decrease by 1.
- `*` → `low` decreases by 1 (treated as `)`), `high` increases by 1
  (treated as `(`).

After each char, clamp `low` to 0 (we can never go below 0 because
beyond that, the string is already invalid for *any* interpretation).
If `high < 0`, return False — even treating every `*` as `(` we have
too many `)`. At the end, return True iff `low == 0` (some
interpretation balances).
''',
        "optimized": {
            "explanation": r'''
One pass, two counters. O(n).
''',
            "code": r'''
def check_valid_string(s):
    low = high = 0
    for ch in s:
        if ch == '(':
            low += 1; high += 1
        elif ch == ')':
            low -= 1; high -= 1
        else:                      # '*'
            low -= 1; high += 1
        if high < 0:
            return False           # too many ')' even in the best case
        if low < 0:
            low = 0                # clamp: more ')' than '(' is invalid; pretend '*' was something else
    return low == 0
''',
            "walkthrough": r'''
A beautiful **range-tracking** algorithm. Instead of trying
each interpretation of `*` (3 options each → exponential), we
track the **range** of possible open-paren counts. One pass,
constant memory.

**`def check_valid_string(s):`** — Takes a string of `(`, `)`,
and `*`. Returns True iff some interpretation of `*`
(each can be `(`, `)`, or empty) makes the string a valid
balanced-parens.

**`low = high = 0`** — Two counters tracking the **range**
of possible "open paren counts" after processing each char.

- `low` = minimum possible open count (treat every `*` as a
  `)`).
- `high` = maximum possible open count (treat every `*` as a
  `(`).

At any moment, the actual open count is somewhere in
`[low, high]` depending on how we interpret each `*` seen so
far.

**`for ch in s:`** — Walk every char.

**`if ch == '(': low += 1; high += 1`** — A `(` increases the
open count by exactly 1, regardless of interpretation. Both
bounds shift up.

**`elif ch == ')': low -= 1; high -= 1`** — A `)` decreases
the open count by exactly 1. Both bounds shift down.

**`else: low -= 1; high += 1`** — A `*` can decrease (acting
as `)`), increase (acting as `(`), or leave unchanged (empty).
The minimum action is to decrease (`low -= 1`). The maximum
is to increase (`high += 1`). The bounds widen.

**`if high < 0: return False`** — If even the **maximum**
possible open count is negative, then **every** interpretation
has too many `)`s. Invalid — no way to fix it.

**`if low < 0: low = 0`** — **Clamp** `low` to zero. Here's
why: `low < 0` means some bad interpretation has negative
opens, but valid sequences can't have negative opens.
We discard that interpretation by setting `low = 0` — that is,
"the minimum possible open count remains 0; we just won't
consider interpretations that would go negative."

**`return low == 0`** — At the end, the string is valid iff
some interpretation balances exactly. `low <= 0 <= high`
means 0 is in the possible range. After clamping `low` to
zero earlier, the check `low == 0` is sufficient.

**Why does this work?**

The key insight: even though `*` has 3 interpretations each
(creating 3^k possible total interpretations for k stars),
the **range** of resulting open counts is contiguous (an
interval). So we only need to track the two endpoints, not
the whole exponential set.

After processing the whole string, we want some
interpretation to give open count = 0. That's possible iff
0 ∈ [low, high]. With our clamping, that simplifies to
`low == 0`.

**Trace on `s = "(*))"`:**
```
Char '(' : low=1, high=1.
Char '*' : low=0, high=2. (range: 0 to 2 opens)
Char ')' : low=-1 → clamp to 0, high=1.
Char ')' : low=-1 → clamp to 0, high=0.
End: low=0, high=0. Return low == 0 → True.
```

Trace on `s = "((*)`:
```
Char '(' : low=1, high=1.
Char '(' : low=2, high=2.
Char '*' : low=1, high=3.
Char ')' : low=0, high=2.
End: low=0, high=2. Return low == 0 → True.
```

Trace on `s = ")("`:
```
Char ')' : low=-1, high=-1. high < 0 → return False.
```

**Properties:**
- **Time**: *O(n)* single pass.
- **Space**: *O(1)*.

The pattern — **track a feasibility interval** rather than
each possibility — appears in many other constraint problems
(longest valid substring, validate IP, etc).
''',
            "complexity": "Time O(n), space O(1).",
        },
        "deep_concept": r'''
This is a beautiful example of **range tracking**: instead of trying
each `*` interpretation, we track the *set* of feasible open counts as
an interval. The interval evolves linearly and validity reduces to
checking whether 0 ever lies in it.
''',
        "confusion_notes": [
            {
                "question": "Why clamp `low` to 0 instead of returning False?",
                "answer": "Because `low < 0` means *one specific* interpretation has too many `)` — but other interpretations may still work. We clamp because in a valid prefix we always have ≥ 0 open parens; if `low` went negative, *forget* that interpretation by resetting to 0. We only fail when `high` (the *most favorable* interpretation) goes negative.",
            },
            {
                "question": "Why is `low == 0` the success condition at the end?",
                "answer": "Because we need *some* interpretation where the total opens equal total closes. `low` is the minimum possible final open count; if it's 0, some interpretation balances exactly. If it's > 0, every interpretation has unmatched opens.",
            },
        ],
        "summary": "Track [low, high] of possible open counts as you scan. Fail if high < 0, succeed if final low == 0.",
    },

    # ------------------------------------------------------------------
    # 5) Job Sequencing Problem
    # ------------------------------------------------------------------
    {
        "id": "job-sequencing",
        "title": "Job Sequencing with Deadlines",
        "step_id": 12,
        "lecture_id": 1,
        "difficulty": "medium",
        "tags": ["greedy", "sorting", "union-find"],
        "what_this_teaches": "Schedule each job in the *latest available slot* ≤ its deadline. Greedy by profit descending.",
        "pattern": "Sort by profit + latest-slot scheduling.",
        "prerequisite_lessons": ["sorting", "greedy"],
        "prerequisite_problems": ["fractional-knapsack"],
        "next_problems": ["n-meetings"],
        "resources": [
            {"label": "GFG — Job Sequencing Problem", "url": "https://www.geeksforgeeks.org/job-sequencing-problem/"},
            _SHEET,
        ],
        "understanding": r'''
Given N jobs, each with `deadline[i]` and `profit[i]`. Each job takes
exactly one unit of time. You can run at most one job per unit time and
each job must finish by its deadline. Maximize total profit.

**Example:** jobs = [(d=4, p=20), (d=1, p=10), (d=1, p=40), (d=1, p=30)]
→ best schedule: job4 at t=1 (40), job1 at t=2 (20)? But job1's deadline
is 4 so it can run as late as t=4. Total profit = 60.
''',
        "brute_force": {
            "explanation": r'''
Try every subset of jobs that fits within deadlines. Exponential.
''',
            "code": r'''
# Exponential — skipped.
''',
            "complexity": "—",
        },
        "thought_process": r'''
**Sort by profit descending.** For each job (in that order), assign it
to the **latest unused time slot ≤ its deadline**. If no such slot
exists, skip the job.

**Why latest available?** Because leaving early slots free preserves
flexibility for future jobs with tight deadlines.

**Implementation:** maintain a boolean array `slot[1..max_deadline]`.
For each job, walk down from `deadline` to 1, take the first empty.
O(N · max_deadline). For very large deadlines, use a DSU (union-find)
on slot indices for amortized near-O(1) lookup.
''',
        "optimized": {
            "explanation": r'''
Sort + greedy latest-slot. The DSU optimization is worth knowing but
isn't required for typical inputs.
''',
            "code": r'''
def job_sequencing(jobs):
    # jobs: list of (deadline, profit), 1-indexed deadlines
    jobs_sorted = sorted(jobs, key=lambda x: -x[1])    # profit desc
    max_d = max(d for d, _ in jobs)
    slot = [False] * (max_d + 1)                       # slot[0] unused
    total_profit = 0
    count = 0
    for d, p in jobs_sorted:
        # find latest free slot ≤ d
        t = d
        while t > 0 and slot[t]:
            t -= 1
        if t > 0:
            slot[t] = True
            total_profit += p
            count += 1
    return count, total_profit
''',
            "complexity": "Time O(N · max_deadline). With DSU, amortized O(N · α).",
        },
        "deep_concept": r'''
This is the *latest-slot variant* of interval scheduling. Sorting by
profit descending plus 'use the latest legal time' is provably optimal
by exchange: if an optimum runs job X early and skips Y because of a
conflict, we can swap to use the later slot for X and free the early
slot for Y without losing profit.
''',
        "confusion_notes": [
            {
                "question": "Why latest slot instead of earliest?",
                "answer": "Because earliest-slot is greedy by the wrong key — it would block easy-to-schedule (high-deadline) jobs by hogging early slots that tight-deadline jobs need. Latest-slot avoids that.",
            },
        ],
        "summary": "Sort jobs by profit descending. For each, take the latest empty slot ≤ its deadline. Skip if none.",
    },

    # ------------------------------------------------------------------
    # 6) N Meetings in One Room
    # ------------------------------------------------------------------
    {
        "id": "n-meetings",
        "title": "N Meetings in One Room",
        "step_id": 12,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["greedy", "intervals", "sorting"],
        "what_this_teaches": "Classic interval scheduling: sort by *finish time* and take greedily.",
        "pattern": "Earliest-finish-time-first.",
        "prerequisite_lessons": ["sorting", "greedy"],
        "prerequisite_problems": [],
        "next_problems": ["min-platforms", "merge-intervals"],
        "resources": [
            {"label": "GFG — N meetings in one room", "url": "https://www.geeksforgeeks.org/find-maximum-meetings-in-one-room/"},
            _SHEET,
        ],
        "understanding": r'''
Given N meetings with `start[i]` and `end[i]`, find the maximum number
of meetings that can be held in one room (no two overlap).

This is the textbook **interval scheduling** problem.
''',
        "brute_force": {
            "explanation": r'''
Try every subset and check for overlap. O(2^n).
''',
            "code": r'''
# Exponential — skipped.
''',
            "complexity": "—",
        },
        "thought_process": r'''
**Sort meetings by their end time** (ascending). Iterate; accept a
meeting iff its start ≥ the end of the last accepted meeting.

**Why end time, not start time?** Because the meeting that ends earliest
leaves the most room for subsequent meetings. The classic exchange
argument: if some optimal solution doesn't take the earliest-finishing
meeting, swap it in — the new solution is at least as large because
the swap only frees more space for future meetings.
''',
        "optimized": {
            "explanation": r'''
Sort by end, walk, take greedily.
''',
            "code": r'''
def max_meetings(start, end):
    intervals = sorted(zip(start, end), key=lambda x: x[1])
    count = 0
    last_end = -1
    for s, e in intervals:
        if s > last_end:
            count += 1
            last_end = e
    return count
''',
            "complexity": "Time O(n log n), space O(n).",
        },
        "deep_concept": r'''
This is the most-quoted greedy theorem in algorithms textbooks.
Variants include weighted interval scheduling (which needs DP) and
multi-room scheduling (which needs the next problem, Min Platforms).
''',
        "confusion_notes": [
            {
                "question": "Why is `s > last_end` strict (not `>=`)?",
                "answer": "Depends on the problem semantics. Striver's version treats touching intervals as conflicting; LeetCode's 'Non-overlapping intervals' uses `>=` (touch is OK). Read the spec and adjust.",
            },
        ],
        "summary": "Sort by end time; greedy-accept any meeting starting after the last accepted's end.",
    },

    # ------------------------------------------------------------------
    # 7) Jump Game I
    # ------------------------------------------------------------------
    {
        "id": "jump-game-i",
        "title": "Jump Game",
        "step_id": 12,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["greedy", "array"],
        "what_this_teaches": "Track the farthest reachable index in one pass.",
        "pattern": "Greedy farthest-reach.",
        "prerequisite_lessons": ["arrays", "greedy"],
        "prerequisite_problems": [],
        "next_problems": ["jump-game-ii"],
        "resources": [
            _lc(55, "jump-game"),
            _SHEET,
        ],
        "understanding": r'''
You are at index 0 of an array `nums`. From index i you can jump to any
index `i + k` where `0 ≤ k ≤ nums[i]`. Return True iff you can reach
the last index.
''',
        "brute_force": {
            "explanation": r'''
Recursive DFS / memo: from each index, try every reachable next index.
O(n²) time with memoization.
''',
            "code": r'''
def can_jump_brute(nums):
    n = len(nums)
    memo = {}
    def go(i):
        if i >= n - 1:
            return True
        if i in memo:
            return memo[i]
        for k in range(1, nums[i] + 1):
            if go(i + k):
                memo[i] = True
                return True
        memo[i] = False
        return False
    return go(0)
''',
            "complexity": "Time O(n²), space O(n).",
        },
        "thought_process": r'''
Track `farthest`, the maximum index we've proven reachable so far.
Iterate i from 0; if `i > farthest` we're stuck. Otherwise update
`farthest = max(farthest, i + nums[i])`. After scanning, return True
iff `farthest >= n - 1`.

**Why is this optimal?** Because once we know we can reach index i,
we can pick the best jump from any reachable predecessor. Tracking the
single maximum reachable index is enough.
''',
        "optimized": {
            "explanation": r'''
One linear pass.
''',
            "code": r'''
def can_jump(nums):
    farthest = 0
    for i in range(len(nums)):
        if i > farthest:
            return False                         # we cannot even reach i
        farthest = max(farthest, i + nums[i])
        if farthest >= len(nums) - 1:
            return True
    return True
''',
            "complexity": "Time O(n), space O(1).",
        },
        "deep_concept": r'''
This is the canonical introduction to greedy on arrays. The farthest-
reach metric is monotone: as `i` grows, `farthest` can only grow (when
extended) or stay the same. The instant `farthest < i`, no reachable
predecessor exists.
''',
        "confusion_notes": [
            {
                "question": "Why does tracking only the farthest reach suffice?",
                "answer": "Because *any* reachable index ≤ farthest can land us at the same set of next indices we'd reach from the farthest one. The intermediate path doesn't matter — only the maximum extent does.",
            },
        ],
        "summary": "Track farthest reachable index in one pass; fail if `i > farthest`; succeed if `farthest >= n - 1`.",
    },

    # ------------------------------------------------------------------
    # 8) Jump Game II
    # ------------------------------------------------------------------
    {
        "id": "jump-game-ii",
        "title": "Jump Game II — Minimum Jumps",
        "step_id": 12,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["greedy", "bfs"],
        "what_this_teaches": "Implicit BFS-by-layer: track the boundary of the current jump and the farthest reachable from inside it.",
        "pattern": "Two-pointer 'current end' and 'farthest'.",
        "prerequisite_lessons": ["greedy", "bfs"],
        "prerequisite_problems": ["jump-game-i"],
        "next_problems": ["min-platforms"],
        "resources": [
            _lc(45, "jump-game-ii"),
            _SHEET,
        ],
        "understanding": r'''
Same array but now return the *minimum number of jumps* needed to reach
the last index. Assume it's always reachable.
''',
        "brute_force": {
            "explanation": r'''
DP: dp[i] = min jumps to reach i. O(n²).
''',
            "code": r'''
def jump_brute(nums):
    n = len(nums)
    dp = [float('inf')] * n
    dp[0] = 0
    for i in range(n):
        for k in range(1, nums[i] + 1):
            if i + k < n:
                dp[i + k] = min(dp[i + k], dp[i] + 1)
    return dp[-1]
''',
            "complexity": "Time O(n²), space O(n).",
        },
        "thought_process": r'''
Think of jumps as BFS layers: layer 0 = {0}, layer 1 = everything you
can reach in 1 jump, etc. We don't need the full BFS — we just track:
- `current_end`: the rightmost index in the current layer.
- `farthest`: the rightmost index reachable from this layer (= next
  layer's `current_end`).

Walk i from 0; for each i, update farthest. When i hits current_end,
we've finished the current layer → bump jumps, set current_end =
farthest.
''',
        "optimized": {
            "explanation": r'''
One linear pass with two pointers. O(n).
''',
            "code": r'''
def jump(nums):
    jumps = 0
    current_end = 0       # rightmost we can reach with `jumps` jumps
    farthest = 0          # rightmost we can reach with `jumps + 1` jumps
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == current_end:
            jumps += 1
            current_end = farthest
    return jumps
''',
            "complexity": "Time O(n), space O(1).",
        },
        "deep_concept": r'''
This is BFS *without* an explicit queue. The two-pointer view collapses
each layer to a single right boundary. Each layer is processed in one
left-to-right scan, no per-node enqueue/dequeue overhead.

A reminder: BFS on graphs gives shortest paths; whenever a problem
reduces to "minimum number of steps over layered structure" and you
can compute each layer's reach implicitly, the BFS becomes linear.
''',
        "confusion_notes": [
            {
                "question": "Why iterate to `len(nums) - 1` and not the end?",
                "answer": "Because reaching the last index ends the game — we don't need to count a jump *from* it. If we looped through the last index, we'd add a spurious +1 when `i == current_end` and current_end is already n-1.",
            },
        ],
        "summary": "Two-pointer BFS: `current_end` is the layer boundary, `farthest` is the next layer's boundary. Bump jumps when `i == current_end`.",
    },

    # ------------------------------------------------------------------
    # 9) Minimum Number of Platforms
    # ------------------------------------------------------------------
    {
        "id": "min-platforms",
        "title": "Minimum Number of Platforms",
        "step_id": 12,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["greedy", "intervals", "sweep-line"],
        "what_this_teaches": "Sweep line: sort arrivals and departures separately, walk both, track max concurrent trains.",
        "pattern": "Two-pointer merge of arrival/departure events.",
        "prerequisite_lessons": ["sorting", "intervals"],
        "prerequisite_problems": ["n-meetings"],
        "next_problems": ["merge-intervals"],
        "resources": [
            {"label": "GFG — Minimum platforms", "url": "https://www.geeksforgeeks.org/minimum-number-platforms-required-railwaybus-station/"},
            _SHEET,
        ],
        "understanding": r'''
Given arrival and departure times of N trains, find the minimum number
of platforms needed at the station so no train waits.

**Example:** arr = [900, 940, 950, 1100, 1500, 1800], dep = [910, 1200,
1120, 1130, 1900, 2000] → 3 platforms.
''',
        "brute_force": {
            "explanation": r'''
For each pair of trains, check overlap. Track max simultaneous overlap.
O(n²).
''',
            "code": r'''
def min_platforms_brute(arr, dep):
    n = len(arr)
    best = 1
    for i in range(n):
        count = 1
        for j in range(n):
            if i != j and arr[j] <= arr[i] <= dep[j]:
                count += 1
        best = max(best, count)
    return best
''',
            "complexity": "Time O(n²).",
        },
        "thought_process": r'''
**Sweep line.** Sort arrivals and departures separately. Walk both
arrays with pointers `i` (arrivals) and `j` (departures). At each step,
compare `arr[i]` and `dep[j]`:
- If `arr[i] <= dep[j]`: a new train arrives before the next train
  departs → need an extra platform.
- Else: a train departs → free one platform.

Track the running platform count and its maximum.
''',
        "optimized": {
            "explanation": r'''
Sort both arrays; two-pointer sweep.
''',
            "code": r'''
def find_platform(arr, dep):
    arr = sorted(arr)
    dep = sorted(dep)
    n = len(arr)
    i = j = 0
    plat = 0
    best = 0
    while i < n and j < n:
        if arr[i] <= dep[j]:
            plat += 1
            i += 1
            best = max(best, plat)
        else:
            plat -= 1
            j += 1
    return best
''',
            "complexity": "Time O(n log n), space O(1).",
        },
        "deep_concept": r'''
This is the canonical sweep-line algorithm: convert each interval to
two events (start +1, end −1), sort by time, walk while tracking the
running sum. The maximum sum is the answer. The two-pointer version is
just the most efficient implementation when start/end times come as
parallel arrays.
''',
        "confusion_notes": [
            {
                "question": "Why do we sort arr and dep *separately* rather than as paired intervals?",
                "answer": "Because we process *events* (arrival and departure) in time order, not intervals. The sorted-arr and sorted-dep arrays let us merge events in O(n) like a merge-sort step. Pairing them back doesn't help — a train's identity is irrelevant for counting platforms.",
            },
        ],
        "summary": "Sweep line over sorted arrivals and departures; track running platform count and its max.",
    },

    # ------------------------------------------------------------------
    # 10) Candy
    # ------------------------------------------------------------------
    {
        "id": "candy",
        "title": "Candy",
        "step_id": 12,
        "lecture_id": 2,
        "difficulty": "hard",
        "tags": ["greedy", "two-pass"],
        "what_this_teaches": "Two-pass greedy: left-to-right enforces left neighbor constraints; right-to-left fixes the rest.",
        "pattern": "Two-pass max.",
        "prerequisite_lessons": ["greedy"],
        "prerequisite_problems": [],
        "next_problems": ["sjf-scheduling"],
        "resources": [
            _lc(135, "candy"),
            _SHEET,
        ],
        "understanding": r'''
Children stand in a line, each with a rating `ratings[i]`. Distribute
candies such that each child gets ≥ 1 candy and any child with a higher
rating than a neighbor gets more candies than that neighbor. Minimize
total candies.
''',
        "brute_force": {
            "explanation": r'''
Iteratively bump candies until stable. O(n²) worst case.
''',
            "code": r'''
def candy_brute(ratings):
    n = len(ratings)
    c = [1] * n
    changed = True
    while changed:
        changed = False
        for i in range(n):
            if i > 0 and ratings[i] > ratings[i - 1] and c[i] <= c[i - 1]:
                c[i] = c[i - 1] + 1
                changed = True
            if i + 1 < n and ratings[i] > ratings[i + 1] and c[i] <= c[i + 1]:
                c[i] = c[i + 1] + 1
                changed = True
    return sum(c)
''',
            "complexity": "Time O(n²), space O(n).",
        },
        "thought_process": r'''
**Two-pass approach.**
- Left-to-right: `left[i] = left[i - 1] + 1` if `ratings[i] > ratings[i - 1]`,
  else 1. This satisfies the *left neighbor* constraint.
- Right-to-left: `right[i] = right[i + 1] + 1` if `ratings[i] > ratings[i + 1]`,
  else 1. This satisfies the *right neighbor* constraint.
- Final candy[i] = `max(left[i], right[i])`.

Total = sum of `max(...)`.
''',
        "optimized": {
            "explanation": r'''
Two passes, O(n).
''',
            "code": r'''
def candy(ratings):
    n = len(ratings)
    left  = [1] * n
    right = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            left[i] = left[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            right[i] = right[i + 1] + 1
    return sum(max(l, r) for l, r in zip(left, right))
''',
            "complexity": "Time O(n), space O(n). There is also a O(1)-extra-space slope-tracking variant.",
        },
        "deep_concept": r'''
A neighbor-pair constraint factors cleanly into 'satisfy left' and
'satisfy right' independently. Taking the max of the two per-direction
solutions satisfies both simultaneously and is optimal because any
valid assignment must dominate each direction's minimum.
''',
        "confusion_notes": [
            {
                "question": "Why does `max(left, right)` give the *minimum* total?",
                "answer": "Because `left[i]` is the smallest value satisfying the left-side constraint at i, and similarly for right. Any valid assignment must be ≥ left[i] and ≥ right[i] at each position, so ≥ max of the two. Taking exactly max is feasible (both directional constraints hold) and minimal.",
            },
        ],
        "summary": "Two passes, take per-position max. left[i] handles left neighbor, right[i] handles right neighbor.",
    },

    # ------------------------------------------------------------------
    # 11) Restore IP Addresses
    # ------------------------------------------------------------------
    {
        "id": "ip-address-restoration",
        "title": "Restore IP Addresses",
        "step_id": 12,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["backtracking", "strings"],
        "what_this_teaches": "Bounded backtracking: try every split into 4 segments with length pruning and validation.",
        "pattern": "Backtracking with early constraints.",
        "prerequisite_lessons": ["recursion"],
        "prerequisite_problems": [],
        "next_problems": ["insert-intervals"],
        "resources": [
            _lc(93, "restore-ip-addresses"),
            _SHEET,
        ],
        "understanding": r'''
Given a string of digits `s`, return all valid IP address forms. A
valid IP consists of 4 integers each in `[0, 255]` and *without leading
zeros* (unless the integer itself is 0).

**Example:** `s = "25525511135"` → `["255.255.11.135", "255.255.111.35"]`.
''',
        "brute_force": {
            "explanation": r'''
Try every triple of split points (positions 1..n-1 of three dots),
validate. O(n³) splits, each validation O(n). Fine for n ≤ 12.
''',
            "code": r'''
def restore_ip_brute(s):
    n = len(s)
    out = []
    def valid(seg):
        return seg and (seg == "0" or (seg[0] != "0" and int(seg) <= 255))
    for i in range(1, min(n - 2, 4)):
        for j in range(i + 1, min(n - 1, i + 4)):
            for k in range(j + 1, min(n, j + 4)):
                parts = [s[:i], s[i:j], s[j:k], s[k:]]
                if all(valid(p) for p in parts):
                    out.append(".".join(parts))
    return out
''',
            "complexity": "Time O(1) — at most 81 candidates; the input is bounded to ≤ 12 digits.",
        },
        "thought_process": r'''
A backtracking version is cleaner: at each step pick the next segment
(of length 1, 2, or 3), validate, recurse with one fewer segment
remaining. Prune by remaining length: if `remaining_segments * 3 <
remaining_length` we can't fit; if `remaining_segments > remaining_length`
we can't fill.
''',
        "optimized": {
            "explanation": r'''
Backtracking with length pruning.
''',
            "code": r'''
def restore_ip(s):
    out = []
    def back(i, parts):
        if len(parts) == 4:
            if i == len(s):
                out.append(".".join(parts))
            return
        for L in (1, 2, 3):
            if i + L > len(s):
                break
            seg = s[i:i + L]
            if (L > 1 and seg[0] == '0') or int(seg) > 255:
                continue
            back(i + L, parts + [seg])
    back(0, [])
    return out
''',
            "complexity": "Time O(1) — bounded recursion tree (each of 4 segments has ≤ 3 choices).",
        },
        "deep_concept": r'''
Backtracking with constant depth (here 4) is effectively brute-force
enumeration with cheap pruning. Recognize problems where the branching
factor is small (3) and the depth is fixed (4) — those are perfect for
backtracking.
''',
        "confusion_notes": [
            {
                "question": "Why is `(L > 1 and seg[0] == '0')` the leading-zero check?",
                "answer": "Because '0' alone is valid (the integer 0), but '00', '01', '012' are not — they have an unnecessary leading zero. Only reject when L > 1 *and* starts with '0'.",
            },
        ],
        "summary": "Backtrack over segment lengths 1..3, four segments total, validate each segment is in [0, 255] with no extra leading zero.",
    },

    # ------------------------------------------------------------------
    # 12) Insert Interval
    # ------------------------------------------------------------------
    {
        "id": "insert-intervals",
        "title": "Insert Interval",
        "step_id": 12,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["intervals", "greedy"],
        "what_this_teaches": "Sweep through sorted intervals: copy non-overlapping ones, merge the overlapping band into one interval, copy the rest.",
        "pattern": "Three-phase scan: before / merge / after.",
        "prerequisite_lessons": ["intervals"],
        "prerequisite_problems": ["n-meetings"],
        "next_problems": ["merge-intervals"],
        "resources": [
            _lc(57, "insert-interval"),
            _SHEET,
        ],
        "understanding": r'''
Given a sorted list of non-overlapping intervals and a new interval,
insert it into the list and merge if necessary.
''',
        "brute_force": {
            "explanation": r'''
Append the new interval, sort, then merge. O(n log n).
''',
            "code": r'''
def insert_brute(intervals, new):
    intervals = intervals + [new]
    intervals.sort()
    out = []
    for s, e in intervals:
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out
''',
            "complexity": "Time O(n log n).",
        },
        "thought_process": r'''
Since the input is already sorted, we can do it in O(n):
1. Copy all intervals that end *before* the new one starts.
2. While the current interval *overlaps* the new one, merge it into
   the new one (expand new's start/end).
3. Append the merged new interval.
4. Copy the rest.
''',
        "optimized": {
            "explanation": r'''
Single linear pass.
''',
            "code": r'''
def insert(intervals, new):
    out = []
    i, n = 0, len(intervals)
    # phase 1: copy ones that end strictly before new starts
    while i < n and intervals[i][1] < new[0]:
        out.append(intervals[i])
        i += 1
    # phase 2: merge overlapping
    while i < n and intervals[i][0] <= new[1]:
        new = [min(new[0], intervals[i][0]), max(new[1], intervals[i][1])]
        i += 1
    out.append(new)
    # phase 3: copy the rest
    while i < n:
        out.append(intervals[i])
        i += 1
    return out
''',
            "complexity": "Time O(n), space O(n) for output.",
        },
        "deep_concept": r'''
The three-phase scan is a clean idiom when the input is already sorted
and you need to insert/replace a contiguous region: copy untouched
prefix, process the middle, copy untouched suffix.
''',
        "confusion_notes": [
            {
                "question": "Why is the merge condition `intervals[i][0] <= new[1]` and not `<`?",
                "answer": "Because touching intervals like [1, 3] and [3, 5] should merge into [1, 5] in this problem's convention. The `<=` includes the touching case.",
            },
        ],
        "summary": "Three-phase scan: untouched prefix, merge phase, untouched suffix.",
    },

    # ------------------------------------------------------------------
    # 13) Merge Intervals
    # ------------------------------------------------------------------
    {
        "id": "merge-intervals",
        "title": "Merge Intervals",
        "step_id": 12,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["intervals", "sorting"],
        "what_this_teaches": "Sort by start, then walk and merge with the last accepted interval.",
        "pattern": "Sort + linear merge.",
        "prerequisite_lessons": ["intervals", "sorting"],
        "prerequisite_problems": ["n-meetings", "insert-intervals"],
        "next_problems": ["non-overlapping-intervals"],
        "resources": [
            _lc(56, "merge-intervals"),
            _SHEET,
        ],
        "understanding": r'''
Given a list of intervals, merge all overlapping ones.

**Example:** `[[1,3], [2,6], [8,10], [15,18]]` → `[[1,6], [8,10], [15,18]]`.
''',
        "brute_force": {
            "explanation": r'''
Iteratively merge any overlapping pair until no overlap remains. O(n²)
or worse.
''',
            "code": r'''
# Skipped — sort + sweep is clearly the right approach.
''',
            "complexity": "—",
        },
        "thought_process": r'''
Sort by start time. Walk; for each interval, either extend the last
accepted one (if overlapping) or append a fresh entry.
''',
        "optimized": {
            "explanation": r'''
Sort + one pass.
''',
            "code": r'''
def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    out = []
    for s, e in intervals:
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out
''',
            "complexity": "Time O(n log n), space O(n).",
        },
        "deep_concept": r'''
After sorting by start, an interval `(s, e)` overlaps the last accepted
one `(S, E)` iff `s ≤ E`. The merge extends only the *right* edge; the
left edge is fixed by sort order.
''',
        "confusion_notes": [
            {
                "question": "Should I use `<` or `<=` for the overlap check?",
                "answer": "`<=` if touching intervals like [1,3] and [3,5] should merge; `<` if they shouldn't. The LeetCode version uses `<=`.",
            },
        ],
        "summary": "Sort by start; extend the last interval if start ≤ last_end, else append.",
    },

    # ------------------------------------------------------------------
    # 14) Non-overlapping Intervals
    # ------------------------------------------------------------------
    {
        "id": "non-overlapping-intervals",
        "title": "Non-overlapping Intervals",
        "step_id": 12,
        "lecture_id": 2,
        "difficulty": "medium",
        "tags": ["intervals", "greedy"],
        "what_this_teaches": "Remove the *fewest* intervals to make the rest non-overlapping. Sort by end + greedy keep.",
        "pattern": "Earliest-finish-time-first (same as N Meetings).",
        "prerequisite_lessons": ["intervals", "greedy"],
        "prerequisite_problems": ["n-meetings", "merge-intervals"],
        "next_problems": ["sjf-scheduling"],
        "resources": [
            _lc(435, "non-overlapping-intervals"),
            _SHEET,
        ],
        "understanding": r'''
Given a list of intervals, return the *minimum number* you must remove
so that the rest don't overlap.

**Example:** `[[1,2], [2,3], [3,4], [1,3]]` → remove 1 (the [1,3]).
''',
        "brute_force": {
            "explanation": r'''
Enumerate subsets to remove, check if the remainder is non-overlapping.
Exponential.
''',
            "code": r'''
# Exponential — skipped.
''',
            "complexity": "—",
        },
        "thought_process": r'''
This is the *complement* of "Max non-overlapping intervals". The
greedy: sort by end time, keep an interval iff it starts ≥ the last
kept end. Removals = total − kept.
''',
        "optimized": {
            "explanation": r'''
Sort by end, greedy keep.
''',
            "code": r'''
def erase_overlap_intervals(intervals):
    intervals.sort(key=lambda x: x[1])
    kept = 0
    last_end = float('-inf')
    for s, e in intervals:
        if s >= last_end:
            kept += 1
            last_end = e
    return len(intervals) - kept
''',
            "complexity": "Time O(n log n), space O(1).",
        },
        "deep_concept": r'''
Maximum non-overlapping subset = sort-by-end greedy. Minimum to remove
= total − max non-overlapping. Both rely on the same exchange argument
that picking the earliest-finishing leaves the most room.
''',
        "confusion_notes": [
            {
                "question": "Why `s >= last_end` (with `>=`) here but `s > last_end` in N Meetings?",
                "answer": "Because LeetCode 435 treats touching intervals (like [1, 2] and [2, 3]) as non-overlapping (`>=` allows touch). Striver's N Meetings treats touching as conflict. Read the problem statement carefully.",
            },
        ],
        "summary": "Sort by end, greedy-keep when `start >= last_end`. Removals = n − kept.",
    },

    # ------------------------------------------------------------------
    # 15) Shortest Job First (SJF) Scheduling
    # ------------------------------------------------------------------
    {
        "id": "sjf-scheduling",
        "title": "Shortest Job First (SJF) Scheduling",
        "step_id": 12,
        "lecture_id": 2,
        "difficulty": "easy",
        "tags": ["greedy", "sorting", "scheduling"],
        "what_this_teaches": "Minimize average waiting time by running shortest jobs first.",
        "pattern": "Sort by burst time.",
        "prerequisite_lessons": ["sorting", "greedy"],
        "prerequisite_problems": [],
        "next_problems": [],
        "resources": [
            {"label": "GFG — SJF Scheduling", "url": "https://www.geeksforgeeks.org/program-for-shortest-job-first-or-sjf-cpu-scheduling-set-1-non-preemptive/"},
            _SHEET,
        ],
        "understanding": r'''
Given burst times of N jobs all arriving at time 0, run them on a
single CPU to minimize the *average waiting time*. The waiting time of
a job is the time it spends in the queue before getting CPU.
''',
        "brute_force": {
            "explanation": r'''
Try every permutation, compute total waiting time. O(n!).
''',
            "code": r'''
# Skipped — exponential.
''',
            "complexity": "—",
        },
        "thought_process": r'''
**Greedy by burst time ascending.** Sort jobs by burst time; the first
job has 0 wait, the second waits for the first's burst, etc. Total wait
is a prefix sum.

**Why optimal?** Exchange argument: if you ran a longer job before a
shorter one, swapping them reduces the total wait by `(long − short) * (n − k)`,
where `n − k` is the number of jobs after them. So any optimum places
the shortest first.
''',
        "optimized": {
            "explanation": r'''
Sort by burst, accumulate.
''',
            "code": r'''
def sjf_average_wait(bursts):
    bursts = sorted(bursts)
    wait_total = 0
    elapsed = 0
    for b in bursts:
        wait_total += elapsed
        elapsed += b
    return wait_total / len(bursts)
''',
            "complexity": "Time O(n log n), space O(1).",
        },
        "deep_concept": r'''
SJF is a textbook example of operating system scheduling. In practice
SJF is *not* implementable directly (we don't know burst times in
advance), but the principle 'short jobs first' motivates approximations
like Multilevel Feedback Queue.
''',
        "confusion_notes": [
            {
                "question": "Does SJF also minimize turnaround time?",
                "answer": "Yes, on identical arrival times. Turnaround = wait + burst, and since burst sum is fixed, minimizing wait minimizes turnaround. On varying arrival times the picture is more complex (preemptive SRTF).",
            },
        ],
        "summary": "Sort by burst ascending; cumulative wait is the running prefix sum. Average = total wait / n.",
    },
]
