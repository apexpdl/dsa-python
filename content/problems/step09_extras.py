"""Step 9 extras — stacks and queues."""
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
    # ============ Lecture 1 — Implementations ============
    {"id": "stack-using-arrays", "title": "Implement Stack Using Arrays",
     "step_id": 9, "lecture_id": 1, "difficulty": "easy",
     "tags": ["stack", "implementation"],
     "what_this_teaches": "How a stack is implemented internally with a fixed-size array + top index.",
     "pattern": "Array + top pointer; push increments, pop decrements.",
     "prerequisite_lessons": ["stacks"],
     "prerequisite_problems": [], "next_problems": ["queue-using-arrays"],
     "resources": [_SHEET],
     "understanding": "Implement a stack with a fixed-size array. Track `top` as the index of the most recent push.",
     "optimized": {
         "explanation": "Array + top index.",
         "code": r'''class ArrayStack:
    def __init__(self, capacity: int):
        self.data = [0] * capacity
        self.top = -1
        self.cap = capacity
    def push(self, x):
        if self.top + 1 >= self.cap:
            raise OverflowError
        self.top += 1
        self.data[self.top] = x
    def pop(self):
        if self.top < 0:
            raise IndexError
        x = self.data[self.top]
        self.top -= 1
        return x
    def peek(self):
        if self.top < 0:
            raise IndexError
        return self.data[self.top]
    def is_empty(self):
        return self.top == -1
''',
         "complexity": "**All ops O(1)**. **Space**: *O(capacity)*."
     },
     "summary": "**Pattern**: array + top index for O(1) stack ops."},

    {"id": "queue-using-arrays", "title": "Implement Queue Using Arrays (Circular)",
     "step_id": 9, "lecture_id": 1, "difficulty": "easy",
     "tags": ["queue", "implementation"],
     "what_this_teaches": "Circular buffer implementation: head and tail indices wrap around modulo capacity.",
     "pattern": "Two indices (head, tail) and a size counter.",
     "prerequisite_lessons": ["queues"],
     "prerequisite_problems": ["stack-using-arrays"], "next_problems": ["stack-using-queue", "queue-using-stack"],
     "resources": [_SHEET],
     "understanding": "Fixed-size circular buffer. head points at the next element to dequeue; tail at the next empty slot.",
     "optimized": {
         "explanation": "Circular buffer.",
         "code": r'''class ArrayQueue:
    def __init__(self, capacity: int):
        self.data = [0] * capacity
        self.head = 0
        self.tail = 0
        self.size = 0
        self.cap = capacity
    def enqueue(self, x):
        if self.size == self.cap:
            raise OverflowError
        self.data[self.tail] = x
        self.tail = (self.tail + 1) % self.cap
        self.size += 1
    def dequeue(self):
        if self.size == 0:
            raise IndexError
        x = self.data[self.head]
        self.head = (self.head + 1) % self.cap
        self.size -= 1
        return x
''',
         "complexity": "**All ops O(1)**. **Space**: *O(capacity)*."
     },
     "summary": "**Pattern**: circular buffer with head/tail/size."},

    {"id": "stack-using-queue", "title": "Implement Stack Using a Single Queue",
     "step_id": 9, "lecture_id": 1, "difficulty": "easy",
     "tags": ["stack", "queue"],
     "what_this_teaches": "After every push, rotate the queue so the new element is at the front. Then pop = dequeue from front.",
     "pattern": "Push: enqueue then rotate.",
     "prerequisite_lessons": ["stacks", "queues"],
     "prerequisite_problems": ["queue-using-arrays"], "next_problems": ["queue-using-stack"],
     "resources": [_SHEET, _lc(225, "implement-stack-using-queues")],
     "understanding": "Use one queue. After each push, rotate (dequeue and re-enqueue) every prior element. Stack pop = queue dequeue.",
     "optimized": {
         "explanation": "Push-then-rotate.",
         "code": r'''from collections import deque

class StackFromQueue:
    def __init__(self):
        self.q = deque()
    def push(self, x):
        self.q.append(x)
        # Rotate everyone except the just-added element to the back.
        for _ in range(len(self.q) - 1):
            self.q.append(self.q.popleft())
    def pop(self):
        return self.q.popleft()
    def top(self):
        return self.q[0]
    def empty(self):
        return not self.q
''',
         "complexity": "**Push**: *O(n)*. **Pop/top**: *O(1)*."
     },
     "summary": "**Pattern**: push + rotate makes the queue's front behave like a stack's top."},

    {"id": "queue-using-stack", "title": "Implement Queue Using Two Stacks",
     "step_id": 9, "lecture_id": 1, "difficulty": "easy",
     "tags": ["stack", "queue"],
     "what_this_teaches": "Two stacks (in, out): push to in; on pop, if out is empty, transfer all from in to out.",
     "pattern": "Amortized O(1) per op via two-stack trick.",
     "prerequisite_lessons": ["stacks", "queues"],
     "prerequisite_problems": ["stack-using-queue"], "next_problems": ["stack-using-ll"],
     "resources": [_SHEET, _lc(232, "implement-queue-using-stacks")],
     "understanding": "Push to in_stack. On dequeue/peek, if out_stack is empty, drain in_stack into out_stack (which reverses order). Then pop from out_stack.",
     "optimized": {
         "explanation": "Two stacks with lazy transfer.",
         "code": r'''class QueueFromStacks:
    def __init__(self):
        self.in_stack = []
        self.out_stack = []
    def push(self, x):
        self.in_stack.append(x)
    def pop(self):
        self._fill_out()
        return self.out_stack.pop()
    def peek(self):
        self._fill_out()
        return self.out_stack[-1]
    def empty(self):
        return not self.in_stack and not self.out_stack
    def _fill_out(self):
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())
''',
         "complexity": "**Amortized O(1)** per op."
     },
     "summary": "**Pattern**: two stacks with lazy transfer."},

    {"id": "stack-using-ll", "title": "Implement Stack Using Linked List",
     "step_id": 9, "lecture_id": 1, "difficulty": "easy",
     "tags": ["stack", "linked-list"],
     "what_this_teaches": "Linked list as stack: head = top; push/pop on the head.",
     "pattern": "Push: new node points at old head, becomes new head. Pop: head = head.next.",
     "prerequisite_lessons": ["stacks", "linked-lists"],
     "prerequisite_problems": ["queue-using-stack"], "next_problems": ["queue-using-ll"],
     "resources": [_SHEET],
     "understanding": "Use a singly linked list. The head represents the top of the stack. Push and pop are O(1).",
     "optimized": {
         "explanation": "Linked list with head pointer.",
         "code": r'''class StackLL:
    class Node:
        def __init__(self, val, next=None):
            self.val = val
            self.next = next
    def __init__(self):
        self.head = None
    def push(self, x):
        self.head = self.Node(x, self.head)
    def pop(self):
        if self.head is None:
            raise IndexError
        val = self.head.val
        self.head = self.head.next
        return val
    def peek(self):
        if self.head is None:
            raise IndexError
        return self.head.val
''',
         "complexity": "**All ops O(1)**. No fixed capacity."
     },
     "summary": "**Pattern**: linked list with head pointer for O(1) push/pop."},

    {"id": "queue-using-ll", "title": "Implement Queue Using Linked List",
     "step_id": 9, "lecture_id": 1, "difficulty": "easy",
     "tags": ["queue", "linked-list"],
     "what_this_teaches": "Linked list with head and tail pointers; enqueue at tail, dequeue at head.",
     "pattern": "Two-pointer linked list.",
     "prerequisite_lessons": ["queues", "linked-lists"],
     "prerequisite_problems": ["stack-using-ll"], "next_problems": ["min-stack"],
     "resources": [_SHEET],
     "understanding": "Singly linked list with head and tail. Enqueue at tail (head used for empty-check); dequeue at head (rewire head, handle tail=None case).",
     "optimized": {
         "explanation": "Two-pointer linked list.",
         "code": r'''class QueueLL:
    class Node:
        def __init__(self, val, next=None):
            self.val = val
            self.next = next
    def __init__(self):
        self.head = self.tail = None
    def enqueue(self, x):
        node = self.Node(x)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
    def dequeue(self):
        if self.head is None:
            raise IndexError
        val = self.head.val
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return val
''',
         "complexity": "**All ops O(1)**."
     },
     "summary": "**Pattern**: linked list with head + tail for O(1) FIFO."},

    {"id": "min-stack", "title": "Min Stack",
     "step_id": 9, "lecture_id": 1, "difficulty": "medium",
     "tags": ["stack"],
     "what_this_teaches": "A parallel stack of running minimums lets us return getMin() in O(1).",
     "pattern": "Two stacks: main and min. Push to min only if new value <= current min.",
     "prerequisite_lessons": ["stacks"],
     "prerequisite_problems": ["balanced-parentheses"], "next_problems": [],
     "resources": [_SHEET, _lc(155, "min-stack")],
     "understanding": "Support push/pop/top/getMin all in O(1). Use a parallel 'min stack' that stores the running minimum.",
     "optimized": {
         "explanation": "Main stack + parallel min stack.",
         "code": r'''class MinStack:
    def __init__(self):
        self.stack = []
        self.mins = []  # running minimum at each level
    def push(self, x):
        self.stack.append(x)
        self.mins.append(x if not self.mins else min(x, self.mins[-1]))
    def pop(self):
        self.stack.pop()
        self.mins.pop()
    def top(self):
        return self.stack[-1]
    def getMin(self):
        return self.mins[-1]
''',
         "complexity": "**All ops O(1)**. **Space**: *O(n)*."
     },
     "summary": "**Pattern**: parallel min-stack tracks the running minimum."},

    # ============ Lecture 2 — Conversions (6 problems) ============
    {"id": "infix-to-postfix", "title": "Infix to Postfix Conversion",
     "step_id": 9, "lecture_id": 2, "difficulty": "medium",
     "tags": ["stack", "expressions"],
     "what_this_teaches": "Shunting-yard algorithm: read infix left-to-right; output operands immediately; push operators to a stack with precedence-based popping.",
     "pattern": "Operators stack; pop higher-or-equal precedence on each new operator.",
     "prerequisite_lessons": ["stacks"],
     "prerequisite_problems": [], "next_problems": ["postfix-to-infix", "infix-to-prefix"],
     "resources": [_SHEET, {"label": "Wikipedia — Shunting-yard",
                            "url": "https://en.wikipedia.org/wiki/Shunting-yard_algorithm"}],
     "understanding": "Convert infix (a + b * c) to postfix (a b c * +). Dijkstra's shunting-yard algorithm.",
     "optimized": {
         "explanation": "Shunting-yard.",
         "code": r'''def infix_to_postfix(expr: str) -> str:
    prec = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    output = []
    stack = []
    for ch in expr:
        if ch.isalnum():
            output.append(ch)
        elif ch == '(':
            stack.append(ch)
        elif ch == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # remove '('
        else:  # operator
            while stack and stack[-1] != '(' and prec.get(stack[-1], 0) >= prec[ch]:
                output.append(stack.pop())
            stack.append(ch)
    while stack:
        output.append(stack.pop())
    return ''.join(output)
''',
         "complexity": "**Time**: *O(n)*. **Space**: *O(n)*."
     },
     "summary": "**Pattern**: shunting-yard — output operands, stack operators with precedence-based popping."},

    {"id": "infix-to-prefix", "title": "Infix to Prefix Conversion",
     "step_id": 9, "lecture_id": 2, "difficulty": "medium",
     "tags": ["stack", "expressions"],
     "what_this_teaches": "Reverse the infix, convert to postfix (with adjusted operator handling), reverse the result.",
     "pattern": "Reverse → infix-to-postfix-variant → reverse.",
     "prerequisite_lessons": ["stacks"],
     "prerequisite_problems": ["infix-to-postfix"], "next_problems": ["postfix-to-infix", "postfix-to-prefix"],
     "resources": [_SHEET],
     "understanding": "Convert (a + b * c) to (+ a * b c). Approach: reverse infix (swapping brackets), do a postfix-like conversion, reverse the result.",
     "optimized": {
         "explanation": "Reverse-postfix-reverse.",
         "code": r'''def infix_to_prefix(expr: str) -> str:
    # Reverse and swap brackets.
    rev = []
    for ch in reversed(expr):
        if ch == '(': rev.append(')')
        elif ch == ')': rev.append('(')
        else: rev.append(ch)
    rev = ''.join(rev)
    # Convert to postfix using the shunting-yard with strict > for ^ (left-associativity of original).
    prec = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    output = []
    stack = []
    for ch in rev:
        if ch.isalnum():
            output.append(ch)
        elif ch == '(':
            stack.append(ch)
        elif ch == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and stack[-1] != '(' and prec.get(stack[-1], 0) > prec[ch]:
                output.append(stack.pop())
            stack.append(ch)
    while stack:
        output.append(stack.pop())
    return ''.join(reversed(output))
''',
         "complexity": "**Time**: *O(n)*. **Space**: *O(n)*."
     },
     "summary": "**Pattern**: reverse → postfix-style → reverse."},

    {"id": "postfix-to-infix", "title": "Postfix to Infix Conversion",
     "step_id": 9, "lecture_id": 2, "difficulty": "easy",
     "tags": ["stack", "expressions"],
     "what_this_teaches": "Stack of expression-strings: push operands; on operator, pop two and combine.",
     "pattern": "Walk postfix; build expression strings on a stack.",
     "prerequisite_lessons": ["stacks"],
     "prerequisite_problems": ["infix-to-postfix"], "next_problems": ["prefix-to-infix"],
     "resources": [_SHEET],
     "understanding": "Walk the postfix string. For each token: if operand, push the string. If operator, pop two strings, combine as '(left op right)', push.",
     "optimized": {
         "explanation": "Stack of strings.",
         "code": r'''def postfix_to_infix(expr: str) -> str:
    stack = []
    for ch in expr:
        if ch.isalnum():
            stack.append(ch)
        else:
            r = stack.pop()
            l = stack.pop()
            stack.append(f'({l}{ch}{r})')
    return stack[0]
''',
         "complexity": "**Time**: *O(n)*. **Space**: *O(n)*."
     },
     "summary": "**Pattern**: stack of substrings; combine on each operator."},

    {"id": "prefix-to-infix", "title": "Prefix to Infix Conversion",
     "step_id": 9, "lecture_id": 2, "difficulty": "easy",
     "tags": ["stack", "expressions"],
     "what_this_teaches": "Walk prefix right-to-left; stack of expression strings.",
     "pattern": "Right-to-left scan; on operator, pop and combine.",
     "prerequisite_lessons": ["stacks"],
     "prerequisite_problems": ["postfix-to-infix"], "next_problems": ["postfix-to-prefix"],
     "resources": [_SHEET],
     "understanding": "Walk prefix from right to left. For each token: operand → push; operator → pop two, combine as '(left op right)', push.",
     "optimized": {
         "explanation": "Right-to-left scan.",
         "code": r'''def prefix_to_infix(expr: str) -> str:
    stack = []
    for ch in reversed(expr):
        if ch.isalnum():
            stack.append(ch)
        else:
            l = stack.pop()
            r = stack.pop()
            stack.append(f'({l}{ch}{r})')
    return stack[0]
''',
         "complexity": "**Time**: *O(n)*. **Space**: *O(n)*."
     },
     "summary": "**Pattern**: right-to-left walk + stack."},

    {"id": "postfix-to-prefix", "title": "Postfix to Prefix Conversion",
     "step_id": 9, "lecture_id": 2, "difficulty": "easy",
     "tags": ["stack", "expressions"],
     "what_this_teaches": "Stack of expression strings; combine as 'op left right' on each operator.",
     "pattern": "Walk left-to-right; on operator, pop two and prepend.",
     "prerequisite_lessons": ["stacks"],
     "prerequisite_problems": ["postfix-to-infix"], "next_problems": ["prefix-to-postfix"],
     "resources": [_SHEET],
     "understanding": "Walk postfix; on operator, combine as 'op + left + right' (operator first).",
     "optimized": {
         "explanation": "Stack with prefix combining.",
         "code": r'''def postfix_to_prefix(expr: str) -> str:
    stack = []
    for ch in expr:
        if ch.isalnum():
            stack.append(ch)
        else:
            r = stack.pop()
            l = stack.pop()
            stack.append(f'{ch}{l}{r}')
    return stack[0]
''',
         "complexity": "**Time**: *O(n)*. **Space**: *O(n)*."
     },
     "summary": "**Pattern**: stack of strings; operator prefixes the combined operands."},

    {"id": "prefix-to-postfix", "title": "Prefix to Postfix Conversion",
     "step_id": 9, "lecture_id": 2, "difficulty": "easy",
     "tags": ["stack", "expressions"],
     "what_this_teaches": "Right-to-left scan with stack of postfix strings.",
     "pattern": "On operator, pop two and append the operator at the end.",
     "prerequisite_lessons": ["stacks"],
     "prerequisite_problems": ["prefix-to-infix"], "next_problems": [],
     "resources": [_SHEET],
     "understanding": "Walk prefix right-to-left. On operator, pop two, combine as 'left + right + op'.",
     "optimized": {
         "explanation": "Right-to-left with postfix combining.",
         "code": r'''def prefix_to_postfix(expr: str) -> str:
    stack = []
    for ch in reversed(expr):
        if ch.isalnum():
            stack.append(ch)
        else:
            l = stack.pop()
            r = stack.pop()
            stack.append(f'{l}{r}{ch}')
    return stack[0]
''',
         "complexity": "**Time**: *O(n)*. **Space**: *O(n)*."
     },
     "summary": "**Pattern**: right-to-left walk + postfix combining."},

    # ============ Lecture 3 — Monotonic Stack/Queue ============
    {"id": "next-greater-element-ii", "title": "Next Greater Element II (Circular Array)",
     "step_id": 9, "lecture_id": 3, "difficulty": "medium",
     "tags": ["stack", "monotonic-stack", "circular"],
     "what_this_teaches": "For a circular array, simulate two passes by iterating index 0..2n-1, using mod n for actual indexing.",
     "pattern": "Same as next-greater-element-i, with 2n iterations and indices mod n.",
     "prerequisite_lessons": ["stacks"],
     "prerequisite_problems": ["next-greater-element-i"], "next_problems": ["next-smaller-element"],
     "resources": [_SHEET, _lc(503, "next-greater-element-ii")],
     "understanding": "Circular variant: after the last element, wrap around. Simulate by iterating index 0..2n-1; use mod n to index into the array.",
     "optimized": {
         "explanation": "Iterate twice the length.",
         "code": r'''def next_greater_circular(nums: list[int]) -> list[int]:
    n = len(nums)
    result = [-1] * n
    stack = []
    for i in range(2 * n):
        idx = i % n
        while stack and nums[stack[-1]] < nums[idx]:
            result[stack.pop()] = nums[idx]
        if i < n:
            stack.append(idx)
    return result
''',
         "complexity": "**Time**: *O(n)*. **Space**: *O(n)*."
     },
     "summary": "**Pattern**: iterate 2n with mod n indexing."},

    {"id": "next-smaller-element", "title": "Next Smaller Element",
     "step_id": 9, "lecture_id": 3, "difficulty": "easy",
     "tags": ["stack", "monotonic-stack"],
     "what_this_teaches": "Same monotonic-stack pattern as next-greater but flip the comparison; the stack is increasing instead of decreasing.",
     "pattern": "Stack of increasing values; pop when current is smaller.",
     "prerequisite_lessons": ["stacks"],
     "prerequisite_problems": ["next-greater-element-i"], "next_problems": ["count-nges-right", "sum-subarray-minimums"],
     "resources": [_SHEET],
     "understanding": "Find the next smaller element on the right for each index. Flip the comparison from next-greater.",
     "optimized": {
         "explanation": "Monotonic increasing stack.",
         "code": r'''def next_smaller(nums: list[int]) -> list[int]:
    n = len(nums)
    result = [-1] * n
    stack = []
    for i in range(n):
        while stack and nums[stack[-1]] > nums[i]:
            result[stack.pop()] = nums[i]
        stack.append(i)
    return result
''',
         "complexity": "**Time**: *O(n)*. **Space**: *O(n)*."
     },
     "summary": "**Pattern**: monotonic increasing stack of indices."},

    {"id": "count-nges-right", "title": "Count of Next Greater Elements to the Right",
     "step_id": 9, "lecture_id": 3, "difficulty": "hard",
     "tags": ["stack", "monotonic-stack", "advanced"],
     "what_this_teaches": "Beyond simple next-greater: count *how many* elements to the right are greater than each. Requires BIT/segment tree or coordinate compression.",
     "pattern": "Offline processing with a sorted structure tracking right-side counts.",
     "prerequisite_lessons": ["stacks"],
     "prerequisite_problems": ["next-greater-element-i"], "next_problems": [],
     "resources": [_SHEET, _lc(315, "count-of-smaller-numbers-after-self")],
     "understanding": "For each element, count strictly-greater elements to its right. Linear scan from the right with a sorted multiset gives O(n log n).",
     "optimized": {
         "explanation": "Right-to-left scan with sorted structure (bisect on a sorted list).",
         "code": r'''import bisect

def count_greater_right(arr: list[int]) -> list[int]:
    n = len(arr)
    result = [0] * n
    sorted_right = []
    for i in range(n - 1, -1, -1):
        # Number of values strictly greater than arr[i] already seen.
        pos = bisect.bisect_right(sorted_right, arr[i])
        result[i] = len(sorted_right) - pos
        bisect.insort(sorted_right, arr[i])
    return result
''',
         "complexity": "**Time**: *O(n²)* worst case due to insort; *O(n log n)* with a BIT. **Space**: *O(n)*."
     },
     "summary": "**Pattern**: right-to-left with a sorted multiset to count greater elements."},

    {"id": "trapping-rain-water", "title": "Trapping Rain Water",
     "step_id": 9, "lecture_id": 3, "difficulty": "hard",
     "tags": ["array", "two-pointers", "stack"],
     "what_this_teaches": "Two-pointer approach: water at index i = min(max_left, max_right) - height[i]. Use two pointers from ends + running maxes.",
     "pattern": "Left/right pointers; track left_max and right_max; add water from the smaller side.",
     "prerequisite_lessons": ["stacks", "two-pointers"],
     "prerequisite_problems": ["next-greater-element-i"], "next_problems": ["largest-rectangle-histogram"],
     "resources": [_SHEET, _lc(42, "trapping-rain-water")],
     "understanding": r'''
For each index, the trapped water is `min(max_left, max_right) -
height[i]`.

Two-pointer trick: from both ends, the side with the smaller max
determines water for that position. Move that pointer inward
while accumulating.

*O(n)* time, *O(1)* space.
''',
     "optimized": {
         "explanation": "Two pointers + running maxes.",
         "code": r'''def trap(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    total = 0
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                total += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                total += right_max - height[right]
            right -= 1
    return total
''',
         "complexity": "**Time**: *O(n)*. **Space**: *O(1)*."
     },
     "summary": "**Pattern**: two pointers + running max from each side; add water from the smaller side."},

    {"id": "sum-subarray-minimums", "title": "Sum of Subarray Minimums",
     "step_id": 9, "lecture_id": 3, "difficulty": "medium",
     "tags": ["stack", "monotonic-stack"],
     "what_this_teaches": "For each element, count how many subarrays have it as the minimum. Sum (element × count).",
     "pattern": "Use prev-smaller and next-smaller indices to compute the 'domain' of each element.",
     "prerequisite_lessons": ["stacks"],
     "prerequisite_problems": ["next-smaller-element"], "next_problems": ["sum-subarray-ranges"],
     "resources": [_SHEET, _lc(907, "sum-of-subarray-minimums")],
     "understanding": "For each element at index i, find the previous-smaller (or equal) on the left and the next-smaller strict on the right. The element is the minimum of (i - left) * (right - i) subarrays. Sum element × count for all.",
     "optimized": {
         "explanation": "Monotonic stack twice.",
         "code": r'''def sum_subarray_mins(arr: list[int]) -> int:
    MOD = 10**9 + 7
    n = len(arr)
    # Previous less (or equal) — left boundary.
    prev_less = [-1] * n
    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] > arr[i]:
            stack.pop()
        prev_less[i] = stack[-1] if stack else -1
        stack.append(i)
    # Next less strict — right boundary.
    next_less = [n] * n
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        next_less[i] = stack[-1] if stack else n
        stack.append(i)
    return sum(arr[i] * (i - prev_less[i]) * (next_less[i] - i) for i in range(n)) % MOD
''',
         "complexity": "**Time**: *O(n)*. **Space**: *O(n)*."
     },
     "summary": "**Pattern**: prev-less and next-less indices = element's 'domain'; sum element × count."},

    {"id": "asteroid-collision", "title": "Asteroid Collision",
     "step_id": 9, "lecture_id": 3, "difficulty": "medium",
     "tags": ["stack", "simulation"],
     "what_this_teaches": "Stack-based collision simulation. Positive (right-moving) on the stack survive until a negative (left-moving) arrives.",
     "pattern": "Stack of surviving asteroids; on a new asteroid, resolve collisions with the top.",
     "prerequisite_lessons": ["stacks"],
     "prerequisite_problems": ["balanced-parentheses"], "next_problems": [],
     "resources": [_SHEET, _lc(735, "asteroid-collision")],
     "understanding": "Positive numbers move right, negative move left. They collide when a negative meets a positive on its right. Use a stack to simulate.",
     "optimized": {
         "explanation": "Stack with collision resolution.",
         "code": r'''def asteroid_collision(asteroids: list[int]) -> list[int]:
    stack = []
    for a in asteroids:
        alive = True
        while alive and a < 0 and stack and stack[-1] > 0:
            if stack[-1] < -a:
                stack.pop()
            elif stack[-1] == -a:
                stack.pop()
                alive = False
            else:
                alive = False
        if alive:
            stack.append(a)
    return stack
''',
         "complexity": "**Time**: *O(n)*. **Space**: *O(n)*."
     },
     "summary": "**Pattern**: stack with collision resolution per new asteroid."},

    {"id": "sum-subarray-ranges", "title": "Sum of Subarray Ranges",
     "step_id": 9, "lecture_id": 3, "difficulty": "medium",
     "tags": ["stack", "monotonic-stack"],
     "what_this_teaches": "Sum of (max - min) over all subarrays = sum-of-maxes - sum-of-mins. Two monotonic-stack passes.",
     "pattern": "sum_of_maxes - sum_of_mins via twin monotonic-stack algorithms.",
     "prerequisite_lessons": ["stacks"],
     "prerequisite_problems": ["sum-subarray-minimums"], "next_problems": [],
     "resources": [_SHEET, _lc(2104, "sum-of-subarray-ranges")],
     "understanding": "Subarray range = max - min. Total = sum_of_maxes - sum_of_mins. Each computed by a monotonic-stack technique similar to sum-of-mins.",
     "optimized": {
         "explanation": "Twin sum-of-extremes via monotonic stacks.",
         "code": r'''def sum_subarray_ranges(arr: list[int]) -> int:
    def sum_with(comparator_max):
        # Sum of subarray extremes based on comparator.
        # comparator_max: pass True for max, False for min.
        n = len(arr)
        prev = [-1] * n
        nxt = [n] * n
        stack = []
        for i in range(n):
            while stack and (arr[stack[-1]] < arr[i] if comparator_max else arr[stack[-1]] > arr[i]):
                nxt[stack.pop()] = i
            prev[i] = stack[-1] if stack else -1
            stack.append(i)
        return sum(arr[i] * (i - prev[i]) * (nxt[i] - i) for i in range(n))

    return sum_with(True) - sum_with(False)
''',
         "complexity": "**Time**: *O(n)*. **Space**: *O(n)*."
     },
     "summary": "**Pattern**: sum-of-maxes minus sum-of-mins via monotonic stacks."},

    {"id": "largest-rectangle-histogram", "title": "Largest Rectangle in Histogram",
     "step_id": 9, "lecture_id": 3, "difficulty": "hard",
     "tags": ["stack", "monotonic-stack"],
     "what_this_teaches": "For each bar, the largest rectangle that includes it has the bar's height and width = (next-smaller - prev-smaller - 1).",
     "pattern": "Monotonic increasing stack; pop on smaller; compute area at the popped index.",
     "prerequisite_lessons": ["stacks"],
     "prerequisite_problems": ["next-smaller-element"], "next_problems": ["maximal-rectangle"],
     "resources": [_SHEET, _lc(84, "largest-rectangle-in-histogram")],
     "understanding": r'''
For each bar h[i], find the largest rectangle with h[i] as the
height. Width = (next-smaller - prev-smaller - 1). Track the
max.

A single monotonic stack pass computes prev-smaller and
next-smaller on the fly.

*O(n)* time and space.
''',
     "optimized": {
         "explanation": "Single monotonic stack pass with sentinels.",
         "code": r'''def largest_rectangle(heights: list[int]) -> int:
    # Append a sentinel 0 to flush the stack at the end.
    heights = heights + [0]
    stack = []
    best = 0
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            top = stack.pop()
            left = stack[-1] if stack else -1
            width = i - left - 1
            best = max(best, heights[top] * width)
        stack.append(i)
    return best
''',
         "complexity": "**Time**: *O(n)*. **Space**: *O(n)*."
     },
     "summary": "**Pattern**: monotonic stack + sentinel 0 to flush remaining bars."},

    {"id": "maximal-rectangle", "title": "Maximal Rectangle in a Binary Matrix",
     "step_id": 9, "lecture_id": 3, "difficulty": "hard",
     "tags": ["stack", "matrix", "dp"],
     "what_this_teaches": "Reduce each row to a histogram of consecutive 1s ending at that row. For each row, run largest-rectangle-in-histogram.",
     "pattern": "Per-row histogram + largest-rectangle-in-histogram.",
     "prerequisite_lessons": ["stacks"],
     "prerequisite_problems": ["largest-rectangle-histogram"], "next_problems": [],
     "resources": [_SHEET, _lc(85, "maximal-rectangle")],
     "understanding": "For each row, build a histogram where heights[j] = consecutive 1s in column j ending at this row. Apply largest-rectangle-in-histogram per row. Track global max.",
     "optimized": {
         "explanation": "Row-by-row histograms.",
         "code": r'''def maximal_rectangle(matrix: list[list[str]]) -> int:
    if not matrix or not matrix[0]:
        return 0
    n = len(matrix[0])
    heights = [0] * n
    best = 0

    def largest_rect_histogram(h):
        h = h + [0]
        stack = []
        result = 0
        for i, x in enumerate(h):
            while stack and h[stack[-1]] > x:
                top = stack.pop()
                left = stack[-1] if stack else -1
                result = max(result, h[top] * (i - left - 1))
            stack.append(i)
        return result

    for row in matrix:
        for j in range(n):
            heights[j] = heights[j] + 1 if row[j] == '1' else 0
        best = max(best, largest_rect_histogram(heights))
    return best
''',
         "complexity": "**Time**: *O(m * n)*. **Space**: *O(n)*."
     },
     "summary": "**Pattern**: row-wise histograms + largest-rectangle-in-histogram per row."},

    {"id": "remove-k-digits", "title": "Remove K Digits to Minimize the Number",
     "step_id": 9, "lecture_id": 3, "difficulty": "medium",
     "tags": ["stack", "monotonic-stack", "greedy"],
     "what_this_teaches": "Greedy with monotonic increasing stack. Pop the top whenever it's greater than the next digit (and we have remaining removals).",
     "pattern": "Monotonic stack with a removal budget.",
     "prerequisite_lessons": ["stacks"],
     "prerequisite_problems": ["next-greater-element-i"], "next_problems": [],
     "resources": [_SHEET, _lc(402, "remove-k-digits")],
     "understanding": r'''
Given a digit string, remove k digits so the resulting number is
smallest.

Greedy with monotonic stack: walk the digits; if the current
digit is smaller than the stack's top and we still have removals
left, pop the top (and decrement k). At the end, if removals
remain, pop from the back. Strip leading zeros.
''',
     "optimized": {
         "explanation": "Monotonic stack + remaining-budget pops.",
         "code": r'''def remove_k_digits(num: str, k: int) -> str:
    stack = []
    for d in num:
        while stack and k > 0 and stack[-1] > d:
            stack.pop()
            k -= 1
        stack.append(d)
    # If k > 0 remaining, remove from the end.
    while k > 0 and stack:
        stack.pop()
        k -= 1
    result = ''.join(stack).lstrip('0')
    return result if result else '0'
''',
         "complexity": "**Time**: *O(n)*. **Space**: *O(n)*."
     },
     "summary": "**Pattern**: monotonic stack + budget; strip leading zeros."},

    {"id": "sliding-window-maximum", "title": "Sliding Window Maximum",
     "step_id": 9, "lecture_id": 3, "difficulty": "hard",
     "tags": ["queue", "deque", "monotonic-deque", "sliding-window"],
     "what_this_teaches": "Monotonic deque: maintain a deque of indices with decreasing values. Front always holds the current max.",
     "pattern": "Pop stale indices from front; pop smaller from back; record front for each window position.",
     "prerequisite_lessons": ["queues", "sliding-window"],
     "prerequisite_problems": ["next-greater-element-i"], "next_problems": ["online-stock-span"],
     "resources": [_SHEET, _lc(239, "sliding-window-maximum")],
     "understanding": r'''
Sliding window of size k; return max of each window. Use a
monotonic-decreasing deque of indices.

For each i:
1. Pop indices from front that are outside the window (< i - k + 1).
2. Pop indices from back whose values are <= arr[i] (they will never be max again).
3. Push i.
4. Once i >= k - 1, the front of the deque is the current max.
''',
     "optimized": {
         "explanation": "Monotonic deque of indices.",
         "code": r'''from collections import deque

def max_sliding_window(arr: list[int], k: int) -> list[int]:
    dq = deque()
    result = []
    for i, x in enumerate(arr):
        # Pop stale indices from front.
        while dq and dq[0] <= i - k:
            dq.popleft()
        # Pop smaller values from back.
        while dq and arr[dq[-1]] < x:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(arr[dq[0]])
    return result
''',
         "complexity": "**Time**: *O(n)*. **Space**: *O(k)*."
     },
     "summary": "**Pattern**: monotonic decreasing deque; front is the window max."},

    # ============ Lecture 4 — Implementations ============
    {"id": "online-stock-span", "title": "Online Stock Span",
     "step_id": 9, "lecture_id": 4, "difficulty": "medium",
     "tags": ["stack", "monotonic-stack", "design"],
     "what_this_teaches": "Stream-based monotonic stack. For each new price, compute the span (number of consecutive previous days with price <=).",
     "pattern": "Stack of (price, span) pairs; pop smaller-or-equal; accumulate spans.",
     "prerequisite_lessons": ["stacks"],
     "prerequisite_problems": ["next-greater-element-i"], "next_problems": ["celebrity-problem"],
     "resources": [_SHEET, _lc(901, "online-stock-span")],
     "understanding": "For each `next(price)` call, return the span — the count of consecutive previous days (including today) with price <= today.",
     "optimized": {
         "explanation": "Monotonic stack of (price, span) pairs.",
         "code": r'''class StockSpanner:
    def __init__(self):
        self.stack = []  # (price, span)
    def next(self, price: int) -> int:
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack.pop()[1]
        self.stack.append((price, span))
        return span
''',
         "complexity": "**Amortized O(1)** per next call."
     },
     "summary": "**Pattern**: monotonic stack of (price, span); accumulate spans on pop."},

    {"id": "celebrity-problem", "title": "The Celebrity Problem",
     "step_id": 9, "lecture_id": 4, "difficulty": "medium",
     "tags": ["stack", "elimination"],
     "what_this_teaches": "Elimination via the 'knows' relation. Two-pointer / stack approach narrows to a candidate, then verifies.",
     "pattern": "Use 'knows(a, b)' to eliminate one of two candidates per query.",
     "prerequisite_lessons": ["stacks"],
     "prerequisite_problems": [], "next_problems": [],
     "resources": [_SHEET, _lc(277, "find-the-celebrity")],
     "understanding": "A celebrity is known by everyone but knows no one. Use the knows(a,b) query: if a knows b, a is not the celebrity; else b is not.",
     "optimized": {
         "explanation": "Two-pointer elimination.",
         "code": r'''def find_celebrity(knows, n: int) -> int:
    # Phase 1: find a candidate.
    candidate = 0
    for i in range(1, n):
        if knows(candidate, i):
            candidate = i
    # Phase 2: verify.
    for i in range(n):
        if i != candidate and (knows(candidate, i) or not knows(i, candidate)):
            return -1
    return candidate
''',
         "complexity": "**Time**: *O(n)*. **Space**: *O(1)*."
     },
     "summary": "**Pattern**: candidate-then-verify elimination."},

    {"id": "lru-cache", "title": "LRU Cache",
     "step_id": 9, "lecture_id": 4, "difficulty": "medium",
     "tags": ["linked-list", "design", "hashing"],
     "what_this_teaches": "Doubly linked list + hash map for O(1) get/put with eviction of the least-recently-used item.",
     "pattern": "Hash map of key→node, DLL for recency.",
     "prerequisite_lessons": ["linked-lists", "hashing"],
     "prerequisite_problems": ["dll-introduction"], "next_problems": ["lfu-cache"],
     "resources": [_SHEET, _lc(146, "lru-cache")],
     "understanding": "Maintain a DLL of nodes in access order (most-recent at head). Hash map gives O(1) lookup. On access/put, move to head. On eviction, remove tail.",
     "optimized": {
         "explanation": "Hash map + DLL.",
         "code": r'''class LRUCache:
    class Node:
        __slots__ = ('key', 'val', 'prev', 'next')
        def __init__(self, key, val):
            self.key = key; self.val = val
            self.prev = None; self.next = None

    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}  # key -> Node
        self.head = self.Node(0, 0)  # sentinel
        self.tail = self.Node(0, 0)  # sentinel
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_head(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_head(node)
            return node.val
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._remove(node)
            self._add_to_head(node)
            return
        if len(self.cache) >= self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
        new_node = self.Node(key, value)
        self.cache[key] = new_node
        self._add_to_head(new_node)
''',
         "complexity": "**get/put O(1)**. **Space**: *O(capacity)*."
     },
     "summary": "**Pattern**: hash map + DLL = O(1) LRU cache."},

    {"id": "lfu-cache", "title": "LFU Cache",
     "step_id": 9, "lecture_id": 4, "difficulty": "hard",
     "tags": ["linked-list", "design", "hashing"],
     "what_this_teaches": "Two-dim structure: hash maps for key→node and freq→DLL. On access, move node to next frequency's DLL.",
     "pattern": "Per-frequency LRU lists; min-freq tracker.",
     "prerequisite_lessons": ["linked-lists", "hashing"],
     "prerequisite_problems": ["lru-cache"], "next_problems": [],
     "resources": [_SHEET, _lc(460, "lfu-cache")],
     "understanding": "LFU evicts the least-frequently-used. Maintain a DLL per frequency. On access, increment freq and move the node to that freq's DLL head. Track the min frequency for eviction.",
     "optimized": {
         "explanation": "Per-frequency DLLs + min-freq tracker.",
         "code": r'''from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.size = 0
        self.min_freq = 0
        self.key_to_val = {}   # key -> (val, freq)
        self.freq_to_keys = defaultdict(OrderedDict)  # freq -> ordered dict of keys (LRU within freq)

    def _bump(self, key):
        val, freq = self.key_to_val[key]
        del self.freq_to_keys[freq][key]
        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if self.min_freq == freq:
                self.min_freq += 1
        self.key_to_val[key] = (val, freq + 1)
        self.freq_to_keys[freq + 1][key] = None

    def get(self, key: int) -> int:
        if key not in self.key_to_val:
            return -1
        self._bump(key)
        return self.key_to_val[key][0]

    def put(self, key: int, value: int) -> None:
        if self.cap == 0:
            return
        if key in self.key_to_val:
            val, freq = self.key_to_val[key]
            self.key_to_val[key] = (value, freq)
            self._bump(key)
            return
        if self.size >= self.cap:
            # Evict LRU of min frequency.
            evict_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            del self.key_to_val[evict_key]
            self.size -= 1
        self.key_to_val[key] = (value, 1)
        self.freq_to_keys[1][key] = None
        self.min_freq = 1
        self.size += 1
''',
         "complexity": "**get/put O(1)**. **Space**: *O(capacity)*."
     },
     "summary": "**Pattern**: per-frequency LRU + min-freq tracker."},
]
